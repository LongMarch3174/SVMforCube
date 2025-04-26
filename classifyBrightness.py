import os
import cv2
import numpy as np

# Define the input and output folders
input_folders = {
    'R': './R',
    #'G': './G',
    #'B': './B',
    #'O': './O',
    #'Y': './Y',
    #'W': './W'
}

# Define brightness thresholds for classification
# Adjust these values based on your specific needs
low_threshold = 50
high_threshold = 80


# Function to classify brightness
def classify_brightness(avg_brightness):
    if avg_brightness < low_threshold:
        return 'L'
    elif avg_brightness > high_threshold:
        return 'H'
    else:
        return 'M'


# Function to calculate the average brightness of the center region
def calculate_average_brightness(image):
    center_region = image[30:70, 30:70]
    avg_brightness = np.mean(center_region)
    return avg_brightness


# Process each folder and rename the images
for color, folder in input_folders.items():
    sequence_number = 1
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder, filename)

            # Load the image
            image = cv2.imread(image_path)

            # Check if image is loaded properly
            if image is None:
                print(f"Image not loaded: {image_path}")
                continue

            # Convert the image to grayscale for brightness calculation
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Calculate the average brightness of the center region
            avg_brightness = calculate_average_brightness(image_gray)

            # Classify the brightness
            brightness_class = classify_brightness(avg_brightness)

            # Generate the new filename
            new_filename = f"{color}_{sequence_number}_{brightness_class}.png"
            new_image_path = os.path.join(folder, new_filename)

            # Rename the image
            os.rename(image_path, new_image_path)
            print(f"Renamed {image_path} to {new_image_path}")

            sequence_number += 1

print('All images processed and renamed.')
