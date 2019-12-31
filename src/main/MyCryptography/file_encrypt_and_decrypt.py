from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#key generation


def generate_key(password):

    password_provided = password  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    salt1 = 'salt'.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt1,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    file = open('key.key', 'wb')
    file.write(key)  # The key is type bytes still
    file.close()
    print("generated key!!")
    return key


#file encryption

def encrypt_file(input_file, password):

    key = generate_key(password)

    output_file = "test.encrypted"

    with open(input_file, 'rb') as f:
        data = f.read()
    print(len(data))

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    print(len(encrypted))

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print("file is encrypted!")
    return encrypted.decode('utf8')


#file decryption

def decrypt_file(msg, password):

    key = generate_key(password)

    output_file = '../data/hidden_message/secret.decrypted'

    fernet = Fernet(key)

    try:
        encrypted = fernet.decrypt(msg.encode('utf8'))
    except (InvalidSignature, InvalidToken):
        return "Niewlasciwe haslo lub algorytm albo plik!\nSprawdz jeszcze raz!\nZamykam program"
    except:
        return "Nieoczekiwany blad"

    with open(output_file, 'wb') as f:
        f.write(encrypted)

    return "Odzyskana wiadomosc: " + output_file.split("/")[-1]
