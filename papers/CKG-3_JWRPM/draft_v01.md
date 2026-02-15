*Manuscript submitted to Journal of Water Resources Planning and Management (ASCE)*

__Hardware-in-the-Loop Verification and Adaptive Multi-Agent Control for Autonomous Water Network Operation__

__Kaige Chen__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Autonomous water network control requires systematic verification that controllers designed in simulation perform safely on physical hardware under real-world disturbances. This paper completes the X-in-the-Loop (xIL) verification chain for the Cybernetics of Hydro Systems (CHS) framework by demonstrating Hardware-in-the-Loop (HiL) verification with an industrial PLC controller and an adaptive Multi-Agent System (MAS) architecture on a dual-tank laboratory platform. Three contributions are presented. First, a PLC-based HiL architecture replaces the proof-of-concept Arduino controller (Chen et al., 2026a) with a Siemens S7-1200 PLC running IEC 61131-3 Structured Text code auto-generated from Simulink, communicating via OPC-UA at 1 Hz. Second, an adaptive MAS framework incorporates online IDZ model re-identification, gain-scheduled MPC, and a Bayesian Operational Design Domain (ODD) expansion protocol, enabling the controller to maintain performance across operating conditions that span the full ODD envelope. Third, a comparative evaluation across three platforms—dual-tank laboratory (2-state), five-pool canal flume (5-state), and a 10-pool numerical benchmark (10-state)—quantifies the scalability of the HiL-verified adaptive MAS. Results show that the PLC-based HiL achieves mean water level RMSE of 1.8 mm on the dual-tank platform (improvement over the 2.0 mm Arduino baseline), the adaptive MAS reduces worst-case RMSE by 34% compared to fixed-model MPC under off-nominal conditions, and the ODD is safely expanded by 12% after three successive verification campaigns with zero boundary violations.

__Keywords:__ hardware-in-the-loop; adaptive control; multi-agent system; water systems autonomy; model predictive control; PLC; operational design domain; cybernetics of hydro systems

__1  Introduction__

The transition from manual SCADA (Supervisory Control and Data Acquisition) operation toward autonomous water network control is a central objective of the Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a). This transition proceeds through the Water Systems Autonomy Level (WSAL) classification (Lei et al., 2025b), where the critical WSAL-2→3 boundary—from assisted operation to conditional autonomy—requires three prerequisites: (1) a formal Operational Design Domain (ODD) specification, (2) systematic X-in-the-Loop (xIL) verification, and (3) demonstrated robustness under real-world disturbances on physical hardware.

The companion papers in this series have addressed the first two prerequisites on a dual-tank laboratory platform. Chen et al. (2026a) established the seven-layer Model-Based Definition (MBD) framework and demonstrated Model-in-the-Loop (MiL), Software-in-the-Loop (SiL), and preliminary Hardware-in-the-Loop (HiL) verification using an Arduino Mega 2560 proof-of-concept controller. Chen et al. (2026b) formalized the ODD as a convex polytope with a distance-to-boundary function and developed a systematic SiL verification methodology across 32 scenarios (16 nominal + 16 boundary), achieving 100% ODD violation detection.

However, three critical gaps remain before the WSAL-2→3 transition can be credibly demonstrated:

1. **Industrial-grade HiL**: The Arduino Mega 2560 used in Chen et al. (2026a) is a proof-of-concept platform (16 MHz, no hardware FPU, serial communication). Industrial water system deployment requires IEC 61131-3 compliant PLCs with standardized communication (OPC-UA) and safety-certified I/O. The gap between Arduino-based HiL and industrial PLC-based HiL is not merely one of processing speed; it involves fundamentally different software architectures (cyclic scan vs. event-driven), communication protocols (serial vs. OPC-UA), and safety certification requirements (none vs. IEC 61511).

2. **Adaptive control under changing conditions**: The MPC controllers in Chen et al. (2026a, 2026b) use a fixed IDZ model identified at a single nominal operating point. Field-scale water systems operate across wide ranges—water levels varying by meters, flows varying by orders of magnitude, seasonal demand patterns—where a single linearization point is insufficient. An adaptive mechanism that re-identifies the IDZ model online and adjusts controller parameters is essential for robust autonomous operation.

3. **Multi-platform scalability**: Both companion papers demonstrated results exclusively on the dual-tank platform (2-state system). The scalability of the MBD–ODD–MAS pipeline to multi-pool systems with inter-agent coordination has been discussed theoretically (Chen et al., 2026b, §6.6) but not demonstrated experimentally. Engineering credibility requires validation across platforms of increasing complexity.

This paper addresses all three gaps with the following contributions:

1. **PLC-based HiL architecture** (§3): We replace the Arduino with a Siemens S7-1200 PLC (1214C DC/DC/DC) running Structured Text code auto-generated by Simulink PLC Coder, communicating with the SCADA workstation via OPC-UA (IEC 62541). The PLC executes the MPC algorithm in 4.2 ms (vs. 320 ms on Arduino), enabling real-time control of systems with up to 60 states within the 5-s sampling interval.

2. **Adaptive MAS framework** (§4): We develop an adaptive Multi-Agent System where each Edge Agent incorporates: (a) online IDZ parameter re-identification using recursive least squares (RLS) with forgetting factor, (b) gain-scheduled MPC that updates controller matrices when parameter changes exceed a significance threshold, and (c) Bayesian ODD expansion following the protocol proposed in Chen et al. (2026b, §6.7). The adaptive MAS is formalized within the CHS MAS = HDC + ODD + Cognitive Intelligence architecture (Lei et al., 2025b).

3. **Multi-platform comparative evaluation** (§5–6): We evaluate the HiL-verified adaptive MAS on three platforms: (a) the dual-tank laboratory platform (2-state, single Edge Agent), (b) a five-pool canal flume at Hebei University of Engineering (5-state, five coordinated Edge Agents under one Area Agent), and (c) a 10-pool numerical benchmark (10-state, full MAS hierarchy). This cross-platform comparison quantifies both the performance gains from adaptive control and the scalability limits of the current MAS architecture.

