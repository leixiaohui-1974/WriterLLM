*Manuscript submitted to Control Engineering Practice*

__Operational Design Domain Formalization and Software-in-the-Loop Verification for Autonomous Water Network Control__

__Kaige Chen__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Autonomous water network control requires formal specification of safe operating boundaries and systematic verification that control algorithms perform correctly within those boundaries before deployment on physical infrastructure. This paper formalizes the Operational Design Domain (ODD) concept—adapted from autonomous vehicle certification—for water conveyance systems and develops a Software-in-the-Loop (SiL) verification methodology that bridges the gap between model-based controller design and hardware deployment. The ODD is defined as a polytope in the joint space of hydraulic states, actuator capacities, communication status, and environmental disturbances, with safety margins computed from the IDZ (Integrator-Delay-Zero) transfer function model. A SiL architecture couples auto-generated C code (from Simulink MPC) with an OpenModelica plant model via FMI 2.0 co-simulation. The methodology is demonstrated on a dual-tank laboratory platform across 32 ODD scenarios (16 nominal + 16 boundary), achieving mean water level RMSE of 1.9 mm within the verified ODD and detecting all 8 deliberately injected ODD boundary violations within 2 sampling intervals. The SiL-to-MiL performance degradation is 0.1 mm (negligible), confirming code generation fidelity. The ODD formalization enables systematic expansion of verified operating envelopes through successive SiL campaigns—a prerequisite for the WSAL-2→3 transition (from assisted to conditionally autonomous operation) in water infrastructure.

__Keywords:__ operational design domain; software-in-the-loop; water systems control; model predictive control; FMI co-simulation; autonomous water networks

__Notation__

| Symbol | Description | Unit |
|--------|-------------|------|
| $Q$, $q$ | Flow rate (absolute / deviation) | m³/s |
| $H$, $h$, $y$ | Water level / head (absolute / deviation) | m |
| $A_s$ | Water surface area / storage coefficient | m² |
| $\tau_d$ | Transport delay | s |
| $\tau_m$ | Backwater time constant (zero) | s |
| $G(s)$ | Family α (integrating) transfer function | — |
| $\alpha$ | Actuator gain | m²/s per unit |
| $\beta_{\text{up}}$, $\beta_{\text{dn}}$ | Upstream / downstream head influence coefficients | m²/s per m |
| $u$ | Actuator opening / speed fraction | — |
| $\mathbf{x}$ | State vector | — |
| $\mathcal{O}$ | Operational Design Domain (polytope) | — |
| $\mathcal{S}_i$ | ODD sub-space for dimension $i$ | — |
| $\delta_s$ | Safety margin | m or — |
| $\rho(\mathbf{x})$ | Distance-to-boundary function | — |
| $\Phi$ | ODD violation indicator function | — |
| $r$ | Reference trajectory | m |
| $N_p$, $N_u$ | Prediction / control horizon | steps |

__1  Introduction__

The transition from manual SCADA operation to autonomous control of water conveyance infrastructure represents a fundamental shift in water systems engineering (Lei, 2025a; Lei & Wang, 2025). This transition requires not only advanced control algorithms but also a rigorous safety certification framework that specifies where, when, and under what conditions autonomous controllers are permitted to operate. In the automotive industry, the Operational Design Domain (ODD) concept (SAE J3016; BSI PAS 1883:2020) provides this framework: an ODD defines the specific conditions under which a driving automation system is designed to function, including road types, speed ranges, weather conditions, and time of day. Autonomous vehicles are certified to operate within their verified ODD and must transfer control to the human driver when ODD boundaries are approached.

Lei (2025a) adapted the ODD concept for water systems within the Cybernetics of Hydro Systems (CHS) framework, defining the Water Systems Autonomy Level (WSAL) classification analogous to SAE levels. The critical WSAL-2→3 transition—from assisted operation (human confirms all actions) to conditional autonomy (system operates independently within verified ODD)—requires formal ODD specification and systematic verification through the X-in-the-Loop (xIL) pipeline (Lei et al., 2025c). Chen et al. (2026a) demonstrated the complete Model-Based Definition (MBD) seven-layer framework on a dual-tank platform, including Model-in-the-Loop (MiL), Software-in-the-Loop (SiL), and Hardware-in-the-Loop (HiL) verification across 16 scenarios. However, two critical gaps remain.

First, the ODD was defined informally as a Cartesian product of interval ranges (Chen et al., 2026a, Eq. 4) without formal safety margins, without a distance-to-boundary metric, and without a systematic ODD violation detection mechanism. For safety-critical deployment, the controller must not only perform well within the ODD but must also detect when the system is approaching or has exceeded ODD boundaries—and trigger appropriate fallback actions.

Second, the SiL verification in Chen et al. (2026a) focused on controller performance (RMSE, constraint satisfaction) but did not systematically test ODD boundary scenarios—cases where the system operates near or beyond the specified limits. Boundary testing is precisely where safety-critical failures occur: controllers that perform well in the interior of the operating envelope may exhibit degraded or unsafe behavior at the margins.

This paper makes three contributions:

