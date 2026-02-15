# Review Report — Paper P-DC (EMS v05)

**Iteration**: 6 of 20+
**Reviewer**: A (Control Theorist) — European professor, 2nd review
**Date**: 2026-02-13

---

## Overall Assessment

This is my second review of this paper (first review: iteration 3, score 7.5/10, Minor Revision). My previous concerns have been addressed satisfactorily:

- **Gramian evaluation**: P1 and P2 now specify worst-case evaluation over ODD vertices with $\sigma_{min}(W_c) = \min_{p \in \mathcal{V}(ODD)} \sigma_{min}(W_c(p))$ and condition number from balanced realization. The threshold $\gamma_c = Q_{max}^2 / (N \cdot \Delta t)$ is physically motivated. ✓
- **Five-level hierarchy mapping**: Table 0 explicitly maps LSV→IDZ→ID→I→SS to MBD Layers 7–6, with Theorem 3 cited. This grounds the MBD framework in the CHS theoretical foundation. ✓
- **IDZ identification**: Levenberg-Marquardt with time-domain RMSE criterion, 95% confidence intervals stated, ±10% sensitivity on $A_s$ confirmed within threshold. Litrico & Fromion (2009) methodology cited. ✓
- **Preissmann θ**: Specified as 0.6 with justification. ✓
- **ODD coverage ratio**: Redefined as discrete grid fraction. Clean and consistent. ✓
- **MPC horizon**: Formal delay-compensation condition cited. ✓
- **Data-driven safety**: Statistical validation vs. formal guarantee distinction made explicit. ✓

Additionally, Reviewer B's industry adoption pathway and cost-benefit framing (added in v05) enhance the paper's practical relevance without compromising theoretical rigor.

The paper now provides a well-grounded bridge between CHS theory (Lei, 2025a) and engineering practice. The mathematical specifications are precise. The five-level hierarchy mapping ensures consistency with the parent theory. The reference workflow provides credible quantitative validation. The cross-disciplinary extensions (digital twins, ML, competency framework) are additive and well-integrated.

I have no remaining substantive concerns.

**Score: 9.0/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8.5 | DfO with formal metrics is a genuine contribution |
| Mathematical Rigor | 8.5 | Gramian specifications, IDZ methodology, sensitivity all precise |
| Reproducibility | 8.5 | Detailed reference workflow; open-source pipeline |
| Case Validation | 8 | Single case, but thorough with sensitivity analysis |
| Literature Completeness | 8.5 | Good cross-domain; Litrico & Fromion for IDZ methodology |
| Writing Quality | 9 | Clear, precise, well-organized |
| System Differentiation | 9 | Five-level mapping, digital twin, cross-domain comparison all effective |

---

## Major Issues

None.

---

## Minor Issues

### m1. Notation Consistency with P1a

A minor suggestion for the final manuscript: ensure that all mathematical notation (particularly $A_s$, $\tau_d$, $\tau_m$, $G(s)$, $H(s)$) is typographically consistent with Lei (2025a) to facilitate cross-referencing between the CHS papers. This is a copy-editing matter rather than a revision requirement.

---

## Summary

This paper successfully bridges the gap between CHS theory and engineering practice. The DfO paradigm provides a structured design philosophy, the MBD framework provides an implementable engineering pipeline, and the competency framework provides an educational foundation. The mathematical specifications have been tightened to the level required for a control-theory audience while remaining accessible to the EMS readership. I recommend acceptance.
