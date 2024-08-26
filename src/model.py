# model.py
from tensorflow.keras import layers, models, Input
from config import NUM_CLASSES


def create_model(input_shape=(28, 28, 1), num_classes=NUM_CLASSES):
    model = models.Sequential()
    model.add(Input(shape=input_shape))  # Specify the input shape here
    model.add(layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))

    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model
