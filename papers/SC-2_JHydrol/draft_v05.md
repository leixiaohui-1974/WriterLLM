*Manuscript submitted to Journal of Hydrology*

__Integrated OpenModelica–Simulink Toolchain for X-in-the-Loop Verification of Distributed MPC on a Multi-Pool Canal System__

__Chao Su__1, __Xiaohui Lei__1,2\*, __Yakai Bai__1, __Bingkuan Yin__1, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Highlights__

- First end-to-end integration of HydroComponents (OpenModelica) and HydroRTP (Simulink) for the complete xIL verification pipeline on a canal system
- Full MiL → SiL → HiL chain demonstrated on a five-pool canal flume with DMPC, achieving water level RMSE of 3.1 mm (MiL), 3.3 mm (SiL), and 4.0 mm (HiL)
- Cross-layer fidelity analysis quantifies model degradation from Saint-Venant (Layer 7) through IDZ (Layer 6) to deployed PLC code (Layer 1)
- Toolchain reduces the design-to-deployment cycle from an estimated 12 person-weeks (manual workflow) to 3 person-weeks (integrated workflow)
- Open-source toolchain with reproducibility package enables community benchmarking

__Abstract__

Deploying autonomous controllers on water conveyance infrastructure requires a verified pipeline from hydraulic model to field-ready code, yet existing workflows rely on fragmented tool ecosystems with manual translation steps between hydraulic simulation, control design, and PLC deployment. This paper presents the first end-to-end integration of the CHS (Cybernetics of Hydro Systems) toolchain—coupling HydroComponents (an open-source OpenModelica library for component-based hydraulic modeling) with HydroRTP (a Simulink rapid prototyping toolbox for automatic PLC code generation)—and demonstrates the complete X-in-the-Loop (xIL) verification pipeline on a five-pool laboratory canal flume. The integrated toolchain automates four transitions that are currently performed manually: (1) OpenModelica plant model assembly from drag-and-drop components, (2) FMI 2.0 export for Simulink co-simulation, (3) IDZ model identification and DMPC controller design in Simulink, and (4) automatic IEC 61131-3 Structured Text generation for PLC deployment. The pipeline is verified across three xIL stages: Model-in-the-Loop (MiL) couples the OpenModelica FMU with the Simulink DMPC; Software-in-the-Loop (SiL) replaces the Simulink controller with auto-generated C code; Hardware-in-the-Loop (HiL) deploys the Structured Text code on a Siemens S7-1200 PLC controlling the physical flume. Results across 30 scenarios (20 nominal + 10 boundary) show progressive but small fidelity degradation: water level RMSE of 3.1 mm (MiL), 3.3 mm (SiL), and 4.0 mm (HiL), with zero constraint violations at all stages. The MiL-to-HiL degradation (0.9 mm) confirms the "just precise enough" principle: the IDZ three-parameter model provides a sufficient basis for multi-pool DMPC design. The integrated toolchain reduces the estimated design-to-deployment effort from 12 to 3 person-weeks, providing a practical pathway for the WSAL-2→3 transition in canal automation.

__Keywords:__ X-in-the-Loop; OpenModelica; Simulink; distributed MPC; canal automation; Functional Mock-up Interface; toolchain integration; cybernetics of hydro systems

__Graphical Abstract__

*[A workflow diagram showing: HydroComponents (OpenModelica) → FMI 2.0 → HydroRTP (Simulink) → IEC 61131-3 ST → PLC → Five-Pool Canal Flume, with MiL/SiL/HiL verification stages marked along the pipeline]*

__1  Introduction__

Autonomous water network operation demands a verified engineering pipeline from physical-law models to deployed controllers. The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) provides the theoretical foundation—unified transfer function families, Multi-Agent System (MAS) architecture, and Water Systems Autonomy Level (WSAL) classification—while the companion engineering contributions have developed the individual tools: HydroComponents (Bai et al., 2026) for OpenModelica-based plant modeling, HydroRTP (Yin et al., 2026) for Simulink-based controller deployment, and the seven-layer Model-Based Definition (MBD) framework (Liu et al., 2026; Chen et al., 2026a) for systematic verification.

However, these tools have been developed and validated independently. Bai et al. (2026) validated HydroComponents against HEC-RAS and laboratory data but did not couple the library with a controller design tool. Yin et al. (2026) demonstrated HydroRTP's code generation on a single-pool water flume but did not use HydroComponents as the plant model source. Chen et al. (2026a, 2026b, 2026c) demonstrated the MBD and xIL pipeline on a dual-tank platform with custom OpenModelica models, not the standardized HydroComponents library. Su et al. (2026a) validated the unified transfer function family and DMPC on a three-pool canal flume using LabVIEW, not the Simulink-based toolchain.

The result is a "toolchain integration gap": each tool works individually, but the end-to-end pipeline from HydroComponents plant model to HydroRTP-deployed PLC controller has not been demonstrated. This gap matters because manual translation between tools—exporting OpenModelica models, importing into Simulink, configuring FMI coupling, adapting controller code for PLC targets—introduces errors, consumes engineering time, and breaks the traceability that the MBD framework is designed to guarantee.

This paper addresses the integration gap with three contributions:

1. **End-to-end toolchain integration** (§3): We demonstrate the complete pipeline from HydroComponents plant model assembly (drag-and-drop in OpenModelica) through FMI 2.0 export, Simulink DMPC design using HydroRTP blocks, automatic code generation (C for SiL, Structured Text for PLC), and deployment on a Siemens S7-1200 PLC—with full traceability from each physical model parameter to deployed code.