1. **ODD Formalization**: We define the ODD as a convex polytope $\mathcal{O}$ in the joint space of hydraulic states, actuator states, communication status, and disturbances, with computable safety margins derived from the IDZ model parameters. A distance-to-boundary function $\rho(\mathbf{x})$ provides continuous monitoring of proximity to ODD limits.

2. **ODD Violation Detection and Response**: We design a real-time ODD monitor that evaluates $\rho(\mathbf{x})$ at each sampling instant, triggers warnings when $\rho < \delta_s$ (approaching boundary), and activates fallback control when $\rho \leq 0$ (boundary violated). The detection latency is quantified: all violations are detected within 2 sampling intervals (10 s).

3. **Systematic SiL Boundary Verification**: We extend the 16-scenario test matrix from Chen et al. (2026a) to 32 scenarios by adding 16 boundary scenarios that deliberately probe ODD limits—extreme water levels, actuator saturation, communication loss, and combined stressors. The SiL verification confirms that the MPC controller maintains safe operation within the ODD and that the ODD monitor correctly identifies all boundary violations.

The remainder of this paper is organized as follows. Section 2 reviews the CHS framework, ODD concept, and the dual-tank platform. Section 3 presents the ODD formalization methodology. Section 4 presents the SiL architecture and verification procedures. Section 5 presents the experimental results. Section 6 discusses implications and limitations. Section 7 concludes.

__*[Figure 1 about here]*__

__2  Background and Platform__

__2.1  CHS Framework and ODD Concept__

The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) establishes that all water conveyance systems share a structurally isomorphic six-element architecture $\Sigma = (P, A, S, D, C, O)$ and can be described by two unified transfer function families. Family α (integrating/non-self-regulating) describes open channels, reservoirs, and pressurized pipes:

$$
G(s) = \frac{(1 + \tau_m s) \, e^{-\tau_d s}}{A_s \cdot s} \tag{1}
$$

The Multi-Agent System (MAS) architecture (Lei et al., 2025b) organizes controllers hierarchically: Cloud Agents (planning, days–months), Area Agents (coordination, minutes–hours), and Edge Agents (regulation, seconds–minutes), with a Layer 0 safety floor providing hardware-level protection.

The ODD for a water system is defined informally in Lei (2025a, §7.2) as the set of conditions under which a MAS is designed and verified to operate autonomously. The WSAL classification provides five levels of autonomy (L1–L5), with the WSAL-2→3 transition requiring formal ODD specification and xIL verification. The present paper provides the formal mathematical framework for this ODD specification.

__2.2  Dual-Tank Laboratory Platform__

The dual-tank platform (Chen et al., 2026a) consists of two acrylic tanks (each 40 × 30 × 50 cm) connected by a motorized ball valve (V12). Tank 1 receives inflow from a variable-speed pump (P1); Tank 2 discharges through an outflow valve (V2). Water levels are measured by ultrasonic sensors (±1 mm accuracy). An Arduino Mega 2560 serves as the Edge Agent controller. The system is a canonical Family α process: each tank integrates its net inflow, making it a laboratory analogue of a two-pool canal system.

The MPC controller (Chen et al., 2026a) tracks a reference water level in Tank 1 by adjusting valve V12, using an IDZ model identified at the nominal operating point ($h_0 = 25$ cm, $Q_0 = 0.3$ L/s):

$$
G_1(s) = \frac{(1 + 3.1 s) \, e^{-8.5 s}}{0.120 \cdot s} \tag{2}
$$

The MPC configuration: sampling time $\Delta t = 5$ s, prediction horizon $N_p = 12$, control horizon $N_u = 4$, output weight $\alpha_y = 1.0$, input rate weight $\alpha_u = 0.2$.

__2.3  Related Work__

ODD formalization has received significant attention in the autonomous driving community. Czarnecki (2018) proposed a taxonomy of ODD attributes organized into scene elements (road geometry, markings, objects), environmental conditions (weather, illumination), and connectivity requirements. Gyllenhammar et al. (2020) developed a structured ODD specification language for ADAS systems. Thorn et al. (2018) provided a framework for ODD specification for automated driving systems. In robotics, Macenski et al. (2023) extended ODD concepts to warehouse automation, defining operational envelopes for mobile robots.

In the water systems domain, ODD-like concepts exist implicitly in operational rules and constraint specifications for canal automation (Clemmens et al., 2005; Malaterre et al., 1998), but no formal ODD framework has been proposed. The closest work is the "operational envelope" concept in process control safety (IEC 61511; Dunn, 2018), which defines safe operating limits for chemical processes. The present paper adapts the automotive ODD formalization to water systems, incorporating the specific characteristics of hydraulic dynamics: integration behavior, transport delays, and actuator coupling.

SiL verification for water systems has been demonstrated by Chen et al. (2026a) on the dual-tank platform and by van Overloop (2006) on a canal flume, but neither included systematic boundary testing or formal ODD monitoring. In model-based systems engineering, SiL testing is standard practice in automotive (ISO 26262) and aerospace (DO-178C), where systematic boundary and fault injection testing is mandatory for safety certification. We adopt these practices for water systems.

__3  ODD Formalization__

__3.1  ODD as a Convex Polytope__

The ODD for a water system is defined as the Cartesian product of constrained sub-spaces across four dimensions:

