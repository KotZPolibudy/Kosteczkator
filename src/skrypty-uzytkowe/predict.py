import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model


def predict_number(model, img_path):
    img = image.load_img(img_path, target_size=(64, 64), color_mode='grayscale')
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    print(prediction)
    predicted_class = np.argmax(prediction, axis=1)
    class_names = ['1', '2', '3', '4', '5', '6', '7', '8']
    print(predicted_class)
    predicted_label = class_names[predicted_class[0]]
    return predicted_label



# Load the model
model = load_model("die_number_recognizer.keras")

print(predict_number(model, "../../data_first/data/rescaled/2/k8_5_2024-11-22_19_06_03.jpg"))

