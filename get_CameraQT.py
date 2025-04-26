import cv2

class Camera:
    def __init__(self, camera_indices=[0]):
        self.camera_indices = camera_indices
        self.cameras = [cv2.VideoCapture(i) for i in self.camera_indices]

    def start_camera(self):
        for cam in self.cameras:
            if not cam.isOpened():
                raise ValueError("无法打开摄像头")

        while True:
            frames = []
            for cam in self.cameras:
                ret, frame = cam.read()
                if ret:
                    frames.append(frame)
                    cv2.imshow(f'Camera {self.camera_indices[0]}', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):  # 按 's' 拍摄照片
                self.capture_images(frames)
            elif key == ord('q'):  # 按 'q' 退出
                break

        self.release_cameras()
        cv2.destroyAllWindows()

    def capture_images(self, frames):
        for i, frame in enumerate(frames):
            filename = f"camera_{self.camera_indices[i]}.png"
            cv2.imwrite(filename, frame)
            print(f"图片已保存: {filename}")

    def release_cameras(self):
        for cam in self.cameras:
            cam.release()
