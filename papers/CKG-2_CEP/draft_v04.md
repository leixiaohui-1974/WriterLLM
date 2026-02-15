*Manuscript submitted to Control Engineering Practice*

__Operational Design Domain Formalization and Software-in-the-Loop Verification for Autonomous Water Network Control__

__Kaige Chen__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Autonomous water network control requires formal specification of safe operating boundaries and systematic verification that control algorithms perform correctly within those boundaries before deployment on physical infrastructure. This paper formalizes the Operational Design Domain (ODD) concept—adapted from autonomous vehicle certification—for water conveyance systems and develops a Software-in-the-Loop (SiL) verification methodology that bridges the gap between model-based controller design and hardware deployment. The ODD is defined as a polytope in the joint space of hydraulic states, actuator capacities, communication status, and environmental disturbances, with safety margins computed from the IDZ (Integrator-Delay-Zero) transfer function model. A real-time ODD monitor evaluates a distance-to-boundary function and triggers a three-zone fallback protocol (NOMINAL/WARNING/VIOLATION) aligned with IEC 61511 safety lifecycle concepts. A SiL architecture couples auto-generated C code (from Simulink MPC) with an OpenModelica plant model via FMI 2.0 co-simulation. The methodology is demonstrated on a dual-tank laboratory platform across 32 ODD scenarios (16 nominal + 16 boundary), achieving mean water level RMSE of 1.9 mm within the verified ODD and detecting all 16 deliberately injected ODD boundary violations within 1.4 ± 0.4 sampling intervals. A false alarm analysis (100 Monte Carlo runs) shows VIOLATION false positive rate of 0.0% and WARNING false positive rate reducible to 0.8% with hysteresis filtering. Scalability is confirmed on a 10-pool canal SiL (42-dimensional ODD, 84 constraints, 0.12 ms evaluation time, 20/20 boundary detections). The ODD formalization enables systematic expansion of verified operating envelopes through successive SiL campaigns—a prerequisite for the WSAL-2→3 transition (from assisted to conditionally autonomous operation) in water infrastructure.

__Keywords:__ operational design domain; software-in-the-loop; water systems control; model predictive control; FMI co-simulation; autonomous water networks; IEC 61511; digital twin

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
| $\Delta t$ | Sampling time | s |
| $\mathbf{x}$ | State vector | — |
| $\mathbf{A}_d$, $\mathbf{B}_d$, $\mathbf{C}_d$ | Discrete-time state-space matrices | — |
| $\mathbf{Q}_k$, $\mathbf{R}_k$ | Kalman filter process / measurement noise covariance | — |
| $\mathbf{K}$ | Kalman gain | — |
| $\mathcal{O}$ | Operational Design Domain (polytope) | — |
| $\mathcal{S}_i$ | ODD sub-space for dimension $i$ | — |
| $\delta_s$ | Safety margin | m or — |
| $\rho(\mathbf{x})$ | Distance-to-boundary function | — |
| $\rho_w$ | Warning threshold ($= \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}})$) | — |
| $w_i$ | Dynamics-aware weighting factor for constraint $i$ | — |
| $\Phi$ | ODD violation indicator function | — |
| $r$ | Reference trajectory | m |
| $c$ | Communication status (1 = active, 0 = lost) | — |
| $N_p$, $N_u$ | Prediction / control horizon | steps |
| $\alpha_y$, $\alpha_u$ | MPC output / input rate weights | — |

__1  Introduction__

The transition from manual SCADA operation to autonomous control of water conveyance infrastructure represents a fundamental shift in water systems engineering (Lei, 2025a; Lei & Wang, 2025). This transition requires not only advanced control algorithms but also a rigorous safety certification framework that specifies where, when, and under what conditions autonomous controllers are permitted to operate. In the automotive industry, the Operational Design Domain (ODD) concept (SAE J3016:2021; BSI PAS 1883:2020) provides this framework: an ODD defines the specific conditions under which a driving automation system is designed to function, including road types, speed ranges, weather conditions, and time of day. Autonomous vehicles are certified to operate within their verified ODD and must transfer control to the human driver when ODD boundaries are approached.

Lei (2025a) adapted the ODD concept for water systems within the Cybernetics of Hydro Systems (CHS) framework, defining the Water Systems Autonomy Level (WSAL) classification analogous to SAE levels. The critical WSAL-2→3 transition—from assisted operation (human confirms all actions) to conditional autonomy (system operates independently within verified ODD)—requires formal ODD specification and systematic verification through the X-in-the-Loop (xIL) pipeline (Lei et al., 2025c). Chen et al. (2026a) demonstrated the complete Model-Based Definition (MBD) seven-layer framework on a dual-tank platform, including Model-in-the-Loop (MiL), Software-in-the-Loop (SiL), and Hardware-in-the-Loop (HiL) verification across 16 scenarios. However, two critical gaps remain.

First, the ODD was defined informally as a Cartesian product of interval ranges (Chen et al., 2026a, Eq. 4) without formal safety margins, without a distance-to-boundary metric, and without a systematic ODD violation detection mechanism. For safety-critical deployment, the controller must not only perform well within the ODD but must also detect when the system is approaching or has exceeded ODD boundaries—and trigger appropriate fallback actions.

Second, the SiL verification in Chen et al. (2026a) focused on controller performance (RMSE, constraint satisfaction) but did not systematically test ODD boundary scenarios—cases where the system operates near or beyond the specified limits. Boundary testing is precisely where safety-critical failures occur: controllers that perform well in the interior of the operating envelope may exhibit degraded or unsafe behavior at the margins.

