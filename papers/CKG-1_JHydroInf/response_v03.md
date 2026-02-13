# Response to Reviewer C — Paper CKG-1 (J. Hydroinformatics v02 → v03)

We thank Reviewer C for the cross-disciplinary suggestions that strengthen the paper's impact and positioning.

---

## Major Issues

### M1. Digital Twin Connection

**Response**: Added §7.4 "The MBD Pipeline as a Digital Twin Development Methodology" connecting:
- Layer 7 model + real-time sensor data = descriptive digital twin (monitoring)
- Complete MBD pipeline (L7→L1) = prescriptive digital twin (monitoring + control)
- FMI as the interoperability standard enabling tool-independent digital twin components
- Reference to Liu et al. (2026) for the theoretical DfO-digital twin relationship; this paper provides the first physical demonstration
- The dual-tank HiL deployment is, concretely, a prescriptive digital twin: the OpenModelica model runs in parallel with the physical system (as the Kalman filter prediction model), and the MPC uses this model to compute optimal control actions

### M2. Community Benchmark Framing

**Response**: Added §7.8 "Dual-Tank Platform as a Community Benchmark" with:
- Standardized benchmark protocol: the 16 ODD scenarios as a baseline test suite with defined metrics (RMSE, constraint violations, solve time, settling time, cross-layer degradation)
- Reporting template: Table 11 defines what should be reported for benchmark comparison
- Open invitation: the platform design (dimensions, sensors, actuators), the OpenModelica model, the test scenarios, and the baseline results are all provided in the open repository for community reproduction and extension
- Suggested extensions: additional disturbance scenarios, multi-tank configurations, alternative controllers (PID, RL, data-driven MPC)

---

## Minor Issues

### m1. Abstract Update
**Response**: Updated abstract to reflect 2.0 mm HiL RMSE (with Kalman filter).

### m2. Cross-Layer Fidelity Visualization
**Response**: Added a waterfall panel to Figure 4 showing cumulative RMSE buildup from model validation (1.8 mm) through IDZ identification (+1.2 mm) to HiL deployment (+0.2 mm).

### m3. Broader Impact Statement
**Response**: Added a brief workforce impact paragraph in §7.4: the MBD methodology requires engineers who can work across the full stack (hydraulics + control + software + hardware), highlighting the educational framework established in Liu et al. (2026) and the need for cross-disciplinary training.

---

## Summary of Changes (v02 → v03)

| Change | Section | Type |
|--------|---------|------|
| Digital twin connection | §7.4 (new) | Major |
| Community benchmark framing | §7.8 (new) | Major |
| Abstract HiL RMSE updated | Abstract | Minor |
| Waterfall visualization | Figure 4 caption | Minor |
| Workforce impact | §7.4 | Minor |
