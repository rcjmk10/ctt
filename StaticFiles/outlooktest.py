from azure.identity import CertificateCredential
import requests
import json
import os

CLIENT_ID = '7848fbbb-8995-47a3-afc2-8279a845355c'
TENANT_ID = '7df3304f-b1fe-4617-afd0-3898de44deae'
CERTIFICATE_PATH = 'certificate.pfx'
CERTIFICATE_PASSWORD = 'changeit'  # Only needed for .pfx files

# Make sure the path is valid and file is readable
if not os.path.exists(CERTIFICATE_PATH):
    raise FileNotFoundError(f"Certificate not found at {CERTIFICATE_PATH}")
# Use ClientCertificateCredential for authentication
credential = CertificateCredential(
    client_id=CLIENT_ID,
    tenant_id=TENANT_ID,
    certificate_path=CERTIFICATE_PATH,
    password=CERTIFICATE_PASSWORD.strip()
)

token = credential.get_token('https://graph.microsoft.com/.default').token

 
# Get user ID from email
 

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Get all users to confirm the correct UPN
user_list_url = 'https://graph.microsoft.com/v1.0/users'

response = requests.get(user_list_url, headers=headers)

if response.status_code == 200:
    users = response.json().get('value', [])
    for user in users:
        print(f"User: {user.get('displayName')} - {user.get('mail')} - {user.get('userPrincipalName')}")
else:
    print(f"Failed to fetch user list: {response.status_code}")
    print(response.json())


email = 'zhongfali@msn.com'
user_url = f'https://graph.microsoft.com/v1.0/users?$filter=mail eq \'{email}\''

response = requests.get(user_url, headers=headers)
user_id=email
if response.status_code == 200:
    user_data = response.json().get('value', [])
    if user_data:
        user_id = user_data[0].get('id')
        print(f"User ID: {user_id}")
    else:
        print("User not found.")
else:
    print(f"Failed to fetch user ID: {response.status_code}")
    print(response.json())   

ooo_url = f'https://graph.microsoft.com/v1.0/users/{user_id}/mailboxSettings'
print("ooo_url:", ooo_url)
ooo_settings = {
    "automaticRepliesSetting": {
        "status": "scheduled",
        "scheduledStartDateTime": {
            "dateTime": "2025-03-25T09:00:00",
            "timeZone": "UTC"
        },
        "scheduledEndDateTime": {
            "dateTime": "2025-03-30T18:00:00",
            "timeZone": "UTC"
        },
        "internalReplyMessage": "I am currently out of the office.",
        "externalReplyMessage": "I'm out of the office. Please contact support@example.com.",
        "externalAudience": "all"
    }
}

response = requests.patch(ooo_url, headers=headers, json=ooo_settings)

if response.status_code == 200:
    print("Out-of-office set successfully!")
else:
    print(f"Failed to set out-of-office: {response.status_code}")
    print(response.json())