# Review — HZF-2 Iteration 6

**Reviewer**: A (Control Theorist)
**Draft reviewed**: v05
**Score**: 9.0 / 10
**Verdict**: Accept

---

## Summary

ParaQP presents a well-developed parallel QP solver for distributed MPC of water conveyance networks. The convergence theory is now properly scoped (Remark 1 on constrained applicability, expanded Theorem 3 proof, ADMM penalty sensitivity), and the benchmarking is thorough. The paper bridges optimization theory and water engineering practice effectively.

## Strengths

1. **Rigorous convergence analysis**: Theorems 1–3 with the important Remark 1 on constrained QP convergence are correctly stated and practically validated. The spectral radius bounds are conservative but useful for strategy selection.

2. **ADMM penalty robustness**: Table 14 and Figure 7 demonstrate that performance is within 20% of optimal for $\rho \in [0.5\rho^*, 3\rho^*]$. The auto-tuning validation gives practitioners confidence in default settings.

3. **Warm-starting analysis**: The 63% reduction in active-set iterations (Table 5) is a significant practical contribution, as warm-starting is often discussed but rarely quantified this rigorously.

4. **Integration coherence**: ParaQP's positioning within the cuSVE/HydroRTP/ODD tool chain is clear and well-motivated. The SiL verification (Table 7) with 3.8 mm IDZ-to-SVE gap quantifies the model mismatch that motivates the ODD safety margins.

5. **Honest limitations**: The explicit acknowledgment of looped network limitations, field validation gap, and nonlinear MPC extension needs demonstrates intellectual honesty.

## Minor Comments (Non-Blocking)

1. The convergence rates in Table 12 could be further analyzed by examining the effect of warm-starting on convergence speed (warm-started vs. cold-started spectral radius estimates).

## Decision

**Accept**. The paper provides a solid theoretical and computational contribution to parallel distributed optimization for water networks. The convergence analysis is sound, the implementation is practical, and the validation is comprehensive.
