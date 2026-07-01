from ai.predict_utils import predict_image

image_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\test\Potato___Late_blight\123.jpg"

disease, confidence = predict_image(image_path)

print("Disease :", disease)
print("Confidence :", confidence)