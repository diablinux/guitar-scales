import argparse
import sys

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

# --- Core Functions (Unchanged Logic, Modified Output) ---
def generate_diatonic_scale(root_note: str, mode_name: str) -> list[str] | None:
    # Function is unchanged
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
    # Function is unchanged
    fretboard_map = []
    for open_note in REVERSED_TUNING:
        string_notes = []
        start_index = CHROMATIC_SCALE_SHARPS.index(ENHARMONIC_MAP.get(open_note, open_note))
        for fret in range(FRET_COUNT + 1):
            note_index = (start_index + fret) % 12
            string_notes.append(CHROMATIC_SCALE_SHARPS[note_index])
        fretboard_map.append(string_notes)
    return fretboard_map

def display_fretboard_for_scale(scale_name: str, root_note: str, scale_notes: list[str], full_fretboard: list[list[str]], file_handle):
    """Writes the HTML table for a single scale to the provided file handle."""
    print(f"<h3>Scale: {scale_name} (<code>{' - '.join(scale_notes)}</code>)</h3>", file=file_handle)
    print("<table><thead><tr>", file=file_handle)
    print('<th style="background-color: #f0f0f0; text-align: center;">String</th>', file=file_handle)
    for i in range(FRET_COUNT + 1): print(f'<th style="text-align: center;">{i}</th>', file=file_handle)
    print("</tr></thead><tbody>", file=file_handle)
    scale_notes_set = set(scale_notes)
    for i, string_notes in enumerate(full_fretboard):
        string_name = REVERSED_TUNING[i]
        print("<tr>", file=file_handle)
        print(f'<td style="background-color: #f0f0f0; text-align: center;"><strong>{string_name}</strong></td>', file=file_handle)
        for note in string_notes:
            cell_content = "--"
            if note in scale_notes_set or ENHARMONIC_MAP.get(note) in scale_notes_set:
                is_root = (note == root_note) or (ENHARMONIC_MAP.get(note) == root_note)
                cell_content = f"<strong>{note}</strong>" if is_root else note
            print(f'<td style="text-align: center;">{cell_content}</td>', file=file_handle)
        print("</tr>", file=file_handle)
    print("</tbody></table>\n<hr>\n", file=file_handle)

def write_html_header(title: str, file_handle):
    """Writes the complete HTML document header."""
    header = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        table {{ border-collapse: collapse; margin-bottom: 2em; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #ccc; padding: 0.5em; }}
        code {{ background-color: #eee; padding: 0.2em 0.4em; border-radius: 3px; }}
        h1, h3 {{ color: #333; }}
        hr {{ border: 0; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>{title}</h1>"""
    print(header, file=file_handle)

def write_html_footer(file_handle):
    """Writes the HTML document footer."""
    print("</body>\n</html>", file=file_handle)

# --- Main Execution Block with File Output Logic ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate musical scale diagrams for a guitar fretboard.")
    parser.add_argument('-r', '--root', nargs='+', choices=ALL_CHROMATIC_NOTES, metavar='ROOT', help="One or more root notes.")
    parser.add_argument('-m', '--mode', nargs='+', choices=MODE_INTERVALS.keys(), metavar='MODE', help="One or more modes.")
    parser.add_argument('-o', '--outfile', metavar='FILE', help="Specify a name for the output HTML file.")
    
    args = parser.parse_args()

    # Determine which roots and modes to process
    if args.root and args.mode:
        roots_to_process = args.root
        modes_to_process = args.mode
        title = f"Fretboard Diagrams for {', '.join(roots_to_process)} {', '.join(modes_to_process)}"
        default_filename = f"{'-'.join(roots_to_process)}_{'-'.join(modes_to_process)}.html"
    else:
        # If specific roots/modes are not provided, process all of them
        roots_to_process = CHROMATIC_SCALE_SHARPS
        modes_to_process = MODE_INTERVALS.keys()
        title = "Fretboard Diagrams for All Notes and Modes"
        default_filename = "all_notes_all_modes.html"

    output_filename = args.outfile if args.outfile else default_filename
    
    master_fretboard = generate_full_fretboard_map()

    try:
        with open(output_filename, 'w') as f:
            write_html_header(title, f)
            print(f"Generating diagrams. Output will be saved to '{output_filename}'...")

            for mode_name in modes_to_process:
                for root_note in roots_to_process:
                    scale = generate_diatonic_scale(root_note, mode_name)
                    if scale:
                        display_fretboard_for_scale(f"{root_note} {mode_name}", root_note, scale, master_fretboard, f)
            
            write_html_footer(f)
        
        print(f"Successfully generated '{output_filename}'.")

    except IOError as e:
        print(f"Error: Could not write to file '{output_filename}'. Reason: {e}", file=sys.stderr)
