from cryptography.fernet import Fernet

#file encryption

def encryptFile():
    file = open('key.key', 'wb')
    key = file.read() # The key is type bytes still
    file.close()

    input_file = 'test.txt'
    output_file = 'test.encrypted'

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

# You can delete input_file if you want


#file decryption

def decryptFile():
    key = b'' # Use one of the methods to get a key (it must be the same as used in encrypting)
    input_file = 'test.encrypted'
    output_file = 'test.txt'

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

# You can delete input_file if you want