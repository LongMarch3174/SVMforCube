import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel
from get_CameraQT import Camera
from setCoordinateQT import CoordinateSetter
from SVMClassifyAllQT import SVMClassifier


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多功能工具")

        # 实例化各个功能类
        self.camera = Camera()
        self.coordinate_setter = CoordinateSetter()
        self.svm_classifier = SVMClassifier()

        # 创建按钮
        self.camera_button = QPushButton("启动相机")
        self.coordinate_button = QPushButton("设置坐标")
        self.classify_button = QPushButton("分类")

        # 创建输入框和标签
        self.image_path_label = QLabel("图像路径:")
        self.image_path_input = QLineEdit(self)
        self.position_file_label = QLabel("坐标文件路径:")
        self.position_file_input = QLineEdit(self)
        self.save_path_label = QLabel("保存路径:")
        self.save_path_input = QLineEdit(self)

        # 连接按钮和相应的方法
        self.camera_button.clicked.connect(self.start_camera)
        self.coordinate_button.clicked.connect(self.set_coordinates)
        self.classify_button.clicked.connect(self.classify)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.camera_button)
        layout.addWidget(self.coordinate_button)
        layout.addWidget(self.classify_button)
        layout.addWidget(self.image_path_label)
        layout.addWidget(self.image_path_input)
        layout.addWidget(self.position_file_label)
        layout.addWidget(self.position_file_input)
        layout.addWidget(self.save_path_label)
        layout.addWidget(self.save_path_input)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_camera(self):
        self.camera.start_camera()
        print("相机已启动")

    def set_coordinates(self):
        image_path = self.image_path_input.text()
        if not image_path:
            image_path, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "图像文件 (*.png *.jpg *.jpeg)")
            self.image_path_input.setText(image_path)

        save_path = self.save_path_input.text()
        if not save_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "保存坐标文件", "", "JSON 文件 (*.json)")
            self.save_path_input.setText(save_path)

        self.coordinate_setter.set_coordinates(image_path, save_path)
        print(f"坐标已设置并保存至 {save_path}")

    def classify(self):
        image_paths = self.image_path_input.text().split(';')
        position_files = self.position_file_input.text().split(';')
        output_file = self.save_path_input.text() or 'predictions.txt'

        self.svm_classifier.classify(image_paths, position_files, output_file)
        print(f"分类完成，结果保存至 {output_file}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
