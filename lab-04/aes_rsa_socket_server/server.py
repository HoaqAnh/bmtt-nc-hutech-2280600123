import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

clients = []
client_data = {}

def generate_keys():
    try:
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        logging.info("Tạo cặp khóa RSA thành công.")
        return private_key, public_key
    except Exception as e:
        logging.error(f"Lỗi khi tạo khóa RSA: {e}")
        return None, None

def handle_client(client_socket, addr, rsa_private_key):
    logging.info(f"Chấp nhận kết nối từ {addr}")
    
    try:
        client_socket.send(public_key)
        logging.info(f"Đã gửi khóa công khai RSA đến {addr}")

        name = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Client {addr} đã đặt tên là: {name}")

        encrypted_aes_key = client_socket.recv(256)

        rsa_cipher = PKCS1_OAEP.new(RSA.import_key(rsa_private_key))
        aes_key = rsa_cipher.decrypt(encrypted_aes_key)
        logging.info(f"Đã giải mã khóa AES từ {name} thành công.")

        clients.append(client_socket)
        client_data[client_socket] = (aes_key, name)

        broadcast(f"{name} đã tham gia cuộc trò chuyện!", client_socket)
        
        while True:
            encrypted_message_with_iv = client_socket.recv(1024)
            if not encrypted_message_with_iv:
                break

            iv = encrypted_message_with_iv[:16]
            encrypted_message = encrypted_message_with_iv[16:]

            aes_cipher = AES.new(aes_key, AES.MODE_CFB, iv=iv)
            message = aes_cipher.decrypt(encrypted_message).decode('utf-8')
            
            logging.info(f"Tin nhắn nhận từ {name}: {message}")

            broadcast(f"{name}: {message}", client_socket)

    except Exception as e:
        logging.error(f"Lỗi khi xử lý client {addr}: {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
            name_to_remove = client_data[client_socket][1]
            del client_data[client_socket]
            broadcast(f"{name_to_remove} đã rời khỏi cuộc trò chuyện.", None)
        client_socket.close()
        logging.info(f"Đã đóng kết nối với {addr}")

def broadcast(message, sender_socket):
    logging.info(f"Phát tin nhắn: {message}")
    for client in clients:
        aes_key = client_data[client][0]
        aes_cipher = AES.new(aes_key, AES.MODE_CFB)
        iv = aes_cipher.iv
        encrypted_message = aes_cipher.encrypt(message.encode('utf-8'))
        
        try:
            client.send(iv + encrypted_message)
        except Exception as e:
            logging.error(f"Lỗi khi gửi tin nhắn đến client: {e}")
            client.close()
            if client in clients:
                clients.remove(client)


# --- Khởi động Server ---
private_key, public_key = generate_keys()

if not private_key:
    logging.error("Không thể tạo khóa RSA. Server dừng hoạt động.")
else:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    logging.info("Server đang lắng nghe trên cổng 9999...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr, private_key))
        thread.start()
