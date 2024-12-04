import argparse
from PIL import Image, ImageEnhance
import pytesseract
import matplotlib.pyplot as plt
import glob


# If Tesseract is not in your PATH, uncomment and adjust the line below
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

    # Show the images
    plt.show()


def read_number_from_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)

        # Preprocess the image to increase contrast
        processed_img = preprocess_image(img)

        # Show the original and processed images
        show_images(img, processed_img)

        # Use Tesseract to do OCR on the image
        # psm 6 - block text
        # psm 10 - single character
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
    # Set up argument parser
    # parser = argparse.ArgumentParser(description="Extract a numeric value from an image using Tesseract OCR.")
    # parser.add_argument("image_path", help="Path to the image file containing the number")

    # Parse arguments
    # args = parser.parse_args()

    # Read the number from the image
    # number = read_number_from_image(args.image_path)
    # path = "../data/7/k8_5_2024-11-22_19_24_24.jpg"
    """i = 0
    for input_fn in glob.glob('./data/cropped/1/*.jpg'):
        i += 1
        number = read_number_from_image(input_fn)
        if number is not None:
            print(f"Extracted Number: {number}")
        if i > 5:
            break"""
    path = "../data/cropped/3/k8_5_2024-11-22_19_06_13.jpg"
    number = read_number_from_image(path)
    print(number)


if __name__ == "__main__":
    main()
