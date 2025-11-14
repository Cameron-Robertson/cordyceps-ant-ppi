# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 20:40:30 2025

@author: Cameron
"""

# Editable scoring matrix for ranking Ophiocordyceps-Camponotus PPIs
# Adjust weights and keyword lists to tune model selection

import pandas as pd
import re

df = pd.read_excel("Ocf-Cf_final_strict_PPIs_from_MOESM3_4.xlsx")

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

# To apply this to a dataframe:
df['priority_score'] = df.apply(score_ppi_row, axis=1)
df_top20 = df.sort_values('priority_score', ascending=False).head(20)
df_top20.to_excel("Top20_PPIs_ranked2.xlsx", index=False)