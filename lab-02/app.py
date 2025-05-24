from flask import Flask, request, jsonify, render_template # Thêm render_template

app = Flask(__name__)

# --- 1. Logic Mã Hóa Caesar ---
def caesar_encrypt(text, key_int):
    """Mã hóa văn bản bằng Caesar cipher."""
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
    """Giải mã văn bản bằng Caesar cipher."""
    if not isinstance(key_int, int):
        raise ValueError("'key' cho Caesar phải là một số nguyên")
    return caesar_encrypt(text, -key_int)

# --- 2. Logic Mã Hóa Vigenère ---
def vigenere_process_key(key_string):
    """Chuẩn bị key cho Vigenere: chỉ lấy chữ cái, viết hoa."""
    processed_key = "".join(filter(str.isalpha, key_string)).upper()
    if not processed_key:
        raise ValueError("Key cho Vigenère phải chứa ít nhất một chữ cái.")
    return processed_key

def vigenere_crypt(text, key_string, encrypt=True):
    """Mã hóa hoặc giải mã văn bản bằng Vigenère cipher."""
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
    """Mã hóa văn bản bằng Vigenère cipher."""
    return vigenere_crypt(text, key_string, encrypt=True)

def vigenere_decrypt(text, key_string):
    """Giải mã văn bản bằng Vigenère cipher."""
    return vigenere_crypt(text, key_string, encrypt=False)

# --- 3. API Endpoints ---

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
    if not isinstance(text, str):
        return jsonify({"error": "'text' phải là một chuỗi"}), 400

    try:
        encrypted_text = caesar_encrypt(text, key)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

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
    if not isinstance(text, str):
        return jsonify({"error": "'text' phải là một chuỗi"}), 400
        
    try:
        decrypted_text = caesar_decrypt(text, key)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# == Vigenère API Endpoints ==
@app.route('/api/vigenere/encrypt', methods=['POST'])
def api_vigenere_encrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) trong JSON body"}), 400

    text = data['text']
    key = data['key'] 
    
    if not isinstance(text, str) or not isinstance(key, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400

    try:
        encrypted_text = vigenere_encrypt(text, key)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/vigenere/decrypt', methods=['POST'])
def api_vigenere_decrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) trong JSON body"}), 400

    text = data['text']
    key = data['key']

    if not isinstance(text, str) or not isinstance(key, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
        
    try:
        decrypted_text = vigenere_decrypt(text, key)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# --- 4. Routes cho Giao Diện HTML ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/caesar')
def caesar_page():
    return render_template('caesar.html')

@app.route('/vigenere')
def vigenere_page():
    return render_template('vigenere.html')

# --- Chạy ứng dụng ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)