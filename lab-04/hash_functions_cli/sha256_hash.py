import hashlib

def get_sha256_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hasher = hashlib.sha256(encoded_string)
    return sha256_hasher.hexdigest()

if __name__ == "__main__":
    text = input("Nhập chuỗi để băm với SHA-256: ")
    sha256_result = get_sha256_hash(text)
    print(f"Chuỗi gốc: {text}")
    print(f"Giá trị băm SHA-256: {sha256_result}")