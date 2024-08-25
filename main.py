# main.py
import tensorflow as tf
import numpy as np
import cv2
from config import NUM_CLASSES


def predict_digit(image_path):
    model = tf.keras.models.load_model('digit_recognition_model.h5')

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28))
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0

    prediction = model.predict([img])
    return np.argmax(prediction)


if __name__ == "__main__":
    image_path = './data/test/20240822_141459.jpg'
    digit = predict_digit(image_path)
    print(f"The digit in the image is: {digit}")
