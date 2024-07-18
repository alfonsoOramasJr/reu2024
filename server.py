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

def start_server():
    data_type = input("Please enter the type of data you will be collecting: ")
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