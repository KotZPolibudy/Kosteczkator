import shutil
from pathlib import Path
from tensorflow.keras.models import load_model
from predict import predict_number  # Import the predict_number function from predict.py


def process_and_move_images(input_base, output_base, model, class_names):
    """
    Predicts the class of all .jpg images in input_base and moves them to the corresponding
    subfolders in output_base based on their predicted class.

    Args:
        input_base (str or Path): Base directory containing the images to process.
        output_base (str or Path): Base directory where images will be moved.
        model: Loaded Keras model for prediction.
        class_names (list): List of all possible class names.
    """
    input_base = Path(input_base)
    output_base = Path(output_base)

    # Pre-create all class subdirectories
    for class_name in class_names:
        target_dir = output_base / class_name
        target_dir.mkdir(parents=True, exist_ok=True)
    print("All class folders created successfully.")

    # Iterate over all .jpg files in the input directory and its subdirectories
    for img_path in input_base.rglob("*.jpg"):
        print(f"Processing: {img_path}...")

        try:
            # Predict the class label
            predicted_class = predict_number(model, img_path)

            # Define the target directory for this class
            target_dir = output_base / predicted_class

            # Define the new path for the image
            target_path = target_dir / img_path.name

            # Move the image to the target directory
            shutil.move(str(img_path), str(target_path))
            print(f"Moved: {img_path} --> {target_path}")

        except Exception as e:
            print(f"Failed to process {img_path}: {e}")


if __name__ == "__main__":
    # Paths to input and output directories
    input_folder = "../data/TO-BE-LABELED"  # Folder with images to process
    output_folder = "../data/TO-BE-LABELCHECKED"  # Base folder for labeled images

    # List of class names (predefined based on model training)
    class_names = ['1', '2', '3', '4', '5', '6', '7', '8']

    # Load the pre-trained model
    model_path = "die_number_recognizer.keras"
    model = load_model(model_path)
    print("Model loaded successfully.")

    # Process images and move them
    process_and_move_images(input_folder, output_folder, model, class_names)
    print("Processing complete.")
