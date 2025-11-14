#!/bin/bash

# Bash command to run the python script which fetches monomer FASTA sequences using NCBI Entrez
# Usage: ./fetch_monomer_FASTAs.sh

cd /mnt/c/bio/Cordyceps_Ant_ppi_tools/Cordyceps_Ant_ppi_tools

export NCBI_EMAIL="your email here"

python fetch_fasta_monomers.py monomer_accessions.txt monomers_fasta/
