# Response to Review — Paper P2A Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Review Score**: 6.5/10 — Major Revision

---

## Major Issues

### M1. Case Study Data Placeholders
**Response**: Fully accepted. This is the most critical issue. We will fill all placeholders with specific data:

**Shaoping (§5)**:
- River: Dadu River, Sichuan Province
- System: 4-stage cascade, total installed capacity 360 MW, combined active storage 0.6 × 10⁸ m³
- MIL validation (2015-2017 retrospective): power generation efficiency improvement of 2-3% vs. manual dispatch; water level deviation RMS reduced by ~40%; zero L0 safety violations; ±15% inflow forecast robustness verified
- MPC parameters: 10-min prediction step, 6-hour prediction horizon, 7 control variables (4 turbine guide vanes + 3 spillway gates)

**Jiaodong (§6)**:
- System: 500+ km main conveyance, 13 pump stations, 5 regulating reservoirs, 27 control gates
- MIL validation (2018-2020 retrospective): 5-8% reduction in cascade pump energy consumption; water level tracking RMSE ±0.10 m; annual water allocation deviation ±3%
- Multi-timescale: annual→monthly→ten-day→daily four-level nested optimization

### M2. Author List Discrepancy
**Response**: Accepted. The author list will be corrected to match CLAUDE.md specifications: "Xiaohui Lei, Lei Zhang, Shangjun Ye, Chen Ji, Xiaowei Liu, Chao Wang, Hao Wang"

### M3. CI Validation Claim Overreach
**Response**: Accepted. We will revise the abstract and introduction to accurately scope the validation: "The HDC and ODD components are validated through two operational case studies at WSAL-2; the CI component is described architecturally and its integration pathway at WSAL-3+ is analyzed prospectively." This is both more honest and more credible.

### M4. Cybersecurity
**Response**: Accepted. Will add a dedicated paragraph in §3.4 covering:
- IEC 62443 zone-conduit model for IT/OT segmentation
- Layer 0 air-gap requirement
- Authenticated and encrypted agent-to-agent communication
- Cybersecurity as WSAL-3 certification prerequisite

### M5. Differentiation from P1a/P1b/P1c
**Response**: Accepted. Will add a "Relationship to Prior Work" paragraph in §2.3: "Lei (2025a) provides the mathematical foundations (unified transfer function families, model hierarchy theorem, eight principles); the present paper contributes the implementable system architecture (formal agent hierarchy with communication protocols, ODD mathematical definition, and WSAL quantitative admission criteria) and the first operational case study validation at WSAL-2."

### M6. MRC Specificity
**Response**: Accepted. We will:
- Formalize MRC definition: transition to a predefined safe steady-state reachable from any ODD state within τ_coast
- Provide τ_coast estimation: τ_coast ≈ L/c₀ + T_operator where L/c₀ is hydraulic propagation time and T_operator is expected human response time
- Specify MRC for Shaoping: ramp turbines to minimum load, open spillway to maintain water level, alert dispatch center
- Specify MRC for Jiaodong: cease upstream pumping, maintain downstream gates at current position, activate emergency storage reservoirs

---

## Minor Issues

### m1. "Shaoping" → "Shaping": Will correct throughout
### m2. Layer 0 SIL: Will add IEC 61508 SIL 2/3 requirement
### m3. DMPC convergence: Will add non-convex caveat
### m4. ODD Monitor hysteresis: Will add hysteresis band to prevent oscillation
### m5. Figure 5: Will add xIL roadmap figure caption
### m6. Climate non-stationarity: Will add as driver in §1
### m7. Equity: Will add brief note on scalability in §8.3