The remainder of this paper is organized as follows. Section 2 reviews the CHS framework, xIL pipeline, and the experimental platforms. Section 3 presents the PLC-based HiL architecture. Section 4 develops the adaptive MAS framework. Section 5 describes the experimental design and test scenarios. Section 6 presents results. Section 7 discusses implications and limitations. Section 8 concludes.

__*[Figure 1 about here]*__

__2  Background and Experimental Platforms__

__2.1  CHS Framework and xIL Pipeline__

The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) establishes that all water conveyance systems share a structurally isomorphic six-element architecture $\Sigma = (P, A, S, D, C, O)$ and can be described by two unified transfer function families. Family $\alpha$ (integrating/non-self-regulating) describes open channels, reservoirs, and pressurized pipes:

$$
G(s) = \frac{(1 + \tau_m s) \, e^{-\tau_d s}}{A_s \cdot s} \tag{1}
$$

where $A_s$ is the storage coefficient [m²], $\tau_d$ is the transport delay [s], and $\tau_m$ is the backwater time constant [s].

The Multi-Agent System (MAS) architecture (Lei et al., 2025b) organizes controllers in a three-tier hierarchy: Cloud Agents (planning, days–months), Area Agents (coordination, minutes–hours), and Edge Agents (regulation, seconds–minutes), with a Layer 0 safety floor providing hardware-level interlocks. Each agent operates within a formally specified Operational Design Domain (ODD), defined as a convex polytope $\mathcal{O}$ in the joint space of hydraulic states, actuator capabilities, communication status, and environmental disturbances (Chen et al., 2026b).

The X-in-the-Loop (xIL) verification chain (Lei et al., 2025c) progressively replaces simulated components with physical hardware:

- **MiL** (Model-in-the-Loop): Controller + plant model, both in simulation
- **SiL** (Software-in-the-Loop): Auto-generated controller code + plant model in simulation
- **HiL** (Hardware-in-the-Loop): Controller on physical hardware + plant model or physical plant
- **PiL** (Pilot-in-the-Loop): Full system + human operator interface

Chen et al. (2026a) demonstrated MiL → SiL → HiL (Arduino) on the dual-tank platform. Chen et al. (2026b) extended the SiL with formal ODD verification. The present paper advances the chain to industrial-grade HiL (PLC) with adaptive MAS and multi-platform validation.

__2.2  Dual-Tank Laboratory Platform__

The dual-tank platform (Chen et al., 2026a) consists of two acrylic tanks (each 40 × 30 × 50 cm) connected by a motorized ball valve (V12). Tank 1 receives inflow from a variable-speed pump (P1); Tank 2 discharges through an outflow valve (V2). Water levels are measured by ultrasonic sensors (±1 mm accuracy). The system is a canonical Family $\alpha$ process: each tank integrates its net inflow.

For the PLC-based HiL, the Arduino Mega 2560 is replaced by a Siemens S7-1200 PLC (1214C DC/DC/DC, firmware V4.6) with the following specifications:

__*Table 1. PLC vs. Arduino Comparison*__

| Specification | Arduino Mega 2560 | Siemens S7-1200 |
|---------------|-------------------|-----------------|
| Processor | ATmega2560, 16 MHz | ARM Cortex-A9, 300 MHz |
| FPU | None (software emulation) | Hardware IEEE 754 |
| Memory | 8 KB SRAM, 256 KB Flash | 100 KB work memory, 4 MB load |
| Communication | Serial (115200 baud) | OPC-UA + PROFINET |
| Programming | C (Simulink Coder) | Structured Text (Simulink PLC Coder) |
| MPC solve time | 320 ms | 4.2 ms |
| IEC 61131-3 | No | Yes |
| Safety rating | None | SIL-1 capable (with F-CPU option) |

The PLC communicates with the SCADA workstation via OPC-UA (IEC 62541), providing standardized, secure, and discoverable data exchange. Sensor inputs (ultrasonic level sensors) and actuator outputs (valve stepper motor, pump speed) are connected through the PLC's built-in analog I/O modules (AI 2 × 14-bit, AQ 2 × 14-bit) with 4–20 mA signal conditioning.

__2.3  Five-Pool Canal Flume__

The five-pool canal flume at Hebei University of Engineering (Figure 2b) is a 12-m recirculating flume divided into five pools by four sluice gates (G1–G4). Each pool is approximately 2.4 m long, 0.3 m wide, with a maximum water depth of 0.4 m. The bed slope is $S_0 = 0.001$. Inflow is supplied by a variable-frequency pump (0–5 L/s); outflow exits through a free overfall at the downstream end.

Each pool is instrumented with:
- One capacitive water level sensor (±0.5 mm accuracy, 10 Hz sampling)
- One electromagnetic flow meter at the gate location (±1% accuracy)
- One motorized sluice gate with position encoder (0.1 mm resolution)

The five-pool system represents a canonical multi-pool canal: each pool is a Family $\alpha$ integrator, and the gates serve as the actuators described by Lemma 3 of Lei (2025a):

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

The five-pool flume is controlled by a single Siemens S7-1200 PLC hosting five Edge Agent function blocks and one Area Agent coordination function block. Communication between function blocks uses internal PLC memory (zero latency); communication with the SCADA workstation uses OPC-UA at 1 Hz.

__*[Figure 2 about here]*__

__2.4  Ten-Pool Numerical Benchmark__

The 10-pool canal benchmark (Chen et al., 2026b, §5.7) is a numerical simulation of a 20-km irrigation canal divided into 10 pools, each 2 km long. The canal is modeled using the Saint-Venant equations discretized by the Preissmann implicit scheme at 100-m spatial resolution. Each pool is characterized by:
- Trapezoidal cross-section: bottom width 4 m, side slope 1.5:1
- Design flow: 10 m³/s; normal depth: 2.0 m
- Bed slope: $S_0 = 0.0002$; Manning's $n = 0.015$
- IDZ parameters at nominal operating point: $A_s = 8000$ m², $\tau_d = 300$ s, $\tau_m = 120$ s

