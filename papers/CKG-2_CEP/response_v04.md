# Point-by-Point Response — CKG-2 Iteration 3

**Reviewer**: A (Control Theorist)
**Draft**: v03 → v04

---

## Major Issues

### M1. Dynamics-Aware Distance-to-Boundary

**Response**: Accepted. Added §3.3.1 "Dynamics-Aware Weighting" after Eq. (11):
- Acknowledged that $\rho$ as defined is not dynamics-aware: rapidly changing states (e.g., water level under full pump flow) reach the boundary faster than slowly changing states
- Introduced weighted distance: $\rho_w(\mathbf{x}) = \min_i \frac{b_i - \mathbf{a}_i^T \mathbf{x}}{(b_i - b_{i,\text{nom}}) \cdot w_i}$ where $w_i = \dot{x}_{i,\max} / \dot{x}_{\text{ref}}$
- For dual-tank: $w_{h_1} = (Q_{\max}/A_s) / (Q_{\text{nom}}/A_s) = 1.67$ (water level changes fast), $w_u = \Delta u_{\max} / \Delta u_{\text{nom}} = 2.0$ (valve rate high)
- Table 2b: Weighted vs. unweighted $\rho$ for scenarios S11, S17, S31 — weighted version predicts violations 0.5 intervals earlier on average
- Noted that for the dual-tank (dominated by water level constraints), the practical improvement is modest; the weighting becomes more important for multi-dimensional systems with heterogeneous dynamics

### M2. Bayesian ODD Expansion Guarantee

**Response**: Accepted. Added Proposition 1 in §6.7:
- Specified likelihood: $p(k | \text{SF}, N) = \binom{N}{k} p_v(\text{SF})^k (1 - p_v(\text{SF}))^{N-k}$ where $p_v(\text{SF})$ is the violation probability interpolated from Table 9
- Proposition 1: "If the prior $\text{SF}_0$ satisfies $P(\text{PFD}(\text{SF}_0) < 10^{-1}) > 1 - \epsilon$ and the likelihood is monotonically decreasing in SF for $k=0$, then the posterior SF after observing $k=0$ in $N$ scenarios also satisfies the SIL-1 constraint: $P(\text{PFD}(\text{SF}_{\text{post}}) < 10^{-1}) > 1 - \epsilon$."
- Proof: The posterior shifts SF downward (toward less conservative), but the shift is bounded by the prior support. Since PFD is monotonically increasing as SF decreases, the SIL-1 constraint is preserved if the prior's lower support bound exceeds the critical SF (SF = 1.0 from Table 9).
- Convergence: posterior variance decreases as $O(1/N)$; after 3 campaigns ($N=48$), 95% CI width is ~0.3

---

## Minor Issues

### m1. Eq. (15) Likelihood

**Response**: Added explicit functional form as described above (binomial with $p_v(\text{SF})$ from Table 9 interpolation).

### m2. $\rho_w$ vs. $\delta_s$ Notation

**Response**: Unified notation throughout: defined $\rho_w$ once in §3.4 (Eq. 12) with the explicit formula $\rho_w = \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}})$, then used only $\rho_w$ in all subsequent text. Added $\rho_w$ to the Notation table.
