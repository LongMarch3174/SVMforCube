import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# Define the input and output folders
input_folder = 'crop_Camera4'
output_folder = os.path.join(input_folder, 'blocks')
os.makedirs(output_folder, exist_ok=True)

# Define the size of the individual blocks
block_size = 100

# Indices of blocks to be excluded (1-based index)
excluded_indices = {3, 5}

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

        # Split the image into 9 blocks
        blocks = []
        for i in range(3):
            for j in range(3):
                block = image_rgb[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]
                blocks.append(block)

        # Save the individual blocks except for the excluded ones
        base_filename = os.path.splitext(filename)[0]
        for idx, block in enumerate(blocks):
            if idx in excluded_indices:
                continue  # Skip the block if its index is in the excluded list
            block_path = os.path.join(output_folder, f'{base_filename}_block_{idx + 1}.png')
            block_pil = Image.fromarray(block)
            block_pil.save(block_path)
            print(f'Saved: {block_path}')

print('All images processed.')
