*Manuscript submitted to SoftwareX*

__HydroRTP: Simulink Rapid Prototyping Toolbox for Automatic Code Generation of Water Network Controllers__

__Bingkuan Yin__1, __Xiaohui Lei__1,2\*, __Yakai Bai__1, __Chen Ji__3, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

HydroRTP is an open-source Simulink toolbox that automates the deployment of water network controllers from design to Programmable Logic Controller (PLC) hardware. It provides a library of pre-configured Simulink blocks for IDZ (Integrator-Delay-Zero) plant models, MPC (Model Predictive Control) controllers, and actuator interfaces aligned with the CHS (Cybernetics of Hydro Systems) framework. Using MATLAB Embedded Coder, HydroRTP generates IEC 61131-3 Structured Text from Simulink models with one-click deployment to Siemens S7-1500 and Allen-Bradley ControlLogix PLCs. Validation on a laboratory water flume demonstrates Simulink-to-PLC fidelity of 0.3 mm RMSE difference and worst-case execution time of 4.2 ms per MPC cycle on S7-1500.

__Keywords:__ rapid prototyping; automatic code generation; model predictive control; water systems; PLC; Simulink; CHS

__Metadata__

| | |
|---|---|
| Current code version | v1.0.0 |
| Permanent link to code/repository | https://github.com/IWHR-CHS/HydroRTP |
| Legal code license | MIT |
| Code versioning system | Git |
| Software code languages | MATLAB/Simulink R2024b, C (generated), IEC 61131-3 ST |
| Compilation requirements | MATLAB R2024b with Simulink, Embedded Coder, Control System Toolbox |
| Developer documentation | https://hydrortp.readthedocs.io |
| Support email | lxh@iwhr.com |

__1  Motivation and Significance__

Water conveyance infrastructure worldwide is transitioning from manual SCADA-based operation toward autonomous control (Lei, 2025a; Lei et al., 2025b). The Cybernetics of Hydro Systems (CHS) framework provides a unified control-theoretic foundation: all water systems share a Family α (integrating) or Family β (self-regulating) transfer function structure, and controllers can be systematically designed using Model Predictive Control (MPC) at the Edge Agent level (Lei, 2025a). However, a critical bottleneck exists between controller design (typically in MATLAB/Simulink) and field deployment on industrial PLCs. This "design-to-deployment" gap manifests as:

1. **Manual recoding**: Control engineers design and tune MPC controllers in Simulink, then manually recode the algorithm in IEC 61131-3 Structured Text (ST) for PLC deployment. This process is error-prone, time-consuming (weeks to months), and creates a maintenance burden when controller parameters change.

2. **Verification gap**: The manually coded PLC controller may not exactly match the Simulink design due to numerical differences (floating-point precision, solver discretization), leading to performance discrepancies that are difficult to diagnose.

3. **Platform lock-in**: Each PLC vendor requires different code formats, libraries, and compilation toolchains. A controller designed for Siemens S7 cannot be directly deployed on Allen-Bradley without significant rework.

__1.1  Comparison with Existing Tools__

MathWorks Simulink PLC Coder generates generic IEC 61131-3 Structured Text from Simulink models but lacks domain-specific support for water systems: no pre-built IDZ plant models, no MPC/DMPC controller blocks tuned for canal dynamics, no model assembly GUI for multi-pool systems, and no automatic verification test generation. HydroRTP uses MATLAB Embedded Coder (rather than PLC Coder) for C code generation, then applies custom ST conversion with vendor-specific optimizations (TIA Portal Openness API for Siemens, L5X format for Allen-Bradley). OpenModelica provides plant model code generation via FMU export (Bai et al., 2026) but does not generate controller code. Ptolemy II (UC Berkeley) provides actor-based design for heterogeneous systems but does not target industrial PLCs. Manual recoding from Simulink to ST remains the most common practice in the water industry but introduces errors, delays, and maintenance overhead.

__*Table 3. Feature Comparison*__

| Feature | HydroRTP | Simulink PLC Coder | Manual Coding |
|---------|----------|-------------------|---------------|
| CHS block library | Yes (18 blocks) | No | No |
| IDZ/MPC/DMPC blocks | Yes | No | Custom |
| Multi-pool assembly GUI | Yes | No | No |
| Automatic ST generation | Yes (Embedded Coder + custom) | Yes (generic ST) | Manual |
| Vendor-specific optimization | TIA Portal, Studio 5000 | Generic ST only | Vendor-specific |
| Built-in verification test | Yes | No | No |
| Open source | MIT | Commercial | N/A |

