data "azurerm_public_ip" "public_ip" {
  name                = azurerm_public_ip.public_ip.name
  resource_group_name = azurerm_linux_virtual_machine.vm.resource_group_name
  depends_on          = [azurerm_linux_virtual_machine.vm]
}

output "web_dashboard_url" {
  value       = "http://${data.azurerm_public_ip.public_ip.ip_address}:5000"
  description = "URL для доступу до веб-інтерфейсу"
}

output "ssh_command" {
  value       = "ssh -i private_key.pem azureuser@${data.azurerm_public_ip.public_ip.ip_address}"
  description = "Команда для підключення до ВМ по SSH"
}

output "private_key" {
  value     = tls_private_key.ssh.private_key_pem
  sensitive = true
}