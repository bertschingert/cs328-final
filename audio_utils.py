# Thomas Bertschinger and Sanders McMillan
# This file has useful audio code

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

def create_sine_wave(freq, amp, dur):
    dur *= SR
    wave = []
    for i in range(dur):
        wave.append(amp * math.sin(i*freq*2*math.pi*SP))
    return wave

def create_saw_wave(freq, amp, dur):
    dur *= SR
    period = SR / freq
    wave = []
    for i in range(dur):
        wave.append((i%period) / period)
    return wave
