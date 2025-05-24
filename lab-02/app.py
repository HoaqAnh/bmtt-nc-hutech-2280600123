from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- 1. Logic Mã Hóa Caesar ---
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

# --- 2. Logic Mã Hóa Vigenère ---
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

# --- 3. Logic Mã Hóa Rail Fence ---
def rail_fence_encrypt(text, rails):
    """Mã hóa văn bản bằng Rail Fence cipher."""
    if not isinstance(rails, int):
        raise ValueError("'key' (số hàng rào) cho Rail Fence phải là một số nguyên.")
    if rails < 2:
        raise ValueError("Số hàng rào (key) cho Rail Fence phải lớn hơn hoặc bằng 2.")
    if rails >= len(text):
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
    """Giải mã văn bản bằng Rail Fence cipher."""
    if not isinstance(rails, int):
        raise ValueError("'key' (số hàng rào) cho Rail Fence phải là một số nguyên.")
    if rails < 2:
        raise ValueError("Số hàng rào (key) cho Rail Fence phải lớn hơn hoặc bằng 2.")
    if rails >= len(cipher_text):
        return cipher_text

    text_len = len(cipher_text)
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

# --- 4. API Endpoints ---

# == Caesar API Endpoints ==
@app.route('/api/caesar/encrypt', methods=['POST'])
def api_caesar_encrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số nguyên) trong JSON body"}), 400
    text = data['text']
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({"error": "'key' cho Caesar phải là một số nguyên"}), 400
    if not isinstance(text, str): return jsonify({"error": "'text' phải là một chuỗi"}), 400
    try:
        return jsonify({"encrypted_text": caesar_encrypt(text, key)})
    except ValueError as e: return jsonify({"error": str(e)}), 400

@app.route('/api/caesar/decrypt', methods=['POST'])
def api_caesar_decrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số nguyên) trong JSON body"}), 400
    text = data['text']
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({"error": "'key' cho Caesar phải là một số nguyên"}), 400
    if not isinstance(text, str): return jsonify({"error": "'text' phải là một chuỗi"}), 400
    try:
        return jsonify({"decrypted_text": caesar_decrypt(text, key)})
    except ValueError as e: return jsonify({"error": str(e)}), 400

# == Vigenère API Endpoints ==
@app.route('/api/vigenere/encrypt', methods=['POST'])
def api_vigenere_encrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) trong JSON body"}), 400
    text, key_str = data['text'], data['key']
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    try:
        return jsonify({"encrypted_text": vigenere_encrypt(text, key_str)})
    except ValueError as e: return jsonify({"error": str(e)}), 400

@app.route('/api/vigenere/decrypt', methods=['POST'])
def api_vigenere_decrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) trong JSON body"}), 400
    text, key_str = data['text'], data['key']
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    try:
        return jsonify({"decrypted_text": vigenere_decrypt(text, key_str)})
    except ValueError as e: return jsonify({"error": str(e)}), 400

# == Rail Fence API Endpoints ==
@app.route('/api/railfence/encrypt', methods=['POST'])
def api_railfence_encrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số hàng rào) trong JSON body"}), 400
    
    text = data['text']
    try:
        rails = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({"error": "'key' (số hàng rào) cho Rail Fence phải là một số nguyên"}), 400
    if not isinstance(text, str):
        return jsonify({"error": "'text' phải là một chuỗi"}), 400
        
    try:
        encrypted_text = rail_fence_encrypt(text, rails)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/railfence/decrypt', methods=['POST'])
def api_railfence_decrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số hàng rào) trong JSON body"}), 400
    
    text = data['text']
    try:
        rails = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({"error": "'key' (số hàng rào) cho Rail Fence phải là một số nguyên"}), 400
    if not isinstance(text, str):
        return jsonify({"error": "'text' phải là một chuỗi"}), 400

    try:
        decrypted_text = rail_fence_decrypt(text, rails)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# --- 5. Routes cho Giao Diện HTML ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/caesar')
def caesar_page():
    return render_template('caesar.html')

@app.route('/vigenere')
def vigenere_page():
    return render_template('vigenere.html')

@app.route('/railfence')
def railfence_page():
    return render_template('railfence.html')

# --- Chạy ứng dụng ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)