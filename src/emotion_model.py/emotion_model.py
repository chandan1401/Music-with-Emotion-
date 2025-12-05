"""Emotion prediction model using TensorFlow."""
import cv2
import numpy as np
import tensorflow as tf
import os

# Supported emotion categories
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# Model configuration
MODEL_PATH = "models/emotion_model.h5"
FACE_SIZE = 48

# Load model
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model from {MODEL_PATH}: {e}")
        print("Please ensure the model file exists at the specified path.")
else:
    print(f"Warning: Model file not found at {MODEL_PATH}")


def predict_emotion(face):
    """
    Predict emotion from a face image.
    
    Args:
        face: Face image (BGR format from OpenCV)
        
    Returns:
        Tuple of (emotion_label, confidence_score)
        Returns ('unknown', 0.0) if model not loaded or prediction fails
    """
    if model is None:
        return 'unknown', 0.0
        
    if face is None or face.size == 0:
        return 'unknown', 0.0
        
    try:
        # Preprocess face image
        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face_resized = cv2.resize(face_gray, (FACE_SIZE, FACE_SIZE))
        face_normalized = face_resized.astype('float32') / 255.0
        face_input = np.expand_dims(face_normalized, axis=[0, -1])
        
        # Predict emotion
        predictions = model.predict(face_input, verbose=0)[0]
        emotion_idx = predictions.argmax()
        confidence = float(predictions[emotion_idx])
        
        return EMOTIONS[emotion_idx], confidence
        
    except Exception as e:
        print(f"Error in emotion prediction: {e}")
        return 'unknown', 0.0
