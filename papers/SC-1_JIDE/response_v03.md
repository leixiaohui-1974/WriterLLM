# Response to Reviewer C — Paper SC-1 (J. Irrig. Drain. Eng. v02 → v03)

We thank Reviewer C for the constructive suggestions on broadening the paper's impact.

---

## Major Issues

### M1. Broader Impact: Digital Water and Data-Driven Connections

**Response**: Added §7.5 "From Experimental Identification to Operational Deployment" with three new paragraphs:

1. **IDZ vs. data-driven**: The IDZ model is physics-informed (structure from Saint-Venant, parameters from data). Compared to purely data-driven approaches (neural networks, Gaussian processes), the IDZ has three advantages: (a) physical interpretability (each parameter maps to a hydraulic property), (b) transferability across operating points (the structure is invariant; only parameters change), and (c) minimal data requirements (one step-response per pool). Online parameter updating via recursive least squares is straightforward and would enable the IDZ model to track slow changes (sedimentation, vegetation growth).

2. **Ready-made control models from Muskingum data**: As the reviewer notes, thousands of river reaches worldwide have calibrated Muskingum parameters from decades of flood routing studies. Via the duality (Eq. 5), each calibrated Muskingum model immediately provides an IDZ control model. This means that real-time control could be deployed on these reaches without additional identification campaigns — a powerful practical implication.

3. **SCADA integration**: For operational canals with existing SCADA systems, the step-response identification methodology can be applied using routine gate operation data (gate adjustments made by operators), avoiding the need for dedicated identification experiments. The 600-s observation window and three-parameter fitting are compatible with standard SCADA data logging intervals.

### M2. Community Benchmark Protocol

**Response**: Added §7.8 "Canal Flume Benchmark Protocol" with Table 14 (reporting template) specifying: the 25 ODD scenarios, standard metrics (RMSE, MAE, IAE, settling time, constraint violations), data formats (CSV with timestamp, gate opening, water levels, flow rates), and scenario definition files. The protocol is modeled on Chen et al. (2026, Table 11) and the ASCE test case tradition.

---

## Minor Issues

### m1. Abstract Tightened

**Response**: Removed "non-self-regulating" parenthetical; abstract now 188 words.

### m2. Table 12 — Schuurmans Added

**Response**: Added Schuurmans et al. (1999) to Table 12 (decentralized PI, single-pool canal, RMSE ~6 mm).

### m3. Conclusion — 25 Scenarios

**Response**: Finding 3 updated to "25 ODD scenarios."

---

## Summary of Changes (v02 → v03)

| Change | Section | Type |
|--------|---------|------|
| Digital water / data-driven connections | §7.5 | Major |
| Ready-made control models from Muskingum | §7.5 | Major |
| SCADA integration discussion | §7.5 | Major |
| Benchmark protocol + Table 14 | §7.8 | Major |
| Abstract tightened | Abstract | Minor |
| Schuurmans added to Table 12 | §7.4 | Minor |
| Conclusion scenario count corrected | §8 | Minor |
| 1 new reference (Schuurmans et al. 1999) | References | Minor |
