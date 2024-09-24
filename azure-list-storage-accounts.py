from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

# Variables
subscription_id = "your_subscription_id"

# Authentication
credential = DefaultAzureCredential()
storage_client = StorageManagementClient(credential, subscription_id)

# List all storage accounts
storage_accounts = storage_client.storage_accounts.list()
for account in storage_accounts:
    print(f"Storage Account: {account.name} in Resource Group: {account.resource_group}")