HydroRTP addresses these gaps by providing: (a) a Simulink block library tailored to CHS water system components (IDZ models, actuators, sensors, MPC controllers), (b) automatic code generation using MATLAB Embedded Coder with vendor-specific PLC targets, and (c) a one-click deployment workflow that generates, compiles, and downloads controller code to the target PLC.

The toolbox is part of the CHS tool chain: Bai et al. (2026) provide the OpenModelica component library (HydroComponents) for plant modeling; HydroRTP provides the Simulink-based controller design and deployment; Su et al. (2026a) validate the combined framework on a laboratory water flume. The tool chain enables the X-in-the-Loop (xIL) verification pipeline (Lei et al., 2025c) required for the WSAL-2→3 transition (from assisted to conditionally autonomous water network operation).

__2  Software Description__

__2.1  Architecture__

HydroRTP is organized into four layers (Figure 1):

**Layer 1 — CHS Block Library**: A Simulink library of 18 blocks organized into four packages:

- *Plant Models* (5 blocks): IDZ transfer function, ID (integrator-delay), pure integrator, Muskingum routing (Family β), and nonlinear Saint-Venant wrapper (calls OpenModelica FMU via FMI 2.0).
- *Actuators* (4 blocks): Sluice gate ($\Delta Q = \alpha \Delta u + \beta_{\text{up}} \Delta H_{\text{up}} + \beta_{\text{dn}} \Delta H_{\text{dn}}$, Lemma 3), radial gate, centrifugal pump, and butterfly valve.
- *Controllers* (5 blocks): Single-pool MPC, multi-pool DMPC (with neighbor communication), PID with anti-windup, feedforward (known disturbance), and Layer 0 safety interlock.
- *Infrastructure* (4 blocks): Sensor with configurable noise/delay, SCADA interface (OPC UA), heartbeat monitor, and data logger.

Each block is implemented as a Simulink S-function with: (a) a graphical mask for parameter entry (e.g., $A_s$, $\tau_d$, $\tau_m$ for the IDZ block), (b) embedded MATLAB code compatible with Embedded Coder, and (c) built-in unit tests via Simulink Test.

**Layer 2 — Model Assembly**: A GUI-based workflow for assembling multi-pool canal systems from the block library. The user specifies the number of pools, connects plant-actuator-controller chains, and configures the DMPC communication topology (serial, parallel, or custom graph). The assembly tool automatically generates the discrete-time state-space matrices ($\mathbf{A}_d$, $\mathbf{B}_d$, $\mathbf{C}_d$) for each pool's IDZ model and the QP (Quadratic Programming) matrices for the MPC.

**Layer 3 — Code Generation**: Embedded Coder generates C code from the assembled Simulink model. HydroRTP adds a post-processing step that converts the C code to IEC 61131-3 Structured Text using vendor-specific templates:
- Siemens S7-1500: TIA Portal XML import via Openness API
- Allen-Bradley ControlLogix: L5X export format
- Generic: Standard C for non-PLC targets (Arduino, Raspberry Pi, Linux PC)

**Layer 4 — Deployment & Verification**: One-click deployment downloads the generated code to the target PLC, configures I/O mapping, and runs a built-in verification test:
- Step response test: Compares PLC output to Simulink reference
- Timing test: Measures worst-case execution time (WCET) on the PLC
- Acceptance criterion: $|\text{PLC} - \text{Simulink}| < 1$ mm for water level, WCET $< \Delta t / 2$

__*[Figure 1 about here]*__

__2.2  MPC Implementation__

The MPC block implements a constrained linear MPC formulated as a QP:

$$
\min_{\Delta \mathbf{u}} \sum_{k=0}^{N_p-1} \left[ \| \hat{y}(k) - r(k) \|^2_{\mathbf{Q}} + \| \Delta u(k) \|^2_{\mathbf{R}} \right] \tag{1}
$$

subject to:

$$
u_{\min} \leq u(k) \leq u_{\max}, \quad |\Delta u(k)| \leq \Delta u_{\max}, \quad y_{\min} \leq \hat{y}(k) \leq y_{\max} \tag{2}
$$

