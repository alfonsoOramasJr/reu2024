import socket
import os

def read_server_config():
    ip_file_path = os.path.join('server_configuration', 'ip.txt')
    port_file_path = os.path.join('server_configuration', 'port.txt')

    if not os.path.exists(ip_file_path) or not os.path.exists(port_file_path):
        raise FileNotFoundError("Configuration files not found in server_configuration folder")

    with open(ip_file_path, 'r') as ip_file:
        ip = ip_file.read().strip()

    with open(port_file_path, 'r') as port_file:
        port = port_file.read().strip()

    if not ip:
        raise ValueError("IP address in ip.txt is empty")
    if not port:
        raise ValueError("Port number in port.txt is empty")
    
    return ip, int(port)

def get_data_type():
    finger_types = {
        1: "thumb",
        2: "index finger",
        3: "middle finger",
        4: "ring finger",
        5: "pinky"
    }

    while True:
        print("Please select the type of data you will be collecting:")
        for key, value in finger_types.items():
            print(f"{key}. {value}")

        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if choice in finger_types:
                return finger_types[choice]
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

def start_server():
    data_type = get_data_type()
    print(f"Data type set to: {data_type}")

    try:
        ip, port = read_server_config()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading configuration: {e}")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Server started at {ip}:{port}")

    clients = []
    buffers = [b'', b'']

    try:
        while len(clients) < 2:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            clients.append((client_socket, client_address))
        
        print("Both clients are connected. Switching between clients to record data.")

        while True:
            for i, (client_socket, client_address) in enumerate(clients):
                data = client_socket.recv(1024)
                buffers[i] += data
                print(f"Data from {client_address}: {data}")

    except KeyboardInterrupt:
        print("Server interrupted by user. Closing connections.")
    finally:
        for client_socket, client_address in clients:
            if client_socket:
                client_socket.close()
        server_socket.close()
        print("Server shut down gracefully.")

if __name__ == "__main__":
    start_server()
