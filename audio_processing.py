# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio-processing.py

import math
import wave
import struct
import numpy.fft as fft
import audio_utils as au
import numpy as np

"""
throughout our project, the sample rate
is always 44100 hz 
"""
SR = 44100

def euclidean_distance(a, b):
    """
    used for spectral flux
    gets the euclidean distance between two vectors
    """
    d = 0
    # if len(a) != len(b):
        # print("Warning: vectors are of different sizes")
    l = min(len(a), len(b))
    for i in range(l):
        d += ( abs(a[i]) - abs(b[i]) )**2
    return math.sqrt(d)

# THIS FUNCTION IS IN ROUGH DRAFT MODE RIGHT NOW
def attack_time(signal, f_s):
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

def zero_crossing_rate(signal):
    """
    Computes the zero crossing rate of the signal
    which is the number of sign changes
    divided by the total number of samples
    """
    n = 0
    for i in range(1, len(signal)):
        if (signal[i] * signal[i - 1]) < 0: # if there is a zero crossing
            n += 1
    n = n / len(signal)
    return n

def fundamental(signal):
    """
    Gets the fundamental frequency
    which is the strongest frequency present in the signal
    """
    s = fft.rfft(signal)

    m = np.argmax(s)
    f = m * SR / (2 * len(s))
    return f

def harmonic_representation(signal):
    """
    gets a harmonic representation of the signal
    first gets the fundamental frequency
    and then gets the amount of energy in integer multiples
    of the fundamental (considers 8 harmonics)
    and then normalizes these with respect to the fundamental
    """
    harmonics = []

    fund = fundamental(signal)
    num_harmonics = 8

    # get the spectrum, and start working on
    # getting the harmonic information
    s = fft.rfft( ap.hann_window(signal) )
    L = len(s)
    m = np.argmax(s)
    harmonics.append( abs(s[m]) )

    for i in range(2, num_harmonics + 1):
        c = m * i
        if c < L:
            b = max(0, c - 50)
            e = min(c + 50, L - 1)
            m0 = np.argmax(s[b:e])
            harmonics.append( abs(s[m0]) )
        else:
            harmonics.append( 0 )

    t = harmonics[0]
    for i in range(len(harmonics)):
        harmonics[i] = harmonics[i] / t

    return harmonics

def spectral_centroid(signal):
    """
    * computes the spectral centroid
    * which is the weighted mean of the spectrum
    """
    spectrum = fft.rfft(signal)
    l = len(spectrum)
    centroid = 0
    d = 0
    for i in range(l):
        f = (i * SR) / (2 * l) # the freqency of the ith bin
        x = abs(spectrum[i])
        centroid += f * x
        d += x
    if d == 0:
        return 0
    centroid = centroid / d
    return centroid

def spectral_flux(signal):
    """
    divide the signal into 16 chunks and compute the flux
    which is the amount of change in the spectrum
    from one frame to the next
    """
    flux = []
    step = int(len(signal) / 16)
    start = 0
    end = start + step
    old_spectrum = [0] * (int(step / 2) + 1)
    for i in range(16):
        new_spectrum = fft.rfft(signal[start:end])
        d = euclidean_distance(old_spectrum, new_spectrum)
        flux.append(d)
        old_spectrum = list(new_spectrum)
        start = end
        end = min(start + step, len(signal) - 1)

    return flux

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
    """
    f = au.read_wav_mono('audio_files/saxophone/saxophone_A5_15_fortissimo_normal.wav')

    h = harmonic_representation(f)
    print(np.array(h))
    """

    fnames = open('filenames.txt', 'r')
    for line in fnames:
        line = line.strip()
        if 'guitar' in line:
            print("guitar", end = ' ')
        if 'saxophone' in line:
            print("saxophone", end = ' ')
        if 'violin' in line:
            print("violin", end = ' ')
        f = au.read_wav_mono(line)
        print(zero_crossing_rate(f))

if __name__ == '__main__':
    main()
