from PIL import Image, ImageFilter, ImageOps
import numpy as np
import cv2
import glob
from pathlib import Path

def process_and_crop(image_path, masked_output_path, cropped_output_path):
    image = Image.open(image_path).convert("RGB")
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()
    blurred_v = s.filter(ImageFilter.GaussianBlur(radius=5))
    v_array = np.array(blurred_v)
    threshold = 224
    binary_mask = (v_array > threshold).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))
    closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    mask = Image.fromarray(closed_mask)
    masked_image = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)
    # masked_image.save(masked_output_path)
    # print(f"Saved masked image to {masked_output_path}")
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cropped_image = image.crop((x, y, x + w, y + h))
        # cropped_image.save(cropped_output_path)
        # print(f"Saved cropped image to {cropped_output_path}")
        return cropped_image  # Return cropped image for further processing
    else:
        print(f"No valid mask found for {image_path}. Skipping cropping.")
        return None

def rescale_image_and_gray(image, output_path, size=(64, 64)):
    resized_image = image.resize(size, Image.Resampling.LANCZOS)
    # resized_image.save(output_path)
    grayscale_image = resized_image.convert("L")
    grayscale_image.save(output_path)
    print(f"Saved resized image to {output_path}")


input_base = Path("../../data/raw")
masked_output_base = Path("../data/masked")
cropped_output_base = Path("../data/cropped")
rescaled_output_base = Path("../../data/rescaled")
gray_output_base = Path("../../data/gray")

for input_fn in glob.glob(str(input_base / "*/*.jpg")):
    input_fn = Path(input_fn)
    relative_path = input_fn.relative_to(input_base)
    masked_output_fn = masked_output_base / relative_path
    cropped_output_fn = cropped_output_base / relative_path
    rescaled_output_fn = rescaled_output_base / relative_path
    gray_output_fn = gray_output_base / relative_path

    # Create directories for the output files if they don't exist
    # masked_output_fn.parent.mkdir(parents=True, exist_ok=True)
    # cropped_output_fn.parent.mkdir(parents=True, exist_ok=True)
    # rescaled_output_fn.parent.mkdir(parents=True, exist_ok=True)
    gray_output_fn.parent.mkdir(parents=True, exist_ok=True)

    cropped_image = process_and_crop(input_fn, masked_output_fn, cropped_output_fn)

    if cropped_image:
        rescale_image_and_gray(cropped_image, gray_output_fn, size=(64, 64))
