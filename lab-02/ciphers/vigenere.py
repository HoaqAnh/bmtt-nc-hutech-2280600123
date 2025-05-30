import re

def vigenere_process_key(key_string):
    processed_key = "".join(filter(str.isalpha, key_string)).upper()
    if not processed_key:
        raise ValueError("Key cho Vigenère phải chứa ít nhất một chữ cái.")
    return processed_key

def vigenere_crypt(text, key_string, encrypt=True):
    if not isinstance(key_string, str):
        raise ValueError("'key' cho Vigenère phải là một chuỗi.")
    processed_key = vigenere_process_key(key_string)
    key_len = len(processed_key)
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            start_char_ord = ord('a') if char.islower() else ord('A')
            key_char_ord = ord(processed_key[key_index % key_len]) - ord('A')
            char_ord = ord(char)
            if encrypt:
                shifted_ord = (char_ord - start_char_ord + key_char_ord) % 26 + start_char_ord
            else:
                shifted_ord = (char_ord - start_char_ord - key_char_ord + 26) % 26 + start_char_ord
            result.append(chr(shifted_ord))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def vigenere_encrypt(text, key_string):
    return vigenere_crypt(text, key_string, encrypt=True)

def vigenere_decrypt(text, key_string):
    return vigenere_crypt(text, key_string, encrypt=False)