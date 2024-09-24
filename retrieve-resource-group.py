from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Variables
subscription_id = "your_subscription_id"
resource_group_name = "myResourceGroup"

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

# Get resource group details
resource_group = resource_client.resource_groups.get(resource_group_name)
print(f"Resource Group: {resource_group.name} located in: {resource_group.location}")