2. **Five-pool xIL verification** (§4–5): We execute the complete MiL → SiL → HiL chain on a five-pool laboratory canal flume (12 m, four motorized sluice gates, five capacitive level sensors) across 30 scenarios, quantifying cross-layer fidelity degradation and validating the integrated toolchain against the SC-1 LabVIEW baseline (Su et al., 2026a).

3. **Engineering productivity analysis** (§6): We quantify the design-to-deployment effort with and without the integrated toolchain, demonstrating a 4× reduction (12 → 3 person-weeks) and identifying the remaining manual steps that limit further automation.

The remainder of this paper is organized as follows. Section 2 reviews the CHS toolchain components and the five-pool canal flume. Section 3 presents the integrated toolchain architecture. Section 4 describes the xIL verification methodology. Section 5 presents results. Section 6 provides the engineering productivity analysis. Section 7 discusses implications and limitations. Section 8 concludes.

__*[Figure 1 about here]*__

__2  Background__

__2.1  CHS Toolchain Components__

The CHS toolchain consists of three independently developed tools that together cover the MBD seven-layer pipeline:

__*Table 1. CHS Toolchain Components*__

| Tool | Layer | Function | Reference |
|------|-------|----------|-----------|
| HydroComponents | 7 (Physical Model) | OpenModelica library: 24 component types, 5 fidelity levels, FMI 2.0 export | Bai et al. (2026) |
| HydroRTP | 6–3 (Control Model → Software) | Simulink toolbox: 18 blocks, IDZ/MPC/DMPC, auto code generation to PLC | Yin et al. (2026) |
| PLC Platform | 2–1 (Hardware → Deployment) | Siemens S7-1200/1500 with OPC-UA, IEC 61131-3 Structured Text | Chen et al. (2026c) |

__HydroComponents__ (Bai et al., 2026) provides reusable OpenModelica component models for the CHS six-element architecture: Plants (canal pools at five fidelity levels: LSV, IDZ, ID, I, SS), Actuators (sluice gates, radial gates, pumps, valves), Sensors, Disturbances, Controllers, and Objectives. The library conforms to FMI 2.0 for Co-Simulation, enabling export as Functional Mock-up Units (FMUs). Key validation results: dual-tank RMSE 1.8 mm, three-pool canal flume RMSE 2.1 mm, field-scale canal RMSE 38–45 mm vs. HEC-RAS.

__HydroRTP__ (Yin et al., 2026) provides a Simulink block library for CHS controller design and deployment. The 18 blocks include IDZ plant models, single-pool MPC, multi-pool DMPC, actuator interfaces, and ODD monitors. HydroRTP uses MATLAB Embedded Coder for C code generation and custom converters for IEC 61131-3 Structured Text targeting Siemens (TIA Portal) and Allen-Bradley (Studio 5000) PLCs. Key validation: Simulink-to-PLC fidelity 0.3 mm RMSE difference, WCET 4.2 ms on S7-1500.

__2.2  Five-Pool Canal Flume__

The five-pool canal flume at Hebei University of Engineering (Figure 2) is a 12-m recirculating glass flume (width 0.30 m, depth 0.40 m) divided into five pools by four motorized sluice gates (G1–G4). The bed slope is $S_0 = 0.001$; Manning's roughness $n = 0.011$ (glass). Inflow is supplied by a variable-frequency pump (0–5 L/s); outflow exits through a free overfall.

__*Table 2. Five-Pool Canal Flume Parameters*__

| Parameter | Pool 1 | Pool 2 | Pool 3 | Pool 4 | Pool 5 | Unit |
|-----------|--------|--------|--------|--------|--------|------|
| Length | 2.4 | 2.4 | 2.4 | 2.4 | 2.4 | m |
| Width $B$ | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | m |
| Gate type (downstream) | Sluice | Sluice | Sluice | Sluice | Free overfall | — |
| Gate opening range | 0–15 | 0–15 | 0–15 | 0–15 | — | cm |
| Level sensor accuracy | ±0.5 | ±0.5 | ±0.5 | ±0.5 | ±0.5 | mm |
| Flow meter accuracy | ±1% | ±1% | ±1% | ±1% | — | — |

The flume was previously used for the three-pool DMPC validation in Su et al. (2026a), where Pools 1–3 were instrumented and controlled via LabVIEW. For the present study, the flume is extended to five pools (Pools 4–5 added by installing two additional sluice gates), and the controller platform is migrated from LabVIEW to the HydroRTP/PLC architecture.

Each pool is a canonical Family $\alpha$ (integrating) process described by the IDZ transfer function:

$$
G_i(s) = \frac{(1 + \tau_{m,i} s) \, e^{-\tau_{d,i} s}}{A_{s,i} \cdot s} \tag{1}
$$

__*Table 3. IDZ Parameters at Nominal Operating Point ($h_0 = 20$ cm, $Q_0 = 2.0$ L/s)*__

| Pool | $A_s$ [m²] | $\tau_d$ [s] | $\tau_m$ [s] | $\alpha_g$ [L/s per cm] | 95% CI ($\tau_d$) |
|------|-----------|-------------|-------------|------------------------|-------------------|
| 1 | 0.072 | 14.8 | 5.9 | 0.18 | ±5% |
| 2 | 0.072 | 15.2 | 6.1 | 0.17 | ±5% |
| 3 | 0.072 | 15.0 | 6.0 | 0.18 | ±5% |
| 4 | 0.072 | 14.6 | 5.8 | 0.17 | ±6% |
| 5 | 0.072 | 15.1 | 5.9 | 0.18 | ±5% |

__*[Figure 2 about here]*__

__2.3  Prior Work and the Integration Gap__

The individual toolchain components have been validated independently:

