from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

import auth
import models
from blob_storage import get_container_client

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


# ---------------------------------------------------------
# Upload file
# ---------------------------------------------------------

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Upload a file to Azure Blob Storage.

    The user's ID is included in the blob path so each user
    has their own folder inside the taskapp-files container.
    """

    try:
        container_client = get_container_client()

        blob_name = f"{current_user.id}/{file.filename}"

        blob_client = container_client.get_blob_client(blob_name)

        await file.seek(0)

        blob_client.upload_blob(
            file.file,
            overwrite=True,
            content_type=file.content_type,
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
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    List files belonging to the authenticated user.
    """

    try:
        container_client = get_container_client()

        prefix = f"{current_user.id}/"

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
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Download one of the authenticated user's files.
    """

    try:
        container_client = get_container_client()

        blob_name = f"{current_user.id}/{filename}"

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
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Delete one of the authenticated user's files.
    """

    try:
        container_client = get_container_client()

        blob_name = f"{current_user.id}/{filename}"

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
