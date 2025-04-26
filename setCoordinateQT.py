import cv2
import json


class CoordinateSetter:
    def __init__(self):
        self.positions = []
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.img = None
        self.img_copy = None
        self.image_path = ''
        self.window_name = 'image'
        self.save_path = 'positions.json'

    def set_coordinates(self, image_path=None, save_path=None):
        self.image_path = image_path if image_path else self.image_path
        self.save_path = save_path if save_path else self.save_path

        self.img = cv2.imread(self.image_path)
        if self.img is None:
            raise ValueError("图像加载失败，请检查路径")
        self.img_copy = self.img.copy()

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.draw_rectangle)

        while True:
            cv2.imshow(self.window_name, self.img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # 按 'q' 退出
                break
            elif key == ord('s'):  # 按 's' 保存并退出
                self.save_positions()
                break

        cv2.destroyAllWindows()

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.rectangle(self.img, (self.ix, self.iy), (self.ix + 20, self.iy + 20), (0, 255, 0), 2)
            self.positions.append((self.ix, self.iy))
            print(f"Added position: {self.ix, self.iy}")

        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.positions:
                removed_pos = self.positions.pop()
                print(f"Removed position: {removed_pos}")
                self.redraw_image()

    def redraw_image(self):
        self.img = self.img_copy.copy()
        for (x, y) in self.positions:
            cv2.rectangle(self.img, (x, y), (x + 20, y + 20), (0, 255, 0), 2)

    def save_positions(self):
        with open(self.save_path, 'w') as f:
            json.dump({"positions": self.positions}, f)
        print(f"Positions saved to {self.save_path}")
