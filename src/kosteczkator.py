import RPi.GPIO as GPIO
import time
import datetime
import os
from picamera2 import Picamera2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image, ImageFilter
import cv2

# Konfiguracja kamery
camera = Picamera2()
camera_config = camera.create_still_configuration()
camera.configure(camera_config)

# Konfiguracja GPIO
GPIO.setmode(GPIO.BCM)

# Piny silnika
IN1 = 24
IN2 = 23
ENA = 25
# Pin LED
LED = 16
# Pin przycisku
BUTTON = 17

# Konfiguracja pinów
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Wbudowany rezystor pull-up

# Konfiguracja PWM dla ENA
pwm = GPIO.PWM(ENA, 2000)  # Częstotliwość PWM: 2 kHz
pwm.start(0)  # Początkowe wypełnienie: 0%

# Oblicz wypełnienie PWM dla napięcia 5.5V
duty_cycle = 55  # Wypełnienie PWM w procentach (dla 5.5V z 12V)

# Zmienna przechowująca kierunek obrotu
global direction
direction = True  # True: zgodnie z ruchem wskazówek zegara, False: przeciwnie

global model
model = load_model("na_nowych_final_unbalanced.keras")


def process_and_crop(image_path, size=(64, 64)):
    image = Image.open(image_path).convert("RGB")
    hsv_image = image.convert("HSV")
    h, s, v = hsv_image.split()
    blurred_v = s.filter(ImageFilter.GaussianBlur(radius=5))
    v_array = np.array(blurred_v)
    threshold = 224  # You can adjust this value
    binary_mask = (v_array > threshold).astype(np.uint8) * 255

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))
    closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    mask = Image.fromarray(closed_mask)
    # masked_image = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)

    # Find bounding box of the mask and crop the image
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cropped_image = image.crop((x, y, x + w, y + h))
        try:
            resized_image = cropped_image.resize(size, Image.Resampling.LANCZOS)
        except AttributeError:
            resized_image = cropped_image.resize(size, Image.LANCZOS)

        grayscale_image = resized_image.convert("L")
        return grayscale_image
    else:
        print(f"No valid mask found for {image_path}. Skipping cropping.")
        return None


def predict_number_from_loaded_img(model, img):
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    # print(prediction)
    predicted_class = np.argmax(prediction, axis=1)
    class_names = ['1', '2', '3', '4', '5', '6', '7', '8']
    # print(predicted_class)
    predicted_label = class_names[predicted_class[0]]
    return predicted_label


# Funkcje sterowania silnikiem
def start_motor(direction):
    if direction:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(duty_cycle)  # Ustaw wypełnienie PWM

def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)  # Wyłącz sygnał PWM



def doRoll():
    global direction
    global model

    # # Kręcenie silnikiem w aktualnym kierunku
    start_motor(direction)
    # print("Silnik się kręci...")
    time.sleep(0.5)  # Czas pracy silnika
    stop_motor()
    # print("Silnik zatrzymany.")
    time.sleep(1)
    
    # Zmiana kierunku obrotów na kolejny rzut
    direction = not direction
    
    camera.start()
    camera.capture_file("last_image.jpg")
    camera.stop()
    
    img = process_and_crop("last_image.jpg")
    # image.save("last_image.jpg")
    lab = predict_number_from_loaded_img(model,img)
    num = int(lab) % 8
    return num

def genEntropy(numberOfBytes: int):
    bytes = []
    global num
    global cycle
    for _ in range(numberOfBytes):
        if cycle == 1:
            num+=doRoll()
            num = num<<3
            num+=doRoll()
            num = num<<3
            num+=doRoll()
            cycle += 1
            bytes.append(0b11111111 & num)
            num = num>>8
        elif cycle == 2:
            num+=doRoll()
            num = num<<3
            num+=doRoll()
            num = num<<3
            num+=doRoll()
            cycle = 0
            bytes.append(0b11111111 & num)
            num = num>>8
        else:
            num+=doRoll()
            num = num<<3
            num+=doRoll()
            num = num<<3
            cycle += 1
            bytes.append(0b11111111 & num)
            num = num>>8
            
    return bytes


def fillEntropy(usb:serial.Serial,numberOfBytes):
    global num
    num = 0
    while True:
        numbers = bytes(genEntropy(numberOfBytes))
        # print(numbers)
        usb.write(numbers)
        # print(f"Sent: {numbers}")
        # time.sleep(5)

def rolling(usb:serial.Serial):
    while True:
        c = usb.read()
        if(c == b'r'):
            num = doRoll()
            usb.write(num)
        

if __name__ == "__main__":
    global cycle
    cycle = 1
    
    serialPort = "/dev/ttyGS0"

    try:
        x=1
        GPIO.output(LED, GPIO.HIGH)
        # print("Świecimy")
        # fillEntropy(serialPort,1)
          
        usb = serial.Serial(serialPort)
        
        a = usb.read()
        if(a == b'e'):
            fillEntropy(usb,1)
        elif(a == b'd'):
            rolling(usb)
        else:
            print('error')      
            
        
        GPIO.output(LED, GPIO.LOW)

    finally:
        pwm.stop()  # Zatrzymaj PWM
        GPIO.cleanup()  # Wyczyść GPIO
        print("GPIO wyczyszczone.")
    
        
  


