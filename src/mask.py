from PIL import Image, ImageFilter, ImageOps, ImageMorph
import numpy as np
import cv2
import glob
from pathlib import Path


def process(image_path, output_path):
    # Load the image
    image = Image.open(image_path).convert("RGB")

    # Convert the image to HSV
    hsv_image = image.convert("HSV")

    # Extract channels
    h, s, v = hsv_image.split()

    # Apply a blur to the Saturation channel
    blurred_v = s.filter(ImageFilter.GaussianBlur(radius=5))

    # Convert to numpy array for thresholding
    v_array = np.array(blurred_v)

    # Apply thresholding
    threshold = 224  # You can adjust this value
    binary_mask = (v_array > threshold).astype(np.uint8) * 255

    # Convert the mask back to a Pillow Image
    mask = Image.fromarray(binary_mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))
    closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    mask = Image.fromarray(closed_mask)

    # Apply the mask to the original image
    result = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)

    # Save and show the result
    result.save(output_path)


for input_fn in glob.glob('foty_kostek/*/*.jpg'):
    input_fn = Path(input_fn)
    output_fn = Path('output') / input_fn
    output_fn.parent.mkdir(parents=True, exist_ok=True)
    print(input_fn)
    process(input_fn, output_fn)