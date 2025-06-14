import socket
import threading
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Server - %(levelname)s - %(message)s')

P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF
G = 2

server_private_key = 19876543210987654321098765432109876543210

def handle_client(conn, addr):
    logging.info(f"Kết nối được chấp nhận từ {addr}")
    try:
        server_public_key = pow(G, server_private_key, P)
        logging.info("Đã tính khóa công khai của server.")
        
        conn.send(str(P).encode())
        conn.recv(1024)
        conn.send(str(G).encode())
        conn.recv(1024)
        conn.send(str(server_public_key).encode())
        logging.info("Đã gửi P, G, và khóa công khai của server đến client.")

        client_public_key = int(conn.recv(2048).decode())
        logging.info("Đã nhận khóa công khai của client.")

        shared_secret = pow(client_public_key, server_private_key, P)
        logging.info("Đã tính khóa bí mật chung.")

        aes_key = hashlib.sha256(str(shared_secret).encode()).digest()[:16]
        logging.info("Đã tạo khóa AES từ khóa bí mật chung.")

        encrypted_data = conn.recv(1024)
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_message = unpad(aes_cipher.decrypt(encrypted_message), AES.block_size).decode()
        logging.info(f"Tin nhắn đã giải mã từ {addr}: {decrypted_message}")

        response_message = f"Chào {decrypted_message}, server đã nhận được tin nhắn của bạn!"
        aes_cipher_response = AES.new(aes_key, AES.MODE_CBC)
        iv_response = aes_cipher_response.iv
        encrypted_response = aes_cipher_response.encrypt(pad(response_message.encode(), AES.block_size))
        conn.send(iv_response + encrypted_response)
        logging.info("Đã gửi phản hồi mã hóa cho client.")

    except Exception as e:
        logging.error(f"Lỗi trong quá trình xử lý client {addr}: {e}")
    finally:
        conn.close()
        logging.info(f"Đã đóng kết nối với {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    server_socket.listen(5)
    logging.info("Server đang lắng nghe trên cổng 8888...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
