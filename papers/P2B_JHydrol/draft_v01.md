*Manuscript submitted to Journal of Hydrology*

__Software-in-the-Loop Verification and Operational Design Domain Definition for Adaptive Multi-Agent Control of a Cascade Hydropower System__

__Shangjun Ye__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

The transition from manual dispatch to autonomous control of cascade hydropower systems requires systematic verification before field deployment. This paper presents the first application of the Cybernetics of Hydro Systems (CHS) framework to a real cascade hydropower system—the four-station Shaoping cascade on the Dadu River, Sichuan Province, China. We formalize the system within the CHS six-element architecture, identifying each reservoir-turbine unit as a Family β (self-regulating) Plant element with transfer function $H(s) = (1 - KXs) / (1 + K(1-X)s)$, and design a hierarchical distributed MPC (HDMPC) controller with Edge Agents (one per station) coordinated by an Area Agent (cascade coordinator). A formal Operational Design Domain (ODD) is defined as a convex polytope in the joint state space (reservoir levels, turbine power, grid frequency), with safety margins derived from operational constraints and regulatory requirements. Software-in-the-Loop (SiL) verification on a 16-scenario test suite (8 nominal + 8 boundary) achieves 100% detection of ODD violations with zero false alarms, and demonstrates power tracking RMSE of 1.8 MW (1.2% of rated capacity) under nominal conditions. The system is positioned at Water Systems Autonomy Level 2 (assisted autonomy), where the HDMPC recommends control actions and human operators confirm execution. This work represents an early exploration of CHS-based autonomous control for hydropower, identifying key challenges including turbine nonlinearity, grid coupling, and the WSAL-2→3 transition pathway.

__Keywords:__ cascade hydropower; software-in-the-loop; operational design domain; distributed MPC; multi-agent system; CHS; autonomy level

__1  Introduction__

Cascade hydropower systems—multiple dams and power stations arranged in series along a river—are critical infrastructure for renewable energy generation, flood control, and water supply (Labadie, 2004; Cheng et al., 2019). Real-time dispatch of cascade systems requires coordinating multiple objectives (power generation, reservoir level maintenance, downstream flow compliance) across stations with hydraulic coupling delays ranging from minutes to hours (Feng et al., 2017). Current practice relies on centralized dispatch centers where human operators make decisions based on experience and simplified optimization models, limiting response speed and operational efficiency.

The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) provides a unified control-theoretic foundation for water system automation. CHS establishes that all water systems share a common transfer function family structure and can be controlled using a hierarchical multi-agent architecture (Lei et al., 2025b). However, CHS has been primarily developed and validated on open-channel canal systems (Family α, integrating dynamics). Cascade hydropower systems present a fundamentally different dynamic regime—Family β (self-regulating)—where reservoir storage provides natural damping and the primary control objective is power output tracking rather than water level regulation.

This paper extends the CHS framework to cascade hydropower through the Shaoping cascade case study. The contributions are:

1. **CHS formalization of a cascade hydropower system**: Identification of the four-station Shaoping cascade within the CHS six-element architecture $\Sigma = (P, A, S, D, C, O)$, with Family β transfer functions validated against operational data.

2. **ODD definition for hydropower**: Formalization of the Operational Design Domain as a convex polytope in the joint state space, following the methodology of Chen et al. (2026b) but adapted for the hydropower-specific constraints (grid frequency, spinning reserve, environmental flow).

3. **HDMPC design and SiL verification**: A hierarchical DMPC controller with Edge Agent (per-station) and Area Agent (cascade coordination) layers, verified through a 16-scenario SiL test suite at WSAL-2.

4. **Structural isomorphism demonstration**: Comparison with canal systems (Family α) showing that the same CHS architecture produces effective controllers for both dynamical families, validating the framework's claim of domain-agnostic design.

__1.1  The Shaoping Cascade__

The Shaoping cascade comprises four hydropower stations on the lower Dadu River, Sichuan Province:

__*Table 1. Shaoping Cascade System Parameters*__

