
variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "static-web-apps-rg"
}

variable "static_web_app_name" {
  description = "Globally unique Static Web App name"
  type        = string
  default     = "my-first-static-web-app-2026"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US 2"
}