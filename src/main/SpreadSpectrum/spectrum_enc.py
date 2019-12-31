import soundfile as sf
import numpy as np
from src.main.SpreadSpectrum import mixer
from src.main.PhaseCoding.phase_enc import get_length

def spectrum_enc(signal, text, carrier_wave):

    data, samplerate = sf.read(signal)

    # Minimum value length for each segment

    #Changing text to bit and I have list of ints
    bitText = toBits(text)

    # Change length of text to bits -> max 32 bits
    length_bit_message = get_length(text)

    # Add length info to actual text
    # bitText.extend(length_bit_message)

    # Length of segments
    L = int(np.floor(len(data)/len(bitText)))

    #Number of segments (for 8 bits)
    nframe = np.floor(len(data) / L)

    # mod to ensure that number of segments is divisor of 8
    N = int(nframe - np.mod(nframe, 8))

    # if len(bitText) > N:  # this condition is true only when L2 < L_min
    #     print("Message is too long, is being cropped")
    #     bitText = bitText[1:N]
    # else:
    #     bitText.extend(np.zeros(N - len(bitText), dtype=str))

    # Generate pseudorandom noise sequence
    r = rand_gen(L)
    pr = np.reshape(np.ones((N, 1)) * r, (N * L, 1))
    pr = np.squeeze(pr)
    alpha = 0.005


    # Embedding message
    result = mixer.mixer(L, bitText, -1, 1, carrier_wave, samplerate)
    smoothed_text = result[0]
    normal_signal = result[1]

    out = data
    # Simple adding pseudo numbers and smoothed_text into our data
    # Now for only one channel
    # OUTPUT = MESSAGE * PRN * CARRIER
    check = np.reshape(alpha * smoothed_text * np.transpose(pr), (N*L, 1))
    stego = data[0:N*L, 0] + np.array(alpha * smoothed_text * np.transpose(pr))
    check_stego = np.reshape(stego, (len(stego), 1))

    # Adding stego signal to the rest of the original signal
    out[0:N*L, 0] = stego

    x = signal.split(".")

    sf.write(x[0] + '_stego.wav', out, samplerate)
    print("Stego signal saved in " + x[0] + "_stego.wav !")


def rand_gen(L):
    np.random.seed(1)
    white_noise = np.random.normal(0, 1, L)
    white_noise_binarized = binarize(white_noise, [-1, 1])
    return white_noise_binarized


def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def binarize(xs, digits):
    return np.array([digits[0] if x <= 0 else digits[1] for x in xs])