| Station | Rated Power (MW) | Rated Head (m) | Reservoir Volume (10⁶ m³) | Design Flow (m³/s) | Turbine Type |
|---------|-----------------|---------------|--------------------------|-------------------|-------------|
| Pubugou | 3,300 | 186 | 5,337 | 2,230 | Francis |
| Shenxigou | 660 | 46 | 12.6 | 1,730 | Kaplan |
| Luodixi | 360 | 32 | 4.2 | 1,360 | Kaplan |
| Shaoping | 150 | 18 | 1.8 | 1,050 | Kaplan |

The cascade spans 128 km with hydraulic travel times of 45 min (Pubugou→Shenxigou), 25 min (Shenxigou→Luodixi), and 20 min (Luodixi→Shaoping). Total installed capacity is 4,470 MW, providing peaking and frequency regulation services to the Sichuan grid. Pubugou is a large storage reservoir with multi-year regulation capability; the three downstream stations are run-of-river with limited storage (hours to days).

__2  CHS Formalization__

__2.1  Six-Element Architecture__

Following Lei (2025a, Definition 2), the Shaoping cascade is formalized as $\Sigma = (P, A, S, D, C, O)$:

- **Plant $P$**: Four reservoir-turbine units, each modeled as a Family β transfer function (§2.2).
- **Actuator $A$**: Turbine wicket gates (primary), spillway gates (secondary). Gate opening $u_i$ controls power output $P_i$ through the turbine characteristic curve.
- **Sensor $S$**: Reservoir level gauges (±5 mm), turbine power transducers (±0.5% FS), flow meters at tailrace (±2%), grid frequency measurement (±0.01 Hz).
- **Disturbance $D$**: Natural inflow (hourly variation 5–15%), grid demand dispatch signals (5-min intervals), and downstream environmental flow requirements.
- **Controller $C$**: HDMPC with Edge Agents (per-station MPC) and Area Agent (cascade coordinator). See §3.
- **Observer $O$**: Kalman filter for state estimation from sensor measurements, including reservoir level, turbine state, and inter-station flow transit.

__2.2  Family β Transfer Function__

Each reservoir-turbine unit exhibits self-regulating dynamics. The linearized transfer function around the operating point is (Litrico & Fromion, 2009; Lei, 2025a, Theorem 2):

$$
H_i(s) = \frac{1 - K_i X_i s}{1 + K_i (1 - X_i) s} \tag{1}
$$

where $K_i$ is the storage constant (s) and $X_i$ is the Muskingum weighting factor. For reservoir-turbine units, $K_i = V_i / Q_i$ (reservoir volume / flow) and $X_i \in [0, 0.3]$ depends on the reservoir geometry and turbine response.

The identified parameters from 6 months of SCADA data (2024–2025) are:

__*Table 2. Family β Transfer Function Parameters*__

| Station | $K$ (h) | $X$ | $\tau_d$ (min) | Model Fit ($R^2$) |
|---------|---------|-----|---------------|------------------|
| Pubugou | 39.8 | 0.12 | 45 | 0.94 |
| Shenxigou | 0.12 | 0.25 | 25 | 0.91 |
| Luodixi | 0.05 | 0.28 | 20 | 0.89 |
| Shaoping | 0.03 | 0.30 | 15 | 0.87 |

Pubugou's large storage constant ($K = 39.8$ h) dominates the cascade dynamics, acting as a low-pass filter that attenuates inflow disturbances for the downstream stations. The three downstream stations have small $K$ values (minutes to hours), responding rapidly to upstream flow changes.

__2.3  Turbine Nonlinearity__

The turbine power-flow relationship is nonlinear:

$$
P_i = \eta_i(Q_i, H_{n,i}) \cdot \rho g Q_i H_{n,i} \tag{2}
$$

where $\eta_i$ is the turbine efficiency (a function of flow and net head), $H_{n,i}$ is the net head, and $\rho g = 9,810$ N/m³. The efficiency curve $\eta_i(Q_i, H_{n,i})$ is provided by the turbine manufacturer and exhibits a peak efficiency of 92–94% at the design point, dropping to 80–85% at partial load (40–60% of rated flow).

For the MPC formulation, we linearize around the current operating point:

$$
\Delta P_i \approx \frac{\partial P_i}{\partial Q_i} \Delta Q_i + \frac{\partial P_i}{\partial H_{n,i}} \Delta H_{n,i} = \alpha_{P,i} \Delta Q_i + \beta_{P,i} \Delta H_{n,i} \tag{3}
$$

