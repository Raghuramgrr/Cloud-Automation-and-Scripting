import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

# Variables
subscription_id = "your_subscription_id"
resource_group_name = "myResourceGroup"
location = "East US"
vm_name = "myUbuntuVM"
admin_username = "azureuser"
ssh_public_key = open(os.path.expanduser("~/.ssh/myazurekey.pub")).read().strip()
network_interface_name = f"{vm_name}-nic"
storage_account_name = f"mystorageaccount{int(time.time())}"  # Unique name for storage account

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Create a resource group
resource_client.resource_groups.create_or_update(resource_group_name, {"location": location})

# Create a virtual network
vnet_params = {
    "location": location,
    "address_space": {
        "address_prefixes": ["10.0.0.0/16"]
    }
}
vnet_result = network_client.virtual_networks.begin_create_or_update(resource_group_name, "myVNet", vnet_params)
vnet_result.wait()

# Create a subnet
subnet_params = {
    "address_prefix": "10.0.0.0/24"
}
subnet_result = network_client.subnets.begin_create_or_update(resource_group_name, "myVNet", "mySubnet", subnet_params)
subnet_result.wait()

# Create a public IP
public_ip_params = {
    "location": location,
    "public_ip_allocation_method": "Dynamic"
}
public_ip_result = network_client.public_ip_addresses.begin_create_or_update(resource_group_name, f"{vm_name}-pip", public_ip_params)
public_ip_result.wait()

# Create a network interface
nic_params = {
    "location": location,
    "ip_configurations": [{
        "name": "myIpConfig",
        "public_ip_address": {
            "id": public_ip_result.result().id
        },
        "subnet": {
            "id": subnet_result.result().id
        }
    }]
}
nic_result = network_client.network_interfaces.begin_create_or_update(resource_group_name, network_interface_name, nic_params)
nic_result.wait()

# Create a VM
vm_parameters = {
    "location": location,
    "os_profile": {
        "computer_name": vm_name,
        "admin_username": admin_username,
        "linux_configuration": {
            "ssh": {
                "public_keys": [{
                    "path": f"/home/{admin_username}/.ssh/authorized_keys",
                    "key_data": ssh_public_key
                }]
            }
        },
    },
    "hardware_profile": {
        "vm_size": "Standard_DS1_v2"
    },
    "storage_profile": {
        "image_reference": {
            "publisher": "Canonical",
            "offer": "UbuntuServer",
            "sku": "18.04-LTS",
            "version": "latest"
        },
        "os_disk": {
            "name": f"{vm_name}-osdisk",
            "caching": "ReadWrite",
            "create_option": "FromImage",
        },
    },
    "network_profile": {
        "network_interfaces": [{
            "id": nic_result.result().id
        }]
    }
}

# Create the VM
async_vm_creation = compute_client.virtual_machines.begin_create_or_update(resource_group_name, vm_name, vm_parameters)
async_vm_creation.wait()

print(f"Ubuntu VM '{vm_name}' created successfully.")

# Harden the VM: Execute commands to install updates and configure firewall
import paramiko
import time

# Connect to the VM using SSH
def ssh_connect(hostname, username, key_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, key_filename=key_file)
    return client

vm_public_ip = public_ip_result.result().ip_address
ssh_client = ssh_connect(vm_public_ip, admin_username, os.path.expanduser("~/.ssh/myazurekey"))

# Execute commands to harden the VM
commands = [
    "sudo apt update && sudo apt upgrade -y",  # Update packages
    "sudo apt install ufw -y",  # Install UFW
    "sudo ufw allow OpenSSH",  # Allow SSH
    "sudo ufw enable",  # Enable UFW
    "sudo ufw status",  # Check UFW status
    "sudo apt install fail2ban -y",  # Install Fail2Ban
]

for command in commands:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    time.sleep(1)  # Wait for command to complete
    print(f"Command: {command} \nOutput: {stdout.read().decode()} \nErrors: {stderr.read().decode()}")

ssh_client.close()
print("VM hardening completed.")
