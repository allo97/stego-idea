import soundfile as sf
from scipy.io import wavfile
import numpy as np



def decode(signal):
    print("Wykonuję dekodowanie fazowe...")

    samplerate, data = wavfile.read(signal)

    N = 10
    L = int(len(data) / N)
    if L % 2 != 0:
        L = L - 1

    # check if there is stereo signal and get the first channel
    shape_of_data = np.shape(data)
    if len(shape_of_data) > 1:
        # get one channel
        new_data = data[:, 0]
    else:
        new_data = data



    # Phase angles of first segment
    segments = np.reshape(new_data[0:(N * L)], (L, N), 'F')
    w = np.fft.fft(segments, axis=0)
    Phi = np.angle(w)

    # Retrieving length back
    # First 32 bits are the length of the message, the rest of it is the message
    length = Phi[L // 2 - 32:L // 2, 0]

    text_length = []

    for count, ele in enumerate(length):
        if ele > 0:
            text_length.append(0)
        else:
            text_length.append(1)

    # Length of my message as integer
    length_of_message = 0
    for ele in text_length:
        length_of_message = (length_of_message << 1) | ele
    print(length_of_message)

    # Retrieving data back from phases of first segments
    m = 8 * length_of_message

    new_data = np.zeros(m, dtype=int)

    for i in range(m):
        if Phi[L//2 - 32 - m + i, 0] > 0:
            new_data[i] = 0
        else:
            new_data[i] = 1

    # Converting to string
    my_string = fromBits(new_data)
    return my_string


def fromBits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
