import RPi.GPIO as GPIO
import time

def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temp_str = file.read().strip()
        return int(temp_str) / 1000  # Convert from millidegrees Celsius to degrees Celsius

# Konfiguracja GPIO
GPIO.setmode(GPIO.BCM)

# Pin wentylatora
Fan = 22

# Konfiguracja pinu wentylatora
GPIO.setup(Fan, GPIO.OUT)
GPIO.output(Fan, GPIO.LOW)  # Wyłącz wentylator na start


try:
    fan_active = False  # Czy wentylator jest aktualnie włączony

    while True:
        cpu_temp = get_cpu_temperature()
        
        if cpu_temp > 55 and not fan_active:
            GPIO.output(Fan, GPIO.HIGH)
            fan_active = True
        elif cpu_temp < 50 and fan_active:
            GPIO.output(Fan, GPIO.LOW)
            fan_active = False

        time.sleep(1)  # Sprawdzaj temperaturę co 1 sekundę
        print(f"CPU Temperature: {cpu_temp}°C, Fan Active: {fan_active}")


finally:
    GPIO.cleanup()  # Wyczyść GPIO po zakończeniu
    print("GPIO wyczyszczone.")