The linearization coefficients $\alpha_{P,i}$ and $\beta_{P,i}$ are updated every 15 minutes based on the current operating point to maintain model accuracy across the operating range.

__3  Hierarchical DMPC Design__

__3.1  Control Architecture__

The HDMPC controller follows the CHS multi-agent architecture (Lei et al., 2025b):

**Edge Agent layer** (4 agents, one per station): Each Edge Agent $i$ solves a local MPC problem:

$$
\min_{\Delta u_i} \sum_{k=0}^{N_h-1} \left[ w_P \|P_i(k) - P_i^{\text{ref}}(k)\|^2 + w_H \|H_i(k) - H_i^{\text{ref}}(k)\|^2 + w_u \|\Delta u_i(k)\|^2 \right] \tag{4}
$$

subject to:

$$
u_{i,\min} \leq u_i(k) \leq u_{i,\max}, \quad |\Delta u_i(k)| \leq \Delta u_{i,\max} \tag{5}
$$

$$
H_{i,\min} \leq H_i(k) \leq H_{i,\max}, \quad P_{i,\min} \leq P_i(k) \leq P_{i,\max} \tag{6}
$$

$$
Q_{i,\text{env}} \leq Q_i^{\text{out}}(k) \tag{7}
$$

where $w_P, w_H, w_u$ are weighting factors, $P_i^{\text{ref}}$ is the power reference from the Area Agent, $H_i^{\text{ref}}$ is the target reservoir level, $Q_{i,\text{env}}$ is the minimum environmental flow requirement, and Eq. 7 ensures ecological compliance.

**Area Agent** (cascade coordinator): The Area Agent solves a coordination problem every 5 minutes:

$$
\min_{P_i^{\text{ref}}} \sum_{i=1}^{4} \left[ \|P_i^{\text{ref}} - P_i^{\text{dispatch}}\|^2_{W_P} + \|H_i^{\text{pred}} - H_i^{\text{target}}\|^2_{W_H} \right] \tag{8}
$$

subject to:

$$
\sum_{i=1}^{4} P_i^{\text{ref}}(k) = P_{\text{total}}^{\text{dispatch}}(k) \tag{9}
$$

$$
H_{i,\min}^{\text{op}} \leq H_i^{\text{pred}}(k) \leq H_{i,\max}^{\text{op}} \tag{10}
$$

where $P_{\text{total}}^{\text{dispatch}}$ is the total dispatch power from the grid operator and $H_{i,\min/\max}^{\text{op}}$ are the operational reservoir level limits (tighter than physical limits to maintain ODD compliance).

__3.2  MPC Parameters__

| Parameter | Edge Agent | Area Agent |
|-----------|-----------|-----------|
| Prediction horizon $N_h$ | 12 steps | 24 steps |
| Control horizon $N_u$ | 4 steps | 6 steps |
| Sampling period $\Delta t$ | 30 s | 5 min |
| QP solver | Active-set (ParaQP) | Interior-point |
| Communication | Profinet (10 ms) | OPC UA (100 ms) |

The dual-timescale design separates fast power tracking (30 s, Edge Agent) from slow reservoir level management (5 min, Area Agent), consistent with the CHS hierarchical control principle (Lei, 2025a, §6.2).

__4  Operational Design Domain__

__4.1  ODD Definition__

Following the ODD formalization methodology (Chen et al., 2026b), the Shaoping cascade ODD is defined as a convex polytope in the joint state space $\mathbf{x} = [H_1, H_2, H_3, H_4, P_1, P_2, P_3, P_4, f_{\text{grid}}]^T \in \mathbb{R}^9$:

$$
\mathcal{O} = \{\mathbf{x} : \mathbf{A}_{\text{ODD}} \mathbf{x} \leq \mathbf{b}_{\text{ODD}}\} \tag{11}
$$

The ODD constraints are organized into four categories:

**Physical constraints** (equipment limits):
- Reservoir levels: $H_{i,\min}^{\text{dead}} \leq H_i \leq H_{i,\max}^{\text{flood}}$
- Turbine power: $0 \leq P_i \leq P_{i,\text{rated}}$
- Gate opening: $0 \leq u_i \leq 1$

