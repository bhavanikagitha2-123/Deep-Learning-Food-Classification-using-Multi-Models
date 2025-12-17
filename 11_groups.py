import os
import shutil
import random

base_dir = r"C:\Users\BHAVANI\Downloads\food_internship\Selected_200_Images"
output_dir = r"C:\Usersr\BHAVANI\Downloads\food_internship\Split_Data_11"


splits = ["train", "val", "test"]
for split in splits:
    os.makedirs(os.path.join(output_dir, split), exist_ok=True)


for split in splits:
    for i in range(1, 12):  # 1 to 11
        os.makedirs(os.path.join(output_dir, split, f"group_{i}"), exist_ok=True)

train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

class_list = sorted(os.listdir(base_dir))
group_count = 11
group_index = 0

for class_name in class_list:
    class_path = os.path.join(base_dir, class_name)

    if not os.path.isdir(class_path):
        continue

    print(f"Processing class: {class_name}")


    assigned_group = f"group_{(group_index % group_count) + 1}"
    group_index += 1


    for split in splits:
        os.makedirs(os.path.join(output_dir, split, assigned_group, class_name), exist_ok=True)

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
        shutil.copy(
            os.path.join(class_path, img),
            os.path.join(output_dir, "train", assigned_group, class_name, img)
        )

    for img in val_imgs:
        shutil.copy(
            os.path.join(class_path, img),
            os.path.join(output_dir, "val", assigned_group, class_name, img)
        )

    for img in test_imgs:
        shutil.copy(
            os.path.join(class_path, img),
            os.path.join(output_dir, "test", assigned_group, class_name, img)
        )

    print(f" Group: {assigned_group} | Train: {len(train_imgs)}, Val: {len(val_imgs)}, Test: {len(test_imgs)}")

print("\n DONE — Dataset successfully split into 11 groups for train/val/test.")