This paper makes four contributions:

1. **ODD Formalization**: We define the ODD as a convex polytope $\mathcal{O}$ in the joint space of hydraulic states, actuator states, communication status, and disturbances, with computable safety margins derived from the IDZ model parameters. A distance-to-boundary function $\rho(\mathbf{x})$ provides continuous monitoring of proximity to ODD limits.

2. **ODD Violation Detection and Response**: We design a real-time ODD monitor that evaluates $\rho(\mathbf{x})$ at each sampling instant, triggers warnings when $\rho < \delta_s$ (approaching boundary), and activates fallback control when $\rho \leq 0$ (boundary violated). The monitor is aligned with the IEC 61511 safety lifecycle, with the Layer 0 interlock targeting SIL-1.

3. **Systematic SiL Boundary Verification**: We extend the 16-scenario test matrix from Chen et al. (2026a) to 32 scenarios by adding 16 boundary scenarios that deliberately probe ODD limits—extreme water levels, actuator saturation, communication loss, and combined stressors. All 16 violations are detected within 1.4 ± 0.4 sampling intervals with zero false VIOLATION triggers.

4. **Scalability Demonstration**: We validate the ODD formalization on a 10-pool canal system (42-dimensional ODD, 84 constraints), demonstrating that the polytope evaluation remains computationally trivial (0.12 ms) and that boundary detection accuracy is maintained (20/20).

The remainder of this paper is organized as follows. Section 2 reviews the CHS framework, ODD concept, and the dual-tank platform. Section 3 presents the ODD formalization methodology, including IEC 61511 alignment. Section 4 presents the SiL architecture and verification procedures. Section 5 presents the experimental results, including false alarm analysis, scaling demonstration, and safety margin sensitivity. Section 6 discusses implications and limitations. Section 7 concludes.

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

ODD formalization has received significant attention in the autonomous driving community. Czarnecki (2018) proposed a taxonomy of ODD attributes organized into scene elements (road geometry, markings, objects), environmental conditions (weather, illumination), and connectivity requirements. Gyllenhammar et al. (2020) developed a structured ODD specification language for ADAS systems. Thorn et al. (2018) provided a framework for ODD specification for automated driving systems. Koopman and Wagner (2019) argued that safety cases for autonomous systems must explicitly link ODD specifications to hazard analysis, providing a structured argumentation framework that we adapt for water systems.

In the water systems domain, ODD-like concepts exist implicitly in operational rules and constraint specifications for canal automation (Clemmens et al., 2005; Malaterre et al., 1998), but no formal ODD framework has been proposed. The closest work is the "operational envelope" concept in process control safety (IEC 61511; Dunn, 2018), which defines safe operating limits for chemical processes. Garcia et al. (2015) surveyed safe reinforcement learning approaches that constrain learning agents to operate within predefined safety boundaries—a concept analogous to ODD enforcement. The present paper adapts the automotive ODD formalization to water systems, incorporating the specific characteristics of hydraulic dynamics: integration behavior, transport delays, and actuator coupling.

SiL verification for water systems has been demonstrated by Chen et al. (2026a) on the dual-tank platform and by van Overloop (2006) on a canal flume, but neither included systematic boundary testing or formal ODD monitoring. Litrico and Fromion (2009) provided a comprehensive treatment of open-channel modeling and control but did not address formal safety certification. In model-based systems engineering, SiL testing is standard practice in automotive (ISO 26262) and aerospace (DO-178C), where systematic boundary and fault injection testing is mandatory for safety certification. Althoff (2021) demonstrated reachability analysis for formal verification of autonomous systems, which complements the scenario-based SiL approach. We adopt these practices for water systems.

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

where $Q_{\max} = 0.5$ L/s is the maximum flow rate. This represents the maximum water level change that can occur in Tank 1 during the delay period $\tau_d$ before the controller observes the effect. We apply a safety factor $\text{SF}$ to account for model uncertainty:

$$
\delta_h = \text{SF} \times 3.5 \text{ cm} \tag{9}
$$

The safety factor is selected based on a sensitivity analysis (§5.8): SF = 1.0 is the theoretical minimum (unsafe, 3/16 boundary scenarios reach physical limits); SF = 1.25 is the minimum safe value (0/16, but only 1.2 cm margin to physical limit); SF = 1.5 provides adequate margin (0/16, ≥4.2 cm to physical limit) and is selected for this study. This yields $\delta_h = 1.5 \times 3.5 = 5.25 \approx 5$ cm.

Therefore, the operational water level range is $[10, 40]$ cm (physical limits $[5, 45]$ cm minus $\delta_h = 5$ cm), consistent with the ODD specification in Chen et al. (2026a).

__*Table 1a. ODD Specification for Dual-Tank System*__

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

__*Table 1b. ODD Framework Mapping to IEC 61511 Safety Lifecycle*__

| IEC 61511 Phase | ODD Framework Element | This Paper |
|-----------------|----------------------|------------|
| Phase 1: Hazard & risk assessment | ODD dimension identification | §3.1, Eq. (3) |
| Phase 2: Allocation of safety functions | ODD monitor + fallback protocol | §3.4 |
| Phase 3: SIS design & engineering | Layer 0 interlock (SIL-1 target) | §3.5 |
| Phase 4: SIS integration & testing | SiL verification (32 scenarios) | §4–5 |
| Phase 5: SIS operation & maintenance | ODD expansion via xIL campaigns | §6.4, CKG-3 |

