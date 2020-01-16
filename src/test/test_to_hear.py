import src.main.LSBalgorithm.LSB_algorithm as LSB
import src.test.GenerateRandomString.random_string as randomString
import src.main.PhaseCoding.phase_enc_charts as PhaseEncoding
import src.main.PhaseCoding.phase_dec_charts as PhaseDecoding
import time
import pickle
import random as rd
import difflib
import numpy as np


def checkDiff(data1, data2):
    for i in range(len(data1)):
        if abs(abs(data1[i]) - abs(data2[i])) > 0.3:
            print("phi_new: ", data1[i], "phi from decode: ", data2[i])


choose_song = "C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/coverAudio.wav"
choose_return_song = "C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_from_embedding/stego4_coverAudio.wav"



num_of_chars = 331
text = randomString.randomStringwithDigitsAndSymbols(num_of_chars)
print("Liczba znakow: ", num_of_chars)
print(PhaseEncoding.encode(choose_song, text))
new_text = PhaseDecoding.decode(choose_return_song)

output_list = [li for li in difflib.ndiff(text, new_text) if li[0] != ' ']

if output_list:
    print("there is an error!")
    print(output_list)
    print(len(output_list))











