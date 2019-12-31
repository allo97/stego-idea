import src.main.LSBalgorithm.LSB_algorithm as LSB
import src.test.GenerateRandomString.random_string as randomString
import random as rd
import difflib


for i in range(10):
    my_rand = rd.randint(130000, 132000)
    text = randomString.randomStringwithDigitsAndSymbols(my_rand)
    print(text)
    print("Licznik: ", i)
    print("Losowa liczba: ", my_rand)

    print(LSB.encode("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/coverAudio.wav", text))
    new_text = LSB.decode("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_from_embedding/stego_coverAudio.wav")

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

