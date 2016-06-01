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
    # wave.close()
    return out

def get_good_chunk(signal):
    N = 44100/4
    start = 0
    while abs(signal[start]) < 50:
        start += 1

    if start + N - 1 >= len(signal):
        return (-1, -1)
    return ( int(start) , int(start + N) )


def create_sine_wave(freq, amp, dur):
    dur *= SR
    wave = []
    for i in range(dur):
        wave.append(amp * math.sin(i*freq*2*math.pi*SP))
    return wave

def fetch_harmonic_rep(instr):
    h = []
    if instr not in ["guitar", "clarinet", "flute", "saxophone", "violin"]:
        print("invalid instrument")
        return ["nope"]
    infile = open("reps/" + instr + "_harmonics.txt", 'r')
    for line in infile:
        ex = []
        for i in line.split(','):
            ex.append( float(i.strip()) )
        h.append(ex)
    infile.close()
    return h

def fetch_flux_rep(instr):
    h = []
    if instr not in ["guitar", "clarinet", "flute", "saxophone", "violin"]:
        print("invalid instrument")
        return ["nope"]
    infile = open("reps/" + instr + "_flux.txt", 'r')
    for line in infile:
        ex = []
        for i in line.split(','):
            ex.append( float(i.strip()) )
        h.append(ex)
    infile.close()
    return h

def fetch_nflux_rep(instr):
    h = []
    if instr not in ["guitar", "clarinet", "flute", "saxophone", "violin"]:
        print("invalid instrument")
        return ["nope"]
    infile = open("reps/" + instr + "_nflux.txt", 'r')
    for line in infile:
        ex = []
        for i in line.split(','):
            ex.append( float(i.strip()) )
        h.append(ex)
    infile.close()
    return h

def fetch_centroid_rep(instr):
    h = []
    if instr not in ["guitar", "clarinet", "flute", "saxophone", "violin"]:
        print("invalid instrument")
        return ["nope"]
    infile = open("reps/" + instr + "_centroid.txt", 'r')
    for line in infile:
        h.append( float(line.strip()) )
    infile.close()
    return h

def fetch_zcr_rep(instr):
    h = []
    if instr not in ["guitar", "clarinet", "flute", "saxophone", "violin"]:
        print("invalid instrument")
        return ["nope"]
    infile = open("reps/" + instr + "_zcr.txt", 'r')
    for line in infile:
        h.append( float(line.strip()) )
    infile.close()
    return h
