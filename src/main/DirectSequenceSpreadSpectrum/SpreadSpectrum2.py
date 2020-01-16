import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
import soundfile as sf



def binarize(xs, digits):
    return np.array([digits[0] if x <= 0 else digits[1] for x in xs])

def tobits(s):
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

def rand_gen(L):
    np.random.seed(1)
    white_noise = np.random.normal(0, 1, L)
    white_noise_binarized = binarize(white_noise, [-1, 1])
    return white_noise_binarized

def plot_signal_and_spectrum(signal_td, t, pos_start_td, pos_end_td, pos_start_fd, pos_end_fd, title_td, xlabel_td,
                             ylabel_td, title_fd, xlabel_fd, ylabel_fd, title_window, savefig):
    global plot_counter
    plot_counter += 1

    signal_fd = np.abs(np.fft.rfft(signal_td)) ** 2
    dt = t[1] - t[0]
    signal_frequencies = np.fft.rfftfreq(signal_td.size, dt)
    df = signal_frequencies[1] - signal_frequencies[0]

    pos_start_td = int(pos_start_td / dt)
    if pos_end_td != -1:
        pos_end_td = int(pos_end_td / dt)
    pos_start_fd = int(pos_start_fd / df)
    if pos_end_fd != -1:
        pos_end_fd = int(pos_end_fd / df)

    fig = plt.figure(plot_counter)
    splt = plt.subplot(211)
    plt.plot(t[pos_start_td:pos_end_td], signal_td[pos_start_td:pos_end_td], lw=0.5)
    splt.set_title(title_td)
    splt.set_xlabel(xlabel_td)
    splt.set_ylabel(ylabel_td)

    splt = plt.subplot(212)
    plt.semilogy(signal_frequencies[pos_start_fd:pos_end_fd], signal_fd[pos_start_fd:pos_end_fd], lw=0.2)
    splt.set_title(title_fd)
    splt.set_xlabel(xlabel_fd)
    splt.set_ylabel(ylabel_fd)

    fig.canvas.set_window_title(str(plot_counter) + " " + title_window)
    if savefig:
        default_size = fig.get_size_inches()
        fig.set_size_inches((default_size[0] * 2, default_size[1] * 2))
        fig.savefig(str(plot_counter) + "-" + title_window.replace(" ", "-") + ".svg", bbox_inches='tight')
        fig.set_size_inches((default_size[0] * 3, default_size[1] * 3))
        fig.savefig(str(plot_counter) + "-" + title_window.replace(" ", "-") + ".png", bbox_inches='tight')
        print(title_window + " saved.")
    # plt.show(fig)
    plt.close(fig)

def plot_two_signals(signal1, t1, signal2, t2, pos_start1, pos_end1, pos_start2, pos_end2, title1, xlabel1, ylabel1,
                     title2, xlabel2, ylabel2, title_window, savefig):
    global plot_counter
    plot_counter += 1

    pos_start1 = int(pos_start1)
    pos_end1 = int(pos_end1)
    pos_start2 = int(pos_start2)
    pos_end2 = int(pos_end2)

    fig = plt.figure(plot_counter)
    splt = plt.subplot(211)
    if t1 is None:
        plt.plot(signal1[pos_start1:pos_end1], lw=0.5)
    else:
        plt.plot(t1[pos_start1:pos_end1], signal1[pos_start1:pos_end1], lw=0.5)
    splt.set_title(title1)
    splt.set_xlabel(xlabel1)
    splt.set_ylabel(ylabel1)

    splt = plt.subplot(212)
    if t2 is None:
        plt.plot(signal2[pos_start2:pos_end2], lw=0.5)
    else:
        plt.plot(t2[pos_start2:pos_end2], signal2[pos_start2:pos_end2], lw=0.5)
    splt.set_title(title2)
    splt.set_xlabel(xlabel2)
    splt.set_ylabel(ylabel2)

    fig.canvas.set_window_title(str(plot_counter) + " " + title_window)
    fig.canvas.set_window_title(str(plot_counter) + " " + title_window)
    if savefig:
        default_size = fig.get_size_inches()
        fig.set_size_inches((default_size[0] * 2, default_size[1] * 2))
        fig.savefig(str(plot_counter) + "-" + title_window.replace(" ", "-") + ".svg", bbox_inches='tight')
        fig.set_size_inches((default_size[0] * 3, default_size[1] * 3))
        fig.savefig(str(plot_counter) + "-" + title_window.replace(" ", "-") + ".png", bbox_inches='tight')
        print(title_window + " saved.")
    plt.close(fig)

