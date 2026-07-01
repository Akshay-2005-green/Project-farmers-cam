import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import models
from tensorflow.keras import layers

IMG_SIZE = (224,224)
BATCH_SIZE = 32

train_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\train"
val_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\val"
test_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\test"

# Load dataset

train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_path,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_dataset = tf.keras.utils.image_dataset_from_directory(
    val_path,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_path,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Normalize

normalization_layer = layers.Rescaling(1./255)

train_dataset = train_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

val_dataset = val_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

test_dataset = test_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

# Data Augmentation

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2)
])

base_model = MobileNetV2(
    input_shape=(224,224,3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = models.Sequential([
    data_augmentation,
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(128, activation="relu"),
    layers.Dense(15, activation="softmax")
])

model.build((None,224,224,3))
model.summary()

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
EPOCHS = 3
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS
)

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS
)

test_loss, test_accuracy = model.evaluate(test_dataset)

print(f"Test Accuracy: {test_accuracy:.4f}")

model.save("saved_model/crop_disease_model.keras")

print("Model Saved Successfully!")