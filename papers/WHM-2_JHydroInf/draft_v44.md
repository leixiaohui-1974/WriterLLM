*Manuscript prepared for Journal of Hydroinformatics*

__Model-Based Definition to Digital-Twin Deployment for Autonomous Reservoir Operation: A Seven-Layer Engineering Framework and xIL Evidence Chain for Miyun Reservoir__

__Wu Huiming__1, __Xiaohui Lei__2*, __Ji Chen__3, __Chao Wang__2, __Hao Wang__2

1 Project Team for Miyun Reservoir Intelligent Operation, Beijing, China
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

*Corresponding author: Xiaohui Lei (lxh@iwhr.com)*

__Abstract__

Translating validated Model-Based Definition (MBD) assets into operational reservoir digital twins requires a disciplined engineering chain that preserves model semantics, ensures auditable authority transfer, and maintains safety during staged autonomy rollout. This paper presents a seven-layer MBD-to-deployment framework for Miyun Reservoir grounded in the Cybernetics of Hydro Systems (CHS) six-element formulation. The framework couples a unified actuator boundary relation with a model-predictive control objective to structure the migration from laboratory-validated models to control-room-ready operation. An experience-in-the-loop (xIL) evidence chain -- spanning Model-in-the-Loop, Software-in-the-Loop, and Hardware-in-the-Loop stages -- provides staged verification before live pilot deployment. Application to Miyun Reservoir demonstrates that the proposed framework maintains traceability from design intent through operational execution while supporting bounded autonomy under declared operational design domain constraints.

__Keywords__: Miyun Reservoir; Model-Based Definition; digital twin; xIL; autonomous operation; CHS

## 1. Introduction

Reservoir operation increasingly demands integration of physics-based models, real-time control, and digital-twin architectures. However, a persistent deployment gap exists between validated MBD assets developed in research settings and control-room-ready systems that must operate under real disturbances, multi-objective constraints, and human accountability requirements.

This paper addresses the MBD-to-deployment migration problem for reservoir operation. Building on the CHS theoretical baseline (P1a), autonomy governance framework (P2A), and three-agent reservoir decomposition for Miyun (WHM-1), the present work contributes a structured engineering integration that links seven MBD layers to auditable deployment evidence through an xIL verification chain.

## 2. CHS-Consistent Formulation and Notation

The controlled reservoir system is represented using the CHS six-element formulation:

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

where $P$ denotes the physical plant (reservoir-channel system), $A$ the actuator set (gates, valves, pumps), $S$ the sensor network, $D$ the disturbance inputs (inflows, precipitation), $C$ the controller, and $O$ the operational objectives.

Actuator boundary behavior follows the unified relation:

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

where $Q$ [m$^3$/s] is discharge, $H$ [m] is hydraulic head, $u$ [-] is the normalized actuator command, and $\alpha$ [m$^2$/s per unit] characterizes the actuator gain.

## 3. Problem Definition: MBD-to-Deployment Migration

### 3.1 Engineering objective

The MBD-to-deployment migration targets three coupled goals:

1. preserve model semantics from design artifacts to operational artifacts,
2. ensure control authority can be transferred under auditable bounded conditions,
3. maintain safety and service continuity during staged autonomy rollout.

### 3.2 Multi-objective control formulation

For reservoir operation over a prediction horizon $N_p$, the model-predictive control cost function is:

$$
J = \sum_{k=0}^{N_p-1} \left( \|y(k)-r(k)\|_Q^2 + \|\Delta u(k)\|_R^2 + \lambda_s S_{\text{safe}}(k) \right) \tag{3}
$$

where $y(k)$ is the predicted output vector, $r(k)$ is the reference trajectory, $Q$ and $R$ are weighting matrices for tracking error and control effort respectively, and $S_{\text{safe}}(k)$ represents safety-penalty terms for constraint boundary proximity.

## 4. Seven-Layer MBD Engineering Framework

The proposed framework organizes the MBD-to-deployment chain into seven layers:

1. **L1 -- Mission/Policy Layer**: legal and service objectives governing reservoir operation,
2. **L2 -- System Architecture Layer**: reservoir inflow-storage-release structure and subsystem boundaries,
3. **L3 -- Control Strategy Layer**: hierarchical decomposition and agent coordination logic,
4. **L4 -- Executable Model Layer**: simulation-ready dynamic and boundary models with version control,
5. **L5 -- Verification Layer**: MiL/SiL/HiL/xIL campaign assets and acceptance criteria,
6. **L6 -- Operational Interface Layer**: SCADA command, alarm, and fallback pathways,
7. **L7 -- Governance Layer**: signoff, traceability, and release constraints.

Each layer produces version-linked artifacts with checksum records to support reproducibility and audit traceability across the deployment chain.

## 5. Digital-Twin and xIL Verification Path

Deployment progression follows a staged evidence chain with strict promotion gates:

1. **MiL (Model-in-the-Loop)**: validates model structure, scenario generation, and baseline performance against historical data,
2. **SiL (Software-in-the-Loop)**: validates controller software determinism and numerical reproducibility,
3. **HiL/xIL (Hardware/Experience-in-the-Loop)**: validates interface timing, rollback routes, alarm routing, and operator interaction,
4. **Pilot shift operation**: validates bounded live operability within the declared operational design domain (ODD).

Campaign promotion is blocked if any stage lacks traceable evidence identifiers. A four-gate authorization structure (model integrity, determinism, safety, fallback) must be jointly satisfied before bounded authority transfer.

## 6. Miyun Reservoir Application

### 6.1 Site description and operational context

*[To be completed: Miyun Reservoir characteristics, operational objectives, existing SCADA infrastructure, and current decision-support workflow.]*

### 6.2 MBD asset configuration

*[To be completed: specific model configurations for each MBD layer, actuator parameterization, and sensor network mapping for the Miyun system.]*

### 6.3 xIL campaign results

*[To be completed: quantitative results from MiL, SiL, and HiL campaigns including scenario coverage, replay reproducibility statistics, and gate-pass evidence.]*

## 7. Discussion

*[To be completed: interpretation of xIL campaign outcomes, comparison with conventional deployment practices, limitations of the current framework, and implications for broader reservoir digital-twin adoption.]*

## 8. Conclusions

*[To be completed: summary of contributions, key findings from Miyun application, and directions for future work including multi-reservoir extension and real-time learning integration.]*

## Acknowledgments

*[To be completed.]*

## References

*[To be completed.]*
