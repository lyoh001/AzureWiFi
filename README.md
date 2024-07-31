# ISE Portal Password Reset

This Python script automates the process of resetting the registration code for a Cisco ISE (Identity Services Engine) Sponsored Guest Portal. It connects to the ISE server, updates the portal settings with a new randomly generated registration code, and sends the new code via email using a Logic App.

## Features

- Automatically detects the correct ISE server based on the local IP address
- Generates a random 6-digit registration code
- Updates the ISE Sponsored Guest Portal settings
- Sends the new registration code via email using a Logic App
- Includes error handling and logging

## Prerequisites

- Python 3.x
- `requests` library
- Access to a Cisco ISE server
- Azure Logic App for sending emails

## Environment Variables

The script requires the following environment variables to be set:

- `WIFI_RESET_USERNAME`: Username for ISE authentication
- `WIFI_RESET_PASSWORD`: Password for ISE authentication
- `LOGICAPP_URL`: URL of the Azure Logic App for sending emails
- `ISE_URL_BUR`: URL of the ISE server in Burwood
- `ISE_URL_BAL`: URL of the ISE server in Ballarat

## Installation

1. Clone this repository:
git clone https://github.com/yourusername/ise-portal-password-reset.git


2. Install the required Python packages:
pip install requests


3. Set up the required environment variables.

## Usage

Run the script using Python:

python ise_portal_reset.py


The script will automatically:
1. Determine the correct ISE server to connect to
2. Generate a new registration code
3. Update the ISE Sponsored Guest Portal settings
4. Send the new code via email

## Error Handling

The script includes error handling for common issues such as:
- Connection failures to the ISE server
- Failures in updating the portal settings
- Errors in sending emails

In case of any errors, the script will attempt to send an email notification with details about the error.

## Security Notes

- This script uses environment variables for sensitive information like usernames and passwords. Ensure these are properly secured.
- The script disables SSL verification (`verify=False`) when connecting to the ISE server. In a production environment, proper SSL certificate validation should be implemented.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit a Pull Request.
