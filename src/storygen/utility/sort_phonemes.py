#! /usr/bin/env python
from storygen.utility.paths import FilePaths


def main():
    ph_file_path = FilePaths.data_dir / "phonemes.txt"
    with ph_file_path.open() as f:
        phonemes = [l.strip() for l in f if l.strip()]
    original = phonemes
    phonemes = set(phonemes)
    if len(original) != len(phonemes):
        print("Removed {} duplicates".format(len(original) - len(phonemes)))
    phonemes = sorted(phonemes)
    with ph_file_path.open('w') as f:
        for ph in phonemes:
            f.write(ph + "\n")


if __name__ == "__main__":
    main()
