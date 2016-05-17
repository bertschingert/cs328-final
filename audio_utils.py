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
