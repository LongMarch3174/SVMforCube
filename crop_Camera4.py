import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Define paths
input_folder = 'cubephotos'
output_folder = 'crop_Camera4'
os.makedirs(output_folder, exist_ok=True)

# Define the coordinates of the corners of the two faces in the original image
# Adjust these values based on your specific image
pts_src1 = np.array([
    [141, 33],  # top-left corner of the first face
    [450, 30],  # top-right corner of the first face
    [516, 250], # bottom-right corner of the first face
    [95, 245]  # bottom-left corner of the first face
], dtype=float)

pts_src2 = np.array([
    [92, 274],  # top-left corner of the second face
    [518, 281],  # top-right corner of the second face
    [449, 477],  # bottom-right corner of the second face
    [141, 473]   # bottom-left corner of the second face
], dtype=float)

# Define the coordinates of the corners of the faces in the destination image
size = 300
pts_dst = np.array([
    [0, 0],
    [size - 1, 0],
    [size - 1, size - 1],
    [0, size - 1]
], dtype=float)

# Get perspective transform matrices
M1, _ = cv2.findHomography(pts_src1, pts_dst)
M2, _ = cv2.findHomography(pts_src2, pts_dst)

# Process each image in the input folder that starts with 'camera_2'
for filename in os.listdir(input_folder):
    if filename.startswith('camera_4') and filename.endswith(('.png', '.jpg', '.jpeg')):
        # Load the image
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Apply perspective transform to get the top-down view of the faces
        face1 = cv2.warpPerspective(image, M1, (size, size))
        face2 = cv2.warpPerspective(image, M2, (size, size))

        # Save the transformed images
        base_filename = os.path.splitext(filename)[0]
        face1_path = os.path.join(output_folder, f'{base_filename}_face1.png')
        face2_path = os.path.join(output_folder, f'{base_filename}_face2.png')
        cv2.imwrite(face1_path, face1)
        cv2.imwrite(face2_path, face2)

        print(f'Processed and saved: {face1_path} and {face2_path}')

print('All images processed.')
