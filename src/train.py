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

# Check if the dataset path exists
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Run preprocess.py first.")

# Load and preprocess data
print("Loading dataset...")

datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,  # zacząłem się zastanawiać czy to jest potrzebne, czy nie...
    validation_split=0.3,
    rotation_range=90,  # Rotate images up to 90 degrees
    horizontal_flip=False,  # DONT MIRROR
    vertical_flip=False
)


train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    color_mode="grayscale",  # Specify grayscale mode
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    color_mode="grayscale",  # Specify grayscale mode
    subset="validation"
)


print(f"Training samples: {train_data.samples}")
print(f"Validation samples: {val_data.samples}")

# Define the CNN model
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

# Create and summarize the model
print("Creating model...")
model = create_model()
model.summary()

# Train the model
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


# Extract final metrics
final_train_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
final_train_loss = history.history['loss'][-1]
final_val_loss = history.history['val_loss'][-1]

# Print final statistics
print("\nFinal Training Accuracy: {:.4f}".format(final_train_acc))
print("Final Validation Accuracy: {:.4f}".format(final_val_acc))
print("Final Training Loss: {:.4f}".format(final_train_loss))
print("Final Validation Loss: {:.4f}".format(final_val_loss))


# Save the trained model
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
