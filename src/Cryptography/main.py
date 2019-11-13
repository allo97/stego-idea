from src.Cryptography.fileEncryptAndDecrypt import encryptFile, decryptFile
from src.PhaseCoding.phase_enc import phase_enc
from src.PhaseCoding.phase_dec import phase_dec
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


######
# Mam szyfrowanie i deszyfrowanie

# encryptFile("../data/test.xml", "alek")
#
# decryptFile("../data/encrypted.xml", "alek")

# file_path = filedialog.askopenfilename(initialdir = "C:/Users/aslod/Documents/Ważne foldery\STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data")

file = open("../data/tekst.txt", "r+")
text = file.read()

# Phase Coding
#
#
#
file_path = "C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/coverAudio.wav"
phase_enc(file_path, text)

file_path = "../data/coverAudio_stego.wav"
phase_dec(file_path)



# Spread Spectrum
#
#
#
