# Review — HZF-2 Iteration 2

**Reviewer**: C (Cross-Disciplinary Scholar)
**Draft reviewed**: v02
**Score**: 7.5 / 10
**Verdict**: Minor Revision

---

## Summary

This paper presents ParaQP, a parallel QP solver for distributed MPC of water conveyance networks with three decomposition strategies (Gauss-Seidel, Jacobi, ADMM). The major revision substantially improved the manuscript: commercial solver comparison, fault tolerance analysis, HiL validation, resource utilization, and reduced self-citation rate all strengthen the contribution. The paper is now technically sound but needs refinement in two areas: the relationship to learning-based control and the scalability to heterogeneous networks.

## Major Issues

### M1. No discussion of learning-based alternatives to QP-based MPC
The paper positions ParaQP within a classical optimization framework. However, recent work on neural network-based approximate MPC (e.g., Karg & Lucia, 2020; Chen et al., 2022) offers microsecond-level inference that could replace QP solving entirely for well-characterized systems. The paper should:
- Discuss neural MPC as a computational alternative
- Explain when QP-based DMPC remains preferable (safety guarantees, constraint satisfaction, interpretability)
- Position ParaQP within a hybrid architecture where neural controllers handle routine operation and QP solvers are used for safety-critical or out-of-distribution scenarios

**Required**: Add a subsection in §6 comparing QP-based DMPC with neural MPC approaches.

### M2. Heterogeneous agent models not addressed
The paper assumes all pools use the same IDZ model structure. Real networks may include:
- Family α (integrating) pools alongside Family β (self-regulating) pools
- Pools with nonlinear gate hydraulics requiring different QP structures
- Mixed sampling rates (e.g., 10 s for short pools, 60 s for long pools)

How does ParaQP handle heterogeneous agent models? Do the convergence proofs (Theorems 1–3) still hold when local QPs have different dimensions or structures?

**Required**: Discuss heterogeneous agent support, either as a current capability or as a stated limitation.

## Minor Issues

### m1. No convergence rate comparison with theory
Table 1 shows empirical outer iterations, but the paper does not compare these against the theoretical bounds from Theorems 1–3. Computing the predicted spectral radius $\rho_{\text{GS}} = \kappa^2$ for each benchmark and comparing against the observed convergence rate would validate the theory.

### m2. Figure 6 not clearly described
Figure 6 (coupling strength vs. pool length) is referenced in §2.4 but the figure caption does not specify the exact parameter values used ($A_s$ range, gate coefficients, $Q/R$ ratio). Readers cannot reproduce this plot.

### m3. Energy consumption analysis sparse
Power consumption is mentioned briefly (0.07 W for B4) but not systematically compared across platforms. A comparison of energy per DMPC cycle (Joules/cycle) across the three hardware platforms would help practitioners select appropriate hardware for remote installations.

### m4. Missing notation for junction constraints
Equations 20–21 use $\mathcal{U}(j)$ and $\mathcal{D}(j)$ notation that is not defined in the notation section. Define these sets formally.

### m5. Abstract length
The abstract is 198 words, close to the JWRPM limit of 200 words. With the new content (HiL, solver comparison), consider whether the abstract needs tightening or restructuring.

## Recommendation

**Minor Revision**. The paper is technically solid after the major revision. Addressing the learning-based alternative discussion and heterogeneous agent support will position the work more strongly within the broader control community.
