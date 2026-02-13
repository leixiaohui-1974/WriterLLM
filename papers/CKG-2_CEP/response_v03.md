# Point-by-Point Response — CKG-2 Iteration 2

**Reviewer**: C (Cross-disciplinary Scholar)
**Draft**: v02 → v03

---

## Major Issues

### M1. Learning-Based ODD Expansion Pathway

**Response**: Accepted. Added §6.7 "Data-Driven ODD Refinement":
- Bayesian framework for safety margin updating: posterior SF = prior SF × likelihood(observed violations)
- After N SiL campaigns with zero violations at SF=1.5, posterior can tighten to SF=1.3 (expanding ODD by ~7%)
- Conversely, if violation rate exceeds expected (e.g., due to model degradation), SF increases automatically
- Connects to safe RL (Garcia & Fernandez, 2015): ODD boundary as constraint for Constrained MDP
- Formal criterion: expand ODD only if 95% credible interval for PFD remains < SIL-1 threshold
- Notes that CKG-3 will implement one ODD expansion cycle on the physical platform

### M2. Digital Twin Positioning

**Response**: Accepted. Added §6.8 "ODD-Monitored Digital Twin":
- Reframed SiL architecture as a "safety-certified digital twin" (SCDT)
- Three capabilities beyond standard DT: (1) real-time ODD monitoring, (2) boundary violation prediction, (3) safety certificate (verified scenario set)
- Connected to digital twin literature: Rasheed et al. (2020), Lei et al. (2025b, §5.3 digital twin for water networks)
- Noted that SCDT enables "what-if" scenario testing: operators can test proposed reference changes against ODD before execution
- Added reference: Rasheed, A., San, O., & Kvamsdal, T. (2020). Digital twin: Values, challenges and enablers. IEEE Access.

---

## Minor Issues

### m1. Robust MPC / Tube MPC Comparison

**Response**: Added paragraph in §6.1 comparing ODD monitoring vs. tube MPC:
- Tube MPC (Mayne et al., 2005) tightens constraints internally to guarantee robust feasibility
- ODD monitoring operates externally to the MPC as a supervisory layer
- Complementary: tube MPC handles bounded uncertainties within ODD; ODD monitor handles scenarios where the plant leaves the tube MPC's assumed disturbance set
- Added reference: Mayne, D.Q., Seron, M.M., & Raković, S.V. (2005)

### m2. FAIR Data Compliance

**Response**: Updated Data Availability section:
- Zenodo DOI for archival snapshot (DOI: 10.5281/zenodo.XXXXXXX, to be minted)
- MIT license for code, CC-BY-4.0 for data
- FAIR metadata: README with variable descriptions, scenario parameters, and reproduction instructions

### m3. ODD Visualization

**Response**: Added Figure 5: 2D projection of ODD in ($h_1$, $h_2$) plane with:
- Green polytope interior (NOMINAL zone)
- Yellow annulus (WARNING zone, $\rho < 0.13$)
- Red boundary ($\rho = 0$, ODD limit)
- Gray exterior (VIOLATION zone)
- Overlaid trajectories from S1 (nominal), S11 (near-boundary), S17 (violation + recovery)
- Color-coded $\rho$ heatmap in background

### m4. Broader Impact Statement

**Response**: Added paragraph before Conclusions:
- ODD formalization for water → climate adaptation (verified operation under extreme conditions)
- SDG 6 alignment: autonomous control reduces water losses (2-5% improvement demonstrated in P2C)
- Democratization: formal safety framework lowers barrier to autonomous deployment in developing regions

### m5. Table 1c Extrapolation Basis

**Response**: Added footnote to Table 1c: "50-pool and 500-pool values estimated by linear scaling with constraint count (verified up to 84 constraints; $O(n)$ complexity for box-constraint polytope evaluation)."
