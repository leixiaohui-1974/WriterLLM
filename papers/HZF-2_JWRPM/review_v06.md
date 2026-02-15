# Review — HZF-2 Iteration 5

**Reviewer**: C (Cross-Disciplinary Scholar)
**Draft reviewed**: v05
**Score**: 9.0 / 10
**Verdict**: Accept

---

## Summary

This paper presents ParaQP, a parallel QP solver for distributed MPC of water conveyance networks, with three decomposition strategies (Gauss-Seidel, Jacobi, ADMM), formal convergence analysis, and comprehensive benchmarking on 3–50 pool systems. The manuscript has undergone four thorough revision rounds and now represents a mature, well-documented contribution.

## Strengths

1. **Complete theoretical treatment**: Three decomposition strategies with formal convergence proofs, practical Remark 1 on constrained QP applicability, and empirical validation of theoretical bounds (Table 12). The ADMM penalty sensitivity analysis (Table 14) demonstrates robustness.

2. **Comprehensive benchmarking**: Four systems spanning 3 orders of magnitude in complexity, comparison with OSQP/Gurobi (Table 10), HiL validation on a physical flume, and SiL verification at Saint-Venant fidelity via cuSVE integration.

3. **Practitioner-ready**: The deployment guide (§4.4) with strategy selection criteria, early termination guidance, and warm-start verification is exactly what a field engineer needs. The alternative hardware discussion broadens applicability.

4. **Strong positioning**: The neural MPC discussion (§6.6) and heterogeneous agent analysis (§6.7) position the work within both the MPC theory and the practical water systems communities.

5. **Fault tolerance**: The three failure scenarios with quantified impact build confidence for operational deployment.

## Minor Comments (Non-Blocking)

1. A brief comparison of communication overhead between OpenMP shared memory and MPI distributed memory for multi-cabinet installations would be informative for very large systems, though not required for this paper.

## Decision

**Accept**. The paper makes a clear contribution to parallel optimization for water network control, with rigorous theory, extensive validation, and practical deployment guidance. It meets JWRPM standards for both algorithmic novelty and engineering relevance.
