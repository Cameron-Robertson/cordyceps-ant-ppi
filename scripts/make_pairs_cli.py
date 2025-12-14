# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 23:52:45 2025

@author: Cameron
"""

#!/usr/bin/env python

"""
Front-door script for generating protein pair FASTA sets.
"""

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import argparse
from cordyceps_ppi.make_pairs import run


def main():
    parser = argparse.ArgumentParser(
        description="Generate protein pairs for docking or PPI prediction"
    )
    parser.add_argument(
        "monomers_dir",
        help="Directory containing monomer FASTA files"
    )
    parser.add_argument(
        "output_dir",
        help="Directory to write paired FASTA files"
    )

    args = parser.parse_args()

    run(
        monomers_dir=args.monomers_dir,
        out_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