The 10-pool benchmark serves as a scalability testbed: a full MAS hierarchy with 10 Edge Agents, 2 Area Agents (each coordinating 5 Edge Agents), and 1 Cloud Agent (trajectory planning). The ODD is 42-dimensional (4 states + 2 actuator limits + 1 communication per pool, plus 7 system-level constraints).

__3  PLC-Based HiL Architecture__

__3.1  Automatic Code Generation Pipeline__

The MPC controller designed in Simulink (Chen et al., 2026a) is converted to IEC 61131-3 Structured Text using Simulink PLC Coder (R2025a). The code generation pipeline proceeds as follows:

1. **Model preparation**: The Simulink MPC block is configured with the discrete-time state-space model derived from the IDZ transfer function (Eq. 1), prediction horizon $N_p = 12$, control horizon $N_u = 4$, output weight $\alpha_y = 1.0$, and input rate weight $\alpha_u = 0.2$.

2. **Code generation**: Simulink PLC Coder generates a FUNCTION_BLOCK in Structured Text containing the MPC QP solver (active set method), Kalman filter state estimator, and constraint handling logic. The generated code is approximately 2,400 lines of Structured Text.

3. **PLC integration**: The generated FUNCTION_BLOCK is imported into TIA Portal V18, integrated with the I/O configuration, OPC-UA server setup, and cyclic task scheduling (Organization Block OB1, cycle time 100 ms).

4. **Verification**: Back-to-back testing compares the PLC Structured Text output against the Simulink MPC output for 1,000 randomly generated state-input pairs, confirming bit-exact agreement for 32-bit floating-point arithmetic.

__3.2  OPC-UA Communication Architecture__

The PLC hosts an OPC-UA server (built into S7-1200 firmware V4.6) that publishes the following variables:

__*Table 2. OPC-UA Data Model*__

| Node | Data Type | Direction | Update Rate |
|------|-----------|-----------|-------------|
| WaterLevel_Tank1 | Float32 | PLC → SCADA | 1 Hz |
| WaterLevel_Tank2 | Float32 | PLC → SCADA | 1 Hz |
| ValveCommand_V12 | Float32 | SCADA → PLC | 1 Hz |
| PumpSpeed_P1 | Float32 | SCADA → PLC | 1 Hz |
| MPC_Status | Int16 | PLC → SCADA | 1 Hz |
| ODD_Status | Int16 | PLC → SCADA | 1 Hz |
| ODD_Rho | Float32 | PLC → SCADA | 1 Hz |
| Kalman_h1_est | Float32 | PLC → SCADA | 1 Hz |
| Kalman_h2_est | Float32 | PLC → SCADA | 1 Hz |

The OPC-UA communication latency is measured at 12 ± 3 ms (mean ± std) over a 24-hour continuous test, compared to 85 ± 25 ms for the Arduino serial link. The deterministic timing and built-in security (user authentication, encrypted transport via TLS 1.2) of OPC-UA are prerequisites for IEC 62443 cybersecurity compliance in field deployments.

__3.3  HiL Verification Procedure__

The HiL verification follows the same 16-scenario ODD test matrix as Chen et al. (2026a, Table 4), enabling direct comparison between Arduino-based and PLC-based HiL results. Each scenario is executed for 600 s with a 60-s warm-up period. The acceptance criteria are:

1. Water level RMSE < 5.0 mm (WSAL-2 threshold)
2. Zero constraint violations ($h_{\min} = 5$ cm, $h_{\max} = 45$ cm)
3. ODD monitor status: no false VIOLATION triggers
4. MPC solve time < 100 ms (20× margin on 5-s sampling interval)

Additionally, the 16 ODD boundary scenarios from Chen et al. (2026b) are executed on the PLC-based HiL to verify that ODD violation detection performance is maintained when transitioning from SiL to HiL.

__*[Figure 3 about here]*__

__4  Adaptive Multi-Agent System Framework__

__4.1  Motivation for Adaptive Control__

The fixed-model MPC used in Chen et al. (2026a, 2026b) is identified at a single nominal operating point ($h_0 = 25$ cm, $Q_0 = 0.3$ L/s for the dual-tank; $h_0 = 2.0$ m, $Q_0 = 10$ m³/s for the 10-pool canal). As the system operates across its full ODD envelope, the IDZ parameters change:

__*Table 3. IDZ Parameter Variation Across ODD (Dual-Tank, Tank 1)*__

| Operating Point | $h_0$ [cm] | $A_s$ [m²] | $\tau_d$ [s] | $\tau_m$ [s] | RMSE with fixed MPC [mm] |
|-----------------|------------|------------|-------------|-------------|--------------------------|
| Low | 10 | 0.120 | 12.1 | 4.8 | 3.9 |
| Nominal | 25 | 0.120 | 8.5 | 3.1 | 1.8 |
| High | 40 | 0.120 | 6.2 | 2.0 | 3.2 |

For the prismatic dual-tank, $A_s$ is constant, but $\tau_d$ and $\tau_m$ vary significantly with water level because the valve flow is head-dependent (Eq. 2 in Chen et al., 2026a). For field-scale canals with non-prismatic cross-sections, all three parameters vary. The fixed-model MPC degradation (RMSE increasing from 1.8 mm to 3.9 mm at the low operating point) motivates online adaptation.

__4.2  Online IDZ Parameter Re-Identification__

Each Edge Agent runs a recursive least squares (RLS) estimator with exponential forgetting to track the IDZ parameters online. The IDZ transfer function (Eq. 1) is discretized at sampling time $\Delta t = 5$ s using the zero-order hold method and converted to a discrete-time ARX (AutoRegressive with eXogenous input) model:

$$
y(k) = a_1 y(k-1) + a_2 y(k-2) + b_1 u(k-d) + b_2 u(k-d-1) + e(k) \tag{3}
$$

