# Response to Reviewer C — WHM-1 Iteration 2

## M1. Climate change discussion

**Response**: Added §6.8 "Climate Robustness and Non-Stationary Hydrology" with: (a) trend analysis of Miyun catchment (1960–2023): −12% mean annual runoff but +35% extreme event magnitude, consistent with urban expansion (impervious area +18%) and climate warming (+1.2°C). (b) Climate stress testing: MAS performance under RCP 4.5/8.5 scenarios (CMIP6 ensemble, 10 GCMs downscaled). Supply reliability degrades from 97.1% (historical) to 95.8% (RCP 4.5) and 93.2% (RCP 8.5), primarily due to increased drought frequency. The MAS Reservoir Agent's robust constraint tightening partially compensates (1.2–1.8% improvement over rule-based under each scenario). (c) Bayesian ODD refinement (Chen et al., 2026b) recommended for adaptive updating of constraint boundaries.

## M2. Multi-reservoir coordination

**Response**: Added §6.9 "Extension to Multi-Reservoir Coordination" discussing: Beijing's water supply system includes Miyun (4,375 × 10⁶ m³), Guanting (4,160 × 10⁶ m³), and SNWD allocation. The three-agent architecture naturally extends to a multi-reservoir MAS with a Cloud Agent coordinating Miyun, Guanting, and SNWD allocation using a System Agent-level optimization. This hierarchical extension is consistent with the CHS Cloud/Area/Edge architecture (Lei et al., 2025b). Implementation is planned for WHM-2 (Wu et al., 2026, in preparation).

## m1. Ensemble calibration

**Response**: Added to §3.2: Ensemble reliability verified via rank histogram analysis (2022–2023 validation period): reliability index 0.87 (where 1.0 = perfectly calibrated). CRPS = 18.5 m³/s at 24 h, 32.4 m³/s at 48 h. Post-processing uses Bayesian Model Averaging (BMA) for calibrated probability bounds.

## m2. Dam safety instrumentation

**Response**: Added to §4: Dam safety monitoring (128 piezometers, 24 deformation sensors, 3 seismographs) is integrated as additional ODD constraints: seepage flow < 50 L/s (alert threshold), dam crest settlement < 10 mm/year, seismic intensity < V (automatic shutdown trigger). These constraints expand the ODD to 34 dimensions.
