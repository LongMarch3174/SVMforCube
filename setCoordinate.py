import cv2
import json

# 定义全局变量
positions = []
drawing = False
ix, iy = -1, -1

# 鼠标回调函数
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, positions

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (ix+20, iy+20), (0, 255, 0), 2)
        positions.append((ix, iy))
        print(f"Added position: {ix, iy}")

    elif event == cv2.EVENT_RBUTTONDOWN:
        if positions:
            removed_pos = positions.pop()
            print(f"Removed position: {removed_pos}")
            redraw_image()

# 重绘图像
def redraw_image():
    global img
    img = img_copy.copy()
    for (x, y) in positions:
        cv2.rectangle(img, (x, y), (x+20, y+20), (0, 255, 0), 2)

# 加载图像
image_path = 'testAll/camera_3.png'  # 修改为你的图像路径
img = cv2.imread(image_path)
if img is None:
    raise ValueError("图像加载失败，请检查路径")
img_copy = img.copy()

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)

while True:
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # 按 'q' 退出
        break
    elif key == ord('s'):  # 按 's' 保存并退出
        with open('C3positions.json', 'w') as f:
            json.dump({"positions": positions}, f)
        print("Positions saved to C2positions.json")
        break

cv2.destroyAllWindows()
