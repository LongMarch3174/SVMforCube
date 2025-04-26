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

# 读取 JSON 文件中的坐标
with open('C4positions.json', 'r') as f:
    data = json.load(f)
positions = data['positions']

# 定义测试图像路径
image_path = 'testAll/camera_4.png'  # 修改为实际图像路径

# 读取图像
image = cv2.imread(image_path)
if image is None:
    raise ValueError("图像加载失败，请检查路径")

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

# 打印预测结果并在图像上标注
for (x, y), prediction in zip(positions, predictions):
    color_name = color_labels[prediction]
    cv2.rectangle(image, (x, y), (x+20, y+20), (0, 255, 0), 2)  # 绘制绿色矩形框
    cv2.putText(image, color_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# 显示标注后的图像
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Color Predictions')
plt.axis('off')
plt.show()

# 打印并保存预测结果
output_file = 'predictions.txt'
with open(output_file, 'w') as f:
    for idx, (pos, prediction) in enumerate(zip(positions, predictions)):
        color_name = color_labels[prediction]
        print(f"Position {idx+1}: Predicted Color: {color_name}")
        f.write(f"Position {idx+1}: Predicted Color: {color_name}\n")

print(f'Predictions saved to {output_file}')