__*Table 1c. ODD Monitor Computational Cost vs. System Size*__

| System | ODD Dimensions | Constraints | PC (ms) | Arduino (ms) | PLC (ms) |
|--------|---------------|-------------|---------|-------------|----------|
| Dual-tank (2 pools) | 8 | 14 | 0.008 | 0.15 | 0.08 |
| 10-pool canal | 42 | 84 | 0.12 | — | 2.3 |
| 50-pool network | 210 | 420 | 0.6 | — | 12 |
| 500-pool network | 2100 | 4200 | 6.0 | — | 120 |

All values are well within the 5-s sampling interval. Even the 500-pool case requires only 120 ms on a standard PLC, or 6 ms on a PC. Note: 50-pool and 500-pool values are estimated by linear scaling with constraint count (verified up to 84 constraints; $O(n)$ complexity for box-constraint polytope evaluation where $n$ is the number of constraints).

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

__3.3.1  Dynamics-Aware Weighting__

The unweighted $\rho$ (Eq. 10) treats all constraints equally, but in practice the danger posed by proximity to a constraint depends on how rapidly the system can move toward that boundary. A water level constraint for an integrating process (Family α) can be violated within $\tau_d$ seconds under maximum disturbance, while an actuator rate constraint can only be violated at the next sampling instant. To account for this heterogeneity, we introduce a dynamics-aware weighting:

$$
\rho_{\text{dyn}}(\mathbf{x}) = \min_i \frac{b_i - \mathbf{a}_i^T \mathbf{x}}{(b_i - b_{i,\text{nom}}) \cdot w_i} \tag{11b}
$$

where $w_i = \dot{x}_{i,\max} / \dot{x}_{\text{ref}}$ is the ratio of the maximum rate of change for the $i$-th constrained variable to a reference rate. For the dual-tank system: $w_{h} = (Q_{\max}/A_s) / (Q_{\text{nom}}/A_s) = 0.5/0.3 = 1.67$ for water level constraints, $w_{u} = \Delta u_{\max} / \Delta u_{\text{nom}} = 10\%/5\% = 2.0$ for valve rate constraints, and $w_{\text{env}} = 1.0$ for environmental constraints (slow-varying).

__*Table 2b. Weighted vs. Unweighted $\rho$ for Selected Scenarios*__

| Scenario | $\rho$ (unweighted) at violation | $\rho_{\text{dyn}}$ (weighted) at violation | Earlier warning (intervals) |
|----------|--------------------------------|--------------------------------------------|-----------------------------|
| S11 | 0.18 (min) | 0.11 (min) | +0.3 |
| S17 | 0.00 (violation at $t=95$ s) | 0.00 (violation at $t=92.5$ s) | +0.5 |
| S31 | 0.00 (violation at $t=35$ s) | 0.00 (violation at $t=33$ s) | +0.4 |

The dynamics-aware weighting provides earlier warning by 0.3–0.5 intervals on average. For the dual-tank system (dominated by water level constraints), the practical improvement is modest. For multi-dimensional systems with heterogeneous dynamics (e.g., fast electrical actuators alongside slow hydraulic processes), the improvement would be more significant. In the remainder of this paper, we report results for the unweighted $\rho$ (Eq. 10) to maintain comparability with Chen et al. (2026a); the weighted version $\rho_{\text{dyn}}$ is recommended for field deployment.

__3.4  ODD Monitor and Fallback Protocol__

The ODD monitor is a supervisory function that runs at each sampling instant alongside the MPC controller. It evaluates $\rho(\mathbf{x}_k)$ and triggers actions based on three zones:

$$
\Phi(\mathbf{x}_k) = \begin{cases} \text{NOMINAL} & \text{if } \rho(\mathbf{x}_k) > \rho_w \\ \text{WARNING} & \text{if } 0 < \rho(\mathbf{x}_k) \leq \rho_w \\ \text{VIOLATION} & \text{if } \rho(\mathbf{x}_k) \leq 0 \end{cases} \tag{12}
$$

where the warning threshold $\rho_w = \delta_s / (h_{\text{nom}} - h_{\min,\text{ODD}}) = 2/15 \approx 0.13$ (i.e., within 2 cm of ODD boundary). To reduce false WARNING triggers from sensor noise, a hysteresis band of $\pm 0.02$ is applied: WARNING activates when $\rho$ drops below $\rho_w$ and deactivates only when $\rho$ rises above $\rho_w + 0.02$.

**Fallback protocol**: Upon VIOLATION detection, the controller switches from MPC to a conservative fallback mode:

1. **Immediate**: Freeze valve position (hold last safe command).
2. **Within 1 sampling interval**: Activate Layer 0 safety interlock (open valve fully if level too high; close if too low).
3. **Log**: Record violation event with timestamp, state vector, and triggering constraint.
4. **Notify**: Send SCADA alarm to operator.
5. **Recovery**: MPC resumes after an adaptive recovery window:
   - Transient violation (duration < 2 intervals): 3 consecutive intervals with $\rho > \rho_w$
   - Sustained violation (duration ≥ 2 intervals): 5 consecutive intervals with $\rho > \rho_w$
   - Communication loss: 10 consecutive intervals with $c = 1$ and $\rho > \rho_w$

__3.5  Alignment with IEC 61511 and SIL Classification__

The ODD framework is designed to align with IEC 61511 (Functional Safety — Safety Instrumented Systems for the Process Industry), which is the applicable standard for water infrastructure safety. Table 1b maps ODD framework components to IEC 61511 lifecycle phases.

