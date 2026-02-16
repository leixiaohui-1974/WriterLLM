*Manuscript prepared for Journal of Hydroinformatics*

__Model-Based Definition to Digital-Twin Deployment for Autonomous Reservoir Operation: A Seven-Layer Engineering Framework and xIL Evidence Chain for Miyun Reservoir__

__Wu Huiming__1, __Xiaohui Lei__2*, __Ji Chen__3, __Chao Wang__2, __Hao Wang__2

1 Project Team for Miyun Reservoir Intelligent Operation, Beijing, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

*Corresponding author: Xiaohui Lei (lxh@iwhr.com)*

__Abstract__

This initial draft develops WHM-2 as the B4 engineering-integration paper on Model-Based Definition (MBD) migration from laboratory validation to reservoir-scale digital-twin deployment for Miyun Reservoir. Consistent with Cybernetics of Hydro Systems (CHS), the manuscript adopts the six-element formulation $\Sigma=(P,A,S,D,C,O)$, unified actuator boundary relation, and model-layer/control-layer consistency constraints inherited from P1a, P2A, and WHM-1. The contribution focus is deployment discipline: translating seven-layer MBD assets into auditable operational artifacts, linking xIL evidence to SCADA authority pathways, and defining bounded autonomy governance for reservoir operation. This version establishes scope, notation, and staged verification protocol; quantitative field statistics will be added in subsequent iterations.

__Keywords__: Miyun Reservoir; Model-Based Definition; digital twin; xIL; autonomous operation; CHS

## 1. Introduction

WHM-2 addresses the deployment gap between validated MBD assets and control-room-ready reservoir operation under real disturbances, multi-objective constraints, and human accountability requirements.

Following CHS baseline positioning, WHM-2 is an engineering governance paper rather than a new theorem paper:

- theory baseline from P1a (model hierarchy and actuator characteristic),
- autonomy governance baseline from P2A (HDC/ODD/MAS and WSAL framing),
- reservoir-agent baseline from WHM-1 (three-agent decomposition for Miyun).

## 2. CHS-consistent formulation and notation lock

The controlled system is represented as:

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

Actuator boundary behavior uses the unified relation:

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

Symbols follow shared CHS conventions: $Q$ [m$^3$/s], $H$ [m], $u$ [-], and $\alpha$ [m$^2$/s per unit].

## 3. Problem definition: MBD-to-deployment migration for reservoir operation

### 3.1 Engineering objective

WHM-2 targets three coupled goals:

1. preserve model semantics from design artifacts to operation artifacts,
2. ensure control authority can be transferred under auditable bounded conditions,
3. maintain safety and service continuity during staged autonomy rollout.

### 3.2 Initial multi-objective structure

For reservoir operation stage $k$, initial cost structure is defined as:

$$
J = \sum_{k=0}^{N_p-1} \left( \|y(k)-r(k)\|_Q^2 + \|\Delta u(k)\|_R^2 + \lambda_s S_{\text{safe}}(k) \right) \tag{3}
$$

where $S_{\text{safe}}(k)$ represents safety-penalty terms for boundary proximity; weighting calibration is deferred to later iterations.

## 4. Seven-layer MBD engineering chain for Miyun

WHM-2 adopts a seven-layer chain from intent to deployment evidence:

1. **L1 Mission/Policy Layer**: legal and service objectives,
2. **L2 System Architecture Layer**: reservoir inflow-storage-release structure,
3. **L3 Control Strategy Layer**: HDC and agent coordination logic,
4. **L4 Executable Model Layer**: simulation-ready dynamic and boundary models,
5. **L5 Verification Layer**: MiL/SiL/HiL/xIL campaign assets,
6. **L6 Operational Interface Layer**: SCADA command, alarm, and fallback pathways,
7. **L7 Governance Layer**: signoff, traceability, and release constraints.

Each layer outputs version-linked artifacts and checksum records to support reproducibility.

## 5. Digital-twin and xIL verification path

Deployment progression is constrained by staged evidence:

1. **MiL** validates model structure and scenario generation,
2. **SiL** validates controller software determinism,
3. **HiL/xIL** validates interface timing, rollback route, and alarm routing,
4. **Pilot shift operation** validates bounded live operability within declared ODD.

Campaign promotion is blocked if any stage lacks traceable evidence identifiers.

## 6. Initial governance gate set (iteration-0 skeleton)

A four-gate skeleton is defined for operational promotion:

- **G1 Model integrity**: MBD artifacts and executable models are version-consistent,
- **G2 Determinism**: replay outputs are reproducible under fixed build identifiers,
- **G3 Safety**: no unresolved hard-constraint violation in xIL scenarios,
- **G4 Fallback**: downgrade/rollback path verified in bounded response time.

Only when all gates pass can bounded authority transfer be considered.

## 7. Scope boundary and cross-paper differentiation

WHM-2 does not claim:

- new CHS dynamics theorem (covered by P1a),
- new WSAL taxonomy (covered by P2A),
- first reservoir-agent decomposition (covered by WHM-1).

WHM-2 claims an integration contribution: **seven-layer MBD migration + digital-twin xIL evidence chain + auditable deployment governance for Miyun Reservoir**.

## 8. Iteration-0 to iteration-1 plan

Next iteration will add:

1. explicit ODD envelope variables and violation handling policy,
2. MBD layer-to-artifact traceability table for audit packaging,
3. Reviewer-B-oriented control-room operability checklist for shift execution.

## 9. Reviewer-B driven operability refinements (iteration 1)

### 9.1 ODD envelope and deterministic violation policy

To convert iteration-0 skeleton into shift-executable constraints, WHM-2 defines an explicit ODD envelope:

- reservoir-state envelope: $H_{\min} \le H(t) \le H_{\max}$ and release bounds $Q_{\min} \le Q(t) \le Q_{\max}$,
- telemetry envelope: data age $\le T_{\text{stale,max}}$ and command/feedback latency $\le T_{\text{lat,max}}$,
- authority envelope: command increments must remain compatible with L0/L1 hard safety logic.

Violation policy is non-compensable:

1. hard state-bound violation triggers immediate `DOWNGRADE` to assisted operation,
2. telemetry envelope violation blocks authority promotion and forces checklist requalification,
3. re-entry requires refreshed xIL evidence under unchanged build/version identifiers.

### 9.2 MBD artifact-to-shift traceability minimum set

Reviewer-B requested concrete control-room traceability. WHM-2 defines the minimal immutable package per shift window:

- `model_bundle_id`,
- `controller_build_id`,
- `scenario_hash`,
- `replay_hash`,
- `alarm_trace_id`,
- `rollback_test_id`.

Any missing artifact invalidates release readiness even if optimization performance is improved.

### 9.3 Shift execution checklist for SCADA operability

Before bounded authority transfer, operators must complete a signed checklist:

1. ODD envelope confirmation for current hydrologic and telemetry conditions,
2. rollback path test in active SCADA topology within declared response bound,
3. unresolved Class A/B alarm disposition recorded,
4. authority handover signed by duty engineer and shift supervisor,
5. package IDs archived in immutable release note.

These additions bind MBD migration to practical control-room execution and directly address Reviewer-B operability concerns.
