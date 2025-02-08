import numpy as np
import pygame
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def bandpass_filter(data, lowcut, highcut, fs, order=2):
    """Simple bandpass filter using a Butterworth design."""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

def generate_trumpet_note(freq=440, duration=2.0, sample_rate=44100):
    """
    Synthesize a trumpet-like note using additive synthesis with harmonics,
    a fast ADSR envelope, vibrato, and a filtered noise burst for a lip-buzz attack.
    
    Parameters:
        freq (float): Fundamental frequency in Hz.
        duration (float): Duration of the note in seconds.
        sample_rate (int): Sampling rate in samples per second.
        
    Returns:
        numpy.ndarray: The synthesized trumpet waveform (normalized to [-1, 1]).
    """
    # Time vector
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # --- ADSR Envelope ---
    # Trumpet notes have a very fast attack with a brief burst of energy.
    attack_time  = 0.05   # 50 ms attack
    decay_time   = 0.1    # 100 ms decay to sustain
    sustain_level = 0.8   # sustain level (relative amplitude)
    release_time = 0.3    # 300 ms release
    sustain_time = duration - (attack_time + decay_time + release_time)
    if sustain_time < 0:
        sustain_time = 0
    
    env_attack  = np.linspace(0, 1, int(attack_time * sample_rate))
    env_decay   = np.linspace(1, sustain_level, int(decay_time * sample_rate))
    env_sustain = np.full(int(sustain_time * sample_rate), sustain_level)
    env_release = np.linspace(sustain_level, 0, int(release_time * sample_rate))
    envelope = np.concatenate((env_attack, env_decay, env_sustain, env_release))
    if len(envelope) < len(t):
        envelope = np.pad(envelope, (0, len(t)-len(envelope)), 'constant')
    else:
        envelope = envelope[:len(t)]
    
    # --- Vibrato ---
    vibrato_rate = 4.0      # Hz
    vibrato_depth = 0.005   # very slight modulation
    
    # --- Additive Synthesis of Harmonics ---
    note = np.zeros_like(t)
    num_partials = 10  # More partials yield a brighter sound
    
    for n in range(1, num_partials + 1):
        # Each harmonic gets a small random phase offset for natural variation.
        phase_offset = np.random.uniform(0, 2*np.pi)
        # Optionally add an almost-negligible detuning (trumpets are tight in pitch)
        detune = 1 + np.random.uniform(-0.0005, 0.0005)
        harmonic_freq = freq * n * detune
        
        # Apply a slight vibrato to each harmonic.
        inst_freq = harmonic_freq * (1 + vibrato_depth * np.sin(2*np.pi * vibrato_rate * t + phase_offset))
        # Integrate the instantaneous frequency to form the phase.
        phase = 2*np.pi * np.cumsum(inst_freq) / sample_rate
        
        # For a trumpet, higher harmonics remain relatively strong.
        amplitude = 1 / (n ** 0.5)  # gentle roll-off (half-power)
        
        note += amplitude * np.sin(phase + phase_offset)
    
    # --- Lip Buzz Noise Burst ---
    # A very short burst of band–passed noise simulates the initial lip buzz.
    noise = np.random.randn(len(t))
    # Pass noise through a bandpass filter centered in the mid-range (~800-2000 Hz)
    filtered_noise = bandpass_filter(noise, 800, 2000, sample_rate, order=2)
    # Create a short envelope for the noise (lasting about 50 ms)
    noise_env = np.concatenate((np.linspace(1, 0, int(0.05 * sample_rate)),
                                np.zeros(len(t) - int(0.05 * sample_rate))))
    noise_burst = filtered_noise * noise_env
    noise_amplitude = 0.07  # adjust to taste
    note += noise_amplitude * noise_burst

    # --- Final Processing ---
    note *= envelope
    # Normalize the waveform to [-1, 1]
    note /= np.max(np.abs(note))
    
    return note

def main():
    sample_rate = 44100
    duration = 2.0   # seconds
    freq = 440       # A4 (change as desired)
    
    # Generate the trumpet note
    trumpet_wave = generate_trumpet_note(freq, duration, sample_rate)
    
    # Convert to 16-bit PCM
    buffer = np.int16(trumpet_wave * 32767)
    
    # Initialize pygame mixer and play the sound
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.sndarray.make_sound(buffer)
    sound.play()
    pygame.time.wait(int(duration * 1000))
    
    # Plot the waveform for visualization
    plt.figure(figsize=(10, 4))
    plt.plot(trumpet_wave, lw=0.8)
    plt.title("Synthesized Trumpet Note")
    plt.xlabel("Sample Number")
    plt.ylabel("Normalized Amplitude")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
