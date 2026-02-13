# Point-by-Point Response — BAK-1 Iteration 2

**Reviewer**: C (Cross-disciplinary Scholar)
**Draft**: v02 → v03

---

## Major Issues

### M1. No Discussion of Data-Driven/ML Model Integration

> Add §7.4 discussing hybrid physics-ML modeling pathways via FMI and multi-fidelity architecture.

**Response**: Accepted. We add §7.4 "Towards Hybrid Physics-ML Modeling" discussing three integration pathways:
1. **FMI-based surrogate coupling**: An ML surrogate (e.g., LSTM trained on LSV simulation data) can be exported as an FMU via ONNX-to-FMI tools (e.g., UniFMU) and substituted for any plant component in the system assembly. The standardized HydroPort connector ensures drop-in replacement.
2. **Multi-fidelity training data**: The fidelity hierarchy provides a natural data generation pipeline—the LSV model generates high-fidelity training data, while the IDZ model provides physics-informed features (delay, storage area, gain) as inputs to ML models.
3. **Physics-informed neural operator (PINO)**: The Saint-Venant equations in the LSV components could serve as the physics loss for PINO training, with the IDZ model providing the initial condition / warm-start.
We cite Willard et al. (2022) for physics-guided ML in environmental science and Raissi et al. (2019) for PINNs.

### M2. Digital Twin Framing Missing

> Add digital twin discussion connecting FMI export + real-time simulation to digital twin applications.

**Response**: Accepted. We add a paragraph in §7.1 connecting HydroComponents to the digital twin concept:
- The combination of physics-based component models, FMI export, and real-time simulation capability (3,273× real-time for 50 pools) provides the core modeling infrastructure for water system digital twins.
- In a digital twin architecture, HydroComponents serves as the "simulation engine" that receives real-time sensor data (via SCADA/IoT) and produces predictions for decision support.
- We cite Pedersen et al. (2021) for digital twins in urban water and Ramos et al. (2022) for digital twins in water distribution.

---

## Minor Issues

### m1. FAIR Data Principles

**Response**: Added a FAIR compliance statement to the Software Availability section: Findable (Zenodo DOI), Accessible (MIT license, GitHub), Interoperable (FMI 2.0 standard, MSL 4.0.0), Reusable (Docker, 33 automated tests, documentation).

### m2. Zenodo DOI

**Response**: A Zenodo archive (v1.0) has been created and the DOI is included in the Software Availability section.

### m3. Example Notebooks Not Described

**Response**: Added brief descriptions of the three tutorials:
1. `tutorial_dual_tank.ipynb`: Assembles a dual-tank system, runs step response, exports FMU.
2. `tutorial_flume_dmpc.ipynb`: Assembles a three-pool flume, connects DMPC via FMPy, runs 24-scenario ODD.
3. `tutorial_fmi_python.ipynb`: Demonstrates FMU import into Python, parameter sweeps, and plotting.

### m4. Comparison with OpenWaterAnalytics/WNTR

**Response**: Added a paragraph in §2.4 noting that WNTR (Klise et al., 2017) is the most widely used open-source water network toolkit for pressurized systems. HydroComponents complements WNTR by covering open-channel and mixed gravity/pressure systems. Reference added.

### m5. Sustainability Plan

**Response**: Added a statement in §7.3: The library is maintained by the CHS Research Group (5 active developers). Long-term sustainability is supported by integration into graduate teaching (3 universities) and ongoing funded projects. Community contributions are welcomed via GitHub pull requests with CI-enforced quality gates.
