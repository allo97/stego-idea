import numpy as np




def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def binarize(xs, digits):
    return np.array([digits[0] if x <= 0 else digits[1] for x in xs])

def rand_gen(num_of_periods):
    np.random.seed(1)
    white_noise = np.random.normal(0, 1, num_of_periods)
    white_noise_binarized = binarize(white_noise, [-1, 1])
    return white_noise_binarized

message_frequency = 500
message_code = np.array(toBits("Test"))
carrier_frequency = 1000
amplitude = 1
phase = 0
time_start = 0
time_end = 1/message_frequency * message_code.size
time_duration = time_end - time_start
samples_per_carrier_period = 5
dt = 1 / carrier_frequency / samples_per_carrier_period
time_steps = time_duration / dt
t = np.linspace(time_start, time_end, int(time_steps))



carrier_signal = amplitude * np.sin(2 * np.pi * carrier_frequency * t + phase)

random_period = 1/1000 # frequency is 1000Hz twice than 500Hz message freq



original_binarized_coarse_acquisition_code = rand_gen(1023)
coarse_acquisition_code = np.tile(original_binarized_coarse_acquisition_code, int(time))
print(int(time_duration/random_period))
print(coarse_acquisition_code.size)
coarse_acquisition_code = np.repeat(coarse_acquisition_code, t.size / coarse_acquisition_code.size)
print(coarse_acquisition_code.size)
coarse_acquisition_code_signal = binarize(coarse_acquisition_code, [-1, 1])
print(coarse_acquisition_code_signal.size)
print(coarse_acquisition_code_signal)

check = time_duration * message_frequency
check2 = int(time_duration / random_period)

message_signal = binarize(np.repeat(message_code, t.size / message_code.size), [-1, 1])
xddd = "fefe"




