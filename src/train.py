import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt

# Set dataset paths
DATASET_PATH = "../data/gray"
MODEL_SAVE_PATH = "na_nowych_final_unbalanced2.keras"

# Image parameters
IMAGE_SIZE = (64, 64)
BATCH_SIZE = 16
EPOCHS = 20


if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}.")
print("Loading dataset...")

datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    validation_split=0.3,
    rotation_range=90,  # Obrót o losowy kąt w zakresie od -90° do 90°
    width_shift_range=0.2,  # Przesunięcie w poziomie w zakresie od -20% do 20% szerokości obrazu
    height_shift_range=0.2,  # Przesunięcie w pionie w zakresie od -20% do 20% wysokości obrazu
    shear_range=0.1,  # Transformacja perspektywiczna (shear) w zakresie od -10% do 10%
    zoom_range=0.1,  # Losowe przybliżenia lub oddalenia w zakresie od 90% do 110% oryginalnego rozmiaru
    horizontal_flip=False,  # Brak poziomego odbicia
    vertical_flip=False  # Brak pionowego odbicia
)


train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    color_mode="grayscale",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    color_mode="grayscale",
    subset="validation"
)

print(f"Training samples: {train_data.samples}")
print(f"Validation samples: {val_data.samples}")
print(train_data.class_indices)
print(val_data.class_indices)

def create_model():
    model = models.Sequential([
        layers.Input(shape=(64, 64, 1)),  # Input layer

        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(8, activation='softmax')  # 8 classes for numbers 1–8
    ])
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

print("Creating model...")
model = create_model()
model.summary()

print("Starting training...")
steps_per_epoch = train_data.samples // BATCH_SIZE
validation_steps = val_data.samples // BATCH_SIZE

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps
)


final_train_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
final_train_loss = history.history['loss'][-1]
final_val_loss = history.history['val_loss'][-1]

print("\nFinal Training Accuracy: {:.4f}".format(final_train_acc))
print("Final Validation Accuracy: {:.4f}".format(final_val_acc))
print("Final Training Loss: {:.4f}".format(final_train_loss))
print("Final Validation Loss: {:.4f}".format(final_val_loss))

print(f"Saving model to {MODEL_SAVE_PATH}...")
model.save(MODEL_SAVE_PATH)
print("Model saved!")

# Plot accuracy
plt.figure()
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Model Accuracy')
plt.show()

# Plot loss
plt.figure()
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Model Loss')
plt.show()

print("Training complete!")
