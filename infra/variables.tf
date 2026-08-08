variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "uksouth"
}

variable "project_name" {
  description = "Project prefix used in resource names."
  type        = string
  default     = "fastapi-todo"
}

variable "container_registry_login_server" {
  description = "ACR login server, for example myregistry.azurecr.io."
  type        = string
  default     = "CHANGE_ME.azurecr.io"
}

variable "backend_image" {
  description = "Backend image name and tag."
  type        = string
  default     = "fastapi-todo-backend:latest"
}

variable "frontend_image" {
  description = "Frontend image name and tag."
  type        = string
  default     = "fastapi-todo-frontend:latest"
}

variable "environments" {
  description = "Deployment environments."
  type        = set(string)
  default     = ["dev", "staging", "prod"]
}
