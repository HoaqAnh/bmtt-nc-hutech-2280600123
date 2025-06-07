import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.main_window_ui import Ui_MainWindow

# Địa chỉ của server API Flask
API_BASE_URL = "http://127.0.0.1:5000/api"

class CipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút bấm với các hàm xử lý tương ứng
        self.connect_signals()

    def connect_signals(self):
        """Hàm này kết nối tất cả các tín hiệu (như click chuột) với các slot (hàm xử lý)."""
        # Caesar
        self.ui.caesar_btn_encrypt.clicked.connect(self.handle_caesar_encrypt)
        self.ui.caesar_btn_decrypt.clicked.connect(self.handle_caesar_decrypt)
        
        # Vigenere
        self.ui.vigenere_btn_encrypt.clicked.connect(self.handle_vigenere_encrypt)
        self.ui.vigenere_btn_decrypt.clicked.connect(self.handle_vigenere_decrypt)

        # Rail Fence
        self.ui.railfence_btn_encrypt.clicked.connect(self.handle_railfence_encrypt)
        self.ui.railfence_btn_decrypt.clicked.connect(self.handle_railfence_decrypt)

        # Playfair
        self.ui.playfair_btn_encrypt.clicked.connect(self.handle_playfair_encrypt)
        self.ui.playfair_btn_decrypt.clicked.connect(self.handle_playfair_decrypt)
        
        # Transposition
        self.ui.transposition_btn_encrypt.clicked.connect(self.handle_transposition_encrypt)
        self.ui.transposition_btn_decrypt.clicked.connect(self.handle_transposition_decrypt)

    def show_message(self, title, message, icon=QMessageBox.Information):
        """Hiển thị một hộp thoại thông báo."""
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def call_api(self, endpoint, payload):
        """Hàm chung để gọi API và xử lý kết quả."""
        try:
            # Thêm timeout để tránh việc treo ứng dụng vĩnh viễn
            response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload, timeout=10)
            response.raise_for_status()  # Ném lỗi nếu mã trạng thái là 4xx hoặc 5xx
            return response.json()
        except requests.exceptions.Timeout:
            self.show_message("Lỗi Mạng", "Server không phản hồi (timeout).", QMessageBox.Critical)
            return None
        except requests.exceptions.RequestException as e:
            self.show_message("Lỗi Mạng", f"Không thể kết nối đến server API: {e}\n"
                              "Hãy đảm bảo bạn đã chạy file `app.py` từ `lab-02`.", QMessageBox.Critical)
            return None

    # --- Các hàm xử lý cho Caesar ---
    def handle_caesar_encrypt(self):
        text = self.ui.caesar_text_plain.toPlainText()
        key_str = self.ui.caesar_line_key.text()
        if not text or not key_str:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản và khóa.")
            return
        
        try:
            key_int = int(key_str)
        except ValueError:
            self.show_message("Lỗi Khóa Caesar", "Khóa cho Caesar phải là một số nguyên.", QMessageBox.Warning)
            return
            
        payload = {"text": text, "key": key_int}
        result = self.call_api("caesar/encrypt", payload)
        
        if result and "encrypted_text" in result:
            self.ui.caesar_text_cipher.setText(result["encrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    def handle_caesar_decrypt(self):
        text = self.ui.caesar_text_cipher.toPlainText()
        key_str = self.ui.caesar_line_key.text()
        if not text or not key_str:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản mã hóa và khóa.")
            return

        try:
            key_int = int(key_str)
        except ValueError:
            self.show_message("Lỗi Khóa Caesar", "Khóa cho Caesar phải là một số nguyên.", QMessageBox.Warning)
            return

        payload = {"text": text, "key": key_int}
        result = self.call_api("caesar/decrypt", payload)

        if result and "decrypted_text" in result:
            self.ui.caesar_text_plain.setText(result["decrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)
            
    # --- Các hàm xử lý cho Vigenere ---
    def handle_vigenere_encrypt(self):
        text = self.ui.vigenere_text_plain.toPlainText()
        key = self.ui.vigenere_line_key.text()
        if not text or not key:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản và khóa.")
            return
        
        # Thêm kiểm tra khóa Vigenere ở client
        if not any(c.isalpha() for c in key):
            self.show_message("Lỗi Khóa Vigenère", "Khóa cho Vigenère phải chứa ít nhất một chữ cái.", QMessageBox.Warning)
            return
            
        payload = {"text": text, "key": key}
        result = self.call_api("vigenere/encrypt", payload)
        
        if result and "encrypted_text" in result:
            self.ui.vigenere_text_cipher.setText(result["encrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    def handle_vigenere_decrypt(self):
        text = self.ui.vigenere_text_cipher.toPlainText()
        key = self.ui.vigenere_line_key.text()
        if not text or not key:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản mã hóa và khóa.")
            return

        # Thêm kiểm tra khóa Vigenere ở client
        if not any(c.isalpha() for c in key):
            self.show_message("Lỗi Khóa Vigenère", "Khóa cho Vigenère phải chứa ít nhất một chữ cái.", QMessageBox.Warning)
            return

        payload = {"text": text, "key": key}
        result = self.call_api("vigenere/decrypt", payload)

        if result and "decrypted_text" in result:
            self.ui.vigenere_text_plain.setText(result["decrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    # --- Các hàm xử lý cho Rail Fence ---
    def handle_railfence_encrypt(self):
        text = self.ui.railfence_text_plain.toPlainText()
        key_str = self.ui.railfence_line_key.text()
        if not text or not key_str:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản và khóa (số hàng rào).")
            return
        
        # Thêm kiểm tra khóa Rail Fence ở client
        try:
            key_int = int(key_str)
            if key_int < 2:
                self.show_message("Lỗi Khóa Rail Fence", "Khóa (số hàng rào) phải là một số nguyên lớn hơn hoặc bằng 2.", QMessageBox.Warning)
                return
        except ValueError:
            self.show_message("Lỗi Khóa Rail Fence", "Khóa (số hàng rào) phải là một số nguyên.", QMessageBox.Warning)
            return
            
        payload = {"text": text, "key": key_int}
        result = self.call_api("railfence/encrypt", payload)
        
        if result and "encrypted_text" in result:
            self.ui.railfence_text_cipher.setText(result["encrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    def handle_railfence_decrypt(self):
        text = self.ui.railfence_text_cipher.toPlainText()
        key_str = self.ui.railfence_line_key.text()
        if not text or not key_str:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản mã hóa và khóa (số hàng rào).")
            return

        # Thêm kiểm tra khóa Rail Fence ở client
        try:
            key_int = int(key_str)
            if key_int < 2:
                self.show_message("Lỗi Khóa Rail Fence", "Khóa (số hàng rào) phải là một số nguyên lớn hơn hoặc bằng 2.", QMessageBox.Warning)
                return
        except ValueError:
            self.show_message("Lỗi Khóa Rail Fence", "Khóa (số hàng rào) phải là một số nguyên.", QMessageBox.Warning)
            return

        payload = {"text": text, "key": key_int}
        result = self.call_api("railfence/decrypt", payload)

        if result and "decrypted_text" in result:
            self.ui.railfence_text_plain.setText(result["decrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    # --- Các hàm xử lý cho Playfair ---
    def handle_playfair_encrypt(self):
        text = self.ui.playfair_text_plain.toPlainText()
        key = self.ui.playfair_line_key.text()
        if not text or not key:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản và khóa.")
            return
            
        payload = {"text": text, "key": key}
        result = self.call_api("playfair/encrypt", payload)
        
        if result and "encrypted_text" in result:
            self.ui.playfair_text_cipher.setText(result["encrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    def handle_playfair_decrypt(self):
        text = self.ui.playfair_text_cipher.toPlainText()
        key = self.ui.playfair_line_key.text()
        if not text or not key:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản mã hóa và khóa.")
            return

        payload = {"text": text, "key": key}
        result = self.call_api("playfair/decrypt", payload)

        if result and "decrypted_text" in result:
            self.ui.playfair_text_plain.setText(result["decrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    # --- Các hàm xử lý cho Transposition ---
    def handle_transposition_encrypt(self):
        text = self.ui.transposition_text_plain.toPlainText()
        key = self.ui.transposition_line_key.text()
        if not text or not key:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản và khóa.")
            return
            
        payload = {"text": text, "key": key}
        result = self.call_api("transposition/encrypt", payload)
        
        if result and "encrypted_text" in result:
            self.ui.transposition_text_cipher.setText(result["encrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

    def handle_transposition_decrypt(self):
        text = self.ui.transposition_text_cipher.toPlainText()
        key = self.ui.transposition_line_key.text()
        if not text or not key:
            self.show_message("Lỗi đầu vào", "Vui lòng nhập đầy đủ văn bản mã hóa và khóa.")
            return

        payload = {"text": text, "key": key}
        result = self.call_api("transposition/decrypt", payload)

        if result and "decrypted_text" in result:
            self.ui.transposition_text_plain.setText(result["decrypted_text"])
        elif result and "error" in result:
            self.show_message("Lỗi API", result["error"], QMessageBox.Warning)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec_())
