import soundfile as sf
import math
import numpy as np


def phase_enc(signal, text):

    data, samplerate = sf.read(signal)

    # get one channel
    new_data = data[:,0]

    #convert text to bit
    bitText = toBits(text)

    # amount of frames
    F = 50

    #Get length of each frame
    L = int(len(data) / F)
    if L % 2 != 0:
        L = L - 1

    I = len(new_data)

    # Reserve place for information about length of text -> max 32 bits
    list_of_bits = [int(x) for x in list('{0:032b}'.format(len(text)))]

    # Add length info to actual text
    bitText.extend(list_of_bits)

    # length of bit sequence to hide
    m = len(bitText)

    #number of frames
    N = int(np.floor(I / L))

    segments = np.reshape(new_data[0:(N * L)], (L, N), 'F')

    w = np.fft.fft(segments, axis=0)
    Phi = np.angle(w)
    A = np.abs(w)


    DeltaPhi = np.zeros((L, N))

    #Calculating phase differences of adjacent segments
    for i in range(1, N):
        DeltaPhi[:,i] = Phi[:,i] - Phi[:,i-1]

    #Binary data is represented as {-pi / 2, pi / 2} and stored in PhiData
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
    data[:,0] = out

    x = signal.split(".")

    sf.write(x[0] + '_stego.wav', data, samplerate)
    print("Stego signal saved in " + x[0] + "_stego.wav !")


def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result



def checkEqual(data, out):
    for i in range(len(out)):
        if data[i, 0] != out[i]:
            return "nie sa rowne, ale powinny byc"
        else:
            return "sa rowne"