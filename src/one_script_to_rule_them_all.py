from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import argparse
from PIL import Image, ImageEnhance
import pytesseract
import os


def detect_die(image_path, output_path="cropped_die.jpg"):
    # Load the YOLO model
    model = YOLO("yolov8n.pt")  # Replace with your custom model if available

    # Run inference on the input image
    results = model(image_path)

    # Load the original image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load the image.")
        return

    # Get image dimensions
    img_height, img_width, _ = image.shape

    # Loop through detected objects
    die_found = False
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # Bounding box coordinates
        confidence = result.conf[0]  # Confidence score
        width, height = x2 - x1, y2 - y1
        aspect_ratio = width / float(height)

        # Filtering criteria
        if confidence > 0.5 and 0.8 < aspect_ratio < 1.2:  # High confidence and square shape
            # Ensure the bounding box is not too large (exclude the cup bottom)
            if width < 0.5 * img_width and height < 0.5 * img_height:  # Adjust size thresholds
                # Crop the detected die
                cropped_die = image[y1:y2, x1:x2]
                cv2.imwrite(output_path, cropped_die)
                print(f"Cropped die saved to {output_path}")
                die_found = True

                # Display the cropped die
                plt.imshow(cv2.cvtColor(cropped_die, cv2.COLOR_BGR2RGB))
                plt.title("Cropped Die")
                plt.axis("off")
                plt.show()

                break

    if not die_found:
        print("No dice was detected in the image.")
    return die_found


def preprocess_image(image):
    # Convert the image to grayscale
    img = image.convert("L")

    # Increase the contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3)  # You can adjust the factor to increase or decrease contrast

    return img


def show_images(original, processed):
    # Create a figure to show original and processed images side by side
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Display original image
    axes[0].imshow(original)
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    # Display processed image
    axes[1].imshow(processed, cmap='gray')
    axes[1].set_title("Processed Image (High Contrast)")
    axes[1].axis("off")

    plt.show()  # DEBUG: Show the images


def read_number_from_image(image_path):
    try:
        img = Image.open(image_path)
        processed_img = preprocess_image(img)
        show_images(img, processed_img)  # DEBUG: Show the original and processed images

        # Use Tesseract to do OCR on the image
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        print("Extracted Text: ", text)

        # Strip any non-numeric characters and whitespace
        number = ''.join(filter(str.isdigit, text))

        if number:
            return int(number)
        else:
            print("No number found.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    input_image_path = "../data/3/k8_5_2024-11-22_19_23_08.jpg"  # Replace with your image path
    output_image_path = "../data/cropped/cropped_die.jpg"  # Path to save the cropped image
    if not os.path.exists(input_image_path):
        print(f"Error: Image path {input_image_path} does not exist.")
        return
    if not os.path.exists(os.path.dirname(output_image_path)):
        os.makedirs(os.path.dirname(output_image_path))
    found = detect_die(input_image_path, output_image_path)
    if not found:
        print(f"Error: No dice found ")
        return
    number = read_number_from_image(output_image_path)
    if not number:
        print(f"Error: No number found on dice")
    print(f"Extracted Number: {number}")


# Run the function
if __name__ == "__main__":
    main()


# todo
# To jest sklejka dwóch kodów, oczywiście że używają innych lib'ek do obsługi obrazków - trzeba to naprawić.
# A i żeby było lepiej, to żadna z części, czyli ani czytanie, ani wykrywanie kostki, nie działają perfekcyjnie.
# Wykrywanie kostki zadziała, ale sporadycznie, może 1/10 wykryje, z czego 3/5 wykrytych to nie są kości.
# Odczytywanie działa, coś czyta, ale prawie nigdy dobrze obecnie.
# No więc jest słabo :((
