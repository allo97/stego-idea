import soundfile as sf
import numpy as np
from src.SpreadSpectrum import mixer
from src.PhaseCoding.phase_enc import get_length

def spectrum_enc(signal, text, carrier_wave):

    data, samplerate = sf.read(signal)

    # Minimum value length for each segment
    L_min = 8 * 1024

    #Changing text to bit and I have list of ints
    bitText = toBits(text)

    # Change length of text to bits -> max 32 bits
    length_bit_message = get_length(text)

    # Add length info to actual text
    # bitText.extend(length_bit_message)

    # Length of segments
    L2 = np.floor(len(data)/len(bitText))

    # Keeping length of sequence big enough
    L = int(max(L_min, L2))

    #Number of segments (for 8 bits)
    nframe = np.floor(len(data) / L)
    N = int(nframe - np.mod(nframe, 8))  # mod to ensure that number of segments is divisor of 8

    if len(bitText) > N:  # this condition is true only when L2 < L_min
        print("Message is too long, is being cropped")
        bitText = bitText[1:N]
    else:
        bitText.extend(np.zeros(N - len(bitText), dtype=str))

    r = rand_gen("password", L)
    pr = np.reshape(r * np.ones((N,1)), (N * L, 1))
    alpha = 0.005


    # Embedding message
    result = mixer.mixer(L, bitText, -1, 1, carrier_wave, samplerate)
    smoothed_text = result[0]
    normal_signal = result[1]

    out = data
    # Simple adding pseudo numbers and smoothed_text into our data
    stego = data[0:N*L, 0] + alpha * smoothed_text * np.transpose(pr)

    # Adding stego signal to the rest of the original signal
    out[0:N*L, 0] = stego

    x = signal.split(".")

    sf.write(x[0] + '_stego.wav', out, samplerate)
    print("Stego signal saved in " + x[0] + "_stego.wav !")


def rand_gen(key, L):
    passw = sum(np.array([ord(c) for c in key]) * np.array(range(len(key))))
    np.random.seed(passw)
    # I want to randomize with 1 and -1
    # When  rand > 0.5 => 1,
    # When  rand < 0.5 =>-1
    out = 2 * (np.random.rand(int(L)) > 0.5) - 1
    return out



def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result