import soundfile as sf
import numpy as np
from src.main.SpreadSpectrum.band_pass_filter import butter_bandpass_filter


def spectrum_dec_sin_wave(signal):

    data, samplerate = sf.read(signal)

    # Variables
    modulation_freq = 1000
    modulation_period = 1 / modulation_freq
    oscillations_per_chip = 5
    chip_period = oscillations_per_chip * modulation_period  # tc
    chip_freq = 1 / chip_period
    phase = np.pi / 2
    probes_per_period = samplerate / chip_freq
    t = np.arange(0, (len(data)) / samplerate, 1 / samplerate)

    # Generate pseudorandom noise sequence
    random_length = int(np.ceil(len(data) / probes_per_period))
    pseudo_random_noise = rand_gen(random_length)

    # Modulating pseudorandom noise to change with chip frequency
    modulated_noise = modulate_pseudo_random_numbers(len(data), probes_per_period, pseudo_random_noise)

    # Input signal * chip signal without text
    my_input = data[:,0] * np.reshape(modulated_noise, (1, len(modulated_noise)))
    my_input = np.squeeze(my_input)

    # Now filtering by band pass filter

    # plt.figure(1)
    # plt.clf()
    # plt.plot(t, my_input, label='Noisy signal')

    y = butter_bandpass_filter(my_input, 750, 1250, samplerate, order=6)
    # plt.plot(t, y, label='Filtered signal (%g Hz)' % modulation_freq)
    # plt.xlabel('time (seconds)')
    # plt.grid(True)
    # plt.axis('tight')
    # plt.legend(loc='upper left')
    #
    # plt.show()





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