import os
from PIL import Image
import matplotlib.pyplot as plt

# Define paths
input_folder = 'cubephotos'
output_folder = 'crop_Camera2'
os.makedirs(output_folder, exist_ok=True)

# Define the cropping coordinates and the desired size
left = 145
top = 190
right = 605
bottom = 630
crop_width = 300
crop_height = 300

# Process each image in the input folder that starts with 'camera_1'
for filename in os.listdir(input_folder):
    if filename.startswith('camera_2') and filename.endswith(('.png', '.jpg', '.jpeg')):
        # Load the image
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)

        # Rotate the image by 48 degrees
        rotated_image = image.rotate(45, expand=True)

        # Crop the image
        cropped_image = rotated_image.crop((left, top, right, bottom))

        # Resize the cropped image
        resized_image = cropped_image.resize((crop_width, crop_height))

        # Save the cropped and resized image
        output_path = os.path.join(output_folder, filename)
        resized_image.save(output_path)

        print(f'Processed and saved: {output_path}')

print('All images processed.')

