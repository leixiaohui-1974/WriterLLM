# Review — HZF-2 Iteration 3

**Reviewer**: A (Control Theorist)
**Draft reviewed**: v03
**Score**: 8.0 / 10
**Verdict**: Minor Revision

---

## Summary

This paper presents ParaQP, a parallel QP solver for distributed MPC of water conveyance networks. The three decomposition strategies (Gauss-Seidel, Jacobi, ADMM) are mathematically well-developed, and the convergence analysis (Theorems 1–3 with Table 12 validation) is convincing. The additions of neural MPC positioning (§6.6) and heterogeneous agent discussion (§6.7) strengthen the paper. Two issues remain concerning the theoretical analysis.

## Major Issues

### M1. Convergence proof for Theorem 2 assumes unconstrained QP
The proof sketch for Theorem 2 (Jacobi convergence) invokes the spectral radius of the Jacobi splitting $\mathbf{M}_J = \mathbf{D}^{-1}(\mathbf{L} + \mathbf{U})$, which applies to the unconstrained QP. When active constraints change between iterations (different active sets at different agents), the iteration becomes a nonlinear mapping and the linear convergence bound $\rho_J \leq 2\kappa^2$ is not guaranteed. The authors should either:
- Provide a convergence result for the constrained case (e.g., using variational inequality theory)
- Explicitly state the assumption that active sets are stable near the optimum and argue that this holds for typical water network operating conditions

**Required**: Clarify the constrained vs. unconstrained applicability of Theorems 1–2.

### M2. ADMM penalty sensitivity not quantified
Theorem 3 gives the optimal penalty $\rho^* = \sqrt{\lambda_{\min}(H_i) \cdot \lambda_{\max}(H_i)}$, and §4.1 mentions auto-tuning achieves "within 8% of oracle-optimal." However, the sensitivity of convergence speed to $\rho$ misspecification is not shown. A plot of outer iterations vs. $\rho/\rho^*$ for benchmark B4 would demonstrate robustness (or sensitivity) to penalty selection.

**Required**: Add sensitivity analysis for ADMM penalty parameter.

## Minor Issues

### m1. Notation inconsistency in Eq. 10
Equation 10 introduces $\Delta h_{\text{ref}}$ without formal definition. Is this the reference head difference across the gate, the pool depth, or something else?

### m2. Theorem 3 proof is too brief
The proof simply cites Boyd et al. (2011, §3.2), but the water network QP has additional structure (tridiagonal coupling, warm-starting) not covered by the general ADMM convergence theorem. A brief argument connecting the general result to the specific problem structure would strengthen the claim.

## Recommendation

**Minor Revision**. The convergence analysis needs clarification on constrained QP applicability and ADMM sensitivity. These are addressable issues that do not require new experiments.
