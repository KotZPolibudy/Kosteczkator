from PIL import Image, ImageFilter, ImageOps
import numpy as np
import cv2
import glob
from pathlib import Path

def process_and_crop(image_path, masked_output_path, cropped_output_path):
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

    # Apply morphological closing to the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))
    closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)

    # Create the mask image
    mask = Image.fromarray(closed_mask)

    # Create the masked image
    masked_image = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)

    # Save the masked image
    masked_image.save(masked_output_path)
    print(f"Saved masked image to {masked_output_path}")

    # Find bounding box of the mask and crop the image
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Get bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cropped_image = image.crop((x, y, x + w, y + h))

        # Save the cropped image
        cropped_image.save(cropped_output_path)
        print(f"Saved cropped image to {cropped_output_path}")
        return cropped_image  # Return cropped image for further processing
    else:
        print(f"No valid mask found for {image_path}. Skipping cropping.")
        return None

def rescale_image(image, output_path, size=(64, 64)):
    # Resize the image
    resized_image = image.resize(size, Image.ANTIALIAS)

    # Save the resized image
    resized_image.save(output_path)
    print(f"Saved resized image to {output_path}")


# Main loop to process images
input_base = Path("../data/raw")   # Base input directory
masked_output_base = Path("../data/masked")  # Base masked output directory
cropped_output_base = Path("../data/cropped")  # Base cropped output directory
rescaled_output_base = Path("../data/rescaled")  # Base rescaled output directory

for input_fn in glob.glob(str(input_base / "*/*.jpg")):  # Match all JPG files in subdirectories
    input_fn = Path(input_fn)

    # Derive the corresponding masked and cropped output paths
    relative_path = input_fn.relative_to(input_base)  # Get path relative to input base
    masked_output_fn = masked_output_base / relative_path  # Combine with masked output base
    cropped_output_fn = cropped_output_base / relative_path  # Combine with cropped output base
    rescaled_output_fn = rescaled_output_base / relative_path  # Combine with rescaled output base

    # Create directories for the output files if they don't exist
    masked_output_fn.parent.mkdir(parents=True, exist_ok=True)
    cropped_output_fn.parent.mkdir(parents=True, exist_ok=True)
    rescaled_output_fn.parent.mkdir(parents=True, exist_ok=True)

    # Process the image and save both outputs
    cropped_image = process_and_crop(input_fn, masked_output_fn, cropped_output_fn)

    # If a cropped image was successfully created, rescale it
    if cropped_image:
        rescale_image(cropped_image, rescaled_output_fn, size=(64, 64))
