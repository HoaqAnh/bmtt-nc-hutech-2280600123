import hashlib

def get_md5_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    md5_hasher = hashlib.md5(encoded_string)
    return md5_hasher.hexdigest()

if __name__ == "__main__":
    text = input("Nhập chuỗi để băm với MD5: ")
    md5_result = get_md5_hash(text)
    print(f"Chuỗi gốc: {text}")
    print(f"Giá trị băm MD5: {md5_result}")