output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}

output "frontend_app_urls" {
  value = {
    for env, app in azurerm_linux_web_app.frontend : env => "https://${app.default_hostname}"
  }
}

output "key_vault_names" {
  value = {
    for env, kv in azurerm_key_vault.main : env => kv.name
  }
}
