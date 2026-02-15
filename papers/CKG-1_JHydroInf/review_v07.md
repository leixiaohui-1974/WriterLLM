# Review Report — Paper CKG-1 (J. Hydroinformatics v05)

**Iteration**: 6 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

The authors have thoroughly addressed both major issues from my previous review. The Kalman filter tuning is now grounded in measured system characteristics (IDZ-to-SV residual for $Q_k$, static sensor calibration for $R_k$) with a sensitivity analysis that demonstrates robustness across order-of-magnitude variations. The IDZ parameter variation table (Table 2b) clearly shows that the single-linearization approach is justified within the defined ODD, while honestly acknowledging the need for gain scheduling at larger scales. The valve regularization and QP solver clarifications are correctly stated. The paper is technically sound and makes a clear contribution.

**Score: 9.0/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | Complete pipeline is the novelty, not any single component |
| Mathematical Rigor | 8.5 | Kalman justification + IDZ validity now adequate |
| Reproducibility | 9 | Open data, all parameters stated, benchmark protocol |
| Case Validation | 9 | Comprehensive xIL + sensitivity + operating point variation |
| Literature Completeness | 8.5 | Good |
| Writing Quality | 8.5 | Well-structured, appropriate detail level |
| Technical Correctness | 9 | All formulations verified, solver clarified |

---

## Major Issues

None.

---

## Minor Issues

None requiring revision. The paper is ready for publication.

---

## Comments for the Record

The five-limitation paragraph in §7.8 (now including gain scheduling as the fifth point) demonstrates appropriate scientific humility. The progression from dual-tank to multi-pool (CKG-2/3) is a logical research agenda. The cross-layer fidelity analysis (Table 9) remains the paper's most distinctive contribution — I am not aware of analogous quantification in the water systems literature.

## Summary

Accept. The paper provides a solid methodological contribution to the water systems engineering literature, demonstrating that MBD principles from automotive/aerospace can be successfully adapted to water infrastructure control.
