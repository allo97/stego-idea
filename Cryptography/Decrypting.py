from cryptography.fernet import Fernet
encrypted = b"...encrypted bytes..."

file = open('key.key', 'rb')
key = file.read() # The key will be type bytes
file.close()

f = Fernet(key)
decrypted = f.decrypt(encrypted)