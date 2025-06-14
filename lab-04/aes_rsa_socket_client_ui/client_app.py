import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject

from ui.chat_window_ui import Ui_MainWindow
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunicationSignals(QObject):
    message_received = pyqtSignal(str)
    connection_failed = pyqtSignal(str)
    connection_success = pyqtSignal()

class ChatClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.client_socket = None
        self.aes_key = None
        self.signals = CommunicationSignals()

        self.ui.btnConnect.clicked.connect(self.connect_to_server)
        self.ui.btnSend.clicked.connect(self.send_message)
        self.ui.txtMessage.returnPressed.connect(self.send_message)

        self.signals.message_received.connect(self.display_message)
        self.signals.connection_failed.connect(self.show_connection_error)
        self.signals.connection_success.connect(self.on_connection_success)

    def connect_to_server(self):
        username = self.ui.txtName.text()
        if not username:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên của bạn.")
            return

        self.ui.btnConnect.setEnabled(False)
        self.ui.btnConnect.setText("Đang kết nối...")

        threading.Thread(target=self.connection_thread, args=(username,), daemon=True).start()

    def connection_thread(self, username):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 9999))

            server_public_key = self.client_socket.recv(450) # Kích thước có thể thay đổi

            self.client_socket.send(username.encode('utf-8'))

            self.aes_key = get_random_bytes(16) # AES-128

            rsa_key = RSA.import_key(server_public_key)
            rsa_cipher = PKCS1_OAEP.new(rsa_key)
            encrypted_aes_key = rsa_cipher.encrypt(self.aes_key)

            self.client_socket.send(encrypted_aes_key)

            self.signals.connection_success.emit()

            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

        except Exception as e:
            logging.error(f"Lỗi kết nối: {e}")
            self.signals.connection_failed.emit(str(e))

    def on_connection_success(self):
        self.ui.btnConnect.setText("Đã kết nối")
        self.ui.txtName.setReadOnly(True)
        self.ui.btnSend.setEnabled(True)
        self.ui.statusbar.showMessage("Kết nối thành công!", 5000)

    def show_connection_error(self, error_message):
        QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối đến server: {error_message}")
        self.ui.btnConnect.setEnabled(True)
        self.ui.btnConnect.setText("Kết nối")
        
    def receive_messages(self):
        while True:
            try:
                encrypted_message_with_iv = self.client_socket.recv(1024)
                if not encrypted_message_with_iv:
                    break

                iv = encrypted_message_with_iv[:16]
                encrypted_message = encrypted_message_with_iv[16:]

                cipher = AES.new(self.aes_key, AES.MODE_CFB, iv=iv)
                decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')

                self.signals.message_received.emit(decrypted_message)
            except Exception as e:
                logging.error(f"Lỗi khi nhận tin nhắn: {e}")
                self.signals.message_received.emit("Mất kết nối với server.")
                self.client_socket.close()
                break

    def send_message(self):
        message = self.ui.txtMessage.text()
        if message and self.client_socket:
            try:
                cipher = AES.new(self.aes_key, AES.MODE_CFB)
                iv = cipher.iv
                encrypted_message = cipher.encrypt(message.encode('utf-8'))

                self.client_socket.sendall(iv + encrypted_message)
                
                self.ui.txtMessage.clear()
            except Exception as e:
                logging.error(f"Lỗi khi gửi tin nhắn: {e}")
                self.display_message("Không thể gửi tin nhắn.")

    def display_message(self, message):
        self.ui.txtChatHistory.append(message)
    
    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatClient()
    window.show()
    sys.exit(app.exec_())