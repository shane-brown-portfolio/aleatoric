# Define all print functions for verbose and debugging functionality

def print_song_settings(root_note, tempo, scale):
    """Print information about the generated key and tempo."""

    print(f"Key MIDI Note: {root_note}")
    print(f"Tempo: {tempo} BPM")
    print(f"Scale: {scale}")


def print_song_structure(structure, labels, assignments, scale, build_progression):
    """
    Print song structure information including assigned
    chord loops and generated progressions.
    """

    print("\nSong Structure:", structure)

    print("\nAssignments:")
    for label, loop in assignments.items():
        print(f"{label}: {loop}")

    print("\nProgressions:")
    for label, loop in assignments.items():
        progression = build_progression(scale, loop)
        print(f"{label}: {progression}")


def print_generation_results(song_progression, melody, audio):
    """Print generated musical content."""

    print("\nSong Chords:")
    for index, chord in enumerate(song_progression):
        print(index + 1, chord)

    print(f"\nGenerated {len(melody)} melody notes (show first 20):")
    print(melody[:20])

    print(f"\nGenerated {len(audio)} audio samples...")


def print_bass_results(bass_line):
    """Print generated bass notes."""

    print("\nBass Line:")
    print(bass_line)


def print_harmony_results(harmony):
    """Print generated harmony notes."""

    print(f"\nGenerated {len(harmony)} harmony notes (show first 20):")
    print(harmony[:20])