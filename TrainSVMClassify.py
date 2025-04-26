import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Define the input folders and corresponding labels
input_folders = {
    'R': './R',
    'G': './G',
    'B': './B',
    'O': './O',
    'Y': './Y',
    'W': './W'
}


# Define a function to extract the center 20x20 average color
def extract_center_color(image):
    center_region = image[40:60, 40:60]
    avg_color = np.mean(center_region, axis=(0, 1))
    return avg_color


# Prepare the data
data = []
labels = []
for color, folder in input_folders.items():
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder, filename)
            image = cv2.imread(image_path)
            if image is not None:
                avg_color = extract_center_color(image)
                data.append(avg_color)
                labels.append(color)

data = np.array(data)
labels = np.array(labels)

# Split the data into training (70%), validation (15%), and test (15%) sets
X_train, X_temp, y_train, y_temp = train_test_split(data, labels, test_size=0.3, random_state=42, stratify=labels)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

# Train the SVM model
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train, y_train)

# Validate the model
y_val_pred = svm_model.predict(X_val)
val_accuracy = accuracy_score(y_val, y_val_pred)
print(f'Validation Accuracy: {val_accuracy * 100:.2f}%')

# Test the model
y_test_pred = svm_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
print(f'Test Accuracy: {test_accuracy * 100:.2f}%')

# Save the model if needed
import joblib

joblib.dump(svm_model, 'svm_color_classifier.pkl')


# Function to predict the color of a single image
def predict_color(image_path, model):
    image = cv2.imread(image_path)
    if image is not None:
        avg_color = extract_center_color(image)
        prediction = model.predict([avg_color])
        return prediction[0]
    else:
        return None


# Example prediction
example_image_path = 'O/O_100_M.png'  # Change to an actual image path
predicted_color = predict_color(example_image_path, svm_model)
print(f'Predicted Color: {predicted_color}')
