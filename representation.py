# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# representation.py

import audio_utils as au
import audio_processing as ap

def load_audio_files():
    filenames = open('filenames.txt', 'r')
    guitars = []
    violins = []
    saxophones = []
    for line in filenames:
        if 'guitar' in line:
            print("got guitar =p")
            wave = au.read_wav_mono(line.strip())
            guitars.append(wave)
        if 'saxophone' in line:
            print("got saxophone =p")
            wave = au.read_wav_mono(line.strip())
            saxophones.append(wave)
        if 'violin' in line:
            print("got violin =p")
            wave = au.read_wav_mono(line.strip())
            violins.append(wave)
    return (guitars, violins, saxophones)

def get_harmonic_representations():
    filenames = open('filenames.txt', 'r')
    for line in filenames:
        if 'guitar' in line:
            print("guitar", end=' ')
        if 'saxophone' in line:
            print("saxophone", end=' ')
        if 'violin' in line:
            print("violin", end=' ')

        s = au.read_wav_mono(line.strip())
        h = ap.harmonic_representation(s)
        for i in h:
            print(i, end = ' ')
        print(' ')

def get_zcrs():
    

def main():
    get_harmonic_representations()

if __name__ == '__main__':
    main()
