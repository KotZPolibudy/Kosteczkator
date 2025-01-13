from tensorflow.keras.models import load_model

model = load_model("na_nowych_final_unbalanced.keras")
num_classes = model.output_shape[-1]
print(f"Liczba klas: {num_classes}")

if hasattr(model, 'class_names'):
    print("Klasy:", model.class_names)
else:
    print("Klasy nie są zapisane w modelu.")