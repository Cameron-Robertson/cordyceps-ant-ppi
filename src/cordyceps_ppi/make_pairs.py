# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 22:02:06 2025

@author: Cameron
"""

#!/usr/bin/env python3
# make_pairs.py

import os
import sys
import pandas as pd
from pathlib import Path

# === Usage ===
# python make_pairs.py pairs_list.csv monomers_fasta/ pairs_fasta/

pairs_csv = sys.argv[1]
monomer_dir = Path(sys.argv[2])
out_dir = Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)

# Load CSV with 2 columns: ophio_GenBank, cflo_GenBank
df = pd.read_csv(pairs_csv)

def read_fasta(acc):
    fpath = monomer_dir / f"{acc}.fasta"
    if not fpath.exists():
        raise FileNotFoundError(f"Missing monomer FASTA: {fpath}")
    return fpath.read_text().strip()

for i, row in df.iterrows():
    ophio_acc = str(row["ophio_GenBank"]).strip()
    cflo_acc = str(row["cflo_GenBank"]).strip()

    try:
        ophio_seq = read_fasta(ophio_acc)
        cflo_seq = read_fasta(cflo_acc)
    except FileNotFoundError as e:
        print(f"[!] Skipping pair {ophio_acc} + {cflo_acc}: {e}")
        continue

    # Combined two-chain FASTA for AF-Multimer
    combined_fasta = ophio_seq + "\n" + cflo_seq + "\n"
    outfile_name = f"{ophio_acc}__{cflo_acc}.fasta"
    outfile_path = out_dir / outfile_name

    with open(outfile_path, "w") as f:
        f.write(combined_fasta)

    print(f"[{i+1}/{len(df)}] Saved {outfile_name}")
