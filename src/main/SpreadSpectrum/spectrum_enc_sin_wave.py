import soundfile as sf
import numpy as np
from src.main.SpreadSpectrum import mixer_sin_wave
from src.main.PhaseCoding.phase_enc import get_length


def spectrum_enc_sin_wave(signal, text):

    data, samplerate = sf.read(signal)



    #Changing text to bit and I have list of ints
    bitText = toBits(text)

    # Change length of text to bits -> max 32 bits
    length_bit_message = get_length(text)

    # Add length info to actual text
    # bitText.extend(length_bit_message)

    # Length of segments
    L = int(np.floor((len(data)-len(length_bit_message))/len(bitText)))

    #Number of segments (for 8 bits)
    nframe = np.floor(len(data) / L)

    # mod to ensure that number of segments is divisor of 8
    N = int(nframe - np.mod(nframe, 8))

    # Embedding message

    # Simple adding out coded signal to already existing data
    # Now for only one channel
    # OUTPUT = MESSAGE * PRN * CARRIER

    # Amplitude -> higher amplitude enhances quality of extraction
    #           -> but also has negative impact on the security
    amplitude = 0.005

    modulated_carrier = mixer_sin_wave.mixer_sin_wave(L, bitText, length_bit_message, samplerate)

    out = data

    stego = data[0:len(modulated_carrier), 0] + amplitude * modulated_carrier
    check_stego = np.reshape(stego, (len(stego), 1))

    # Adding stego signal to the rest of the original signal
    out[0:len(modulated_carrier), 0] = stego

    x = signal.split(".")

    sf.write(x[0] + '_stego.wav', out, samplerate)
    print("Stego signal saved in " + x[0] + "_stego.wav !")



def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def fromBits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

