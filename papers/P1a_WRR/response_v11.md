# Revision Response — P1a WRR v10 → v11

**Iteration**: 2
**Reviewer**: C (Cross-disciplinary Scholar)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. "Cognitive Intelligence" Component Underdeveloped

**Response**: Fully accepted. This was a genuine gap. The Cognitive Intelligence component was underspecified relative to its architectural importance.

**Action taken**: Substantially expanded Section 7.3 with:
- A concrete operational example: drought escalation scenario recognition → objective function modification → constraint set adjustment → HDC re-parameterization
- Explicit description of the propose-validate interface: Cognitive AI outputs a candidate {objective, constraints, ODD-status} tuple; HDC validates feasibility via constraint checking before execution
- Failure mode specification: confidence threshold mechanism; below-threshold defaults to last-valid HDC configuration
- Replaced generic ML citations (Brown et al., 2020; Lewis et al., 2020) with water-domain-specific AI references (Kratzert et al., 2019; added Bommasani et al., 2021 for foundation models context)

### M2. Missing Engagement with Data-Driven Hydrology and Digital Twin Literature

**Response**: Accepted. This is an important positioning gap that limits the paper's cross-disciplinary appeal.

**Action taken**:
- Added new subsection 8.4 "CHS and Data-Driven Approaches: Complementarity, Not Competition" explicitly positioning the relationship:
  - CHS provides the structural backbone (model hierarchy, control architecture)
  - Data-driven methods provide calibration, gap-filling, and pattern recognition within the CHS structure
  - RL is explicitly discussed as the paradigm most constrained by OS5, with sim-to-real transfer via digital twins as the resolution pathway
- Added references: Kratzert et al. (2019), Castelletti et al. (2010) for RL, Bommasani et al. (2021) for foundation models

### M3. Proposition 1 Needs Formal Strengthening

**Response**: We adopt approach (b) — explicit counterexample analysis — as the more scientifically honest choice. Converting Proposition 1 to a theorem would require restrictive assumptions that could narrow the framework's applicability.

**Action taken**: Added a "Scope and Limits" paragraph after Proposition 1 in Section 3.2, explicitly discussing:
- Groundwater systems (Darcy flow): fundamentally diffusive, no wave propagation → S1 (transport delay dominance) does not hold. CHS covers conveyance/distribution but NOT subsurface flow.
- Stormwater/CSO systems: partially covered under pressurized networks, but episodic activation violates the continuous-operation assumption implicit in S3 (slow actuators).
- This boundary sharpens the claim: CHS covers systems with wave-propagation physics and continuous operations, which encompasses the vast majority of infrastructure by investment value.

### M4. The "Third Revolution" Claim Needs Calibration

**Response**: Accepted. Scientific humility strengthens the claim.

**Action taken**: Revised the relevant paragraph in Section 10:
- Added explicit dating: First revolution (1871-1960s, from Saint-Venant to computational hydraulics); Second revolution (1962-2010s, from Maass et al. to modern WRSA); Third revolution (2020s-, real-time autonomous operation)
- Added criteria: "A revolution in water infrastructure science is characterized by a qualitative shift in the fundamental question the discipline addresses"
- Reframed: "CHS provides what we believe to be the necessary theoretical foundation for this third revolution" — acknowledging that validation, prototyping, and community adoption remain ahead

### M5. Section 5.3 Tradeoffs Lack Quantitative Treatment

**Response**: Accepted. This is an excellent suggestion that strengthens the paper's analytical depth.

**Action taken**: Added an analytical derivation of the P2-P6 tradeoff in Section 5.3:
- Defined buffer fraction f_b = V_buffer / V_total
- Derived: optimal f_b = min(1, τ_d / T_comm) under simplified assumptions (single-pool, constant disturbance amplitude)
- This yields Prediction 3's quantitative boundaries: when τ_d/T_comm > 1, f_b → 1 (full local buffering); when τ_d/T_comm → 0, f_b → 0 (full coordination)
- Noted that the actual optimum includes a coordination penalty factor that shifts the curve, requiring DMPC simulation for precise values

---

## Response to Minor Issues

### m1. "Cybernetics" in the Title
**Action**: Retained. The term is a deliberate intellectual positioning choice linking to Wiener's transdisciplinary vision. The Chinese-language companion (P1c) uses 水系统控制论, which directly translates to "water systems cybernetics." Changing the English title would break this bilingual parallelism. Added a brief footnote at first use explaining the choice.

### m2. Table 2 Readability
**Action**: Added a companion schematic diagram description in the figure captions (new Figure 1b) showing the cross-sector mapping visually. Table 2 content unchanged but reformatted for improved column alignment.

### m3. WSAL Table Missing Detail
**Action**: Added measurable transition criteria to Table 6:
- WSAL-1→2: MPC controller commissioned and validated at MiL/SiL stages
- WSAL-2→3: Full xIL certification for normal-flow ODD; operator intervention rate <5% within certified ODD
- WSAL-3→4: ODD covers >80% of operating scenarios; autonomous ODD expansion demonstrated
- WSAL-4→5: Full-envelope ODD with self-expanding capability; zero human intervention under all certified scenarios

### m4. Lemma 3 Generality
**Action**: Added a brief validity note: "The linearization is valid within ±20% of the nominal operating point for gates and valves, and within ±15% for pumps operating near their Best Efficiency Point. For pumps operating far from BEP, a piecewise-linear or gain-scheduled extension is required."

### m5. Plain Language Summary
**Action**: No changes (reviewer praised it).

---

## Reference Changes

### Added:
1. Kratzert, F., Klotz, D., Brenner, C., Shalev, G., & Nearing, G. (2019). Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks. HESS, 23(12), 6005–6022.
2. Bommasani, R., et al. (2021). On the opportunities and risks of foundation models. arXiv:2108.07258.
3. Castelletti, A., Galelli, S., Restelli, M., & Soncini-Sessa, R. (2010). Tree-based reinforcement learning for optimal water reservoir operation. WRR, 46(9), W09507.

### Removed:
- Brown, T. B., et al. (2020) — replaced by more specific references
- Lewis, P., et al. (2020) — replaced by more specific references

---

## Version Summary

- **v10 → v11 changes**: Expanded Cognitive Intelligence with concrete operational example, added Section 8.4 (CHS vs. data-driven approaches), added Proposition 1 scope/limits, calibrated "third revolution" claim, added quantitative P2-P6 tradeoff derivation, added WSAL transition criteria, updated references.
- **Self-citation rate**: Recounted — ~16% (unchanged, within target).
- **Next focus**: Mathematical rigor review (Reviewer A), further case validation strengthening.
