import hashlib

def get_blake2b_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    blake2_hasher = hashlib.blake2b(encoded_string)
    return blake2_hasher.hexdigest()

if __name__ == "__main__":
    text = input("Nhập chuỗi để băm với Blake2b: ")
    blake2_result = get_blake2b_hash(text)
    print(f"Chuỗi gốc: {text}")
    print(f"Giá trị băm Blake2b: {blake2_result}")