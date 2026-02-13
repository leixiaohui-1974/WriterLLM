# Review Report — Paper YBK-1 (SoftwareX v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

The toolbox is well-designed and the paper clearly describes its architecture and capabilities. The comparison with existing tools, software quality metrics, and scalability data are all adequate. Two minor theoretical concerns remain.

**Score: 8.0/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. QP Solver Numerical Stability

The active-set QP solver (§2.2) with 20 iterations maximum may not converge for poorly conditioned problems. What happens when convergence fails? Is there a fallback (e.g., return last feasible solution)? The paper should state the convergence criterion and the failure handling mechanism.

### M2. State Estimation Robustness

The Kalman filter uses a precomputed steady-state gain. For nonlinear actuator dynamics (e.g., nonlinear gate discharge curves), the linearization may be inaccurate far from the operating point. A brief discussion of when the steady-state Kalman filter is adequate vs. when an Extended Kalman Filter (EKF) should be used would be helpful.

---

## Minor Issues

### m1. Code Generation Determinism

Is the generated code deterministic across MATLAB versions? If a user generates code on R2023b vs. R2024b, will the ST output be identical?

---

## Summary

Two focused additions (QP convergence handling and state estimation robustness) complete the paper.
