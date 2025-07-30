import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import (
    Input, Conv3D, MaxPool3D, Activation,
    TimeDistributed, Reshape, Dense, Dropout, Bidirectional, LSTM
)

# === Character mapping (must match training) ===
VOCAB = [x for x in "abcdefghijklmnopqrstuvwxyz'?!123456789 "]
char_to_num = tf.keras.layers.StringLookup(vocabulary=VOCAB, oov_token="")
num_to_char = tf.keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)

# === Build LipNet model ===
def build_lipnet_model():
    """
    Builds LipNet model with 46x140 input resolution and 3 pooling layers (1,2,2).
    After pooling: 46→5, 140→17 → Reshape(5*17*75) = 6375
    """
    model = Sequential([
        Input(shape=(None, 46, 140, 1), name='input_layer'),

        # Conv3D block 1
        Conv3D(128, 3, padding='same', name='conv3d_1'),
        Activation('relu', name='relu_1'),
        MaxPool3D((1, 2, 2), name='maxpool_1'),

        # Conv3D block 2
        Conv3D(256, 3, padding='same', name='conv3d_2'),
        Activation('relu', name='relu_2'),
        MaxPool3D((1, 2, 2), name='maxpool_2'),

        # Conv3D block 3
        Conv3D(75, 3, padding='same', name='conv3d_3'),
        Activation('relu', name='relu_3'),
        MaxPool3D((1, 2, 2), name='maxpool_3'),

        # Flatten per frame → 5*17*75 = 6375
        TimeDistributed(Reshape((5 * 17 * 75,)), name='reshape_per_frame'),

        TimeDistributed(Dense(128, activation='relu'), name='timedist_dense'),

        # Recurrent layers
        Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True), name='bidi_lstm_1'),
        Dropout(0.5),
        Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True), name='bidi_lstm_2'),
        Dropout(0.5),

        # Output layer (softmax)
        Dense(char_to_num.vocabulary_size() + 1, kernel_initializer='he_normal',
              activation='softmax', dtype='float32', name='output_dense')
    ])
    return model


# === Load weights ===
def load_lipnet(weights_path="models/epoch_080.weights.h5"):
    """Load pretrained weights into the correct architecture"""
    model = build_lipnet_model()
    model.load_weights(weights_path)
    return model


# === TensorFlow CTC decode ===
def load_and_predict(video_batch, model):
    """
    Perform prediction and CTC greedy decoding using tf.keras.backend.ctc_decode
    (Fixed: use .predict() to avoid SymbolicTensor error)
    """
    # Run prediction eagerly
    yhat = model.predict(video_batch)

    # Prepare input lengths for ctc_decode
    input_length = tf.cast(tf.shape(yhat)[1], dtype="int32")
    input_length = input_length * tf.ones(shape=(tf.shape(yhat)[0],), dtype="int32")

    # Decode using greedy CTC
    decoded = tf.keras.backend.ctc_decode(yhat, input_length, greedy=True)[0][0]
    return decoded


# === Predict function ===
def predict_video( model,video_tensor):
    """
    Predict text from video tensor using TensorFlow's CTC decoding
    """
    # Add batch dimension
    video_batch = np.expand_dims(video_tensor, axis=0)

    # Decode prediction
    decoded_preds = load_and_predict(video_batch, model)
    predicted_text = tf.strings.reduce_join(num_to_char(decoded_preds[0])).numpy().decode('utf-8')
    return predicted_text
