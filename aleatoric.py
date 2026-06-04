import argparse

import music
import audio
from debug_output import (
    print_song_settings,
    print_song_structure,
    print_generation_results
)

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
        help="Set the tempo (BPM). If omitted, a random tempo is used."
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display detailed song generation information."
    )

    parser.add_argument(
        "--bass",
        action="store_true",
        help="Add a bass line two octaves below the chord root."
    )

    parser.add_argument(
        "--harmony",
        action="store_true",
        help="Add harmony using the closest chord tone below the melody."
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("Aleatoric Music Generator", end=" - ")

    if args.output:
        print(f"Output File: {args.output}\n")
    else:
        print("Playback Mode\n")
    
    root_note = music.random_key()
    
    if args.tempo is not None:
        if not (80 <= args.tempo <= 160):
            raise ValueError("Tempo must be between 80 and 160 BPM.")
        tempo = args.tempo
    else:
        tempo = music.random_tempo()
    
    scale = music.build_major_scale(root_note)

    if args.verbose:
        print_song_settings(root_note, tempo, scale)

    structure = music.random_song_structure()
    labels = music.get_structure_labels(structure)
    assignments = music.assign_loops_to_labels(labels)

    if args.verbose:
        print_song_structure(structure, labels, assignments,
                             scale, music.build_progression)
    
    song_progression = music.build_song_progression(labels, assignments, scale)
    melody = music.generate_melody(song_progression, scale)
    audio_data = audio.generate_song_audio(melody, tempo)

    if args.bass:
        bass_line = music.generate_bass_line(song_progression)
        bass_audio = audio.generate_bass_audio(bass_line, tempo)
        audio_data = audio.mix_audio_tracks(audio_data, bass_audio)
    
    if args.harmony:
        harmony = music.generate_harmony(song_progression, melody)
        harmony_audio = audio.generate_song_audio(harmony, tempo)
        audio_data = audio.mix_audio_tracks(audio_data, harmony_audio)

    audio_data = audio.normalize_audio(audio_data)

    if args.verbose:
        print_generation_results(song_progression, melody, audio_data)

    if args.output:
        audio.write_wav(args.output, audio_data)
        print(f"Wrote audio to {args.output}")
    else:
        print("Playing audio...")
        audio.play_audio(audio_data)


if __name__ == "__main__":
    main()