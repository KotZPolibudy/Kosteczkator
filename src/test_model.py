import os
import numpy as np
from tensorflow.keras.preprocessing import image
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model
from PIL import Image

# Funkcja do ładowania obrazów i ich etykiet z folderu
def load_images_from_folder(folder_path, target_size=(64, 64)):
    images = []
    labels = []
    class_names = sorted(os.listdir(folder_path))
    print(class_names)
    for label in class_names:
        class_folder = os.path.join(folder_path, label)
        if os.path.isdir(class_folder):
            for img_name in os.listdir(class_folder):
                img_path = os.path.join(class_folder, img_name)
                try:
                    img = image.load_img(img_path, target_size=target_size, color_mode='grayscale')  # Wczytanie obrazu
                    img_array = image.img_to_array(img) / 255.0  # Normalizacja
                    images.append(img_array)
                    labels.append(int(label))
                except Exception as e:
                    print(f"Nie udało się wczytać obrazu {img_path}: {e}")
    return np.array(images), np.array(labels)


# Ścieżka do folderu z danymi testowymi
test_folder = "../data/test_data"

# Wczytanie modelu
model = load_model("na_nowych_final_unbalanced.keras")
X_test, y_test = load_images_from_folder(test_folder)

# Przewidywanie klas dla danych testowych
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)
class_names = ['1', '2', '3', '4', '5', '6', '7', '8']

y_test_adjusted = y_test - 1  # Przesunięcie etykiet o -1, bo tak z treningiem wychodzi

# to tylko debug ;)
# for root, dirs, files in os.walk(test_folder):
#     print("Podfoldery (klasy):", dirs)

# print("Unikalne klasy w y_test:", np.unique(y_test))  # Sprawdź klasy w danych testowych
# print("Unikalne klasy w y_pred:", np.unique(y_pred))  # Sprawdź klasy w przewidywaniach


# Wyświetlenie macierzy konfuzji
conf_matrix = confusion_matrix(y_test_adjusted, y_pred)
print("Confusion matrix:")
print(conf_matrix)


# Wyświetlenie statystyk
report = classification_report(y_test_adjusted, y_pred, target_names=class_names)
print("Raport:")
print(report)