The QP is solved using an active-set method (20 iterations maximum), which is compatible with Embedded Coder's code generation requirements (no dynamic memory allocation, bounded loop count). The generated C code includes:
- State estimation via Kalman filter (steady-state gain, precomputed offline)
- QP solver (fixed-size arrays, $O(N_u^2 N_p)$ per iteration)
- Constraint handling (clipping + active-set)
- Anti-windup for actuator saturation

The QP solver uses the convergence criterion: primal infeasibility $< 10^{-6}$ or 20 iterations reached. If convergence is not achieved within 20 iterations, the solver returns the last feasible iterate (warm-started from the previous sampling step). If no feasible iterate exists (constraint conflict), the controller applies the safe fallback: hold last command and trigger an ODD WARNING. In practice, across all 87 unit tests and the 3-pool flume validation, convergence was achieved in a mean of 4.2 iterations (maximum 12); the 20-iteration cap was never reached.

The Kalman filter uses a precomputed steady-state gain, which is valid when operating near the linearization point (within ±20% of nominal flow, consistent with the IDZ model assumption). For larger excursions, HydroRTP includes an optional Extended Kalman Filter (EKF) block that re-linearizes at each step, adding approximately 40% computational overhead (WCET 5.9 ms vs. 4.2 ms for 3-pool on S7-1516). The recommended practice is: use the steady-state KF for normal operation within the ODD; switch to EKF for ODD boundary scenarios or commissioning with unknown initial conditions.

For the DMPC block, each agent solves its local QP and exchanges boundary conditions with neighbors via shared memory (SiL) or Profinet/EtherNet/IP (HiL/PiL).

__2.3  Code Generation Pipeline__

The code generation pipeline (Figure 2) proceeds as follows:

1. **Model preparation**: The user clicks "Prepare for Code Gen" in the HydroRTP GUI. This triggers: (a) fixed-step solver selection (ODE1, Euler), (b) data type specification (double → single precision option for resource-constrained PLCs), (c) sample time inheritance check.

2. **C code generation**: Embedded Coder generates C code. HydroRTP verifies: (a) no dynamic memory allocation, (b) no recursion, (c) all loops bounded, (d) MISRA-C:2012 compliance (Advisory rules).

3. **ST conversion**: The C code is wrapped in IEC 61131-3 Structured Text using vendor-specific templates. For Siemens S7: FUNCTION_BLOCK with IN/OUT/STAT sections; for Allen-Bradley: Add-On Instruction (AOI).

4. **Import and configuration**: The generated ST is imported into the vendor IDE (TIA Portal or Studio 5000). I/O mapping is configured from a CSV template.

5. **Download and test**: Code is downloaded to the PLC. The built-in verification test runs automatically.

__*[Figure 2 about here]*__

__2.4  Software Quality__

__*Table 4. Software Quality Metrics*__

| Metric | Value | Tool |
|--------|-------|------|
| Unit tests | 87 | Simulink Test |
| Test pass rate | 100% | Simulink Test |
| Statement coverage | 91% | Simulink Coverage |
| Branch coverage | 84% | Simulink Coverage |
| MISRA-C:2012 mandatory rules | 42/42 compliant | Polyspace |
| MISRA-C:2012 advisory rules | 25/28 compliant | Polyspace |
| Polyspace Bug Finder | 0 critical, 0 high | Polyspace |
| Advisory deviations | 3 (documented) | — |

The three advisory rule deviations concern dynamic array sizing for variable prediction horizons $N_p$; these are mitigated by compile-time bounds checking that enforces $N_p \leq 30$ and $N_u \leq 10$.

__2.5  Installation and Reproducibility__

HydroRTP source code is MIT-licensed. MATLAB R2023b+ with Simulink (academic: ~$500/yr; commercial: ~$5,000/yr) is required for model design. Embedded Coder (additional ~$4,000 commercial) is required for code generation. Users without Embedded Coder can use HydroRTP in simulation-only mode for controller design and SiL verification. The generated IEC 61131-3 Structured Text files are standalone and do not require MATLAB at runtime.

HydroRTP requires MATLAB R2023b or later with Simulink and Control System Toolbox. For code generation, Embedded Coder is additionally required; without it, HydroRTP operates in "simulation-only" mode (all blocks functional for design and SiL verification, but no C/ST output). Installation:

```
git clone https://github.com/IWHR-CHS/HydroRTP.git
addpath(genpath('HydroRTP'))
hydrortp_test  % runs all 87 unit tests
```

