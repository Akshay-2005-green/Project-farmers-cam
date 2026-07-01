import tensorflow as tf
import matplotlib.pyplot as plt

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\train"
val_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\val"
test_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test\test"

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
    batch_size=BATCH_SIZE,
    shuffle=False
)

print("Classes:")
print(train_dataset.class_names)

print("\nNumber of Classes:", len(train_dataset.class_names))

plt.figure(figsize=(12, 12))

for images, labels in train_dataset.take(1):

    for i in range(9):

        plt.subplot(3, 3, i + 1)

        plt.imshow(images[i].numpy().astype("uint8"))

        plt.title(train_dataset.class_names[labels[i]])

        plt.axis("off")

plt.tight_layout()

plt.show()