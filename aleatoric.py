import argparse
import random
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd

from debug_output import (
    print_song_settings,
    print_song_structure,
    print_generation_results
)

# Define Constants
MIN_KEY = 57  # A3
MAX_KEY = 69  # A4

MIN_TEMPO = 80
MAX_TEMPO = 160

NOTES_PER_MEASURE = 8

SAMPLE_RATE = 48000
MAX_AMPLITUDE = 0.5

CHORD_LOOPS = [
    ["I", "IV", "ii", "V"],
    ["I", "vi", "ii", "V"],
    ["I", "iii", "IV", "iv"],
    ["I", "V", "ii", "V"],
    ["I", "vi", "IV", "V"],
    ["IV", "I", "vi", "IV"],
    ["I", "V", "vi", "I"],
    ["I", "IV", "iv", "I"],
    ["IV", "V", "I", "I"],
    ["vi", "IV", "I", "V"],
]

ROMAN_TO_DEGREE = {"I": 0, "ii": 1, "iii": 2, "IV": 3, "iv": 3, "V": 4, "vi": 5}

SONG_STRUCTURES = ["AABB/CC", "ABAB/CD", "AB/CDDD"]

def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Generate aleatoric music."
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Write generated audio to WAV file instead of playing."
    )

    parser.add_argument(
        "--tempo",
        type=int,
        default=120,
        help="Set the tempo (BPM)."
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display detailed song generation information."
    )

    return parser.parse_args()

def note_to_frequency(note_number):
    """
    Convert MIDI note number to frequency.
    Uses A4 (440Hz) as reference note.
    """
    return 440.0 * (2 ** ((note_number - 69) / 12))

def generate_sawtooth(frequency, duration):
    """
    Generate a sawtooth waveform for a single note.
    Return a numpy array of audio samples.
    """
    sample_count = int(duration * SAMPLE_RATE)
    samples = np.arange(sample_count)

    waveform = (2 * ((samples * frequency / SAMPLE_RATE) % 1)) - 1

    return waveform * MAX_AMPLITUDE


def build_major_scale(root_note):
    """
    Builds a major scale based on the given root note (MIDI note number).
    Return major scale notes as MIDI note numbers.
    """
    intervals = [0, 2, 4, 5, 7, 9, 11]
    scale = []

    for interval in intervals:
        scale.append(root_note + interval)

    return scale

def random_key():
    """Generate a random MIDI note number within the specified range."""
    return random.randint(MIN_KEY, MAX_KEY)

def random_tempo():
    """Generate a random tempo within the specified range."""
    return random.randint(MIN_TEMPO, MAX_TEMPO)

def eighth_note_duration(tempo):
    """Calculate the duration of an eighth note in seconds."""
    quarter_note_duration = 60 / tempo
    return quarter_note_duration / 2

def random_song_structure():
    """Select a random song structure from the predefined list."""
    return random.choice(SONG_STRUCTURES)

def get_structure_labels(structure):
    """Extract labels from the song structure string."""
    labels = []

    for char in structure:
        # Add each alphabet character to the list
        if char.isalpha():
            labels.append(char)

    return labels

def assign_loops_to_labels(labels):
    """
    Assign loops to labels based on the unique alphabet characters in the structure.
    Return a dictionary mapping each label to its corresponding loop.
    """
    # Get unique labels from song structure
    unique_labels = sorted(set(labels))

    # Shuffle the available loops to ensure randomness
    available_loops = CHORD_LOOPS.copy()
    random.shuffle(available_loops)

    # Assign each label to a loop until all labels are assigned
    assignments = {}
    for label in unique_labels:
        assignments[label] = available_loops.pop()

    return assignments

def build_chord(scale, roman):
    """
    Build a triad by selecting the root, third, and fifth scale degrees relative
    to the chord root. Return a list of notes for the chord.
    """
    # Define Roman numeral to degree mapping
    root_index = ROMAN_TO_DEGREE[roman]
    third_index = root_index + 2
    fifth_index = root_index + 4

    root = scale[root_index]
    third = scale[third_index % 7]
    fifth = scale[fifth_index % 7]

    if third <= root:
        third += 12

    if fifth <= root:
        fifth += 12

    return [root, third, fifth]

def build_progression(scale, loop):
    """
    Build a progression of chords based on the loop.
    Return a list of chords for the progression.
    """
    progression = []

    for roman in loop:
        progression.append(build_chord(scale, roman))

    return progression

def build_song_progression(labels, assignments, scale):
    """
    Build a song progression based on the labels and assignments.
    Return a list of all the chords for the song.
    """
    song = []

    for label in labels:
        loop = assignments[label]
        progression = build_progression(scale, loop)
        song.extend(progression)

    return song


def choose_melody_note(chord, scale):
    """
    Choose a random note from the given chord or a non-chord note if it's not present.
    Return the chosen note.
    """
    val = random.random()

    # 80% chord tones, 20% non-chord scale tones
    if val < 0.8:
        return random.choice(chord)

    non_chord_notes = []

    for note in scale:
        if note not in chord:
            non_chord_notes.append(note)

    return random.choice(non_chord_notes)


def generate_melody(song_progression, scale):
    """
    Generate an eighth-note melody over the entire song.
    Each chord contributes NOTES_PER_MEASURE melody notes.
    """
    melody = []

    for chord in song_progression:
        for _ in range(NOTES_PER_MEASURE):
            note = choose_melody_note(chord, scale)
            melody.append(note)

    return melody

def generate_song_audio(melody, tempo):
    """Generate audio samples for the entire melody."""
    
    note_duration = eighth_note_duration(tempo)
    
    audio_segments = []
    for note in melody:
        frequency = note_to_frequency(note)
        segment = generate_sawtooth(frequency, note_duration)
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

def main():
    args = parse_args()

    print("Aleatoric Music Generator", end=" - ")

    if args.output:
        print(f"Output File: {args.output}\n")
    else:
        print("Playback Mode\n")
    
    if args.tempo:
        tempo = args.tempo
    else:
        random_tempo()
    
    root_note = random_key()
    scale = build_major_scale(root_note)

    if args.verbose:
        print_song_settings(root_note, tempo, scale)

    structure = random_song_structure()
    labels = get_structure_labels(structure)
    assignments = assign_loops_to_labels(labels)

    if args.verbose:
        print_song_structure(structure, labels, assignments,
                             scale, build_progression)
    
    song_progression = build_song_progression(labels, assignments, scale)
    melody = generate_melody(song_progression, scale)
    audio = generate_song_audio(melody, tempo)
    audio = normalize_audio(audio)

    if args.verbose:
        print_generation_results(song_progression, melody, audio)

    if args.output:
        write_wav(args.output, audio)
        print(f"Wrote audio to {args.output}")
    else:
        print("Playing audio...")
        play_audio(audio)

if __name__ == "__main__":
    main()