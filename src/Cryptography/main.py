from src.Cryptography.fileEncryptAndDecrypt import encryptFile, decryptFile
from src.PhaseCoding.phase_enc import phase_enc

######
# Mam szyfrowanie i deszyfrowanie

encryptFile("../data/test.xml", "alek")

decryptFile("../data/encrypted.xml", "alek")

phase_enc("..\data\coverAudio.wav", "a l", 1024)