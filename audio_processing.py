# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio-processing.py

import math
import numpy.fft as fft
import matplotlib.pyplot as plt
import audio_utils

SR = 44100
SP = 1 / SR

# returns the "Hamming" distance of two vectors
def get_vector_distance(a, b):
    d = 0
    if len(a) != len(b):
        print("Warning: vectors are of different sizes")
    l = min(len(a), len(b))
    for i in range(l):
        d += abs(a[i] - b[i])
    return d

# THIS FUNCTION IS IN ROUGH DRAFT MODE RIGHT NOW
def get_attack_time(signal, f_s):
    """
    * ostensibly returns the attack time in milliseconds
    * signal : a vector with the samples
    * f_s : the sample rate
    """
    l = len(signal)
    if l < (f_s / 2):
        print("Warning: very short signal")
    # divide the signal up into chunks
    step = int(f_s / 50)
    start = 0
    end = start + step
    old_spectrum = [0] * (int(step / 2) + 1)
    while end < l:
        chunk = signal[start:end]
        new_spectrum = fft.rfft(chunk)
        d = get_vector_distance(old_spectrum, new_spectrum)
        print(d)
        old_spectrum = list(new_spectrum)
        # print( "Old: ", id(old_spectrum), "New: ", id(new_spectrum) )
        start = end
        end = start + step
    return 0

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

def main():
    left, right = audio_utils.read_raw_stereo("audio_files/violin-a440.raw")

    chunk = left[:44100]
    freqs = fft.rfft(chunk)
    """
    for i in range(len(freqs)):
        print("bin ", i * SR / len(chunk), " : ", end = "")
        print(abs(freqs[i]))
    """
    get_attack_time(left, SR)


if __name__ == '__main__':
    main()
