import numpy as np
import pygame
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def generate_better_violin(freq=440, duration=1.0, sample_rate=44100):
    """
    Synthesize a violin-like tone with improved realism using additive synthesis,
    vibrato, a detailed ADSR envelope, and a filtered noise component to mimic bow noise.

    Parameters:
        freq (float): Fundamental frequency in Hz.
        duration (float): Duration of the note in seconds.
        sample_rate (int): Samples per second.

    Returns:
        numpy.ndarray: The synthesized waveform normalized to the range [-1, 1].
    """
    # Create time vector
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # --- ADSR Envelope ---
    # Violin sounds have a smooth onset and a gradual release.
    attack_time  = 0.2   # seconds
    decay_time   = 0.2   # seconds
    sustain_level = 0.8  # amplitude (relative)
    release_time = 0.4   # seconds
    sustain_time = duration - (attack_time + decay_time + release_time)
    if sustain_time < 0:
        sustain_time = 0

    env_attack  = np.linspace(0, 1, int(attack_time * sample_rate))
    env_decay   = np.linspace(1, sustain_level, int(decay_time * sample_rate))
    env_sustain = np.full(int(sustain_time * sample_rate), sustain_level)
    env_release = np.linspace(sustain_level, 0, int(release_time * sample_rate))
    envelope = np.concatenate((env_attack, env_decay, env_sustain, env_release))
    # Ensure envelope has the correct length
    if len(envelope) < len(t):
        envelope = np.pad(envelope, (0, len(t)-len(envelope)), 'constant')
    else:
        envelope = envelope[:len(t)]

    # --- Vibrato ---
    vibrato_rate = 6.0      # Hz (typical for violin vibrato)
    vibrato_depth = 0.015   # Fractional frequency deviation (~1.5%)

    # --- Sum of Partials ---
    note = np.zeros_like(t)
    num_partials = 12  # More harmonics add richness to the tone

    for n in range(1, num_partials + 1):
        # Introduce a slight detuning per harmonic (±0.1%)
        detune = 1 + np.random.uniform(-0.001, 0.001)
        harmonic_freq = freq * n * detune

        # Each partial gets a random phase offset for natural variation
        phase_offset = np.random.uniform(0, 2 * np.pi)

        # Apply vibrato to the instantaneous frequency of the partial
        inst_freq = harmonic_freq * (1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t + phase_offset))
        # Integrate frequency to obtain the instantaneous phase
        phase = 2 * np.pi * np.cumsum(inst_freq) / sample_rate

        # Amplitude roll-off: higher harmonics are less intense.
        # The exponent here controls how quickly the amplitude falls off.
        amplitude = (1 / n) ** 0.8

        # Slow amplitude modulation to simulate subtle bow pressure variations
        amplitude_mod = 1 + 0.05 * np.sin(2 * np.pi * 0.5 * t + phase_offset)

        note += amplitude * amplitude_mod * np.sin(phase)

    # --- Bow Noise Component ---
    # A small amount of filtered noise can emulate the friction noise of the bow.
    noise = np.random.randn(len(t))
    # Use a simple Butterworth low-pass filter to smooth the noise
    b, a = butter(2, 0.1)  # 2nd-order filter with a normalized cutoff
    filtered_noise = lfilter(b, a, noise)
    noise_amplitude = 0.04  # Adjust to taste
    note += noise_amplitude * filtered_noise

    # --- Final Processing ---
    # Apply the ADSR envelope to shape the note
    note *= envelope
    # Normalize to avoid clipping
    note /= np.max(np.abs(note))
    
    return note

def main():
    sample_rate = 44100
    duration = 1.0   # seconds
    freq = 440       # A4
    
    # Generate the improved violin note
    violin_wave = generate_better_violin(freq, duration, sample_rate)
    
    # Convert the waveform to 16-bit PCM
    buffer = np.int16(violin_wave * 32767)
    
    # Initialize pygame mixer and play the sound
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.sndarray.make_sound(buffer)
    sound.play()
    pygame.time.wait(int(duration * 1000))
    
    # Plot the waveform for visualization
    plt.figure(figsize=(10, 4))
    plt.plot(violin_wave, lw=0.8)
    plt.title("Improved Violin Synthesis Waveform")
    plt.xlabel("Sample Number")
    plt.ylabel("Normalized Amplitude")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
