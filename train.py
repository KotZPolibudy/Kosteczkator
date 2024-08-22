# train.py
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import model
from config import NUM_CLASSES


def load_data(data_dir, target_size=(28, 28), batch_size=32):
    datagen = ImageDataGenerator(rescale=1.0 / 255.0)
    data = datagen.flow_from_directory(data_dir,
                                       target_size=target_size,
                                       color_mode='grayscale',
                                       class_mode='sparse',
                                       batch_size=batch_size)
    return data


def train_model(train_data_dir, validation_data_dir=None, epochs=10):
    train_data = load_data(train_data_dir)
    validation_data = load_data(validation_data_dir) if validation_data_dir else None

    cnn_model = model.create_model(num_classes=NUM_CLASSES)

    cnn_model.fit(train_data,
                  validation_data=validation_data,
                  epochs=epochs)

    cnn_model.save('digit_recognition_model.h5')


if __name__ == "__main__":
    train_model('data/train', validation_data_dir='data/validation')
