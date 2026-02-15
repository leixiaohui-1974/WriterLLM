# Revision Response — SC-2 v02 → v03

**Responding to**: Reviewer C, Iteration 2

**M1.** Added §7.6 "Open-Source Alternative: Python/CasADi Pathway." CasADi (Andersson et al., 2019) can replace Simulink for DMPC design and C code generation. Feasibility: CasADi QP solver (qpOASES) achieves comparable solve times; C code generation is native. Barrier: no equivalent of HydroRTP's PLC-specific ST converter. Estimated development: 6 person-months. Timeline: planned for 2027.

**M2.** Added §7.7 "Digital Twin Pipeline." The HydroComponents FMU serves as the digital twin plant model; the DMPC controller runs in parallel as the control twin. Combined with RLS online re-identification (CKG-3), this constitutes a self-calibrating digital twin for canal systems. Connected to Rasheed et al. (2020) and Grieves & Vickers (2017).

**M3.** Added §7.8 "Community Adoption Roadmap": target users (irrigation district engineers, water utility automation teams, university courses), 4 tutorial videos planned, annual CHS Toolchain Workshop at EWRI conferences.

**m2.** FAIR compliance statement added to Data Availability section.
**m3.** Added §7.5 limitation: Family β requires HydroComponents `PipeSegment` component with MPC using the $H(s)$ transfer function — not yet tested in integrated pipeline.
