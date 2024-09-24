


# Ubuntu VM Hardening on Azure

This project demonstrates how to provision and harden an Ubuntu Virtual Machine (VM) in Azure using a Python script. The script creates necessary resources in Azure and applies basic hardening measures to the VM.

## Overview

The script performs the following actions:

1. **Create Resources**:
   - Creates a resource group.
   - Sets up a virtual network and a subnet.
   - Allocates a public IP address.
   - Creates a network interface.
   - Provisions an Ubuntu VM and configures SSH access using a public key.

2. **Harden the VM**:
   - Uses the `paramiko` library to SSH into the VM.
   - Executes commands to:
     - Update system packages.
     - Install and configure the Uncomplicated Firewall (UFW).
     - Install Fail2Ban to help prevent brute-force attacks.

## Prerequisites

- **Azure SDK for Python**: Install the required packages:
    ```bash
    pip install azure-identity azure-mgmt-resource azure-mgmt-compute azure-mgmt-network paramiko
    ```

- **SSH Key**: Generate an SSH key pair if you don't have one:
    ```bash
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/myazurekey
    ```

- **Azure Subscription**: Ensure you have the necessary permissions to create resources in Azure.

## Script Configuration

Replace `your_subscription_id` with your actual Azure subscription ID in the script. Ensure your SSH key paths and VM configurations are correct.

## Python Script
harden-vm.py



# Other tasks 
These code snippets provide a solid foundation for managing Azure resources programmatically using Python. The tasks covered include:

## Creating a virtual machine
## Listing storage accounts
## Retrieving resource group information
## Deleting a resource group
## Listing all virtual machines in a specific resource group