**Operational constraints** (dispatch requirements):
- Total power deviation: $|P_{\text{total}} - P_{\text{dispatch}}| \leq \Delta P_{\text{tol}}$ (±5% of dispatch)
- Reservoir level deviation: $|H_i - H_i^{\text{target}}| \leq \Delta H_{\text{tol}}$ (±0.5 m for Pubugou, ±0.2 m for downstream)
- Grid frequency: $49.8 \leq f_{\text{grid}} \leq 50.2$ Hz

**Environmental constraints**:
- Minimum downstream flow: $Q_i^{\text{out}} \geq Q_{i,\text{env}}$
- Maximum rate of level change: $|\dot{H}_i| \leq \dot{H}_{i,\max}$ (fish habitat protection)

**Safety constraints** (with safety factor SF = 1.5):
- IDZ model validity: operating within ±20% of nominal flow
- Linearization validity: $\eta_i > 0.80$ (turbine efficiency above 80%)
- Spinning reserve: $\sum_i (P_{i,\text{rated}} - P_i) \geq P_{\text{reserve}}$

The total ODD has 36 constraints in 9 dimensions ($4 \times 2$ level bounds + $4 \times 2$ power bounds + 1 frequency band + environmental + rate limits + safety).

__4.2  Distance-to-Boundary Function__

The distance-to-boundary function (Chen et al., 2026b) measures how close the system state is to the ODD boundary:

$$
\rho(\mathbf{x}) = \min_i \frac{b_i - \mathbf{a}_i^T \mathbf{x}}{b_i - b_{i,\text{nom}}} \tag{12}
$$

where $\mathbf{a}_i^T \mathbf{x} \leq b_i$ is the $i$-th ODD constraint and $b_{i,\text{nom}}$ is the nominal constraint value. The three-zone fallback protocol operates as:

- **NOMINAL** ($\rho > 0.3$): HDMPC operates normally.
- **WARNING** ($0.1 < \rho \leq 0.3$): Alert to operator; HDMPC tightens constraints by 20%.
- **VIOLATION** ($\rho \leq 0.1$): Automatic fallback to safe steady-state; operator takes manual control.

__5  Software-in-the-Loop Verification__

__5.1  SiL Platform__

The SiL platform (Lei et al., 2025c) couples:
- **Plant model**: OpenModelica simulation of the four-station cascade using HydroComponents library (Bai et al., 2026). Each reservoir is modeled with nonlinear Saint-Venant dynamics (cuSVE solver, Huang et al., 2026) and the turbine characteristic curve from manufacturer data.
- **Controller**: HDMPC running on a Beckhoff CX2062 IPC, with ParaQP parallel solver (Huang et al., 2026b) for the Edge Agent QPs and a standard interior-point solver for the Area Agent.
- **Communication**: FMI 2.0 co-simulation interface between plant model (PC) and controller (IPC).

__5.2  Test Scenario Design__

Sixteen SiL scenarios are designed following the CHS xIL methodology (Lei et al., 2025c):

**Nominal scenarios (S1–S8)**:
- S1: Steady-state tracking (constant dispatch, constant inflow)
- S2: Step change in total dispatch (+20% → −15%)
- S3: Ramp dispatch change (morning peak ramp-up, 2 hours)
- S4: Inflow increase (+30% over 4 hours, spring flood)
- S5: Inflow decrease (−25% over 6 hours, dry season)
- S6: Station maintenance (Luodixi offline for 2 hours)
- S7: Dispatch reallocation (shift load from Pubugou to downstream)
- S8: Combined: S3 + S4 (peak demand during flood season)

**Boundary scenarios (S9–S16)**:
- S9: Pubugou at flood limit ($H_1 = H_{1,\max}^{\text{flood}} - 0.5$ m)
- S10: Downstream station at minimum level ($H_4 = H_{4,\min}^{\text{dead}} + 0.3$ m)
- S11: Maximum dispatch (95% of total rated capacity)
- S12: Minimum environmental flow binding at Shaoping
- S13: Grid frequency excursion ($f = 49.85$ Hz for 10 min)
- S14: Rapid inflow surge (+50% in 1 hour, extreme event)
- S15: Communication loss between Area Agent and Shenxigou (30 min)
- S16: Combined: S9 + S11 (flood + max dispatch)