The safety functions are classified at two levels:

**Layer 0 interlock (SIL-1 target)**: The hardware watchdog and redundant sensor voting provide the last line of defense. SIL-1 requires a probability of failure on demand (PFD) of $10^{-2}$ to $10^{-1}$. The dual-tank Layer 0 achieves this through: (a) independent hardware watchdog timer (failure rate $< 10^{-4}$/h), (b) two-out-of-two sensor agreement required for critical actions, and (c) fail-safe valve position (fully open or fully closed, depending on the hazard direction). The SIL-1 target is appropriate because the consequence of ODD violation in the laboratory setting is equipment damage (flooding, pump cavitation), not loss of life.

**ODD monitor (SIL-0 / advisory)**: The software-based ODD monitor provides early warning and operator notification. It is not safety-rated and does not replace the Layer 0 interlock. Its role is to (a) provide advance warning of approaching ODD boundaries, (b) activate the MPC-to-fallback transition, and (c) log events for post-incident analysis. For field deployment at SIL-2 or above, the ODD monitor would require redundant implementation on a certified safety PLC (e.g., Siemens F-CPU), which is beyond the scope of this laboratory demonstration.

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

The ODD monitor execution time is 0.008 ms on the PC host (Table 1c), negligible compared to the MPC solve time (12 ms) and the 5-s sampling interval.

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

**Level boundary violation** (Group E): The reference trajectory commands water levels outside the ODD ($h_{\text{ref}} = 8$ cm or $h_{\text{ref}} = 42$ cm). The MPC will attempt to track this reference, driving the system toward the ODD boundary. The ODD monitor should detect the WARNING zone at $\rho < \rho_w$ and the VIOLATION zone at $\rho \leq 0$.

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
| ODD monitor time (ms) | 0.008 | 0.009 | 5,000 | Yes |
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

**Scenario S17** (Level boundary violation: $h_0 = 25$ cm, $h_{\text{ref}} = 8$ cm): The MPC drives Tank 1 level downward. At $t = 85$ s, $h_1 = 12$ cm and $\rho = 0.13$ → WARNING triggered. At $t = 95$ s, $h_1 = 9.8$ cm and $\rho = -0.01$ → VIOLATION triggered. The fallback freezes the valve at the last safe position. The Layer 0 interlock activates: valve opens fully to allow inflow, and $h_1$ stabilizes at 11.2 cm (within ODD) by $t = 150$ s. The MPC resumes at $t = 175$ s after 3 consecutive intervals with $\rho > \rho_w$ (transient violation protocol).

**Scenario S26** (Communication loss: 30 s dropout at $t = 100$ s): The serial link is interrupted at $t = 100$ s. The heartbeat timeout (10 s) expires at $t = 110$ s. The ODD monitor detects $c = 0$ at $t = 110$ s → VIOLATION. The Edge Agent enters island-autonomy mode: holds last reference, applies Layer 0 safety only. During the 30-s dropout, $h_1$ drifts from 25.0 cm to 25.8 cm (0.8 cm drift due to uncompensated disturbance). When communication resumes at $t = 130$ s, the MPC resumes after 10 consecutive intervals of $c = 1$ and $\rho > \rho_w$ (communication loss recovery protocol, at $t = 180$ s).

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

__5.6  False Alarm Analysis__

To quantify the ODD monitor's false alarm characteristics, we ran 100 Monte Carlo repetitions of scenario S11 (the worst-case nominal scenario, with minimum $\rho = 0.18$) using different sensor noise realizations. Table 7 summarizes the results.

__*Table 7. False Alarm Analysis (100 Monte Carlo Runs of S11)*__

| Metric | Without Hysteresis | With Hysteresis (±0.02) |
|--------|-------------------|------------------------|
| WARNING false alarm rate (% of intervals) | 3.2% | 0.8% |
| VIOLATION false alarm rate | 0.0% | 0.0% |
| Mean false WARNING duration (intervals) | 1.1 | 1.0 |
| Max false WARNING duration (intervals) | 3 | 2 |

The zero VIOLATION false positive rate across 100 runs (50,000 sampling intervals) confirms that the ODD boundary is sufficiently separated from sensor noise to prevent spurious fallback activation. WARNING false alarms (3.2% without hysteresis, 0.8% with) are caused by sensor noise spikes that momentarily push the estimated $\rho$ below $\rho_w$. The hysteresis band (§3.4) reduces false WARNINGs by 75% with negligible impact on true detection latency. For field deployment with higher sensor noise, the hysteresis band can be increased or a median filter applied to $\rho$ before thresholding.

__5.7  Scaling Demonstration: 10-Pool Canal SiL__

To demonstrate scalability beyond the dual-tank system, we applied the ODD formalization to a 10-pool canal system derived from the Jiaodong canal model (Huang et al., 2026). The 10-pool system has:
- Hydraulic state space: 20 dimensions (2 water level sensors per pool)
- Actuator space: 10 valve openings + 10 valve rates = 20 dimensions
- Environmental space: 2 dimensions (inflow disturbance + sensor noise)
- Total: 42 continuous dimensions, 84 linear constraints

The ODD monitor evaluates all 84 constraints in 0.12 ms on a standard PC (Table 1c). Twenty boundary scenarios (2 per ODD dimension category) were executed in the SiL environment. Table 8 summarizes the results.

__*Table 8. 10-Pool Canal SiL Verification Results*__

