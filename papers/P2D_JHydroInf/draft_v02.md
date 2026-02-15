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
