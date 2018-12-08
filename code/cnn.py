import numpy as np

import keras
from keras.models import Sequential, Model
from keras.layers import Input, Embedding, Dense, Flatten, Conv1D, MaxPooling1D

def build_model(embedding_matrix):
    
    embedding_layer = Embedding(185674, 300, weights=[embedding_matrix], input_length=2000, trainable=False)
    sequence_input = Input(shape=(2000,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)
    x = Conv1D(128, 5, activation='relu')(embedded_sequences)
    x = MaxPooling1D(5)(x)
    x = Conv1D(128, 5, activation='relu')(x)
    x = MaxPooling1D(5)(x)
    x = Conv1D(128, 5, activation='relu')(x)
    x = MaxPooling1D(35)(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    preds = Dense(1, activation='sigmoid')(x)

    model = Model(sequence_input, preds)
    return model

if __name__ == "__main__":

    X_train_Q = np.load('../data/numpy_array/train_Q_index.npy')
    X_train_A = np.load('../data/numpy_array/train_A_index.npy')
    X_train = np.concatenate((X_train_Q, X_train_A), axis=1)
    X_val_Q = np.load('../data/numpy_array/validation_Q_index.npy')
    X_val_A = np.load('../data/numpy_array/validation_A_index.npy')
    X_val = np.concatenate((X_val_Q, X_val_A), axis=1)
    Y_train = np.load('../data/numpy_array/train_label.npy')
    Y_val = np.load('../data/numpy_array/validation_label.npy')
    embedding_matrix = np.load('../data/numpy_array/word_vector.npy')
    
    model = build_model(embedding_matrix)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=10, batch_size=100)
        
    