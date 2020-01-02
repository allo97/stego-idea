# We will use wave package available in native Python installation to read and write .wav audio file
import wave
from tqdm import tqdm


def encode(signal, text):

    print("Wykonuję metodę najmniej znaczącego bitu...")
    # read wave audio file
    song = wave.open(signal, mode='rb')
    song_name = signal.split("/")[-1]
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    len_frame_bytes = len(frame_bytes)


    # Append dummy data to fill out rest of the bytes.
    # check if file is too big to embed the data
    if len(text) * 8 > len_frame_bytes:
        answer = "Plik jest za duży! Usuń conajmniej " + str(abs(int((len_frame_bytes / 8 - len(text)) / 1.33))) + " znaków z pliku! \nSpróbuj jeszcze raz!"
        print(answer)
        exit()

    dummy = "*&w1`"
    hashes = (int((len(frame_bytes) - (len(text) * 8)) / 8) - len(dummy)) * '#'
    hashes = dummy + hashes
    text = text + hashes
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in tqdm(text)])))
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(tqdm(bits)):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)
    # Write bytes to a new wave audio file
    with wave.open('../data/data_from_embedding/' + 'stego_' + song_name, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

    return "Tekst zostal osadzony w: stego_" + song_name


def decode(signal):

    print("Wykonuję metodę najmniej znaczącego bitu...")

    song = wave.open(signal, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in tqdm(range(len(frame_bytes)))]
    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in tqdm(range(0, len(extracted), 8)))
    # Cut off at the filler characters
    decoded = string.split("*&w1`")[0]
    song.close()
    return decoded