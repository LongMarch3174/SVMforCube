import cv2
import json

# 读取图像和JSON文件
image_path = 'testAll/camera_4.png'
json_path = 'C4positions.json'

image = cv2.imread(image_path)

with open(json_path, 'r') as f:
    data = json.load(f)

# 获取方框的左顶点坐标
positions = data['positions']

# 绘制方框和标记
for idx, (x, y) in enumerate(positions, start=1):
    top_left = (x, y)
    bottom_right = (x + 20, y + 20)

    # 绘制方框
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # 标记数字
    cv2.putText(image, str(idx), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

# 显示图像
cv2.imshow('Image with Boxes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存图像
cv2.imwrite('testAll/c4_label.png', image)
