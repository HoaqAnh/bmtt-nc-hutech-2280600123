def caesar_encrypt(text, key_int):
    result = ''
    if not isinstance(key_int, int):
        raise ValueError("'key' cho Caesar phải là một số nguyên")
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - start + key_int) % 26 + start)
            result += shifted_char
        else:
            result += char
    return result

def caesar_decrypt(text, key_int):
    if not isinstance(key_int, int):
        raise ValueError("'key' cho Caesar phải là một số nguyên")
    return caesar_encrypt(text, -key_int)