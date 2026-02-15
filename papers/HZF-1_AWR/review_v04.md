# Review Report — Paper HZF-1 (Adv. Water Resour. v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

The GPU parallelization strategy is sound, and the extension to tree topologies addresses a key practical need. The ML surrogate comparison and multi-GPU discussion complete the paper's positioning. Two technical concerns remain regarding the predictor-corrector convergence analysis and the stability of the domain decomposition.

**Score: 8.0/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. Predictor-Corrector Convergence Proof

The paper states that the predictor-corrector "converges in one iteration for weakly coupled networks" (§3.3) but provides no formal convergence analysis. What is the contraction factor? Under what conditions (pool length, flow velocity, time step) is convergence guaranteed in ≤2 iterations? A brief analysis using the spectral radius of the boundary iteration matrix would strengthen the paper.

**Recommendation**: Add a convergence analysis in §3.3 showing the contraction factor as a function of the coupling strength (ratio of pool delay to time step).

### M2. Boundary Condition Treatment at Domain Interfaces

The predictor-corrector uses boundary values from the previous time step as the initial guess. This is first-order in time. For the Preissmann scheme (which is second-order in time with θ = 0.6), this may degrade the overall temporal accuracy. Is the global scheme still second-order? A verification via the method of manufactured solutions would clarify.

**Recommendation**: Add a temporal convergence test (halving Δt) to verify the order of accuracy of the domain-decomposed scheme.

---

## Minor Issues

None requiring revision beyond the major items.

## Summary

Minor revision. The convergence analysis and temporal order verification are important for the computational methods community reading AWR.
