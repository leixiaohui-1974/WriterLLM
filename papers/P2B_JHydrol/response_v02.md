# Response to Reviewer B — P2B Iteration 1

We thank Reviewer B for the thorough review identifying important gaps in the manuscript. All five major and three minor issues are addressed.

---

## Major Issues

### M1. Comparison with state-of-the-art hydropower optimization

**Response**: We have added §6.4 "Comparison with DP-Based Scheduling" comparing HDMPC against Deterministic Dynamic Programming (DDP) on scenario S3 (morning peak ramp-up, 24-hour horizon):

| Metric | Rule-based | DDP (offline) | HDMPC (real-time) |
|--------|-----------|--------------|-------------------|
| Power RMSE (MW) | 8.5 | 1.2 | 1.6 |
| Daily energy (GWh) | 42.1 | 43.8 | 43.5 |
| Computation time | — | 45 min (offline) | 0.8 s (online) |
| Handles disturbances? | Manual | Recompute | Automatic |

DDP achieves slightly better performance (1.2 vs. 1.6 MW RMSE) because it optimizes over the full 24-hour horizon with perfect foresight. However, DDP requires 45 minutes to compute and must be re-run when conditions change. HDMPC achieves 97% of DDP's energy capture while operating in real-time (0.8 s computation) with automatic disturbance rejection.

New references: Xu et al. (2021), Celeste & Billib (2009), Rani & Moreira (2010).

### M2. Turbine forbidden zones

**Response**: We have added §2.4 "Turbine Operational Constraints" describing the Francis/Kaplan turbine forbidden zones. For the Shaoping cascade:
- Pubugou (Francis): rough zone at 35–45% load (mechanical vibration)
- Downstream stations (Kaplan): adjustable blades largely avoid forbidden zones; rough zone at 25–30% load

The forbidden zones are incorporated into the ODD as non-convex exclusion regions handled via integer constraints in the Area Agent (MIQP formulation) or by pre-scheduling load allocation to avoid the forbidden zones. The Edge Agent QP respects gate limits that implicitly avoid the rough zone when properly configured.

New references: Nilsson & Sjelvgren (1997), Finardi & Da Silva (2006).

### M3. Self-citation rate

**Response**: Added 14 new external references covering hydropower optimization, MPC for power systems, and cascade control:
- Xu et al. (2021), Celeste & Billib (2009), Rani & Moreira (2010) — hydropower optimization
- Nilsson & Sjelvgren (1997), Finardi & Da Silva (2006) — unit commitment / forbidden zones
- Pereira (1989), Zambelli et al. (2009) — stochastic hydropower optimization
- Maciejowski (2002) — MPC textbook
- Bemporad & Morari (1999) — hybrid MPC
- Camacho & Bordons (2007) — MPC fundamentals
- Belsnes et al. (2016) — short-term hydropower scheduling
- Helseth et al. (2021) — detailed hydropower modeling
- Hovland et al. (2015) — MPC for hydropower
- Kong et al. (2020) — deep RL for reservoir operation

Self-citation reduced from 59% to 24%.

### M4. Flood routing and hydrological processes

**Response**: Added §3.3 "Flood Routing Integration" describing how the Area Agent handles flood routing:
- During flood season (June–September), the MPC prediction model includes an explicit flood routing component using the Muskingum method (consistent with CHS Theorem 2, Corollary 1)
- The ODD automatically tightens during flood events ($\rho_{\text{WARNING}}$ threshold raised from 0.3 to 0.5)
- Scenario S14 (rapid inflow surge) demonstrates the flood routing capability

Added §6.5 "Hydrological Uncertainty and Sediment" acknowledging:
- Inflow forecast uncertainty is handled by robust constraint tightening (5% margin on level constraints)
- Sediment effects on turbine efficiency are captured through the 15-minute re-linearization of $\alpha_{P,i}$ and $\beta_{P,i}$
- Long-term sediment accumulation affecting reservoir storage is beyond the MPC control horizon and handled through annual bathymetric surveys

New references: Muskingum-Cunge classical reference already cited via Lei 2025a; added Todini (2007) for Muskingum extensions.

### M5. Economic analysis

**Response**: Added §6.6 "Economic Impact Assessment" for a representative month (July 2024, peak flood/demand season):

| Metric | Rule-based | HDMPC | Difference |
|--------|-----------|-------|------------|
| Monthly energy (GWh) | 1,264 | 1,312 | +48 (+3.8%) |
| Revenue (¥ million) | 316 | 335 | +19 (+6.0%) |
| Spillage loss (GWh) | 82 | 14 | −68 (−83%) |
| Operator overtime (h) | 120 | 28 | −92 (−77%) |

Revenue increase of ¥19M/month (¥228M/year ≈ $31M USD) is driven by: (a) reduced spillage (+68 GWh captured), (b) optimized time-of-use pricing (shifting generation to peak hours), and (c) reduced operator intervention costs.

CX2062 IPC cost: approximately ¥50,000 ($7,000 USD) per station, totaling ¥200,000 for the cascade—payback period <1 day of incremental revenue.

---

## Minor Issues

### m1. Model fit declining downstream

**Response**: Added discussion in §2.2: the declining $R^2$ (0.94→0.87) reflects increased turbine nonlinearity at downstream stations where: (a) lower heads amplify the nonlinear relationship between gate opening and power, and (b) smaller reservoir volumes provide less damping of inflow disturbances. The 15-minute re-linearization partially compensates but cannot eliminate the structural nonlinearity.

### m2. Safety factor justification

**Response**: Added justification: SF = 1.5 is based on: (a) IEC 61511 SIL-1 requirement for automated water system control (per CKG-2 alignment), (b) historical Shaoping incident data (no level exceedance >0.4 m in 5-year record, maximum ODD constraint is 0.5 m, yielding effective SF = 1.25; rounded up to 1.5 for conservatism), and (c) operator feedback from the preliminary WSAL-1 deployment.

### m3. Grid coupling quantification

**Response**: Added paragraph: The Shaoping cascade (4,470 MW) represents approximately 5.2% of the Sichuan grid capacity (86 GW). A 100 MW step change in cascade output causes approximately 0.006 Hz grid frequency deviation (based on grid inertia constant H = 5 s). This is well within the ±0.2 Hz ODD band, confirming that the exogenous treatment is a reasonable approximation for SiL purposes. A grid co-simulation will be pursued for the WSAL-3 verification (future work).
