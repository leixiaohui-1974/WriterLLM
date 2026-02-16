*Manuscript prepared for Journal of Hydroinformatics*

__Energy-Aware Hierarchical Distributed MPC with Digital-Twin xIL for the Jiaodong Water Transfer System: A CHS-Governed Deployment Framework__

__Liu Xiaowei__1, __Xiaohui Lei__1,2*, __Ji Chen__3, __Chao Wang__2, __Yang Minghan__2, __Jin Pengyu__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

*Corresponding author: Xiaohui Lei (lxh@iwhr.com)*

__Abstract__

This initial draft develops P2D as the B4 engineering paper on energy-efficiency optimization and digital-twin xIL deployment for the Jiaodong water transfer system. Consistent with Cybernetics of Hydro Systems (CHS), the manuscript adopts the six-element formulation $\Sigma=(P,A,S,D,C,O)$, the unified actuator boundary relation, and model-layer/control-layer matching rules inherited from P1a and P2A. The contribution focus is deployment governance: integrating hierarchical distributed MPC (HDMPC), pump-station energy objectives, and xIL evidence for safe authority transfer from assisted operation toward bounded autonomy. This version defines scope, notation, and validation protocol skeleton; quantitative benchmark and field campaign statistics will be completed in subsequent iterations.

__Keywords__: digital twin; xIL; HDMPC; energy optimization; water transfer; CHS

## 1. Introduction

P2D targets the engineering gap between algorithmic optimization and auditable field deployment in long-distance regulated water transfer. The Jiaodong system requires simultaneous satisfaction of hydraulic safety, delivery reliability, and energy efficiency under multi-timescale disturbances.

Following the CHS baseline, P2D is positioned as a deployment-and-verification paper (not a new theorem paper):

- theory baseline from P1a (unified model hierarchy and actuator characteristic),
- architecture baseline from P2A (MAS/WSAL and autonomy governance),
- engineering focus on digital-twin xIL and energy-aware HDMPC rollout.

## 2. CHS-consistent formulation and notation lock

The controlled system is written as:

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

Actuator boundary behavior follows the unified local relation:

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

Symbols and units follow the shared CHS table (P1a-consistent): $Q$ [m$^3$/s], $H$ [m], $A_s$ [m$^2$], $\alpha$ [m$^2$/s per unit], and $u$ [-].

## 3. Problem definition: energy-aware operation in Jiaodong transfer

### 3.1 Multi-objective operational requirement

P2D addresses three coupled objectives under safety constraints:

1. **Hydraulic safety**: maintain water level/pressure within hard bounds;
2. **Delivery service**: satisfy planned transfer targets and schedule adherence;
3. **Energy efficiency**: minimize pumping energy and peak-demand penalties.

### 3.2 Baseline optimization structure

For control region $i$, the stage cost is initialized as:

$$
J_i = \sum_{k=0}^{N_p-1} \left( \|y_i(k)-r_i(k)\|_{Q_i}^2 + \|\Delta u_i(k)\|_{R_i}^2 + \lambda_E \, E_i(k) \right) \tag{3}
$$

where $E_i(k)$ is an energy proxy coupled with pump operating point and hydraulic head, and $\lambda_E$ is the energy weighting coefficient to be calibrated in later iterations.

## 4. Digital-twin xIL deployment chain

P2D uses a staged chain to close the gap from controller design to operational authorization:

1. **MiL**: model-level consistency and scenario generation;
2. **SiL**: controller-software verification with deterministic replay;
3. **HiL/xIL**: SCADA/PLC interface timing, fallback, and alarm-route verification;
4. **Pilot shift window**: bounded live trial under ODD constraints.

Each stage must produce immutable artifacts (`dataset_checksum`, `controller_build_id`, `replay_hash`, `alarm_trace_id`) before progressing.

## 5. Initial governance gates (iteration-0 skeleton)

A preliminary four-gate deployment policy is defined:

- **G1 Observability**: required sensors and timestamps complete;
- **G2 Determinism**: deterministic replay reproduces decision traces;
- **G3 Safety**: no unresolved hard-constraint violation in xIL scenarios;
- **G4 Fallback**: rollback to assisted operation verified within bounded time.

Promotion to bounded autonomous execution is allowed only when all four gates pass.

## 6. Scope boundary and cross-paper differentiation

P2D does not claim:

- new hydrodynamic equivalence theorem (covered by P1a),
- WSAL taxonomy novelty (covered by P2A),
- hardware-bench method novelty (covered by CKG-3).

P2D claims a Jiaodong-focused integration contribution: **energy-aware HDMPC + digital-twin xIL + auditable deployment governance**.

## 7. Iteration-0 to iteration-1 plan

Next iteration will add:

1. explicit ODD envelope variables and violation policy;
2. energy KPI set (kWh per transferred volume, peak power, off-peak ratio);
3. reviewer-B-oriented field execution checklist linked to SCADA operations.