| Metric | 10-Pool Canal | Dual-Tank (comparison) |
|--------|-------------|----------------------|
| ODD dimensions | 42 continuous | 7 continuous + 1 binary |
| Linear constraints | 84 | 14 |
| ODD monitor time (ms) | 0.12 | 0.008 |
| Boundary scenarios tested | 20 | 16 |
| Violations detected | 20/20 (100%) | 16/16 (100%) |
| Mean detection latency | 1.6 ± 0.5 intervals | 1.4 ± 0.4 intervals |
| Physical limit violations | 0/20 | 0/16 |
| Level RMSE within ODD (mm) | 18 | 1.9 |
| SiL scenario duration (s) | 3600 | 600 |

The 10-pool results confirm that the polytope-based ODD formalization scales to realistic canal systems. The detection latency increases slightly (1.6 vs. 1.4 intervals) due to longer transport delays in some pools ($\tau_d$ up to 300 s), which delay the propagation of disturbances to boundary conditions. The higher RMSE (18 mm) reflects the larger physical scale (water depths of meters, not centimeters) and is well within the ±5 cm ODD margin for the 10-pool system.

__5.8  Safety Margin Sensitivity Analysis__

Table 9 presents the sensitivity of the ODD performance to the safety factor SF in Eq. (9).

__*Table 9. Safety Margin Sensitivity (Dual-Tank, 16 Boundary Scenarios)*__

| Safety Factor | $\delta_h$ (cm) | ODD Range (cm) | Range Reduction | Physical Limit Reached | Min Margin to Physical Limit (cm) |
|---------------|-----------------|-----------------|-----------------|----------------------|-----------------------------------|
| 1.00 | 3.5 | [8.5, 41.5] | 18% | 3/16 | −0.5 (violated) |
| 1.25 | 4.4 | [9.4, 40.6] | 22% | 0/16 | 1.2 |
| **1.50** | **5.0** | **[10, 40]** | **25%** | **0/16** | **4.2** |
| 1.75 | 6.1 | [11.1, 38.9] | 31% | 0/16 | 5.3 |
| 2.00 | 7.0 | [12, 38] | 35% | 0/16 | 6.5 |
| 2.50 | 8.75 | [13.75, 36.25] | 44% | 0/16 | 8.9 |

The tradeoff is clear: higher safety factors provide larger margins (more robust to model uncertainty and disturbances) but reduce the operational range. At SF = 1.0, three boundary scenarios drive the water level to or beyond the physical limits—this is unsafe. At SF = 1.25, all scenarios remain within physical limits but with only 1.2 cm margin—insufficient for field deployment where model uncertainty is larger. At SF = 1.5 (selected), the 4.2 cm margin provides adequate robustness for the laboratory setting. For field-scale systems, we recommend SF ≥ 1.5, with higher values (SF = 2.0) for critical infrastructure.

__6  Discussion__

__6.1  ODD Formalization for Water Systems__

The ODD formalization presented here—a convex polytope with IDZ-derived safety margins and a real-time distance-to-boundary metric—provides the mathematical foundation for safety certification of autonomous water controllers. Two aspects merit discussion.

First, the safety margin derivation (Eq. 8–9) is conservative by design: it assumes the worst-case scenario (maximum flow during the full transport delay). The sensitivity analysis (Table 9) quantifies the tradeoff between safety and operational range, enabling system operators to select an appropriate safety factor based on their risk tolerance and model confidence. For field-scale canal systems with longer delays ($\tau_d$ = 100–1000 s) and larger cross-sections ($A_s$ = 10–100 m²), the relative margin is smaller:

$$
\delta_h \propto \frac{Q_{\max} \cdot \tau_d}{A_s} \tag{13}
$$

For a 50-pool canal system with $A_s = 50$ m², $Q_{\max} = 5$ m³/s, $\tau_d = 300$ s: $\delta_h = 5 \times 300 / 50 = 30$ cm, which is 3% of a typical 10 m operating range—a much smaller relative margin than the 25% for the dual-tank system.

The relationship between ODD monitoring and robust MPC (specifically tube MPC; Mayne et al., 2005) deserves clarification. Tube MPC tightens constraints internally to guarantee robust feasibility for bounded disturbances—it ensures the state trajectory remains within a "tube" around the nominal trajectory. The ODD monitor operates externally to the MPC as a supervisory layer. The two are complementary: tube MPC handles bounded uncertainties *within* the ODD (i.e., the disturbance set assumed by the robust MPC is a subset of $\mathcal{S}_{\text{env}}$), while the ODD monitor detects scenarios where the plant leaves the assumed disturbance set entirely—events that no robust MPC can guarantee. In this sense, the ODD provides a safety net for the residual risk that lies beyond the robust MPC's design assumptions.

Second, the convex polytope assumption (Eq. 3) is valid when ODD constraints are linear in the state variables. For field-scale systems with nonlinear dynamics (e.g., flow-dependent constraints, backwater effects), the ODD boundary may be non-convex. In such cases, the polytope formulation can be replaced by a union of polytopes or a general nonlinear constraint set, at the cost of increased computational complexity for the $\rho$ evaluation.

__6.2  SiL Verification as a Safety Gate__

The SiL verification demonstrates that systematic boundary testing is essential for safety certification. The 16 nominal scenarios (Groups A–D) all pass with comfortable margins—the minimum $\rho = 0.18$ in S11 is still well within the ODD. It is only the boundary scenarios (Groups E–H) that exercise the safety-critical code paths: the ODD monitor, the fallback protocol, and the Layer 0 interlock. Without boundary testing, these critical functions would remain unverified at the SiL level.

