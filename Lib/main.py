import sys
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer

import socket
import time
host = '192.168.1.63'  # Địa chỉ IP của ESP32
port = 80  # Cổng của ESP32


# Tạo một socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối tới máy chủ
client_socket.connect((host, port))
count = 0


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Camera Display with Controls')
        self.setGeometry(100, 100, 800, 600)

        # Layout cho video
        self.layout = QVBoxLayout()

        # Label để hiển thị video
        self.label = QLabel()
        self.layout.addWidget(self.label)

        # Layout cho các nút điều khiển
        self.controlLayout = QHBoxLayout()

        self.upButton = QPushButton('Up')
        self.upButton.clicked.connect(self.on_up)
        self.controlLayout.addWidget(self.upButton)

        self.downButton = QPushButton('Down')
        self.downButton.clicked.connect(self.on_down)
        self.controlLayout.addWidget(self.downButton)

        self.leftButton = QPushButton('Left')
        self.leftButton.clicked.connect(self.on_left)
        self.controlLayout.addWidget(self.leftButton)

        self.rightButton = QPushButton('Right')
        self.rightButton.clicked.connect(self.on_right)
        self.controlLayout.addWidget(self.rightButton)

        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.on_stop)
        self.controlLayout.addWidget(self.stopButton)

        self.layout.addLayout(self.controlLayout)
        self.setLayout(self.layout)

        # Khởi tạo camera
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(convert_to_qt_format))

    def closeEvent(self, event):
        self.cap.release()

    # Các hàm điều khiển cho các nút
    def on_up(self):
        print("Up button clicked")
        # Code chức năng cho nút lên
        client_socket.sendall(str(f"{1}\n").encode())

    def on_down(self):
        print("Down button clicked")
        # Code chức năng cho nút xuống
        client_socket.sendall(str(f"{2}\n").encode())

    def on_left(self):
        print("Left button clicked")
        # Code chức năng cho nút trái
        client_socket.sendall(str(f"{3}\n").encode())

    def on_right(self):
        print("Right button clicked")
        # Code chức năng cho nút phải\
        client_socket.sendall(str(f"{4}\n").encode())


    def on_stop(self):
        print("Stop button clicked")
        # Code chức năng cho nút dừng
        client_socket.sendall(str(f"{5}\n").encode())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_widget = CameraWidget()
    camera_widget.show()
    sys.exit(app.exec())
