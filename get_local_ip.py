import socket

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

# Get the local IP address
local_ip = get_local_ip()

if local_ip:
    print(f"Local IP Address: {local_ip}")
else:
    print("Failed to retrieve local IP address.")

