Thomas Bertschinger and Sanders McMillan
CS 328: Computational Models of Cognition


Our code is organized into several modules:
    audio_utils        : contains utility functions for reading wav files,
                         graphing signals and spectra, etc.
    audio_processing   : contains most of the code for extracting audio features
                         such as spectral centroid, spectral flux, etc.
    representation     : used to loop through every audio file and use the functions
                         in audio_processing to create representations, and then
                         stores these in text files in the directory "reps/"
    prototype          : functions to classify signals based on their representations
                         using prototype models
    neural_net         : functions to classify signals based on their representations
                         using a neural network

We stored several audio files in an archive "audio_files.tgz"; because all the
files together are several hundred megabytes, we did not upload every file.

To test creating representations:
  1) extract the audio files from "audio_files.tgz"
  2) run the file "representation.py". The main
     function in representation.py will compute
     the representations for the included audio files.
  3) The representations will be stored in text files
     in the directory "example_reps/"

The representation information for all 3411 audio files is included
in the directory "reps/"

reps/ is organized into the following types of files:
      [instr] \in {clarinet, flute, guitar, saxophone, violin}
  1) [instr]_centroid.txt
      spectral centroid
  2) [instr]_flux.txt
      spectral flux
  3) [instr]_funds.txt
      fundamental frequencies
  4) [instr]_harmonics.txt
      harmonic representations
  5) [instr]_nflux.txt
      normalized spectral flux
  6) [instr]_ratio.txt
      ratio of spectral centroid to zero-crossing rate
  7) [instr]_zcr.txt
      zero-crossing rate
and corresponding lines of each of these files (for the same instrument)
all refer to the same audio file.

To test the prototype model, run prototype.py. The main function will
provide an example computation.

To test the neural network, run neural_net.py. The main function will
compute an example; more in-depth examples (with graphs of data) can be
found in the notebooks. 
