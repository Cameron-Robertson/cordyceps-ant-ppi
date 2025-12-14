This project uses a staged computational workflow run across multiple environments:

* Structure prediction in ColabFold (create monomers and multimers from FASTA sequences)
* Original src python scripts used local file directories
* Some src scripts had hard-coded input files
* External tools were used such as HADDOCK 
* Some outputs are too large to version, such as FASTA files.



This is therefore not executed as a single automated Snakemake pipeline - but is here as a placeholder and to indicate that it could be extended in future to be partially (or even fully) automated.



