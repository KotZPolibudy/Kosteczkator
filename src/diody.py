import RPi.GPIO as GPIO
import time
import datetime
import os
from picamera2 import Picamera2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

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
dioda_red = 26
dioda_blue = 6
dioda_green = 5

# Konfiguracja pinów
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(dioda_red, GPIO.OUT)
GPIO.setup(dioda_blue, GPIO.OUT)
GPIO.setup(dioda_green, GPIO.OUT)

# Konfiguracja PWM dla ENA
pwm = GPIO.PWM(ENA, 2000)  # Częstotliwość PWM: 2 kHz
pwm.start(0)  # Początkowe wypełnienie: 0%

# Oblicz wypełnienie PWM dla napięcia 5.5V
duty_cycle = 100  # Wypełnienie PWM w procentach (dla 5.5V z 12V)

# Zmienna przechowująca kierunek obrotu
direction = True  # True: zgodnie z ruchem wskazówek zegara, False: przeciwnie

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


# predict function
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

try:
    # Load the model
    model = load_model("die_number_recognizer.keras")
    while True:
        print("Podaj liczbę zdjęć, jakie chcesz zrobić:")
        x = int(input())  # Konwertuj na liczbę całkowitą
        
        # Tworzenie nowego folderu dla serii zdjęć
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"seria_{timestamp}"
        os.makedirs(folder_name, exist_ok=True)  # Tworzy folder, jeśli nie istnieje
        #print(f"Utworzono folder: {folder_name}")
        
        GPIO.output(LED, GPIO.HIGH)
        GPIO.output(dioda_red, GPIO.HIGH)
        
        for n in range(x):
            start_time = time.time()  # Zapisz czas rozpoczęcia iteracji
            
            
            # Kręcenie silnikiem w aktualnym kierunku
            start_motor(direction)
            #print("Silnik się kręci...")
            GPIO.output(dioda_green, GPIO.HIGH)
            time.sleep(0.3)  # Czas pracy silnika
            stop_motor()
            #print("Silnik zatrzymany.")
            GPIO.output(dioda_green, GPIO.LOW)
            time.sleep(1)
            
            # Zmiana kierunku obrotów na kolejny rzut
            direction = not direction
            
            # Robienie zdjęcia
            GPIO.output(dioda_blue, GPIO.HIGH)
            t = datetime.datetime.now()
            t_str = t.strftime("%Y-%m-%d_%H-%M-%S")
            title = f"{folder_name}/{n + 1}_{t_str}.jpg"  # Ścieżka do zdjęcia
            
            camera.start()
            camera.capture_file(title)
            camera.stop()
            GPIO.output(dioda_blue, GPIO.LOW)
            #print(f"Zdjęcie zapisane jako {title}")

            prediction = predict_number(model, title)
            
            end_time = time.time()  # Zapisz czas zakończenia iteracji
            iteration_time = end_time - start_time
            
            # Zapisz czas wykonania iteracji do pliku w folderze
            with open(f"{folder_name}/czas_iteracji.txt", "a") as file:
                file.write(f"{title} ; {iteration_time:.2f} ; {prediction}\n")
        
        GPIO.output(LED, GPIO.LOW)
        GPIO.output(dioda_red, GPIO.LOW)

finally:
    pwm.stop()  # Zatrzymaj PWM
    GPIO.cleanup()  # Wyczyść GPIO
    print("GPIO wyczyszczone.")
