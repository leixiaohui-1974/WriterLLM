# Review Report — Paper SC-1 (J. Irrig. Drain. Eng. v01)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

This paper presents experimental validation of the CHS unified transfer function family on a three-pool canal flume, with a novel Muskingum–IDZ duality verification and a DMPC demonstration. The experimental work is solid, and the three-contribution structure is clear. However, several issues need attention: the practical relevance to field-scale canals needs strengthening, the DMPC coordination scheme is too simple for the claimed generality, and the paper needs better comparison with existing ASCE canal control benchmarks.

**Score: 6.5/10**
**Verdict: Major Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7 | Duality verification is genuinely novel |
| Practical Applicability | 5.5 | Laboratory scale only; field relevance unclear |
| Reproducibility | 7 | Parameters stated; data availability promised |
| Case Validation | 6.5 | 24 scenarios but only rectangular prismatic channel |
| Literature Completeness | 6 | Missing key ASCE canal control references |
| Writing Quality | 7.5 | Clear structure, adequate detail |
| System Differentiation | 6.5 | Needs stronger contrast with van Overloop/Clemmens |

---

## Major Issues

### M1. Missing ASCE Test Canal Benchmarks

The ASCE canal control test cases (Clemmens et al., 2005) define standardized benchmark scenarios that are the community standard for evaluating canal controllers. The paper cites Clemmens et al. but does not compare against the ASCE benchmark results. Please:
- Map your 24 scenarios to the ASCE test case categories (e.g., scheduled changes, unscheduled changes, unknown disturbances)
- Report your DMPC results in the ASCE standard metrics (MAE, IAE) in addition to RMSE
- Discuss how your results compare with the performance reported in the ASCE benchmark literature

### M2. Non-Iterative DMPC Justification

The non-iterative sequential DMPC scheme (upstream solves first, passes trajectory to downstream) is presented without adequate justification:
- What happens when backwater effects are significant? The downstream agent's actions affect the upstream pool through backwater, which the sequential scheme ignores.
- Please quantify the backwater coupling strength in your flume (ratio of backwater-induced level change to gate-induced level change) and relate this to the DMPC degradation.
- Consider adding at least one scenario where backwater effects are deliberately amplified (e.g., high tailwater, subcritical flow) to test the sequential scheme's limits.

### M3. Field-Scale Relevance

The paper claims the results "establish the experimental foundation for the CHS unified framework" but the laboratory flume has a simple rectangular cross-section, controlled environment, and short pools (4 m). To strengthen the claim:
- Discuss how the IDZ parameter variation (Tables 3-4) compares with field-scale canal data (e.g., from ASCE test canal or published field data)
- Provide a scaling analysis: what pool length, flow rate, and time constants would a typical irrigation canal have, and how do these relate to the flume parameters?
- Acknowledge more explicitly the limitation of prismatic geometry

### M4. Muskingum Estimation Methodology

The Muskingum parameter estimation uses both graphical and least-squares methods but does not report which method produces the results in Table 6. Also:
- The graphical method is known to be sensitive to the choice of X; please report the estimation uncertainty
- Only 5 triangular hydrographs per OP is reported; what are the confidence intervals on K and X?
- The triangular hydrograph (peak 2× base flow) may not adequately represent the gradual flow changes typical of canal operations

### M5. Sensor Specification Gap

Capacitance-type level sensors are specified (±0.5 mm, 10 Hz) but:
- What is the sensor mounting configuration (flush-mounted, stilling well)?
- Is the 10 Hz data filtered before IDZ identification? If so, what filter?
- The electromagnetic flowmeter accuracy (±1%) at 0.5 L/s means ±5 mL/s uncertainty — how does this propagate to the gate gain estimation?

---

## Minor Issues

### m1. Table 2 — Missing Pool 3 Control

Pool 3 has no upstream gate (it's downstream of G2). How is Pool 3 level controlled? Is it uncontrolled (slave to G2 discharge + fixed weir)? This should be stated explicitly.

### m2. Eq. (6) — DMPC Cost Function Consistency

Eq. (6) uses $\alpha_y$ and $\alpha_u$ notation, but the CHS convention (P1a §6.2) uses $Q_i$ and $R_i$ for output and input weights. Please align notation with the established CHS convention.

### m3. Table 7 — Prediction Horizon Justification

The prediction horizon is 100 s (20 × 5 s). The theoretical justification is that it should be ≥ 2× the longest transport delay. The longest delay is 30.2 s (Pool 2, OP1), so 2× = 60.4 s. Why was 100 s chosen rather than a tighter 65 s (13 steps)?

### m4. Manning's n Value

Manning's n = 0.010 is stated for a glass flume. The standard value for smooth glass is 0.009–0.011. Was this measured or assumed? If measured, describe the method.

---

## Summary

The paper has a strong experimental core but needs better positioning within the ASCE canal control literature, stronger field-relevance discussion, and more rigorous treatment of the DMPC coordination scheme. The Muskingum–IDZ duality verification is a genuinely novel contribution that should be preserved and strengthened.
