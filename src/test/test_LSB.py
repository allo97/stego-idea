import src.main.LSBalgorithm.LSB_algorithm as LSB
import src.test.GenerateRandomString.random_string as randomString
import src.main.PhaseCoding.phase_enc as PhaseEncoding
import src.main.PhaseCoding.phase_dec as PhaseDecoding
import time
import pickle
import random as rd
import difflib
import numpy as np


def checkDiff(data1, data2):
    for i in range(len(data1)):
        if abs(abs(data1[i]) - abs(data2[i])) > 0.3:
            print("phi_new: ", data1[i], "phi from decode: ", data2[i])


save_data = ['lsb_2.pkl']
choose_song = ["C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/Radioactive.wav"]
choose_return_song = ["C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_from_embedding/stego_Radioactive.wav"]


char_counts = [200]

for a in range(len(save_data)):
    my_time = []
    errors = 0
    char_of_error = []

    for j in range(len(char_counts)):

        for i in range(10):

            num_of_chars = char_counts[j]
            text = randomString.randomStringwithDigitsAndSymbols(num_of_chars)
            print("Licznik: ", i)
            print("Liczba znakow: ", num_of_chars)
            start_time = time.time()
            print(LSB.encode(choose_song[a], text))
            new_text = LSB.decode(choose_return_song[a])
            elapsed_time = time.time() - start_time
            my_time.append(elapsed_time)

            # 1. Czas
            # 2. Ilość błędów
            # 3. Ilosc blednych znaków
            # 4. ilosc znaków z zależnosci od pliku mozliwych do osadzenia


            output_list = [li for li in difflib.ndiff(text, new_text) if li[0] != ' ']

            if output_list:
                errors += 1
                char_of_error.append(len(output_list))

            xdd = "fefefe"

    # Saving the objects:
    with open(save_data[a], 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([my_time, errors, char_of_error], f)
    do_something = "fefefefe"








