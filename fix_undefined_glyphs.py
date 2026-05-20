#!/usr/bin/env python3
"""
fix_nbsp.py — Map U+00A0 (NO-BREAK SPACE) to the same glyph as U+0020 (SPACE).

Fixes fonts where NBSP renders as '?' because it has no cmap entry.

Usage:
    python fix_nbsp.py input.ttf output.ttf
"""

import argparse
import sys
from fontTools.ttLib import TTFont


def fix_nbsp(input_path: str, output_path: str):
    font = TTFont(input_path)

    cmap = font.getBestCmap()
    if cmap is None:
        print("ERROR: No usable cmap table found.")
        sys.exit(1)

    # Check if NBSP is already mapped
    if 0x00A0 in cmap:
        print(f"U+00A0 is already mapped to glyph '{cmap[0x00A0]}' — nothing to do.")
        sys.exit(0)

    # Find what glyph U+0020 (regular space) maps to
    if 0x0020 not in cmap:
        print("ERROR: U+0020 (SPACE) not found in cmap — can't determine space glyph.")
        sys.exit(1)

    space_glyph = cmap[0x0020]
    print(f"U+0020 (SPACE) -> '{space_glyph}'")
    print(f"Mapping U+00A0 (NBSP) -> '{space_glyph}'")

    # Add the mapping to all cmap subtables that contain U+0020
    for table in font["cmap"].tables:
        if hasattr(table, "cmap") and 0x0020 in table.cmap:
            table.cmap[0x00A0] = space_glyph

    font.save(output_path)
    print(f"Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Map U+00A0 (NBSP) to the space glyph to fix '?' rendering."
    )
    parser.add_argument("input", help="Input TTF/OTF font file")
    parser.add_argument("output", help="Output font file path")
    args = parser.parse_args()
    fix_nbsp(args.input, args.output)


if __name__ == "__main__":
    main()
