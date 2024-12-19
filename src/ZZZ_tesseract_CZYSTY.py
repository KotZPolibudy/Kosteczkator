import cv2
import pytesseract
import glob


def process_die_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance contrast
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # (Optional) Apply a median blur to reduce noise
    blurred = cv2.medianBlur(thresh, 3)

    # Use Tesseract OCR to detect numbers
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=12345678'  # Assume single character and 1-8 digits
    detected_text = pytesseract.image_to_string(blurred, config=custom_config)

    # Clean up the result
    number = detected_text.strip()
    return number


if __name__ == "__main__":
    numnum = []
    for num in range(1, 9):
        numbers = []
        for input_fn in glob.glob(f'../data/cropped/{num}/*.jpg'):
            print(f"File: {input_fn}")
            number = process_die_image(input_fn)
            numbers.append(number)
        numnum.append(numbers)
    for el in numnum:
        print(f"{numnum.index(el) +1} : {el}")
