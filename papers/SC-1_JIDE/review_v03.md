# Review Report — Paper SC-1 (J. Irrig. Drain. Eng. v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

The paper provides valuable experimental validation of the CHS unified transfer function framework on a canal flume. The v02 revision substantially improves the paper with ASCE benchmark metrics, backwater coupling quantification, and field-scale comparison. The Muskingum–IDZ duality verification is the paper's most distinctive contribution. Two areas still need attention: the broader impact narrative (connecting to digital water and data-driven methods) and the open-science framing.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | Duality verification is genuinely novel |
| Interdisciplinary Impact | 6.5 | Narrow audience; needs broader framing |
| Reproducibility | 7.5 | Data availability promised; methodology clear |
| Case Validation | 8 | 25 scenarios, 5 OPs, cross-validation |
| Literature Completeness | 7.5 | Improved with Chow; could add Schuurmans 1997 |
| Writing Quality | 7.5 | Clear but dense in §3 |
| Broader Framing | 6 | Missing digital water/AI connections |

---

## Major Issues

### M1. Broader Impact: From Canal Automation to Digital Water

The paper is narrowly framed as a canal control validation study. For J. Irrig. Drain. Eng. readership (which includes both traditional and digital-oriented engineers), the paper should connect to the broader "digital water" narrative:
- How does the IDZ identification methodology relate to data-driven / machine learning approaches? Could the IDZ parameters be estimated online using recursive least squares or Kalman filtering?
- The Muskingum–IDZ duality has implications beyond canal control — it means that any system with calibrated Muskingum parameters (thousands of river reaches worldwide) immediately has IDZ control models available. This "ready-made control model" angle is powerful and underemphasized.
- Consider adding a short paragraph on how the experimental methodology could integrate with SCADA data from operational canals.

### M2. Open-Science and Community Benchmark

The data availability statement promises a GitHub repository, but the paper does not provide a standardized benchmark protocol (unlike Chen et al., 2026, which proposes Table 11 for the dual-tank). For J. Irrig. Drain. Eng., which has a strong community tradition of shared test cases (ASCE Test Canal):
- Propose a standardized flume benchmark protocol with reporting metrics
- Include the specific data formats and scenario definitions that would enable replication

---

## Minor Issues

### m1. Abstract Length

The abstract is 195 words, within the 200-word ASCE limit, but could be tightened. The phrase "non-self-regulating" is redundant with "integrating" in the abstract context.

### m2. Table 12 — Add Schuurmans (1997)

Schuurmans (1997) is a key early ASCE canal automation study that should be in the comparison table.

### m3. Conclusion Finding 3 — Update Scenario Count

Finding 3 should reference 25 ODD scenarios (not 24, since S25 was added in v02).

---

## Summary

The paper has a strong experimental core with a genuinely novel duality verification. Broadening the impact narrative and strengthening the open-science framing would make it a more complete contribution.
