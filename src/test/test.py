import src.main.LSBalgorithm.LSB_algorithm as LSB
import src.test.GenerateRandomString.random_string as randomString
import src.main.PhaseCoding.phase_enc as PhaseEncoding
import src.main.PhaseCoding.phase_dec as PhaseDecoding

import random as rd
import difflib


def checkDiff(data1, data2):
    for i in range(len(data1)):
        if abs(abs(data1[i]) - abs(data2[i])) > 0.3:
            print("phi_new: "  ,data1[i], "phi from decode: ", data2[i])

for i in range(1000):
    my_rand = rd.randint(10, 20)
    text = randomString.randomStringwithDigitsAndSymbols(my_rand)
    print(my_rand)
    print("Licznik: ", i)
    print("Losowa liczba: ", my_rand)

    print(PhaseEncoding.encode("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/coverAudio.wav", text))
    new_text = PhaseDecoding.decode("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_from_embedding/stego_coverAudio.wav")

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

    # print(checkDiff(phi_new, Phi))
    output_list = [li for li in difflib.ndiff(text, new_text) if li[0] != ' ']


    if output_list:
        print(output_list)
        print(text)
        print(new_text)
        break




    # if text == new_text:
    #     continue
    # else:
    #     print("false")
    #     print(text)
    #     print(new_text)
    #     break

