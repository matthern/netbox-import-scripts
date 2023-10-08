import socket
import sys
import requests
import json
from config import API_TOKEN
from config import API_URL
from get_local_ip import get_local_ip

# Get the hostname
hostname = socket.gethostname()

# Get the local IP address
#local_ip = socket.gethostbyname(hostname)

# Get the local IP address
local_ip = get_local_ip()

if local_ip:
    print(f"Local IP Address: {local_ip}")
else:
    print("Failed to retrieve local IP address.")


# Define the interface name you want to associate with the IP address
interface_name = "eth0"

# Define the virtual machine name
virtual_machine_name = hostname  # You can customize this if needed

# Define the data to send for adding the IP address
ip_data_to_send = {
    "address": f"{local_ip}/32",  # Assuming /32 for a single IP address
    "dns_name": hostname,
    "description": f"IP address for {hostname}",
    "status": "active",
    "interface": None,  # Leave interface as None for now
}

# Define the headers with the API token and content type
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {API_TOKEN}",
}

# Define the API endpoints for interfaces and IP addresses
interface_api_endpoint = "virtualization/interfaces/"
ip_api_endpoint = "ipam/ip-addresses/"
vm_api_endpoint = "virtualization/virtual-machines/"

# Step 1: Find the interface ID based on the interface name
#interface_query_params = {"name": interface_name}
#interface_response = requests.get(f"{API_URL}{interface_api_endpoint}", headers=headers, params=interface_query_params)
# Find the interface associated with the VM (hostname)
interface_query_params = {"name": interface_name, "virtual_machine": hostname}
interface_response = requests.get(f"{API_URL}{interface_api_endpoint}", headers=headers, params=interface_query_params)


# Check if the IP address already exists in NetBox
existing_ip_query_params = {"address": local_ip}
existing_ip_response = requests.get(f"{API_URL}{ip_api_endpoint}", headers=headers, params=existing_ip_query_params)

if existing_ip_response.status_code == 200:
    existing_ips = existing_ip_response.json()["results"]

    if existing_ips:
        # IP address already exists, so exit the script
        print(f"IP address {local_ip} already exists in NetBox. Exiting script.")
        sys.exit()  
    else:
        # IP address doesn't exist, continue with the script
        pass
else:
    print(f"Failed to check existing IP addresses. Status code: {existing_ip_response.status_code}")

# ... (rest of your script)

if interface_response.status_code == 200:
    interfaces = interface_response.json()["results"]
    if interfaces:
        # Use the first interface found (assuming unique interface names)
        interface_id = interfaces[0]["id"]

        # Step 2: Define the API endpoint for adding the IP address
        ip_create_url = f"{API_URL}{ip_api_endpoint}"

        # Step 3: Add the IP address to NetBox
        ip_response = requests.post(ip_create_url, data=json.dumps(ip_data_to_send), headers=headers)

        if ip_response.status_code == 201:
            print(f"IP address added successfully")

            # Step 4: Find the virtual machine ID based on the name
            vm_query_params = {"name": virtual_machine_name}
            vm_response = requests.get(f"{API_URL}{vm_api_endpoint}", headers=headers, params=vm_query_params)

            if vm_response.status_code == 200:
                vm_data = vm_response.json()["results"]
                if vm_data:
                    vm_id = vm_data[0]["id"]

                    # Step 5: Update the IP address to associate it with the interface
                    ip_id = ip_response.json()["id"]
                    ip_update_data = {
                        "assigned_object_type": "virtualization.vminterface",
                        "assigned_object_id": interface_id,
                    }
                    ip_update_url = f"{API_URL}{ip_api_endpoint}{ip_id}/"
                    ip_update_response = requests.patch(ip_update_url, data=json.dumps(ip_update_data), headers=headers)

                    if ip_update_response.status_code == 200:
                        print(f"IP address associated with interface successfully")
                    else:
                        print(f"Failed to associate IP address with interface. Status code: {ip_update_response.status_code}")
                else:
                    print(f"No virtual machine found with name: {virtual_machine_name}")
            else:
                print(f"Failed to retrieve virtual machine information. Status code: {vm_response.status_code}")
        else:
            print(f"Failed to add IP address. Status code: {ip_response.status_code}")
    else:
        print(f"No interface found with name: {interface_name}")
else:
    print(f"Failed to retrieve interface information. Status code: {interface_response.status_code}")

