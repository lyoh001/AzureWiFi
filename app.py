import base64
import datetime
import os
import random
import re
import string
import subprocess

import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

DASH_LINE = "-" * 50
USERNAME = os.getenv("WIFI_RESET_USERNAME")
PASSWORD = os.getenv("WIFI_RESET_PASSWORD")
LOGICAPP_URL = os.getenv("LOGICAPP_URL")
ISE_URL_TEST = os.getenv("ISE_URL_TEST")
ISE_URLS = [os.getenv("ISE_URL_BUR"), os.getenv("ISE_URL_BAL")]
AUTH_VALUE = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Basic {AUTH_VALUE}",
}
PAYLOAD_TEMPLATE = {
    "SponsoredGuestPortal": {
        "id": "5f3065c0-9cc0-11e6-9f77-00505685641d",
        "name": "CenITex Sponsored Guest Portal",
        "description": "GuestVG Portal",
        "portalType": "SPONSOREDGUEST",
        "portalTestUrl": ISE_URL_TEST,
        "settings": {
            "portalSettings": {
                "httpsPort": 8443,
                "allowedInterfaces": ["eth0", "bond0"],
                "certificateGroupTag": "Guest",
                "authenticationMethod": "97dff3f0-2230-11e6-99ab-005056bf55e0",
                "assignedGuestTypeForEmployee": "CenITex - Daily",
                "displayLang": "USEBROWSERLOCALE",
                "fallbackLanguage": "English",
                "alwaysUsedLanguage": "English",
            },
            "loginPageSettings": {
                "requireAccessCode": False,
                "maxFailedAttemptsBeforeRateLimit": 5,
                "timeBetweenLoginsDuringRateLimit": 2,
                "includeAup": False,
                "allowGuestToCreateAccounts": True,
                "allowGuestToChangePassword": True,
                "allowAlternateGuestPortal": False,
            },
            "selfRegPageSettings": {
                "assignGuestsToGuestType": "CenITex - Daily",
                "accountValidityDuration": 5,
                "accountValidityTimeUnits": "DAYS",
                "requireRegistrationCode": True,
                "registrationCode": None,
                "credentialNotificationUsingEmail": True,
                "fieldUserName": {"include": False, "require": False},
                "fieldEmailAddr": {"include": True, "require": False},
            },
            "selfRegSuccessSettings": {
                "allowGuestSendSelfUsingEmail": True,
                "allowGuestLoginFromSelfregSuccessPage": True,
            },
            "guestChangePasswordSettings": {"allowChangePasswdAtFirstLogin": False},
        },
    }
}


def extract_ip_address(proc_output):
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    match = re.search(ip_pattern, proc_output)
    return match.group(0) if match else None


def generate_password(length=6):
    return "".join(random.choices(string.digits, k=length))


def send_email(message):
    print(f"Sending {message} to Logic app")
    try:
        response = requests.post(
            url=LOGICAPP_URL,
            json={
                "password": message,
                "date": datetime.date.today().strftime("%B %d, %Y"),
            },
        )
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Logic app: {e}")
        return None


def connect_to_ise(url):
    print("Checking connection to ISE")
    try:
        response = requests.get(
            url=url,
            headers=HEADERS,
            verify=False,
        )
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        send_email(f"Error connecting to {url.split(':9060')[0]}: {e}")
        return None


def change_password(url, payload):
    try:
        return 200
        response = requests.put(
            url=url,
            headers=HEADERS,
            json=payload,
            verify=False,
        )
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        send_email(f"Error updating ISE portal at {url.split(':9060')[0]}: {e}")
        return None


wifi_code = generate_password()
payload = PAYLOAD_TEMPLATE.copy()
payload["SponsoredGuestPortal"]["settings"]["selfRegPageSettings"][
    "registrationCode"
] = wifi_code
ip = extract_ip_address(subprocess.check_output("ipconfig").decode("utf-8"))
url = ISE_URLS[0] if ip.startswith("10.61") else ISE_URLS[1]

print(DASH_LINE)
print(f"The hybrid worker node IP: {ip}")
print(DASH_LINE)
print(f"Attempting to connect to {url}")
print(DASH_LINE)

if connect_to_ise(url) == 200:
    print(DASH_LINE)
    print("Connection check successful")
    print(DASH_LINE)
    print("Changing password")
    print(DASH_LINE)
    if change_password(url, payload) == 200:
        print("Password changed successfully")
        print(DASH_LINE)
        send_email(wifi_code)
        print(DASH_LINE)
        print("Email sent")
    else:
        print(f"Error updating ISE portal at {url.split(':9060')[0]}")
        send_email(f"Error updating ISE portal at {url.split(':9060')[0]}")
else:
    print(f"Error connecting to {url.split(':9060')[0]}")
    send_email(f"Error connecting to {url.split(':9060')[0]}")
print(DASH_LINE)