## 8. Reviewer-B driven engineering revisions (iteration 1)

### 8.1 ODD envelope variables and violation policy

To convert the iteration-0 gate skeleton into shift-executable governance, this revision introduces an explicit ODD envelope for Jiaodong deployment windows:

- hydraulic envelope: $H_{\text{min}} \le H(t) \le H_{\text{max}}$, $Q_{\text{min}} \le Q(t) \le Q_{\text{max}}$,
- telemetry envelope: data age $\le T_{\text{stale,max}}$ and communication latency $\le T_{\text{lat,max}}$,
- actuation envelope: command increment and rate bounds compatible with L0/L1 safety logic.

Violation handling policy is deterministic:

1. any hard hydraulic envelope violation triggers immediate `DOWNGRADE` to assisted operation;
2. any telemetry envelope violation sets observability gate to fail and blocks autonomous authority;
3. recovery requires a full fallback confirmation and requalification record under current build IDs.

### 8.2 Energy KPI package for field assessment

To make energy-efficiency claims auditable, P2D defines three mandatory KPIs per campaign window:

1. **unit transfer energy** $E_{\text{unit}}$ [kWh/m$^3$],
2. **peak power ratio** $R_{\text{peak}}$ against scheduled baseline,
3. **off-peak utilization ratio** $R_{\text{offpeak}}$ for pump dispatch quality.

These KPIs are reported together with safety outcomes; any energy improvement is invalid if accompanied by unresolved safety or fallback failures.

### 8.3 SCADA-linked operator checklist

Before enabling bounded autonomous execution in a live shift, operators must sign a checklist with immutable records:

1. gate package integrity verified (`dataset_checksum`, `replay_hash`, `controller_build_id`),
2. alarm routing and acknowledgement path tested in active SCADA topology,
3. rollback command tested end-to-end within declared response bound,
4. authority handover roles signed by duty engineer and shift supervisor,
5. unresolved Class A/B alarms explicitly dispositioned.

This checklist binds optimization readiness to practical control-room executability and addresses the deployment realism concerns raised by Reviewer B.


## 9. Reviewer-C driven positioning and transferability refinements (iteration 2)

### 9.1 Bounded contribution statement

To avoid over-claiming while improving interdisciplinary clarity, P2D positions its novelty as a **deployment-governance integration** for Jiaodong rather than a new control theorem. The bounded contribution has three coupled parts:

1. energy-aware HDMPC objective integration under CHS-consistent symbols,
2. digital-twin xIL evidence chain for authorization decisions,
3. auditable operational governance that ties gate outcomes to accountable human roles.

### 9.2 Transferability prerequisites and non-transfer conditions

Cross-site transfer is allowed only when the receiving project satisfies all prerequisites:

- equivalent sensor observability for governed states and boundaries,
- compatible actuator authority paths with verified rollback semantics,
- reproducible xIL replay under declared build/version controls,
- regulator/operator acceptance of ODD and escalation policy definitions.

Transfer is **not** claimed when any prerequisite is absent; in such cases, P2D outputs are treated as reference architecture only, not deployable templates.

### 9.3 Responsible autonomy communication boundary

For external stakeholders, P2D maintains three communication constraints:

1. bounded autonomous operation remains ODD-limited and reversible,
2. `HOLD`/`DOWNGRADE` outcomes are valid safety-preserving results,
3. energy gains are reported only together with safety and fallback compliance evidence.

These statements preserve consistency with P2A WSAL governance language and prevent interpretation drift toward unconditional autonomy claims.


## 10. Reviewer-A driven formal consistency refinements (iteration 3)

### 10.1 Gate predicate formalization for deployment authorization

To strengthen equation-governance coupling while preserving CHS scope boundaries, define four binary authorization gates for a qualified campaign window:

- observability gate $g_{\text{obs}}$,
- determinism gate $g_{\text{det}}$,
- safety gate $g_{\text{safe}}$,
- fallback gate $g_{\text{fb}}$.

The deployment authorization predicate is:

$$
\Pi_{\text{dep}} = g_{\text{obs}} \land g_{\text{det}} \land g_{\text{safe}} \land g_{\text{fb}} \tag{4}
$$

Bounded autonomous operation is admissible only if $\Pi_{\text{dep}}=1$; otherwise, operation remains assisted or is downgraded per Section 8 policy.

### 10.2 Non-compensability and evidence freshness constraints

To avoid compensatory interpretation of mixed-quality evidence, gate outcomes are non-compensable and freshness-bound:

$$
\tilde g_i = g_i \land F_i,\quad i\in\{\text{obs,det,safe,fb}\} \tag{5}
$$

where $F_i=1$ only if artifacts are generated under current controller/model/sensor-map configuration. Any configuration drift resets affected $F_i$ to 0 and blocks authorization until requalification.

### 10.3 Authorization consistency implication

Using effective gates, the operational authorization condition is:

