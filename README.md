# Thực hành: Bảo mật Thông tin Nâng cao

## Giới thiệu

Mục tiêu của kho lưu trữ này là:
* Lưu trữ mã nguồn của các bài thực hành.
* Trình bày việc triển khai các thuật toán mã hóa và các khái niệm an toàn mạng bằng ngôn ngữ Python.
* Xây dựng các ứng dụng client-server để minh họa hoạt động của các giao thức bảo mật trong thực tế.

---

## Các chủ đề và bài thực hành đã thực hiện

Repository này bao gồm việc triển khai các khái niệm và thuật toán sau:

### **Bài 1: Lập trình Python cơ bản**
* Ôn tập các khái niệm cốt lõi của Python.
* Lập trình hướng đối tượng (OOP) trong Python.

### **Bài 2: Mã hóa Cổ điển với Python**
* Triển khai các thuật toán mã hóa cổ điển:
    * Caesar
    * Vigenère
    * Rail Fence
    * Playfair
    * Transposition
* Xây dựng API server bằng **Flask** để cung cấp các dịch vụ mã hóa/giải mã.

### **Bài 3: Lập trình Giao diện và Mã hóa Hiện đại**
* Xây dựng ứng dụng Desktop với giao diện đồ họa (GUI) bằng **PyQt5**.
* Triển khai các thuật toán mã hóa bất đối xứng:
    * **RSA**: Tạo khóa, mã hóa/giải mã, ký/xác thực chữ ký số.
    * **ECC**: Tạo khóa, ký/xác thực chữ ký số.
* Thiết kế kiến trúc Client-Server, trong đó ứng dụng GUI (client) giao tiếp với các API server (Flask) để thực hiện các tác vụ mã hóa.

---

## Cấu trúc Thư mục

Dự án được tổ chức theo kiến trúc client-server để mô phỏng các ứng dụng thực tế.
```bash
.
├── lab-02/                       # Server cho các mã hóa cổ điển
│   ├── ciphers/
│   ├── templates/
│   ├── app.py
│   └── requirements.txt
│
├── lab03-rsa-server/             # Server cho các chức năng của RSA
│   ├── keys/
│   ├── api_server_rsa.py
│   └── requirements.txt
│
├── lab03-ecc-server/             # Server cho các chức năng của ECC
│   ├── keys/
│   ├── api_server_ecc.py
│   └── requirements.txt
│
└── lab03-client-app/             # Ứng dụng Client chính có giao diện
├── ui/
│   └── main_window_ui.py
├── platforms/
├── main_app.py
└── requirements.txt
```

---

## Cài đặt & Chuẩn bị môi trường

Để chạy được dự án, cần cài đặt các thư viện cần thiết cho từng thành phần.

1.  **Clone repository:**
    ```bash
    git clone https://github.com/HoaqAnh/bmtt-nc-hutech-2280600123.git
    cd bmtt-nc-hutech-2280600123
    ```

2.  **Cài đặt cho các Server:**
    Mở Terminal và di chuyển vào từng thư mục server (`lab-02`, `lab03-rsa-server`, `lab03-ecc-server`) và chạy lệnh:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Cài đặt cho Client App:**
    Di cKhởi động các server API **trước khi** chạy ứng dụng client. Hãy mở các cửa sổ Terminal riêng biệt cho mỗi thành phần.

1.  **Chạy Server Mã hóa Cổ điển (Cổng 5000):**
    ```bash
    # Di chuyển đến thư mục server của Bài 2
    python api.py
    ```

2.  **Chạy Server RSA (Cổng 5001):**
    ```bash
    # Di chuyển đến thư mục lab03-rsa-server
    python api_server_rsa.py
    ```

3.  **Chạy Server ECC (Cổng 5002):**
    ```bash
    # Di chuyển đến thư mục lab03-ecc-server
    python api_server_ecc.py
    ```

4.  **Chạy Ứng dụng Client:**
    Sau khi cả ba server đã khởi động, mở một Terminal mới, di chuyển đến thư mục `lab03-client-app` và chạy:
    ```bash
    python main_app.py
    ```

---

## Tác giả

* **Họ và tên:** Trần Phạm Hoàng Anh
* **Mã số sinh viên:** 2280600123
* **Lớp:** 22DTHG3

