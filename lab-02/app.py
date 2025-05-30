from flask import Flask, request, jsonify, render_template
from ciphers import caesar, vigenere, rail_fence, playfair, transposition

app = Flask(__name__)

# --- API Endpoints ---

# == Caesar API Endpoints ==
@app.route('/api/caesar/encrypt', methods=['POST'])
def api_caesar_encrypt():
    data = request.get_json()
    text = data.get('text')
    key_val = data.get('key')
    if text is None or key_val is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số nguyên) trong JSON body"}), 400
    try:
        key = int(key_val)
    except (ValueError, TypeError):
        return jsonify({"error": "'key' cho Caesar phải là một số nguyên"}), 400
    if not isinstance(text, str): 
        return jsonify({"error": "'text' phải là một chuỗi"}), 400
    try:
        encrypted_text = caesar.caesar_encrypt(text, key)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e: 
        return jsonify({"error": str(e)}), 400

@app.route('/api/caesar/decrypt', methods=['POST'])
def api_caesar_decrypt():
    data = request.get_json()
    text = data.get('text')
    key_val = data.get('key')
    if text is None or key_val is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số nguyên) trong JSON body"}), 400
    try:
        key = int(key_val)
    except (ValueError, TypeError):
        return jsonify({"error": "'key' cho Caesar phải là một số nguyên"}), 400
    if not isinstance(text, str): 
        return jsonify({"error": "'text' phải là một chuỗi"}), 400
    try:
        decrypted_text = caesar.caesar_decrypt(text, key)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e: 
        return jsonify({"error": str(e)}), 400

# == Vigenère API Endpoints ==
@app.route('/api/vigenere/encrypt', methods=['POST'])
def api_vigenere_encrypt():
    data = request.get_json()
    text = data.get('text')
    key_str = data.get('key')
    if text is None or key_str is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) trong JSON body"}), 400
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    try:
        encrypted_text = vigenere.vigenere_encrypt(text, key_str)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e: 
        return jsonify({"error": str(e)}), 400

@app.route('/api/vigenere/decrypt', methods=['POST'])
def api_vigenere_decrypt():
    data = request.get_json()
    text = data.get('text')
    key_str = data.get('key')
    if text is None or key_str is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) trong JSON body"}), 400
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    try:
        decrypted_text = vigenere.vigenere_decrypt(text, key_str)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e: 
        return jsonify({"error": str(e)}), 400

# == Rail Fence API Endpoints ==
@app.route('/api/railfence/encrypt', methods=['POST'])
def api_railfence_encrypt():
    data = request.get_json()
    text = data.get('text')
    key_val = data.get('key')
    if text is None or key_val is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số hàng rào) trong JSON body"}), 400
    try:
        rails = int(key_val)
    except (ValueError, TypeError):
        return jsonify({"error": "'key' (số hàng rào) cho Rail Fence phải là một số nguyên"}), 400
    if not isinstance(text, str):
        return jsonify({"error": "'text' phải là một chuỗi"}), 400
    try:
        encrypted_text = rail_fence.rail_fence_encrypt(text, rails)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/railfence/decrypt', methods=['POST'])
def api_railfence_decrypt():
    data = request.get_json()
    text = data.get('text')
    key_val = data.get('key')
    if text is None or key_val is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (số hàng rào) trong JSON body"}), 400
    try:
        rails = int(key_val)
    except (ValueError, TypeError):
        return jsonify({"error": "'key' (số hàng rào) cho Rail Fence phải là một số nguyên"}), 400
    if not isinstance(text, str):
        return jsonify({"error": "'text' phải là một chuỗi"}), 400
    try:
        decrypted_text = rail_fence.rail_fence_decrypt(text, rails)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# == Playfair API Endpoints ==
@app.route('/api/playfair/encrypt', methods=['POST'])
def api_playfair_encrypt():
    data = request.get_json()
    text = data.get('text')
    key_str = data.get('key')
    if text is None or key_str is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) cho Playfair"}), 400
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    try:
        encrypted_text = playfair.playfair_encrypt(text, key_str)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/playfair/decrypt', methods=['POST'])
def api_playfair_decrypt():
    data = request.get_json()
    text = data.get('text')
    key_str = data.get('key')
    if text is None or key_str is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) cho Playfair"}), 400
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    try:
        decrypted_text = playfair.playfair_decrypt(text, key_str)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
# == Transposition API Endpoints ==
@app.route('/api/transposition/encrypt', methods=['POST'])
def api_transposition_encrypt():
    data = request.get_json()
    text = data.get('text')
    key_str = data.get('key')
    if text is None or key_str is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) cho Transposition"}), 400
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    if not key_str:
        return jsonify({"error": "Khóa Transposition không được để trống"}), 400
    try:
        encrypted_text = transposition.transposition_encrypt(text, key_str)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/transposition/decrypt', methods=['POST'])
def api_transposition_decrypt():
    data = request.get_json()
    text = data.get('text')
    key_str = data.get('key')
    if text is None or key_str is None:
        return jsonify({"error": "Vui lòng cung cấp 'text' và 'key' (chuỗi) cho Transposition"}), 400
    if not isinstance(text, str) or not isinstance(key_str, str):
        return jsonify({"error": "'text' và 'key' phải là chuỗi"}), 400
    if not key_str:
        return jsonify({"error": "Khóa Transposition không được để trống"}), 400
    try:
        decrypted_text = transposition.transposition_decrypt(text, key_str)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# --- Routes cho Giao Diện HTML ---
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

@app.route('/playfair')
def playfair_page():
    return render_template('playfair.html')

@app.route('/transposition')
def transposition_page():
    return render_template('transposition.html')

# --- Chạy ứng dụng ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)