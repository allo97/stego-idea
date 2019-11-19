import numpy as np

def mixer(L, bitText, lower, upper, carrier_wave, samplerate):

    # INPUT VARIABLES
    # L - length of segment
    # bits - binary sequence
    # K - length to be smoothed
    # upper - Upper bound of mixer signal
    # lower - Lower bound of mixeer signal

    # OUTPUT VARIABLES
    # m_sig: Normal Signal data streched to N * L
    # w_sig: Smoothed mixer signal -> after convolution and normalization

    # Divisibility by 4
    K = int(np.floor(L/4) - np.mod(np.floor(L/4),4))

    # Number of segments ... I can change from (0,1) to (-1,1) so change 0 to -1
    N = len(bitText)

    # Mixer signal
    m_sig = np.reshape(np.ones((L, 1)) * np.array(bitText), (N*L, 1), 'F')
    m_sig = np.squeeze(m_sig)

    # Creating carrier wave
    if carrier_wave == 1:
        carrier = np.squeeze(np.hanning(K))
    else:
        t = np.arange(0, K/samplerate, 1/samplerate)
        carrier = np.sin(2 * np.pi * samplerate * t)


    # Convolution operation
    c = np.convolve(m_sig, carrier)

    # Multiplication operation -> in this case change bitText to -1,1 series

    #Normalization
    wnorm = c[K//2:len(c) - K//2 + 1] / np.max(np.abs(c))

    # Adjusting bounds
    w_sig = wnorm * (upper - lower) + lower
    m_sig = m_sig * (upper - lower) + lower

    return w_sig, m_sig

