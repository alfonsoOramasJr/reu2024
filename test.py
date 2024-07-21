import socket
import struct
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import datetime

# Constants
INPUT_SIZE = 1000  # Number of nodes in each input layer
BUFFER_SIZE = INPUT_SIZE * 4  # Assuming each int is 4 bytes
TOTAL_CLIENTS = 2

# Finger name mapping, including no movement
FINGER_NAMES = ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'pinky', 'no_movement']

def load_isolated_channel_model():
    return load_model('isolated_channel_single_output_model.h5')

def read_server_configuration():
    with open('server_configuration/ip.txt', 'r') as file:
        server_ip = file.read().strip()
    with open('server_configuration/port.txt', 'r') as file:
        server_port = int(file.read().strip())
    return server_ip, server_port

def handle_client(client_socket, client_address, channel_data):
    print(f"Connection from {client_address}")
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if data:
            data_values = list(struct.unpack(f'{len(data)//4}i', data))
            channel_data.extend(data_values)

            # Check if we have enough data to make a prediction
            if len(channel_data) >= INPUT_SIZE:
                input_data = np.array(channel_data[:INPUT_SIZE]).reshape(1, INPUT_SIZE)
                channel_data = channel_data[INPUT_SIZE:]
                return input_data
        else:
            break
    client_socket.close()

def start_test_server():
    # Load the pre-trained model
    model = load_isolated_channel_model()
    print("Model loaded successfully")

    # Read server configuration
    server_ip, server_port = read_server_configuration()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(TOTAL_CLIENTS)
    print(f"Server started at {server_ip}:{server_port}")

    client_sockets = []
    channel_data = [[], []]
    x1, x2 = [], []

    try:
        for i in range(TOTAL_CLIENTS):
            client_socket, client_address = server_socket.accept()
            client_sockets.append((client_socket, client_address))

        print("Both clients are connected. Testing data...")

        while True:
            for i in range(TOTAL_CLIENTS):
                input_data = handle_client(client_sockets[i][0], client_sockets[i][1], channel_data[i])
                if input_data is not None:
                    if i == 0:
                        x1 = input_data
                    else:
                        x2 = input_data

                    if len(x1) > 0 and len(x2) > 0:
                        predictions = model.predict([x1, x2])
                        predicted_class = np.argmax(predictions, axis=1)[0]
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"Timestamp: {timestamp}, Predicted class: {FINGER_NAMES[predicted_class]}")
                        x1, x2 = [], []

    except KeyboardInterrupt:
        print("Server stopped by user")

    finally:
        for client_socket, _ in client_sockets:
            client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    start_test_server()
