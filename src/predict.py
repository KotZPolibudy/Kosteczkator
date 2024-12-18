import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import glob


def predict_number(model, img_path):
    # Load the image in grayscale mode to match the model input
    img = image.load_img(img_path, target_size=(64, 64), color_mode='grayscale')  # Ensure grayscale input
    img_array = image.img_to_array(img) / 255.0  # Rescale pixel values to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension (since the model expects a batch)

    # Make prediction
    prediction = model.predict(img_array)  # Get the model's predictions for the image
    print(prediction)
    predicted_class = np.argmax(prediction, axis=1)  # Get the class with the highest probability

    # List of class labels (from 1 to 8 for dice numbers)
    class_names = ['1', '2', '3', '4', '5', '6', '7', '8']
    print(predicted_class)
    # Return the predicted label (the number corresponding to the class)
    predicted_label = class_names[predicted_class[0]]
    return predicted_label



# Load the model
model = load_model("die_number_recognizer.keras")

"""
numnum = []
for num in range(1, 9):
    numbers = []
    for input_fn in glob.glob(f'../data_first/data/rescaled/{num}/*.jpg'):
        number = predict_number(model, input_fn)
        # print(f"File: {input_fn} -- prediction : {number}")
        numbers.append(number)
    numnum.append(numbers)
# wyniki
for el in numnum:
    print(f"{numnum.index(el) +1} : {el}")
"""

# print(predict_number(model, "../data/other/9-do analizy potem/100_2024-12-10_14-26-39.jpg"))

# print(predict_number(model, "../data/rescaled/6/20_2024-12-10_13-14-03.jpg"))

print(predict_number(model, "../data_first/data/rescaled/2/k8_5_2024-11-22_19_06_03.jpg"))

