import socket
import psutil

def get_local_ip():
    try:
        # Create a socket object to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error while retrieving local IP address: {e}")
        return None

def get_network_interface(local_ip):
    try:
        # Get the network interface for the local IP
        interfaces = psutil.net_if_addrs()
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == local_ip:
                    return interface
    except Exception as e:
        print(f"Error while retrieving network interface: {e}")

    return None

# Get the local IP address
local_ip = get_local_ip()

if local_ip:
    print(f"Local IP Address: {local_ip}")

    # Get the network interface for the local IP
    network_interface = get_network_interface(local_ip)

    if network_interface:
        print(f"Network Interface: {network_interface}")
    else:
        print("Failed to retrieve network interface.")
else:
    print("Failed to retrieve local IP address.")