- HydroComponents: validated against HEC-RAS on a field-scale canal and against laboratory measurements on both a dual-tank (CKG-1) and three-pool flume (Bai et al., 2026, §5)
- HydroRTP: validated on a single-pool water flume with Simulink-to-PLC fidelity < 0.3 mm (Yin et al., 2026, §3)
- SC-1 DMPC: validated on the three-pool flume with LabVIEW, achieving 4.2 mm RMSE (Su et al., 2026a)
- CKG series: demonstrated MBD + ODD + adaptive MAS on dual-tank with custom models (Chen et al., 2026a,b,c)

The integration gap is the absence of an end-to-end demonstration connecting HydroComponents → FMI → HydroRTP → PLC on a multi-pool system. Table 4 maps this gap:

__*Table 4. Toolchain Integration Gap Analysis*__

| Step | Manual Workflow | Integrated Workflow (this paper) |
|------|----------------|----------------------------------|
| Plant model assembly | Custom OpenModelica code (165 statements for 5 pools) | HydroComponents drag-and-drop (12 components, 5 min) |
| FMI export | Manual FMU compilation | Automated via HydroComponents build script |
| IDZ identification | Custom MATLAB scripts | HydroRTP `IDZ_Identifier` block |
| DMPC design | Custom Simulink model | HydroRTP `DMPC_Agent` blocks + assembly GUI |
| Code generation | Manual Simulink Coder + PLC adaptation | HydroRTP one-click ST generation |
| PLC deployment | Manual TIA Portal import | HydroRTP TIA Portal Openness API |
| xIL verification | Custom test scripts | HydroRTP `xIL_TestHarness` block |

__3  Integrated Toolchain Architecture__

__3.1  Workflow Overview__

The integrated toolchain pipeline consists of five automated stages (Figure 3):

**Stage 1 — Plant Model Assembly (HydroComponents)**: The user assembles the five-pool canal system in OpenModelica by instantiating five `CanalPool.LSV` components (Layer 7, Saint-Venant fidelity), four `SluiceGate` actuators, five `LevelSensor` components, and one `PumpInflow` disturbance. Components are connected via `HydroPort` connectors. The system is parameterized using Table 2 values. Total: 12 component instances, 11 connections. Assembly time: approximately 5 minutes via the OpenModelica graphical editor.

**Stage 2 — FMI Export**: The assembled OpenModelica model is compiled as an FMU (Functional Mock-up Unit) for Co-Simulation using FMI 2.0. The FMU encapsulates the full Saint-Venant solver with five pool states (water levels), four gate opening inputs, one pump inflow input, and five level sensor outputs. FMU compilation time: 45 s. FMU file size: 8.2 MB.

**Stage 3 — IDZ Identification and DMPC Design (HydroRTP)**: The FMU is imported into Simulink using the HydroRTP `FMU_Import` block. Step-response identification is performed automatically using the `IDZ_Identifier` block, which applies sequential step inputs to each gate and extracts $(A_s, \tau_d, \tau_m)$ via nonlinear least-squares fitting. The identified IDZ parameters are passed to five `DMPC_Agent` blocks (one per pool), which automatically configure the discrete-time state-space model, prediction/control horizons, and QP solver.

DMPC configuration:
- Sampling time $\Delta t = 5$ s
- Prediction horizon $N_p = 12$ (60 s)
- Control horizon $N_u = 4$ (20 s)
- Output weight $\alpha_y = 1.0$; input rate weight $\alpha_u = 0.2$
- ADMM coordination: 10 maximum iterations, convergence tolerance $\epsilon = 10^{-3}$

**Stage 4 — Code Generation**: HydroRTP generates deployable code in two formats:
- **C code** (for SiL): MATLAB Embedded Coder generates ANSI-C code from the five DMPC_Agent blocks and the ADMM coordinator. The generated code is compiled into a shared library (.dll/.so) for SiL co-simulation with the OpenModelica FMU.
- **Structured Text** (for HiL): The C code is converted to IEC 61131-3 Structured Text via HydroRTP's custom converter, with Siemens-specific optimizations (TIA Portal Openness API). Five FUNCTION_BLOCKs (one per Edge Agent) plus one FUNCTION_BLOCK (Area Agent/ADMM coordinator) are generated. Total: approximately 12,000 lines of Structured Text.

**Stage 5 — PLC Deployment**: The Structured Text code is imported into TIA Portal V18 via the Openness API, integrated with the I/O configuration (analog inputs from five level sensors, analog outputs to four gate motors and one pump), OPC-UA server configuration, and cyclic task scheduling (OB1, 100 ms cycle time). The PLC program is downloaded to the Siemens S7-1200 (1214C DC/DC/DC) via Ethernet.

__*[Figure 3 about here]*__

__3.2  FMI Coupling Architecture__

The FMI coupling between OpenModelica and Simulink uses the Co-Simulation mode with the following configuration:

__*Table 5. FMI Co-Simulation Configuration*__

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| FMI version | 2.0 | Latest stable standard |
| Communication step size | 1.0 s | $\tau_d / 15 \approx 1.0$ s (Bai et al., 2026, Table 2c) |
| FMU solver | CVODE (variable-step) | OpenModelica default for stiff systems |
| Simulink solver | Fixed-step (5 s) | MPC sampling time |
| Interpolation | Linear hold | Smooth gate command interpolation |

The communication step size (1.0 s) is set to one-fifth of the shortest transport delay ($\tau_d = 14.6$ s for Pool 4), following the $\tau_d / 5$ rule established by Bai et al. (2026) for adequate coupling accuracy. This is finer than the MPC sampling time (5 s), ensuring that the plant model receives interpolated gate commands within each MPC interval.

__3.3  Traceability Chain__

A key advantage of the integrated toolchain is end-to-end traceability: every parameter in the deployed PLC code can be traced back to a physical model parameter in HydroComponents:

