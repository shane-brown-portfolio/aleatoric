import random

# Define constants for chord loops and melody

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

ROMAN_TO_DEGREE = {"I": 0, "ii": 1, "iii": 2, "IV": 3, "iv": 3, "V": 4, "vi": 5}
SONG_STRUCTURES = ["AABB/CC", "ABAB/CD", "AB/CDDD"]
NOTES_PER_MEASURE = 8


# Define all functions containing musical-specific functionality
# This includes note generation, chord progression building, melody creation, etc.

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
        chord_tones = []
        for note in chord:
            # Move chord notes back into the original scale octave
            while note > scale[-1]:
                note -= 12

            chord_tones.append(note)

        return random.choice(chord_tones)

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


def generate_bass_line(song_progression):
    """
    Generate one bass note per measure using the root note of each chord.
    Each bass note is two octaves below the root note.
    """
    bass_line = []

    for chord in song_progression:
        root = chord[0]
        bass_note = root - 24

        bass_line.append(bass_note)

    return bass_line


def generate_harmony(song_progression, melody):
    """
    Generate harmony notes by selecting the closest chord note below each melody note.
    """
    harmony = []
    melody_index = 0

    for chord in song_progression:
        chord_tones = []

        for note in chord:
            normalized = note

            # Convert chord tones back into a single octave for note comparisons
            while normalized > chord[0] + 11:
                normalized -= 12

            chord_tones.append(normalized)

        for _ in range(NOTES_PER_MEASURE):
            melody_note = melody[melody_index]
            lower_chord_tones = []

            # Find all chord tones that are lower than the melody note
            for chord_note in chord_tones:
                if chord_note < melody_note:
                    lower_chord_tones.append(chord_note)

            if lower_chord_tones:
                # Highest chord note below melody
                harmony_note = max(lower_chord_tones)
            else:
                # Fallback to lowest note in chord if all notes are higher than melody
                harmony_note = min(chord_tones)

            harmony.append(harmony_note)
            melody_index += 1

    return harmony