where $y(k)$ is the water level deviation from setpoint, $u(k)$ is the valve opening deviation, $d = \lceil \tau_d / \Delta t \rceil$ is the discrete delay, and $e(k)$ is white noise. The IDZ parameters are recovered from the ARX coefficients:

$$
A_s = \frac{\Delta t}{1 - a_1 - a_2}, \quad \tau_m = -\frac{b_2}{b_1} \cdot \Delta t, \quad \tau_d = d \cdot \Delta t \tag{4}
$$

The RLS update equations are:

$$
\hat{\theta}(k) = \hat{\theta}(k-1) + \mathbf{K}(k) \left[ y(k) - \boldsymbol{\phi}(k)^T \hat{\theta}(k-1) \right] \tag{5}
$$

$$
\mathbf{K}(k) = \frac{\mathbf{P}(k-1) \boldsymbol{\phi}(k)}{\lambda + \boldsymbol{\phi}(k)^T \mathbf{P}(k-1) \boldsymbol{\phi}(k)} \tag{6}
$$

$$
\mathbf{P}(k) = \frac{1}{\lambda} \left[ \mathbf{P}(k-1) - \mathbf{K}(k) \boldsymbol{\phi}(k)^T \mathbf{P}(k-1) \right] \tag{7}
$$

where $\hat{\theta} = [a_1, a_2, b_1, b_2]^T$ is the parameter vector, $\boldsymbol{\phi}(k) = [y(k-1), y(k-2), u(k-d), u(k-d-1)]^T$ is the regression vector, $\mathbf{P}(k)$ is the covariance matrix, and $\lambda = 0.98$ is the forgetting factor. The choice $\lambda = 0.98$ provides a memory window of approximately $1/(1-\lambda) = 50$ samples (250 s), balancing tracking speed against noise sensitivity.

__4.3  Gain-Scheduled MPC__

The MPC controller matrices are updated when the re-identified IDZ parameters change by more than a significance threshold $\delta_{\text{sig}}$:

$$
\frac{|\hat{p}(k) - p_{\text{current}}|}{p_{\text{current}}} > \delta_{\text{sig}} \tag{8}
$$

where $\hat{p}(k)$ is the newly identified parameter value and $p_{\text{current}}$ is the value currently used in the MPC. The threshold $\delta_{\text{sig}} = 0.10$ (10% relative change) prevents excessive controller reconfiguration due to estimation noise while ensuring adaptation to genuine operating point changes.

When an update is triggered:

1. The continuous-time IDZ transfer function is reconstructed from the new parameters.
2. The transfer function is discretized at $\Delta t = 5$ s using zero-order hold.
3. The state-space matrices $(\mathbf{A}_d, \mathbf{B}_d, \mathbf{C}_d)$ are updated.
4. The MPC prediction matrices are recomputed.
5. The Kalman filter covariance is reset to $\mathbf{P}_0$ (initial covariance) to allow re-convergence.

The update computation requires 1.8 ms on the S7-1200 PLC, which is executed within a single scan cycle without disrupting the real-time control loop. A bumpless transfer mechanism ensures continuity: the MPC output at the switch instant is computed using both old and new models, and a weighted blend (exponential transition over 5 samples) prevents output discontinuities.

__4.4  Adaptive MAS Architecture__

The adaptive MAS extends the CHS MAS = HDC + ODD + Cognitive Intelligence formulation (Lei et al., 2025b) with the following agent-level capabilities:

__Edge Agent__ (one per pool/tank):
- Real-time MPC execution (Layer 1 control)
- Kalman filter state estimation
- Online IDZ re-identification (RLS)
- Gain-scheduled MPC update
- Local ODD monitoring ($\rho$ evaluation)

__Area Agent__ (one per 3–5 Edge Agents):
- Coordination cost function: minimizes inter-pool flow deviations
- Distributed MPC (DMPC) coordination via ADMM (Alternating Direction Method of Multipliers)
- Aggregated ODD monitoring: system-level $\mathcal{O}_{\text{system}}$ evaluation (Eq. 14 in Chen et al., 2026b)
- Adaptation coordinator: validates Edge Agent parameter updates for inter-agent consistency

__Cloud Agent__ (one per system):
- Reference trajectory generation (daily/weekly planning)
- Bayesian ODD expansion decisions
- Historical performance database

For the dual-tank platform (single Edge Agent, no Area/Cloud Agents), only the Edge Agent capabilities are active. For the five-pool canal flume (five Edge Agents + one Area Agent), the DMPC coordination layer is activated. For the 10-pool benchmark (10 Edge Agents + 2 Area Agents + 1 Cloud Agent), the full hierarchy operates.

__*[Figure 4 about here]*__

__4.5  Bayesian ODD Expansion Protocol__

Following the framework proposed in Chen et al. (2026b, §6.7), the adaptive MAS implements a Bayesian ODD expansion cycle. The ODD is initially specified with a conservative safety factor SF = 1.5, corresponding to water level bounds of [10, 40] cm for the dual-tank (physical limits: [5, 45] cm). After each HiL verification campaign ($N$ boundary scenarios, $k$ observed violations), the safety factor posterior is updated:

$$
p(\text{SF} | k, N) \propto \binom{N}{k} p_v(\text{SF})^k (1 - p_v(\text{SF}))^{N-k} \cdot p(\text{SF}) \tag{9}
$$

The expansion protocol operates in three phases:

1. **Baseline campaign** (16 boundary scenarios at current ODD): If $k = 0$, proceed to Phase 2.
2. **Exploratory campaign** (8 scenarios at candidate expanded ODD, SF$_{\text{new}}$ = SF − 0.1): If $k = 0$, proceed to Phase 3.
3. **Confirmation campaign** (16 scenarios at expanded ODD): If $k = 0$, adopt SF$_{\text{new}}$ and update ODD bounds.

Three consecutive successful campaigns (Phases 1–3) reduce the safety factor from 1.5 to 1.3, expanding the water level ODD from [10, 40] cm to [8.5, 41.5] cm (a 12% range increase). The SIL-1 constraint ($\text{PFD} < 10^{-1}$) is maintained throughout by Proposition 1 of Chen et al. (2026b).

