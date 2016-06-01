Thomas Bertschinger and Sanders McMillan
CS 328: Computational Models of Cognition


Our code is organized into several modules:
    audio_utils        : contains utility functions for reading wav files,
                         graphing signals and spectra, etc.
    audio_processing   : contains most of the code for extracting audio features
                         such as spectral centroid, spectral flux, etc.
    representation     : used to loop through every audio file and use the functions
                         in audio_processing to create representations, and then
                         stores these in text files in the directory 'reps/'
    prototype          : functions to classify signals based on their representations
                         using prototype models
    neural_net         : functions to classify signals based on their representations
                         using a neural network

We stored several audio files in an archive "audio_files.tgz"; because all the
files together are several hundred megabytes, we did not upload every file.
However, the representation information for all 3411 audio files is included. 
