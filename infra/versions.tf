terraform {
  required_version = ">= 1.6.0"

  # Configure this backend after creating the storage account/container.
  # terraform init \
  #   -backend-config="resource_group_name=rg-tfstate" \
  #   -backend-config="storage_account_name=sttfstateexample" \
  #   -backend-config="container_name=tfstate" \
  #   -backend-config="key=fastapi-react-todo.tfstate"
  backend "azurerm" {}

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}