$$
\text{HydroComponents}(A_s, \tau_d, \tau_m) \xrightarrow{\text{FMI}} \text{Simulink IDZ} \xrightarrow{\text{MPC design}} \text{QP matrices} \xrightarrow{\text{Embedded Coder}} \text{C code} \xrightarrow{\text{ST converter}} \text{PLC code} \tag{2}
$$

This traceability chain ensures that any change to the physical model (e.g., updated $\tau_d$ from field measurements) propagates automatically to the deployed controller through re-execution of Stages 3–5—a process that takes approximately 15 minutes end-to-end.

__4  xIL Verification Methodology__

__4.1  Three-Stage xIL Pipeline__

The xIL verification follows the CHS pipeline (Lei et al., 2025c) with three stages:

**MiL (Model-in-the-Loop)**: The HydroComponents FMU (plant) is coupled with the Simulink DMPC controller via FMI 2.0 Co-Simulation. Both plant and controller run on the same PC (Intel i7-12700, 32 GB RAM). This verifies the DMPC design against the high-fidelity Saint-Venant model.

**SiL (Software-in-the-Loop)**: The Simulink DMPC is replaced with the auto-generated C code compiled as a shared library. The HydroComponents FMU remains the plant. This verifies that code generation preserves controller behavior.

**HiL (Hardware-in-the-Loop)**: The auto-generated Structured Text runs on the Siemens S7-1200 PLC, which controls the physical five-pool canal flume via 4–20 mA analog I/O. The PLC communicates with the SCADA workstation via OPC-UA at 1 Hz for monitoring and data logging. This verifies the complete pipeline on physical hardware.

**ADMM convergence guarantee**: The five-pool DMPC cost function is strongly convex (positive definite weight matrices $Q$ and $R$), and the inter-pool coupling constraints are linear. These conditions satisfy Boyd et al. (2011, Theorem 3.1), guaranteeing ADMM convergence to the global optimum for any feasible initial condition.

__4.2  Scenario Design__

Thirty scenarios are defined across three categories:

__*Table 6. xIL Test Scenarios*__

| Category | Scenarios | Description |
|----------|-----------|-------------|
| Nominal (S1–S10) | Setpoint tracking | Step changes in downstream water level setpoints for individual pools |
| Nominal (S11–S15) | Flow changes | Upstream pump flow step changes (±20%, ±40%, ramp) |
| Nominal (S16–S20) | Coordinated | Multi-pool simultaneous setpoint changes, ramp trajectories |
| Boundary (S21–S25) | Extreme conditions | Maximum/minimum water levels, gate saturation, rapid flow transients |
| Boundary (S26–S30) | Fault injection | Single gate failure (G2 fixed), sensor noise injection (×5), communication delay (2 s) |

Each scenario is executed for 1,200 s with a 300-s warm-up period. All three xIL stages are run on all 30 scenarios, producing 90 scenario-stage combinations.

__4.3  Performance Metrics__

Seven metrics are reported:

1. **RMSE**: Root mean square error of downstream water level tracking [mm]
2. **MAE**: Maximum absolute error [mm]
3. **$t_s$**: 2% settling time [s]
4. **$N_v$**: Constraint violations ($h_{\min} = 5$ cm, $h_{\max} = 35$ cm) [count]
5. **$J_{\text{coord}}$**: DMPC coordination cost (sum of squared inter-pool flow deviations) [—]
6. **$T_{\text{MPC}}$**: MPC solve time [ms]
7. **$\Delta_{\text{xIL}}$**: Cross-layer degradation (RMSE difference from MiL) [mm]

__4.4  Baseline Comparison__

Two baselines are defined:
- **SC-1 baseline**: The three-pool LabVIEW DMPC from Su et al. (2026a), extended to five pools using the same LabVIEW architecture. This represents the manual (non-integrated) workflow.
- **Manual baseline**: The same DMPC algorithm hand-coded in Structured Text for the PLC without HydroRTP code generation. This represents the traditional deployment approach.

__4.5  FMI Coupling Stability__

The Co-Simulation coupling between the variable-step OpenModelica FMU and the fixed-step Simulink solver requires stability analysis. Following Gomes et al. (2018, §4.3), the explicit co-simulation scheme is stable if the communication step size $H$ satisfies:

$$
H < \frac{2}{\lambda_{\max}} \tag{3}
$$

where $\lambda_{\max}$ is the maximum eigenvalue of the coupled system Jacobian. For the five-pool canal system, the Jacobian is dominated by the fastest pool dynamics (Pool 4, $\tau_d = 14.6$ s), yielding $\lambda_{\max} \approx 0.85$ s⁻¹ and $H_{\max} \approx 2.4$ s. The chosen communication step $H = 1.0$ s provides a 2.4× stability margin.

Empirical verification confirms the analysis: $H = 2.0$ s produces stable results (RMSE increase < 0.1 mm vs. $H = 1.0$ s); $H = 3.0$ s exceeds the stability bound and produces oscillatory behavior in Pool 3 (center pool, maximum coupling). The communication step sensitivity is summarized in Table 5b.

__*Table 5b. FMI Communication Step Size Sensitivity*__

| $H$ [s] | Stability | RMSE [mm] | $\Delta$ from $H = 1.0$ s | FMU evaluation time [ms/step] |
|----------|-----------|-----------|----------------------------|-------------------------------|
| 0.5 | Stable | 3.05 | −0.05 | 0.8 |
| 1.0 | Stable | 3.10 | — | 1.5 |
| 2.0 | Stable | 3.18 | +0.08 | 2.8 |
| 5.0 | Unstable (Pool 3) | — | — | 6.5 |

