# -*- coding: utf-8 -*-
"""Surface_crack_Detection_Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zHZJkNHFS6Jyp_KsCPC0Zbkeod7M_Hht
"""

import os
import kagglehub
import numpy as np
import tensorflow as tf
from pyspark.sql import SparkSession
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_recall_fscore_support
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

# Initialize PySpark Session
spark = SparkSession.builder.appName("Surface Crack Detection").getOrCreate()

# Dataset directories
path = kagglehub.dataset_download("arunrk7/surface-crack-detection")

cracked_dir = os.path.join(path, 'Positive')
non_cracked_dir = os.path.join(path, 'Negative')

# Load and preprocess data
def load_images_from_folder(folder, label):
    images, labels = [], []
    for filename in os.listdir(folder):
        img = tf.keras.utils.load_img(os.path.join(folder, filename), target_size=(64, 64))
        images.append(tf.keras.utils.img_to_array(img) / 255.0)
        labels.append(label)
    return images, labels

cracked_images, cracked_labels = load_images_from_folder(cracked_dir, 1)
non_cracked_images, non_cracked_labels = load_images_from_folder(non_cracked_dir, 0)

# Combine datasets
images = np.array(cracked_images + non_cracked_images)
labels = to_categorical(cracked_labels + non_cracked_labels, num_classes=2)

# Define the LeNet model
def create_lenet():
    model = Sequential([
        Conv2D(6, kernel_size=(5, 5), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(16, kernel_size=(5, 5), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(120, activation='relu'),
        Dense(84, activation='relu'),
        Dense(2, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = create_lenet()
model.summary()

# Split data into 70% training, 15% validation, and 15% testing
X_train, X_temp, y_train, y_temp = train_test_split(images, labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Data augmentation
datagen = ImageDataGenerator(rotation_range=15, width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)
datagen.fit(X_train)

# Train the model
history = model.fit(datagen.flow(X_train, y_train, batch_size=64), validation_data=(X_val, y_val), epochs=4, verbose=1)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy:.2f}")

# Plot confusion matrix
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)
cm = confusion_matrix(y_true, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Non-Cracked', 'Cracked']).plot(cmap=plt.cm.Blues, values_format='d')
plt.title("Confusion Matrix")
plt.show()

# Precision, Recall, F1 Score
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

# Extract training history
train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
epochs = range(1, len(train_acc) + 1)

# Plot accuracy
plt.figure(figsize=(10, 6))
plt.plot(epochs, train_acc, 'bo-', label='Training Accuracy')
plt.plot(epochs, val_acc, 'ro-', label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid()
plt.show()

# Extract loss values
train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Plot loss
plt.figure(figsize=(10, 6))
plt.plot(epochs, train_loss, 'bo-', label='Training Loss')
plt.plot(epochs, val_loss, 'ro-', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid()
plt.show()
print(classification_report(y_true, y_pred, target_names=["Non-Cracked", "Cracked"]))


# Here performing the preprocessing
def load_images_from_folder(folder, label, limit=None):
    images = []
    labels = []
    for i, filename in enumerate(os.listdir(folder)):
        if limit and i >= limit:
            break
        img_path = os.path.join(folder, filename)
        img = tf.keras.utils.load_img(img_path, target_size=(34, 34))  # Reduced to 34x34
        img_array = tf.keras.utils.img_to_array(img) / 255.0  # Normalize pixel values
        images.append(img_array)
        labels.append(label)
    return images, labels
#Here  loaded limited number of images

limit_per_class = 1000  # Adjust this limit as needed
cracked_images, cracked_labels = load_images_from_folder(cracked_dir, 1, limit=limit_per_class)
non_cracked_images, non_cracked_labels = load_images_from_folder(non_cracked_dir, 0, limit=limit_per_class)

# Here Combining the datasets
images = np.array(cracked_images + non_cracked_images)
labels = np.array(cracked_labels + non_cracked_labels)

# Here Converting the  labels to categorical
labels = to_categorical(labels, num_classes=2)

#Here splitting the dataset for training , testing.
X_train, X_temp, y_train, y_temp = train_test_split(images, labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Data augmentation
datagen = ImageDataGenerator(rotation_range=15, width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)
datagen.fit(X_train)

# Here performing the ResNet50-based model
def create_resnet50():
    # Load the ResNet50 model without the top classification layer
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(34, 34, 3))

    # Here Freezing the  all layers of the base model
    base_model.trainable = False

    # Adding customer layers on the top of the model
    inputs = base_model.input
    x = Flatten()(base_model.output)
    x = Dense(128, activation='relu')(x)  # Reduced dense layer size
    x = Dropout(0.5)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)

    # here is the Output Layer
    outputs = Dense(2, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# here Creating the model
model = create_resnet50()
model.summary()

# Training
history = model.fit(datagen.flow(X_train, y_train, batch_size=16),  # Smaller batch size
                    validation_data=(X_val, y_val),
                    epochs=10,  # Training for fewer epochs initially
                    verbose=1)

# Evaluating the model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}")

# here is the Classification metrics and confusion matrix
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=["Non-Cracked", "Cracked"]))

# Confusion Matrix Visualization
conf_matrix = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Non-Cracked", "Cracked"], yticklabels=["Non-Cracked", "Cracked"])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

# here is the Training and validation metrics visualization
plt.figure(figsize=(12, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.show()


# preprocessing the  data
def load_images_from_folder(folder, label, limit=None):
    images = []
    labels = []
    for i, filename in enumerate(os.listdir(folder)):
        if limit and i >= limit:
            break
        img_path = os.path.join(folder, filename)
        img = tf.keras.utils.load_img(img_path, target_size=(34, 34))  # Resized to 34x34
        img_array = tf.keras.utils.img_to_array(img) / 255.0  # Normalize pixel values
        images.append(img_array)
        labels.append(label)
    return images, labels


limit_per_class = 1000
cracked_images, cracked_labels = load_images_from_folder(cracked_dir, 1, limit=limit_per_class)
non_cracked_images, non_cracked_labels = load_images_from_folder(non_cracked_dir, 0, limit=limit_per_class)

# Combining the datasets
images = np.array(cracked_images + non_cracked_images)
labels = np.array(cracked_labels + non_cracked_labels)

# Convert labels to categorical
labels = to_categorical(labels, num_classes=2)

# Split data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(images, labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Data augmentation
datagen = ImageDataGenerator(rotation_range=15, width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)
datagen.fit(X_train)

# Define VGG16-based model
def create_vgg16():
    # Load the VGG16 model without the top classification layer
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(34, 34, 3))

    # Freeze all layers of the base model
    base_model.trainable = False

    # Add custom layers on top of VGG16
    inputs = base_model.input
    x = Flatten()(base_model.output)
    x = Dense(128, activation='relu')(x)  # Reduced dense layer size
    x = Dropout(0.5)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)

    # Output Layer
    outputs = Dense(2, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Create the model
model = create_vgg16()
model.summary()

# Training the model
history = model.fit(datagen.flow(X_train, y_train, batch_size=16),  # Smaller batch size
                    validation_data=(X_val, y_val),
                    epochs=10,  # Training for fewer epochs initially
                    verbose=1)

# Evaluating the model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}")

# Classification metrics and confusion matrix
y_pred = np.argmax(model.predict(X_test), axis=1)
y_true = np.argmax(y_test, axis=1)

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=["Non-Cracked", "Cracked"]))

# Confusion Matrix
conf_matrix = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Non-Cracked", "Cracked"], yticklabels=["Non-Cracked", "Cracked"])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

# Training and validation metrics
plt.figure(figsize=(12, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.show()