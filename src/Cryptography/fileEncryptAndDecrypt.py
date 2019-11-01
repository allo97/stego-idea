from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#key generation

def generateKey(password):

    password_provided = password  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    salt1 = 'salt'.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
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

def encryptFile(input_file, password):
    #mozna zrobic tak ze szyfruje osobno nazwe pliku i osobno dane w pliku i potem sie to odszyfruje i z tego zrobi
    #nowy plik po wyciągnięciu

    #albo osadzic po prostu nazwe pliku + zaszyfrowana data

    key = generateKey(password)

    extension = os.path.splitext(input_file)[1]
    output_file = "../data/encrypted" + extension

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print("file is encrypted!")



# You can delete input_file if you want


#file decryption

def decryptFile(filename, password):

    key = generateKey(password)

    input_file = filename
    extension = os.path.splitext(input_file)[1]
    output_file = '../data/decrypted' + extension

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print("file is decrypted!!")

# You can delete input_file if you want