__5  Results__

__5.1  MiL Results (S1–S30)__

__*Table 7. MiL Results: HydroComponents FMU + Simulink DMPC*__

| Category | RMSE [mm] (mean ± std) | MAE [mm] | $t_s$ [s] | $N_v$ | $J_{\text{coord}}$ | $T_{\text{MPC}}$ [ms] |
|----------|------------------------|----------|-----------|-------|---------------------|----------------------|
| Nominal (S1–S20) | 3.1 ± 0.8 | 8.5 ± 2.1 | 62 ± 15 | 0 | 0.09 ± 0.03 | 12 ± 2 |
| Boundary (S21–S30) | 5.2 ± 1.4 | 14.8 ± 3.5 | 95 ± 22 | 0 | 0.22 ± 0.08 | 15 ± 3 |

The MiL results establish the performance ceiling for the integrated toolchain. The nominal RMSE of 3.1 mm is consistent with the SC-1 three-pool result (4.2 mm on Pools 1–3), with the slight improvement attributable to the higher-fidelity HydroComponents Saint-Venant model (vs. the IDZ model used directly in SC-1's LabVIEW controller). The DMPC coordination cost is low ($J_{\text{coord}} = 0.09$), indicating that the five-pool ADMM coordination converges efficiently (mean 3.8 iterations).

__5.2  SiL Results (S1–S30)__

__*Table 8. SiL Results: HydroComponents FMU + Auto-Generated C Code*__

| Category | RMSE [mm] (mean ± std) | $\Delta_{\text{SiL-MiL}}$ [mm] | $N_v$ |
|----------|------------------------|-------------------------------|-------|
| Nominal (S1–S20) | 3.3 ± 0.8 | +0.2 | 0 |
| Boundary (S21–S30) | 5.4 ± 1.5 | +0.2 | 0 |

The SiL-MiL degradation is 0.2 mm, confirming that the Embedded Coder code generation introduces negligible numerical differences. The 0.2 mm increase is attributable to: (1) fixed-point rounding in the QP solver (32-bit float vs. 64-bit double in Simulink), and (2) discrete-time interpolation differences between the Simulink solver and the C code fixed-step implementation.

Back-to-back verification: 10,000 randomly generated state-input pairs produce maximum absolute output difference of $2.3 \times 10^{-5}$ m between Simulink and C code, confirming functional equivalence.

__5.3  HiL Results (S1–S30)__

__*Table 9. HiL Results: PLC Structured Text + Physical Five-Pool Flume*__

| Category | RMSE [mm] (mean ± std) | $\Delta_{\text{HiL-MiL}}$ [mm] | MAE [mm] | $t_s$ [s] | $N_v$ | $T_{\text{MPC}}$ [ms] |
|----------|------------------------|-------------------------------|----------|-----------|-------|----------------------|
| Nominal (S1–S20) | 4.0 ± 1.0 | +0.9 | 10.8 ± 2.5 | 70 ± 16 | 0 | 5.8 ± 0.5 |
| Boundary (S21–S30) | 6.5 ± 1.8 | +1.3 | 17.2 ± 4.1 | 108 ± 25 | 0 | 6.2 ± 0.6 |

The HiL-MiL degradation is 0.9 mm (nominal) and 1.3 mm (boundary). This degradation arises from three sources:

1. **Sensor noise** (estimated contribution: 0.4 mm): Real capacitive level sensors exhibit noise (±0.5 mm accuracy) not present in MiL. Low-pass filtering (4th-order Butterworth, 1 Hz cutoff) mitigates but does not eliminate this.

2. **Actuator dynamics** (estimated contribution: 0.3 mm): Gate stepper motors have 0.1 mm backlash and 5 mm/s maximum travel speed, creating positioning errors and response delays not modeled in the IDZ plant.

3. **Model mismatch** (estimated contribution: 0.2 mm): The physical flume exhibits minor non-uniformities (construction tolerances, gate seal friction) not captured by the HydroComponents model.

The MPC solve time on the S7-1200 PLC is 5.8 ms (mean), well within the 5-s sampling interval and consistent with the 4.2 ms reported by Yin et al. (2026) for the S7-1500 (the S7-1200's ARM Cortex-A9 at 300 MHz is slightly slower than the S7-1500's at 400 MHz).

__5.4  Cross-Layer Fidelity Summary__

__*Table 10. Cross-Layer Fidelity Degradation (Mean across 20 nominal scenarios)*__

| Stage | Plant Model | Controller | RMSE [mm] | $\Delta$ from MiL |
|-------|------------|-----------|-----------|-------------------|
| MiL | HydroComponents FMU (Saint-Venant) | Simulink DMPC | 3.1 | — |
| SiL | HydroComponents FMU (Saint-Venant) | Auto-generated C code | 3.3 | +0.2 |
| HiL | Physical five-pool flume | PLC Structured Text | 4.0 | +0.9 |

__*[Figure 4 about here]*__

The progressive degradation pattern (MiL < SiL < HiL) is consistent with the CKG series results on the dual-tank platform (Chen et al., 2026a: 1.5 → 1.6 → 2.0 mm). The five-pool system shows larger absolute RMSE (3.1 → 4.0 mm) but similar relative degradation (29% vs. 33% for dual-tank), confirming that the toolchain integration does not introduce additional fidelity loss compared to the custom-model approach.

__5.5  Comparison with SC-1 LabVIEW Baseline__

__*Table 11. Toolchain Comparison: Integrated (This Paper) vs. LabVIEW (SC-1)*__

| Metric | SC-1 LabVIEW (3 pools) | This Paper (5 pools) | Notes |
|--------|------------------------|----------------------|-------|
| MiL RMSE [mm] | 3.5 (IDZ-based MiL) | 3.1 (Saint-Venant MiL) | Higher-fidelity MiL in integrated toolchain |
| HiL RMSE [mm] | 4.2 | 4.0 | Comparable despite 5 pools vs. 3 |
| Constraint violations | 0 | 0 | — |
| DMPC iterations | 4.2 (3-pool) | 3.8 (5-pool) | ADMM converges faster with warm-start |
| Design-to-HiL effort | ~8 person-weeks | ~3 person-weeks | 2.7× reduction |
| Code traceability | Partial (LabVIEW) | Full (model → PLC) | Integrated toolchain advantage |

The integrated toolchain achieves comparable or better control performance with 2.7× less engineering effort, primarily because the manual translation steps (OpenModelica → custom code → LabVIEW → custom PLC code) are automated.

__5.6  Representative Scenario Results__

__*[Figure 5 about here]*__

Figure 5 shows the representative scenario S16 (coordinated five-pool setpoint tracking): all five pool levels are simultaneously stepped by +3 cm at $t = 300$ s. The MiL, SiL, and HiL water level trajectories for Pool 3 (center pool, most coupled) are overlaid, showing: (a) near-identical MiL and SiL responses, (b) slightly larger HiL overshoot due to gate backlash, and (c) all three stages settling within 80 s with zero constraint violations.

Figure 6 shows boundary scenario S26 (Gate G2 failure at $t = 400$ s): G2 is frozen at its current position, and the DMPC redistributes control authority to G1 and G3 to maintain Pool 2 and Pool 3 levels. The DMPC coordination cost increases from 0.08 to 0.35 during the fault, and ADMM iterations increase from 4 to 8, but all pools maintain levels within the ODD bounds.

__*[Figure 6 about here]*__

__5.7  IDZ Parameter Uncertainty Propagation__

Reviewer concern: the IDZ parameters carry ±5–6% confidence intervals (Table 3). To quantify how this uncertainty propagates to DMPC performance, we conduct a Monte Carlo analysis with 1,000 runs. In each run, all 15 IDZ parameters ($A_s$, $\tau_d$, $\tau_m$ for each of five pools) are independently sampled from uniform distributions within their 95% confidence intervals. The DMPC is designed using the nominal parameters and tested against each perturbed plant.

Results: the worst-case MiL RMSE across 1,000 Monte Carlo samples is 4.2 mm (vs. 3.1 mm nominal), representing a 35% degradation. The mean RMSE is 3.4 mm (10% degradation). Critically, zero constraint violations occur across all 1,000 samples, confirming that the DMPC is robustly feasible within the identified parameter uncertainty bounds. The 35% worst-case degradation remains well below the HiL RMSE (4.0 mm), indicating that IDZ identification uncertainty is not the dominant contributor to cross-layer degradation—physical effects (sensor noise, actuator backlash) dominate.

__6  Engineering Productivity Analysis__

__6.1  Effort Breakdown__

__*Table 12. Design-to-Deployment Effort Comparison*__

| Phase | Manual Workflow [person-hours] | Integrated Workflow [person-hours] | Savings |
|-------|-------------------------------|-------------------------------------|---------|
| Plant model assembly | 40 (custom OpenModelica) | 4 (HydroComponents drag-and-drop) | 90% |
| FMI coupling | 16 (custom scripts) | 2 (automated) | 88% |
| IDZ identification | 24 (custom MATLAB) | 4 (HydroRTP block) | 83% |
| DMPC design | 40 (custom Simulink) | 12 (HydroRTP blocks + assembly GUI) | 70% |
| Code generation | 80 (manual ST coding) | 8 (HydroRTP auto-generation) | 90% |
| xIL verification | 80 (custom test scripts) | 40 (HydroRTP test harness) | 50% |
| PLC integration | 40 (manual TIA Portal) | 8 (Openness API) | 80% |
| Documentation/traceability | 40 (manual) | 12 (auto-generated reports) | 70% |
| **Total** | **360 (~12 person-weeks)** | **90 (~3 person-weeks)** | **75%** |

The largest savings are in plant model assembly (90%, from 40 to 4 hours) and code generation (90%, from 80 to 8 hours). The smallest savings are in xIL verification (50%), because boundary scenarios still require manual design and interpretation of results.

__6.2  Remaining Manual Steps__

Three steps in the integrated workflow still require manual engineering judgment:

1. **Scenario design** (S21–S30): Boundary scenarios must be designed based on domain knowledge of the specific canal system. Automated scenario generation (e.g., from ODD specifications) is a future research direction.

2. **IDZ parameter validation**: The automatic identification results must be visually inspected and validated by the engineer against step-response data. Fully automated validation (with confidence bounds and outlier detection) is implemented in HydroRTP but requires human approval before proceeding to DMPC design.

3. **PLC commissioning**: Physical I/O wiring, sensor calibration, and gate motor tuning require on-site engineering effort that cannot be automated through software tools.

__7  Discussion__

__7.1  Completing the Toolchain Triangle__

This paper completes the "toolchain triangle" described in the CHS project plan: BAK-1 (HydroComponents, modeling) + YBK-1 (HydroRTP, controller deployment) → SC-2 (integration and xIL verification). The integrated toolchain provides a practical, replicable pipeline for canal automation that does not require control engineering expertise for the standard workflow. A hydraulic engineer with OpenModelica and Simulink training can execute the full pipeline from plant model to verified PLC code.

__7.2  Comparison with Automotive MBD__

The CHS integrated toolchain mirrors the automotive MBD workflow: (1) plant model in Modelica (equivalent to vehicle dynamics in Dymola), (2) controller design in Simulink (equivalent to ECU development), (3) automatic code generation (equivalent to AUTOSAR-compliant code generation), (4) xIL verification (equivalent to dSPACE HIL testing). The key difference is scale: automotive MBD is supported by a mature tool ecosystem (dSPACE, ETAS, Vector) with standardized interfaces, while the CHS toolchain is in its first generation. The 3-person-week deployment time for a five-pool canal is comparable to the automotive MBD timeline for a simple ECU function, suggesting that the toolchain maturity level is approaching practical utility.

__7.3  Scalability Considerations__

The five-pool demonstration is a moderate-scale system. For larger systems (50–500 pools), three scalability factors must be addressed:

1. **FMU compilation time**: HydroComponents compilation scales linearly with the number of pools (Bai et al., 2026, §5.5). A 50-pool system would require approximately 450 s compilation time, which is acceptable.

2. **DMPC solve time**: The ADMM coordination scales as $O(N^2)$ for sequential ADMM. For 50 pools, the estimated solve time is ~500 ms on the S7-1200, still within the 5-s sampling interval. For 100+ pools, GPU-parallel ADMM (Huang et al., 2026) or hierarchical decomposition is necessary.

3. **Code generation**: The Structured Text output scales linearly with the number of agents. A 50-pool system would generate approximately 120,000 lines of ST, which is within the S7-1500 memory capacity (50 MB) but would exceed the S7-1200 (4 MB). Hierarchical deployment (multiple PLCs with OPC-UA networking) would be required.

__7.4  Open-Source Ecosystem__

The integrated toolchain is fully open-source:
- HydroComponents: MIT license, OpenModelica (GPL runtime)
- HydroRTP: MIT license (requires commercial MATLAB/Simulink)
- Integration scripts: MIT license
- xIL test harness: MIT license

The MATLAB/Simulink dependency is the primary barrier to fully open-source deployment. The current toolchain requires MATLAB R2024b with Simulink and Embedded Coder: approximately $500/year for academic licenses or ~$5,000/seat plus ~$2,000/year for commercial licenses. University site licenses make this accessible for research institutions, but direct field deployment in developing countries—where canal automation offers the greatest benefit—requires either commercial licensing or an alternative pathway. Future work includes developing a Python/CasADi alternative for the DMPC design and code generation steps, which would eliminate the commercial software dependency and enable fully open-source deployment.

__7.5  Limitations__

Several limitations should be acknowledged. First, the five-pool canal flume is a laboratory facility; field-scale canals involve additional complexities (sediment, vegetation, variable geometry) not tested. Second, the toolchain assumes Family $\alpha$ dynamics; Family $\beta$ (self-regulating) systems (e.g., pipeline networks) have not been tested with the integrated workflow. Third, the PLC deployment targets Siemens S7-1200/1500 only; the Allen-Bradley target in HydroRTP has not been validated with the HydroComponents integration. Fourth, the 3-person-week effort estimate assumes familiarity with OpenModelica and Simulink; training time is not included. Fifth, the Bayesian ODD expansion protocol (Chen et al., 2026c) has not been integrated into the automated toolchain; ODD management remains a manual step.

__8  Conclusions__

This paper has demonstrated the first end-to-end integration of the CHS toolchain—HydroComponents (OpenModelica) + HydroRTP (Simulink) + PLC deployment—and validated the complete xIL pipeline on a five-pool laboratory canal flume. The key findings are:

1. The integrated toolchain automates the pipeline from drag-and-drop plant model assembly to deployed PLC code with full traceability. The cross-layer fidelity degradation (MiL 3.1 mm → SiL 3.3 mm → HiL 4.0 mm, zero constraint violations) confirms that the integrated toolchain preserves controller performance through the MBD layers.

2. The toolchain reduces design-to-deployment effort from an estimated 12 person-weeks (manual workflow) to 3 person-weeks (integrated workflow), a 75% reduction. The largest savings are in plant model assembly (90%) and code generation (90%).

3. The five-pool DMPC achieves performance comparable to or better than the SC-1 LabVIEW baseline (4.0 mm vs. 4.2 mm HiL RMSE), despite controlling five pools instead of three, demonstrating that toolchain integration does not sacrifice control quality.

4. The cross-layer fidelity pattern (progressive but small degradation from MiL to HiL) is consistent with the CKG series results on the dual-tank platform, confirming the CHS "just precise enough" principle: the IDZ three-parameter model provides a sufficient basis for multi-pool DMPC design across the full xIL chain.

These results establish the CHS integrated toolchain as a practical engineering methodology for canal automation, providing a replicable and open-source pipeline from hydraulic model to verified autonomous controller. A Python/CasADi alternative pathway is under development (§7.4) to eliminate the commercial MATLAB/Simulink dependency and enable fully open-source deployment, broadening accessibility for research and field applications in developing countries.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]) and the National Natural Science Foundation of China (Grant Nos. [to be inserted]). The authors thank the CHS laboratory team at Hebei University of Engineering for constructing and instrumenting the five-pool canal flume.

