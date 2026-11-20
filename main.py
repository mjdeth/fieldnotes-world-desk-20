#!/usr/bin/env python3
"""FIELDNOTES World Desk — entry program for make.fun news-image-20261120.

Standard library only. Copies the poster image held in this repository
(entry.png, rendered at build time by render.py) to the output directory,
so every run writes exactly the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
