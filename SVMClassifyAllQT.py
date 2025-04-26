import os
import cv2
import numpy as np
import joblib
import json
from matplotlib import pyplot as plt


class SVMClassifier:
    def __init__(self, model_path='svm_color_classifier.pkl'):
        self.svm_model = joblib.load(model_path)
        self.color_labels = {
            'R': 'Red',
            'G': 'Green',
            'B': 'Blue',
            'O': 'Orange',
            'Y': 'Yellow',
            'W': 'White'
        }
        self.color_to_char = {
            'Red': 'F',
            'Green': 'D',
            'Blue': 'U',
            'Orange': 'B',
            'Yellow': 'R',
            'White': 'L'
        }
        self.map_indices = [
            34, 19, 41, 7, 52, 15, 32, 23, 43,
            31, 22, 44, 5, 51, 13, 29, 20, 46,
            42, 14, 39, 12, 53, 8, 45, 10, 36,
            40, 18, 35, 9, 48, 1, 38, 16, 25,
            37, 17, 26, 11, 49, 3, 47, 21, 28,
            24, 0, 33, 2, 50, 6, 27, 4, 30
        ]

    def classify(self, image_paths, position_files, output_file='predictions.txt'):
        predicted_colors = [None] * 54
        all_predictions = []

        for image_path, position_file in zip(image_paths, position_files):
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
                center_region = image[y:y + 20, x:x + 20]
                avg_color = np.mean(center_region, axis=(0, 1))
                test_data.append(avg_color)

            # 使用 SVM 模型进行预测
            predictions = self.svm_model.predict(np.array(test_data))
            all_predictions.extend(predictions)

            # 在图像上标注预测结果
            for (x, y), prediction in zip(positions, predictions):
                color_name = self.color_labels[prediction]
                cv2.rectangle(image, (x, y), (x + 20, y + 20), (0, 255, 0), 2)
                cv2.putText(image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # 显示标注后的图像
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title('Color Predictions')
            plt.axis('off')
            plt.show()

        # 填入 cube_colors
        for idx, prediction in enumerate(all_predictions):
            mapped_idx = self.map_indices[idx]
            predicted_colors[mapped_idx] = self.color_labels[prediction]

        # 提取角块和边块（前48个位置）
        corner_edge_colors = [predicted_colors[i] for i in range(48)]
        corner_edge_chars = [self.color_to_char[color] for color in corner_edge_colors]

        # 拼接成字符串
        result_string = ''.join(corner_edge_chars)

        # 保存预测结果
        with open(output_file, 'w') as f:
            for idx, color in enumerate(corner_edge_colors):
                f.write(f"Position {idx + 1}: Predicted Color: {color}\n")
            f.write(f"Cube Configuration: {result_string}\n")

        print(f'Predictions saved to {output_file}')
