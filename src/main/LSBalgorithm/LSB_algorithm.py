# We will use wave package available in native Python installation to read and write .wav audio file
import wave
from tqdm import tqdm


def encode(signal, text):

    print("Wykonuję kodowanie metodą najmniej znaczącego bitu...")
    # read wave audio file
    audio = wave.open(signal, mode='rb')
    audio_name = signal.split("/")[-1]
    # Zapisz w wektorze n wartości sygnału audio
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    len_frame_bytes = len(frame_bytes)
    print("ilosc znakow mozliwych do osadzenia: ", int((len_frame_bytes / 8) / 1.33))


    # sprawdzenie czy plik jest za duży
    if len(text) * 8 > len_frame_bytes:
        answer = "Plik jest za duży! Usuń conajmniej " + str(abs(int((len_frame_bytes / 8 - len(text)) / 1.33))) + " znaków z pliku! \nSpróbuj jeszcze raz!"
        print(answer)
        exit()

    # dopisz ciąg znaków do tekstu aby wypełnić wektor audio
    dummy = "*&w1`"
    hashes = (int((len(frame_bytes) - (len(text) * 8)) / 8) - len(dummy)) * '#'
    hashes = dummy + hashes
    text = text + hashes
    # przekonwertuj tekst na n bitów
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in tqdm(text)])))
    # osadź bit tekstu w najmniej znaczaącym bicie w audio
    for i, bit in enumerate(tqdm(bits)):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)
    # Zapisz audio jako wav
    with wave.open('../data/data_from_embedding/' + 'stego_lsb_' + audio_name, 'wb') as fd:
        fd.setparams(audio.getparams())
        fd.writeframes(frame_modified)
    audio.close()

    return "Tekst zostal osadzony w: stego_" + audio_name


def decode(signal):

    print("Wykonuję dekodowanie metodą najmniej znaczącego bitu...")

    audio = wave.open(signal, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    # wyciągnij bit tekstu z najmniej znaczącego bitu w audio
    extracted = [frame_bytes[i] & 1 for i in tqdm(range(len(frame_bytes)))]
    # przekonwertuj n bitów na tekst
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in tqdm(range(0, len(extracted), 8)))
    # usuń dopisany ciąg znaków
    decoded = string.split("*&w1`")[0]
    audio.close()
    return decoded