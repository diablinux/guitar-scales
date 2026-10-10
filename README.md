# Guitar Scale Fretboard Generator

[![Deploy Fretboard Diagrams to GitHub Pages](https://github.com/diablinux/guitar-scales/actions/workflows/deploy_pages.yaml/badge.svg)](https://github.com/diablinux/guitar-scales/actions/workflows/deploy_pages.yaml)
[![GitHub Pages](https://img.shields.io/github/deployments/diablinux/guitar-scales/github-pages?label=docs&logo=github)](https://diablinux.github.io/guitar-scales/all_notes_all_modes.html)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A command-line tool written in Python to generate and display musical scale diagrams on a guitar fretboard. The output is a portable, self-contained HTML file, ideal for study and reference.

The primary documentation, which includes diagrams for all notes in all modes, is automatically generated and deployed via GitHub Actions. You can view the live version here:
**[View Live Fretboard Diagrams](https://diablinux.github.io/guitar-scales/all_notes_all_modes.html)**

---

## Table of Contents

- [Guitar Scale Fretboard Generator](#guitar-scale-fretboard-generator)
  - [Table of Contents](#table-of-contents)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command-Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Continuous Integration (CI/CD)](#continuous-integration-cicd)
  - [Technical Implementation](#technical-implementation)
  - [Future Enhancements](#future-enhancements)
  - [License](#license)

---

## Key Features

- **Complete Modal System:** Generates diagrams for all seven diatonic modes (Ionian, Dorian, Phrygian, Lydian, Mixo-lydian, Aeolian, Locrian).
- **Full Chromatic Support:** Supports all 12 chromatic notes as the root for any scale.
- **Command-Line Interface:** A robust and user-friendly CLI powered by Python's `argparse` module for specifying desired scales.
- **HTML Output:** Creates clean, styled, and self-contained HTML files that can be viewed in any modern web browser.
- **Automated Deployment:** Integrates with GitHub Actions to automatically generate and deploy a comprehensive reference (`all_notes_all_modes.html`) to GitHub Pages.

## Installation

No external packages are required. The script uses only the Python standard library.

1. **Ensure Python is installed.** Python 3.8 or higher is recommended.

    ```bash
    python --version
    ```

2. **Clone the repository:**

    ```bash
    git clone https://github.com/diablinux/guitar-scales.git
    cd guitar-scales
    ```

## Usage

The script is executed from the command line, providing root notes and modes as arguments.

### Command-Line Arguments

```bash
(.venv) ➜  guitar git:(main) ✗ python guitar_scales.py --help
usage: guitar_scales.py [-h] [-r ROOT [ROOT ...]] [-m MODE [MODE ...]] [-o FILE]

Generate musical scale diagrams for a guitar fretboard.

options:
  -h, --help            show this help message and exit
  -r, --root ROOT [ROOT ...]
                        One or more root notes.
  -m, --mode MODE [MODE ...]
                        One or more modes.
  -o, --outfile FILE    Specify a name for the output HTML file.
```

### Examples

1. **Generate a diagram for C Ionian (Major):**

    ```bash
    python fretboard_generator.py --root C --mode Ionian
    ```

    This will create an output file named `C_Ionian.html`.

2. **Generate diagrams for E Aeolian and G Mixo-lydian:**

    ```bash
    python fretboard_generator.py --root E G --mode Aeolian Mixo-lydian
    ```

    This will create an output file named `E-G_Aeolian-Mixo-lydian.html`.

3. **Generate the master reference file manually:**
    Running the script with no arguments generates the complete reference for all scales.

    ```bash
    python fretboard_generator.py
    ```

    This will create the output file `all_notes_all_modes.html`.

4. **Specify a custom output filename:**

    ```bash
    python fretboard_generator.py --root A --mode Dorian -o my_dorian_study.html
    ```

## Continuous Integration (CI/CD)

This project utilizes a GitHub Actions workflow defined in `.github/workflows/deploy-pages.yml`.

- **Trigger:** The workflow runs automatically on every `push` to the `main` branch.
- **Process:**
    1. Sets up a Python 3.11 environment.
    2. Executes `python fretboard_generator.py` to build the `all_notes_all_modes.html` file.
    3. Uploads the generated HTML file as a build artifact.
    4. Deploys the artifact to the `gh-pages` environment.
- **Result:** The master documentation is kept consistently up-to-date with the latest version of the code.

## Technical Implementation

- **Music Theory Engine:** Scale generation is based on fundamental music theory. A chromatic scale (`list`) serves as the base, and modal interval patterns (e.g., `W-W-H-W-W-W-H` or `[2, 2, 1, 2, 2, 2, 1]`) are applied to derive the notes of a given scale.
- **Fretboard Representation:** The guitar fretboard is modeled as a 2D list (a list of lists), where each inner list represents a string.
- **Scale Highlighting:** To display a scale, the script iterates through the fretboard map and checks if each note is a member of the generated scale notes (`set` for O(1) average-time complexity lookups). Root notes are highlighted in bold.
- **HTML Generation:** The script uses standard `print` functions redirected to a file handle to write a complete HTML5 document, including an embedded CSS `<style>` block for presentation.

## Future Enhancements

Potential improvements and contributions are welcome in the following areas:

- Support for alternate tunings (e.g., Drop D, DADGAD).
- Inclusion of other scale types (e.g., Pentatonic, Harmonic Minor, Melodic Minor).
- Highlighting specific scale degrees (3rd, 5th, 7th) with different colors or styles.
- An option to generate graphical output (e.g., SVG or PNG) instead of HTML tables.
- Implementation of a testing suite (e.g., `unittest` or `pytest`) to validate scale generation logic.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
