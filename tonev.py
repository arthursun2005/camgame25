import numpy as np
import pygame
import matplotlib.pyplot as plt

def generate_violin_note(freq=440, duration=2.0, sample_rate=44100):
    """
    Synthesize a violin-like note by summing sinusoids with vibrato and an ADSR envelope.
    
    Parameters:
      freq        : Fundamental frequency (Hz)
      duration    : Duration of the note (seconds)
      sample_rate : Samples per second
      
    Returns:
      note        : A numpy array of the synthesized note (normalized to -1..1)
    """
    # Time axis
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    note = np.zeros_like(t)
    
    # === Vibrato parameters ===
    vibrato_rate = 5.0      # Vibrato frequency in Hz
    vibrato_depth = 0.005   # Vibrato depth (fractional frequency variation; about 0.5%)
    
    # === ADSR Envelope Parameters for Violin ===
    # Violin notes have a slower attack and release than piano notes.
    attack_time  = 0.15     # 150 ms attack
    decay_time   = 0.1      # 100 ms decay to sustain
    sustain_level = 0.8     # Sustain level (80% of peak)
    release_time = 0.3      # 300 ms release
    sustain_time = duration - (attack_time + decay_time + release_time)
    if sustain_time < 0:
        sustain_time = 0

    envelope = np.zeros_like(t)
    attack_samples  = int(attack_time * sample_rate)
    decay_samples   = int(decay_time * sample_rate)
    sustain_samples = int(sustain_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    
    # Attack: ramp from 0 to 1
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay: ramp from 1 to sustain_level
    envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain_level, decay_samples)
    # Sustain: hold sustain_level
    envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain_level
    # Release: ramp from sustain_level to 0
    envelope[attack_samples+decay_samples+sustain_samples:
             attack_samples+decay_samples+sustain_samples+release_samples] = np.linspace(sustain_level, 0, release_samples)
    
    # === Partial structure for violin timbre ===
    # Compared to piano, violin partials tend to decay less aggressively, allowing for a sustained tone.
    partials = [
        (1, 1.0, 0.5),   # fundamental
        (2, 0.9, 0.7),   # first overtone
        (3, 0.7, 0.9),
        (4, 0.5, 1.1),
        (5, 0.3, 1.3),
        (6, 0.2, 1.5)
    ]
    
    for mult, amp, decay in partials:
        # Each partial’s base frequency
        partial_freq = freq * mult
        
        # Apply vibrato: modulate the frequency slowly in time.
        # The instantaneous frequency is adjusted by a sine wave.
        inst_freq = partial_freq * (1 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t))
        
        # Integrate the instantaneous frequency to get the phase.
        phase = 2 * np.pi * np.cumsum(inst_freq) / sample_rate
        
        # Each partial is a sine wave with a gentle exponential decay.
        note += amp * np.sin(phase) * np.exp(-decay * t)
    
    # Apply the ADSR envelope
    note *= envelope
    
    # Normalize to ensure the amplitude is in the -1 to 1 range
    note /= np.max(np.abs(note))
    return note

def main():
    sample_rate = 44100
    duration = 2.0  # seconds
    freq = 440      # A4
    
    # Generate the synthesized violin note.
    violin_note = generate_violin_note(freq, duration, sample_rate)
    
    # Convert the waveform to 16-bit PCM format.
    buffer = np.int16(violin_note * 32767)
    
    # Initialize the pygame mixer and play the note.
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
    sound = pygame.sndarray.make_sound(buffer)
    sound.play()
    pygame.time.wait(int(duration * 1000))
    
    # Plot the waveform for visualization.
    plt.plot(buffer)
    plt.title("Synthesized Violin Note")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.show()

if __name__ == "__main__":
    main()
