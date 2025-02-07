import numpy as np
import pygame
import matplotlib.pyplot as plt

def generate_piano_note(freq=440, duration=1.5, sample_rate=44100):
    """
    Synthesize a piano-like note by summing decaying sinusoidal partials.
    
    Parameters:
      freq        : Fundamental frequency (Hz)
      duration    : Duration of the note (seconds)
      sample_rate : Samples per second
      
    Returns:
      note        : A numpy array of the synthesized note (float values between -1 and 1)
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    note = np.zeros_like(t)
    
    # Define partials: each tuple is (partial multiplier, relative amplitude, decay constant)
    # In a real piano, the higher partials typically have lower amplitudes and decay faster.
    partials = [
        (1, 1.00, 3.0),  # Fundamental
        (2, 0.60, 4.0),  # 1st overtone
        (3, 0.40, 5.0),  # 2nd overtone
        (4, 0.30, 6.0),  # 3rd overtone
        (5, 0.20, 7.0)   # 4th overtone
    ]
    
    for mult, amp, decay in partials:
        # Optionally, introduce a tiny amount of inharmonicity (piano strings are not perfect)
        inharmonicity = 1 + 0.001 * (mult ** 2)
        # Each partial is a sine wave with an exponential decay envelope.
        note += amp * np.sin(2 * np.pi * freq * mult * inharmonicity * t) * np.exp(-decay * t)
    
    # Add a short noise burst at the beginning to mimic the hammer strike (transient)
    noise_duration = 0.02  # 20 ms of noise
    noise_samples = int(noise_duration * sample_rate)
    noise_envelope = np.linspace(1, 0, noise_samples)
    note[:noise_samples] += 0.2 * noise_envelope * np.random.randn(noise_samples)
    
    # Apply a quick attack envelope (linear ramp) for a smoother start
    attack_time = 0.01  # 10 ms attack time
    attack_samples = int(attack_time * sample_rate)
    attack_env = np.linspace(0, 1, attack_samples)
    note[:attack_samples] *= attack_env
    
    # Normalize to prevent clipping (values between -1 and 1)
    note /= np.max(np.abs(note))
    
    return note

def main():
    sample_rate = 44100
    duration = 1.5  # seconds
    freq = 392 # A4 (440 Hz)
    
    # Generate the synthesized note
    note = generate_piano_note(freq, duration, sample_rate)
    
    # Convert the note to 16-bit PCM data
    buffer = np.int16(note * 32767)
    
    # Initialize pygame mixer and create a sound object
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.sndarray.make_sound(buffer)
    
    # Play the sound
    sound.play()
    pygame.time.wait(int(duration * 1000))
    
    # Plot the waveform for visualization
    plt.plot(buffer)
    plt.title("Synthesized Piano Note")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.show()

if __name__ == '__main__':
    main()
