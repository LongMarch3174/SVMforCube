import os
import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
from matplotlib import pyplot as plt
from PIL import Image

# Define the input and output folders
input_folder = 'crop_Camera4/blocks'
output_folders = {
    'R': './R',
    'G': './G',
    'B': './B',
    'O': './O',
    'Y': './Y',
    'W': './W'
}

# Create output directories if they do not exist
for folder in output_folders.values():
    os.makedirs(folder, exist_ok=True)

# Define the colors for classification (in RGB)
colors = {
    'R': [255, 0, 0],
    'G': [0, 255, 0],
    'B': [0, 0, 255],
    'O': [255, 165, 0],
    'Y': [255, 255, 0],
    'W': [255, 255, 255]
}


# Function to classify the color
def classify_color(color):
    color = np.array(color)
    min_distance = float('inf')
    classified_color = None
    for key, value in colors.items():
        distance = np.linalg.norm(color - value)
        if distance < min_distance:
            min_distance = distance
            classified_color = key
    return classified_color


# Iterate over all image files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)

        # Load the image
        image = cv2.imread(image_path)

        # Check if image is loaded properly
        if image is None:
            print(f"Image not loaded: {image_path}")
            continue

        # Convert the image to RGB (OpenCV loads images in BGR format)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Extract the center 20x20 region
        center_region = image_rgb[40:60, 40:60]

        # Calculate the average color of the center region
        avg_color = np.mean(center_region, axis=(0, 1)).astype(int)

        # Classify the color
        color_class = classify_color(avg_color)

        # Save the image to the corresponding folder
        output_path = os.path.join(output_folders[color_class], filename)
        cv2.imwrite(output_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
        print(f'Saved: {output_path} as {color_class}')

print('All images processed.')
