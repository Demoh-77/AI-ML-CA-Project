import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

def build_autoencoder(input_dim):
    input_layer = Input(shape=(input_dim,))
    x = Dense(128, activation='relu')(input_layer)
    x = Dense(64, activation='relu')(x)
    x = Dense(32, activation='relu')(x)
    bottleneck = Dense(16, activation='relu')(x)
    x = Dense(32, activation='relu')(bottleneck)
    x = Dense(64, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    output_layer = Dense(input_dim, activation='linear')(x)

    autoencoder = Model(inputs=input_layer, outputs=output_layer)
    autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return autoencoder

def compute_anomaly_scores(autoencoder, X):
    reconstructions = autoencoder.predict(X, verbose=0)
    return np.mean(np.square(X - reconstructions), axis=1)