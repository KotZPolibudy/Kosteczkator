import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, save_img

# Ustawienia parametrów dla transformacji
rotation_range = 90
width_shift_range = 0.2
height_shift_range = 0.2
shear_range = 3
zoom_range = 0.3

# Ścieżki
image_path = "../../Pracka/chapters/04-czytanie/figures/5_preprocessed.jpg"  # Zmień na odpowiednią ścieżkę
output_dir = "transformed_images"  # Folder na zapisane obrazy
os.makedirs(output_dir, exist_ok=True)


# Funkcja do zapisywania obrazów
def save_images(images, folder_name):
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    for idx, img in enumerate(images):
        save_path = os.path.join(folder_path, f"{folder_name}_{idx + 1}.jpg")
        save_img(save_path, img[0])  # Usuń wymiar batcha przed zapisaniem


# Funkcja do wyświetlania obrazów
def plot_images(images, titles):
    num_images = len(images)
    cols = min(5, num_images)  # Maksymalnie 5 kolumn
    rows = (num_images + cols - 1) // cols  # Oblicz liczbę wierszy

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = np.array(axes).reshape(-1)  # Spłaszcz macierz osi, aby uprościć iterację

    for i, (img, title) in enumerate(zip(images, titles)):
        ax = axes[i]
        ax.imshow(np.clip(img[0], 0, 1))  # Obraz po transformacji
        ax.set_title(title)
        ax.axis("off")

    # Ukryj nieużywane podwykresy
    for ax in axes[len(images):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


# Załaduj obraz i przekształć do formatu NumPy
original_image = load_img(image_path)
image_array = img_to_array(original_image)
image_array = np.expand_dims(image_array, axis=0)  # Dodaj wymiar batcha

# Tworzenie przekształceń
datagen_rotation = ImageDataGenerator(rotation_range=rotation_range)
rotated_images = [datagen_rotation.flow(image_array, batch_size=1).__next__() for _ in range(5)]

datagen_shift = ImageDataGenerator(width_shift_range=width_shift_range, height_shift_range=height_shift_range)
shifted_images = [datagen_shift.flow(image_array, batch_size=1).__next__() for _ in range(5)]

datagen_shear = ImageDataGenerator(shear_range=shear_range)
sheared_images = [datagen_shear.flow(image_array, batch_size=1).__next__() for _ in range(5)]

datagen_zoom = ImageDataGenerator(zoom_range=zoom_range)
zoomed_images = [datagen_zoom.flow(image_array, batch_size=1).__next__() for _ in range(5)]

datagen_all = ImageDataGenerator(
    rotation_range=rotation_range,
    width_shift_range=width_shift_range,
    height_shift_range=height_shift_range,
    shear_range=shear_range,
    zoom_range=zoom_range,
    horizontal_flip=False,
    vertical_flip=False,
)
combined_images = [datagen_all.flow(image_array, batch_size=1).__next__() for _ in range(5)]

# Wyświetlenie i zapisanie wyników
print("Transformations: Rotation (90° max)")
plot_images(rotated_images, ["Rotation"] * 5)
save_images(rotated_images, "rotation")

print("Transformations: Shift (horizontal + vertical)")
plot_images(shifted_images, ["Shift"] * 5)
save_images(shifted_images, "shift")

print("Transformations: Shear Transformation")
plot_images(sheared_images, ["Shear"] * 5)
save_images(sheared_images, "shear")

print("Transformations: Zoom Transformation")
plot_images(zoomed_images, ["Zoom"] * 5)
save_images(zoomed_images, "zoom")

print("Transformations: Combined Transformations")
plot_images(combined_images, ["Combined"] * 5)
save_images(combined_images, "combined")

print(f"Wszystkie obrazy zostały zapisane w folderze: {output_dir}")