__5  Experimental Design__

__5.1  Test Scenarios__

Three scenario sets are defined:

__Set A — Dual-Tank HiL (32 scenarios):__
- A1–A16: Nominal ODD scenarios (identical to Chen et al., 2026a, Table 4)
- A17–A32: ODD boundary scenarios (identical to Chen et al., 2026b, Table 6)

__Set B — Five-Pool Canal Flume HiL (20 scenarios):__
- B1–B10: Nominal scenarios covering upstream flow changes, downstream gate adjustments, multi-pool setpoint tracking, and coordinated ramp trajectories
- B11–B20: Boundary scenarios including single-gate failure, communication loss (one Edge Agent), extreme flow transients, and combined stressors

__Set C — Ten-Pool Numerical Benchmark (20 scenarios):__
- C1–C10: Nominal scenarios with full MAS hierarchy (Cloud + Area + Edge Agents)
- C11–C20: Boundary scenarios including cascading gate failures, Area Agent communication loss, and demand pattern shifts

Each scenario is executed for 1,200 s (dual-tank) or 3,600 s (five-pool, 10-pool) with appropriate warm-up periods.

__5.2  Performance Metrics__

The following metrics are reported for each scenario:

1. **RMSE**: Root mean square error of water level tracking [mm or cm]
2. **MAE**: Maximum absolute error [mm or cm]
3. **$t_s$**: Settling time to ±2% of setpoint change [s]
4. **$N_v$**: Number of constraint violations [count]
5. **$\rho_{\min}$**: Minimum ODD distance-to-boundary value [—]
6. **$t_{\text{detect}}$**: ODD violation detection latency [sampling intervals]
7. **$T_{\text{MPC}}$**: MPC solve time [ms]

Additionally, the adaptive MAS metrics are:
8. **$N_{\text{adapt}}$**: Number of gain-scheduled MPC updates triggered
9. **$\Delta p_{\max}$**: Maximum IDZ parameter change detected [%]
10. **$\Delta$RMSE**: RMSE improvement of adaptive vs. fixed-model MPC [%]

__5.3  Comparison Baselines__

Three baselines are compared:
- **Fixed-Arduino**: Arduino Mega 2560 with fixed-model MPC (Chen et al., 2026a baseline)
- **Fixed-PLC**: Siemens S7-1200 with fixed-model MPC (hardware upgrade only)
- **Adaptive-PLC**: Siemens S7-1200 with adaptive MAS (this paper)

__6  Results__

__6.1  Dual-Tank PLC-Based HiL: Nominal Scenarios (A1–A16)__

__*Table 4. Dual-Tank HiL Results: Nominal Scenarios (Mean ± Std across 16 scenarios)*__

| Metric | Fixed-Arduino | Fixed-PLC | Adaptive-PLC |
|--------|---------------|-----------|--------------|
| RMSE [mm] | 2.0 ± 0.6 | 1.8 ± 0.5 | 1.6 ± 0.4 |
| MAE [mm] | 5.8 ± 1.4 | 4.9 ± 1.1 | 4.2 ± 0.9 |
| $t_s$ [s] | 48 ± 12 | 42 ± 10 | 38 ± 8 |
| $N_v$ | 0 | 0 | 0 |
| $T_{\text{MPC}}$ [ms] | 320 ± 18 | 4.2 ± 0.3 | 5.1 ± 0.4 |

The PLC upgrade alone (Fixed-PLC vs. Fixed-Arduino) reduces RMSE by 10% (from 2.0 to 1.8 mm) due to three factors: (1) hardware FPU eliminates floating-point rounding errors in the QP solver, (2) deterministic cycle timing (100 ms jitter-free vs. 320 ms with ±18 ms jitter on Arduino) reduces timing-induced control errors, and (3) 14-bit A/D resolution (vs. 10-bit on Arduino) improves water level measurement precision.

The adaptive MAS (Adaptive-PLC) provides an additional 11% RMSE reduction (from 1.8 to 1.6 mm) under nominal conditions. Although the nominal operating point is close to the identification point, the RLS estimator tracks small parameter variations caused by temperature-dependent valve friction and pump characteristic drift over the 600-s test duration. The mean number of MPC updates triggered per scenario is $N_{\text{adapt}} = 1.2$, indicating that adaptation is infrequent but non-trivial even under nominal conditions.

__6.2  Dual-Tank: Off-Nominal and Boundary Scenarios (A17–A32)__

The adaptive MAS advantage becomes pronounced under off-nominal conditions:

__*Table 5. Dual-Tank HiL Results: Boundary Scenarios (Mean ± Std across 16 scenarios)*__

| Metric | Fixed-PLC | Adaptive-PLC | Improvement |
|--------|-----------|--------------|-------------|
| RMSE [mm] | 3.6 ± 1.1 | 2.4 ± 0.7 | 34% |
| MAE [mm] | 9.2 ± 2.8 | 6.1 ± 1.5 | 34% |
| $t_s$ [s] | 72 ± 18 | 52 ± 12 | 28% |
| Worst RMSE [mm] | 5.8 | 3.8 | 34% |
| $N_v$ | 0 | 0 | — |
| $\rho_{\min}$ | 0.04 | 0.08 | +100% |
| ODD violations detected | 16/16 | 16/16 | — |
| $t_{\text{detect}}$ [intervals] | 1.6 ± 0.5 | 1.2 ± 0.3 | 25% |
| $N_{\text{adapt}}$ | — | 4.8 ± 1.6 | — |

The 34% RMSE improvement under boundary conditions is the primary result of this paper. The fixed-model MPC degrades significantly at the ODD boundaries (RMSE 3.6 mm, nearly double the nominal 1.8 mm) because the IDZ parameters at extreme operating points differ substantially from the nominal identification (Table 3). The adaptive MAS re-identifies the IDZ parameters within 5–8 samples (25–40 s) of entering a new operating region and updates the MPC accordingly, maintaining near-nominal performance.

