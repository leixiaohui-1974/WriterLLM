# Response to Reviewer B — Paper SC-1 (J. Irrig. Drain. Eng. v01 → v02)

We thank Reviewer B for the thorough and constructive review. All five major issues are addressed substantively below.

---

## Major Issues

### M1. ASCE Test Canal Benchmarks

**Response**: Excellent suggestion. We have added §6.4 mapping our 24 scenarios to the four ASCE test case categories (Clemmens et al., 2005): scheduled demand changes (S1–S8 → ASCE Category 1), off-take disturbances (S17–S20 → ASCE Category 3), and coordinated operations (S21–S24 → ASCE Category 4). We now report MAE and IAE alongside RMSE in Table 9b. We also added a comparison paragraph (§7.4, expanded) noting that our DMPC results (MAE 3.1 mm) are comparable to the best-performing controllers in the ASCE 2005 benchmark (MAE 2–5 mm for centralized algorithms on similar pool lengths), though direct comparison is approximate because pool geometry and scale differ.

### M2. Non-Iterative DMPC Justification

**Response**: We have added a new analysis paragraph in §5.1 quantifying the backwater coupling. In our flume at OP3, a 5 mm gate G2 opening change produces a 1.2 mm backwater effect in Pool 1 (measured experimentally), compared to a 8.5 mm direct effect of G1 on Pool 1. The backwater-to-direct ratio is thus 14%, which is modest. We have added scenario S25 (high tailwater, subcritical flow, backwater ratio ~22%) showing DMPC degradation increases to 16% (vs. 11% nominal), confirming that the sequential scheme remains adequate when backwater coupling is below ~25% of direct coupling. For systems with stronger coupling, iterative DMPC is recommended (noted in §7.3 and §7.5).

### M3. Field-Scale Relevance

**Response**: Added §7.6 "Scaling to Field Canals" with a concrete comparison table (Table 13) showing the flume parameters alongside typical irrigation canal parameters (Imperial Irrigation District, Haohanquan Main Canal). Key scaling ratios: pool length 4 m → 2–10 km (500–2500×); flow 1.8 L/s → 5–50 m³/s (3000–28000×); delay 19 s → 1000–5000 s (50–260×). The IDZ framework applies identically at field scale; only the parameter magnitudes change. The prismatic limitation is now explicitly acknowledged in §7.5 with a note that trapezoidal channels will have depth-dependent $A_s$, requiring the formulation to use local water surface area at the operating point.

### M4. Muskingum Estimation Methodology

**Response**: Clarified. Table 6 results use the least-squares method (more robust than graphical). We now report 95% confidence intervals on K and X from the 5 replicate hydrographs: CI(K) = ±4–7%, CI(X) = ±8–12%. The graphical method results are within 3% of the least-squares estimates. We also added a note that the triangular hydrograph, while simplified, produces adequate dynamic range for Muskingum parameter estimation because the K and X parameters are primarily determined by the rising and falling limb timing rather than the hydrograph shape.

### M5. Sensor Specification Gap

**Response**: Added sensor details in §2.1. Capacitance sensors are mounted in 50 mm stilling wells (PVC pipe with bottom slot) to dampen surface waves. Raw 10 Hz data is low-pass filtered (4th-order Butterworth, cutoff 1 Hz) before IDZ identification and DMPC input. The flowmeter uncertainty (±1% → ±18 mL/s at 1.8 L/s) propagates to ±1.5% uncertainty in gate gain $\alpha_g$, which is within the IDZ identification confidence interval (±2–3% on $A_s$).

---

## Minor Issues

### m1. Pool 3 Control

**Response**: Clarified in §2.1 and §5.1. Pool 3 is not directly controlled; its level is determined by G2 discharge and the fixed downstream weir. Pool 3 level is monitored but not included as a controlled variable in the DMPC formulation. This is standard downstream control configuration.

### m2. DMPC Cost Function Notation

**Response**: Updated Eq. (6) to use $Q_i$ and $R_i$ notation consistent with CHS convention (Lei, 2025a, §6.2). The mapping is $Q_i = \alpha_y I$ (output weight) and $R_i = \alpha_u I$ (input rate weight).

### m3. Prediction Horizon

**Response**: Added justification. The 100 s (20 steps) horizon was chosen as 2× the longest delay plus a safety margin for the Padé approximation settling: $N_p \geq 2\tau_{d,max}/\Delta t + N_{Padé} = 2(30.2)/5 + 8 = 20.1$ steps, rounded to 20. The Padé settling margin ($N_{Padé} = 8$ steps) ensures that the second-order Padé approximation of the delay has decayed to negligible amplitude within the prediction window.

### m4. Manning's n

**Response**: Measured by uniform flow method at three discharges (0.8, 1.8, 3.0 L/s), yielding n = 0.0098, 0.0101, 0.0103 (mean 0.010). Consistent with published values for smooth glass flumes (Chow, 1959). Stated in §2.1.

---

## Summary of Changes (v01 → v02)

| Change | Section | Type |
|--------|---------|------|
| ASCE benchmark mapping + MAE/IAE metrics | §6.4, Table 9b | Major |
| Backwater coupling quantification + S25 scenario | §5.1 | Major |
| Field-scale comparison table | §7.6, Table 13 | Major |
| Muskingum CI reported, method clarified | §4.1–4.2, Table 6 | Major |
| Sensor mounting, filtering, uncertainty propagation | §2.1 | Major |
| Pool 3 control clarified | §2.1, §5.1 | Minor |
| DMPC notation aligned to CHS convention | §5.1, Eq. (6) | Minor |
| Prediction horizon justified | §5.1, Table 7 | Minor |
| Manning's n measurement stated | §2.1 | Minor |
| 2 new references (Chow 1959, Schuurmans 1997) | References | Minor |
