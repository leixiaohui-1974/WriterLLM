# Response to Reviewer A — HZF-2 Iteration 3

We thank Reviewer A for the rigorous theoretical critique. Both major and minor issues are addressed.

---

## Major Issues

### M1. Constrained vs. unconstrained convergence

**Response**: The reviewer correctly identifies that the linear convergence bounds in Theorems 1 and 2 strictly apply to the unconstrained QP. We have added Remark 1 after Theorem 2 clarifying this:

**Remark 1** (Constrained QP convergence). *The bounds $\rho_{\text{GS}} \leq \kappa^2$ and $\rho_J \leq 2\kappa^2$ hold exactly for the unconstrained problem. For the constrained QP, convergence is guaranteed when the active set is stable (i.e., the same constraints are active at the solution across consecutive outer iterations). Near the optimum, active-set stability holds when the strict complementarity condition is satisfied (Nocedal & Wright, 2006, Theorem 16.4). In practice, active sets stabilize within 2–3 outer iterations for all benchmarks (B1–B4) because: (a) warm-starting provides a near-optimal initial active set, and (b) water network constraints (gate limits, level bounds) are typically not simultaneously active at multiple neighboring pools. Table 12 confirms that observed convergence rates match the unconstrained bounds to within 20–30%, validating the practical applicability.*

New reference: Nocedal & Wright (2006).

### M2. ADMM penalty sensitivity

**Response**: We have added Table 14 and Figure 7 showing ADMM outer iterations vs. $\rho/\rho^*$ for B4:

| $\rho / \rho^*$ | Outer iterations | Wall time (ms) | Relative to optimal |
|-----------|--------|---------|------|
| 0.1 | 22.4 | 756 | 2.22× |
| 0.3 | 14.1 | 478 | 1.41× |
| 0.5 | 11.2 | 382 | 1.12× |
| 1.0 | 9.8 | 340 | 1.00× |
| 2.0 | 10.5 | 358 | 1.05× |
| 3.0 | 11.8 | 402 | 1.18× |
| 10.0 | 18.6 | 632 | 1.86× |

The convergence is robust within a factor of 3 around $\rho^*$ (wall time within 20% of optimal). The auto-tuning method (Wohlberg, 2017) consistently selects $\rho$ within $[0.7\rho^*, 1.5\rho^*]$, explaining its near-optimal performance.

---

## Minor Issues

### m1. $\Delta h_{\text{ref}}$ definition

**Response**: Added definition: $\Delta h_{\text{ref}}$ is the nominal head difference across the gate at the operating point (typically 0.1–0.5 m for canal gates).

### m2. Theorem 3 proof

**Response**: Expanded the proof to explicitly connect Boyd et al.'s general ADMM convergence to the water network structure: the tridiagonal coupling means each ADMM consensus update (Step 2) involves only 2 agents per edge (rather than a global consensus), and the warm-starting of dual variables $\mu_{ij}$ from the previous sampling step provides a near-feasible starting point that accelerates dual convergence.
