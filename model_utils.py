from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("saved_model/crop_disease_model.keras")

print("AI Model Loaded Successfully!")