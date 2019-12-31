import soundfile as sf
import numpy as np


def decode(signal):
    print("Wykonuję kodowanie fazowe...")

    data, samplerate = sf.read(signal)

    F = 50
    L = int(len(data) / F)
    if L % 2 != 0:
        L = L - 1

    # First segment
    x = data[:L, 0]

    # Phase angles of first segment
    Phi = np.angle(np.fft.fft(x, axis=0))

    # Retrieving length back
    # First 32 bits are the length of the message, the rest of it is the message
    length = Phi[L // 2 - 32:L // 2]

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

    # Retrieving data back from phases of first segments
    m = 8 * length_of_message
    #new_data = [chr(x) for x in np.zeros(m, dtype=int)]
    new_data = np.zeros(m, dtype=int)

    for i in range(m):
        if Phi[L//2 - 32 - m + i] > 0:
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
