import soundfile as sf
import math
import numpy as np
import matplotlib.pyplot as plt


def encode(signal, text):
    print("Wykonuję kodowanie fazowe...")

    data, samplerate = sf.read(signal)

    song_name = signal.split("/")[-1]

    # get one channel
    new_data = data[:, 0]

    # amount of frames
    F = 50

    # Get length of each frame
    L = int(len(data) / F)
    if L % 2 != 0:
        L = L - 1

    I = len(new_data)

    # convert text to bit
    bitText = toBits(text)

    # Change length of text to bits -> max 32 bits
    length_bit_message = get_length(text)

    # Add length info to actual text
    bitText.extend(length_bit_message)

    # length of bit sequence to hide
    m = len(bitText)

    # number of frames
    N = int(np.floor(I / L))

    segments = np.reshape(new_data[0:(N * L)], (L, N), 'F')

    w = np.fft.fft(segments, axis=0)
    Phi = np.angle(w)
    A = np.abs(w)

    DeltaPhi = np.zeros((L, N))

    # Calculating phase differences of adjacent segments
    for i in range(1, N):
        DeltaPhi[:, i] = Phi[:, i] - Phi[:, i - 1]

    # Binary data is represented as {-pi / 2, pi / 2} and stored in PhiData
    PhiData = np.zeros(m)

    for count, ele in enumerate(bitText):
        if ele == 0:
            PhiData[count] = (math.pi / 2)
        else:
            PhiData[count] = (-math.pi / 2)

    # PhiData is written onto the middle of first phase matrix
    Phi_new = np.zeros((L, N))


    Phi_new[:, 0] = Phi[:, 0]
    t = np.arange(0, len(Phi_new), 1)

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

    Phi_new[L // 2 - m:L // 2, 0] = PhiData  # Hermitian symmetry
    Phi_new[L // 2 + 1:L // 2 + m + 1, 0] = -np.flip(PhiData)  # Hermitian symmetry


    # splt = plt.subplot(212)
    # plt.plot(t[2600:2800], Phi_new[2600:2800, 0], lw=1)
    # splt.set_title("Faza sygnału zmienionego")
    # splt.set_xlabel("Próbki")
    # splt.set_ylabel("Faza [rad]")
    # plt.show(fig)
    # plt.close(fig)

    # Re-creating phase matrixes using phase differences
    for i in range(1, N):
        Phi_new[:, i] = Phi_new[:, i - 1] + DeltaPhi[:, i]

    # Reconstructing the sound signal by applying the inverse FFT
    z = np.real(np.fft.ifft(A * np.exp(1j * Phi_new), axis=0))

    snew = np.reshape(z, N * L, 'F')
    out = np.append(snew, new_data[N * L: I])
    data[:, 0] = out

    x = signal.split(".")

    sf.write('../data/data_from_embedding/' + 'stego_' + song_name, data, samplerate)
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
