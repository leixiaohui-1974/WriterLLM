# Review Report — Paper CKG-1 (J. Hydroinformatics v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

This paper demonstrates the seven-layer MBD framework on a dual-tank platform with MiL→SiL→HiL verification. The cross-layer fidelity analysis is the paper's distinctive contribution. The v03 revision adds useful digital twin positioning and benchmark framing. From a control-theoretic perspective, two issues merit attention: the Kalman filter design should be more carefully justified, and the IDZ model validity should be more precisely bounded. These are precision issues, not structural problems.

**Score: 8.0/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7.5 | Complete pipeline + fidelity analysis is novel |
| Mathematical Rigor | 7 | MPC/Kalman formulation adequate; IDZ validity bounds needed |
| Reproducibility | 8.5 | Open data; benchmark protocol defined |
| Case Validation | 8 | 16 scenarios; MiL/SiL/HiL all quantified |
| Literature Completeness | 8 | Good coverage after v02-v03 additions |
| Writing Quality | 8 | Clear, well-structured |
| System Differentiation | 8 | Digital twin, scaling roadmap, benchmark all effective |

---

## Major Issues

### M1. Kalman Filter Tuning Justification

The Kalman filter is introduced with process noise covariance $Q_k = 0.01I$ and measurement noise covariance $R_k = 0.64 \times 10^{-6}$. These values are stated but not justified:
- How was $Q_k$ determined? It should reflect the IDZ model uncertainty (model mismatch), not be an arbitrary value. A principled approach: estimate $Q_k$ from the IDZ→Saint-Venant residual.
- The ratio $Q_k/R_k$ determines the filter bandwidth; is the current tuning optimal for the dual-tank dynamics?
- Please add a brief sensitivity analysis: how does HiL RMSE vary with $Q_k$? This would quantify the robustness of the Kalman filter tuning.

### M2. IDZ Model Validity Domain

Table 2 reports IDZ parameters at one operating point ($h_0 = 25$ cm, $Q_0 = 0.3$ L/s). The validation shows RMSE increasing from 1.2 mm (nominal) to 2.8 mm (ODD boundary). This operating-point dependence should be characterized more precisely:
- At what operating point does the IDZ model error exceed the MPC's ability to compensate? (i.e., where does closed-loop RMSE exceed the 5 mm threshold?)
- Is the IDZ model gain-scheduled across the ODD, or is a single linearization used? For the dual-tank, the valve characteristic is nonlinear; a single IDZ model may not adequately capture the dynamics across the full ODD range [10, 40] cm.
- Consider reporting the IDZ parameters at 3 operating points (low, nominal, high) to quantify the parameter variation.

---

## Minor Issues

### m1. Equation (2) Valve Model

The valve flow equation uses $\text{sign}(\Delta h) \cdot \sqrt{2g|\Delta h|}$. For numerical implementation, this should be regularized near $\Delta h = 0$ to avoid discontinuous derivatives. Was this done in the OpenModelica model? If so, state the regularization.

### m2. Table 3 Solver

The solver is listed as "quadprog" which is MATLAB's active-set QP solver. The auto-generated C code cannot use quadprog; what QP solver is used in the Arduino implementation? Please clarify.

---

## Summary

The paper is nearing publication quality. The two major issues (Kalman filter justification and IDZ validity domain) require additional analysis paragraphs but no structural changes. The benchmark framing and digital twin positioning are welcome additions.
