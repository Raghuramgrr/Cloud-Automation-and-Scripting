from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Variables
subscription_id = "your_subscription_id"
resource_group_name = "myResourceGroup"

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

# Delete resource group
resource_client.resource_groups.begin_delete(resource_group_name).wait()
print(f"Resource Group '{resource_group_name}' deleted successfully.")