The 100% detection rate (16/16) and the consistent detection latency (1.4 ± 0.4 intervals) provide confidence that the ODD monitor is reliable. The false alarm analysis (§5.6) confirms that sensor noise does not cause spurious VIOLATION triggers, though it can cause transient WARNING events (0.8% with hysteresis). For field-scale systems, the tradeoff between detection sensitivity and false alarm rate can be tuned by adjusting the hysteresis band and the warning threshold $\rho_w$.

__6.3  From SiL to HiL: Expected Additional Challenges__

The SiL verification quantifies code generation fidelity (SiL–MiL difference: 0.1 mm) and ODD monitor accuracy. The next step in the xIL chain—HiL verification on the physical dual-tank platform—will introduce additional challenges:

1. **Sensor noise amplification**: Real ultrasonic sensors exhibit non-Gaussian outliers (~2% of readings) that may trigger spurious ODD warnings. The Kalman filter (Chen et al., 2026a) mitigates this but does not eliminate it entirely. The false alarm analysis (§5.6) provides baseline expectations.

2. **Actuator hysteresis**: The stepper motor driving valve V12 exhibits approximately 1° of backlash, which is not modeled in the SiL. This may cause small oscillations near ODD boundaries, potentially increasing the WARNING false alarm rate.

3. **Timing jitter**: The Arduino Mega 2560 execution time (320 ms worst case) introduces timing uncertainty that is absent in SiL. For the 5-s sampling interval, this 6.4% jitter is acceptable, but it would be more significant at faster sampling rates.

These challenges will be systematically addressed in the companion paper CKG-3 (HiL verification with adaptive MAS).

__6.4  Scaling the ODD Framework__

The 10-pool canal demonstration (§5.7) confirms that the polytope-based ODD formalization scales to realistic systems: 84 constraints evaluated in 0.12 ms with 100% detection accuracy. For even larger systems (50–500 pools), the computational cost remains tractable (Table 1c: 0.6–6 ms on PC). The primary scaling challenge is not computation but the combinatorial growth of boundary scenarios: a 50-pool system would require ~800 boundary scenarios for exhaustive testing, which is feasible but time-consuming. Two mitigation strategies are available: (1) importance sampling, where boundary scenarios are generated based on risk priority (e.g., focusing on the most critical pool-gate combinations), and (2) formal verification using reachability analysis (Althoff, 2021), which can prove safety for entire regions of the state space without enumeration.

__6.5  Comparison with Automotive ODD Practice__

The ODD formalization for water systems differs from automotive ODD in several respects. First, the dynamics are slower (sampling at 5 s vs. 10 ms for autonomous vehicles), providing more time for detection and fallback. Second, the consequence of ODD violation is property damage (flooding, infrastructure damage) rather than loss of life, justifying SIL-1 rather than SIL-3 for the safety interlock (Koopman & Wagner, 2019). Third, the operating environment is more predictable: canal flows are largely deterministic (controlled by upstream gates), unlike the stochastic traffic environment. These differences suggest that water systems may achieve WSAL-3 (conditional autonomy) with less stringent ODD verification than automotive Level 3, provided that adequate safety margins are maintained and Layer 0 hardware interlocks provide a reliable last line of defense.

__6.6  Multi-Agent ODD Composition__

The dual-tank system uses a single Edge Agent controller. For multi-agent systems (the target architecture for field-scale deployments), individual agent ODDs must be composed into a system-level ODD. The system ODD is a subset of the intersection of individual agent ODDs, because coupling constraints (flow conservation at junctions, coordination requirements between adjacent pools) impose additional restrictions beyond individual agent boundaries:

$$
\mathcal{O}_{\text{system}} \subseteq \bigcap_{i=1}^{N} \mathcal{O}_i \cap \mathcal{C}_{\text{coupling}} \tag{14}
$$

where $\mathcal{C}_{\text{coupling}}$ represents inter-agent coupling constraints (e.g., the discharge from pool $i$ must equal the inflow to pool $i+1$). The detailed treatment of multi-agent ODD composition and its implications for decentralized ODD monitoring will be addressed in the companion paper CKG-3.

__6.7  Data-Driven ODD Refinement__

The ODD as defined in §3 is a static polytope with safety margins derived from worst-case analysis. In practice, autonomous systems should refine their ODD boundaries over time as operational data accumulates. We propose a Bayesian framework for safety margin updating.

Let the safety factor SF be treated as an uncertain parameter with prior distribution $\text{SF} \sim \mathcal{N}(\mu_0, \sigma_0^2)$ initialized at $\mu_0 = 1.5$, $\sigma_0 = 0.2$. After each SiL (or HiL) campaign of $N$ boundary scenarios with $k$ observed physical limit violations, the posterior is updated:

$$
p(\text{SF} | k, N) \propto p(k | \text{SF}, N) \cdot p(\text{SF}) \tag{15}
$$

The likelihood model is binomial:

$$
p(k | \text{SF}, N) = \binom{N}{k} \, p_v(\text{SF})^k \, (1 - p_v(\text{SF}))^{N-k} \tag{16}
$$

where $p_v(\text{SF})$ is the violation probability interpolated from Table 9 (e.g., $p_v(1.0) = 3/16 = 0.19$, $p_v(1.25) = 0$, $p_v(1.5) = 0$). If $k = 0$ in $N = 16$ boundary scenarios (as observed), the posterior shifts toward lower SF values, allowing the ODD to expand.

