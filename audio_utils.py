# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio_utils.py
# This file has useful audio code

import math
import wave
import struct
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
    plt.ylable('amplitude')
    plt.title('Signal')
    plt.show()

def read_wav_mono(filename):
    """
    * returns a LIST of samples
    * each sample is a (signed 16-bit) integer
    """
    f = wave.open(filename, 'r')
    if f.getnchannels() != 1:
        print("Error: this is not mono")
        return
    out = []
    for i in range(f.getnframes()):
        # readframes returns a byte string
        # this is interpreted by the struct.unpack method
        # "<h" means a little-endian signed 16-bit integer
        # which is the format of our wav files
        val = struct.unpack("<h", f.readframes(1))[0]
        out.append(val)
    return out


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
