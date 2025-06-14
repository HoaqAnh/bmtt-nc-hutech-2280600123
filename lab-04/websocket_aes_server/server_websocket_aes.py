import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Server - %(levelname)s - %(message)s')

AES_KEY = b'MySecretKey12345'  # 16 bytes

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        logging.info("WebSocket opened")

    def on_message(self, message):
        logging.info(f"Received message: {message}")
        try:
            iv = get_random_bytes(16)

            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)

            padded_data = pad(message.encode('utf-8'), AES.block_size)

            encrypted_data = cipher.encrypt(padded_data)

            full_encrypted_message = iv + encrypted_data
            encrypted_message_b64 = base64.b64encode(full_encrypted_message).decode('utf-8')
            
            self.write_message(encrypted_message_b64)
            logging.info(f"Sent IV + encrypted (base64): {encrypted_message_b64}")

        except Exception as e:
            logging.error(f"Encryption error: {e}", exc_info=True)
            self.write_message(f"Error processing your message: {e}")

    def on_close(self):
        logging.info("WebSocket closed")

    def check_origin(self, origin):
        return True

def make_app():
    return tornado.web.Application([
        (r"/websocket", EchoWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    logging.info("Server is listening on port 8889...")
    tornado.ioloop.IOLoop.current().start()