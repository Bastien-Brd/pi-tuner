import sounddevice as sd
import numpy as np
import time


def is_in_range(f, f_range):
    """
    f_range is a tuple (f_min, f_max)
    """
    return (f >= f_range[0]) and (f < f_range[1])

pitch_ranges = {
    'E2': (0.0, 82.41, 96.21),
    'A2': (96.21, 110.0, 128.41),
    'D3': (128.41, 146.83, 171.41),
    'G3': (171.41, 196.0, 221.47),
    'B3': (221.47, 246.94, 288.28),
    'E4': (288.28, 329.63, 10000.0),
}

def is_in_range(f, f_range):
    """
    f_range is a tuple (f_min, f_max)
    """
    return (f >= f_range[0]) and (f < f_range[1])

def tuning_guidance(f, precision=0.02):
    """
    Given a detected fundamental frequency f, 
    work out what is the most likely pitch to hit,
    and if the user should tune the string up or down to set it to that exact note or do nothing
    """
    # First we detect what is the most likely pitch to hit
    for pitch, pitch_boundaries in pitch_ranges.iteritems():
        if is_in_range(f, (pitch_boundaries[0], pitch_boundaries[2])):
            exact_target = pitch_boundaries[1]
            precision_range = ((1-precision)*exact_target, (1+precision)*exact_target)
            if is_in_range(f, precision_range):
                return pitch, 0
            elif f <= exact_target:
                return pitch, 1
            else:
                return pitch, -1

device = 0    # we use my USB sound card device
duration = 1  # seconds
fs = 44100    # samples by second

while True:
    print("---------")
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, device=device)
    time.sleep(1.1*duration)
    fourier = np.fft.fft(myrecording.ravel())
    f_max_index = np.argmax(abs(fourier[:fourier.size/2]))
    freqs = np.fft.fftfreq(len(fourier))
    print(freqs[f_max_index]*fs)
    print(tuning_guidance(f))
