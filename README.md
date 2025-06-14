# Thực hành: Bảo mật Thông tin Nâng cao

## Giới thiệu

Mục tiêu của kho lưu trữ này là:
* Lưu trữ mã nguồn của các bài thực hành.
* Trình bày việc triển khai các thuật toán mã hóa và các khái niệm an toàn mạng bằng ngôn ngữ Python.
* Xây dựng các ứng dụng client-server để minh họa hoạt động của các giao thức bảo mật trong thực tế.

---

## Các chủ đề và bài thực hành đã thực hiện

### **Bài 1: Lập trình cơ bản với Python**
* Ôn tập các khái niệm cốt lõi của Python.
* Lập trình hướng đối tượng (OOP) trong Python.

### **Bài 2: Mã hóa với Python**
* Triển khai các thuật toán mã hóa cổ điển: Caesar, Vigenère, Rail Fence, Playfair, Transposition.
* Xây dựng API server bằng **Flask** để cung cấp các dịch vụ mã hóa/giải mã.

### **Bài 3: Lập trình giao diện ứng dụng bảo mật**
* Xây dựng ứng dụng Desktop với giao diện đồ họa (GUI) bằng **PyQt5**.
* Triển khai các thuật toán mã hóa bất đối xứng:
    * **RSA**: Tạo khóa, mã hóa/giải mã, ký/xác thực chữ ký số.
    * **ECC**: Tạo khóa, ký/xác thực chữ ký số.
* Thiết kế kiến trúc Client-Server, trong đó ứng dụng GUI (client) giao tiếp với các API server (Flask) để thực hiện các tác vụ mã hóa.

### **Bài 4: Socket, Websocket, Trao đổi khóa và hàm băm**
* Socket:
    * Xây dựng ứng dụng chat client-server.
    * Sử dụng **RSA** để trao đổi khóa **AES** một cách an toàn.
    * Mã hóa toàn bộ phiên trò chuyện bằng **AES**.
* Trao đổi khóa Diffie-Hellman (DH):
    * Triển khai Giao thức DH để hai bên thiết lập một khóa bí mật chung trên một kênh không an toàn.
    * Sử dụng khóa chung để mã hóa và giải mã tin nhắn.
* Các Hàm băm:
    * Triển khai và so sánh các hàm băm phổ biến: MD5, SHA-256, SHA-3, Blake2.
* WebSocket và Tornado:
    * Xây dựng một ứng dụng chat thời gian thực bằng WebSocket với framework Tornado.
    * Mã hóa tin nhắn truyền qua WebSocket bằng **AES**.
* Xây dựng giao diện desktop (PyQt5) cho tất cả các ứng dụng trên.

---

## Cấu trúc Thư mục

```bash
.
├── lab-02/
│   ├── ciphers/
│   ├── templates/
│   ├── app.py
│   └── requirements.txt
│
├── lab-03/
│   ├── lab03-rsa-server/
│   ├── lab03-ecc-server/
│   └── lab03-client-app/
│
└── lab-04/
    ├── aes_rsa_socket_server/
    ├── aes_rsa_socket_client_ui/
    ├── dh_key_pair_server/
    ├── dh_key_pair_client_ui/
    ├── hash_functions_cli/
    ├── hash_functions_ui/
    ├── websocket_aes_server/
    └── websocket_aes_client_ui/
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
    Mở Terminal và di chuyển vào từng thư mục server (`lab-02`, `lab03-rsa-server`, `lab-04/aes_rsa_socket_server`, v.v.) và chạy lệnh:
    ```bash
    pip install -r requirements.txt
    ```
    Lưu ý: Mỗi thư mục con trong `lab-04` đều có file `requirements.txt` riêng.

---

## Tác giả

* **Họ và tên:** Trần Phạm Hoàng Anh
* **Mã số sinh viên:** 2280600123
* **Lớp:** 22DTHG3

