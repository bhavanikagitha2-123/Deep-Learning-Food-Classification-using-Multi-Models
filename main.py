import os
import shutil
import random
input_dir = r"C:\Users\BHAVANI\Downloads\food_internship\Food Classification dataset"
output_dir = r"C:\Users\BHAVANI\Downloads\food_internship\Selected_200_Images"


os.makedirs(output_dir, exist_ok=True)
for class_name in sorted(os.listdir(input_dir)):
    class_path = os.path.join(input_dir, class_name)

    if not os.path.isdir(class_path):
        continue


    output_class_path = os.path.join(output_dir, class_name)
    os.makedirs(output_class_path, exist_ok=True)

    images = [img for img in os.listdir(class_path)
              if img.lower().endswith(('.jpg', '.jpeg'))]

    print(f"Class: {class_name} | Total JPEG images found: {len(images)}")

    selected_images = random.sample(images, min(200, len(images)))


    for img in selected_images:
        src = os.path.join(class_path, img)
        dst = os.path.join(output_class_path, img)
        shutil.copy(src, dst)

    print(f" Saved {len(selected_images)} images -> {output_class_path}")

print("\n DONE! 200 JPEG images per class created successfully.")
