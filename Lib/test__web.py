import socket
import time
host = '192.168.1.63'  # Địa chỉ IP của ESP32
port = 80  # Cổng của ESP32

# Tạo một socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối tới máy chủ
client_socket.connect((host, port))
count = 0
while True:
    # Gửi dữ liệu tới ESP32
    message = "Hello ESP32"
    count += 1
    print(f"Sending to ESP32: {count}")
    client_socket.sendall(str(f"{count}\n").encode())

    # # Nhận phản hồi từ ESP32
    # response = client_socket.recv(1024)
    # print('Received from ESP32:', response.decode())
    # print()
    time.sleep(0.2)

# Đóng kết nối
client_socket.close()
