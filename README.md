# Aleatoric Music Generator

This project implements an aleatoric music generator that creates simple randomized musical compositions using basic music theory concepts. The program generates a random key, tempo, chord progression, and melody, then synthesizes the result using sawtooth waveforms and either plays the audio directly or writes it to a WAV file.

The generated music consists of:
- A randomly selected major key between A3 and A4 (inclusive)
- A randomly selected tempo between 80 and 160 BPM
- Random chord loops assigned to song sections
- An eighth-note melody generated from the active chord and scale
- Sawtooth waveform synthesis as a mono 48 kHz 16-bit WAV file

The melody generation follows a simple rule:
- **80% probability** → choose a note from the current chord
- **20% probability** → choose another note from the major scale

## Build Instructions

### Requirements
- Python 3.x
- numpy
- scipy
- sounddevice

### Install Dependencies
```
pip install numpy scipy sounddevice
```
Or
```
pip install -r requirements.txt
```

### Run
Generate and play a random song:
```
python3 aleatoric.py
```
The following command-line arguments are available:

| Argument | Description |
| ------------ | ----------- |
| `-v`, `--verbose`  | Display detailed information about the generated song, including scales, chord progressions, and notes. |
| `--tempo` BPM | Use a specific tempo instead of selecting a random tempo. BPM must be between 80 and 160. |
| `--bass` | Add a bass line that plays the root note of each chord two octaves lower for the duration of each measure. |
| `--harmony` | Add a harmony line by playing the closest chord tone below each melody note. |
| `--output` FILE.wav | Write the generated audio to a WAV file instead of only playing it through the speakers. |

Arguments may be combined:
```
python3 aleatoric.py -v --tempo 120 --bass --harmony --output ALEATORIC.wav
```

## Output
After running the program:
- A random song is generated
- Audio is played directly through the speakers by default
- A WAV file is created if `--output` is specified
- Additional generation details are displayed when using `-v` or `--verbose`

## How It Works
This program generates music by combining randomized music theory elements with simple waveform synthesis.

1. **Generate Key and Tempo**
   - A random root note is selected between A3 and A4 and used to construct a major scale.
   - A tempo is either randomly selected between 80 and 160 BPM or specified using the `--tempo` argument.

2. **Generate Song Structure**

   The program randomly selects one of three song structures:
     ```
     AABB/CC
     ABAB/CD
     AB/CDDD
     ```
   Each letter represents a four-chord phrase. Repeated letters reuse the same progression.

3. **Assign Chord Loops and Build Chord Progressions**

   Each unique song section is assigned a randomly selected chord loop from a predefined collection of common chord progressions. No two labels are assigned the same loop.

   Examples include:

     ```
     I IV ii V
     I vi ii V
     vi IV I V
     ```
   Roman numerals are converted into scale degrees and used to construct triads from the generated major scale. The chords contain a root, third, and fifth. The third and fifth may be raised by an octave to maintain proper chord voicing.
   
4. **Generate Melody**

   For every measure:
   - Eight melody notes are generated.
   - Notes are selected from the active chord with a probability of 80%.
   - Otherwise, a non-chord note from the major scale is selected.

   Melody notes are restricted to the original octave of the generated scale.
   
5. **Synthesize Audio**

   Each melody note is converted from a MIDI note number into a frequency using the equal temperament formula with A4 as the reference frequency:
     ```
     frequency = 440 * (2 ** ((note - 69) / 12))
     ```
   A sawtooth waveform is generated for each note and the resulting audio segments are concatenated together to form the final song.

6. **Playback or Export WAV File**
   - Audio is played directly using `sounddevice`.
   - If the `--output` argument is used, the audio is written as a 48 kHz 16-bit mono WAV file using `scipy`.

## How It Went
Overall, the project went well once the song generation logic was established.
I was able to incrementally work through the project by creating a scale from the root note, then building chord progressions and eventually generating melodies from those chords.

One of the more interesting challenges was representing music as MIDI note numbers.
Although this made it straightforward to generate scales, chords, and melodies, additional work was needed to convert these note numbers into frequencies that could be synthesized into audio.

Another challenge was constructing chords near the top of the scale. Initially some chords wrapped back into lower notes, producing unusual voicings.
This was corrected by raising chord tones by an octave when necessary so that the chord tones remained stacked above the root note.

During development, the verbose output mode was very useful because it made it easy to inspect scales, chord assignments, progressions, and generated melodies to verify that the program was following the project requirements correctly. It also allowed me to focus on specific function implementation outputs before moving onto the next task at hand.

## Still To Be Done
While the program successfully generates and synthesizes random songs, there are several possible improvements:
- Add a drum track using white noise by picking a one-measure rhythm to use for every measure in the song
- Improve song generation with rhythmic variation by picking a random note pattern for the verse, and another for the chorus
- Add note name display alongside MIDI note numbers
- Export generated songs to MIDI files

These improvements would create more varied and musically interesting compositions while making the generator more flexible for experimentation.