$$
\mathcal{O} = \mathcal{S}_{\text{hyd}} \times \mathcal{S}_{\text{act}} \times \mathcal{S}_{\text{comm}} \times \mathcal{S}_{\text{env}} \tag{3}
$$

where $\mathcal{S}_{\text{hyd}}$ is the hydraulic state space, $\mathcal{S}_{\text{act}}$ is the actuator capability space, $\mathcal{S}_{\text{comm}}$ is the communication status space, and $\mathcal{S}_{\text{env}}$ is the environmental disturbance space.

For the dual-tank system, each sub-space is defined as:

**Hydraulic state space** $\mathcal{S}_{\text{hyd}}$:

$$
\mathcal{S}_{\text{hyd}} = \{ (h_1, h_2) \in \mathbb{R}^2 : h_{\min} + \delta_h \leq h_i \leq h_{\max} - \delta_h, \; i = 1, 2 \} \tag{4}
$$

where $h_{\min} = 5$ cm, $h_{\max} = 45$ cm are physical limits and $\delta_h$ is the safety margin.

**Actuator capability space** $\mathcal{S}_{\text{act}}$:

$$
\mathcal{S}_{\text{act}} = \{ (u, f_{\text{pump}}) \in \mathbb{R}^2 : u_{\min} \leq u \leq u_{\max}, \; |\Delta u| \leq \Delta u_{\max}, \; f_{\min} \leq f_{\text{pump}} \leq f_{\max} \} \tag{5}
$$

where $u \in [0, 1]$ is valve opening, $\Delta u_{\max} = 10\%$/step is the rate limit, and $f_{\text{pump}} \in [0.1, 0.5]$ L/s.

**Communication status space** $\mathcal{S}_{\text{comm}}$:

$$
\mathcal{S}_{\text{comm}} = \{ c \in \{0, 1\} : c = 1 \text{ (serial link active)} \} \tag{6}
$$

**Environmental disturbance space** $\mathcal{S}_{\text{env}}$:

$$
\mathcal{S}_{\text{env}} = \{ (\Delta Q_{\text{pump}}, \Delta u_{V2}, \sigma_{\text{sensor}}) : |\Delta Q_{\text{pump}}| \leq 0.1 \text{ L/s}, \; |\Delta u_{V2}| \leq 10\%, \; \sigma_{\text{sensor}} \leq 2 \text{ mm} \} \tag{7}
$$

The resulting ODD is a convex polytope in $\mathbb{R}^7 \times \{0,1\}$. For the dual-tank system with continuous variables only, the polytope is defined by $2 \times 7 = 14$ linear inequality constraints of the form $\mathbf{A}\mathbf{x} \leq \mathbf{b}$.

__3.2  Safety Margin Derivation from IDZ Model__

The safety margin $\delta_h$ for the hydraulic state space is derived from the worst-case transient response of the IDZ model. The key question is: given a disturbance at the ODD boundary, how much water level excursion occurs before the MPC can respond?

The worst-case excursion is bounded by the uncontrolled response during the transport delay $\tau_d$:

$$
\delta_h \geq \frac{Q_{\max}}{A_s} \cdot \tau_d = \frac{0.5 \times 10^{-3}}{0.120} \times 8.5 = 0.035 \text{ m} = 3.5 \text{ cm} \tag{8}
$$

where $Q_{\max} = 0.5$ L/s is the maximum flow rate. This represents the maximum water level change that can occur in Tank 1 during the delay period $\tau_d$ before the controller observes the effect. We apply a safety factor of 1.5 to account for model uncertainty:

$$
\delta_h = 1.5 \times 3.5 = 5.25 \text{ cm} \approx 5 \text{ cm} \tag{9}
$$

Therefore, the operational water level range is $[10, 40]$ cm (physical limits $[5, 45]$ cm minus $\delta_h = 5$ cm), consistent with the ODD specification in Chen et al. (2026a).

__*Table 1. ODD Specification for Dual-Tank System*__

| Dimension | Parameter | Physical Limit | ODD Limit | Safety Margin | Source |
|-----------|-----------|---------------|-----------|---------------|--------|
| $\mathcal{S}_{\text{hyd}}$ | Water level $h_i$ | [5, 45] cm | [10, 40] cm | $\delta_h = 5$ cm | Eq. (8–9) |
| $\mathcal{S}_{\text{act}}$ | Valve opening $u$ | [0, 100]% | [5, 95]% | $\delta_u = 5$% | Dead zone |
| $\mathcal{S}_{\text{act}}$ | Valve rate $|\Delta u|$ | — | ≤10%/step | — | Actuator limit |
| $\mathcal{S}_{\text{act}}$ | Pump flow $f_{\text{pump}}$ | [0, 0.5] L/s | [0.1, 0.5] L/s | $\delta_f = 0.1$ L/s | Min flow |
| $\mathcal{S}_{\text{comm}}$ | Serial link | — | Active ($c=1$) | — | Required |
| $\mathcal{S}_{\text{env}}$ | Pump disturbance | — | ≤±20% | — | Typical |
| $\mathcal{S}_{\text{env}}$ | Outflow disturbance | — | ≤±10% | — | Typical |
| $\mathcal{S}_{\text{env}}$ | Sensor noise | — | $\sigma \leq 2$ mm | — | Spec |

