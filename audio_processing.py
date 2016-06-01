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

def euclidean_distance(a, b):
    d = 0
    if len(a) != len(b):
        print("Warning: vectors are of different sizes")
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

# THIS FUNCTION IS IN ROUGH DRAFT MODE RIGHT NOW
def trim_silence(signal):
    """
    * trims leading and trailing silence from the signal
    * to make further processing easier
    """
    signal_begin = -1    # will be first relevant sample
    signal_end = -1      # will be last relevant sample

    l = len(signal)
    step = int(SR / 200) # consider 50 ms chunks
    start = 0
    end = start + step
    centroids = []
    while end < l:
        chunk = signal[start:end]
        spectrum = fft.rfft(chunk)
        c = spectral_centroid(spectrum)
        centroids.append(c)
        if c > 200 and signal_begin < 0:
            signal_begin = start
        if c < 200 and signal_begin >= 0:
            signal_end = end

        start = end
        end = start + step
    return (signal[ signal_begin : signal_end ], centroids)

def zero_crossing_rate(signal):
    n = 0
    for i in range(1, len(signal)):
        if (signal[i] * signal[i - 1]) < 0: # if there is a zero crossing
            n += 1
    n = n / len(signal)
    return n

def fundamental(signal):
    s = fft.rfft(signal)

    """
    N = len(s)
    print("number of bins:", N)

    hz = 1000
    step = int (2 * hz * N / SR)
    start = 0
    end = start + step

    while end < N:
        m = np.argmax(s[start:end]) + start
        f = m * SR / (2 * N)
        print(f)
        start = end
        end += step
    """
    m = np.argmax(s)
    f = m * SR / (2 * len(s))
    return f

def harmonic_representation(signal):
    harmonics = []

    fund = fundamental(signal)
    num_harmonics = min(8, int( 22050 / fund) )

    start = int( SR / 4 )
    end = int( start + SR / 4 )

    # get the spectrum, and start working on
    # getting the harmonic information
    spectrum = fft.rfft( hann_window( signal[start:end] ) )
    L = len(spectrum)

    f = fundamental( signal[start : end] )
    # print(fund, f)

    # f_indx = int( (f * 2 * L) / SR )
    # harmonics.append( abs(spectrum[f_indx]) )

    for i in range(1, num_harmonics + 1):
        f_indx = int( f * i * 2 * L / SR)
        print("now on ", f_indx)

        r = abs( spectrum[f_indx] )
        for j in range(f_indx - 10, f_indx + 20):
            if abs( spectrum[j] ) > r:
                r = abs( spectrum[j] )

        harmonics.append( r )

    t = harmonics[0]
    for i in range(len(harmonics)):
        harmonics[i] = harmonics[i] / t

    return harmonics

def spectral_centroid(spectrum):
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
        f = (i * SR) / (2 * l) # the freqency of the ith bin
        x = abs(spectrum[i])
        centroid += f * x
        d += x
    if d == 0:
        return 0
    centroid = centroid / d
    return centroid

def harmonic_representation(signal):
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

def spectral_mean(signal):
    return np.sum(np.absolute(signal))/len(signal)

def spectral_flux(signal):
    """
    divide the signal into 16 chunks and compute the flux
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
