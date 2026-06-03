import argparse
import math


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate aleatoric music."
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Write generated audio to WAV file instead of playing."
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

def main():
    args = parse_args()

    print("Aleatoric Music Generator")

    if args.output:
        print(f"Output file: {args.output}")
    else:
        print("Playback mode")
    
    root_note = 57  # A3
    scale = build_major_scale(root_note)
    print("Scale:")
    print(scale)

if __name__ == "__main__":
    main()