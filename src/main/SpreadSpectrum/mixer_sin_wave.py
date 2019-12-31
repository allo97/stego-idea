import numpy as np
import matplotlib.pyplot as plt
from pylfsr import LFSR
from scipy import signal

def mixer_sin_wave(L, bitText, length_bit_message, samplerate):

    # INPUT VARIABLES
    # L - length of segment
    # bitText - binary sequence

    # OUTPUT VARIABLES
    # w_sig: Smoothed mixer signal -> after convolution and normalization




    # Variables
    modulation_freq = 1000
    modulation_period = 1/modulation_freq
    oscillations_per_chip = 5
    chip_period = oscillations_per_chip * modulation_period # tc
    chip_freq = 1/chip_period
    phase = np.pi/2
    probes_per_period = samplerate/chip_freq


    # Number of segments ... I can change from (0,1) to (-1,1) so change 0 to -1
    N = len(bitText)
    data_length = N * L

    # Mixer signal
    m_sig = np.reshape(np.ones((L, 1)) * np.array(bitText), (data_length, 1), 'F')
    m_sig = np.squeeze(m_sig)
    m_sig = binarize(m_sig, [-1, 1])
    check_msig = np.reshape(m_sig, (len(m_sig), 1))

    # Generate pseudorandom noise sequence
    random_length = int(np.ceil(data_length / probes_per_period))
    pseudo_random_noise = rand_gen(random_length)

    # Modulating pseudorandom noise to change with chip frequency
    modulated_noise = modulate_pseudo_random_numbers(data_length, probes_per_period, pseudo_random_noise)

    # Multiplying noise * text
    chip = m_sig * np.reshape(modulated_noise, (1, len(modulated_noise)))
    chip = np.squeeze(chip)
    # Appending binarized length_bit_text to the end of the pseudorandom text
    length_bit_message = binarize(length_bit_message, [-1, 1])
    chip = np.append(chip, length_bit_message)
    check_chip = np.reshape(chip, (len(chip), 1))

    # Creating carrier wave with modulation frequency
    t = np.arange(0, (len(chip))/samplerate, 1/samplerate)
    tc = t / oscillations_per_chip
    carrier = np.sin(2*np.pi*modulation_freq*t + phase)
    carrier2 = np.sin(2*np.pi*modulation_freq*tc + phase)

    # plt.plot(t[268000:-1], carrier[268000:-1], lw=1, label="zmodulowany sinus")
    # plt.plot(t[268000:-1], carrier2[268000:-1], lw=1, label="wolniejszy sinus")
    # plt.title("Modulacja sygnału nośnego")
    # plt.xlabel("Czas [s]")
    # plt.ylabel("Amplituda [V]")
    # plt.legend()
    # plt.show()
    # plt.close()

    # Modulating sin wave with noise
    modulated_carrier = chip * carrier

    # Appending binarized length_bit_text to the end of the modulated carrier
    # length_bit_message = binarize(length_bit_message, [-1, 1])
    # modulated_carrier = np.append(modulated_carrier, length_bit_message)

    # plt.plot(t[268000:-1], modulated_carrier[268000:-1], lw=1, label="zmodulowany sinus")
    # plt.plot(t[268000:-1], chip[268000:-1], lw=1, label="pseudolosowa informacja")
    # plt.plot(t[268000:-1], carrier[268000:-1], lw=1, label="oryginalny sinus")
    # plt.title("Modulacja sygnału nośnego")
    # plt.xlabel("Czas [s]")
    # plt.ylabel("Amplituda [V]")
    # plt.legend()
    # plt.show()
    # plt.close()


    return modulated_carrier

def binarize(xs, digits):
    return np.array([digits[0] if x <= 0 else digits[1] for x in xs])

def rand_gen(num_of_periods):
    np.random.seed(1)
    white_noise = np.random.normal(0, 1, num_of_periods)
    white_noise_binarized = binarize(white_noise, [-1, 1])
    return white_noise_binarized

def modulate_pseudo_random_numbers(data_length, probes_per_period, pseudo_random_noise):
    modulated = np.ones((int(probes_per_period), 1)) * pseudo_random_noise
    modulated_signal = np.reshape(modulated, (modulated.size, 1), 'F')
    modulated_signal = modulated_signal[0:data_length]
    return modulated_signal






def generate_LFSR():
    state = [1,1]
    fpoly = [2,1]
    L = LFSR(fpoly=fpoly, initstate=state, verbose=True)
    L.info()
    tempseq = L.runKCycle(20)
    tempseq = np.reshape(tempseq, (len(tempseq), 1))

    xddd = " fdferf"