# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 21:04:23 2025

@author: Cameron
"""

#!/usr/bin/env python3
# Usage: python fetch_fasta_monomers.py monomer_accessions.txt monomers_fasta/

from Bio import Entrez
import sys, os, time

input_file = sys.argv[1]
output_dir = sys.argv[2]
email = os.environ.get("NCBI_EMAIL", "your_email@example.com")
Entrez.email = email
os.makedirs(output_dir, exist_ok=True)

with open(input_file) as f:
    accessions = [line.strip() for line in f if line.strip()]

for i, acc in enumerate(accessions, 1):
    try:
        handle = Entrez.efetch(db="protein", id=acc, rettype="fasta", retmode="text")
        fasta = handle.read()
        handle.close()

        if not fasta.strip():
            print(f"[!] Empty FASTA for {acc}")
            continue

        out_path = os.path.join(output_dir, f"{acc}.fasta")
        with open(out_path, "w") as f_out:
            f_out.write(fasta)

        print(f"[{i}/{len(accessions)}] Saved {acc}.fasta")
        time.sleep(0.34)  # NCBI polite rate limit
    except Exception as e:
        print(f"[x] Error fetching {acc}: {e}")
