import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QDateTime

class CameraApp(QWidget):
    def __init__(self, camera_indices):
        super().__init__()
        
        self.camera_indices = camera_indices
        self.cameras = [cv2.VideoCapture(i) for i in self.camera_indices]
        self.labels = [QLabel(self) for _ in self.camera_indices]
        self.initUI()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        
        cam_layout = QHBoxLayout()
        for label in self.labels:
            cam_layout.addWidget(label)
        
        button = QPushButton('拍摄', self)
        button.clicked.connect(self.capture_images)
        
        layout.addLayout(cam_layout)
        layout.addWidget(button)
        
        self.setLayout(layout)
        self.setWindowTitle('摄像头显示')
        self.show()

    def update_frames(self):
        for i, cam in enumerate(self.cameras):
            ret, frame = cam.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.labels[i].setPixmap(QPixmap.fromImage(image))

    def capture_images(self):
        for i, cam in enumerate(self.cameras):
            ret, frame = cam.read()
            if ret:
                filename = f"camera_{self.camera_indices[i]}_{QDateTime.currentDateTime().toString('yyyyMMdd_HHmmss')}.png"
                cv2.imwrite(filename, frame)
                print(f"图片已保存: {filename}")

    def closeEvent(self, event):
        for cam in self.cameras:
            cam.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_indices = [0]  # 指定你要使用的摄像头索引
    ex = CameraApp(camera_indices)
    sys.exit(app.exec_())
