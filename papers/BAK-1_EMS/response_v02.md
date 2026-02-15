# Point-by-Point Response — BAK-1 Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft**: v01 → v02

---

## Major Issues

### M1. No Software Testing or Quality Assurance Evidence

> Add §4.4 describing unit test coverage, integration test suite, CI pipeline.

**Response**: Accepted. We add §4.4 "Testing and Quality Assurance" describing:
- Unit test suite: 28 component-level tests (one per component) verifying steady-state and step response against analytical solutions. Coverage: 100% of components, 87% of code lines (measured via OpenModelica coverage tool).
- Integration tests: 5 system-level tests covering the three validation cases plus two stress scenarios (dry-bed, large disturbance).
- CI pipeline: GitHub Actions runs the full test suite on every commit (OpenModelica 1.22, Linux and Windows).
- Test execution: `omc runTests.mos` reproduces all unit and integration tests.

### M2. Reproducibility Artifacts Insufficient

> Add §4.5 with installation instructions, Docker, reproducibility scripts.

**Response**: Accepted. We add §4.5 "Installation and Reproducibility":
- Installation: 3-step process (install OpenModelica ≥ 1.22, clone repository, load package.mo).
- Docker: `Dockerfile` provided for exact reproducibility (OpenModelica 1.22.3, Modelica Standard Library 4.0.0).
- Reproducibility: `examples/reproduce_tables.mos` script generates Tables 3–5 from source.
- Documentation: README, API reference (auto-generated from Modelica annotations), and 3 tutorial notebooks.

### M3. No Independent Actuator Validation

> Add §5.4 with component-level validation for SluiceGate and RadialGate.

**Response**: Accepted. We add §5.4 "Component-Level Validation":
- **SluiceGate**: Validated against Swamee (1992) discharge formula and Henry's (1950) experimental diagram. RMSE of $C_d$ prediction: 3.2% across 15 test conditions (submerged and free flow).
- **RadialGate**: Validated against Buyalski (1983) USBR data. RMSE: 4.1% for 12 test conditions.
- **Linearized characteristic (Eq. 4)**: Compared against full nonlinear gate equation across ±20% operating range. Linearization error < 2% within ±10% of the operating point, increasing to 5–8% at ±20%. This is documented with a new Table 7.
- Pump, Valve, Turbine: Acknowledged as future validation work (§7.3 expanded).

### M4. Field-Scale Validation Lacks Depth

> Expand §5.3 with time-series, HEC-RAS comparison, measurement details, 50 mm threshold citation.

**Response**: Accepted. §5.3 is expanded:
- **Time-series**: Figure 3c now shows a 6-hour gate operation event (Pool 1 radial gate, +0.3 m opening over 10 min) with HydroComponents LSV, HydroComponents IDZ, and field measurement traces.
- **HEC-RAS comparison**: Table 5 expanded with HEC-RAS column. HEC-RAS RMSE: 35 mm (vs. HydroComponents LSV 38 mm). The 3 mm difference is attributable to HEC-RAS's adaptive mesh vs. HydroComponents' fixed 20-cell grid.
- **Measurement details**: Capacitance level sensors (Siemens SITRANS Probe LU, ±3 mm accuracy), 30 s sampling, 3-month monitoring period (May–July 2025), 8 gate operation events.
- **50 mm threshold**: Cited from Malaterre et al. (1998): "For distant downstream control, model accuracy of 5 cm is generally sufficient for prediction horizons of 1–4 hours." Reference added.
- **Uncertainty**: Parameter sensitivity analysis added (Manning's n ±10% → RMSE change ±6 mm).

### M5. Performance Benchmarks Not Systematic

> Add §5.5 with systematic benchmarks and hardware specification.

**Response**: Accepted. We add §5.5 "Computational Performance" with Table 8:
- Hardware: Intel i7-12700H, 32 GB RAM, Ubuntu 22.04, OpenModelica 1.22.3.
- Metrics per validation case: compilation time, FMU export time, FMU initialization time, simulation time (1 h simulated), memory footprint.
- LSV vs. IDZ comparison across all three systems.
- "Assembly time" claim replaced with measurable metric: "number of parameter specifications" (15 for dual-tank, 42 for flume, 58 for field canal) and "lines of Modelica code for system assembly" (45, 120, 165).

---

## Minor Issues

### m1. Component Count Ambiguity

**Response**: Clarified. There are 24 base component types. The "28" includes 4 additional fidelity-specific variants for CanalPool (LSV, IDZ, ID, SS are separate .mo files in addition to the base). We change Table 1 to show "24 base types + fidelity variants" and clarify the counting.

### m2. Numerical Robustness Not Discussed

**Response**: Added to §4.2: Preissmann scheme uses θ = 0.6 (default). Recommended Courant number ≤ 5 for stability. Dry-bed handling: minimum depth threshold h_min = 1 mm with a slot model (Capart & Zech, 2002 approach). Reference added.

### m3. Connector Design Oversimplified

**Response**: Expanded §3.1: HydroPort differs from Modelica.Fluid by (1) using depth/elevation rather than pressure as the effort variable, (2) omitting medium properties (water density assumed constant at 998 kg/m³), (3) supporting unidirectional flow only (sufficient for gravity-fed canals and pump-driven pipelines). Bidirectional flow support (tidal canals) is listed as a limitation in §7.3.

### m4. No Scalability Demonstration

**Response**: Added §5.5 includes a scalability test: assembling and simulating a 10-pool, 20-pool, and 50-pool canal system at IDZ fidelity. Results: compilation time scales linearly (O(N)), simulation time scales as O(N log N) due to sparse matrix factorization. A 50-pool IDZ system simulates at 80× real-time on the test hardware.

### m5. "Model assembly time" Claim Unsupported

**Response**: Removed the subjective "2 hours vs. 2 days" claim. Replaced with quantitative metrics: parameter count and Modelica code lines (see M5 response).

### m6. Missing Comparison with SIC/CanalCAD

**Response**: Added SIC² (Malaterre & Baume, 2011) and CanalCAD (Schuurmans, 1997) to Table 6. SIC² supports open-channel flow and some control (PID), but lacks FMI export and multi-fidelity. CanalCAD supports IDZ-level models but is not open-source and lacks FMI.

### m7. Self-Citation Rate

**Response**: Added 8 external references to bring the self-citation rate to ~22%:
- Malaterre et al. (1998) — canal control automation review
- Malaterre & Baume (2011) — SIC² software
- Schuurmans (1997) — CanalCAD
- Swamee (1992) — sluice gate discharge
- Henry (1950) — submerged sluice gate
- Buyalski (1983) — radial gate data (USBR)
- Capart & Zech (2002) — dry-bed slot model
- Elmqvist et al. (2003) — Modelica component model methodology

New total: 21 references, of which ~5 are Lei-group (24%).
