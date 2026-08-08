resource "azurerm_resource_group" "shared" {
  name     = "rg-${var.project_name}-shared"
  location = var.location

  tags = {
    project     = var.project_name
    environment = "shared"
    managed_by  = "terraform"
  }
}

resource "azurerm_container_registry" "main" {
  name                = replace("acr${var.project_name}", "-", "")
  resource_group_name = azurerm_resource_group.shared.name
  location            = azurerm_resource_group.shared.location
  sku                 = "Basic"
  admin_enabled       = false

  retention_policy_in_days = 7

  tags = azurerm_resource_group.shared.tags
}

resource "azurerm_storage_account" "tfstate" {
  name                     = substr(replace("st${var.project_name}tfstate", "-", ""), 0, 24)
  resource_group_name      = azurerm_resource_group.shared.name
  location                 = azurerm_resource_group.shared.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = azurerm_resource_group.shared.tags
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.tfstate.id
  container_access_type = "private"
}
