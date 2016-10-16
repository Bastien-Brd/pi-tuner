import sounddevice as sd
import numpy as np


device = 0    # we use my USB sound card device
duration = 1  # seconds
fs = 44100    # samples by second

while True:
    print("---------")
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, device=device)
    time.sleep(1.1*duration)
    fourier = np.fft.fft(myrecording.ravel()[25000:30000])
    f_max_index = np.argmax(abs(fourier[:fourier.size/2]))
    freqs = np.fft.fftfreq(len(fourier))
    print(freqs[f_max_index]*fs)
