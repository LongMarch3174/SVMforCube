import os
import cv2
import numpy as np
import joblib
import json
from matplotlib import pyplot as plt

# 加载训练好的 SVM 模型
svm_model = joblib.load('svm_color_classifier.pkl')

# 定义颜色标签映射
color_labels = {
    'R': 'Red',
    'G': 'Green',
    'B': 'Blue',
    'O': 'Orange',
    'Y': 'Yellow',
    'W': 'White'
}

# 定义颜色到字符的映射
color_to_char = {
    'Red': 'F',
    'Green': 'D',
    'Blue': 'U',
    'Orange': 'B',
    'Yellow': 'R',
    'White': 'L'
}

# 图像路径和位置文件
output_folder = "testAll/"
image_paths = ['camera_2.png', 'camera_1.png', 'camera_4.png', 'camera_3.png']
position_files = ['C2positions.json', 'C1positions.json', 'C4positions.json', 'C3positions.json']

# 映射数组
map_indices = [
    34, 19, 41, 7, 52, 15, 32, 23, 43,
    31, 22, 44, 5, 51, 13, 29, 20, 46,
    42, 14, 39, 12, 53, 8, 45, 10, 36,
    40, 18, 35, 9, 48, 1, 38, 16, 25,
    37, 17, 26, 11, 49, 3, 47, 21, 28,
    24, 0, 33, 2, 50, 6, 27, 4, 30
]

# 初始化一个54位的列表来存储颜色
predicted_colors = [None] * 54

# 处理每张图像
all_predictions = []
for image_path, position_file in zip(image_paths, position_files):
    image_path = output_folder + image_path

    # 读取 JSON 文件中的坐标
    with open(position_file, 'r') as f:
        data = json.load(f)
    positions = data['positions']

    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"图像 {image_path} 加载失败，请检查路径")

    # 提取每个位置的颜色特征
    test_data = []
    for (x, y) in positions:
        center_region = image[y:y+20, x:x+20]
        avg_color = np.mean(center_region, axis=(0, 1))
        test_data.append(avg_color)

    # 将测试数据转换为 NumPy 数组
    test_data = np.array(test_data)

    # 使用 SVM 模型进行预测
    predictions = svm_model.predict(test_data)
    all_predictions.extend(predictions)

    # 打印预测结果并在图像上标注
    for (x, y), prediction in zip(positions, predictions):
        color_name = color_labels[prediction]
        cv2.rectangle(image, (x, y), (x + 20, y + 20), (0, 255, 0), 2)  # 绘制绿色矩形框
        cv2.putText(image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 显示标注后的图像
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Color Predictions')
    plt.axis('off')
    plt.show()

# 将预测结果按照映射数组填入 cube_colors
for idx, prediction in enumerate(all_predictions):
    mapped_idx = map_indices[idx]
    predicted_colors[mapped_idx] = color_labels[prediction]

# 提取角块和边块（前48个位置）
corner_edge_colors = [predicted_colors[i] for i in range(48)]

# 映射颜色到字符
corner_edge_chars = [color_to_char[color] for color in corner_edge_colors]

# 拼接成字符串
result_string = ''.join(corner_edge_chars)

# 打印并保存预测结果
output_file = 'predictions.txt'
with open(output_file, 'w') as f:
    for idx, color in enumerate(corner_edge_colors):
        print(f"Position {idx+1}: Predicted Color: {color}")
        f.write(f"Position {idx+1}: Predicted Color: {color}\n")

    # 输出拼接字符串
    print(f"Cube Configuration: {result_string}")
    f.write(f"Cube Configuration: {result_string}\n")

print(f'Predictions saved to {output_file}')