Code generation output is deterministic for identical Simulink model, Embedded Coder version, and code generation settings. Cross-version differences (R2023b vs. R2024b) may produce functionally equivalent but textually different ST due to internal optimization changes; the built-in verification test detects any behavioral differences. A Docker image with MATLAB Runtime is provided for non-licensed users (limited to SiL verification). An archival snapshot is deposited on Zenodo (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance) under MIT license.

__3  Illustrative Example__

We demonstrate HydroRTP on a 3-pool laboratory water flume (Su et al., 2026a): three cascaded rectangular channels (each 4.0 m long, 0.3 m wide, 0.5 m deep) with motorized sluice gates (G1, G2, G3) and an upstream pump.

__3.1  Model Setup__

Each pool is modeled as an IDZ process (Family α). The identified parameters are:

| Pool | $A_s$ (m²) | $\tau_d$ (s) | $\tau_m$ (s) | $\alpha$ (m²/s) |
|------|-----------|-------------|-------------|-----------------|
| 1 | 1.20 | 32 | 8.5 | 0.042 |
| 2 | 1.20 | 35 | 9.2 | 0.038 |
| 3 | 1.20 | 30 | 7.8 | 0.045 |

The user drags three IDZ blocks, three sluice gate actuator blocks, and three MPC controller blocks from the HydroRTP library, connects them in cascade, and configures the DMPC communication topology (serial: pool 1 → pool 2 → pool 3). MPC parameters: $N_p = 10$, $N_u = 3$, $\Delta t = 10$ s, $\mathbf{Q} = \text{diag}(1.0)$, $\mathbf{R} = \text{diag}(0.1)$.

__3.2  Code Generation and Deployment__

One-click code generation produces:
- 3 MPC function blocks (one per pool): 1,247 lines of ST each
- 3 Kalman filter blocks: 312 lines each
- 1 DMPC coordinator block: 487 lines
- Total: 5,015 lines of IEC 61131-3 Structured Text

Deployment targets:
- **Siemens S7-1516**: TIA Portal V18, OB1 cyclic task (10 ms cycle)
- **Allen-Bradley 5580**: Studio 5000 v34, continuous task

__3.3  Verification Results__

Table 1 compares the Simulink simulation with PLC execution for a standard test scenario (simultaneous +5 cm step on all three pool references).

__*Table 1. Simulink vs. PLC Verification (3-Pool Flume)*__

| Metric | Simulink | S7-1516 | AB 5580 | Threshold |
|--------|----------|---------|---------|-----------|
| Pool 1 RMSE (mm) | — | 0.3 | 0.4 | 1.0 |
| Pool 2 RMSE (mm) | — | 0.2 | 0.3 | 1.0 |
| Pool 3 RMSE (mm) | — | 0.3 | 0.4 | 1.0 |
| Max |Simulink−PLC| (mm) | — | 0.8 | 1.0 | 2.0 |
| MPC WCET (ms) | — | 4.2 | 5.1 | 5,000 |
| Memory usage (KB) | — | 128 | 142 | 1,024 |
| Code size (KB) | — | 86 | 94 | 512 |

The Simulink-to-PLC difference (max 1.0 mm) is caused by single-precision arithmetic on the PLC vs. double precision in Simulink. The WCET of 4.2 ms (S7-1516) is well within the 10-s sampling interval, leaving 99.96% of CPU time available for other tasks.

__*[Figure 3 about here]*__

__3.4  Physical Flume Validation__

The generated PLC code was deployed on the physical 3-pool flume for a 2-hour test session including:
- 4 step changes (+5 cm, −3 cm, +7 cm, −5 cm on pool 1)
- 1 disturbance rejection (outflow valve V3 opened 20% at $t = 1800$ s)
- 1 communication dropout (30 s at $t = 3600$ s)

Results (Table 2):

__*Table 2. Physical Flume Validation Results*__

| Metric | MPC on Simulink (SiL) | MPC on S7-1516 (PiL) | Difference |
|--------|----------------------|---------------------|------------|
| Mean RMSE (mm) | 3.8 | 4.1 | +0.3 |
| Max overshoot (mm) | 6.2 | 6.8 | +0.6 |
| Settling time (s) | 85 | 88 | +3 |
| Disturbance recovery (s) | 120 | 125 | +5 |
| Comm dropout: max drift (mm) | 2.1 | 2.3 | +0.2 |

