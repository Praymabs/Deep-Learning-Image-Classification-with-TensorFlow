# -*- coding: utf-8 -*-
"""Flowers  DIP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11v6lJ6QLfMT9DTeH9ilJ6tU7iUuaKxqy
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Step 1: Import Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Upload the zip file to Colab
from google.colab import files

# Step 2: Load and Preprocess the Dataset
data_dir = Path("/content/drive/MyDrive/DIP - Flowers/flowers")

# Load images and labels
image_paths = list(data_dir.glob("*/*.jpg"))
labels = [path.parent.name for path in image_paths]

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(image_paths, encoded_labels, test_size=0.2, random_state=42)

# Step 3: Apply Histogram Equalization
def apply_histogram_equalization(image_path):
    img = cv2.imread(str(image_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Apply histogram equalization
    equalized = cv2.equalizeHist(gray)

    # Visualize the original and equalized images
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(equalized, cmap='gray')
    plt.title('Equalized Image')

    plt.show()

# Choose an image path for demonstration
sample_image_path = X_train[0]
apply_histogram_equalization(sample_image_path)

# Step 4: Load Preprocessed Images
# Function to load and preprocess images
def load_and_preprocess_images(image_paths):
    images = []
    for path in image_paths:
        img = load_img(path, target_size=(224, 224))  # Adjust target_size as needed
        img_array = img_to_array(img)
        images.append(img_array)
    return np.array(images)

# Load and preprocess training and testing images
X_train_images = load_and_preprocess_images(X_train)
X_test_images = load_and_preprocess_images(X_test)

# Step 5: Train Deep Learning Models
# EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Build a custom model on top of EfficientNet
model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(5, activation='softmax'))  # Assuming 5 flower categories

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train_images, y_train, validation_data=(X_test_images, y_test), epochs=10, batch_size=32)

# Plot training history
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Step 6: Evaluate and Visualize Results
# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test_images, y_test)
print(f'Test Accuracy: {test_accuracy * 100:.2f}%')

# Confusion Matrix
y_pred = model.predict(X_test_images).argmax(axis=1)
conf_mat = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

!git clone https://github.com/HRNet/HRNet-Image-Classification

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import EfficientNetB0, Xception, MobileNetV2
from keras.preprocessing.image import ImageDataGenerator

#Function to create a common model structure
def create_model(base_model, num_classes):
    model = Sequential()
    model.add(base_model)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(num_classes, activation='softmax'))
    return model

# Assuming you have a class HRNet with a function build_hrnet_model
class HRNet:
    def build_hrnet_model(self, input_shape, num_classes):
        # Implement the HRNet model architecture here
        # Replace the following line with the actual HRNet model creation
        hrnet_model = Sequential()  # Placeholder, replace this line
        hrnet_model.add(GlobalAveragePooling2D())
        hrnet_model.add(Dense(num_classes, activation='softmax'))
        return hrnet_model

# Instantiate HRNet class
hrnet = HRNet()

# Build and compile HRNet model
hrnet_model = hrnet.build_hrnet_model(input_shape=(224, 224, 3), num_classes=5)
hrnet_model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train HRNet model
history_hrnet = hrnet_model.fit(X_train_images, y_train, validation_data=(X_test_images, y_test), epochs=10, batch_size=32)

import cv2
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have a function to load and preprocess an image
def load_and_preprocess_image(image_path, target_size=(224, 224)):
    # Load the image
    image = cv2.imread(str(image_path))  # Use str() to convert PosixPath to string

    # Resize the image to the target size
    image = cv2.resize(image, target_size)

    # Convert to float and normalize (assuming pixel values are in the range [0, 255])
    image = image.astype("float32") / 255.0

    # Apply any other necessary preprocessing steps
    # ...

    return image

# Convert image paths to image data and resize to a common shape
common_image_shape = (224, 224, 3)  # Adjust the shape to your needs
X_test_images = [load_and_preprocess_image(path, target_size=common_image_shape[:2]) for path in X_test]

# Convert to NumPy array
X_test_images = np.array(X_test_images)

# Evaluate HRNet model on the test set
test_loss, test_acc = hrnet_model.evaluate(X_test_images, y_test)
print(f"Test Accuracy: {test_acc}")

# Predict the classes for the test set
y_pred = hrnet_model.predict(X_test_images)
y_pred_classes = np.argmax(y_pred, axis=1)

# Create the confusion matrix
cm = confusion_matrix(y_test, y_pred_classes)

# Plot the confusion matrix using seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=np.unique(y_test), yticklabels=np.unique(y_test))
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# EfficientNet model
efficientnet_model = create_model(EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3)), 5)
efficientnet_model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history_efficientnet = efficientnet_model.fit(X_train_images, y_train, validation_data=(X_test_images, y_test), epochs=10, batch_size=32)