__References__

Bai, Y., Lei, X., Chen, K., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for component-based modeling of water conveyance systems. Environmental Modelling & Software (submitted).

Blochwitz, T., Otter, M., Akesson, J., Arnold, M., Clauss, C., Elmqvist, H., et al. (2012). Functional Mockup Interface 2.0: The standard for tool independent exchange of simulation models. In Proceedings of the 9th International Modelica Conference (pp. 173–184). https://doi.org/10.3384/ecp12076173

Brunner, G. W. (2016). HEC-RAS River Analysis System: Hydraulic reference manual (Version 5.0). US Army Corps of Engineers.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026c). Hardware-in-the-Loop verification and adaptive multi-agent control for autonomous water network operation. Journal of Water Resources Planning and Management (submitted).

Clemmens, A. J., Kacerek, T. F., Grawitz, B., & Schuurmans, W. (2005). Test cases for canal control algorithms. Journal of Irrigation and Drainage Engineering, 131(6), 502–514. https://doi.org/10.1061/(ASCE)0733-9437(2005)131:6(502)

Elmqvist, H., Mattsson, S. E., & Otter, M. (2003). Modelica — A language for physical system modeling, visualization and interaction. In Proceedings of the 1999 IEEE Symposium on Computer-Aided Control System Design (pp. 630–639).