plot_counter = 0
savefig = True

# Transmitt the message at given frequency
message_frequency = 500
message_code = np.array(tobits("hehehehehehehehehehehe xd"))
carrier_frequency = 44e3

# nasz wav do ukrycia w nim danych

data, samplerate = sf.read("C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/coverAudio.wav")

#
coarse_acquisition_code_frequency = carrier_frequency / 10


amplitude = 1

phase = 0



time_start = 0

# 0.056 s = 56 ms
time_end = 1 / message_frequency * message_code.size

# 56 ms
time_duration = time_end - time_start

# How many samples per carrier period will the simulation have, since we can't have a truly continuous signal.
samples_per_carrier_period = 5
dt = 1 / carrier_frequency / samples_per_carrier_period
time_steps = time_duration / dt
t = np.linspace(time_start, time_end, int(time_steps))

carrier_signal = amplitude * np.sin(2 * np.pi * carrier_frequency * t + phase)



pos_start_td = 2.4e-3 - 0.7e-3
pos_end_td = 2.4e-3 + 0.7e-3

plot_signal_and_spectrum(carrier_signal, t, pos_start_td, pos_end_td, carrier_frequency - coarse_acquisition_code_frequency,
                         carrier_frequency + coarse_acquisition_code_frequency,
                         "Carrier signal time domain",
                         "Time [s]",
                         "Amplitude [V]", "Carrier signal frequency domain", "Frequency [Hz]", "Power [W]",
                         "Carrier signal", savefig)

# Randomize

password_to_random = 'password'

coarse_acquisition_code_signal = rand_gen(t.size)

plot_signal_and_spectrum(coarse_acquisition_code_signal, t, pos_start_td, pos_end_td,0,
                         coarse_acquisition_code_frequency * 10,
                         "PRN code time domain", "Time [s]", "Amplitude [V]", "PRN code frequency domain",
                         "Frequency [Hz]", "Power [W]",
                         "Coarse acquisition code signal", savefig)


# Message
message_signal = binarize(np.repeat(message_code, t.size / message_code.size), [-1, 1])

plot_signal_and_spectrum(message_signal, t, 0, -1, 0, message_frequency * 4,
                             "Message signal time domain",
                             "Time [s]",
                             "Amplitude [V]",
                             "Message signal frequency domain", "Frequency [Hz]", "Power [W]", "Message signal",
                             savefig)

# Output signal
# OUTPUT = MESSAGE * PRN * CARRIER
output_signal = carrier_signal * message_signal * coarse_acquisition_code_signal

plot_signal_and_spectrum(output_signal, t, pos_start_td, pos_end_td,
                             carrier_frequency - coarse_acquisition_code_frequency * 10,
                             carrier_frequency + coarse_acquisition_code_frequency * 10,
                             "Output signal time domain",
                             "Time [s]",
                             "Amplitude [V]", "Output signal frequency domain", "Frequency [Hz]", "Power [W]",
                             "Output signal", savefig)


# Tutaj możemy dodać naszego wava, jako szum moze sie uda usrednic






# MESSAGE = OUTPUT * PRN * CARRIER
decoded_message = output_signal * coarse_acquisition_code_signal * carrier_signal
decoded_message_code = binarize(np.average(decoded_message.reshape((int(time_duration * message_frequency), -1)), 1), [0, 1])

plot_two_signals(decoded_message, t, decoded_message_code,
                 t[::int(t.size / decoded_message_code.size)],
                 0, 1 / message_frequency / (t[1] - t[0]), 0, -1,
                 "One bit of demodulated and digitized signal time domain", "Time [s]", "Amplitude [V]",
                 "Decoded message time domain", "Time [s]", "Bit value", "Decoded message", savefig)

decoded_message = fromBits(decoded_message_code)
print(decoded_message)