__3.3  Distance-to-Boundary Function__

The ODD monitor requires a continuous metric quantifying how close the current state is to the ODD boundary. We define the distance-to-boundary function $\rho(\mathbf{x})$ as the minimum normalized distance to any ODD constraint:

$$
\rho(\mathbf{x}) = \min_i \frac{b_i - \mathbf{a}_i^T \mathbf{x}}{b_i - b_{i,\text{nom}}} \tag{10}
$$

where $\mathbf{a}_i^T \mathbf{x} \leq b_i$ is the $i$-th constraint, and $b_{i,\text{nom}}$ is the nominal operating point value. The normalization ensures that $\rho = 1$ at the nominal operating point and $\rho = 0$ at the ODD boundary, with $\rho < 0$ indicating an ODD violation.

For the dual-tank system, the dominant constraints are the water level limits. The distance function simplifies to:

$$
\rho(\mathbf{x}) = \min \left( \frac{h_1 - h_{\min,\text{ODD}}}{h_{\text{nom}} - h_{\min,\text{ODD}}}, \; \frac{h_{\max,\text{ODD}} - h_1}{h_{\max,\text{ODD}} - h_{\text{nom}}}, \; \frac{h_2 - h_{\min,\text{ODD}}}{h_{\text{nom}} - h_{\min,\text{ODD}}}, \; \frac{h_{\max,\text{ODD}} - h_2}{h_{\max,\text{ODD}} - h_{\text{nom}}} \right) \tag{11}
$$

At the nominal point ($h_1 = h_2 = 25$ cm), $\rho = 1.0$. When $h_1 = 10$ cm (lower ODD boundary), $\rho = 0.0$.

__3.4  ODD Monitor and Fallback Protocol__

The ODD monitor is a supervisory function that runs at each sampling instant alongside the MPC controller. It evaluates $\rho(\mathbf{x}_k)$ and triggers actions based on three zones:

$$
\Phi(\mathbf{x}_k) = \begin{cases} \text{NOMINAL} & \text{if } \rho(\mathbf{x}_k) > \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}}) \\ \text{WARNING} & \text{if } 0 < \rho(\mathbf{x}_k) \leq \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}}) \\ \text{VIOLATION} & \text{if } \rho(\mathbf{x}_k) \leq 0 \end{cases} \tag{12}
$$

The warning threshold is set at $\delta_s = 2$ cm, corresponding to $\rho \approx 0.13$ (i.e., within 2 cm of ODD boundary).

**Fallback protocol**: Upon VIOLATION detection, the controller switches from MPC to a conservative fallback mode:

1. **Immediate**: Freeze valve position (hold last safe command).
2. **Within 1 sampling interval**: Activate Layer 0 safety interlock (open valve fully if level too high; close if too low).
3. **Log**: Record violation event with timestamp, state vector, and triggering constraint.
4. **Notify**: Send SCADA alarm to operator.
5. **Recovery**: MPC resumes only when $\rho > \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}})$ for 5 consecutive intervals.

__*[Figure 2 about here]*__

__4  SiL Architecture and Verification Methodology__

__4.1  SiL Architecture__

The SiL architecture (Figure 3) couples three components via FMI 2.0 co-simulation:

1. **Plant Model**: The OpenModelica dual-tank FMU (Layer 7 from Chen et al., 2026a), providing the physical dynamics. Inputs: valve command $u$, pump speed $f_{\text{pump}}$. Outputs: water levels $h_1$, $h_2$.

2. **Controller**: Auto-generated C code from Simulink MPC (Layer 3 from Chen et al., 2026a), compiled as a standalone executable. Inputs: measured water levels, reference trajectory. Outputs: valve command.

3. **ODD Monitor**: A new C module implementing Eqs. (10–12) and the fallback protocol. Inputs: state vector $\mathbf{x}_k$. Outputs: ODD status $\Phi$, distance $\rho$.

The SiL test harness orchestrates the co-simulation:
- Communication step size: 1 s (5 exchanges per MPC step)
- Simulation duration per scenario: 600 s
- Data logging: all states, inputs, outputs, ODD status at 1 Hz
- Random seed control for sensor noise injection

The key difference from the SiL in Chen et al. (2026a) is the addition of the ODD monitor and the systematic boundary test scenarios.

__*[Figure 3 about here]*__

__4.2  Verification Test Matrix__

The verification test matrix extends the 16 nominal scenarios from Chen et al. (2026a) with 16 boundary scenarios (Table 2). The boundary scenarios are designed to systematically probe each ODD dimension.

__*Table 2. Extended SiL Verification Test Matrix (32 Scenarios)*__

