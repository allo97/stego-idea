from cryptography.fernet import Fernet
message = "my deep dark secret".encode()

file = open('key.key', 'rb')
key = file.read() # The key will be type bytes
file.close()

f = Fernet(key)
encrypted = f.encrypt(message)