def rail_fence_encrypt(text, rails):
    if not isinstance(rails, int):
        raise ValueError("'key' (số hàng rào) cho Rail Fence phải là một số nguyên.")
    if rails < 2:
        raise ValueError("Số hàng rào (key) cho Rail Fence phải lớn hơn hoặc bằng 2.")
    if rails >= len(text) or len(text) <=1:
        return text

    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1
    
    encrypted_text = "".join(["".join(row) for row in fence])
    return encrypted_text

def rail_fence_decrypt(cipher_text, rails):
    if not isinstance(rails, int):
        raise ValueError("'key' (số hàng rào) cho Rail Fence phải là một số nguyên.")
    if rails < 2:
        raise ValueError("Số hàng rào (key) cho Rail Fence phải lớn hơn hoặc bằng 2.")
    
    text_len = len(cipher_text)
    if rails >= text_len or text_len <= 1:
        return cipher_text

    fence = [['' for _ in range(text_len)] for _ in range(rails)]
    
    rail = 0
    direction = 1
    for j in range(text_len):
        fence[rail][j] = '*'
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1
            
    index = 0
    for i in range(rails):
        for j in range(text_len):
            if fence[i][j] == '*' and index < text_len:
                fence[i][j] = cipher_text[index]
                index += 1
                
    decrypted_text = []
    rail = 0
    direction = 1
    for j in range(text_len):
        decrypted_text.append(fence[rail][j])
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1
            
    return "".join(decrypted_text)