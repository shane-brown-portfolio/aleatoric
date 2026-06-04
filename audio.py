import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
from music import note_to_frequency

# Define constants for audio generation and playback

SAMPLE_RATE = 48000
MAX_AMPLITUDE = 0.5


# Define all functions containing audio-specific functionality

def eighth_note_duration(tempo):
    """Calculate the duration of an eighth note in seconds."""
    quarter_note_duration = 60 / tempo
    return quarter_note_duration / 2


def generate_sawtooth(frequency, duration):
    """
    Generate a sawtooth waveform for a single note.
    Return a numpy array of audio samples.
    """
    sample_count = int(duration * SAMPLE_RATE)
    samples = np.arange(sample_count)

    waveform = (2 * ((samples * frequency / SAMPLE_RATE) % 1)) - 1

    return waveform * MAX_AMPLITUDE


def generate_song_audio(melody, tempo):
    """Generate audio samples for the entire melody."""
    
    note_duration = eighth_note_duration(tempo)
    
    audio_segments = []
    for note in melody:
        frequency = note_to_frequency(note)
        segment = generate_sawtooth(frequency, note_duration)
        audio_segments.append(segment)

    return np.concatenate(audio_segments)


def generate_bass_audio(bass_line, tempo):
    """Generate bass audio using one note per measure."""
    measure_duration = eighth_note_duration(tempo) * 8    # 8 beats per measure

    audio_segments = []
    for note in bass_line:
        frequency = note_to_frequency(note)
        segment = generate_sawtooth(frequency, measure_duration)
        audio_segments.append(segment)

    return np.concatenate(audio_segments)


def normalize_audio(audio):
    """Normalize audio to prevent clipping."""
    peak = np.max(np.abs(audio))

    if peak == 0:
        return audio

    return audio / peak


def write_wav(filename, audio):
    """Write audio data to a WAV file."""
    audio_16bit = np.int16(audio * 32767)
    write(filename, SAMPLE_RATE, audio_16bit)


def play_audio(audio):
    """Play generated audio through speakers."""
    sd.play(audio, SAMPLE_RATE)
    sd.wait()


def mix_audio_tracks(track_a, track_b):
    """Mix two audio tracks together."""
    min_length = min(len(track_a), len(track_b))
    return track_a[:min_length] + track_b[:min_length]