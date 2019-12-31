import soundfile as sf
import numpy as np



def spectrum_dec_sin_wave(signal):

    data, samplerate = sf.read(signal)

    modulation_freq = 1000
    modulation_period = 1 / modulation_freq
    oscillations_per_chip = 5
    chip_period = oscillations_per_chip * modulation_period # tc
    chip_freq = 1 / chip_period
    t_start = 0
    phase = np.pi / 2
    probes_per_period = samplerate / chip_freq

    # Creating carrier wave with modulation frequency
    t = np.arange(0, (len(data)) / samplerate, 1 / samplerate)
    tc = t / oscillations_per_chip
    # # carrier = np.sin(2 * np.pi * modulation_freq * t + phase)
    #
    d = []
    for i in range(len(tc)):
        my_data = data[i, 0]
        my_sin = np.sin(2 * np.pi * modulation_freq * tc[i])
        diff = tc[1] - tc[0]
        xd = data[:, 0] * np.sin(2 * np.pi * modulation_freq * tc[i]) * (tc[1] - tc[0])
        d.append(xd)
        wait = "Fefefeffe"



    why = "fefef"
    ffefe = " efefefefe"





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