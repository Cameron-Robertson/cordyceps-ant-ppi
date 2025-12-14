# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 23:49:07 2025

@author: Cameron
"""

#!/usr/bin/env python

"""
Front-door script for fetching monomer FASTA sequences.

This script parses command-line arguments and calls the
cordyceps_ppi.fetch_fasta_monomers library function.
"""

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import argparse
from cordyceps_ppi.fetch_fasta_monomers import run


def main():
    parser = argparse.ArgumentParser(
        description="Fetch monomer FASTA sequences from NCBI"
    )
    parser.add_argument(
        "accessions_file",
        help="Text file containing protein accession IDs (one per line)"
    )
    parser.add_argument(
        "output_dir",
        help="Directory to write downloaded FASTA files"
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Email address for NCBI Entrez"
    )

    args = parser.parse_args()

    run(
        accessions_file=args.accessions_file,
        out_dir=args.output_dir,
        email=args.email
    )


if __name__ == "__main__":
    main()
