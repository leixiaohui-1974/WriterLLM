# Review Report — Paper BAK-1 (Environ. Model. Softw. v01)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The paper presents HydroComponents, an open-source Modelica library for water conveyance systems aligned with the CHS framework. The concept is sound and addresses a genuine toolchain gap—hydraulic simulators lack control integration, control tools lack hydraulic libraries. However, the manuscript reads more like a software design document than a peer-reviewed paper for *Environmental Modelling & Software*. Several critical aspects expected by EMS reviewers are missing: software testing and quality assurance, reproducibility artifacts, systematic performance benchmarks, and independent actuator/sensor validation. The field-scale validation (§5.3) is particularly thin, presenting only summary metrics without time-series evidence or comparison against established tools on the same system.

**Score: 6.0/10**
**Verdict: Major Revision**

---

## Major Issues

### M1. No Software Testing or Quality Assurance Evidence

EMS explicitly expects papers to describe software testing methodology. The manuscript mentions "tested for FMI 2.0 Co-Simulation export" (§4.3) but provides **zero information** about:
- Unit test coverage (how many of the 28 components have automated tests?)
- Integration tests (do assembled systems produce correct results under edge cases?)
- Continuous integration pipeline (GitHub Actions, automated regression?)
- Test data and expected outputs

For a paper claiming to present an *open-source library* for the water community, this is a critical omission. The reader cannot assess software reliability.

**Recommendation**: Add a §4.4 "Testing and Quality Assurance" describing unit test coverage (target ≥80%), integration test suite, CI pipeline, and how users can run the test suite.

### M2. Reproducibility Artifacts Insufficient

EMS requires a Software Availability section (provided) but the manuscript lacks:
- Installation instructions (beyond "OpenModelica ≥ v1.22")
- Dependency specification (Modelica Standard Library version? Other libraries?)
- Docker/conda environment for exact reproducibility
- Step-by-step instructions to reproduce each validation case (Tables 3–5)
- Test datasets and expected outputs

The GitHub link is given but no mention of: README, documentation, tutorials, API reference, or contributing guidelines. An open-source library without documented installation and usage is not truly "available."

**Recommendation**: Add a §4.5 "Installation and Reproducibility" section. Provide a Dockerfile or environment specification. Include a `tests/` directory with scripts that reproduce Tables 3–5.

### M3. No Independent Actuator Validation

The validation (§5) only validates the *assembled system* response. The individual actuator models—which use the unified characteristic Eq. (4)—are never independently validated. Key questions:
- What are the discharge coefficient ($C_d$) values used for the sluice gates? How were they determined?
- Have the pump affinity law implementations been validated against manufacturer curves?
- What is the accuracy of the linearized actuator characteristic (Eq. 4) compared to the full nonlinear gate equation at different operating points?

The paper claims 5 actuator types but only the sluice gate is used in validation cases. The RadialGate, Pump, Valve, and Turbine components have **no validation evidence**.

