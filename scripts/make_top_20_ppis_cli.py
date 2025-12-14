# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 18:49:27 2025

@author: Cameron
"""

#!/usr/bin/env python

import argparse
from cordyceps_ppi.make_top_20_ppis2 import run


def main():
    parser = argparse.ArgumentParser(
        description="Rank Ophiocordyceps–Camponotus PPIs and extract top candidates."
    )

    parser.add_argument(
        "input_file",
        help="Input PPI reference table (.tsv, .csv, or .xlsx)"
    )

    parser.add_argument(
        "-o", "--output",
        default="results/Top20_PPIs_ranked.tsv",
        help="Output file path (default: results/Top20_PPIs_ranked.tsv)"
    )

    parser.add_argument(
        "-n", "--top-n",
        type=int,
        default=20,
        help="Number of top PPIs to return (default: 20)"
    )

    args = parser.parse_args()

    run(
        input_file=args.input_file,
        output_file=args.output,
        top_n=args.top_n
    )


if __name__ == "__main__":
    main()
