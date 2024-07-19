# Application Documentation
This documentation provides an overview of the server and machine learning models used in this project. The server collects data from multiple clients, and the models classify this data based on the source.

## Create a Virtual Environment
#### Windows:
```sh
python -m venv myenv
.\myenv\Scripts\activate
```

#### Linux:
```sh
python3 -m venv myenv
source myenv/bin/activate
```

### Install the Necessary Libraries
#### Windows:
```sh
pip install -r requirements.txt
```

#### Linux:
```sh
pip3 install -r requirements.txt
```

## How to Run the Server
1. Ensure the `server_configuration` folder contains `ip.txt` and `port.txt` with the appropriate IP address and port number.
2. Ensure the database is set up correctly with the necessary tables.

### Example Code to Run the Server
1. Make sure that you are in the root path as the server.py and run the following command,
#### Windows:
```sh
python server.py
```

#### Linux:
```sh
python3 server.py
```

## What is the Server for?
The server is for collecting data from multiple clients, such as ESP32 devices, and storing the collected data in a database. It ensures that data from each client is processed sequentially and consistently.

### Values to Modify
To configure the server for your specific use case, you may need to modify the following values in the server code:

1. **TOTAL_CLIENTS**: The number of clients (e.g., ESP32 devices) from which the server is expected to collect data.
   ```python
   TOTAL_CLIENTS = 2  # Example: change to the number of clients you have
   ```
2. **TOTAL_VALUES_FROM_EACH_CLIENT**: The expected number of values from each client.
    ```python
    TOTAL_VALUES_FROM_EACH_CLIENT = 1000  # Example: change to the number of values expected from each client
    ```
3. **DEBUG**: Set to 'True' to enable debug output, which provides detailed information about the data being collected from each client.
    ```python
    DEBUG = True  # Set to True for detailed debug output
    ```

### How the Server Collects Data
The server collects data from clients by iterating back and forth between them. Here is a brief overview of that process:

1. **Collects data from a specified amount of clients**
2. **Stops collecting data based on a keyboard interrupt from the user**: For the data to be recorded the user needs to stop the data collection manually via the 'Crtl-C' shortcut (Keyboard Interrupt).
3. **Records specific client data into their own distinct channels**:D Data from the clients is then transformed into 'channel data' which basically just means which computer was this information recorded from.