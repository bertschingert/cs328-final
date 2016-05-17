# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# audio-processing.py

import math
import numpy.fft as fft
import matplotlib.pyplot as plt
import audio_utils

SR = 44100
SP = 1 / SR

# dur in seconds
# amp between 0 and 1


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

def graph_fft(spectrum):
    length = len(spectrum)
    plt.plot(range(length), spectrum)
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.title('Spectrum')
    plt.show()

def main():
    """
    wave1 = create_sine_wave(440, 1, 1)
    chunk1 = wave1[:400]

    wave2 = create_saw_wave(441, 1, 1)
    for i in wave2:
        print(i)

    freqs = fft.rfft(wave1)
    #for i in range(len(freqs)):
        #print("bin ", i * SR / len(chunk), " : ", end = "")
        #print(abs(freqs[i]))
    """
    left, right = read_raw_stereo("audio_files/violin-a440.raw")

    # print(len(left), len(right))
    chunk = left[:44100]
    freqs = fft.rfft(chunk)
    for i in range(len(freqs)):
        print("bin ", i * SR / len(chunk), " : ", end = "")
        print(abs(freqs[i]))


if __name__ == '__main__':
    main()
