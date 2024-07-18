import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate, Add
from tensorflow.keras.optimizers import Adam

# Constants
INPUT_SIZE = 100  # Number of nodes in each input layer
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

# Example usage
if __name__ == "__main__":
    dual_channel_model = create_dual_channel_model()
    isolated_channel_single_output_model = create_isolated_channel_single_output_model()
    
    dual_channel_model.summary()
    isolated_channel_single_output_model.summary()
    
    # Generate some dummy data for demonstration
    x1 = np.random.random((32, INPUT_SIZE))
    x2 = np.random.random((32, INPUT_SIZE))
    y = np.random.randint(5, size=(32, 1))
    y = tf.keras.utils.to_categorical(y, num_classes=5)
    
    # Train the dual channel model
    dual_channel_model.fit([x1, x2], y, epochs=10, batch_size=32)
    
    # Train the isolated channel single output model
    isolated_channel_single_output_model.fit([x1, x2], y, epochs=10, batch_size=32)
    
    # Save the models
    dual_channel_model.save('dual_channel_model.h5')
    isolated_channel_single_output_model.save('isolated_channel_single_output_model.h5')
    
    # To load the models
    # loaded_dual_channel_model = tf.keras.models.load_model('dual_channel_model.h5')
    # loaded_isolated_channel_single_output_model = tf.keras.models.load_model('isolated_channel_single_output_model.h5')
