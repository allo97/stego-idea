import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

choose_song = "C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_to_embedding/coverAudio.wav"
choose_return_song = "C:/Users/aslod/Documents/Ważne foldery/STUDIA/7 semestr/Praca inzynierska/Stegography/MyStego/src/data/data_from_embedding/stego4_coverAudio.wav"

samplerate, audio = wavfile.read(choose_song)
audio = audio.astype(np.float32, order='C') / 32768.0
samplerate2, audio2 = wavfile.read(choose_return_song)
audio2 = audio2.astype(np.float32, order='C') / 32768.0

t = np.arange(0, len(audio), 1) / samplerate

SMALL_SIZE = 16
MEDIUM_SIZE = 14

plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
my_list = list(np.arange(0,31,5))
my_list.append(33)
fig = plt.figure(1)
splt = plt.subplot(211)
plt.subplots_adjust(top = 0.95, hspace=0.43)
# plt.plot(t[2600:2800], audio[2600:2800,0], lw=1)
plt.plot(t, audio[:, 0], lw=0.5)
# plt.xticks(my_list)
plt.xticks(my_list)
splt.tick_params(axis='both', labelsize='12')
splt.set_title("Sygnał coverAudio przed osadzeniem")
splt.set_xlabel("czas [s]")
splt.set_ylabel("Amplituda [V]")



splt = plt.subplot(212)
plt.plot(t, audio2[:,0], lw=1)
plt.xticks(my_list)
splt.tick_params(axis='both', labelsize='12')
splt.set_title("Sygnał stego_coverAudio po osadzaniu metodą kodowania fazowego dla N = 50")
splt.set_xlabel("czas [s]")
splt.set_ylabel("Amplituda [V]")
plt.show(fig)
plt.close(fig)