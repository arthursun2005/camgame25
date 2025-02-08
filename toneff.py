import numpy as np
import pygame
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def generate_flute_note(freq=440, duration=3.0, sample_rate=44100):
    """
    Synthesize a flute-like note using additive synthesis with a few partials,
    gentle vibrato, a smooth ADSR envelope, and a subtle breath noise.
    
    Parameters:
        freq (float): Fundamental frequency in Hz.
        duration (float): Duration of the note in seconds.
        sample_rate (int): Sampling rate (samples per second).
        
    Returns:
        numpy.ndarray: The synthesized waveform (normalized to [-1, 1]).
    """
    # Create time vector.
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # --- ADSR Envelope ---
    # Flute notes typically have a smooth attack, a brief decay to a steady level,
    # and a gentle release.
    attack_time  = 0.1   # 100 ms attack
    decay_time   = 0.1   # 100 ms decay
    sustain_level = 0.9  # sustain level (relative amplitude)
    release_time = 0.3   # 300 ms release
    sustain_time = duration - (attack_time + decay_time + release_time)
    if sustain_time < 0:
        sustain_time = 0

    env_attack  = np.linspace(0, 1, int(attack_time * sample_rate))
    env_decay   = np.linspace(1, sustain_level, int(decay_time * sample_rate))
    env_sustain = np.full(int(sustain_time * sample_rate), sustain_level)
    env_release = np.linspace(sustain_level, 0, int(release_time * sample_rate))
    envelope = np.concatenate((env_attack, env_decay, env_sustain, env_release))
    # Ensure the envelope length matches the time vector length.
    if len(envelope) < len(t):
        envelope = np.pad(envelope, (0, len(t) - len(envelope)), mode='constant')
    else:
        envelope = envelope[:len(t)]
    
    # --- Vibrato ---
    # A gentle vibrato typical for flute performance.
    vibrato_rate = 5.0      # vibrato frequency in Hz
    vibrato_depth = 0.005   # fractional frequency deviation (~0.5%)

    # --- Additive Synthesis ---
    # Flute sound is mostly pure, so we only add a few harmonics.
    note = np.zeros_like(t)
    # Define partials as tuples: (harmonic number, amplitude scaling)
    partials = [
        (1, 1.0),   # fundamental
        (2, 0.3),   # second harmonic (mild)
        (3, 0.1),   # third harmonic (very slight)
        (4, 0.05)   # fourth harmonic (optional, very soft)
    ]
    
    for mult, amp in partials:
        # A random phase offset gives a little natural variation.
        phase_offset = np.random.uniform(0, 2*np.pi)
        harmonic_freq = freq * mult
        # Modulate the harmonic frequency with vibrato.
        inst_freq = harmonic_freq * (1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t + phase_offset))
        # Integrate the instantaneous frequency to get the phase.
        phase = 2 * np.pi * np.cumsum(inst_freq) / sample_rate
        note += amp * np.sin(phase + phase_offset)
    
    # --- Breath Noise ---
    # Flute tone always has a hint of breathiness.
    # Generate a small amount of white noise and filter it gently.
    noise = np.random.randn(len(t)) * 0.02  # noise amplitude is kept low
    # Apply a lowpass filter to smooth the noise (removing harsh high frequencies).
    b, a = butter(2, 0.3)  # 2nd-order Butterworth lowpass with a normalized cutoff frequency of 0.3
    filtered_noise = lfilter(b, a, noise)
    note += filtered_noise
    
    # --- Final Processing ---
    # Apply the ADSR envelope and normalize the output.
    note *= envelope
    note /= np.max(np.abs(note))
    
    return note

def main():
    sample_rate = 44100
    duration = 3.0  # seconds
    freq = 440      # Fundamental frequency (A4)

    # Generate the flute note.
    flute_wave = generate_flute_note(freq, duration, sample_rate)
    
    # Convert to 16-bit PCM for playback.
    buffer = np.int16(flute_wave * 32767)
    
    # Initialize Pygame mixer and play the sound.
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.sndarray.make_sound(buffer)
    sound.play()
    pygame.time.wait(int(duration * 1000))
    
    # Plot the waveform.
    plt.figure(figsize=(10, 4))
    plt.plot(flute_wave, lw=0.8)
    plt.title("Synthesized Flute Note")
    plt.xlabel("Sample Number")
    plt.ylabel("Normalized Amplitude")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
