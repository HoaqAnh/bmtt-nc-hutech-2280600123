import sys
import websocket
import threading
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
from ui.websocket_window_ui import Ui_MainWindow
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

AES_KEY = b'MySecretKey12345'  # 16 bytes

class WorkerSignals(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    message_received = pyqtSignal(str)
    error = pyqtSignal(str)

class WebSocketThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.ws = None
        self.signals = WorkerSignals()
        self.daemon = True

    def run(self):
        try:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()
        except Exception as e:
            self.signals.error.emit(str(e))
        self.signals.disconnected.emit()

    def on_open(self, ws):
        self.signals.connected.emit()

    def on_message(self, ws, message):
        self.signals.message_received.emit(message)

    def on_error(self, ws, error):
        self.signals.error.emit(str(error))

    def on_close(self, ws, close_status_code, close_msg):
        pass

    def send(self, message):
        if self.ws:
            self.ws.send(message)

    def close(self):
        if self.ws:
            self.ws.close()

class WebSocketClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.is_connected = False
        self.ws_thread = None

        self.ui.btnConnect.clicked.connect(self.toggle_connection)
        self.ui.btnSend.clicked.connect(self.send_message)

    def log(self, message):
        self.ui.txtLog.append(message)

    def toggle_connection(self):
        if not self.is_connected:
            url = self.ui.txtUrl.text()
            if not url:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập URL của server.")
                return

            self.ui.btnConnect.setText("Đang kết nối...")
            self.ui.btnConnect.setEnabled(False)

            self.ws_thread = WebSocketThread(url)
            self.ws_thread.signals.connected.connect(self.on_connected)
            self.ws_thread.signals.disconnected.connect(self.on_disconnected)
            self.ws_thread.signals.message_received.connect(self.on_message_received)
            self.ws_thread.signals.error.connect(self.on_error)
            self.ws_thread.start()
        else:
            self.ws_thread.close()

    def on_connected(self):
        self.is_connected = True
        self.ui.btnConnect.setText("Ngắt kết nối")
        self.ui.btnConnect.setEnabled(True)
        self.ui.txtUrl.setReadOnly(True)
        self.ui.txtMessage.setEnabled(True)
        self.ui.btnSend.setEnabled(True)
        self.log(">>> Đã kết nối tới server.")
        self.ui.statusbar.showMessage("Kết nối thành công.", 3000)

    def on_disconnected(self):
        self.is_connected = False
        self.ui.btnConnect.setText("Kết nối")
        self.ui.btnConnect.setEnabled(True)
        self.ui.txtUrl.setReadOnly(False)
        self.ui.txtMessage.setEnabled(False)
        self.ui.btnSend.setEnabled(False)
        self.log(">>> Đã ngắt kết nối.")
        self.ui.statusbar.showMessage("Đã ngắt kết nối.", 3000)

    def on_message_received(self, message):
        self.log(f"Nhận được bản mã (Base64): {message}")
        try:
            encrypted_data_with_iv = base64.b64decode(message)

            iv = encrypted_data_with_iv[:16]
            encrypted_data = encrypted_data_with_iv[16:]

            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
            decrypted_padded_data = cipher.decrypt(encrypted_data)

            decrypted_data = unpad(decrypted_padded_data, AES.block_size).decode('utf-8')
            
            self.log(f"Giải mã thành công: {decrypted_data}")
        except (ValueError, KeyError, TypeError) as e:
            self.log(f"Lỗi giải mã: {e}. Dữ liệu nhận được có thể không hợp lệ hoặc không được mã hóa đúng cách.")

    def on_error(self, error):
        self.log(f"Lỗi: {error}")
        QMessageBox.critical(self, "Lỗi WebSocket", str(error))
        self.on_disconnected()

    def send_message(self):
        message = self.ui.txtMessage.text()
        if self.is_connected and message:
            self.log(f"Gửi đi: {message}")
            self.ws_thread.send(message)
            self.ui.txtMessage.clear()

    def closeEvent(self, event):
        if self.ws_thread:
            self.ws_thread.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebSocketClientApp()
    window.show()
    sys.exit(app.exec_())