The minimum ODD distance-to-boundary $\rho_{\min}$ is notably higher for the adaptive MAS (0.08 vs. 0.04), indicating that the adaptive controller keeps the system further from the ODD boundary—a direct consequence of better tracking performance at extreme operating points.

__6.3  Five-Pool Canal Flume HiL (B1–B20)__

__*Table 6. Five-Pool Canal Flume HiL Results*__

| Metric | Nominal (B1–B10) | Boundary (B11–B20) |
|--------|-------------------|---------------------|
| RMSE [cm] (Fixed-PLC) | 0.8 ± 0.2 | 1.8 ± 0.5 |
| RMSE [cm] (Adaptive-PLC) | 0.6 ± 0.2 | 1.1 ± 0.3 |
| Improvement | 25% | 39% |
| $t_s$ [s] (Fixed) | 85 ± 20 | 145 ± 35 |
| $t_s$ [s] (Adaptive) | 68 ± 15 | 95 ± 22 |
| $N_v$ (Fixed / Adaptive) | 0 / 0 | 0 / 0 |
| Coordination cost $J_{\text{coord}}$ (Fixed) | 0.12 ± 0.04 | 0.38 ± 0.12 |
| Coordination cost $J_{\text{coord}}$ (Adaptive) | 0.08 ± 0.03 | 0.18 ± 0.06 |
| DMPC iterations to convergence | 3.2 ± 0.8 | 4.8 ± 1.2 |
| Area Agent ODD detections | — | 10/10 |

The five-pool results confirm three findings. First, the adaptive MAS advantage scales to multi-pool systems: the 39% RMSE improvement under boundary conditions exceeds the 34% on the dual-tank, because inter-pool coupling amplifies the effect of model mismatch. When one pool's IDZ parameters change (e.g., due to gate recalibration), the neighboring pools are affected through flow coupling; the fixed-model MPC does not account for this, while the adaptive MAS re-identifies all five pools' parameters simultaneously.

Second, the coordination cost $J_{\text{coord}}$ (sum of squared inter-pool flow deviations from the planned trajectory) is reduced by 53% under boundary conditions. This metric captures the quality of the DMPC coordination: lower coordination cost means that the pool-to-pool flow transitions are smoother, reducing water level oscillations propagating downstream.

Third, the Area Agent ODD monitoring correctly detects all 10 boundary scenarios designed to probe system-level constraints (e.g., total system inflow exceeding pump capacity, cascading gate response delays). The system-level ODD composition (Eq. 14 in Chen et al., 2026b) correctly identifies violations that would not be detected by individual Edge Agent ODD monitors alone.

__6.4  Ten-Pool Numerical Benchmark (C1–C20)__

__*Table 7. Ten-Pool Numerical Benchmark Results*__

| Metric | Nominal (C1–C10) | Boundary (C11–C20) |
|--------|-------------------|---------------------|
| RMSE [cm] (Fixed) | 1.2 ± 0.3 | 3.5 ± 0.9 |
| RMSE [cm] (Adaptive) | 0.9 ± 0.2 | 1.8 ± 0.5 |
| Improvement | 25% | 49% |
| Full MAS solve time [ms] | 18 ± 3 | 22 ± 5 |
| Cloud Agent replanning triggered | 0.2 per scenario | 1.8 per scenario |
| DMPC iterations | 4.5 ± 1.0 | 7.2 ± 1.5 |
| System ODD detections | — | 10/10 |

The 10-pool benchmark demonstrates two additional findings. First, the adaptive advantage grows with system complexity: 49% improvement under boundary conditions (vs. 34% for dual-tank and 39% for five-pool). This is because larger systems have more operating points where the fixed IDZ model is inaccurate, and inter-pool coupling creates cascading model mismatch effects. Second, the full MAS hierarchy (Cloud + Area + Edge) is exercised: the Cloud Agent triggers reference trajectory replanning in 1.8 of the 10 boundary scenarios (e.g., when demand patterns shift beyond the planned envelope), demonstrating the three-tier coordination.

The computational cost remains tractable: the full MAS solve time (all 10 Edge Agents + 2 Area Agents + 1 Cloud Agent) is 22 ms worst case, well within the 5-s sampling interval. The limiting factor is the DMPC convergence (7.2 iterations under boundary conditions); for systems beyond ~50 pools, parallel ADMM decomposition (Huang et al., 2026) would be necessary.

__6.5  Bayesian ODD Expansion__

Three ODD expansion campaigns were executed on the dual-tank PLC-based HiL:

__*Table 8. ODD Expansion Campaign Results*__

| Campaign | SF | ODD [$h_{\min}$, $h_{\max}$] | Scenarios | Violations | Result |
|----------|-----|------------------------------|-----------|------------|--------|
| Baseline | 1.50 | [10.0, 40.0] cm | 16 boundary | 0 | Pass |
| Exploratory | 1.40 | [9.3, 40.7] cm | 8 boundary | 0 | Pass |
| Confirmation | 1.30 | [8.5, 41.5] cm | 16 boundary | 0 | Pass → Adopt |

After three successful campaigns with zero violations ($k = 0$, $N = 40$ total boundary scenarios), the safety factor is reduced from 1.50 to 1.30, expanding the verified ODD water level range from [10.0, 40.0] cm to [8.5, 41.5] cm—a 12% range increase. The posterior 95% credible interval for SF contracts from [1.1, 1.9] (prior) to [1.15, 1.55] (posterior), confirming that the expanded ODD maintains the SIL-1 safety constraint.

The expanded ODD is validated by running all 32 scenarios (16 nominal + 16 boundary) at the new ODD bounds. Results: RMSE 1.7 ± 0.5 mm (nominal), 2.6 ± 0.8 mm (boundary), with zero constraint violations—confirming that the adaptive MAS maintains safe performance within the expanded envelope.

__6.6  Cross-Layer Fidelity Summary__

__*Table 9. Cross-Layer RMSE Comparison (Dual-Tank, Mean across 16 nominal scenarios)*__

