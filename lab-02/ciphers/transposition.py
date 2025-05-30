import math

def transposition_encrypt(text, key_string):
    if not isinstance(key_string, str) or not key_string:
        raise ValueError("Khóa Transposition không được để trống.")
    
    num_cols = len(key_string)
    if num_cols == 0:
        raise ValueError("Khóa Transposition không được rỗng.")
    if not text: return ""

    key_char_indices = sorted([(char, i) for i, char in enumerate(key_string)])
    
    ciphertext_parts = []
    for _, original_col_index in key_char_indices:
        pointer = original_col_index
        while pointer < len(text):
            ciphertext_parts.append(text[pointer])
            pointer += num_cols
            
    return "".join(ciphertext_parts)

def transposition_decrypt(ciphertext, key_string):
    if not isinstance(key_string, str) or not key_string:
        raise ValueError("Khóa Transposition không được để trống.")

    num_cols = len(key_string)
    if num_cols == 0:
        raise ValueError("Khóa Transposition không được rỗng.")
    if not ciphertext: return ""
        
    text_len = len(ciphertext)
    num_rows = math.ceil(text_len / num_cols)

    col_lengths = [0] * num_cols
    base_len = text_len // num_cols
    remainder = text_len % num_cols
    for i in range(num_cols):
        col_lengths[i] = base_len + (1 if i < remainder else 0)

    key_char_indices_sorted = sorted([(char, i) for i, char in enumerate(key_string)])

    plaintext_cols = [''] * num_cols 
    
    current_cipher_char_index = 0

    for _, original_col_index_of_key_char in key_char_indices_sorted:
        num_chars_in_this_column = col_lengths[original_col_index_of_key_char]
        
        plaintext_cols[original_col_index_of_key_char] = ciphertext[current_cipher_char_index : current_cipher_char_index + num_chars_in_this_column]
        current_cipher_char_index += num_chars_in_this_column

    plaintext_chars_list = []
    for row_index in range(num_rows):
        for original_col_index in range(num_cols):
            if row_index < len(plaintext_cols[original_col_index]):
                plaintext_chars_list.append(plaintext_cols[original_col_index][row_index])
                
    return "".join(plaintext_chars_list)