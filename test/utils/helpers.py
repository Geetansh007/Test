import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from werkzeug.utils import secure_filename
from ..config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def encrypt_data(data):
    cipher = AES.new(Config.AES_KEY, AES.MODE_CBC, Config.AES_IV)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.urlsafe_b64encode(ct_bytes).decode('utf-8')

def decrypt_data(encrypted_data):
    ct = base64.urlsafe_b64decode(encrypted_data)
    cipher = AES.new(Config.AES_KEY, AES.MODE_CBC, Config.AES_IV)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

def secure_filename_wrapper(filename):
    return secure_filename(filename)