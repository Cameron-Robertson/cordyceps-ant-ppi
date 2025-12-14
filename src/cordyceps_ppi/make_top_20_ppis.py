# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 18:12:08 2025

@author: Cameron
"""

# Editable scoring matrix for ranking Ophiocordyceps-Camponotus PPIs
# Adjust weights and keyword lists to tune model selection

import pandas as pd
import re

from pathlib import Path
    


# -----------------------------
# Scoring Parameters (editable)
# -----------------------------
PPI_SCORE_WEIGHT = 4           # Core weighting for D-SCRIPT PPI score (higher = more impact)
UP_WEIGHT = 2                  # DEG_ophio = UP
UPSTEAD_WEIGHT = 1.5           # DEG_ophio = UPstead
SP_WEIGHT = 1.5                # Signal peptide (SP)
SSP_WEIGHT = 2.5               # Small secreted protein (SSP)
TIER_A_WEIGHT = 3              # Highest biological relevance
TIER_B_WEIGHT = 2              # Moderate relevance
TIER_C_WEIGHT = 1              # General support
WGCNA_OVERLAP_WEIGHT = 1.5     # Co-varying expression modules between host and fungus

# -----------------------------
# Tiered Keyword Dictionaries
# -----------------------------
tier_keywords = {
    'A': [  # High-priority functional targets
        "dopamine", "octopamine", "serotonin", "tyramine", "synaptic", "vesicle",
        "GPCR", "G protein-coupled receptor", "dopamine receptor", "transport", "DAT", "SERT", "VMAT",
        "period", "timeless", "clock", "cryptochrome", "pdf", "circadian", "cycle", "rhythm",
        "nAChR", "muscarinic", "synaptobrevin", "SNARE", "syntaxin", "SNAP25", "Nav", "Kv", "Cav"
    ],
    'B': [  # Moderately specific
        "G-protein", "kinase", "MAPK", "phosphatase", "cAMP", "cGMP", "PKA", "PKC", "receptor",
        "juvenile hormone", "ecdysteroid", "insulin", "gustatory", "olfactory", "opsin",
        "photoreceptor", "phototransduction", "adenylate cyclase"
    ],
    'C': [  # General or supportive relevance
        "actin", "myosin", "tubulin", "dynein", "kinesin", "cytoskeleton", "adhesion", "motor",
        "immune", "NF-kB", "oxidase", "peroxidase", "heat shock", "HSP", "detoxification", "P450"
    ]
}

# -----------------------------
# WGCNA module pairs that co-vary (from Will et al. 2023)
# -----------------------------
wgcna_overlap = {("F1", "A14"), ("F1", "A15"), ("F2", "A10"), ("F3", "A4"), ("F3", "A15")}

# -----------------------------
# Scoring Functions
# -----------------------------
def keyword_score(text, tier_dict):
    """Return highest tier score based on keyword presence."""
    if not isinstance(text, str):
        return 0
    for tier, words in tier_dict.items():
        for word in words:
            if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
                if tier == 'A': return TIER_A_WEIGHT
                if tier == 'B': return TIER_B_WEIGHT
                if tier == 'C': return TIER_C_WEIGHT
    return 0

def deg_score(value):
    if isinstance(value, str):
        if "UP" in value:
            return UP_WEIGHT if value == "UP" else UPSTEAD_WEIGHT
    return 0

def secretion_score(row):
    score = 0
    if isinstance(row.get("extracellular"), str) and "SP" in row["extracellular"]:
        score += SP_WEIGHT
    if isinstance(row.get("SSP"), str) and "Small secreted" in row["SSP"]:
        score += SSP_WEIGHT
    return score

def wgcna_score(row):
    fungal_mod = row.get("WGCNA_ophio")
    host_mod = row.get("WGCNA_cflo")
    return WGCNA_OVERLAP_WEIGHT if (fungal_mod, host_mod) in wgcna_overlap else 0

# -----------------------------
# Apply scoring to DataFrame
# -----------------------------
def score_ppi_row(row):
    total = 0
    total += PPI_SCORE_WEIGHT * row.get("ppi_score", 0)
    total += deg_score(row.get("DEG_ophio"))
    total += secretion_score(row)
    total += keyword_score(str(row.get("cflo_blast", "")), tier_keywords)
    total += keyword_score(str(row.get("cflo_GO", "")), tier_keywords)
    total += wgcna_score(row)
    return total


# -----------------------------
# Main orchestration function
# -----------------------------
def run(
    input_file: str,
    output_file: str | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Load PPI reference dataset, score interactions, and return top N PPIs.
    """

    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path.resolve()}")

    # Load data
    if input_path.suffix == ".xlsx":
        df = pd.read_excel(input_path)
    elif input_path.suffix in [".tsv", ".txt"]:
        df = pd.read_csv(input_path, sep="\t")
    elif input_path.suffix == ".csv":
        df = pd.read_csv(input_path)
    else:
        raise ValueError(f"Unsupported input format: {input_path.suffix}")

    # Apply scoring
    df = df.copy()
    df["priority_score"] = df.apply(score_ppi_row, axis=1)

    df_top = df.sort_values("priority_score", ascending=False).head(top_n)

    # Optional output
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.suffix == ".xlsx":
            df_top.to_excel(output_path, index=False)
        else:
            df_top.to_csv(output_path, sep="\t", index=False)

    return df_top