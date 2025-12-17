import os
import shutil
import random


base_dir = r"C:\Users\BHAVANI\Downloads\food_internship\Selected_200_Images"
output_dir = r"C:\Users\BHAVANI\Downloads\food_internship\Split_Data_200"


splits = ["train", "val", "test"]
for split in splits:
    os.makedirs(os.path.join(output_dir, split), exist_ok=True)


train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15


for class_name in sorted(os.listdir(base_dir)):
    class_path = os.path.join(base_dir, class_name)

    if not os.path.isdir(class_path):
        continue

    print(f"Processing class: {class_name}")


    for split in splits:
        os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)


    images = [img for img in os.listdir(class_path)
              if img.lower().endswith(('.jpg', '.jpeg'))]

    random.shuffle(images)

    total = len(images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_imgs = images[:train_end]
    val_imgs = images[train_end:val_end]
    test_imgs = images[val_end:]


    for img in train_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(output_dir, "train", class_name, img))

    for img in val_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(output_dir, "val", class_name, img))

    for img in test_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(output_dir, "test", class_name, img))

    print(f" Train: {len(train_imgs)}, Val: {len(val_imgs)}, Test: {len(test_imgs)}")

print("\n DONE Dataset successfully split into train/val/test folders.")
