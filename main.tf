
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "web" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    project     = "azure-static-web-app"
    environment = "learning"
  }
}

resource "azurerm_static_web_app" "web" {
  name                = var.static_web_app_name
  resource_group_name = azurerm_resource_group.web.name
  location            = azurerm_resource_group.web.location

  sku_tier = "Free"
  sku_size = "Free"

  tags = {
    project = "azure-static-web-app"
  }
}