**Recommendation**: Add a §5.4 "Component-Level Validation" that validates at least the SluiceGate and RadialGate models against published laboratory data (e.g., Henry's diagram, Buyalski radial gate data). Acknowledge that Pump/Valve/Turbine validation is future work.

### M4. Field-Scale Validation Lacks Depth

Table 5 presents only summary statistics (RMSE, wave travel time error, steady-state error) for the field-scale canal. This is insufficient for a journal paper:
- No time-series plots showing model vs. measurement during specific events
- No information about which events were simulated (gate operations? demand changes?)
- No uncertainty quantification (measurement uncertainty, parameter sensitivity)
- No comparison with HEC-RAS on the same canal (Table 6 claims LSV capability comparable to HEC-RAS but never demonstrates it)
- "Field measurement" as reference—how many events? What time period? What instruments?

The 45 mm RMSE claim for IDZ fidelity is stated as "adequate for MPC design where 50 mm accuracy is typically sufficient"—what is the source for this 50 mm threshold?

**Recommendation**: Expand §5.3 with: (a) at least one detailed time-series comparison figure, (b) a HEC-RAS benchmark on the same canal, (c) measurement instrumentation and uncertainty, (d) citation for the 50 mm MPC accuracy threshold.

### M5. Performance Benchmarks Not Systematic

The paper reports scattered performance numbers (FMU export time, simulation speed) but lacks a systematic performance assessment:
- Memory consumption vs. number of components
- Compilation time scaling (critical for large systems with many pools)
- FMU initialization time (important for real-time MPC)
- Comparison of LSV vs. IDZ computational cost for the same system across the three validation cases
- No hardware specification for reported timing results

The claim "model assembly time: 2 hours vs. 2 days" (Table 4) is subjective and depends heavily on user experience. How was this measured?

**Recommendation**: Add a §5.5 "Computational Performance" with systematic benchmarks (Table format), specify hardware, and replace subjective "assembly time" with measurable metrics (e.g., number of parameter specifications required, lines of code).

---

## Minor Issues

### m1. Component Count Ambiguity

Table 1 lists Plant as "5 × 5 fidelity levels" (=25 variants) but the total is "28 (including 5 fidelity variants for Plant)." This arithmetic is confusing. Are there 28 unique component *types* (5 plant + 5 actuator + 3 sensor + 4 disturbance + 4 controller + 3 objective = 24 base types) or 28 including fidelity variants? Clarify.

### m2. Numerical Robustness Not Discussed

The Preissmann scheme (§3.2) can suffer from numerical instability and oscillations. What Courant number range is recommended? How does the solver handle dry-bed conditions (common in irrigation canals during shutdown)? What happens when water levels approach zero?

### m3. Connector Design Oversimplified

The paper states HydroPort is "analogous to Modelica.Fluid connectors but simplified for open channels." What was removed? Modelica.Fluid connectors handle stream variables, medium properties, and reversible flow—features that may be important for certain water system configurations (e.g., tidal canals, bidirectional pipe networks).

### m4. No Scalability Demonstration

All three validation cases are small systems (2 tanks, 3 pools). Can HydroComponents handle a 50-pool canal system? A network with 100+ components? The practical value for field-scale water transfer networks requires evidence of scalability.

### m5. "Model assembly time" Claim Unsupported

"2 hours vs. 2 days" (Table 4) is a strong claim without supporting evidence. Who assembled the models? What was their experience level? Was this a formal user study? If not, remove or qualify significantly.

### m6. Missing Comparison with SIC/CanalCAD

Table 6 compares with HEC-RAS, SWMM, and Modelica.Fluid but omits SIC (Société du Canal de Provence) and CanalCAD—the two most widely used canal-specific simulation tools that *do* include some control integration. This omission weakens the positioning.

### m7. Self-Citation Rate

12 references total, with Lei (2025a,b,c,d) and Lei-supervised papers (Chen 2026, Su 2026, Liu 2026) = 7 Lei-group references. That is 58% group-citation rate, well above the 25% ceiling. Add external references.

---

## Reference Verification

- Blochwitz et al. (2012): Verified — Modelica Conference proceedings.
- Brunner (2016): Verified — HEC-RAS manual.
- Chen et al. (2026): CKG-1 paper, in-system reference.
- DHI (2024): Verified — MIKE manual.
- Fritzson (2014): Verified — Wiley-IEEE Press.
- Lei (2025a): P1a, in-system reference.
- Lei & Wang (2025): Verified — S2N journal paper.
- Lei et al. (2025b): P2A, in-system reference.
- Lei et al. (2025c): P1c, in-system reference.
- Liu et al. (2026): P-DC, in-system reference.
- Rossman (2015): Verified — EPA SWMM manual.
- Schweiger et al. (2019): Verified — Simulation Modelling Practice and Theory.
- Su et al. (2026): SC-1, in-system reference.

**Warning**: Only 5 of 13 references are independent external works. Self/group-citation rate ≈ 62%. This must be reduced to 15–25%.

## Summary

The library concept is valuable and addresses a real need. However, the manuscript needs substantial strengthening in software engineering rigor (testing, reproducibility, documentation), validation depth (independent component tests, field-scale evidence, tool comparison), and external referencing to meet EMS standards. Major revision required.