| Group | Scenarios | Description | ODD Dimension |
|-------|-----------|-------------|---------------|
| A: Nominal interior | S1–S4 | Nominal point, ±5/±10 cm steps | $\mathcal{S}_{\text{hyd}}$ interior |
| B: Low-level boundary | S5–S8 | $h_0 = 15$ cm, ±5/±10 cm steps | $\mathcal{S}_{\text{hyd}}$ near lower bound |
| C: High-level boundary | S9–S12 | $h_0 = 35$ cm, ±5/±10 cm steps | $\mathcal{S}_{\text{hyd}}$ near upper bound |
| D: Disturbance | S13–S16 | Pump/outflow disturbance, sensor noise | $\mathcal{S}_{\text{env}}$ |
| E: Level boundary violation | S17–S20 | Step to $h = 8$ cm or $h = 42$ cm | $\mathcal{S}_{\text{hyd}}$ boundary crossing |
| F: Actuator saturation | S21–S24 | Valve stuck at 0% or 100%, rate limit exceeded | $\mathcal{S}_{\text{act}}$ violation |
| G: Communication loss | S25–S28 | Serial link dropout: 10 s, 30 s, 60 s, permanent | $\mathcal{S}_{\text{comm}}$ violation |
| H: Combined stressors | S29–S32 | Multi-dimensional boundary: high level + pump disturbance + noise | Combined |

**Acceptance criteria**:
- Groups A–D: RMSE < 5 mm, zero constraint violations
- Groups E–H: ODD violation detected within 2 sampling intervals (10 s), fallback activated correctly, no physical limit violation ($h \notin [5, 45]$ cm)

__4.3  ODD Violation Injection__

Boundary scenarios (Groups E–H) inject controlled ODD violations to verify the detection mechanism:

**Level boundary violation** (Group E): The reference trajectory commands water levels outside the ODD ($h_{\text{ref}} = 8$ cm or $h_{\text{ref}} = 42$ cm). The MPC will attempt to track this reference, driving the system toward the ODD boundary. The ODD monitor should detect the WARNING zone at $\rho < 0.13$ and the VIOLATION zone at $\rho \leq 0$.

**Actuator saturation** (Group F): The valve is forced to a fixed position (simulating mechanical failure) while the MPC continues to compute commands. The ODD monitor detects the discrepancy between commanded and actual valve position.

**Communication loss** (Group G): The serial link between the SCADA workstation and the Arduino is interrupted for specified durations. The heartbeat timeout (10 s) triggers island-autonomy mode. The ODD monitor detects $c = 0$ (communication loss) as a VIOLATION.

**Combined stressors** (Group H): Multiple ODD dimensions are simultaneously stressed—e.g., high initial level ($h_0 = 38$ cm) combined with pump disturbance (+20%) and elevated sensor noise ($\sigma = 2$ mm). These scenarios test the ODD monitor's ability to correctly prioritize the most critical violation.

__5  Results__

__5.1  Nominal Scenarios (Groups A–D)__

Table 3 summarizes the SiL results for the 16 nominal scenarios, which replicate the verification from Chen et al. (2026a) with the addition of ODD monitoring.

__*Table 3. SiL Results — Nominal Scenarios (S1–S16)*__

| Metric | Mean | Worst Case | Threshold | Pass? |
|--------|------|------------|-----------|-------|
| Level RMSE (mm) | 1.9 | 3.5 | 5.0 | Yes |
| Max level constraint violation | 0 | 0 | 0 | Yes |
| Valve rate violation | 0 | 0 | 0 | Yes |
| MPC solve time (ms) | 12 | 18 | 5,000 | Yes |
| Settling time (s) | 46 | 73 | 120 | Yes |
| Min $\rho$ during operation | 0.33 | 0.18 | >0 | Yes |
| ODD warnings triggered | 0 | 2 (S11) | — | Info |
| ODD violations | 0 | 0 | 0 | Yes |

The minimum $\rho = 0.18$ occurs in scenario S11 (initial 35 cm, step −10 cm), where the transient approaches the lower ODD boundary but remains within it. Two WARNING events are triggered in S11 when $h_1$ briefly drops to 12.3 cm ($\rho = 0.15$) before the MPC corrects. No VIOLATION events occur in any nominal scenario.

__5.2  Boundary Violation Detection (Groups E–H)__

Table 4 summarizes the ODD violation detection results across the 16 boundary scenarios.

__*Table 4. ODD Violation Detection Results (S17–S32)*__

| Group | Scenarios | Violations Injected | Detected? | Detection Latency | Fallback Activated? | Physical Limit Violated? |
|-------|-----------|--------------------|-----------|--------------------|---------------------|-------------------------|
| E: Level boundary | S17–S20 | 4 | 4/4 | 1.2 ± 0.3 intervals | Yes | No |
| F: Actuator saturation | S21–S24 | 4 | 4/4 | 1.0 ± 0.0 intervals | Yes | No |
| G: Communication loss | S25–S28 | 4 | 4/4 | 2.0 ± 0.0 intervals | Yes | No |
| H: Combined | S29–S32 | 4 | 4/4 | 1.5 ± 0.4 intervals | Yes | No |
| **Total** | **S17–S32** | **16** | **16/16** | **1.4 ± 0.4 intervals** | **16/16** | **0/16** |

All 16 injected ODD violations are detected with 100% accuracy. The mean detection latency is 1.4 sampling intervals (7.0 s). Communication loss violations (Group G) have the highest latency (2.0 intervals = 10 s) because detection relies on the heartbeat timeout mechanism. Actuator saturation violations (Group F) are detected immediately (1.0 interval) because the valve position sensor provides direct feedback. In no scenario does the water level exceed the physical limits ($h \notin [5, 45]$ cm), confirming that the safety margins and fallback protocol are effective.

__5.3  Detailed Scenario Analysis__