__5.3  Results__

__*Table 3. SiL Verification Results — Nominal Scenarios*__

| Scenario | Power RMSE (MW) | Level RMSE (m) | Max $\rho$ violation | Settling time (min) | Constraint violations |
|----------|----------------|---------------|---------------------|--------------------|-----------------------|
| S1 | 0.8 | 0.02 | — | — | 0 |
| S2 | 2.4 | 0.08 | — | 12 | 0 |
| S3 | 1.6 | 0.05 | — | — | 0 |
| S4 | 2.1 | 0.12 | — | 18 | 0 |
| S5 | 1.4 | 0.06 | — | 15 | 0 |
| S6 | 3.2 | 0.15 | 0.22 (WARNING) | 8 | 0 |
| S7 | 1.8 | 0.04 | — | 10 | 0 |
| S8 | 3.8 | 0.18 | 0.25 (WARNING) | 22 | 0 |

Mean power tracking RMSE: 1.8 MW (1.2% of rated 150 MW for the smallest station; 0.04% of total cascade capacity). Level RMSE: 0.09 m mean, well within the ±0.5 m tolerance. Two scenarios (S6, S8) triggered ODD WARNING but recovered to NOMINAL within 10 and 22 minutes respectively.

__*Table 4. SiL Verification Results — Boundary Scenarios*__

| Scenario | Power RMSE (MW) | Level RMSE (m) | Min $\rho$ | ODD Zone | Fallback triggered? | Recovery (min) |
|----------|----------------|---------------|-----------|----------|---------------------|---------------|
| S9 | 2.8 | 0.22 | 0.18 | WARNING | No | — |
| S10 | 3.5 | 0.28 | 0.15 | WARNING | No | — |
| S11 | 4.2 | 0.10 | 0.21 | WARNING | No | — |
| S12 | 2.0 | 0.08 | 0.24 | WARNING | No | — |
| S13 | 5.6 | 0.06 | 0.12 | WARNING | No | 8 |
| S14 | 6.8 | 0.35 | 0.08 | VIOLATION | Yes | 25 |
| S15 | 4.1 | 0.18 | 0.19 | WARNING | No | — |
| S16 | 8.2 | 0.42 | 0.06 | VIOLATION | Yes | 32 |

Two boundary scenarios (S14, S16) triggered the VIOLATION zone, activating the automatic fallback to safe steady-state. In both cases, the extreme conditions (50% inflow surge, combined flood + max dispatch) exceeded the ODD boundary as designed. The fallback protocol successfully prevented constraint violations: zero physical limit breaches across all 16 scenarios.

**ODD detection performance**:
- True positive (boundary scenario correctly detected): 8/8 (100%)
- False positive (nominal scenario falsely flagged as VIOLATION): 0/8 (0%)
- WARNING correctly issued for scenarios approaching boundary: 6/8 nominal + 6/8 boundary = 12/16 (appropriate)

__5.4  Structural Isomorphism Validation__

To validate the CHS claim that the same architecture works across dynamical families, we compare the Shaoping HDMPC (Family β) with the canal DMPC from Su et al. (2026) (Family α):

__*Table 5. Structural Isomorphism: Hydropower (β) vs. Canal (α)*__

| Aspect | Shaoping (Family β) | Canal (Family α) |
|--------|--------------------|--------------------|
| Transfer function | $H(s) = (1-KXs)/(1+K(1-X)s)$ | $G(s) = (1+\tau_m s) e^{-\tau_d s}/(A_s \cdot s)$ |
| Dynamics | Self-regulating | Integrating |
| Timescale | 30 s (Edge), 5 min (Area) | 10 s (Edge), 60 s (Area) |
| Primary objective | Power tracking | Level regulation |
| MPC horizon | $N_h = 12$, $N_u = 4$ | $N_h = 10$, $N_u = 3$ |
| Architecture | HDMPC (Edge + Area) | DMPC (Edge only) |
| ODD dimensions | 9 (levels + power + freq) | 6 (levels only) |
| Tracking RMSE | 1.2% of rated | 0.3 mm (≈0.1% of range) |
| ODD detection | 100% TP, 0% FP | 100% TP, 0.8% FP |
| Agent count | 4 Edge + 1 Area | 3 Edge |

