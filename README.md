# Azure Runbooks

This repository contains an Azure Automation Runbook that resets the WiFi password and sends the new password to the customer via email. The runbook is scheduled to execute every morning on one of the hybrid worker nodes for redundancy.

## Overview
## Logical Architecture
### Logical System Component Overview
![Figure 1: Logical Architecture Overview](./images/workflow.png)

### Code Deployment
- **Repository**: The code is pushed to GitHub.
- **Runbook Deployment**: `Import-AzAutomationRunbook` and `Publish-AzAutomationRunbook` are performed via a CI/CD pipeline.

### Scheduled Execution
- **Frequency**: The runbook is scheduled to execute every morning.
- **Redundancy**: Executes on one of the hybrid worker nodes from two different data centers.

### Site Determination
- **IP Address Check**: The script checks the first two octets of the IP address to determine the site.
- **Connectivity Check**: Verifies connectivity to the ISE on the determined site.

### API Calls
- **GET API Call**: If the GET API call returns 200, it proceeds.
- **PUT API Call**: Resets the WiFi password.

### Email Notification
- **Notification**: Sends an email to the customer with the new password upon successful reset.

## CI/CD Pipeline

The CI/CD pipeline is defined in the GitHub Actions workflow file. Below is the configuration:

## Runbook Script

The runbook script is written in Python and performs the following tasks:

1. **Extract IP Address**: Extracts the IP address of the hybrid worker node.
2. **Generate Password**: Generates a new WiFi password.
3. **Send Email**: Sends the new password to the customer via email.
4. **Connect to ISE**: Checks connectivity to the ISE.
5. **Change Password**: Updates the WiFi password on the ISE.

## Environment Variables

Ensure the following environment variables are set:

- `WIFI_RESET_USERNAME`
- `WIFI_RESET_PASSWORD`
- `LOGICAPP_URL`
- `ISE_URL_TEST`
- `ISE_URL_BUR`
- `ISE_URL_BAL`