$$
\tilde\Pi_{\text{dep}} = \tilde g_{\text{obs}} \land \tilde g_{\text{det}} \land \tilde g_{\text{safe}} \land \tilde g_{\text{fb}} \Rightarrow \text{AuthReady}=1 \tag{6}
$$

Eq. (6) is a governance implication for deployment readiness and does not alter plant dynamics or HDMPC objective structure in Eq. (3).


## 11. Reviewer-B driven field operability refinements (iteration 4)

### 11.1 Rollback service-level objective (SLO) for shift execution

To make fallback governance directly executable in control-room operations, P2D defines a rollback SLO:

$$
t_{\text{rollback}} \le T_{\text{fb,max}} \tag{7}
$$

where $t_{\text{rollback}}$ is measured from downgrade trigger issuance to assisted-mode authority confirmation in SCADA logs. Any violation of Eq. (7) sets $g_{\text{fb}}=0$ for the active campaign window and requires requalification before new authorization attempts.

### 11.2 Alarm triage and authority closure matrix

Operational alarms are mapped to execution authority to remove ambiguity during shift transitions:

- **Class A (critical safety)**: immediate `DOWNGRADE`, shift supervisor approval mandatory,
- **Class B (major operability)**: `HOLD` until disposition and owner sign-off,
- **Class C (advisory)**: continue under observation with logged mitigation actions.

Each unresolved Class A/B alarm must include owner, deadline, and disposition ID in the campaign package.

### 11.3 Multi-shift handover continuity requirement

For campaigns spanning multiple shifts, each handover must archive:

1. current authorization state and rationale,
2. effective gate snapshot $(\tilde g_{\text{obs}},\tilde g_{\text{det}},\tilde g_{\text{safe}},\tilde g_{\text{fb}})$,
3. rollback readiness timestamp and latest Eq. (7) check,
4. open alarm list with owner assignments.

Missing handover artifacts invalidate campaign closure readiness and trigger `HOLD` until records are completed.


## 12. Reviewer-C driven impact framing and reproducibility refinements (iteration 5)

### 12.1 Bounded-impact reporting tuple for cross-disciplinary comparability

To improve comparability across hydroinformatics, control, and operations audiences, P2D introduces a bounded-impact reporting tuple for each campaign window:

$$
\Omega_{\text{impact}} = (\Delta E_{\text{unit}},\, \Delta R_{\text{peak}},\, \Delta R_{\text{offpeak}},\, \mathcal{S}_{\text{safe}},\, \mathcal{S}_{\text{fb}}) \tag{8}
$$

where energy deltas are always paired with safety/fallback compliance indicators. Any report with $\mathcal{S}_{\text{safe}}=0$ or $\mathcal{S}_{\text{fb}}=0$ is classified as a **non-promotional operational record**, not as an autonomy-performance gain.

### 12.2 Negative-transfer registry requirement

To avoid over-generalization from Jiaodong to other projects, each deployment campaign must maintain a negative-transfer registry including:

1. failed or downgraded scenarios and their violated prerequisites,
2. root-cause category (observability, determinism, safety, fallback, or governance),
3. transferability decision (`portable`, `conditional`, `not-portable`) with rationale.

This registry is version-linked to the active controller build and must be archived with campaign artifacts to support external audit and replication studies.

### 12.3 Public-communication guardrail for WSAL interpretation

For responsible communication beyond technical teams, P2D defines a one-line guardrail statement to be attached to summaries and dashboards:

> “Current results indicate **ODD-bounded conditional autonomy readiness** under verified rollback capability; they do not imply unrestricted autonomous operation.”

This wording keeps P2D aligned with P2A WSAL semantics and reduces the risk of interpreting local campaign improvements as full-system autonomy claims.


## 13. Reviewer-A driven formal consistency cleanup (iteration 6)

### 13.1 Safety-priority implication for authorization semantics

To keep governance predicates consistent with CHS safety-first operation, P2D adds an explicit safety-priority implication:

$$
\tilde\Pi_{\text{dep}} = 1 \Rightarrow \tilde g_{\text{safe}}=1 \land \tilde g_{\text{fb}}=1 \tag{9}
$$

Eq. (9) makes the non-compensability logic operationally explicit: deployment authorization cannot be interpreted independently from validated safety and rollback readiness.

### 13.2 Campaign artifact completeness criterion

For pre-shift authorization, define the artifact set:

$$
\mathcal{A}_{\text{camp}}=\{\text{dataset\_checksum},\,\text{controller\_build\_id},\,\text{replay\_hash},\,\text{alarm\_trace\_id}\} \tag{10}
$$

A campaign is deemed evidence-complete only when every element in Eq. (10) is present and version-consistent with the active controller release; otherwise, authorization remains in `HOLD` state.

### 13.3 Iteration-5 reference verification log

Following the 5-iteration verification cadence, iteration 5 includes a reference-integrity check for cited Lei representative works and CHS baseline links. No fabricated entries were identified, and citation usage remains bounded to deployment-relevant scope for P2D.
