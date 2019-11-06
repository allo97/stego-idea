import soundfile as sf
import math
import numpy as np
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

    w = np.fft.fft(segments, axis=0)
    invW = np.fft.ifft(w, axis=0)
    Phi = np.angle(w)
    A = np.abs(w)


    DeltaPhi = np.zeros((L, N))

    #Calculating phase differences of adjacent segments DOBRE!!!!!!
    for i in range(1, N):
        DeltaPhi[:,i] = Phi[:,i] - Phi[:,i-1]

    #Binary data is represented as {-pi / 2, pi / 2} and stored in PhiData DOBRE!!!!
    PhiData = np.zeros(m)

    for count, ele in enumerate(bitText):
        if ele == 0:
             PhiData[count] = (math.pi / 2)
        else:
             PhiData[count] = (-math.pi / 2)

    #PhiData is written onto the middle of first phase matrix
    Phi_new = np.zeros((L,N))
    Phi_new[:,0] = Phi[:, 0]
    Phi_new[L//2-m:L//2,0] = PhiData                    #Hermitian symmetry
    Phi_new[L//2+1:L//2 + m+1, 0] = -np.flip(PhiData)   #Hermitian symmetry

    #Re-creating phase matrixes using phase differences
    for i in range(1, N):
        Phi_new[:,i] = Phi_new[:,i-1] + DeltaPhi[:,i]

    # Reconstructing the sound signal by applying the inverse FFT

    z = np.real(np.fft.ifft(A * np.exp(1j * Phi_new), axis=0))

    snew = np.reshape(z, N * L, 'F')
    out = np.append(snew, new_data[N * L: I])
    sf.write(signal +  '_stego.wav', out, samplerate)


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
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