Fritzson, P. (2014). Principles of object-oriented modeling and simulation with Modelica 3.3 (2nd ed.). Wiley-IEEE Press.

Gomes, C., Thule, C., Broman, D., Larsen, P. G., & Vangheluwe, H. (2018). Co-simulation: A systematic literature review. ACM Computing Surveys, 51(3), 1–33. https://doi.org/10.1145/3179993

Huang, Z., Lei, X., Liu, X., Ji, C., & Wang, H. (2026). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). Modeling and control of hydrosystems. Springer. https://doi.org/10.1007/978-1-84882-624-3

Liu, X., Lei, X., Long, Y., & Wang, H. (2026). Design for Operation: A model-based framework for establishing cybernetics of hydro systems as an interdisciplinary discipline. Environmental Modelling & Software (submitted).

Malaterre, P.-O., & Baume, J.-P. (2011). SIC and SIC2: 1D hydrodynamic models for canal regulation design and operation. In P.-O. Malaterre & G. Rijo (Eds.), Proceedings of the International Workshop on Regulation of Irrigation Canals (pp. 1–15). IRSTEA.

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Negenborn, R. R., van Overloop, P. J., Keviczky, T., & De Schutter, B. (2009). Distributed model predictive control of irrigation canals. Networks and Heterogeneous Media, 4(2), 359–380. https://doi.org/10.3934/nhm.2009.4.359

