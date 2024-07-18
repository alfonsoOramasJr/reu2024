import socket
import os
import struct

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
    TOTAL_CLIENTS = 2  ## The number of ESP32's we're collecting data from
    TOTAL_VALUES_FROM_EACH_CLIENT = 1000  ## The expected number of values from each client
    DEBUG = True  ## Set to True to enable debug output

    data_type = get_data_type()
    print(f"Data type set to: {data_type}")

    try:
        ip, port = read_server_config()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading configuration: {e}")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(TOTAL_CLIENTS)
    print(f"Server started at {ip}:{port}")

    clients = []
    buffers = [[] for _ in range(TOTAL_CLIENTS)]  # List of lists to hold data values for each client

    try:
        while len(clients) < TOTAL_CLIENTS:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            clients.append((client_socket, client_address))
        
        print("Both clients are connected. Collecting data...")

        while True:
            for i, (client_socket, client_address) in enumerate(clients):
                data = client_socket.recv(TOTAL_VALUES_FROM_EACH_CLIENT * 4)  # Assuming each int is 4 bytes
                if data:
                    data_values = list(struct.unpack(f'{len(data)//4}i', data))  # Convert received byte array to a list of integers
                    buffers[i].append(data_values)
                    if DEBUG:
                        print(f"Data from {client_address}: {data_values}")

    except KeyboardInterrupt:
        print("Server interrupted by user. Closing connections.")
    finally:
        for client_socket, client_address in clients:
            if client_socket:
                client_socket.close()
        server_socket.close()
        print("Server shut down gracefully.")

        # Process the collected data
        for i, buffer in enumerate(buffers):
            print(f"Data collected from client {i}: {buffer}")

if __name__ == "__main__":
    start_server()
