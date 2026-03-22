import os
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# Folders
UPLOAD_FOLDER = 'static/original'
ENCRYPTED_FOLDER = 'static/encrypted'
DECRYPTED_FOLDER = 'static/decrypted'

# Create folders if they don't exist
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Configuration
app.config.update({
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'ENCRYPTED_FOLDER': ENCRYPTED_FOLDER,
    'DECRYPTED_FOLDER': DECRYPTED_FOLDER,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16 MB
})

# --------------------------
# AES Encryption / Decryption
# --------------------------

def encrypt_image(image_path, key):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    encrypted_data = cipher.iv + cipher.encrypt(pad(image_data, AES.block_size))
    
    encrypted_filename = os.path.basename(image_path) + '.enc'
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, encrypted_filename)

    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_data)
    
    return encrypted_filename

def decrypt_image(encrypted_filename, key):
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, encrypted_filename)
    
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
    
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    
    try:
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    except ValueError:
        return None  # Incorrect key
    
    decrypted_filename = encrypted_filename.replace('.enc', '')
    decrypted_path = os.path.join(DECRYPTED_FOLDER, decrypted_filename)

    with open(decrypted_path, 'wb') as f:
        f.write(decrypted_data)
    
    return decrypted_filename

# --------------------------
# Routes
# --------------------------

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')  # Add login logic if needed

@app.route('/index', methods=['GET', 'POST'])
def index():
    original_images = os.listdir(UPLOAD_FOLDER)
    encrypted_images = os.listdir(ENCRYPTED_FOLDER)
    decrypted_images = os.listdir(DECRYPTED_FOLDER)
    return render_template('index.html', originals=original_images, encrypted=encrypted_images, decrypted=decrypted_images)

@app.route('/upload-and-encrypt', methods=['POST'])
def upload_and_encrypt():
    file = request.files.get('image')
    secret_key = request.form.get('key')

    if not file or file.filename == '' or not secret_key or len(secret_key) != 16:
        flash("Invalid file or key! The key must be exactly 16 characters.", "danger")
        return redirect(url_for('index'))
    
    original_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(original_path)

    encrypted_filename = encrypt_image(original_path, secret_key)
    flash(f"File '{file.filename}' encrypted successfully!", "success")
    
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    filename = request.form.get('filename')
    secret_key = request.form.get('key')
    
    if not filename or not secret_key or len(secret_key) != 16:
        flash("Invalid filename or key!", "danger")
        return redirect(url_for('index'))
    
    decrypted_filename = decrypt_image(filename, secret_key)
    
    if decrypted_filename is None:
        flash("Decryption failed! Incorrect key.", "danger")
    else:
        flash(f"File '{decrypted_filename}' decrypted successfully!", "success")
    
    return redirect(url_for('index'))

@app.route('/view-image/<folder>/<filename>')
def view_image(folder, filename):
    return send_from_directory(os.path.join('static', folder), filename)

# --------------------------
# Run the App
# --------------------------

if __name__ == '__main__':
    app.run(debug=True)