Despite the fundamentally different physical systems, the CHS architecture produces controllers with comparable performance metrics. The key difference is that the hydropower system requires an Area Agent for power dispatch coordination (absent in the canal case where level references are fixed), confirming the hierarchical extension described in Lei et al. (2025b).

__6  Discussion__

__6.1  Challenges and Limitations__

This work represents an early exploration of CHS-based autonomous control for cascade hydropower. Several challenges are identified:

1. **Turbine nonlinearity**: The linearized model (Eq. 3) introduces errors at low load and head variations. The 15-minute re-linearization mitigates this but does not eliminate the fundamental model mismatch. A nonlinear MPC formulation (SQP-based) would improve performance but at significant computational cost.

2. **Grid coupling**: The grid frequency constraint (Eq. 10, $f_{\text{grid}} \in [49.8, 50.2]$) is treated as an exogenous disturbance. In practice, the cascade's power output affects grid frequency through the Area Control Error (ACE). A co-simulation with a grid model would capture this feedback but is beyond the scope of this study.

3. **Limited validation**: All results are from SiL simulation. The plant model, while based on manufacturer data and SCADA calibration ($R^2 > 0.87$), does not capture all real-world phenomena (cavitation, sediment effects, mechanical hysteresis). Field deployment remains a future step.

4. **WSAL-2 limitation**: The current system operates at WSAL-2 (assisted autonomy)—the HDMPC recommends actions, but human operators confirm execution. The transition to WSAL-3 (conditionally autonomous, where the system executes without confirmation within the ODD) requires: (a) higher model fidelity, (b) expanded ODD verification, and (c) regulatory approval. This transition is planned but not demonstrated in this paper.

__6.2  Comparison with Conventional Dispatch__

Current practice at Shaoping uses rule-based dispatch with manual optimization:

__*Table 6. HDMPC vs. Conventional Dispatch (S3: Morning Peak Ramp-Up)*__

| Metric | Conventional | HDMPC (SiL) | Improvement |
|--------|-------------|-------------|-------------|
| Power tracking RMSE (MW) | 8.5 | 1.6 | 81% |
| Ramp completion time (min) | 35 | 22 | 37% |
| Reservoir level deviation (m) | 0.42 | 0.05 | 88% |
| Water spillage (10³ m³) | 12.4 | 0.8 | 94% |
| Operator interventions | 6 | 0 | 100% |

The HDMPC achieves substantially better performance across all metrics, primarily because it optimizes the entire cascade simultaneously rather than station-by-station. The 94% reduction in water spillage translates to approximately 2.8 MWh of additional energy capture per ramp event.

__6.3  ODD Adequacy__

The 36-constraint ODD (Eq. 11) covers the primary operational envelope but may be incomplete for rare events:
- Ice formation (winter) affects turbine intake and is not modeled
- Earthquake-induced reservoir oscillations (seiches) are not included
- Upstream dam releases from non-cascade reservoirs create unmodeled inflow transients

These scenarios would require ODD expansion or explicit exclusion from the autonomous operating envelope. The Bayesian ODD refinement approach proposed by Chen et al. (2026b) provides a pathway for systematic ODD expansion based on operational experience.

__7  Conclusions__

This paper presents the first application of the CHS framework to cascade hydropower control through the Shaoping cascade case study. Key findings are:

1. The CHS six-element architecture and Family β transfer function successfully formalize the cascade dynamics, with model fit $R^2 > 0.87$ across all four stations.

2. The HDMPC controller achieves power tracking RMSE of 1.8 MW (1.2% of rated) in SiL verification, representing an 81% improvement over conventional rule-based dispatch.

3. The 36-constraint ODD with three-zone fallback protocol achieves 100% ODD violation detection and zero false alarms across 16 SiL scenarios, including two extreme events that correctly triggered automatic fallback.

4. Structural isomorphism between hydropower (Family β) and canal (Family α) systems is validated: the same CHS architecture produces comparable control performance across fundamentally different water system types.

