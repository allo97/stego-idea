import numpy as np
from scipy.io import wavfile
from tqdm import tqdm

import matplotlib.pyplot as plt


def encode(signal, text):
    print("Wykonuję kodowanie fazowe...")

    samplerate, audio = wavfile.read(signal)

    # wczytaj sygnał jako float
    if audio.dtype == "int16":
        audio = audio.astype(np.float32, order='C') / 32768.0
    elif audio.dtype == "float32":
        pass
    else:
        print("nie wspierany format pliku WAV, spróbuj przekonwertować do PCM16 lub float32")
        exit()

    song_name = signal.split("/")[-1]

    # podziel sygnał na N segmentów o długości L (musi byc parzyste)
    N = 10
    L = int(len(audio) / N)
    if L % 2 != 0:
        L = L - 1

    # sprawdź czy sygnał jest stereo
    shape_of_data = np.shape(audio)
    is_stereo = True
    if len(shape_of_data) > 1:
        # pobierz pierwszy kanał
        new_data = audio[:, 0]
    else:
        new_data = audio
        is_stereo = False


    # przekonwertuj tekst wraz new_audio jego długością na n bitów
    bitText = toBits(text)
    # pobierz długość tekstu
    length_bit_message = get_length(text)
    # dodaj długość tekstu do zaszyfrowanej wiadomości
    bitText.extend(length_bit_message)

    # length of bit sequence to hide
    m = len(bitText)

    # sprawdź czy plik jest za duży
    print("ilosc znakow do osadzenia ", int((L/2)/8))
    if L / 2 < m:
        answer = "Plik jest za duży! Usuń conajmniej " + str(
            int(((m - ((L / 2) - (L / 2) % 8))/8) / 1.33)) + " znaków new_audio pliku! \nSpróbuj jeszcze raz!"
        print(answer)
        exit()

    # odziel sygnał na N segmentów o długości L
    segments = np.reshape(new_data[0:(N * L)], (L, N), 'F')

    # oblicz fazę segmentów new_audio Transformaty Fouriera
    w = np.fft.fft(segments, axis=1)
    Phi = np.angle(w)
    A = np.abs(w)

    DeltaPhi = np.zeros((L, N))

    # oblicz różnicę faz pomiędzy kolejnymi segmentami
    for i in tqdm(range(1, N)):
        DeltaPhi[:, i] = Phi[:, i] - Phi[:, i - 1]

    # Binary audio is represented as {-pi / 2, pi / 2} and stored in PhiData
    PhiData = np.zeros(m)

    # zamień bity tekstu na wartości fazy
    for count, ele in enumerate(tqdm(bitText)):
        if ele == 0:
            PhiData[count] = (np.pi / 2)
        else:
            PhiData[count] = (-np.pi / 2)

    # PhiData is written onto the middle of first phase matrix
    Phi_new = np.zeros((L, N))
    Phi_new[:, 0] = Phi[:, 0]

    # Rysujemy dla fazy
    # t = np.arange(0, len(Phi_new), 1)

    # SMALL_SIZE = 14
    # MEDIUM_SIZE = 12
    #
    # plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    # plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels

    # fig = plt.figure(1)
    # splt = plt.subplot(211)
    # plt.plot(t[2600:2800], Phi_new[2600:2800,0], lw=1)
    # splt.set_title("Faza sygnału początkowego")
    # splt.set_xlabel("Próbki")
    # splt.set_ylabel("Faza [rad]")

    # osadź wartości fazy w pierwszym segmencie
    Phi_new[L // 2 - m:L // 2, 0] = PhiData
    Phi_new[L // 2 + 1:L // 2 + m + 1, 0] = -np.flip(PhiData)

    # splt = plt.subplot(212)
    # plt.plot(t[2600:2800], Phi_new[2600:2800, 0], lw=1)
    # splt.set_title("Faza sygnału zmienionego")
    # splt.set_xlabel("Próbki")
    # splt.set_ylabel("Faza [rad]")
    # plt.show(fig)
    # plt.close(fig)

    # Uzupełnij pozostałą fazę sygnału
    for i in tqdm(range(1, N)):
        Phi_new[:, i] = Phi_new[:, i - 1] + DeltaPhi[:, i]

    # Zrekonstruuj sygnał poprzez odwrotną Transformatę Fouriera
    new_audio = np.real(np.fft.ifft(A * np.exp(1j * Phi_new), axis=0))

    snew = np.reshape(new_audio, N * L, 'F')
    out = np.append(snew, new_data[N * L: len(audio)])

    # TODO: Check fft if there is the same error as in decoding phase ->20???

    if is_stereo:
        audio[:, 0] = out
    else:
        audio = out

    audio = (audio * 32768.0).astype(np.int16, order='C')


    x = signal.split(".")

    wavfile.write('../data/data_from_embedding/' + 'stego_' + song_name, samplerate, audio)
    return "Tekst zostal osadzony w: stego_ " + song_name


def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def checkEqual(data, out):
    for i in range(len(out)):
        if data[i, 0] != out[i]:
            return "nie sa rowne, ale powinny byc"
        else:
            return "sa rowne"

def get_length(text):
    list_of_bits = [int(x) for x in list('{0:032b}'.format(len(text)))]
    return list_of_bits
