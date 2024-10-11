import os
from PIL import Image


def resize_images(input_folder, output_folder, size=(64, 64)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            img.save(os.path.join(output_folder, filename))
            print(f"Resized and saved {filename}")


if __name__ == "__main__":
    input_folder = 'input'  # Replace with the path to your input folder
    output_folder = 'input_trans'  # Replace with the path to your output folder
    resize_images(input_folder, output_folder)