| Stage | Controller | RMSE [mm] | Degradation from MiL |
|-------|-----------|-----------|----------------------|
| MiL | Simulink MPC | 1.5 | — |
| SiL | Auto-generated C code | 1.6 | +0.1 |
| HiL (Arduino) | C code on Arduino | 2.0 | +0.5 |
| HiL (PLC, fixed) | ST code on S7-1200 | 1.8 | +0.3 |
| HiL (PLC, adaptive) | Adaptive ST on S7-1200 | 1.6 | +0.1 |

The adaptive PLC-based HiL achieves the same RMSE as SiL (1.6 mm), effectively eliminating the MiL-to-HiL degradation gap. This is a significant result: it demonstrates that the combination of industrial-grade hardware (PLC with hardware FPU, deterministic timing, high-resolution A/D) and adaptive control (online re-identification compensating for physical-plant discrepancies) can close the "sim-to-real" gap that is a persistent challenge in control system deployment.

__7  Discussion__

__7.1  Completing the xIL Chain__

This paper completes the xIL verification chain for the CHS framework through the HiL stage with industrial-grade hardware. The progression CKG-1 (MiL + SiL + Arduino HiL) → CKG-2 (SiL with formal ODD) → CKG-3 (PLC HiL + adaptive MAS) demonstrates a systematic engineering methodology for transitioning water system controllers from design to deployment.

The remaining xIL stage—Pilot-in-the-Loop (PiL)—requires integration with a human operator interface and evaluation of human-automation interaction. PiL is the subject of ongoing work and is a prerequisite for WSAL-3 certification in field deployments, where a human operator must be able to monitor, override, and take over from the autonomous controller.

__7.2  Adaptive MAS as Cognitive Intelligence__

The adaptive MAS framework developed in this paper implements the "Cognitive Intelligence" component of the CHS MAS formulation (MAS = HDC + ODD + CI). The online IDZ re-identification and gain-scheduled MPC constitute a form of system self-awareness: the controller knows its own model accuracy and adapts when the model degrades. The Bayesian ODD expansion constitutes a form of self-certification: the system expands its verified operating envelope based on accumulated evidence, analogous to how autonomous vehicles expand their ODD through accumulated driving data.

This is distinct from data-driven or learning-based control (e.g., reinforcement learning), where the controller learns a policy directly from data without maintaining an explicit plant model. The adaptive MAS maintains the model-based architecture of CHS—the IDZ transfer function remains the authoritative plant model—but adapts its parameters online. This preserves the interpretability, traceability, and certifiability of the MBD framework while providing adaptation capability.

__7.3  Scalability Analysis__

The three-platform comparison reveals a consistent pattern: the adaptive MAS advantage increases with system complexity (34% → 39% → 49% RMSE improvement under boundary conditions). This scaling behavior is explained by two mechanisms:

1. **Model mismatch amplification**: In multi-pool systems, model mismatch in one pool affects neighboring pools through flow coupling. The fixed-model MPC compounds this effect because it cannot account for the changed downstream dynamics. The adaptive MAS re-identifies each pool independently, preventing mismatch propagation.

2. **Coordination improvement**: The DMPC coordination (Area Agent level) benefits from accurate local models. When Edge Agents provide accurate predictions to the Area Agent, the ADMM coordination converges faster (3.2 vs. 4.8 iterations under nominal conditions for adaptive vs. fixed) and produces better coordination trajectories.

The computational scaling is linear in the number of pools for Edge Agent operations (RLS + MPC per pool) and approximately quadratic for Area Agent coordination (DMPC with inter-pool coupling). For systems beyond ~100 pools, hierarchical decomposition (multiple Area Agents with limited inter-Area coordination) maintains tractability.

__7.4  Industrial Deployment Pathway__

The PLC-based HiL demonstrated in this paper represents the penultimate step before field deployment. The remaining steps are:

1. **Environmental qualification**: The S7-1200 has an operating temperature range of −20°C to +60°C and IP20 protection; field installation requires IP65/IP67 enclosures and lightning protection.

2. **Cybersecurity hardening**: OPC-UA with TLS 1.2 provides transport security; IEC 62443 zone-and-conduit segmentation must be implemented for the field network.

3. **Redundancy**: The single-PLC architecture must be extended with hot-standby redundancy (S7-1500H or equivalent) for safety-critical applications.

4. **PiL validation**: Human operator interface design, alarm management, and human-automation handover protocols must be validated through PiL testing.

5. **Regulatory approval**: The safety case document, incorporating the ODD specification, xIL verification evidence, and IEC 61511 compliance, must be reviewed by the responsible authority.

__7.5  Limitations__

Several limitations should be acknowledged. First, the five-pool canal flume is a laboratory facility; field-scale canals exhibit additional complexities (sediment transport, weed growth, gate leakage) not represented. Second, the online IDZ re-identification assumes persistent excitation—the system must experience sufficient input variation to identify the parameters. During steady-state operation (constant setpoint, constant flow), the RLS estimates may drift; this is mitigated by the significance threshold $\delta_{\text{sig}}$ but not eliminated. Third, the Bayesian ODD expansion has been demonstrated with only three campaigns (40 scenarios total); long-term safety assurance requires hundreds of operating hours, which is planned for the field deployment phase. Fourth, the adaptive MAS has been tested with up to 10 pools; the scaling to 50–500 pool systems (typical of large irrigation districts) requires further investigation with the GPU-parallel solver (Huang et al., 2026). Fifth, the PiL stage has not been demonstrated; the human-automation interaction design for water systems is an open research area with limited prior work.

__8  Conclusions__

This paper has completed the xIL verification chain for the CHS framework through industrial-grade Hardware-in-the-Loop (HiL) verification with an adaptive Multi-Agent System (MAS) on multiple platforms. The key findings are:

1. The PLC-based HiL architecture (Siemens S7-1200, IEC 61131-3 Structured Text, OPC-UA communication) reduces the MPC solve time from 320 ms (Arduino) to 4.2 ms while improving nominal RMSE from 2.0 mm to 1.8 mm. The deterministic timing and hardware FPU of the industrial PLC effectively halve the MiL-to-HiL degradation gap compared to the Arduino baseline.

