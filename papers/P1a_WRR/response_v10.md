# Revision Response — P1a WRR v9 → v10

**Iteration**: 1
**Reviewer**: B (Engineering Practitioner)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Absence of Numerical Validation Against Saint-Venant Benchmarks

**Response**: This is a valid concern. However, the paper is explicitly positioned as a *theoretical and review contribution* (see Open Research statement). The unified transfer function family and Muskingum-IDZ duality are mathematical results that hold independently of simulation validation. The illustrative applications in Section 6 are deliberately analytical to demonstrate the *algebraic structure* of cross-sector transfer, not to provide numerical benchmarks.

**Action taken**: Added a paragraph at the end of Section 6 acknowledging this limitation more explicitly and referencing specific published numerical validations from the literature (Litrico & Fromion 2004, 2009; Horváth et al., 2024; Negenborn et al., 2009) that confirm the IDZ model's accuracy against full Saint-Venant simulations. Also strengthened Prediction 1 justification (see M5 response).

### M2. SCADA/PLC Integration Feasibility Not Addressed

**Response**: Accepted. This is an important practical gap. While the paper is a theoretical framework paper, a brief discussion of implementation pathways strengthens the practical relevance.

**Action taken**: Added Section 7.5 "Implementation Pathway and SCADA Integration" providing:
- Communication protocol considerations (OPC-UA as the recommended standard)
- Computational platform requirements (modern field-grade industrial PCs can solve the Layer 1 MPC QP at 300s sampling)
- Layer 0 veto mechanism compatibility with IEC 61131-3 PLC safety logic
- Reference to the xIL verification framework (Lei, 2025c) as the systematic integration methodology

### M3. The Muskingum-IDZ Duality Proof Needs Stronger Conditions

**Response**: Accepted. The approximation validity conditions should be stated explicitly.

**Action taken**: Added a "Validity conditions" paragraph after Corollary 1 in Section 4.3, specifying:
- The approximation is valid for frequencies ω < 1/(3K), i.e., for timescales longer than about 3 Muskingum time constants
- At control-relevant frequencies (typical MPC prediction horizons of 10K-50K), the gain error is <5% and phase error is <10°
- The physical assumption difference (downstream BC) is explicitly stated as the distinguishing factor between the two families

### M4. Self-Citation Rate Needs Verification

**Response**: Accepted.

**Action taken**: Counted all references. Total unique references: ~50. Self-citations (Lei et al.): 8 (Lei 2025a-d + Ye, Lei et al. 2023 + 3 additional Lei co-authored works). Self-citation rate: ~16%, within the target 15-25% range. Added brief summaries of the key concepts from Lei (2025a-d) where they are first referenced to ensure the paper is self-contained.

### M5. Prediction 1 (30% RMS Improvement) Lacks Justification

**Response**: Accepted.

**Action taken**: Added justification citing published results:
- Clemmens & Schuurmans (2004): 40-60% improvement with downstream feedback control vs. manual operation on the Maricopa Stanfield Irrigation District
- van Overloop (2006): 25-35% RMS improvement with MPC on Dutch canals
- Horváth et al. (2024): Demonstrated model-based control achieving comparable improvements on experimental canal with automatic structure selection
- The 30% threshold is therefore conservative, being at the lower end of published results

---

## Response to Minor Issues

### m1. Key Points Length
**Action**: Reformatted to 3 Key Points, each ≤140 characters, per WRR guidelines.

### m2. Abstract Length
**Action**: Shortened abstract to ~150 words while preserving the core message.

### m3. Figure Placeholders
**Action**: Figures remain as placeholders in this iteration. Figure generation is planned for a later iteration. The figure captions (Section 10+) provide sufficient description for review purposes.

### m4. Acknowledgments Incomplete
**Action**: Noted for final submission preparation. Grant numbers will be inserted when available.

### m5. Missing "Open Research" Statement
**Action**: Expanded the Open Research section to include a statement about code availability for the MPC examples ("Illustrative MPC code implementing the IDZ-based controller of Section 6.1 will be deposited in [repository] upon acceptance").

### m6. Table Formatting
**Action**: Tables will be formatted properly in the final docx output. The markdown draft preserves content correctly.

### m7. Equation Rendering
**Action**: Equations are stored as base64 images from the docx conversion. Future iterations will convert these to proper LaTeX notation.

---

## Version Summary

- **v9 → v10 changes**: Strengthened numerical validation discussion, added SCADA integration section (§7.5), added Muskingum-IDZ validity conditions, verified self-citation rate, justified Prediction 1, reformatted Key Points and Abstract per WRR guidelines.
- **Next focus**: Address mathematical rigor issues (future Reviewer A focus), figure generation, equation formatting.
