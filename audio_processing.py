# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio-processing.py

import math
import wave
import struct
import numpy.fft as fft
import audio_utils as au
import numpy as np

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

def get_spectral_centroid(spectrum, f_s):
    """
    * computes the spectral centroid
    * which is the weighted mean of the spectrum
    * spectrum : the output of the FFT of a signal
    * f_s : sample rate
    """
    l = len(spectrum)
    centroid = 0
    d = 0
    for i in range(l):
        f = (i * f_s) / (2 * l) # the freqency of the ith bin
        x = abs(spectrum[i])
        centroid += f * x
        d += x
    centroid = centroid / d
    return centroid

def get_spectral_flux(signal, f_s):
    l = len(signal)
    if l < (f_s / 2):
        print("Warning: very short signal")
    # divide the signal up into chunks
    step = int(f_s / 16)
    start = 0
    end = start + step
    old_spectrum = [0] * (int(step / 2) + 1)
    spectralFlux = []
    while end < l:
        chunk = signal[start:end]
        new_spectrum = fft.rfft(chunk)
        spectralFlux.append(get_vector_distance(old_spectrum, new_spectrum))
        old_spectrum = list(new_spectrum)
        # print( "Old: ", id(old_spectrum), "New: ", id(new_spectrum) )
        start = end
        end = start + step
    return spectralFlux

def get_spectral_mean(signal):
    return np.sum(np.absolute(signal))/len(signal)

def hann_window(signal):
    """
    * the Hann window tapers the beginning and end
    * of a signal
    * this reduces noise when applying the FFT
    """
    windowed_signal = []
    N = len(signal)
    for i in range(N):
        val = 1 - math.cos( (2 * math.pi * i) / (N - 1) )
        val *= 0.5
        windowed_signal.append(val * signal[i])
    return windowed_signal

def main():
    f = au.read_wav_mono('audio_files/trumpet_A3_15_pianissimo_normal.wav')
    print(len(f))
    m = 0
    for i in f:
        if i < m:
            m = i
    print(m)


if __name__ == '__main__':
    main()
