import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui.hash_window_ui import Ui_MainWindow

class HashApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.algorithms = {
            "MD5": hashlib.md5,
            "SHA-256": hashlib.sha256,
            "SHA-3 (256-bit)": hashlib.sha3_256,
            "Blake2b": hashlib.blake2b
        }

        self.ui.comboAlgorithm.addItems(self.algorithms.keys())

        self.ui.btnSelectFile.clicked.connect(self.select_file)
        self.ui.btnHashText.clicked.connect(self.hash_text)
        self.ui.btnHashFile.clicked.connect(self.hash_file)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Chọn một tệp", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.ui.txtFilePath.setText(file_name)
            self.ui.statusbar.showMessage(f"Đã chọn tệp: {file_name}", 5000)

    def hash_text(self):
        input_text = self.ui.txtInputText.toPlainText()
        if not input_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập văn bản để băm.")
            return

        selected_algorithm_name = self.ui.comboAlgorithm.currentText()
        hasher_constructor = self.algorithms[selected_algorithm_name]
        
        try:
            hasher = hasher_constructor()
            hasher.update(input_text.encode('utf-8'))
            hash_result = hasher.hexdigest()
            
            self.ui.txtResult.setText(hash_result)
            self.ui.statusbar.showMessage("Băm văn bản thành công!", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi băm văn bản: {e}")

    def hash_file(self):
        file_path = self.ui.txtFilePath.text()
        if not file_path:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một tệp để băm.")
            return
            
        selected_algorithm_name = self.ui.comboAlgorithm.currentText()
        hasher_constructor = self.algorithms[selected_algorithm_name]

        try:
            hasher = hasher_constructor()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            
            hash_result = hasher.hexdigest()
            self.ui.txtResult.setText(hash_result)
            self.ui.statusbar.showMessage("Băm tệp thành công!", 3000)

        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp. Vui lòng kiểm tra lại đường dẫn.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi băm tệp: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashApp()
    window.show()
    sys.exit(app.exec_())