# Review Report — Paper CKG-1 (J. Hydroinformatics v04)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The paper has matured significantly since my first review. The scaling roadmap, industrial deployment discussion, and MBD vs. traditional comparison addressed my earlier concerns about practical relevance. The v04 additions (Kalman filter sensitivity analysis, IDZ parameter variation across operating points, QP solver clarification) demonstrate solid engineering rigor. From an industry perspective, this is now a convincing proof-of-concept paper with a clear path toward deployment.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7.5 | Complete pipeline demonstration is the contribution |
| Practical Applicability | 8.5 | Industrial roadmap is clear and credible |
| Reproducibility | 9 | Open data + benchmark protocol + 16 scenarios |
| Case Validation | 8.5 | Comprehensive xIL chain with Kalman sensitivity |
| Literature Completeness | 8 | Good coverage |
| Writing Quality | 8 | Clear; minor tightening possible |
| Industry Relevance | 8.5 | Arduino→PLC pathway well articulated |

---

## Major Issues

None. The major issues from my first review (dual-tank simplicity justification, Arduino vs. industrial, comparison with alternatives, sensor noise) have all been adequately addressed in v02–v04.

---

## Minor Issues

### m1. Conclusions Section — Update HiL Numbers

The Conclusions (§8, finding 1) still reference "water level RMSE of 2.3 mm (mean) and 4.1 mm (worst case)" which are the pre-Kalman-filter values from v01. The body text (Table 8) shows 2.0 mm mean and 3.8 mm worst case with Kalman filter. Please update the Conclusions to be consistent with the body.

### m2. Table 10 — Add Cost Column

The MBD Complexity Scaling table (Table 10) would benefit from an approximate hardware cost column, giving readers an immediate sense of the investment required at each scale level. For example: dual-tank ~$200, 3-pool flume ~$5k, field system ~$500k+. This helps utility managers assess feasibility.

---

## Summary

The paper is ready for publication with two minor corrections. The complete MBD pipeline demonstration, cross-layer fidelity analysis, and community benchmark proposal make a solid contribution to the water systems engineering literature.
