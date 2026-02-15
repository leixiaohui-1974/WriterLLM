# Review Report — Paper P2A (JWRPM v6)

**Iteration**: 6 of 20+
**Reviewer**: A (Control Theorist) — European control theory professor
**Date**: 2026-02-13

---

## Overall Assessment

This is my second review of this paper (first review: iteration 3, score 8/10, Minor Revision). My previous concerns have been addressed with precision:

- **"Mathematically provable constraint satisfaction"**: Replaced with the dual-layer guarantee formulation: MPC enforces constraints under model accuracy assumptions within the ODD, while Layer 0 provides a model-independent hard backup. This is the correct argument—the safety guarantee does not rest on model accuracy alone. ✓
- **Hierarchical optimality and consistency**: Dedicated paragraph acknowledging suboptimality tradeoff, time-scale separation argument, constraint softening pathway, and L0 backup. Transparent and technically correct. ✓
- **Feasibility definition in propose-validate loop**: Operationally defined — HDC solves Equations 2–4 with CI-proposed parameters over verification horizon N_v; accepted iff feasible. Computationally tractable because it reuses the MPC solver. Clean. ✓
- **Padé order**: Second-order specified. ✓
- **τ_coast wave celerity**: Kinematic vs. dynamic wave speed distinction clarified with physical justification. ✓
- **Equation (6)**: Relabeled as protocol (P1). ✓
- **DMPC topology**: Cascade-serial clarified for both cases. ✓
- **Terminal cost/constraint**: L0 backup argument provided. ✓
- **Mayne et al. (2000)**: Added. ✓

The v05→v06 revisions (shadow-mode deployment, open standards pathway) add practical value beyond my scope of review but are well-executed.

From a control-theoretic perspective, the paper now handles its formal claims with appropriate care. The mathematical content is correctly specified with transparent assumptions and qualifications. The hierarchical MPC architecture is well-grounded in the established literature (Litrico & Fromion, Negenborn, Maestre, Mayne). The dual-layer safety argument (MPC + L0) is architecturally sound and well-articulated. I have no remaining substantive concerns.

**Score: 9/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | Framework synthesis with formal definitions; individual elements established |
| Mathematical Rigor | 9 | Assumptions transparent; qualifications precise; feasibility defined |
| Reproducibility | 8 | MPC parameters, Padé order, wave speeds all specified |
| Case Validation | 8 | MiL data complete; dual-topology design effective |
| Literature Completeness | 9 | Mayne et al. added; 35 references comprehensive |
| Writing Quality | 8.5 | Clear and well-structured |
| System Differentiation | 9 | Strong positioning across all dimensions |

---

## Major Issues

None.

---

## Minor Issues

### m1. DMPC Convergence Rate
The paper correctly caveats DMPC convergence under non-convexity/strong coupling. A practitioner-facing addition would be to state the typical number of DMPC iterations required for convergence in the two case studies (e.g., "3–5 iterations for Shaping, 5–10 iterations for Jiaodong"). This helps readers assess whether real-time DMPC is computationally feasible for their systems. Optional.

---

## Summary

This paper has achieved publication quality. The MAS architecture and WSAL classification are well-formulated contributions. The mathematical content is correctly stated with appropriate assumptions and qualifications. The dual-layer safety guarantee (MPC optimization + Layer 0 hard backup) is architecturally sound. The two-case topology contrast provides credible MiL validation evidence. I recommend acceptance.
