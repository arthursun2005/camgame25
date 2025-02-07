import numpy as np
import pygame
import matplotlib.pyplot as plt

# pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

sample_rate = 44100
secs = 2
FREQ = 440

sfreqs = np.fft.fftfreq(sample_rate * secs, 1.0 / sample_rate)

n = len(sfreqs)
freqs = np.zeros(n)

us = []
for i in range(20):
    us.append((FREQ * (i + 1) * (1.0 + np.random.rand() * 0.01), 0.5 ** i))

for i in range(n):
    for f, k in us:
        freqs[i] += np.exp(-(f - abs(sfreqs[i])) ** 2 * 5.0) * sample_rate * k

buffer = np.real(np.fft.ifft(freqs))

g = np.arange(len(buffer)) / len(buffer)
buffer = buffer * np.exp(-g * 8.0)

buffer /= np.max(abs(buffer))
buffer = np.array(np.clip(buffer, -1.0, 1.0) * (1 << 15), dtype=np.int16)

# print(buffer)
#

sound = pygame.sndarray.make_sound(buffer)
sound.play()

plt.plot(buffer)
plt.show()

# x = np.stack([buffer, buffer], axis=1)
# print(x.shape)

pygame.time.wait(secs * 1000)