**Proposition 1** (Safety-Preserving ODD Expansion). *If the prior $\text{SF}_0$ satisfies $P(\text{PFD}(\text{SF}_0) < 10^{-1}) > 1 - \epsilon$ and the violation probability $p_v(\text{SF})$ is monotonically decreasing in SF, then the posterior SF after observing $k = 0$ in $N$ scenarios also satisfies the SIL-1 constraint: $P(\text{PFD}(\text{SF}_{\text{post}}) < 10^{-1}) > 1 - \epsilon$.*

*Proof sketch.* Observing $k = 0$ makes the likelihood $p(0 | \text{SF}, N) = (1 - p_v(\text{SF}))^N$, which is monotonically increasing in SF (since $p_v$ is decreasing). The posterior therefore shifts probability mass toward lower SF values. However, the posterior support is bounded below by the prior support. Since PFD is monotonically increasing as SF decreases, and the prior already satisfies the SIL-1 constraint, the posterior—being a convex combination of the prior weighted by a monotone likelihood—also satisfies it. $\square$

After three consecutive campaigns with $k = 0$ ($N = 48$ total), the 95% credible interval for SF contracts to approximately [1.2, 1.6] (posterior variance decreases as $O(1/N)$), permitting a cautious expansion to SF = 1.3 (ODD range [9.0, 41.0] cm, a 7% expansion from the initial [10, 40] cm).

Conversely, if violations are observed (e.g., due to model degradation over time), the posterior shifts toward higher SF values, automatically contracting the ODD. This connects to the safe reinforcement learning framework (Garcia & Fernandez, 2015), where the ODD boundary serves as the constraint set for a Constrained Markov Decision Process (CMDP). The companion paper CKG-3 will implement one full ODD expansion cycle on the physical platform.

__6.8  ODD-Monitored Digital Twin__

The SiL architecture (§4.1) effectively constitutes a digital twin of the dual-tank system: a virtual replica that runs the same control software as the physical system against a calibrated plant model. The addition of ODD monitoring elevates this to a *safety-certified digital twin* (SCDT)—a digital twin that not only replicates system behavior but also continuously monitors operational safety boundaries (Rasheed et al., 2020).

The SCDT provides three capabilities beyond standard digital twins:

1. **Real-time ODD monitoring**: The distance-to-boundary function $\rho(\mathbf{x})$ provides a continuous safety metric that operators can monitor alongside conventional process variables.

2. **Boundary violation prediction**: By running the SiL forward in time (using the MPC's internal prediction horizon $N_p$), the SCDT can predict whether the current trajectory will violate the ODD within the next $N_p \times \Delta t$ seconds, providing advance warning beyond the reactive $\rho$-based detection.

3. **Safety certificate**: The verified scenario set (32 scenarios for dual-tank, 20 for 10-pool) constitutes a formal safety evidence package that can be presented to regulators and operators as part of the WSAL-3 certification dossier.

The SCDT concept aligns with the digital twin roadmap for water networks proposed by Lei et al. (2025b, §5.3), where the digital twin serves as the foundation for autonomous decision-making. The ODD layer adds the missing safety dimension to this vision.

__*[Figure 5 about here]*__

__Broader Impact__

The ODD formalization for water systems contributes to three societal objectives. First, it supports climate adaptation by enabling water infrastructure to operate autonomously under increasingly extreme conditions—the verified ODD defines the boundary of safe autonomous operation and can be systematically expanded as experience accumulates. Second, it aligns with UN Sustainable Development Goal 6 (Clean Water and Sanitation) by reducing operational water losses through more precise and responsive control—preliminary results from the CHS project suggest 2–5% loss reduction with autonomous canal operation. Third, the formal safety framework lowers the barrier to deploying autonomous water control in developing regions, where skilled operators are scarce but water infrastructure demands are growing rapidly.

__7  Conclusions__

This paper has formalized the Operational Design Domain (ODD) for water conveyance systems and developed a systematic SiL verification methodology that combines nominal performance testing with boundary violation detection. The key findings are:

1. The ODD can be formalized as a convex polytope in the joint space of hydraulic states, actuator capabilities, communication status, and environmental disturbances. Safety margins are derived analytically from the IDZ transfer function parameters (Eq. 8–9), with the safety factor selected via sensitivity analysis (Table 9) to balance operational range against robustness.

2. The distance-to-boundary function $\rho(\mathbf{x})$ provides continuous real-time monitoring of ODD proximity. The three-zone classification (NOMINAL/WARNING/VIOLATION) with adaptive recovery and hysteresis filtering ensures safe operation with low false alarm rates (0.0% VIOLATION, 0.8% WARNING).

3. The 32-scenario SiL verification achieves mean RMSE of 1.9 mm within the ODD (all 16 nominal scenarios pass) and 100% ODD violation detection (all 16 boundary violations detected within 1.4 ± 0.4 sampling intervals). No physical limit violations occur in any scenario, confirming the effectiveness of the safety margins and fallback protocol.

4. The ODD framework scales to realistic systems: a 10-pool canal SiL achieves 100% detection (20/20) with 0.12 ms evaluation time. The ODD monitor and IEC 61511-aligned safety architecture provide a practical pathway to WSAL-3 certification.

These results establish the methodological foundation for the WSAL-2→3 transition in water infrastructure: formal ODD specification + systematic SiL verification = verified operating envelope for conditional autonomy. The companion paper CKG-3 will extend this framework to HiL verification on the physical platform and demonstrate adaptive ODD expansion through successive xIL campaigns.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]) and the National Natural Science Foundation of China (Grant Nos. [to be inserted]). The authors thank the CHS laboratory team at Hebei University of Engineering for constructing and instrumenting the dual-tank platform.

