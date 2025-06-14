import socket
import threading
import sys
import hashlib
from os import urandom
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject

from ui.dh_window_ui import Ui_MainWindow
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Client - %(levelname)s - %(message)s')

class DH_Signals(QObject):
    connection_failed = pyqtSignal(str)
    key_exchange_success = pyqtSignal(dict)
    message_received = pyqtSignal(str)
    log_message = pyqtSignal(str)

class DHClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.client_socket = None
        self.aes_key = None
        self.signals = DH_Signals()

        self.ui.btnConnect.clicked.connect(self.start_key_exchange)
        self.ui.btnSend.clicked.connect(self.send_encrypted_message)
        self.signals.connection_failed.connect(self.show_error)
        self.signals.key_exchange_success.connect(self.update_ui_with_keys)
        self.signals.message_received.connect(self.log_server_response)
        self.signals.log_message.connect(self.log)

    def log(self, message):
        self.ui.txtLog.append(message)
        
    def show_error(self, message):
        QMessageBox.critical(self, "Lỗi", message)
        self.ui.btnConnect.setEnabled(True)
        self.ui.btnConnect.setText("Kết nối và Trao đổi khóa")

    def start_key_exchange(self):
        self.ui.btnConnect.setEnabled(False)
        self.ui.btnConnect.setText("Đang trao đổi khóa...")
        threading.Thread(target=self.key_exchange_thread, daemon=True).start()

    def key_exchange_thread(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 8888))
            self.signals.log_message.emit("Đã kết nối tới server.")

            P = int(self.client_socket.recv(2048).decode())
            self.signals.log_message.emit(f"Nhận P: {P}")
            self.client_socket.send(b'ack')

            G = int(self.client_socket.recv(2048).decode())
            self.signals.log_message.emit(f"Nhận G: {G}")
            self.client_socket.send(b'ack')
            
            server_public_key = int(self.client_socket.recv(2048).decode())
            self.signals.log_message.emit("Nhận khóa công khai của server.")

            client_private_key = int.from_bytes(urandom(32), 'big')
            client_public_key = pow(G, client_private_key, P)
            self.signals.log_message.emit("Đã tạo khóa của client.")

            self.client_socket.send(str(client_public_key).encode())
            self.signals.log_message.emit("Đã gửi khóa công khai cho server.")

            shared_secret = pow(server_public_key, client_private_key, P)
            self.aes_key = hashlib.sha256(str(shared_secret).encode()).digest()[:16]
            self.signals.log_message.emit("Đã tạo khóa bí mật chung và khóa AES.")

            key_info = {
                'P': str(P), 'G': str(G),
                'server_public_key': str(server_public_key),
                'client_public_key': str(client_public_key),
                'shared_secret_hex': str(shared_secret.to_bytes(256, 'big').hex())
            }
            self.signals.key_exchange_success.emit(key_info)

        except Exception as e:
            self.signals.connection_failed.emit(f"Lỗi trao đổi khóa: {e}")

    def update_ui_with_keys(self, key_info):
        self.ui.txtP.setText(key_info['P'])
        self.ui.txtG.setText(key_info['G'])
        self.ui.txtServerPublicKey.setText(key_info['server_public_key'])
        self.ui.txtClientPublicKey.setText(key_info['client_public_key'])
        self.ui.txtSharedSecret.setText(key_info['shared_secret_hex'])
        
        self.ui.btnConnect.setText("Trao đổi khóa thành công")
        self.ui.btnSend.setEnabled(True)
        self.ui.statusbar.showMessage("Sẵn sàng gửi tin nhắn mã hóa.", 5000)

    def send_encrypted_message(self):
        message = self.ui.txtMessage.text()
        if not message:
            self.show_error("Vui lòng nhập tin nhắn.")
            return
        if not self.aes_key:
            self.show_error("Khóa AES chưa được tạo. Vui lòng trao đổi khóa trước.")
            return
            
        self.ui.btnSend.setEnabled(False)
        try:
            aes_cipher = AES.new(self.aes_key, AES.MODE_CBC)
            iv = aes_cipher.iv
            encrypted_message = aes_cipher.encrypt(pad(message.encode(), AES.block_size))

            threading.Thread(target=self.send_and_receive_thread, args=(iv + encrypted_message,), daemon=True).start()

        except Exception as e:
            self.show_error(f"Lỗi khi mã hóa hoặc gửi tin: {e}")
            self.ui.btnSend.setEnabled(True)

    def send_and_receive_thread(self, data_to_send):
        try:
            self.client_socket.send(data_to_send)
            self.signals.log_message.emit("Đã gửi tin nhắn mã hóa. Đang chờ phản hồi...")

            encrypted_response = self.client_socket.recv(1024)
            iv_response = encrypted_response[:16]
            encrypted_message_response = encrypted_response[16:]

            aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, iv_response)
            decrypted_response = unpad(aes_cipher.decrypt(encrypted_message_response), AES.block_size).decode()

            self.signals.message_received.emit(decrypted_response)
        except Exception as e:
            self.signals.connection_failed.emit(f"Lỗi khi giao tiếp với server: {e}")
        finally:
            self.ui.btnSend.setEnabled(True)


    def log_server_response(self, message):
        self.log(f"Phản hồi từ Server: {message}")
        self.ui.statusbar.showMessage("Đã nhận phản hồi từ server.", 5000)

    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DHClient()
    window.show()
    sys.exit(app.exec_())