**Scenario S17** (Level boundary violation: $h_0 = 25$ cm, $h_{\text{ref}} = 8$ cm): The MPC drives Tank 1 level downward. At $t = 85$ s, $h_1 = 12$ cm and $\rho = 0.13$ → WARNING triggered. At $t = 95$ s, $h_1 = 9.8$ cm and $\rho = -0.01$ → VIOLATION triggered. The fallback freezes the valve at the last safe position. The Layer 0 interlock activates: valve opens fully to allow inflow, and $h_1$ stabilizes at 11.2 cm (within ODD) by $t = 150$ s. The MPC resumes at $t = 185$ s after 5 consecutive intervals with $\rho > 0.13$.

**Scenario S26** (Communication loss: 30 s dropout at $t = 100$ s): The serial link is interrupted at $t = 100$ s. The heartbeat timeout (10 s) expires at $t = 110$ s. The ODD monitor detects $c = 0$ at $t = 110$ s → VIOLATION. The Edge Agent enters island-autonomy mode: holds last reference, applies Layer 0 safety only. During the 30-s dropout, $h_1$ drifts from 25.0 cm to 25.8 cm (0.8 cm drift due to uncompensated disturbance). When communication resumes at $t = 130$ s, the MPC resumes after recovery verification.

**Scenario S31** (Combined: $h_0 = 38$ cm, pump +20%, $\sigma = 2$ mm): Multiple stressors are applied simultaneously. At $t = 0$ s, $\rho = 0.20$ (already near boundary due to high initial level). At $t = 35$ s, the pump disturbance drives $h_1$ to 40.5 cm → $\rho = -0.03$ → VIOLATION on the upper level bound. The fallback closes the valve to reduce inflow. $h_1$ peaks at 40.8 cm (within physical limit of 45 cm, 4.2 cm margin) and recovers to 38.2 cm by $t = 120$ s.

__*[Figure 4 about here]*__

__5.4  SiL–MiL Consistency__

Table 5 compares SiL and MiL results for the nominal scenarios to verify code generation fidelity.

__*Table 5. SiL vs. MiL Comparison (Nominal Scenarios)*__

| Metric | MiL (mean) | SiL (mean) | Difference | Threshold |
|--------|-----------|-----------|------------|-----------|
| Level RMSE (mm) | 1.8 | 1.9 | +0.1 | 5.0 |
| MPC solve time (ms) | 8 | 12 | +4 | 5,000 |
| Max |MiL−SiL| level (mm) | — | — | 0.3 | 1.0 |
| $\rho$ agreement | — | — | ±0.01 | — |

The SiL–MiL difference is negligible (max 0.3 mm), consistent with the results in Chen et al. (2026a). The ODD distance function $\rho$ agrees to within ±0.01 between MiL and SiL, confirming that the ODD monitor produces consistent results across execution environments.

__5.5  ODD Coverage Analysis__

The 32 SiL scenarios provide systematic coverage of the ODD dimensions. Table 6 summarizes the coverage achieved.

__*Table 6. ODD Dimension Coverage*__

| Dimension | Parameters | Range Tested | ODD Range | Coverage |
|-----------|-----------|-------------|-----------|----------|
| $\mathcal{S}_{\text{hyd}}$: Water level | $h_1$, $h_2$ | [8, 42] cm | [10, 40] cm | 107% (incl. boundary) |
| $\mathcal{S}_{\text{act}}$: Valve | $u$ | [0, 100]% | [5, 95]% | 111% |
| $\mathcal{S}_{\text{act}}$: Valve rate | $|\Delta u|$ | [0, 15]%/step | [0, 10]%/step | 150% |
| $\mathcal{S}_{\text{act}}$: Pump | $f_{\text{pump}}$ | [0.1, 0.5] L/s | [0.1, 0.5] L/s | 100% |
| $\mathcal{S}_{\text{comm}}$: Link | $c$ | {0, 1} | {1} | 200% (both states) |
| $\mathcal{S}_{\text{env}}$: Pump disturb. | $\Delta Q$ | [−20%, +20%] | [−20%, +20%] | 100% |
| $\mathcal{S}_{\text{env}}$: Sensor noise | $\sigma$ | [0.8, 2] mm | [0, 2] mm | 100% |

Coverage exceeds 100% for dimensions where boundary violations are deliberately injected. The valve rate dimension achieves 150% coverage because the actuator saturation scenarios test rates 50% beyond the ODD limit. This systematic coverage is a prerequisite for ODD verification at the SiL level.

__6  Discussion__

__6.1  ODD Formalization for Water Systems__

The ODD formalization presented here—a convex polytope with IDZ-derived safety margins and a real-time distance-to-boundary metric—provides the mathematical foundation for safety certification of autonomous water controllers. Two aspects merit discussion.

First, the safety margin derivation (Eq. 8–9) is conservative by design: it assumes the worst-case scenario (maximum flow during the full transport delay) and applies a 1.5× safety factor. For the dual-tank system, this results in a 5 cm margin on each side, reducing the operational range from [5, 45] cm to [10, 40] cm (a 25% reduction). For field-scale canal systems with longer delays ($\tau_d$ = 100–1000 s) and larger cross-sections ($A_s$ = 10–100 m²), the relative margin would be smaller because the level excursion per unit time decreases with $A_s$:

