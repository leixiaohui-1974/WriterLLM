*Manuscript prepared for Water Resources Research*

__From ODD Expansion to WSAL-2→3 Transition in Shaping Hydropower: A CHS-Governed Validation Framework__

__Zhang Lei__1, __Xiaohui Lei__1,2*, __Ye Shangjun__2, __Chen Ji__3, __Liu Xiaowei__1, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

*Corresponding author: Xiaohui Lei (lxh@iwhr.com)*

__Key Points__

- We formalize a CHS-consistent pathway for WSAL-2 to WSAL-3 transition in Shaping hydropower operation.
- ODD expansion is governed by deterministic gates linking model level, control layer, and xIL evidence.
- Safety floor constraints preserve bounded operation under disturbance and communication degradation.

__Abstract__

This initial draft presents a CHS-consistent framework for extending Operational Design Domain (ODD) in the Shaping hydropower context and supporting the Water Systems Autonomy Level (WSAL) transition from L2 (assisted operation) to L3 (conditional autonomy). The manuscript adopts the six-element system formalization $\Sigma=(P,A,S,D,C,O)$, preserves unified actuator boundary semantics, and maps model layers to control layers under a just-precise-enough criterion. A staged validation workflow is proposed across SiL and xIL evidence gates, including deterministic replay artifacts, fallback policy, and operator override constraints. This version establishes scope, notation, and governance structure; quantitative benchmarking and field statistics will be added in later iterations.

__Plain Language Summary__

Many hydropower stations can recommend actions but still rely on humans to confirm every control decision. This corresponds to WSAL-2. To reach WSAL-3 safely, the system must operate autonomously only within a verified operational boundary (ODD), with reliable fallback to safe control when uncertainty increases. This draft defines that transition pathway for the Shaping case using consistent control-theoretic terms from the CHS framework and a staged verification strategy.

## 1. Introduction

This draft initializes P2E as the engineering transition paper for ODD expansion and WSAL-2→3 crossing in the B4 batch.

## 2. CHS-consistent formulation

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

## 3. Draft scope in iteration 0

- Lock terminology to P1a/P2A and shared symbols.
- Define ODD expansion gate candidates and evidence placeholders.
- Prepare subsequent reviewer-loop iterations.


## 4. Reviewer-B driven engineering refinements (iteration 1)

### 4.1 ODD gate definitions for WSAL-2→3 transition

We define four go/no-go gates for promoting from assisted mode to conditional autonomy in the Shaping pilot:

1. **Observability gate**: level/flow sensing coverage for all active control boundaries; stale-data timeout must trigger safe downgrade.
2. **Determinism gate**: fixed-seed replay hash mismatch rate must equal zero for qualified scenarios.
3. **Safety gate**: no hard-constraint violation in nominal and bounded-fault tests.
4. **Fallback gate**: operator override and automatic rollback can be completed within bounded response time.

### 4.2 Minimal evidence package

Each qualified run stores a minimal package:
- `run_id`, `seed_set`, `plan_hash`, `dataset_checksum`, `replay_hash`
- runtime latency trace and safety monitor log
- operator override timeline and rollback event record

### 4.3 Bounded scope statement

This draft does not claim field-wide autonomous deployment. The current scope is a staged validation pathway for ODD expansion under CHS constraints, with pilot evidence to be added in later iterations.


## 5. Reviewer-C driven innovation and governance refinements (iteration 2)

### 5.1 Two-axis contribution boundary

This manuscript contributes along two bounded axes:

- **Engineering governance axis**: ODD expansion gates and WSAL-2→3 promotion policy for Shaping operations.
- **Verification integration axis**: deterministic replay evidence plus xIL-centered acceptance protocol.

No new hydrodynamic theorem is claimed; equations remain consistent with P1a/P2A foundations.

### 5.2 WSAL transition governance matrix

| Transition condition | Required evidence | Decision |
|---|---|---|
| All four ODD gates pass | replay hash = 0 mismatch; safety log clear | Promote to conditional autonomy trial |
| Any gate fails | failed-gate artifact + rollback trace | Remain in assisted mode |
| Communication degradation beyond ODD | stale-data/latency alarm + override record | Immediate safe downgrade |

### 5.3 Cross-paper linkage note

- P2E reuses CKG-3 HiL evidence logic for WSAL crossing verification.
- P2E remains aligned with P2A WSAL terminology and P1a actuator/symbol conventions.
- P2E will provide engineering feedback to P2D deployment practices in later batch integration.
