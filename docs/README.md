# SilentStacks Evidence Base – PTDTM / Token Blindness

This folder contains the **core evidence base** for the Progressive Token Degradation Threshold Migration (PTDTM) research program.  
All documents are cross-referenced and mutually reinforcing, forming a hierarchical chain of evidence from raw failures to theoretical synthesis.

---

## 📂 Contents

### Core Theories & Summaries
- **ptdtm-theory-summary.md**  
  Executive summary of PTDTM theory: phases, thresholds, statistical tests, cross-platform validation.  
  → Synthesizes all findings into a paper-ready abstract.

- **token-blindness.md**  
  Quantitative analysis of degradation patterns: critical thresholds (65/75/80/85/90/95), multi-phase trajectory, and cross-model validation.  
  → Supplies the numeric backbone of the theory.

### Taxonomy & Classification
- **ptdtm-vs-blindness.md**  
  Defines four types of AI blindness (Context, Size, Resource, Safety).  
  Positions PTDTM as the **measurable proof** of Resource Blindness.  
  → Explains *why* observed failures occur.

- **bridge-table.md**  
  Integration map linking TDT phases ↔ blindness types ↔ PTDTM benchmark levels ↔ clinical analogies.  
  → Shows how quantitative phases align with classification schema.

### Cross-Referencing
- **reference-matrix.md**  
  Crosswalk showing how each file supports the others:  
  - Logs → Thresholds  
  - Thresholds → Taxonomy  
  - Taxonomy → Mechanisms (Step-G / Safety Blindness)  
  - Simulations/Plots → Long-run trajectory  
  → Ensures no file stands alone.

### Visual Evidence
- **Untitled.png**  
  Stabilization and distribution plots:  
  - Convergence at ~78–82% TDT  
  - Variance collapse post-session 195  
  - 81.5% of sessions in catastrophic zone (>85%)  
  → Provides graphical confirmation of textual findings.

---

## 🔗 Evidence Hierarchy

1. **Ground Truth** – P0/CF/RF logs (290 P0s, 4 CFs, 1 RF).  
2. **Quantitative Thresholds** – Defined in *token-blindness.md* and plots.  
3. **Taxonomy** – Blindness types (*ptdtm-vs-blindness.md*).  
4. **Bridge Layer** – Maps thresholds to blindness categories (*bridge-table.md*).  
5. **Mechanism** – Step-G phenomenon (referenced externally).  
6. **Long-Run Dynamics** – Simulations and stabilization plots.  
7. **Synthesis** – *ptdtm-theory-summary.md* for academic use.

---

## ✅ Consistency Check

- Thresholds (65/75/80/85/90/95) are **consistent across all docs**.  
- Sentinel cases (Sessions 5, 12, 15) recur in multiple files.  
- Statistical validation (χ², correlations) match between summaries and analysis docs.  
- Cross-reference matrix confirms **no contradictions** across sources.

---

## 📌 Usage

- **For researchers:** Use the hierarchy as a reproducible framework for testing AI degradation.  
- **For reviewers/auditors:** Begin with *reference-matrix.md* to see how each file connects.  
- **For practitioners:** Treat TDT >75% as a critical intervention point; expect plateau near ~80% without mitigation.  

---

*"When an AI fails to document its own failures, it has perfectly documented its failure mode."*  
— PTDTM Research Team, 2025
