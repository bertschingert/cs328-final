# Thomas Bertschinger and Sanders McMillan
# CS 328 Final Project
# representation.py

import audio_utils as au
import audio_processing as ap

def freq(x):
    """
    helper function for get_funds()
    """
    return {
        'C': 65.41,
        'Cs': 69.30,
        'D': 73.42,
        'Ds': 77.78,
        'E': 82.41,
        'F': 87.31,
        'Fs': 92.50,
        'G': 98.00,
        'Gs': 103.83,
        'A': 110,
        'As': 116.54,
        'B': 123.47,
    }[x]

def get_funds():
    """
    gets the fundamental frequency for each audio file
    """
    instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
    for instr in instrs:
        fnames = open("audio_files/" + instr + ".txt", 'r')
        outfile = open("tmpreps/" + instr + "_funds.txt", 'w')
        for line in fnames:
            s0 = line.split('/')
            s1 = s0[2]
            s2 = s1.split('_')
            s3 = s2[1]
            l = len(s3)
            octave = int( s3[l-1] )
            note = s3[:l-1]
            f = freq(note)
            f = f * 2**(octave - 2)
            outfile.write(str(f) + '\n')
        fnames.close()
        outfile.close()

def normalize_flux():
    """
    used to normalize the spectral flux values
    and store the result in a separate text file
    """
    instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
    lens = [71, 770, 781, 621, 901]
    for instr in instrs:
        print(instr)
        infile = open("reps/" + instr + "_flux.txt", 'r')
        outfile = open("reps/" + instr + "_nflux.txt", 'w')
        for line in infile:
            ps = line.split(',')
            fs = []
            for p in ps:
                fs.append(float(p.strip()))
            m = max(fs)
            for i in range(len(fs)):
                outfile.write(str(fs[i] / m))
                if i < len(fs) - 1:
                    outfile.write(', ')
            outfile.write('\n')
        infile.close()
        outfile.close()

def get_reps():
    """
    CAREFUL
    Running this function will overwrite the text files in reps/
    which contains essential data.
    Consider running get_example_reps() instead.
    -------------------------------------------------------------
    This function gets all of the representation information for every audio file
    and stores it in text files in the directory reps/
    the information computed is:
        1) zero-crossing rate
        2) spectral centroid
        3) ratio of zcr to centroid
        4) harmonic content
        5) spectral flux
    """
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
            h = ap.harmonic_representation(wave)
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
        outzcr.close()
        outcen.close()
        outrat.close()
        outhar.close()
        outflu.close()

def get_example_reps():
    """
    This function is (almost) the same as get_reps
    note that it that it stores
    the information in the directory example_reps/
    in order to avoid overwriting the directory reps/
                                    (which contains the essential info)
    """

    fnames = open("example_audio_filenames.txt", 'r')
    outzcr = open("example_reps/zcr.txt", 'w')
    outcen = open("example_reps/centroid.txt", 'w')
    outhar = open("example_reps/harmonics.txt", 'w')
    outrat = open("example_reps/ratio.txt", 'w')
    outflu = open("example_reps/flux.txt", 'w')

    for line in fnames:
        print("getting representation for")
        print(line.strip())
        wave = au.read_wav_mono(line.strip())
        h = ap.harmonic_representation(wave)
        z = ap.zero_crossing_rate(wave)
        c = ap.spectral_centroid(wave)
        r = c / z
        f = ap.spectral_flux(wave)
        outzcr.write(str(z) + '\n')
        outcen.write(str(c) + '\n')
        outrat.write(str(r) + '\n')
        outhar.write(str(h) + '\n')
        outflu.write(str(f) + '\n')

    outzcr.close()
    outcen.close()
    outrat.close()
    outhar.close()
    outflu.close()

    fnames.close()

    print("stored representations in the directory \'example_reps/\'")

def main():
    print("representation.py")
    print("This file contains the function to get the representations")
    print("for each of our 3411 audio files. It stores this information")
    print("in text files in the directory \'reps/\'.")
    answer = input("Would you like to run an example of get_reps()? y/n ")
    if answer == 'y' or answer == 'Y':
        get_example_reps()

if __name__ == '__main__':
    main()
