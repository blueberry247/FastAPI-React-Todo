from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


KEY_VAULT_URL = "https://taskapp-kv247.vault.azure.net/"
JWT_SECRET_NAME = "jwt-secret-key"


@lru_cache(maxsize=1)
def get_secret_client() -> SecretClient:
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=KEY_VAULT_URL, credential=credential)


@lru_cache(maxsize=1)
def get_jwt_secret_key() -> str:
    secret = get_secret_client().get_secret(JWT_SECRET_NAME)
    return secret.value
