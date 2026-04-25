variable "resource_group_name" {
  type    = string
  default = "rg-docker-lab"
}

variable "location" {
  type    = string
  default = "West Europe"
}

variable "vm_size" {
  type    = string
  default = "Standard_B1ms"
}