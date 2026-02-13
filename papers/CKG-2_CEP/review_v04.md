# Review Report — Paper CKG-2 (Control Eng. Practice v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor, formal methods specialist
**Date**: 2026-02-13

---

## Overall Assessment

The paper has matured considerably over two revision rounds. The ODD polytope formalization is mathematically sound, the IEC 61511 alignment is appropriate, and the scaling demonstration to 10-pool canal systems is convincing. The Bayesian ODD refinement and digital twin framing add valuable perspective. From a control-theoretic standpoint, two issues require attention.

**Score: 8.0/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. Distance-to-Boundary Function Lacks Formal Guarantee

The distance-to-boundary function $\rho(\mathbf{x})$ (Eq. 10) uses the minimum normalized distance to any constraint. However, the normalization denominators $(b_i - b_{i,\text{nom}})$ are state-dependent if the nominal point is not at the centroid of the polytope. More critically, $\rho$ as defined is not a proper metric in the mathematical sense—it does not satisfy the triangle inequality, and equal $\rho$ values for different constraints do not indicate equal danger. For instance, $\rho = 0.1$ for the water level constraint (which can change rapidly due to integrating dynamics) is more dangerous than $\rho = 0.1$ for a slowly changing constraint. The paper should either: (a) acknowledge this limitation and discuss when it matters, or (b) propose a dynamics-aware distance metric that weights constraints by the maximum rate of change of $\rho_i$, i.e., $\dot{\rho}_i^{\max}$.

### M2. Convergence of Bayesian ODD Refinement Not Proven

The Bayesian ODD refinement framework (§6.7, Eq. 15) is appealing but lacks formal analysis. Does the posterior for SF converge? Under what conditions does the expanded ODD remain safe? The claim that "after three consecutive campaigns with k=0, SF contracts to [1.2, 1.6]" requires specification of the prior (stated: $\mathcal{N}(1.5, 0.04)$) and the likelihood model (not fully specified). A brief proposition or lemma showing that the safety guarantee is preserved under posterior updating would strengthen this contribution.

---

## Minor Issues

### m1. Eq. (15) Likelihood Model

The likelihood $p(k | \text{SF}, N)$ is stated to be "derived from the monotonic relationship between SF and violation probability (Table 9)" but the functional form is not given. Is it binomial with probability $p_v(\text{SF})$ read from Table 9?

### m2. Notation: $\rho_w$ vs. $\delta_s$

The paper introduces $\rho_w$ in Eq. (12) (draft v03) but earlier sections still reference $\delta_s$. The relationship $\rho_w = \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}})$ is stated once but should be emphasized more clearly to avoid confusion.

---

## Summary

Two focused revisions are needed: (1) acknowledge or fix the dynamics-agnostic nature of $\rho$, and (2) formalize the Bayesian ODD expansion guarantee. Both are achievable within a minor revision scope.
