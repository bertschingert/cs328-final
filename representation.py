# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# representation.py

import audio_utils as au
import audio_processing as ap
import numpy.fft as fft

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
    # instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
    # lens = [106, 846, 878, 733, 1502]
    instrs = ["saxophone", "violin"]
    lens = [732, 1502]
    for instr in instrs:
        print(instr)
        fnames = open("audio_files/" + instr + ".txt", 'r')
        outfile = open("reps/temp_" + instr + "_zcr.txt", 'w')
        i = 0
        l = sum(1 for line in fnames)
        fnames.seek(0)
        print(l)
        p0 = -1
        for line in fnames:
            line = line.strip()
            wave = au.read_wav_mono(line)
            (start, end) = au.get_good_chunk(wave)
            if start > 0:
                zcr = ap.zero_crossing_rate(wave[start:end])
                outfile.write(str(zcr) + '\n')
                p = int( i * 100 / l )
                if p > p0:
                    print(str(p) + "% done with " + instr, end = '\r')
                    p0 = p
                # print(p)
            i += 1
        print("all ")
        fnames.close()
        outfile.close()

def get_centroids():
        # instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
        # lens = [106, 846, 878, 732, 1502]
        instrs = ["clarinet", "flute", "saxophone", "violin"]
        lens = [846, 878, 732, 1502]
        for instr in instrs:
            print(instr)
            fnames = open("audio_files/" + instr + ".txt", 'r')
            outfile = open("reps/" + instr + "_centroid.txt", 'w')
            log = open("log.txt", 'w')
            i = 0
            l = sum(1 for line in fnames)
            fnames.seek(0)
            print(l)
            p0 = -1
            for line in fnames:
                line = line.strip()
                wave = au.read_wav_mono(line)
                (start, end) = au.get_good_chunk(wave)
                if start > 0:
                    s = fft.rfft(wave[start:end])
                    c = ap.spectral_centroid(s)
                    outfile.write(str(c) + '\n')
                    p = int( i * 100 / l )
                    if p > p0:
                        print(str(p) + "% done with " + instr, end = '\r')
                        p0 = p
                    # print(p)
                else:
                    log.write("skipped " + line + '\n')
                i += 1
            print("all ")
            fnames.close()
            outfile.close()

def get_reps():
            instrs = ["clarinet", "flute", "saxophone", "violin"]
            lens = [846, 878, 732, 1502]
            for instr in instrs:
                print(instr)
                fnames = open("audio_files/" + instr + ".txt", 'r')
                out_zcr= open("tmpreps/" + instr + "_zcr.txt", 'w')
                out_cen= open("tmpreps/" + instr + "_centroid.txt", 'w')
                out_rat= open("tmpreps/" + instr + "_ratio.txt", 'w')
                # log = open("log.txt", 'w')
                i = 0
                l = sum(1 for line in fnames)
                fnames.seek(0)
                print(l)
                p0 = -1
                for line in fnames:
                    wave = au.read_wav_mono(line.strip())
                    s = fft.rfft(wave)
                    c = ap.spectral_centroid(s)
                    out_cen.write(str(c) + '\n')
                    zcr = ap.zero_crossing_rate(wave)
                    out_zcr.write(str(zcr) + '\n')
                    rat = c / zcr
                    out_rat.write(str(rat) + '\n')
                    p = int( i * 100 / l )
                    if p > p0:
                        print(str(p) + "% done with " + instr, end = '\r')
                        p0 = p
                    # print(p)
                    i += 1
                print("all ")
                fnames.close()
                out_zcr.close()
                out_cen.close()
                out_rat.close()

def main():
    get_reps()


if __name__ == '__main__':
    main()
