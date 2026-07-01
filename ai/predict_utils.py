import numpy as np
from PIL import Image

from model_utils import model
from classes import CLASS_NAMES


def predict_image(image_path):
    # Open image
    image = Image.open(image_path).convert("RGB")

    # Resize image
    image = image.resize((224, 224))

    # Convert to numpy array
    image = np.array(image)

    # Normalize
    image = image / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Prediction
    prediction = model.predict(image)

    # Highest probability
    predicted_index = np.argmax(prediction)

    # Confidence
    confidence = float(np.max(prediction)) * 100

    # Disease name
    disease = CLASS_NAMES[predicted_index]

    return disease, confidence