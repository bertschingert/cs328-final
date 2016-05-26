# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# representation.py

import audio_utils as au

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

def main():
    t = load_audio_files()
    print("guitars: ", len(t[0]))
    print("saxophones: ", len(t[1]))
    print("violins: ", len(t[2]))

if __name__ == '__main__':
    main()