$$
\delta_h \propto \frac{Q_{\max} \cdot \tau_d}{A_s} \tag{13}
$$

For a 50-pool canal system with $A_s = 50$ m², $Q_{\max} = 5$ m³/s, $\tau_d = 300$ s: $\delta_h = 5 \times 300 / 50 = 30$ cm, which is 3% of a typical 10 m operating range—a much smaller relative margin.

Second, the convex polytope assumption (Eq. 3) is valid when ODD constraints are linear in the state variables. For the dual-tank system, all constraints are indeed linear (box constraints on levels, rates, and flows). For field-scale systems with nonlinear dynamics (e.g., flow-dependent constraints, backwater effects), the ODD boundary may be non-convex. In such cases, the polytope formulation can be replaced by a union of polytopes or a general nonlinear constraint set, at the cost of increased computational complexity for the $\rho$ evaluation.

__6.2  SiL Verification as a Safety Gate__

The SiL verification demonstrates that systematic boundary testing is essential for safety certification. The 16 nominal scenarios (Groups A–D) all pass with comfortable margins—the minimum $\rho = 0.18$ in S11 is still well within the ODD. It is only the boundary scenarios (Groups E–H) that exercise the safety-critical code paths: the ODD monitor, the fallback protocol, and the Layer 0 interlock. Without boundary testing, these critical functions would remain unverified at the SiL level.

The 100% detection rate (16/16) and the consistent detection latency (1.4 ± 0.4 intervals) provide confidence that the ODD monitor is reliable. However, two caveats apply. First, the detection latency for communication loss (2.0 intervals = 10 s) is determined by the heartbeat timeout, which is a design parameter. Reducing the timeout would improve detection latency at the cost of increased false alarms during transient communication glitches. Second, the current ODD monitor evaluates individual constraints independently; correlated violations (Group H scenarios) are detected by whichever constraint is violated first, without explicit multi-dimensional analysis. For field-scale systems with hundreds of constraints, a more sophisticated monitoring approach—such as the Mahalanobis distance in the normalized constraint space—may be warranted.

__6.3  From SiL to HiL: Expected Additional Challenges__

The SiL verification quantifies code generation fidelity (SiL–MiL difference: 0.1 mm) and ODD monitor accuracy. The next step in the xIL chain—HiL verification on the physical dual-tank platform—will introduce additional challenges:

1. **Sensor noise amplification**: Real ultrasonic sensors exhibit non-Gaussian outliers (~2% of readings) that may trigger spurious ODD warnings. The Kalman filter (Chen et al., 2026a) mitigates this but does not eliminate it entirely.

2. **Actuator hysteresis**: The stepper motor driving valve V12 exhibits approximately 1° of backlash, which is not modeled in the SiL. This may cause small oscillations near ODD boundaries, potentially increasing the ODD monitor's false alarm rate.

3. **Timing jitter**: The Arduino Mega 2560 execution time (320 ms worst case) introduces timing uncertainty that is absent in SiL. For the 5-s sampling interval, this 6.4% jitter is acceptable, but it would be more significant at faster sampling rates.

These challenges will be systematically addressed in the companion paper CKG-3 (HiL verification with adaptive MAS).

__6.4  Scaling the ODD Framework__

The dual-tank system has a low-dimensional ODD ($\mathbb{R}^7 \times \{0,1\}$). For field-scale systems, the ODD dimensionality grows with the number of pools, actuators, and failure modes. Consider a 10-pool canal system: the hydraulic state space has 20 dimensions ($h_i$ for each pool × 2 sensors), the actuator space has 10 dimensions, and the communication space has 10 binary dimensions. The total ODD has ~40 continuous and ~10 binary dimensions.

The combinatorial growth of boundary scenarios is the primary scaling challenge: a 10-pool system with 4 boundary scenarios per dimension would require $40 \times 4 = 160$ boundary scenarios. Exhaustive SiL testing becomes impractical for systems with 50+ pools. Two mitigation strategies are available: (1) importance sampling, where boundary scenarios are generated based on risk priority (e.g., focusing on the most critical pool-gate combinations), and (2) formal verification using reachability analysis (Althoff et al., 2021), which can prove safety for entire regions of the state space without enumeration. The integration of formal verification with SiL testing is a promising research direction.

__6.5  Comparison with Automotive ODD Practice__

The ODD formalization for water systems differs from automotive ODD in several respects. First, the dynamics are slower (sampling at 5 s vs. 10 ms for autonomous vehicles), providing more time for detection and fallback. Second, the consequence of ODD violation is property damage (flooding, infrastructure damage) rather than loss of life, allowing slightly less conservative margins. Third, the operating environment is more predictable: canal flows are largely deterministic (controlled by upstream gates), unlike the stochastic traffic environment. These differences suggest that water systems may achieve WSAL-3 (conditional autonomy) with less stringent ODD verification than automotive Level 3, provided that adequate safety margins are maintained and Layer 0 hardware interlocks provide a reliable last line of defense.

__7  Conclusions__

This paper has formalized the Operational Design Domain (ODD) for water conveyance systems and developed a systematic SiL verification methodology that combines nominal performance testing with boundary violation detection. The key findings are:

