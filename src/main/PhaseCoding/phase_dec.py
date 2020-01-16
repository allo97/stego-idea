from scipy.io import wavfile
import numpy as np
from tqdm import tqdm



def decode(signal):
    print("Wykonuję dekodowanie fazowe...")

    samplerate, audio = wavfile.read(signal)

    # audio = (audio / 32768.0).astype(np.dtype(np.float32))

    if audio.dtype == "int16":
        audio = audio.astype(np.float32, order='C') / 32768.0
    elif audio.dtype == "float32":
        pass
    else:
        print("not supported audio type for WAV, try converting to PCM16 or float32")
        exit()

    N = 10
    L = int(len(audio) / N)
    if L % 2 != 0:
        L = L - 1

    # check if there is stereo signal and get the first channel
    shape_of_data = np.shape(audio)
    if len(shape_of_data) > 1:
        # get one channel
        text_from_phase = audio[:, 0]
    else:
        text_from_phase = audio



    # Phase angles of first segment
    segments = np.reshape(text_from_phase[0:(N * L)], (L, N), 'F')
    w = np.fft.fft(segments, axis=0)
    Phi = np.angle(w)

    # wyciągnij długość tekstu m ze środka pierwszego segmentu
    length = Phi[L // 2 - 32:L // 2, 0]

    text_length = []

    for count, ele in enumerate(length):
        if ele > 0:
            text_length.append(0)
        else:
            text_length.append(1)

    # Length of my message as integer
    m = 0
    for ele in text_length:
        m = (m << 1) | ele
    print(m)

    # Retrieving audio back from phases of first segments
    bit_length_of_message = 8 * m

    text_from_phase = np.zeros(bit_length_of_message, dtype=int)

    # wyciągnij kolejny bit tekstu z pierwszego segmentu i zamień na 0 lub 1
    for i in tqdm(range(bit_length_of_message)):
        if Phi[L//2 - 32 - bit_length_of_message + i, 0] > 0:
            text_from_phase[i] = 0
        else:
            text_from_phase[i] = 1

    # Converting to string
    my_string = fromBits(text_from_phase)
    return my_string


def fromBits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
