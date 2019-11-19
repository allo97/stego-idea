from src.Cryptography.fileEncryptAndDecrypt import encryptFile, decryptFile
from src.PhaseCoding.phase_enc import phase_enc
from src.PhaseCoding.phase_dec import phase_dec
from src.SpreadSpectrum.spectrum_enc import spectrum_enc
from src.SpreadSpectrum.spectrum_dec import spectrum_dec

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

file_path = "C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/coverAudio.wav"
file_path_out = "../data/coverAudio_stego.wav"
carrier_wave = 1
# Phase Coding
#
#
#
# phase_enc(file_path, text)
#
# phase_dec(file_path_out)



# Spread Spectrum
#
#
#
spectrum_enc(file_path, text, carrier_wave)
spectrum_dec(file_path_out)