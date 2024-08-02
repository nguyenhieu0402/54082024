import sys
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QMessageBox, QGridLayout, QSpacerItem, QSizePolicy, QFormLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt
import socket

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.distance = "Unknown"  # Khởi tạo thuộc tính
        self.sensor_status = "Unknown"  # Khởi tạo thuộc tính
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Camera Display with Controls')
        self.setGeometry(100, 100, 800, 600)

        # Đặt màu nền cho widget chính
        self.setStyleSheet("background-color: white;")

        # Layout chính
        self.mainLayout = QVBoxLayout()

        # Layout cho logo, tiêu đề và thông tin cá nhân
        self.headerLayout = QHBoxLayout()

        # Thêm logo vào góc trái
        self.logoLabel = QLabel()
        self.logoPixmap = QPixmap('logo.jpg')  # Thay 'path_to_logo.png' bằng đường dẫn đến file logo của bạn
        self.logoLabel.setPixmap(self.logoPixmap)
        self.logoLabel.setFixedSize(self.logoPixmap.size())
        self.headerLayout.addWidget(self.logoLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        # Layout cho tiêu đề
        self.titleLabel = QLabel("Xe điều khiển từ xa có hệ thống giám sát")
        self.titleLabel.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 10px;
            background-color: #ecf0f1;
            text-align: center;
        """)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addWidget(self.titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        # Thêm thông tin cá nhân vào góc phải
        self.infoLayout = QFormLayout()
        self.nameLabel = QLabel('Tên: Nguyễn Thanh Bình')
        self.mssvLabel = QLabel('MSSV: 1951220001')
        self.gvhcLabel = QLabel('GVHD: Th.s Trần Quang Vinh')

        self.infoLayout.addRow(self.nameLabel)
        self.infoLayout.addRow(self.mssvLabel)
        self.infoLayout.addRow(self.gvhcLabel)

        self.infoWidget = QWidget()
        self.infoWidget.setLayout(self.infoLayout)
        self.headerLayout.addWidget(self.infoWidget, alignment=Qt.AlignmentFlag.AlignRight)

        # Layout cho cấu hình IP
        self.ipLayout = QHBoxLayout()
        self.ipClientLabel = QLabel('IP Client:')
        self.ipLayout.addWidget(self.ipClientLabel)
        self.ipClientInput = QLineEdit()
        self.ipLayout.addWidget(self.ipClientInput)
        self.connectClientButton = QPushButton('Connect IP')
        self.connectClientButton.clicked.connect(self.connect_client)
        self.ipLayout.addWidget(self.connectClientButton)
        self.ipCamLabel = QLabel('IP Cam:')
        self.ipLayout.addWidget(self.ipCamLabel)
        self.ipCamInput = QLineEdit()
        self.ipLayout.addWidget(self.ipCamInput)
        self.connectCamButton = QPushButton('Connect Camera')
        self.connectCamButton.clicked.connect(self.connect_camera)
        self.ipLayout.addWidget(self.connectCamButton)

        # Layout cho video
        self.videoLayout = QVBoxLayout()
        self.label = QLabel()
        self.videoLayout.addWidget(self.label)

        # Layout cho các thông tin trạng thái gần nhau
        self.statusLayout = QHBoxLayout()
        self.distanceLabel = QLabel(f"Distance: {self.distance}")
        self.sensorStatusLabel = QLabel(f"Sensor Status: {self.sensor_status}")

        self.statusLayout.addWidget(self.distanceLabel)
        self.statusLayout.addWidget(self.sensorStatusLabel)

        # Thêm headerLayout, ipLayout, videoLayout và statusLayout vào mainLayout
        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.ipLayout)
        self.mainLayout.addLayout(self.videoLayout)
        self.mainLayout.addLayout(self.statusLayout)

        # Thêm không gian trống để đẩy các nút điều khiển xuống dưới cùng
        self.mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Layout cho các nút điều khiển
        self.controlLayout = QGridLayout()
        self.controlLayout.setSpacing(10)
        self.upButton = QPushButton('Up')
        self.downButton = QPushButton('Down')
        self.leftButton = QPushButton('Left')
        self.rightButton = QPushButton('Right')
        self.stopButton = QPushButton('Stop')

        # Tùy chỉnh giao diện của các nút
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 18px;
                border: 2px solid #2980b9;
                border-radius: 10px;
                padding: 10px;
                min-width: 80px;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """
        self.upButton.setStyleSheet(button_style)
        self.downButton.setStyleSheet(button_style)
        self.leftButton.setStyleSheet(button_style)
        self.rightButton.setStyleSheet(button_style)
        self.stopButton.setStyleSheet(button_style)

        # Thêm các nút vào layout
        self.controlLayout.addWidget(self.upButton, 0, 1)
        self.controlLayout.addWidget(self.leftButton, 1, 0)
        self.controlLayout.addWidget(self.rightButton, 1, 2)
        self.controlLayout.addWidget(self.downButton, 2, 1)
        self.controlLayout.addWidget(self.stopButton, 1, 1)

        self.mainLayout.addLayout(self.controlLayout)

        self.setLayout(self.mainLayout)

        # Khởi tạo timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Tạo QTimer cho các nút nhấn giữ
        self.control_timer = QTimer(self)
        self.control_timer.timeout.connect(self.send_command)
        self.current_command = None

        # Kết nối các nút điều khiển với các phương thức tương ứng
        self.upButton.pressed.connect(self.on_up_pressed)
        self.upButton.released.connect(self.on_button_released)

        self.downButton.pressed.connect(self.on_down_pressed)
        self.downButton.released.connect(self.on_button_released)

        self.leftButton.pressed.connect(self.on_left_pressed)
        self.leftButton.released.connect(self.on_button_released)

        self.rightButton.pressed.connect(self.on_right_pressed)
        self.rightButton.released.connect(self.on_button_released)

        self.stopButton.pressed.connect(self.on_stop_pressed)
        self.stopButton.released.connect(self.on_button_released)

    def connect_camera(self):
        ip_cam = self.ipCamInput.text()
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(ip_cam)
        if not self.cap.isOpened():
            self.show_error_message(f"Unable to connect to camera at {ip_cam}")
        else:
            self.timer.start(30)

    def connect_client(self):
        ip_client = self.ipClientInput.text()
        print(f"Connecting to client at {ip_client}")
        # Kết nối tới ESP32
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip_client, 80))
            print("Connected to client")
        except Exception as e:
            self.show_error_message(f"Unable to connect to client at {ip_client}: {e}")

    def update_frame(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(convert_to_qt_format))

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec()

    def closeEvent(self, event):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        if self.client_socket:
            self.client_socket.close()

    def send_command(self):
        if self.client_socket and self.current_command:
            try:
                self.client_socket.sendall(self.current_command.encode())
            except Exception as e:
                self.show_error_message(f"Failed to send command: {e}")
                self.control_timer.stop()

    def on_up_pressed(self):
        self.current_command = "1\n"
        self.control_timer.start(50)  # Send every 50ms

    def on_down_pressed(self):
        self.current_command = "2\n"
        self.control_timer.start(50)  # Send every 50ms

    def on_left_pressed(self):
        self.current_command = "3\n"
        self.control_timer.start(50)  # Send every 50ms

    def on_right_pressed(self):
        self.current_command = "4\n"
        self.control_timer.start(50)  # Send every 50ms

    def on_stop_pressed(self):
        self.current_command = "5\n"
        self.control_timer.start(50)  # Send every 50ms

    def on_button_released(self):
        self.control_timer.stop()
        self.current_command = None
        print("Button released")

    def update_status(self, distance, sensor_status):
        self.distance = distance
        self.sensor_status = sensor_status
        self.distanceLabel.setText(f"Distance: {self.distance}")
        self.sensorStatusLabel.setText(f"Sensor Status: {self.sensor_status}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_widget = CameraWidget()
    camera_widget.show()
    sys.exit(app.exec())
