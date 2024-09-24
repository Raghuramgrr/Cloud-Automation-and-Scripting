from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# Variables
subscription_id = "your_subscription_id"
resource_group_name = "myResourceGroup"

# Authentication
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

# List all VMs in the specified resource group
virtual_machines = compute_client.virtual_machines.list(resource_group_name)
for vm in virtual_machines:
    print(f"Virtual Machine: {vm.name} with status: {vm.instance_view.statuses[1].display_status}")
