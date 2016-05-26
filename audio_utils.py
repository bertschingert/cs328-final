# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio_utils.py
# This file has useful audio code

import math
import wave
import struct
import matplotlib.pyplot as plt

SR = 44100      # sapmle rate (assumed to be 44100 always)
SP = 1 / SR     # sample period

def graph_fft(spectrum, f):
    """
    * plots the spectrum, which should
    * be the output of an FFT
    * spectrum : must be COMPLETE spectrum
    *            in order to get accurate bin info
    * f : graph stops at this frequency
    """
    real_spectrum = []
    for s in spectrum:
        real_spectrum.append(abs(s))
    length = len(real_spectrum)

    bins = []
    n = 0
    for i in range(length):
        val = i * SR / (2 * length)
        if val > f and n == 0:
            n = i
        bins.append( val )

    fig = plt.plot(bins[:n], real_spectrum[:n])
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.title('Spectrum')
    plt.show()

def graph_signal(signal, rate = 44100):
    """
    * plots the signal
    * rate is how many samples per second
    """
    length = len(signal)

    t_locs = []
    t_names = []
    s = int(length / rate)
    for i in range(s + 1):
        t_locs.append(rate * i)
        t_names.append(str(i))

    plt.plot(range(length), signal)
    plt.xlabel('time')
    plt.xticks(t_locs, t_names)
    plt.ylabel('amplitude')
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