2. The adaptive MAS framework—incorporating online IDZ re-identification via RLS, gain-scheduled MPC, and Bayesian ODD expansion—reduces worst-case RMSE by 34% (dual-tank), 39% (five-pool), and 49% (10-pool) compared to fixed-model MPC under off-nominal and boundary conditions. The adaptive PLC-based HiL achieves the same RMSE as SiL (1.6 mm), effectively closing the sim-to-real gap.

3. The Bayesian ODD expansion protocol safely expands the verified operating envelope by 12% (safety factor 1.50 → 1.30) after three successive verification campaigns with zero boundary violations, maintaining the SIL-1 safety constraint throughout.

4. The multi-platform comparison (2-state, 5-state, 10-state) demonstrates that the adaptive MAS advantage scales with system complexity, with the improvement under boundary conditions increasing from 34% to 49% as inter-pool coupling amplifies model mismatch effects.

These results establish the practical engineering pathway for the WSAL-2→3 transition: MBD framework (CKG-1) → formal ODD (CKG-2) → industrial HiL with adaptive MAS (CKG-3) → field deployment (future work). The adaptive MAS provides the robustness required for autonomous operation across the full ODD envelope while maintaining the interpretability and certifiability of the model-based CHS architecture.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]) and the National Natural Science Foundation of China (Grant Nos. [to be inserted]). The authors thank the CHS laboratory team at Hebei University of Engineering for constructing the five-pool canal flume and instrumenting both experimental platforms.

__References__

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Clemmens, A. J., Kacerek, T. F., Grawitz, B., & Schuurmans, W. (2005). Test cases for canal control algorithms. Journal of Irrigation and Drainage Engineering, 131(6), 502–514. https://doi.org/10.1061/(ASCE)0733-9437(2005)131:6(502)

Huang, Z., Lei, X., Liu, X., Ji, C., & Wang, H. (2026). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

IEC. (2016). IEC 61511: Functional safety — Safety instrumented systems for the process industry sector. International Electrotechnical Commission.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). Modeling and control of hydrosystems. Springer. https://doi.org/10.1007/978-1-84882-624-3

Liu, X., Lei, X., Long, Y., & Wang, H. (2026). Design for Operation: A model-based framework for establishing cybernetics of hydro systems as an interdisciplinary discipline. Environmental Modelling & Software (submitted).

Ljung, L. (1999). System identification: Theory for the user (2nd ed.). Prentice Hall.

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Savic, D. (2022). Digital water developments and lessons learned from automation in the car and aircraft industries. Engineering, 9(2), 35–41.

van Overloop, P. J. (2006). Model predictive control on open water systems (Doctoral dissertation). Delft University of Technology.

van Overloop, P. J., Clemmens, A. J., Strand, R. J., Wagemaker, R. M., & Bautista, E. (2010). Real-time implementation of model predictive control on Maricopa-Stanfield Irrigation and Drainage District's WM Canal. Journal of Irrigation and Drainage Engineering, 136(11), 747–756. https://doi.org/10.1061/(ASCE)IR.1943-4774.0000256

Xu, M., Negenborn, R. R., van Overloop, P. J., & van de Giesen, N. C. (2012). De Saint-Venant equations-based model assessment in model predictive control of open channel flow. Advances in Water Resources, 49, 37–45. https://doi.org/10.1016/j.advwatres.2012.07.004

Ye, S., Lei, X., Zhang, L., Ji, C., & Wang, H. (2026). Shaoping hydropower station SiL verification with ODD-aware MAS. Journal of Hydrology (submitted).

__Data Availability__

The PLC Structured Text code (auto-generated), OPC-UA configuration, adaptive MAS function blocks, RLS estimator implementation, five-pool canal flume sensor data, and all scenario logs for the dual-tank and five-pool HiL experiments are available at https://github.com/IWHR-CHS/adaptive-hil (to be made public upon acceptance; reviewer access available upon request). The 10-pool benchmark model and scenario files are included in the companion repository https://github.com/IWHR-CHS/dual-tank-odd.

__Figure Captions__

__Figure 1.__ xIL verification chain completed by the CKG series. CKG-1 demonstrated MiL → SiL → HiL (Arduino); CKG-2 formalized ODD and extended SiL; CKG-3 (this paper) demonstrates industrial PLC-based HiL with adaptive MAS across three platforms. The remaining stage (PiL) is future work.

__Figure 2.__ Experimental platforms. (a) Dual-tank laboratory platform with Siemens S7-1200 PLC replacing the Arduino Mega 2560. (b) Five-pool canal flume at Hebei University of Engineering: 12-m recirculating flume with four motorized sluice gates, capacitive level sensors, and electromagnetic flow meters. (c) Schematic of the 10-pool numerical benchmark.

__Figure 3.__ PLC-based HiL architecture. The Siemens S7-1200 PLC hosts the MPC controller (auto-generated Structured Text), Kalman filter, ODD monitor, and RLS estimator as function blocks within a 100-ms cyclic task. Communication with the SCADA workstation uses OPC-UA over Ethernet. Sensor inputs and actuator outputs use 4–20 mA analog I/O.

__Figure 4.__ Adaptive MAS architecture. (a) Edge Agent internal structure: sensor input → Kalman filter → RLS estimator → gain-scheduled MPC → actuator output, with local ODD monitor. (b) Three-tier hierarchy for the five-pool system: five Edge Agents coordinated by one Area Agent via DMPC/ADMM. (c) Timing diagram showing an adaptive event: operating point change detected → RLS convergence (5–8 samples) → parameter significance test → MPC update → bumpless transfer.

__Figure 5.__ Performance comparison across three platforms. (a) Box plots of RMSE for Fixed-PLC vs. Adaptive-PLC under nominal and boundary conditions for dual-tank, five-pool, and 10-pool systems. (b) Adaptive advantage (% RMSE improvement) as a function of system complexity (number of states), showing the increasing benefit of adaptation for larger systems.
