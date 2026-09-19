
output "static_web_app_url" {
  description = "Public URL of the Static Web App"

  value = "https://${azurerm_static_web_app.web.default_host_name}"
}

output "deployment_token" {
  description = "Deployment token for GitHub Actions"

  value     = azurerm_static_web_app.web.api_key
  sensitive = true
}