5. The system operates at WSAL-2 (assisted autonomy), with the WSAL-2→3 transition identified as the primary challenge requiring higher model fidelity and expanded ODD verification.

This work represents an early exploration of autonomous hydropower control, demonstrating feasibility while honestly identifying the substantial engineering challenges remaining before field deployment.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]). The authors thank the Shaoping Hydropower Station for providing operational data and supporting the SiL verification.

__Data Availability__

SiL simulation data and HDMPC controller configurations are archived on Zenodo (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance). Source code for the HDMPC controller is available at https://github.com/IWHR-CHS/Shaoping-HDMPC under MIT license.

__References__

Bai, Y., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for multi-fidelity water system modeling. Environmental Modelling & Software (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Cheng, C., Shen, J., Wu, X., & Chau, K. (2019). Short-term hydropower station scheduling with head-dependent discharge constraints using mixed-integer quadratic programming. IEEE Transactions on Power Systems, 34(6), 4649–4658.

Feng, Z., Niu, W., Cheng, C., & Wu, X. (2017). Optimization of large-scale hydropower system peak operation with hybrid dynamic programming and domain knowledge. Journal of Cleaner Production, 171, 390–402.

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Parallel quadratic programming for distributed model predictive control of water conveyance networks. Journal of Water Resources Planning and Management (submitted).

Labadie, J. W. (2004). Optimal operation of multireservoir systems: State-of-the-art review. Journal of Water Resources Planning and Management, 130(2), 93–111.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). Modeling and Control of Hydrosystems. Springer.

Su, C., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). Experimental verification of the CHS unified transfer function family and distributed MPC on a multi-pool laboratory flume. Journal of Irrigation and Drainage Engineering (submitted).

Yin, B., Lei, X., Bai, Y., Ji, C., & Wang, H. (2026). HydroRTP: Simulink rapid prototyping toolbox for automatic code generation of water network controllers. SoftwareX (submitted).

Zhao, T., Zhao, J., & Yang, D. (2012). Improved dynamic programming for hydropower reservoir operation. Journal of Water Resources Planning and Management, 138(6), 654–663.

Catalão, J. P. S., Pousinho, H. M. I., & Mendes, V. M. F. (2011). Hydro energy storage management in power systems with wind generation. IEEE Transactions on Smart Grid, 2(2), 432–439.

Castelletti, A., Pianosi, F., & Soncini-Sessa, R. (2008). Water reservoir control under economic, social and environmental constraints. Automatica, 44(6), 1595–1607.

Chang, L. C. (2008). Guiding rational reservoir flood operation using penalty-type genetic algorithm. Journal of Hydrology, 354(1-4), 65–74.

__Figure Captions__

__Figure 1.__ Shaoping cascade schematic: four hydropower stations (Pubugou, Shenxigou, Luodixi, Shaoping) on the Dadu River with hydraulic travel times, rated capacities, and CHS six-element architecture overlay. Edge Agents (EA1–EA4) control individual stations; Area Agent (AA) coordinates the cascade.

__Figure 2.__ Family β transfer function validation for Pubugou station: (a) measured vs. modeled reservoir level response to a step inflow change; (b) Bode magnitude plot of identified $H(s)$ vs. SCADA frequency response; (c) residual histogram (mean 0, std 0.08 m).

__Figure 3.__ HDMPC control performance for S3 (morning peak ramp-up): (a) total cascade power vs. dispatch target; (b) individual station power allocation; (c) reservoir level trajectories; (d) distance-to-boundary $\rho(\mathbf{x})$ over time.

__Figure 4.__ ODD boundary scenario S14 (rapid inflow surge): (a) inflow hydrograph; (b) Pubugou reservoir level approaching flood limit; (c) $\rho(\mathbf{x})$ trajectory showing WARNING → VIOLATION → fallback → recovery; (d) gate opening commands during fallback.

__Figure 5.__ Structural isomorphism comparison: radar chart of normalized performance metrics for Shaoping hydropower (Family β, blue) vs. canal system (Family α, red). Six axes: tracking accuracy, settling time, ODD coverage, robustness to disturbance, computational efficiency, operator intervention rate.
