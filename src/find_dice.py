from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt


def detect_die(image_path, output_path="cropped_die.jpg"):
    # Load the YOLO model (pre-trained or fine-tuned)
    model = YOLO("yolov8n.pt")  # Replace with your custom model if available

    # Run inference on the input image
    results = model(image_path)

    # Load the original image
    image = cv2.imread(image_path)

    # Loop through the detected objects
    die_found = False
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # Bounding box coordinates
        confidence = result.conf[0]  # Confidence score
        label = result.cls[0]  # Object class

        # Optional: Filter by confidence or specific class (if you train a custom dice model)
        if confidence > 0.5:  # Adjust threshold as needed
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
        print("No die was detected in the image.")


# Run the function
if __name__ == "__main__":
    input_image_path = "../data/7/k8_5_2024-11-22_19_24_24.jpg"  # Replace with your image path
    output_image_path = "../data/cropped/cropped_die.jpg"  # Path to save the cropped image
    detect_die(input_image_path, output_image_path)
