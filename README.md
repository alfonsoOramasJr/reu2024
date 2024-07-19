# Application Documentation
This documentation provides an overview of the server and machine learning models used in this project. The server collects data from multiple clients, and the models classify this data based on the source.

### Create a Virtual Environment
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

### How to Run the Server
1. Ensure the `server_configuration` folder contains `ip.txt` and `port.txt` with the appropriate IP address and port number.
2. Ensure the database is set up correctly with the necessary tables.

### Example Code to Run the Server
1. Make sure that you are in the root path as the server.py and run the following command,
## Windows:
```sh
python server.py
```

## Linux:
```sh
python3 server.py
```