import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate, Add
from tensorflow.keras.optimizers import Adam
from database.database_management import DatabaseManager
import random

# Constants
INPUT_SIZE = 1000  # Number of nodes in each input layer
HIDDEN_LAYER_NODES = 64  # Number of nodes in the hidden layers

def create_dual_channel_model():
    # Define input layers
    input1 = Input(shape=(INPUT_SIZE,), name='Channel1')
    input2 = Input(shape=(INPUT_SIZE,), name='Channel2')
    
    # Define the rest of the model
    x1 = Dense(HIDDEN_LAYER_NODES, activation='relu')(input1)
    x2 = Dense(HIDDEN_LAYER_NODES, activation='relu')(input2)
    
    # Concatenate both branches
    concatenated = Concatenate()([x1, x2])
    
    # Add more layers if needed
    x = Dense(HIDDEN_LAYER_NODES, activation='relu')(concatenated)
    x = Dense(HIDDEN_LAYER_NODES, activation='relu')(x)
    
    # Output layer with 5 outputs
    output = Dense(5, activation='softmax')(x)
    
    # Create model
    model = Model(inputs=[input1, input2], outputs=output, name='dual_channel')
    
    # Compile model
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def create_isolated_channel_single_output_model():
    # Define input layers
    input1 = Input(shape=(INPUT_SIZE,), name='Channel1')
    input2 = Input(shape=(INPUT_SIZE,), name='Channel2')
    
    # Define the rest of the model for Channel 1
    x1 = Dense(HIDDEN_LAYER_NODES, activation='relu')(input1)
    x1 = Dense(HIDDEN_LAYER_NODES, activation='relu')(x1)
    
    # Define the rest of the model for Channel 2
    x2 = Dense(HIDDEN_LAYER_NODES, activation='relu')(input2)
    x2 = Dense(HIDDEN_LAYER_NODES, activation='relu')(x2)
    
    # Combine the outputs of both channels
    combined = Add()([x1, x2])
    
    # Further processing
    x = Dense(HIDDEN_LAYER_NODES, activation='relu')(combined)
    x = Dense(HIDDEN_LAYER_NODES, activation='relu')(x)
    
    # Output layer with 5 outputs
    output = Dense(5, activation='softmax')(x)
    
    # Create model
    model = Model(inputs=[input1, input2], outputs=output, name='isolated_channel_single_output')
    
    # Compile model
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def load_data_from_db():
    db_path = 'database/database.db'
    db_manager = DatabaseManager(db_path)

    # Define tables corresponding to each finger
    fingers = ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'pinky']
    
    # Initialize list to hold data and labels
    combined_data = []

    for i, finger in enumerate(fingers):
        # Load data for both channels for the current finger
        channel1_records = db_manager.get_values_from_table(finger, 1)
        channel2_records = db_manager.get_values_from_table(finger, 2)
        
        # Ensure both channels have the same number of records
        min_length = min(len(channel1_records), len(channel2_records))
        channel1_records = channel1_records[:min_length]
        channel2_records = channel2_records[:min_length]

        # Combine the data and labels
        for j in range(min_length):
            combined_data.append((channel1_records[j][2], channel2_records[j][2], i))

    db_manager.close_connection()

    # Shuffle the combined data
    random.shuffle(combined_data)

    # Separate the combined data into x1, x2, and y
    channel1_data, channel2_data, labels = zip(*combined_data)
    channel1_data = np.array(channel1_data)
    channel2_data = np.array(channel2_data)

    # Ensure the total number of data points is a multiple of INPUT_SIZE
    num_samples = len(channel1_data) - (len(channel1_data) % INPUT_SIZE)
    channel1_data = channel1_data[:num_samples]
    channel2_data = channel2_data[:num_samples]
    labels = labels[:num_samples]

    # Reshape the data
    x1 = channel1_data.reshape(-1, INPUT_SIZE)
    x2 = channel2_data.reshape(-1, INPUT_SIZE)
    y = tf.keras.utils.to_categorical(labels[:len(x1)], num_classes=5)

    return x1, x2, y

# Example usage
if __name__ == "__main__":
    dual_channel_model = create_dual_channel_model()
    isolated_channel_single_output_model = create_isolated_channel_single_output_model()
    
    dual_channel_model.summary()
    isolated_channel_single_output_model.summary()

    # Load data from database
    x1, x2, y = load_data_from_db()

    # Train the dual channel model
    dual_channel_model.fit([x1, x2], y, epochs=10, batch_size=32)
    
    # Train the isolated channel single output model
    isolated_channel_single_output_model.fit([x1, x2], y, epochs=10, batch_size=32)
    
    # Save the models
    # dual_channel_model.save('dual_channel_model.h5')
    # isolated_channel_single_output_model.save('isolated_channel_single_output_model.h5')
    
    # To load the models
    # loaded_dual_channel_model = tf.keras.models.load_model('dual_channel_model.h5')
    # loaded_isolated_channel_single_output_model = tf.keras.models.load_model('isolated_channel_single_output_model.h5')
