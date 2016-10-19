import sounddevice as sd
import numpy as np
import time

from led_display import display_tuning_guidance


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

# Define some settings
device = 0    # we use my USB sound card device
duration = 1  # seconds
fs = 44100    # samples by second
precision=0.02 # how close to the target pitch do we consider a match

while True:
    print("---------")
    # Listen to a bit of sound from the mic, recording it as a numpy array
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, device=device)
    time.sleep(1.1*duration)
    # Calculate the Fourier transform of the recorded signal
    fourier = np.fft.fft(myrecording.ravel())
    # Extrat the fundamental frequency from it 
    f_max_index = np.argmax(abs(fourier[:fourier.size/2]))
    # Get the scale of frequencies corresponding to the numpy Fourier transforms definition
    freqs = np.fft.fftfreq(len(fourier))
    # And so the actual fundamental frequency detected is
    f_detected = freqs[f_max_index]*fs
    print(f_detected)
    # Give relevant guidance to the user (tune up or down)
    display_tuning_guidance(tuning_guidance(f_detected, precision))
