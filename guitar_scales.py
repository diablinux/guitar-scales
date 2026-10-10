import argparse

# --- Foundational Music Theory & Fretboard Data (Unchanged) ---
CHROMATIC_SCALE_SHARPS = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
CHROMATIC_SCALE_FLATS = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
ALL_CHROMATIC_NOTES = sorted(list(set(CHROMATIC_SCALE_SHARPS + CHROMATIC_SCALE_FLATS)))
SHARP_KEYS = {'G', 'D', 'A', 'E', 'B', 'F#', 'C#'}
FLAT_KEYS = {'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb'}
ENHARMONIC_MAP = {'A#': 'Bb', 'Bb': 'A#', 'C#': 'Db', 'Db': 'C#', 'D#': 'Eb', 'Eb': 'D#', 'F#': 'Gb', 'Gb': 'F#', 'G#': 'Ab', 'Ab': 'G#'}
STANDARD_TUNING = ['E', 'A', 'D', 'G', 'B', 'E']
REVERSED_TUNING = STANDARD_TUNING[::-1]
FRET_COUNT = 12

MODE_INTERVALS = {
    "Ionian":    [2, 2, 1, 2, 2, 2, 1], "Dorian":    [2, 1, 2, 2, 2, 1, 2],
    "Phrygian":  [1, 2, 2, 2, 1, 2, 2], "Lydian":    [2, 2, 2, 1, 2, 2, 1],
    "Mixo-lydian": [2, 2, 1, 2, 2, 1, 2], "Aeolian":   [2, 1, 2, 2, 1, 2, 2],
    "Locrian":   [1, 2, 2, 1, 2, 2, 2]
}

# --- Core Functions (Unchanged) ---
def generate_diatonic_scale(root_note: str, mode_name: str) -> list[str] | None:
    if mode_name not in MODE_INTERVALS: return None
    chromatic_source = CHROMATIC_SCALE_FLATS if root_note in FLAT_KEYS else CHROMATIC_SCALE_SHARPS
    if root_note not in chromatic_source:
        chromatic_source = CHROMATIC_SCALE_SHARPS if root_note in CHROMATIC_SCALE_SHARPS else CHROMATIC_SCALE_FLATS
        if root_note not in chromatic_source: return None
    current_index = chromatic_source.index(root_note)
    scale = [root_note]
    pattern = MODE_INTERVALS[mode_name]
    for interval in pattern[:-1]:
        current_index = (current_index + interval) % 12
        scale.append(chromatic_source[current_index])
    return scale

def generate_full_fretboard_map() -> list[list[str]]:
    fretboard_map = []
    for open_note in REVERSED_TUNING:
        string_notes = []
        start_index = CHROMATIC_SCALE_SHARPS.index(ENHARMONIC_MAP.get(open_note, open_note))
        for fret in range(FRET_COUNT + 1):
            note_index = (start_index + fret) % 12
            string_notes.append(CHROMATIC_SCALE_SHARPS[note_index])
        fretboard_map.append(string_notes)
    return fretboard_map

def display_fretboard_for_scale(scale_name: str, root_note: str, scale_notes: list[str], full_fretboard: list[list[str]]):
    print(f"### Scale: {scale_name} (`{' - '.join(scale_notes)}`)")
    print("<table><thead><tr>")
    print('<th style="background-color: #f0f0f0; text-align: center;">String</th>')
    for i in range(FRET_COUNT + 1): print(f'<th style="text-align: center;">{i}</th>')
    print("</tr></thead><tbody>")
    scale_notes_set = set(scale_notes)
    for i, string_notes in enumerate(full_fretboard):
        string_name = REVERSED_TUNING[i]
        print("<tr>")
        print(f'<td style="background-color: #f0f0f0; text-align: center;"><strong>{string_name}</strong></td>')
        for note in string_notes:
            cell_content = "--"
            if note in scale_notes_set or ENHARMONIC_MAP.get(note) in scale_notes_set:
                is_root = (note == root_note) or (ENHARMONIC_MAP.get(note) == root_note)
                cell_content = f"<strong>{note}</strong>" if is_root else note
            print(f'<td style="text-align: center;">{cell_content}</td>')
        print("</tr>")
    print("</tbody></table>\n\n---\n")

# --- MODIFICATION: Main Execution Block with argparse ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate musical scale diagrams for a guitar fretboard.",
        formatter_class=argparse.RawTextHelpFormatter # Improves help text formatting
    )
    parser.add_argument(
        '-r', '--root',
        nargs='+',  # Accept one or more values
        required=True,
        choices=ALL_CHROMATIC_NOTES,
        metavar='ROOT_NOTE',
        help="Specify one or more root notes. Example: C G# Bb"
    )
    parser.add_argument(
        '-m', '--mode',
        nargs='+',
        required=True,
        choices=MODE_INTERVALS.keys(),
        metavar='MODE_NAME',
        help=f"Specify one or more modes from the following:\n" + "\n".join(MODE_INTERVALS.keys())
    )
    
    args = parser.parse_args()
    
    master_fretboard = generate_full_fretboard_map()
    
    print(f"Generating diagrams for Root(s): {', '.join(args.root)} and Mode(s): {', '.join(args.mode)}\n")

    for mode_name in args.mode:
        for root_note in args.root:
            scale = generate_diatonic_scale(root_note, mode_name)
            if scale:
                display_fretboard_for_scale(f"{root_note} {mode_name}", root_note, scale, master_fretboard)