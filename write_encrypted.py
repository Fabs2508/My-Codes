import hashlib
import hmac
import base64
import os
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

def derive_key(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)

def xor_encrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

try:
    password = input("Passwort eingeben: ")
    text = input("Text zum Verschluesseln (max. 24 Zeichen): ")
    if len(text) > 24:
        print("Text zu lang!")
        exit()

    salt = os.urandom(8)  # 8 Byte zufaelliges Salt
    key = derive_key(password, salt)
    
    data_bytes = text.encode("utf-8")
    encrypted = xor_encrypt(data_bytes, key)
    
    # HMAC berechnen
    mac = hmac.new(key, encrypted, hashlib.sha256).digest()

    full = salt + mac[:8] + encrypted  # Salt + HMAC (8 Byte) + Encrypted
    encoded = base64.b64encode(full).decode()

    print("Bitte Karte auflegen...")
    reader.write(encoded)
    print("Text sicher geschrieben.")
except Exception as e:
    print("Fehler beim Schreiben:", e)
finally:
    GPIO.cleanup()
