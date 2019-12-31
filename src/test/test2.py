import math
import statistics

import src.main.LSBalgorithm.LSB_algorithm as LSB
import src.test.GenerateRandomString.random_string as randomString
import random as rd
import src.main.MyCryptography.file_encrypt_and_decrypt as encryption
import difflib

vecor = []

for i in range(50):
    my_rand = rd.randint(1,1000)
    text = randomString.randomStringwithDigitsAndSymbols(my_rand)
    with open("randomText.txt", 'w') as rando:
        rando.write(text)
    print(text)
    print("Licznik: ", i)
    encrypted = encryption.encrypt_file("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/test/randomText.txt", "alek")
    print(encrypted)
    print(len(text))
    print("Dlugosc Zaszyfrowana liczba", len(encrypted))

    vecor.append(len(encrypted) / len(text))
    print("wynik z dzielenia", vecor[i])

print(vecor)
# my_mean = statistics.mean(vecor)
# print(statistics.mean(vecor))
# print(my_rand * my_mean)
# print(max(vecor))
    # print(LSB.encode("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/coverAudio.wav", encrypted))
    # new_text = LSB.decode("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_from_embedding/stego_coverAudio.wav")

    # if text == new_text:
    #     print("true")
    # else:
    #     print("false")
    #     print(text)
    #     print(new_text)
    #     d = difflib.Differ()
    #     diff = d.compare(text, new_text)
    #     print(diff)
    #     break

    # output_list = [li for li in difflib.ndiff(text, new_text) if li[0] != ' ']
    #
    #
    # if output_list:
    #     print(output_list)
    #     print(text)
    #     print(new_text)
    #     break




    # if text == new_text:
    #     continue
    # else:
    #     print("false")
    #     print(text)
    #     print(new_text)
    #     break

