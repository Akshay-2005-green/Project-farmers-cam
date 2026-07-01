import os

# Change this path
dataset_path = r"C:\Users\aksha\Downloads\archive\PlantVillageDataset\train_val_test"

for folder in ["train", "val", "test"]:

    print("\n", "="*40)
    print(folder.upper())
    print("="*40)

    folder_path = os.path.join(dataset_path, folder)

    total = 0

    classes = os.listdir(folder_path)

    print("Number of Classes :", len(classes))
    print()

    for cls in sorted(classes):

        count = len(os.listdir(os.path.join(folder_path, cls)))

        total += count

        print(f"{cls:40} {count}")

    print("\nTotal Images :", total)