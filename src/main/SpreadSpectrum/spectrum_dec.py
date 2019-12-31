import soundfile as sf
import numpy as np


def spectrum_dec(signal, text):

    data, samplerate = sf.read(signal)

    L = int(np.floor(len(data)/(len(text) * 8)))
    nframe = np.floor(len(data) / L)
    N = int(nframe - np.mod(nframe, 8))

    xsig = np.reshape(data[0:N*L,0], (L, N), 'F')

    # Generate pseudo random sequence
    r = rand_gen(L)

    new_data = np.zeros(N, dtype=int)
    c = np.zeros(N)

    for k in range(N):
        # Correlation
        c[k] = np.sum(xsig[:, k] * r) / L
        if c[k] < 0:
            new_data[k] = 0
        else:
            new_data[k] = 1

    my_string = fromBits(new_data)
    print("Here is your hidden message \n" + my_string + "\n!!!!!!!!")


    ffefe = " efefefefe"

    return my_string



def fromBits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def binarize(xs, digits):
    return np.array([digits[0] if x <= 0 else digits[1] for x in xs])

def rand_gen(L):
    np.random.seed(1)
    white_noise = np.random.normal(0, 1, L)
    white_noise_binarized = binarize(white_noise, [-1, 1])
    return white_noise_binarized