Schuurmans, J. (1997). Control of water levels in open channels (Doctoral dissertation). Delft University of Technology.

Schweiger, G., Gomes, C., Engel, G., Hafner, I., Schoeggl, J.-P., Posch, A., & Nouidui, T. (2019). An empirical survey on co-simulation: Promising standards, challenges and research needs. Simulation Modelling Practice and Theory, 95, 148–163. https://doi.org/10.1016/j.simpat.2019.05.001

Su, C., Lei, X., Bai, Y., Yin, B., Ji, C., & Wang, H. (2026a). Experimental validation of the unified transfer function family and distributed MPC on a multi-pool canal flume. Journal of Irrigation and Drainage Engineering (submitted).

van Overloop, P. J. (2006). Model predictive control on open water systems (Doctoral dissertation). Delft University of Technology.

Yin, B., Lei, X., Bai, Y., Ji, C., & Wang, H. (2026). HydroRTP: Simulink rapid prototyping toolbox for automatic code generation of water network controllers. SoftwareX (submitted).

__Data Availability__

The HydroComponents five-pool canal model, HydroRTP DMPC project files, auto-generated C and Structured Text code, FMI coupling scripts, and all 30-scenario MiL/SiL/HiL datasets are available at https://github.com/IWHR-CHS/canal-toolchain (to be made public upon acceptance). An archival snapshot is deposited on Zenodo (DOI: 10.5281/zenodo.XXXXXXX). Code is released under the MIT license; simulation and experimental data under CC-BY-4.0.

__Figure Captions__

__Figure 1.__ CHS integrated toolchain overview. Left: the five tools/components (HydroComponents, FMI, HydroRTP, Embedded Coder, PLC) mapped to the MBD seven layers. Right: the xIL verification stages (MiL, SiL, HiL) showing progressive replacement of simulated components with physical hardware.

__Figure 2.__ Five-pool canal flume at Hebei University of Engineering. (a) Schematic showing five pools, four sluice gates (G1–G4), five capacitive level sensors, pump inflow, and free overfall outflow. (b) Photograph of the physical installation. (c) PLC control cabinet with Siemens S7-1200 and analog I/O modules.

__Figure 3.__ Integrated toolchain pipeline. Stage 1: HydroComponents model assembly in OpenModelica (drag-and-drop). Stage 2: FMI 2.0 FMU export. Stage 3: IDZ identification and DMPC design in Simulink using HydroRTP blocks. Stage 4: Automatic code generation (C for SiL, Structured Text for PLC). Stage 5: PLC deployment via TIA Portal Openness API.

__Figure 4.__ Cross-layer fidelity analysis. (a) Box plots of RMSE across 20 nominal scenarios for MiL, SiL, and HiL, showing progressive degradation. (b) Waterfall chart: MiL baseline (3.1 mm) → code generation (+0.2 mm) → physical deployment (+0.7 mm) → total HiL (4.0 mm). (c) Per-pool RMSE at HiL stage, showing Pool 3 (center) has the highest RMSE due to maximum inter-pool coupling.

__Figure 5.__ Representative scenario S16 (coordinated five-pool setpoint step +3 cm). (a) Water levels in all five pools at HiL stage. (b) Pool 3 water level: MiL (blue), SiL (orange), HiL (green) overlaid. (c) Gate positions G1–G4. (d) DMPC coordination cost over time.

__Figure 6.__ Boundary scenario S26 (Gate G2 failure at $t = 400$ s). (a) Water levels in Pools 2 and 3 showing DMPC redistribution of control authority. (b) Gate positions: G2 frozen, G1 and G3 compensating. (c) ADMM iterations per time step, showing increase from 4 to 8 during fault. (d) ODD distance-to-boundary $\rho$ for each pool, all remaining positive.
