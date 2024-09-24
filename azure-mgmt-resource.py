from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

# Variables
subscription_id = "your_subscription_id"
resource_group_name = "myResourceGroup"
location = "East US"
storage_account_name = "mystorageaccountunique"  # Must be globally unique

# Authentication
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

# Create a resource group
resource_client.resource_groups.create_or_update(resource_group_name, {"location": location})

# Create a storage account
storage_account = storage_client.storage_accounts.create(
    resource_group_name,
    storage_account_name,
    {
        "sku": {"name": "Standard_LRS"},
        "kind": "StorageV2",
        "location": location,
    },
)
print(f"Storage account {storage_account_name} created.")

# Upload a file to the storage account (example file is 'backup.zip')
from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=credential)
blob_client = blob_service_client.get_blob_client(container="mybackupcontainer", blob="backup.zip")

with open("backup.zip", "rb") as data:
    blob_client.upload_blob(data)
print("Backup uploaded successfully.")
