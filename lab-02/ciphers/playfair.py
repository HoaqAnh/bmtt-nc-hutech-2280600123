import re

def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    key = "".join(re.findall("[A-Z]", key))
    
    key_letters = []
    for letter in key:
        if letter not in key_letters:
            key_letters.append(letter)
    
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for letter in alphabet:
        if letter not in key_letters:
            key_letters.append(letter)
            
    if not key_letters:
         raise ValueError("Khóa Playfair không hợp lệ (phải chứa ít nhất một chữ cái).")

    matrix = [key_letters[i:i+5] for i in range(0, 25, 5)]
    return matrix

def find_char_coords(matrix, char):
    for r, row in enumerate(matrix):
        for c, col_char in enumerate(row):
            if col_char == char:
                return r, c
    return None, None 

def prepare_playfair_text(text, filler='X'):
    text = text.upper().replace("J", "I")
    text = "".join(re.findall("[A-Z]", text))
    
    if not text:
        return []

    prepared_text = []
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i+1]
            if char1 == char2:
                prepared_text.extend([char1, filler])
                i += 1 
            else:
                prepared_text.extend([char1, char2])
                i += 2
        else: 
            prepared_text.extend([char1, filler])
            i += 1
            
    return [tuple(prepared_text[j:j+2]) for j in range(0, len(prepared_text), 2)]

def playfair_crypt_digraph(matrix, digraph, encrypt=True):
    char1, char2 = digraph
    r1, c1 = find_char_coords(matrix, char1)
    r2, c2 = find_char_coords(matrix, char2)

    if r1 is None or c1 is None or r2 is None or c2 is None:
         raise ValueError(f"Ký tự không tìm thấy trong ma trận: {char1} hoặc {char2}")

    shift = 1 if encrypt else -1
    if r1 == r2: 
        return matrix[r1][(c1 + shift) % 5], matrix[r2][(c2 + shift) % 5]
    elif c1 == c2: 
        return matrix[(r1 + shift) % 5][c1], matrix[(r2 + shift) % 5][c2]
    else: 
        return matrix[r1][c2], matrix[r2][c1]

def playfair_encrypt(text, key):
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Khóa Playfair không được để trống.")
    matrix = generate_playfair_matrix(key)
    digraphs = prepare_playfair_text(text)
    if not digraphs: return "" 
    
    cipher_text = []
    for digraph in digraphs:
        cipher_text.extend(playfair_crypt_digraph(matrix, digraph, encrypt=True))
    return "".join(cipher_text)

def playfair_decrypt(cipher_text, key):
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Khóa Playfair không được để trống.")
    matrix = generate_playfair_matrix(key)
    cipher_text_upper = cipher_text.upper().replace("J", "I")
    cipher_text_alpha = "".join(re.findall("[A-Z]", cipher_text_upper))


    if len(cipher_text_alpha) % 2 != 0:
        raise ValueError("Ciphertext của Playfair (sau khi lọc chữ cái) phải có độ dài chẵn.")
    if not cipher_text_alpha: return ""

    digraphs = [tuple(cipher_text_alpha[i:i+2]) for i in range(0, len(cipher_text_alpha), 2)]
    
    plain_text_chars = []
    for digraph in digraphs:
        plain_text_chars.extend(playfair_crypt_digraph(matrix, digraph, encrypt=False))

    return "".join(plain_text_chars)