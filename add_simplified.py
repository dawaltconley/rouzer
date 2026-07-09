#!/usr/bin/env python3
"""Prefix each rouzer-flashcards.txt headword with its simplified form.

The deck's first column currently holds only the traditional headword in
brackets, e.g. `[報]`. This script rewrites it to `SIMP[TRAD]` (e.g. `报[報]`)
using flash-2607090109.txt, whose first column already stores each headword as
`SIMP[TRAD]`. Headwords absent from that map are left untouched.
"""

import re
import shutil

FLASH = "flash-2607090109.txt"
DECK = "rouzer-flashcards.txt"
BACKUP = DECK + ".bak"

# Matches a `SIMP[TRAD]` first column. group 1 = simplified, group 2 = traditional.
FLASH_RE = re.compile(r"^(.+)\[(.+)\]\t")
# Matches the bracketed traditional headword at the start of a deck line.
DECK_RE = re.compile(r"^\[([^\]]*)\]")


def build_map(path):
    """Return {traditional -> simplified} parsed from the flash file."""
    mapping = {}
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            if line.startswith("//") or not line.strip():
                continue
            m = FLASH_RE.match(line)
            if m:
                simp, trad = m.group(1), m.group(2)
                mapping[trad] = simp
    return mapping


def main():
    mapping = build_map(FLASH)

    with open(DECK, encoding="utf-8", newline="") as f:
        lines = f.readlines()

    prefixed = 0
    untouched_data = 0  # data lines whose headword isn't in the map
    untouched_other = 0  # comments and blank lines

    out = []
    for line in lines:
        if not line.startswith("["):
            out.append(line)
            untouched_other += 1
            continue
        m = DECK_RE.match(line)
        trad = m.group(1) if m else None
        if trad in mapping:
            out.append(mapping[trad] + line)
            prefixed += 1
        else:
            out.append(line)
            untouched_data += 1

    shutil.copyfile(DECK, BACKUP)
    with open(DECK, "w", encoding="utf-8", newline="") as f:
        f.writelines(out)

    print(f"map entries:          {len(mapping)}")
    print(f"lines prefixed:       {prefixed}")
    print(f"data lines untouched: {untouched_data} (headword not in map)")
    print(f"other lines:          {untouched_other} (comments/blank)")
    print(f"backup written to:    {BACKUP}")


if __name__ == "__main__":
    main()
