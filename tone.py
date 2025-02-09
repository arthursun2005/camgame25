import numpy as np
import pygame
from scipy.signal import butter, lfilter

SAMPLE_RATE = 44100

tunes = {
    'mega': [
        ('D3', 1, 1/4),
        ('D3', 1, 1/4),
        ('D4', 1, 1/2),
        ('A4', 1, 3/4),
        ('A4b', 1, 1/2),
        ('G3', 1, 1/2),
        ('F3', 1, 1/2),
        ('D3', 1, 1/4),
        ('F3', 1, 1/4),
        ('G3', 1, 1/4),
    ]
}

INSTS = {
    'piano': (0.8, 0.0, 2, 1, 1, None),
    'violin': (0.05, 0.01, 1, 0.3, 8, (2, 0.1)),
    'flute': (1.2, 0.01, 1, 0.3, 5, (2, 0.1)),
}

def note_to_freq(note):
    # A4 is 440
    u = {
        'A': 0,
        'B': 2,
        'C': 3,
        'D': 5,
        'E': 7,
        'F': 8,
        'G': 10,
    }
    r = u[note[0]]
    if len(note) >= 3 and note[2] == 'b': r -= 1
    if len(note) >= 3 and note[2] == '#': r += 1
    return 2 ** (r / 12 + int(note[1]) - 4.0 + 8.78136)

def generate_tone(freq, duration, inst, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, 1, int(sample_rate * duration), endpoint=False)
    note = np.zeros_like(t)
    P, W, D, U, S, B = INSTS[inst]
    for mult in range(1, 13):
        amp = np.exp(-(mult - 1) * P)
        decay = mult * U + D

        inst_freq = freq * mult * (1 + W * np.sin(2 * np.pi * 1.0 * t + np.random.uniform(0, 2 * np.pi)))
        phase = 2 * np.pi * np.cumsum(inst_freq) / sample_rate
        note += amp * np.sin(phase) * np.exp(-decay * t)

    noise_duration = min(0.02 * S * duration, duration)
    noise_samples = int(noise_duration * sample_rate)
    noise_envelope = np.linspace(1, 0, noise_samples)
    note[:noise_samples] += 0.01 * noise_envelope * np.random.randn(noise_samples)

    if B:
        b, a = butter(*B)
        note += 0.006 * lfilter(b, a, np.random.randn(len(t)))

    attack_time = min(0.01 * S * duration, duration)
    attack_samples = int(attack_time * sample_rate)
    attack_env = np.linspace(0, 1, attack_samples)
    note[:attack_samples] *= attack_env

    note /= np.max(np.abs(note))
    return note

# second = second
def generate_tune(tune, inst, sec=1, sample_rate=SAMPLE_RATE):
    notes = []
    for note, dur, space in tune:
        freq = note_to_freq(note)
        n = int(space * sec * sample_rate)
        tone = generate_tone(freq, dur * space * sec * 0.8, inst, sample_rate)
        g = np.zeros(n)
        g[:len(tone)] = tone
        notes.append(g)
    return np.concat(notes)

if __name__ == '__main__':
    print(note_to_freq('A4'))

    for i in INSTS:
        buffer = np.int16(generate_tune(tunes['mega'], i, 0.6) * (2**15 - 1))
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
        sound = pygame.sndarray.make_sound(buffer)
        sound.play()
        pygame.time.wait(int(len(buffer) / SAMPLE_RATE * 1000))

    duration = 2
    for i in INSTS:
        buffer = np.int16(generate_tone(440, duration, i) * (2**15 - 1))
        sound = pygame.sndarray.make_sound(buffer)
        sound.play()
        pygame.time.wait(int(duration * 1000))
