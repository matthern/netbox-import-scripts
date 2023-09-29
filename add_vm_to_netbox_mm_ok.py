import requests
import json
import socket
from config import API_TOKEN
from config import API_URL



# NetBox API URL and API token

# Define the VM name and interface name
vm_name = socket.gethostname()
interface_name = "eth0"  # Change this to your desired interface name

# Step 1: Define the data to send for adding the VM (including role, cluster, and site IDs)
vm_data_to_send = {
    "name": vm_name,
    "virtual_machine_role": 1,  # Replace with the appropriate role ID for Virtual Machine
    "status": "active",
    "cluster": 1,  # Replace with the appropriate cluster ID
    "site": 1,  # Replace with the appropriate site ID
    "custom_field": "any_custom_data"  # Add any custom fields as needed
}

# Define the headers with the API token and content type
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {API_TOKEN}"
}

# Define the API endpoints for VMs and interfaces
vm_api_endpoint = "virtualization/virtual-machines/"
interface_api_endpoint = "virtualization/interfaces/"

# Step 1: Add the VM to NetBox
vm_create_url = f"{API_URL}{vm_api_endpoint}"
vm_response = requests.post(vm_create_url, data=json.dumps(vm_data_to_send), headers=headers)

if vm_response.status_code == 201:
    print(f"VM added successfully")

    # Extract the VM ID from the response JSON
    vm_id = vm_response.json()["id"]

    # Step 2: Define the data to send for adding the interface (with VM ID)
    interface_data_to_send = {
        "name": interface_name,
        "virtual_machine": vm_id  # Use the VM ID as the association
    }

    # Step 2: Add the interface to NetBox
    interface_create_url = f"{API_URL}{interface_api_endpoint}"
    interface_response = requests.post(interface_create_url, data=json.dumps(interface_data_to_send), headers=headers)

    if interface_response.status_code == 201:
        print(f"Interface added successfully")
    else:
        print(f"Failed to add interface. Status code: {interface_response.status_code}")
else:
    print(f"Failed to add VM. Status code: {vm_response.status_code}")

