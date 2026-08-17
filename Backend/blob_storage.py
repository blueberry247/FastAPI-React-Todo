from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


STORAGE_ACCOUNT_NAME = "taskappstorage247"
CONTAINER_NAME = "taskapp-files"

ACCOUNT_URL = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"


@lru_cache(maxsize=1)
def get_blob_service_client() -> BlobServiceClient:
    credential = DefaultAzureCredential()

    return BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential,
    )


def get_container_client():
    return get_blob_service_client().get_container_client(CONTAINER_NAME)