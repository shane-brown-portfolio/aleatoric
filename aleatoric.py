import argparse
import math
import random

# Define Constants
MIN_KEY = 57  # A3
MAX_KEY = 69  # A4

MIN_TEMPO = 80
MAX_TEMPO = 160

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

SONG_STRUCTURES = [
    "AABB/CC",
    "ABAB/CD",
    "AB/CDDD",
]

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

    return parser.parse_args()

def note_to_frequency(note_number):
    """
    Convert MIDI note number to frequency.
    Uses A4 (440Hz) as reference note.
    """
    return 440.0 * (2 ** ((note_number - 69) / 12))


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

def random_chord_loop():
    """Select a random chord loop from the predefined list."""
    return random.choice(CHORD_LOOPS)

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

def main():
    args = parse_args()

    print("Aleatoric Music Generator", end=" - ")

    if args.output:
        print(f"Output file: {args.output}\n")
    else:
        print("Playback mode\n")
    
    root_note = random_key()
    tempo = random_tempo()
    scale = build_major_scale(root_note)

    print(f"Key MIDI Note: {root_note}")
    print(f"Tempo: {tempo} BPM")

    print("Scale:")
    print(scale)

    loop = random_chord_loop()
    print("Chord Loop:")
    print(loop)

    structure = random_song_structure()
    print("\nSong Structure:", end=' ')
    print(structure)

    labels = get_structure_labels(structure)
    print(labels)

if __name__ == "__main__":
    main()