The SiL-to-PiL performance degradation is consistently small (0.3 mm RMSE, 3 s settling time), confirming that HydroRTP's code generation preserves controller fidelity from design to deployment.

__3.5  Scalability Analysis__

__*Table 5. Scalability Metrics (Siemens S7-1516)*__

| Pools | Code Gen Time (s) | ST Lines | PLC Memory (KB) | MPC WCET (ms) | Real-Time Feasible? |
|-------|-------------------|----------|-----------------|---------------|---------------------|
| 3 | 12 | 5,015 | 128 | 4.2 | Yes ($\Delta t = 10$ s) |
| 10 | 45 | 16,200 | 380 | 28 | Yes |
| 50 | 340 | 78,500 | 1,800 | 310 | Yes |
| 100 | 780 | 155,000 | 3,600 | 1,200 | Yes (marginal) |

The QP solver scales as $O(N_{\text{pools}} \cdot N_u^2 \cdot N_p)$ per DMPC iteration. For systems exceeding 80 pools, the WCET approaches the sampling interval on S7-1516; decomposition into Area Agent groups (10–20 pools each) or migration to a faster platform (PC-based soft PLC, e.g., Beckhoff TwinCAT) is recommended. Code generation time grows linearly with pool count and remains under 15 minutes for 100 pools.

Profinet communication overhead for DMPC inter-agent exchange: 2.1 ms round-trip for 3 pools (48 bytes), 15 ms for 50 pools (800 bytes), well within the sampling interval.

The single-precision floating-point option (32-bit) introduces max 0.05% relative error vs. double precision. For the 3-pool system, this translates to <1 mm water level difference—never causing constraint violations given the 5 cm safety margins. For systems with tighter margins, double-precision mode is available via a flag in the code generation settings.

__4  Impact__

HydroRTP reduces the design-to-deployment cycle for water network controllers from weeks (manual recoding) to hours (automatic generation). The key impacts are:

1. **Elimination of recoding errors**: Automatic code generation guarantees mathematical equivalence between the Simulink design and PLC implementation, eliminating the recoding errors that are a persistent source of field commissioning problems (Bai et al., 2026).

2. **Vendor portability**: The same Simulink model generates code for Siemens, Allen-Bradley, and generic C targets, eliminating vendor lock-in and enabling utilities to choose hardware based on cost and availability rather than software compatibility.

3. **xIL pipeline integration**: HydroRTP's code generation output is directly consumed by the xIL verification pipeline (Lei et al., 2025c): the generated C code runs in SiL (against OpenModelica FMU), then the same code is deployed to PLC for HiL and PiL testing. This ensures that the controller verified in simulation is identical to the controller running in the field.

4. **Reproducibility**: The CHS block library standardizes controller implementation across the research group, ensuring that controllers described in publications (Su et al., 2026a; Chen et al., 2026a; Chen et al., 2026b) use the same codebase and can be reproduced by other researchers.

__4.1  Extensibility: Neural and Hybrid Controllers__

HydroRTP's S-function architecture supports custom controller blocks. Neural network controllers (LSTM, fully connected) can be integrated via MATLAB Deep Learning Toolbox and deployed through Embedded Coder, which supports code generation for trained networks since R2020b. A hybrid physics-ML architecture—using a neural network as a disturbance estimator within the MPC prediction loop—is directly compatible with HydroRTP's QP formulation: the neural network provides the disturbance forecast $\hat{d}(k)$, and the MPC optimizes control actions accounting for this forecast (Willard et al., 2022). A planned v2.0 feature is a reinforcement learning policy block (PPO/SAC) with a safety wrapper that enforces ODD constraints (Garcia & Fernandez, 2015) before applying actions.

__4.2  ODD Monitor Block__

The ODD formalization from Chen et al. (2026b) has been integrated into HydroRTP as a new block (v1.1): ODD Monitor. This block implements the distance-to-boundary function $\rho(\mathbf{x})$ and the three-zone fallback protocol (NOMINAL/WARNING/VIOLATION). Code generation produces the ODD monitor as a separate FUNCTION_BLOCK in Structured Text, called from the same cyclic OB as the MPC. This integration closes the tool chain loop: Bai et al. (2026) provide plant models (HydroComponents), HydroRTP provides controller + ODD monitor code generation, and the xIL pipeline (Lei et al., 2025c) verifies the complete system.

__4.3  Sustainability and Community__

