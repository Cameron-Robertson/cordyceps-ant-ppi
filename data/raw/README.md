will\_et\_al\_final\_ppi\_ref\_input.tsv:

This raw data file includes the original final strict PPIs list from Will et al. (2023). The starting point of this project.



monomer\_accessions.txt:

This is the list of NCBI GenBank accession IDs for the 24 monomer proteins. This was manually created downstream of the Will et al. final PPI list.



monomers\_fasta:

This folder contains individual monomer FASTA sequence files, one per protein accession. The files in this folder are the output of the src fetch\_fasta\_monomers.py (which used the above monomer\_accessions.txt as the input).



pairs\_fasta:

This folder contains paired FASTA sequences files, used as inputs for the protein-protein modelling in ColabFold's AlphaFold-Multimer. The files in this folder are the output of the src make\_pairs.py (which used the files in the above monomers\_fasta as the input). Each file represents a cordyceps-ant protein pair derived from the Will et al. final PPI list.



All FASTA files are excluded from version control.





Citation:

If you reuse or adapt this original dataset, please cite:



Will et al. (2023). \[Full citation details in main repository README]

