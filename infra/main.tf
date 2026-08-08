resource "azurerm_resource_group" "main" {
  for_each = var.environments

  name     = "rg-${var.project_name}-${each.key}"
  location = var.location

  tags = {
    project     = var.project_name
    environment = each.key
    managed_by  = "terraform"
  }
}

resource "azurerm_key_vault" "main" {
  for_each = var.environments

  name                       = substr("kv-${var.project_name}-${each.key}", 0, 24)
  location                   = azurerm_resource_group.main[each.key].location
  resource_group_name        = azurerm_resource_group.main[each.key].name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7

  tags = azurerm_resource_group.main[each.key].tags
}

resource "azurerm_service_plan" "main" {
  for_each = var.environments

  name                = "plan-${var.project_name}-${each.key}"
  location            = azurerm_resource_group.main[each.key].location
  resource_group_name = azurerm_resource_group.main[each.key].name
  os_type             = "Linux"
  sku_name            = each.key == "prod" ? "B1" : "F1"

  tags = azurerm_resource_group.main[each.key].tags
}

resource "azurerm_linux_web_app" "frontend" {
  for_each = var.environments

  name                = "app-${var.project_name}-${each.key}"
  location            = azurerm_resource_group.main[each.key].location
  resource_group_name = azurerm_resource_group.main[each.key].name
  service_plan_id     = azurerm_service_plan.main[each.key].id

  site_config {
    application_stack {
      docker_image_name   = var.frontend_image
      docker_registry_url = "https://${var.container_registry_login_server}"
    }
  }

  app_settings = {
    WEBSITES_PORT = "80"
  }

  tags = azurerm_resource_group.main[each.key].tags
}

resource "azurerm_mssql_server" "main" {
  for_each = var.environments

  name                         = "sql-${var.project_name}-${each.key}"
  resource_group_name          = azurerm_resource_group.main[each.key].name
  location                     = azurerm_resource_group.main[each.key].location
  version                      = "12.0"
  administrator_login          = "sqladminuser"
  administrator_login_password = random_password.sql_admin[each.key].result

  tags = azurerm_resource_group.main[each.key].tags
}

resource "azurerm_mssql_database" "main" {
  for_each = var.environments

  name      = "sqldb-${var.project_name}-${each.key}"
  server_id = azurerm_mssql_server.main[each.key].id
  sku_name  = each.key == "prod" ? "S0" : "Basic"

  tags = azurerm_resource_group.main[each.key].tags
}

resource "random_password" "sql_admin" {
  for_each = var.environments

  length  = 24
  special = true
}

data "azurerm_client_config" "current" {}
