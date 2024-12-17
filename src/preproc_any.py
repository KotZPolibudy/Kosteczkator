from PIL import Image, ImageFilter
import numpy as np
import cv2
from pathlib import Path


def process_and_crop(image_path, size=(64, 64)):
    image = Image.open(image_path).convert("RGB")
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()
    blurred_v = s.filter(ImageFilter.GaussianBlur(radius=5))
    v_array = np.array(blurred_v)
    threshold = 224  # You can adjust this value
    binary_mask = (v_array > threshold).astype(np.uint8) * 255

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))
    closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    mask = Image.fromarray(closed_mask)
    masked_image = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)

    # Find bounding box of the mask and crop the image
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cropped_image = image.crop((x, y, x + w, y + h))
        resized_image = cropped_image.resize(size, Image.Resampling.LANCZOS)
        grayscale_image = resized_image.convert("L")
        return grayscale_image
    else:
        print(f"No valid mask found for {image_path}. Skipping cropping.")
        return None


def process_images_in_directory(input_base):
    input_base = Path(input_base)
    all_skipped = []
    # Iterate through all JPG files (recursively)
    for image_path in input_base.rglob("*.jpg"):
        # print(f"Processing {image_path}...")
        output_image = process_and_crop(image_path)
        if output_image:
            output_image.save(image_path)
            print(f"Replaced: {image_path}")
        else:
            print(f"Skipped: {image_path}")
            all_skipped.append(image_path)
            # image_path.unlink()
            # print(f"Deleted: {image_path}")
    print(all_skipped)


if __name__ == "__main__":
    input_folder = "../data/TO-BE-LABELED"  # Change this to your input folder path
    process_images_in_directory(input_folder)
