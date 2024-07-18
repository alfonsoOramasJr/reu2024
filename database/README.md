# Database Schema Documentation

This documentation provides an overview of the database schema used in this project. The database is designed to store data collected from various finger sensors.

## Database Structure

The database consists of five main tables, each corresponding to a different finger:

- thumb
- index_finger
- middle_finger
- ring_finger
- pinky

Each table stores the data collected from the respective finger sensor.

## Table Schema

All tables follow the same schema:

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-incrementing         |
| channel     | INTEGER | The channel from which data is collected |
| data_value  | INTEGER | The collected data value               |

## Table Definitions

### thumb
Stores data collected from the thumb sensor.

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-incrementing         |
| channel     | INTEGER | The channel from which data is collected |
| data_value  | INTEGER | The collected data value               |

### index_finger
Stores data collected from the index finger sensor.

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-incrementing         |
| channel     | INTEGER | The channel from which data is collected |
| data_value  | INTEGER | The collected data value               |

### middle_finger
Stores data collected from the middle finger sensor.

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-incrementing         |
| channel     | INTEGER | The channel from which data is collected |
| data_value  | INTEGER | The collected data value               |

### ring_finger
Stores data collected from the ring finger sensor.

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-incrementing         |
| channel     | INTEGER | The channel from which data is collected |
| data_value  | INTEGER | The collected data value               |

### pinky
Stores data collected from the pinky sensor.

| Column      | Type    | Description                            |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Primary key, auto-incrementing         |
| channel     | INTEGER | The channel from which data is collected |
| data_value  | INTEGER | The collected data value               |

## Usage

To interact with the database, use the `DatabaseManager` class provided in the `database_management.py` file. This class includes methods for creating tables, inserting data, and querying data.

## Example

Here is an example of how to use the `DatabaseManager` class to insert data into the database:

```python
from database.database_management import DatabaseManager

db_path = 'path/to/database.db'
db_manager = DatabaseManager(db_path)

# Ensure tables exist
db_manager.create_tables_if_not_exist()

# Insert data
channel = 1
data_value = 123
db_manager.cursor.execute("INSERT INTO thumb (channel, data_value) VALUES (?, ?)", (channel, data_value))
db_manager.conn.commit()

# Close the connection
db_manager.close_connection()
