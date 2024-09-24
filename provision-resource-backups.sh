#!/bin/bash

# Variables
RESOURCE_GROUP_NAME="myResourceGroup"
LOCATION="EastUS"
STORAGE_ACCOUNT_NAME="mystorageaccount$(date +%s)"  # Unique name
BACKUP_CONTAINER_NAME="mybackupcontainer"

# Create a resource group
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Create a storage account
az storage account create --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP_NAME --location $LOCATION --sku Standard_LRS

# Create a container in the storage account for backups
az storage container create --name $BACKUP_CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME

# Upload a file to the backup container (example file is 'backup.zip')
az storage blob upload --container-name $BACKUP_CONTAINER_NAME --file backup.zip --name backup.zip --account-name $STORAGE_ACCOUNT_NAME

echo "Resources provisioned and backup completed."
