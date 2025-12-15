# Cordyceps–Ant PPI (computational pipeline)



This repository contains a computational workflow for prioritising and structurally evaluating protein–protein interactions (PPIs) between the parasitic fungus \*Ophiocordyceps camponoti-floridani\* and its carpenter ant host \*Camponotus floridanus\*. This is an attempt to elucidate the mechanistic actions responsible for the 'summiting phenotype' - sophisticated fungal hijacking of the ant - that is purportedly due to fungal effector proteins acting on ant targets such as enzymes and neuroreceptors.  



The project uses a literature-derived, curated PPI list as a launching point (Will et al., 2023). Then integrates sequence retrieval, heuristic scoring, structural rendering, and interface docking to identify candidate fungal effectors that may contribute to host behavioural manipulation.



This repository accompanies an MSc-level independent research project.





The project workflow consists of 5 conceptual phases:



(1) prioritisation and extraction of the top parasite-host protein pairs

* Make a Top 20 list, extracting from Will et al.'s final PPI list, using Python



(2) retrieving FASTA sequences of the individual proteins from NCBI and pairing respective multimers

* Extract FASTA aa sequences of all 20 protein pairs (40) from NCBI using Python



(3) running interface predictions of multimers and structural predictions of monomers

* Run all 20 multimers through ColabFold - alphafold multimer v1 - as initial screens to get ipTM scores (complex interface confidence).
* Run the 4 Fungal monomers through ColabFold - alphafold2 - to get pLDDT scores (structural confidence). Select the top proteins that have a score of  70. 
* Run the Ant monomers, which pair with the retained Fungal proteins, through ColabFold - alphafold 2. The top monomers, in their respective pairs, are to be advanced to the Docking tool HADDOCK. 



(4) preparation of 3D models and active residue identification

* Prepare the protein monomers in PyMol - by labelling fungal proteins as chain A and ant proteins as chain B. Save an untrimmed version of each monomer, then trim each monomer and save a trimmed version. 
* Load multimers into PyMol to print active residues within 5 angstroms of the other chain. Repeat for both chains, select optimal residues on the 3D model, and align with printed active residue ranges.



(5) docking polished monomer models

* Create a new job in Haddock with an untrimmed pair of monomers - e.g. 'untrimmed\_ophcf\_03720\_cflo\_loc105257681' - enter an active residue, for both monomers, and run. Once completed, save Haddock scores.
* Create a new job in Haddock with a trimmed pair of monomers - e.g. 'trimmed\_ophcf\_03720\_cflo\_loc105257681' - enter the optimal active residue range, for both monomers, and run. Once completed, save Haddock scores and save the PDB file. 







Running the scripts:



All command-line scripts are located in the `scripts/` directory and act as

thin wrappers around the core Python package in `src/cordyceps\_ppi/`.



Example (from the repository root):



```bash

python scripts/make\_top\_20\_ppis\_cli.py \\

&nbsp; data/raw/will\_et\_al\_final\_ppi\_ref\_input.tsv \\

&nbsp; results/top20\_ppis.tsv







The LLMs ChatGPT5.1 and ChatGPT5.2 were used in the generation of source code and scripts.







Reference for Will et al. (2023) paper this project built upon:



Will, I., Beckerson, W.C., de Bekker, C., 2023. Using machine learning to predict protein-protein interactions between a zombie ant fungus and its carpenter ant host. Sci Rep 13, 13821. https://doi.org/10.1038/s41598-023-40764-8



