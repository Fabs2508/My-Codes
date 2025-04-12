import hashlib
import hmac
import base64
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

def derive_key(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)

def xor_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

try:
    password = input("Passwort eingeben: ")

    print("Bitte Karte auflegen...")
    id, raw = reader.read()
    decoded = base64.b64decode(raw.strip())

    salt = decoded[:8]
    mac_received = decoded[8:16]
    encrypted = decoded[16:]

    key = derive_key(password, salt)

    # HMAC pruefen
    mac_expected = hmac.new(key, encrypted, hashlib.sha256).digest()[:8]
    if mac_received != mac_expected:
        print("Manipulation erkannt oder falsches Passwort!")
    else:
        decrypted = xor_decrypt(encrypted, key)
        print("Karten-ID:", id)
        print("Entschluesselter Text:", decrypted.decode())
except Exception as e:
    print("Fehler beim Entschluesseln:", e)
finally:
    GPIO.cleanup()