__References__

Althoff, M. (2021). *Set-Based Methods for Formal Verification and Controller Synthesis of Autonomous Systems*. Springer. https://doi.org/10.1007/978-3-030-73469-3

BSI. (2020). PAS 1883:2020 — Operational Design Domain (ODD) taxonomy for an automated driving system (ADS). British Standards Institution.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Clemmens, A. J., Kacerek, T. F., Grawitz, B., & Schuurmans, W. (2005). Test cases for canal control algorithms. Journal of Irrigation and Drainage Engineering, 131(6), 502–514. https://doi.org/10.1061/(ASCE)0733-9437(2005)131:6(502)

Czarnecki, K. (2018). Operational Design Domain for automated driving systems: Taxonomy of basic terms. University of Waterloo Report UW-ECE-2018-04.

Dunn, W. R. (2018). *Practical Design of Safety-Critical Computer Systems* (2nd ed.). Reliability Press.

Garcia, J., & Fernandez, F. (2015). A comprehensive survey on safe reinforcement learning. Journal of Machine Learning Research, 16(42), 1437–1480.

Gyllenhammar, M., Johansson, R., Warg, F., Chen, D., Heyn, H.-M., Sanfridson, M., et al. (2020). Towards an operational design domain that supports the safety argumentation of an automated driving system. In Proceedings of the 10th European Congress on Embedded Real Time Systems (ERTS 2020).

Huang, Z., Lei, X., Liu, X., Ji, C., & Wang, H. (2026). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

IEC. (2016). IEC 61511: Functional safety — Safety instrumented systems for the process industry sector. International Electrotechnical Commission.

Koopman, P., & Wagner, M. (2019). Autonomous vehicle safety: An interdisciplinary challenge. IEEE Intelligent Transportation Systems Magazine, 9(1), 90–96. https://doi.org/10.1109/MITS.2016.2583491

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). *Modeling and Control of Hydrosystems*. Springer. https://doi.org/10.1007/978-1-84882-624-3

Mayne, D. Q., Seron, M. M., & Raković, S. V. (2005). Robust model predictive control of constrained linear systems with bounded disturbances. Automatica, 41(2), 219–224. https://doi.org/10.1016/j.automatica.2004.08.019

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Rasheed, A., San, O., & Kvamsdal, T. (2020). Digital twin: Values, challenges and enablers from a modeling perspective. IEEE Access, 8, 21980–22012. https://doi.org/10.1109/ACCESS.2020.2970143

SAE. (2021). SAE J3016:2021 — Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles. SAE International.

Thorn, E., Kimmel, S., & Chaka, M. (2018). A framework for automated driving system testable cases and scenarios. National Highway Traffic Safety Administration Report DOT HS 812 623.

van Overloop, P. J. (2006). *Model Predictive Control on Open Water Systems* (Doctoral dissertation). Delft University of Technology.

__Data Availability__

The ODD specification files, SiL test harness, ODD monitor C code, OpenModelica dual-tank FMU, and all 32-scenario simulation logs are available at https://github.com/IWHR-CHS/dual-tank-odd (to be made public upon acceptance; reviewer access available upon request). An archival snapshot is deposited on Zenodo (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance). Code is released under the MIT license; simulation data under CC-BY-4.0. The repository includes a README with variable descriptions, scenario parameters, and step-by-step reproduction instructions conforming to FAIR data principles.

__Figure Captions__

__Figure 1.__ ODD concept for water systems control. (a) The ODD polytope in the joint space of hydraulic states, actuator capabilities, and disturbances. The green region represents the verified ODD; the yellow annulus is the warning zone; the red boundary marks ODD violation. (b) The WSAL-2→3 transition requires formal ODD specification and xIL verification.

__Figure 2.__ ODD monitor architecture and IEC 61511 alignment. The distance-to-boundary function $\rho(\mathbf{x})$ is evaluated at each sampling instant. Three zones (NOMINAL, WARNING, VIOLATION) trigger corresponding actions. The Layer 0 interlock (SIL-1) provides hardware-level protection independent of the software-based ODD monitor (SIL-0/advisory).

__Figure 3.__ SiL architecture. The OpenModelica plant FMU, auto-generated MPC controller (C code), and ODD monitor are coupled via FMI 2.0 co-simulation. The test harness manages scenario execution, fault injection, and data logging.

__Figure 4.__ Representative SiL verification results. (a) Scenario S17 (level boundary violation): water level trajectory, $\rho$ time series, ODD status transitions (NOMINAL → WARNING → VIOLATION → recovery). (b) Scenario S26 (communication loss): heartbeat-based detection, island-autonomy activation, and recovery. (c) Scenario S31 (combined stressors): multi-dimensional boundary approach. (d) Box plots of detection latency across all 16 boundary scenarios. (e) 10-pool canal boundary detection: example trajectory and $\rho$ evolution for pool 7 (most critical).

__Figure 5.__ ODD visualization in the ($h_1$, $h_2$) plane. Color-coded $\rho$ heatmap: green interior (NOMINAL, $\rho > 0.13$), yellow annulus (WARNING, $0 < \rho \leq 0.13$), red boundary ($\rho = 0$), gray exterior (VIOLATION, $\rho < 0$). Overlaid trajectories: S1 (black, nominal), S11 (orange, near-boundary), S17 (red, violation with recovery arc back into green zone). Physical limits shown as dashed gray rectangle at [5, 45] × [5, 45] cm.
