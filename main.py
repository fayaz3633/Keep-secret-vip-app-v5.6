import os
import base64
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

# 1. 2026 کے معیار کے مطابق مضبوط پن ویلیڈیشن (کم از کم 8 ہندسے اور سیکوینس چیک)
def is_valid_pin(pin: str) -> bool:
    # لمبائی کم از کم 8 ہندسے ہونی چاہیے
    if len(pin) < 8:
        return False

    # صرف ہندسے ہونے چاہئیں
    if not pin.isdigit():
        return False

    # یکساں ہندسوں والے پنز (جیسے 11111111، 00000000) کو بلاک کرنا
    if pin == pin[0] * len(pin):
        return False

    # ترتیب وار پنز (جیسے 12345678) کو بلاک کرنے کا اضافی چیک
    sequential = "01234567890123456789"
    if pin in sequential:
        return False

    return True

# 2. PBKDF2 کے ذریعے 300,000 اٹریشنز کے ساتھ کی (Key) جنریشن
def generate_key_from_pin(pin: str, salt: bytes) -> bytes:
    return PBKDF2(pin.encode(), salt, dkLen=32, count=300000, hmac_hash_module=SHA256)

# 3. بائٹس بیسڈ AES-GCM انکرپشن (ٹیکسٹ، امیج، ویڈیو، سب کے لیے یکساں)
def encrypt_bytes_to_json(data_bytes: bytes, pin: str) -> str:
    if not is_valid_pin(pin):
        return "ERROR_WEAK_PIN"
        
    salt = get_random_bytes(16)
    key = generate_key_from_pin(pin, salt)
    
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data_bytes)
    
    # ڈیٹا بیس یا فائل میں محفوظ کرنے کے لیے JSON تیار کرنا
    data_dict = {
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'salt': base64.b64encode(salt).decode('utf-8'),
        'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }
    return json.dumps(data_dict)

# 4. بائٹس بیسڈ ڈیکرپشن (واپس اصل فائل یا ٹیکسٹ بائٹس حاصل کرنا)
def decrypt_bytes_from_json(json_string: str, pin: str) -> bytes:
    try:
        data_dict = json.loads(json_string)
        
        salt = base64.b64decode(data_dict['salt'])
        nonce = base64.b64decode(data_dict['nonce'])
        tag = base64.b64decode(data_dict['tag'])
        ciphertext = base64.b64decode(data_dict['ciphertext'])
        
        key = generate_key_from_pin(pin, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        # ڈیکرپشن اور آتھنٹیکیشن ایک ساتھ
        return cipher.decrypt_and_verify(ciphertext, tag)
    except (ValueError, KeyError, json.JSONDecodeError):
        # اگر پن غلط ہو یا فائل خراب ہو چکی ہو
        return b"ERROR_INVALID_PIN_OR_CORRUPT_DATA"
      
