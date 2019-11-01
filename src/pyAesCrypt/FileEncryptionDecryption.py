import pyAesCrypt
# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
password = "foopassword"
# encrypt
pyAesCrypt.encryptFile("coverAudio.wav", "coverAudio.wav.aes", password, bufferSize)
# decrypt
pyAesCrypt.decryptFile("coverAudio.wav.aes", "dataout.wav", password, bufferSize)