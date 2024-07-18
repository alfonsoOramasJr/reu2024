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