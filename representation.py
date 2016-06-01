# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# representation.py

import audio_utils as au
import audio_processing as ap

def get_reps():
    instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
    lens = [71, 770, 781, 621, 901]
    for instr in instrs:
        print(instr)
        fnames = open("audio_files/" + instr + ".txt", 'r')
        outzcr = open("reps/" + instr + "_zcr.txt", 'w')
        outcen = open("reps/" + instr + "_centroid.txt", 'w')
        outhar = open("reps/" + instr + "_harmonics.txt", 'w')
        outrat = open("reps/" + instr + "_ratio.txt", 'w')
        outflu = open("reps/" + instr + "_flux.txt", 'w')
        i = 0
        l = sum(1 for line in fnames)
        fnames.seek(0)
        print(l)
        p0 = -1
        for line in fnames:
            wave = au.read_wav_mono(line.strip())
            h = harmonic_representation(wave)
            z = ap.zero_crossing_rate(wave)
            c = ap.spectral_centroid(wave)
            r = c / z
            f = ap.spectral_flux(wave)
            outzcr.write(str(z) + '\n')
            outcen.write(str(c) + '\n')
            outrat.write(str(r) + '\n')
            outhar.write(str(h) + '\n')
            outflu.write(str(f) + '\n')
            p = int( i * 100 / l )
            if p > p0:
                print(str(p) + "% done with " + instr, end = '\r')
                p0 = p
            i += 1
        print("all ")
        fnames.close()
        out_zcr.close()
        out_cen.close()
        out_rat.close()
        out_har.close()
        out_flu.close()

def main():
    get_reps()

if __name__ == '__main__':
    main()
