import hashlib

def get_sha3_256_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    sha3_hasher = hashlib.sha3_256(encoded_string)
    return sha3_hasher.hexdigest()

if __name__ == "__main__":
    text = input("Nhập chuỗi để băm với SHA3-256: ")
    sha3_result = get_sha3_256_hash(text)
    print(f"Chuỗi gốc: {text}")
    print(f"Giá trị băm SHA3-256: {sha3_result}")