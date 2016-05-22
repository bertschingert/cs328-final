# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio_utils.py
# This file has useful audio code

import math
import matplotlib.pyplot as plt

SR = 44100
SP = 1 / SR

def graph_fft(spectrum):
    """
    * plots the spectrum, which should
    * be the output of an FFT
    """
    length = len(spectrum)
    plt.plot(range(length), spectrum)
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.title('Spectrum')
    plt.show()

def graph_signal(signal):
    """
    * plots the signal
    """
    length = len(signal)
    plt.plot(range(length), signal)
    plt.xlabel('time')
    plt.title('Signal')
    plt.show()

def read_raw_stereo(filename):
    raw_file = open(filename)
    left = []
    right = []
    i = 0
    for line in raw_file:
        if i%2 == 0:
            left.append(line)
        else:
            right.append(line)
        i = (i+1)%2
    return left, right

def create_sine_wave(freq, amp, dur):
    dur *= SR
    wave = []
    for i in range(dur):
        wave.append(amp * math.sin(i*freq*2*math.pi*SP))
    return wave

# this function is currently NON-FUNCTIONAL
def create_saw_wave(freq, amp, dur):
    dur *= SR
    period = SR / freq
    wave = []
    for i in range(dur):
        wave.append((i%period) / period)
    return wave
