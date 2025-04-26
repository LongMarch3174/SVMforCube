import os
import cv2
import numpy as np
import joblib
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

# 定义测试集文件夹路径
test_folder = './testCover'


# 定义提取指定位置颜色的函数
def extract_color_at_position(image, x, y):
    region = image[y:y + 20, x:x + 20]
    avg_color = np.mean(region, axis=(0, 1))
    return avg_color


# 准备测试数据
test_data = []
test_image_paths = []
sampling_positions = []  # 存储取样位置
for filename in os.listdir(test_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(test_folder, filename)
        image = cv2.imread(image_path)
        if image is not None:
            # 指定取样位置，例如 (40, 40)
            x, y = 40, 40
            avg_color = extract_color_at_position(image, x, y)
            test_data.append(avg_color)
            test_image_paths.append(image_path)
            sampling_positions.append((x, y))

# 将测试数据转换为 NumPy 数组
test_data = np.array(test_data)

# 使用 SVM 模型进行预测
predictions = svm_model.predict(test_data)

# 打印预测结果并显示图像
output_file = 'predictions.txt'
with open(output_file, 'w') as f:
    for image_path, prediction, (x, y) in zip(test_image_paths, predictions, sampling_positions):
        color_name = color_labels[prediction]
        f.write(f"Image: {image_path} -> Predicted Color: {color_name}\n")

        # 读取图像并绘制矩形框和颜色标签
        image = cv2.imread(image_path)
        if image is not None:
            cv2.rectangle(image, (x, y), (x + 20, y + 20), (0, 255, 0), 2)  # 绘制绿色的矩形框
            cv2.putText(image, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # 显示图像
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title(f"Predicted Color: {color_name}")
            plt.axis('off')
            plt.show()

print(f'Predictions saved to {output_file}')
