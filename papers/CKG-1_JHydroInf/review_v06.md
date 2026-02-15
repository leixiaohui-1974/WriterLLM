# Review Report — Paper CKG-1 (J. Hydroinformatics v05)

**Iteration**: 5 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

This paper has developed into a thorough and well-structured demonstration of the MBD framework for water systems control. The v04–v05 revisions have addressed all previously raised concerns: the Kalman filter is now properly justified with sensitivity analysis, the IDZ model validity is characterized across operating points, and the conclusions are internally consistent. The digital twin framing, community benchmark proposal, and cost scaling information make the paper accessible to a broad audience beyond pure control theory. I recommend acceptance.

**Score: 9.0/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | First complete MBD pipeline on physical water hardware |
| Interdisciplinary Impact | 9 | Bridges control, software, hardware, hydraulics |
| Reproducibility | 9.5 | Open data, benchmark protocol, 16 scenarios, reporting template |
| Case Validation | 9 | MiL/SiL/HiL + Kalman sensitivity + IDZ variation |
| Literature Completeness | 8.5 | Comprehensive for the scope |
| Writing Quality | 8.5 | Clear, well-organized, appropriate length |
| Broader Framing | 9 | Digital twin, workforce, benchmark, scaling — all effective |

---

## Major Issues

None.

---

## Minor Issues

None requiring revision. The paper is ready for publication.

---

## Commendations

1. **Table 3b (Kalman filter sensitivity)** is an excellent addition that quantifies robustness without over-claiming optimality.
2. **Table 2b (IDZ parameter variation)** clearly demonstrates why a single linearization suffices for the defined ODD while honestly acknowledging when gain scheduling would be needed.
3. The **community benchmark proposal** (§7.7) with standardized reporting template (Table 11) could catalyze reproducible research in water systems control — a field that has historically lacked such benchmarks.
4. The **cost column** in Table 10 is a simple but effective addition for bridging the academic-practitioner gap.

## Summary

The paper presents a complete, reproducible, and well-validated MBD pipeline for water systems control. The dual-tank demonstration, while intentionally simplified, establishes the methodology and baseline metrics that future work can build upon. Accept.
