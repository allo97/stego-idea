import os

import pyAesCrypt
from os import stat, remove
# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
#password = "foopassword"

def encrypt(password):
    # encrypt
    with open("data.txt", "rb") as fIn:
        encrypted = "encrypted" + os.path.splitext(fIn.name)[1]
        with open(encrypted, "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)

    # get encrypted file size
    encFileSize = stat("data.txt.aes").st_size
    print(encFileSize)

def decrypt(password, encFileSize):
    # decrypt
    with open("test.encrypted", "rb") as fIn:
        try:
            with open("dataout.txt", "wb") as fOut:
                # decrypt file stream
                pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
        except ValueError:
            # remove output file on error
            remove("dataout.txt")
