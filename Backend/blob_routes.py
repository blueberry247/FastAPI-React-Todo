from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from azure.storage.blob import ContentSettings

import auth
from blob_storage import get_container_client

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


def get_user_id_from_claims(claims: dict) -> int:
    user_id = claims.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in again to refresh your access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)


# ---------------------------------------------------------
# Upload file
# ---------------------------------------------------------

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    claims: dict = Depends(auth.get_current_token_claims),
):
    """
    Upload a file to Azure Blob Storage.

    The user's ID is included in the blob path so each user
    has their own folder inside the taskapp-files container.
    """

    try:
        container_client = get_container_client()

        blob_name = f"{get_user_id_from_claims(claims)}/{file.filename}"

        blob_client = container_client.get_blob_client(blob_name)

        await file.seek(0)

        blob_client.upload_blob(
            file.file,
            overwrite=True,
            content_settings=ContentSettings(content_type=file.content_type),
        )

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "blob_name": blob_name,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(exc)}",
        ) from exc


# ---------------------------------------------------------
# List files
# ---------------------------------------------------------

@router.get("/")
def list_files(
    claims: dict = Depends(auth.get_current_token_claims),
):
    """
    List files belonging to the authenticated user.
    """

    try:
        container_client = get_container_client()

        prefix = f"{get_user_id_from_claims(claims)}/"

        blobs = container_client.list_blobs(
            name_starts_with=prefix
        )

        return [
            {
                "filename": blob.name[len(prefix):],
                "blob_name": blob.name,
                "size": blob.size,
            }
            for blob in blobs
        ]

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not list files: {str(exc)}",
        ) from exc


# ---------------------------------------------------------
# Download file
# ---------------------------------------------------------

@router.get("/{filename}")
def download_file(
    filename: str,
    claims: dict = Depends(auth.get_current_token_claims),
):
    """
    Download one of the authenticated user's files.
    """

    try:
        container_client = get_container_client()

        blob_name = f"{get_user_id_from_claims(claims)}/{filename}"

        blob_client = container_client.get_blob_client(blob_name)

        downloader = blob_client.download_blob()

        return StreamingResponse(
            downloader.chunks(),
            media_type=downloader.properties.content_settings.content_type
            or "application/octet-stream",
            headers={
                "Content-Disposition":
                    f'attachment; filename="{filename}"'
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {str(exc)}",
        ) from exc


# ---------------------------------------------------------
# Delete file
# ---------------------------------------------------------

@router.delete("/{filename}")
def delete_file(
    filename: str,
    claims: dict = Depends(auth.get_current_token_claims),
):
    """
    Delete one of the authenticated user's files.
    """

    try:
        container_client = get_container_client()

        blob_name = f"{get_user_id_from_claims(claims)}/{filename}"

        blob_client = container_client.get_blob_client(blob_name)

        blob_client.delete_blob()

        return {
            "message": "File deleted successfully",
            "filename": filename,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail=f"File deletion failed: {str(exc)}",
        ) from exc
