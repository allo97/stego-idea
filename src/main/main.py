from tkinter import filedialog
import src.main.LSBalgorithm.LSB_algorithm as LSB
import src.main.MyCryptography.file_encrypt_and_decrypt as Crypting
import src.main.PhaseCoding.phase_enc as PhaseEncoding
import src.main.PhaseCoding.phase_dec as PhaseDecoding


def execute_encoding_algorithm(algorithm, audio_path, encrypted_text):
    switcher = {
        1: lambda: LSB.encode(audio_path, encrypted_text),
        2: lambda: PhaseEncoding.encode(audio_path, encrypted_text),
        3: lambda: "SpreadSpectrum()",
    }

    func = switcher.get(algorithm, lambda: "Zla wartosc!")
    return func()


def execute_decoding_algorithm(algorithm, audio_path):
    switcher = {
        1: lambda: LSB.decode(audio_path),
        2: lambda: PhaseDecoding.decode(audio_path),
        3: lambda: "SpreadSpectrum()",
    }

    func = switcher.get(algorithm, lambda: "Zla wartosc!")
    return func()


print("Witaj w programie MyStego!")
print("Co chcesz zrobić?")
print("1 - kodowanie")
print("2 - dekodowanie")

choice = int(input())


if choice == 1:
    print("KODOWANIE")
    print("Wybierz plik do osadzenia: ", end=" ")

    file_path = filedialog.askopenfilename(initialdir = "./data/data_to_embedding")
    print(file_path.split("/")[-1])

    print("Wybierz plik audio w formacie wav z ktorego chcesz tekst: ", end=" ")
    audio_path = filedialog.askopenfilename(initialdir = "./data/data_to_embedding")
    print(audio_path.split("/")[-1])

    print("Wybierz algorytm do zakodowania: ")
    print("1 - Metoda najmniej znaczacego bitu")
    print("2 - Kodowanie fazowe")
    print("3 - Metoda rozproszonego widma")

    algorithm = int(input())

    print("Podaj haslo potrzebne do odkodowania: ")

    password = input()

    # tutaj szyfrowanie
    encrypted_text = Crypting.encrypt_file(file_path, password)


    print(execute_encoding_algorithm(algorithm, audio_path, encrypted_text))


elif choice == 2:
    print("DEKODOWANIE")

    print("Wybierz plik audio w formacie wav ktory zawiera ukryta wiadomosc: ", end=" ")
    audio_path = filedialog.askopenfilename(initialdir="./data/data_from_embedding")
    print(audio_path.split("/")[-1])

    print("Wybierz ten sam algorytm do odkodowania: ")
    print("1 - Metoda najmniej znaczacego bitu")
    print("2 - Kodowanie fazowe")
    print("3 - Metoda rozproszonego widma")

    algorithm = int(input())

    print("Podaj haslo: ")

    password = input()

    extracted_data = execute_decoding_algorithm(algorithm, audio_path)

    print(Crypting.decrypt_file(extracted_data, password))

else:
    print("Zla wartosc, zamykam!")