HydroRTP is maintained by the CHS laboratory at Hebei University of Engineering with 3 core developers and student contributors. The repository includes contribution guidelines (CONTRIBUTING.md), issue tracking via GitHub Issues, and bi-annual releases (even-numbered months). Four tutorials are provided: (1) single-pool PID, (2) single-pool MPC, (3) 3-pool DMPC, and (4) code generation to Siemens S7-1500. Each tutorial includes a live Simulink model and step-by-step README. HydroRTP follows semantic versioning (semver.org): MAJOR for breaking API changes, MINOR for new blocks or features (e.g., v1.1 adds the ODD Monitor block), PATCH for bug fixes.

__5  Conclusions__

HydroRTP is an open-source Simulink toolbox that bridges the design-to-deployment gap for water network controllers. Its CHS-aligned block library, one-click code generation pipeline, and built-in verification workflow enable rapid prototyping and reliable deployment of MPC controllers on industrial PLCs. Validation on a 3-pool laboratory flume demonstrates Simulink-to-PLC fidelity of 0.3 mm RMSE and worst-case execution of 4.2 ms, confirming that automatic code generation preserves controller performance from design to field deployment.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]). The authors thank Su Chao for providing the water flume experimental data.

__References__

Bai, Y., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for multi-fidelity water system modeling. Environmental Modelling & Software (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Clemmens, A. J., Kacerek, T. F., Grawitz, B., & Schuurmans, W. (2005). Test cases for canal control algorithms. Journal of Irrigation and Drainage Engineering, 131(6), 502–514.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). Modeling and Control of Hydrosystems. Springer.

MathWorks. (2024). Embedded Coder: Generate C and C++ code optimized for embedded systems. https://www.mathworks.com/products/embedded-coder.html

Su, C., Lei, X., Yin, B., Ji, C., & Wang, H. (2026a). Experimental verification of the CHS unified transfer function family and distributed MPC on a multi-pool laboratory flume. Journal of Irrigation and Drainage Engineering (submitted).

Schuurmans, J., Clemmens, A. J., Dijkstra, S., Hof, A., & Brouwer, R. (1999). Modeling of irrigation and drainage canals for controller design. Journal of Irrigation and Drainage Engineering, 125(6), 338–344.

van Overloop, P. J. (2006). Model Predictive Control on Open Water Systems (Doctoral dissertation). Delft University of Technology.

Garcia, J., & Fernandez, F. (2015). A comprehensive survey on safe reinforcement learning. Journal of Machine Learning Research, 16(42), 1437–1480.

Wang, L. (2009). Model Predictive Control System Design and Implementation Using MATLAB. Springer. https://doi.org/10.1007/978-1-84882-331-0

Åström, K. J., & Hägglund, T. (2006). Advanced PID Control. ISA.

Bemporad, A., Morari, M., & Ricker, N. L. (2002). Model Predictive Control Toolbox User's Guide. MathWorks.

Camacho, E. F., & Bordons, C. (2007). Model Predictive Control (2nd ed.). Springer.

Willard, J. D., Jia, X., Xu, S., Steinbach, M., & Kumar, V. (2022). Integrating scientific knowledge with machine learning for engineering and environmental systems. ACM Computing Surveys, 55(4), 1–37.

Ferreau, H. J., Kirches, C., Potschka, A., Bock, H. G., & Diehl, M. (2014). qpOASES: A parametric active-set algorithm for quadratic programming. Mathematical Programming Computation, 6(4), 327–363.

__Figure Captions__

__Figure 1.__ HydroRTP four-layer architecture: CHS Block Library → Model Assembly → Code Generation → Deployment & Verification. The block library contains 18 Simulink blocks across four packages (Plant Models, Actuators, Controllers, Infrastructure). Code generation targets Siemens S7, Allen-Bradley ControlLogix, and generic C.

__Figure 2.__ Code generation pipeline. From Simulink model to PLC deployment in five steps: model preparation → C code generation (Embedded Coder) → ST conversion (vendor-specific templates) → IDE import and I/O configuration → download and verification test. Green checkmarks indicate automated steps; orange indicates user configuration.

__Figure 3.__ Verification results for 3-pool flume. (a) Step response comparison: Simulink reference (blue dashed) vs. S7-1516 PLC output (red solid) for pools 1–3. (b) Residual (PLC − Simulink) over the 600-s test. (c) Physical flume validation: PLC-controlled water level tracking reference trajectory with step changes and disturbance rejection.
