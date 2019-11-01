import soundfile as sf
import math
import time
import numpy as np
import numpy.fft as fft
#phase_enc("..\data\coverAudio.wav", "lul", 1024)


def phase_enc(signal, text, L):

    data, samplerate = sf.read(signal)
    # get one channel
    new_data = data[:,0]

    #convert text to bit
    bitText = toBits(text)

    I = len(new_data)

    #length of bit sequence to hide
    m = len(bitText)

    #number of frames
    N = int(np.floor(I / L))

    segments = np.reshape(new_data[0:(N * L)], (L, N), 'F')

    w = fft.fft(segments, axis=0)
    Phi = np.angle(w)
    A = np.abs(w)

    DeltaPhi = np.zeros((L, N))

    #Calculating phase differences of adjacent segments
    for i in range(N-1):
        DeltaPhi[:,i] = Phi[:,i + 1] - Phi[:,i]

    PhiData = np.zeros(m)

    for count, ele in enumerate(bitText):
        print(ele)
        print(count)
        if ele == 0:
             PhiData[count] = (math.pi / 2)
        else:
             PhiData[count] = (-math.pi / 2)


    somthibng = "ghhyh"

def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def fromBits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