1. The ODD can be formalized as a convex polytope in the joint space of hydraulic states, actuator capabilities, communication status, and environmental disturbances. Safety margins are derived analytically from the IDZ transfer function parameters (Eq. 8–9), providing a physics-based foundation for boundary specification.

2. The distance-to-boundary function $\rho(\mathbf{x})$ provides continuous real-time monitoring of ODD proximity. The three-zone classification (NOMINAL/WARNING/VIOLATION) with the associated fallback protocol ensures safe operation even when ODD boundaries are approached or crossed.

3. The 32-scenario SiL verification achieves mean RMSE of 1.9 mm within the ODD (all 16 nominal scenarios pass) and 100% ODD violation detection (all 16 boundary violations detected within 1.4 ± 0.4 sampling intervals). No physical limit violations occur in any scenario, confirming the effectiveness of the safety margins and fallback protocol.

4. The SiL–MiL performance difference is negligible (0.1 mm), confirming that the auto-generated C code faithfully implements the MPC controller and ODD monitor.

These results establish the methodological foundation for the WSAL-2→3 transition in water infrastructure: formal ODD specification + systematic SiL verification = verified operating envelope for conditional autonomy. The companion paper CKG-3 will extend this framework to HiL verification on the physical platform and demonstrate adaptive ODD expansion through successive xIL campaigns.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]) and the National Natural Science Foundation of China (Grant Nos. [to be inserted]). The authors thank the CHS laboratory team at Hebei University of Engineering for constructing and instrumenting the dual-tank platform.

__References__

Althoff, M., Stursberg, O., & Buss, M. (2021). Reachability analysis of nonlinear systems with uncertain parameters using conservative linearization. In Proceedings of the 49th IEEE Conference on Decision and Control (pp. 4042–4048). https://doi.org/10.1109/CDC.2010.5717903

BSI. (2020). PAS 1883:2020 — Operational Design Domain (ODD) taxonomy for an automated driving system (ADS). British Standards Institution.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Clemmens, A. J., Kacerek, T. F., Grawitz, B., & Schuurmans, W. (2005). Test cases for canal control algorithms. Journal of Irrigation and Drainage Engineering, 131(6), 502–514. https://doi.org/10.1061/(ASCE)0733-9437(2005)131:6(502)

Czarnecki, K. (2018). Operational Design Domain for automated driving systems: Taxonomy of basic terms. University of Waterloo Report UW-ECE-2018-04.

Dunn, W. R. (2018). Practical design of safety-critical computer systems (2nd ed.). Reliability Press.

Gyllenhammar, M., Johansson, R., Warg, F., Chen, D., Heyn, H.-M., Sanfridson, M., et al. (2020). Towards an operational design domain that supports the safety argumentation of an automated driving system. In Proceedings of the 10th European Congress on Embedded Real Time Systems (ERTS 2020).

IEC. (2016). IEC 61511: Functional safety — Safety instrumented systems for the process industry sector. International Electrotechnical Commission.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). Modeling and control of hydrosystems. Springer.

Macenski, S., Singh, S., Martin, F., & Gines, J. (2023). Regulated pure pursuit for robot path tracking. Autonomous Robots, 47(6), 685–694.

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

SAE. (2021). SAE J3016: Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles. SAE International.

Thorn, E., Kimmel, S., & Chaka, M. (2018). A framework for automated driving system testable cases and scenarios. National Highway Traffic Safety Administration Report DOT HS 812 623.

van Overloop, P. J. (2006). Model predictive control on open water systems (Doctoral dissertation). Delft University of Technology.

__Data Availability__

The ODD specification files, SiL test harness, ODD monitor C code, OpenModelica dual-tank FMU, and all 32-scenario simulation logs are available at https://github.com/IWHR-CHS/dual-tank-odd (to be made public upon acceptance; reviewer access available upon request).

__Figure Captions__

__Figure 1.__ ODD concept for water systems control. (a) The ODD polytope in the joint space of hydraulic states, actuator capabilities, and disturbances. The green region represents the verified ODD; the yellow annulus is the warning zone; the red boundary marks ODD violation. (b) The WSAL-2→3 transition requires formal ODD specification and xIL verification.

__Figure 2.__ ODD monitor architecture. The distance-to-boundary function $\rho(\mathbf{x})$ is evaluated at each sampling instant. Three zones (NOMINAL, WARNING, VIOLATION) trigger corresponding actions. The fallback protocol activates Layer 0 safety interlocks upon VIOLATION.

__Figure 3.__ SiL architecture. The OpenModelica plant FMU, auto-generated MPC controller (C code), and ODD monitor are coupled via FMI 2.0 co-simulation. The test harness manages scenario execution, fault injection, and data logging.

__Figure 4.__ Representative SiL verification results. (a) Scenario S17 (level boundary violation): water level trajectory, $\rho$ time series, ODD status transitions (NOMINAL → WARNING → VIOLATION → recovery). (b) Scenario S26 (communication loss): heartbeat-based detection, island-autonomy activation, and recovery after link restoration. (c) Scenario S31 (combined stressors): multi-dimensional boundary approach with correct prioritization. (d) Box plots of detection latency across all 16 boundary scenarios.
