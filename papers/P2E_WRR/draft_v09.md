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

## 6. Reviewer-A driven rigor refinements (iteration 3)

### 6.1 Explicit assumptions for Eq. (2) validity scope

To keep consistency with P1a Lemma 3 while avoiding over-extension, Eq. (2) is used under the following local assumptions:

- **A1 (local linearization)**: operation remains in a neighborhood of the scheduled point where first-order linearization is valid.
- **A2 (bounded head perturbation)**: $\Delta H_{\text{up}}$ and $\Delta H_{\text{dn}}$ remain within verified ODD bounds used in replay and xIL tests.
- **A3 (actuator smoothness)**: actuator command increments $\Delta u$ satisfy rate limits enforced by L0/L1 safety logic.

Outside these assumptions, the policy is mandatory downgrade to assisted mode rather than model extrapolation.

### 6.2 Model-layer to control-layer acceptance rule

For each candidate ODD expansion, acceptance requires model-layer consistency with the target control layer:

- **L1 regulation scope** uses IDZ-level dynamics and must pass deterministic replay plus bounded-fault stress.
- **L2 coordination scope** uses ID/IDZ abstraction and must satisfy inter-agent constraint consistency under communication delay envelopes.
- **Any mismatch** between required layer fidelity and evidence quality triggers rejection of promotion.

This rule operationalizes the “just precise enough” correspondence for WSAL-2→3 engineering decisions.

### 6.3 Falsifiability-oriented acceptance metrics

To avoid qualitative-only acceptance, three falsifiable metrics are required per gate campaign:

1. **Safety violation count**: zero hard-constraint violations in qualified scenarios.
2. **Replay determinism metric**: zero hash mismatches for fixed seed sets.
3. **Fallback latency bound**: rollback/override completion time not exceeding declared ODD threshold.

A campaign fails if any metric violates threshold; no partial promotion is permitted.

## 7. Reviewer-B driven deployment and evidence refinements (iteration 4)

### 7.1 Scenario taxonomy and minimum campaign size

To avoid under-sampled WSAL promotion decisions, each ODD expansion campaign must include at least three scenario classes:

- **Nominal class**: routine inflow/load trajectories within historical operating envelope.
- **Stress class**: bounded but adverse combinations of inflow disturbance, actuator saturation approach, and communication jitter.
- **Fault-containment class**: single-point sensing/communication degradation cases that must trigger bounded fallback.

For each class, fixed seed sets and timestamped dataset checksums are mandatory; campaigns lacking any class are automatically rejected.

### 7.2 Operator-facing go/no-go checklist

Before promotion from assisted mode to conditional autonomy trial, operations staff must sign off the following checklist:

1. All four ODD gates passed with archived evidence package.
2. Safety monitor thresholds and alarm routing verified in current SCADA configuration.
3. Manual override path tested end-to-end on active shift.
4. Rollback script replayed successfully on current control software version.
5. Communication-loss downgrade tested within declared latency bound.

This checklist binds technical gate success to executable field procedure and accountability.

### 7.3 Evidence traceability table for audit reuse

| Artifact | Producer | Immutable key | Audit purpose |
|---|---|---|---|
| Scenario dataset | Validation pipeline | dataset_checksum | Verify data integrity |
| Closed-loop replay run | Runtime engine | replay_hash | Verify deterministic reproducibility |
| Safety monitor log | L0/L1 safety layer | log_digest | Verify hard-constraint compliance |
| Override/rollback record | Operator + controller | event_chain_id | Verify fallback executability |
| Gate decision package | Review board | package_id | Verify WSAL promotion rationale |

All artifacts are version-coupled to model and controller build IDs; mixed-version evidence is invalid.

## 8. Reviewer-C driven impact and literature refinements (iteration 5)

### 8.1 Positioning statement for cross-domain transfer value

To improve disciplinary impact clarity while keeping claims bounded, P2E positions its contribution as a **transition-governance template** rather than a new control theorem. The reusable value is the coupling of:

- CHS-consistent model-layer/control-layer matching,
- ODD evidence-gated promotion logic,
- and auditable fallback accountability for WSAL crossing.

This template is intended for transfer to other high-consequence regulated water operations after site-specific ODD re-identification.

### 8.2 Responsible autonomy boundary and human role persistence

WSAL-3 in this paper is explicitly defined as **conditional autonomy under verified ODD**, not operator removal. Human roles remain mandatory for:

1. ODD boundary approval and expansion authorization,
2. override governance and exception adjudication,
3. post-event review of failed or downgraded campaigns.

Accordingly, promotion decisions are socio-technical decisions supported by evidence, not fully automated verdicts.

### 8.3 Iteration-5 reference verification note

Following the every-5-iterations verification rule, references were rechecked for this draft cycle.

- Mandatory Lei anchors (`Lei 2025a–d`) remain retained in `references.bib`.
- No fabricated references were added in this iteration.
- Citation scope remains aligned with the pilot-governance contribution boundary.

### 8.4 Cross-paper differentiation guardrail

To maintain low overlap with P1a/P2A while preserving consistency:

- P1a provides theorem-level unified dynamics and model hierarchy foundations.
- P2A provides MAS/WSAL architecture and taxonomy.
- P2E focuses on engineering transition governance for WSAL-2→3 under ODD/xIL evidence and fallback accountability.

This guardrail is applied to avoid re-stating base theory beyond necessary linkage.

## 9. Reviewer-A driven formal consistency refinements (iteration 6)

### 9.1 Gate-decision logic formalization

Let the four ODD promotion gates be observability $g_{\text{obs}}$, determinism $g_{\text{det}}$, safety $g_{\text{safe}}$, and fallback $g_{\text{fb}}$, each evaluated as binary outcomes in a qualified campaign.

Define the promotion predicate:

$$
\Pi = g_{\text{obs}} \land g_{\text{det}} \land g_{\text{safe}} \land g_{\text{fb}} \tag{3}
$$

Promotion to WSAL-3 trial is permitted iff $\Pi=1$; otherwise, the system remains at WSAL-2 or is downgraded according to boundary-exceedance policy.

### 9.2 Mapping Eq. (2) assumptions to gate failures

To avoid ambiguity between model validity and operational decisions, Eq. (2) assumptions (A1–A3) are bound to gate outcomes:

- Violation of A1 (local linearization) or A2 (bounded perturbation) is treated as ODD exceedance and forces $g_{\text{safe}}=0$.
- Violation of A3 (actuator smoothness/rate limits) forces $g_{\text{fb}}=0$ until rollback verification is re-qualified.
- Any unresolved assumption violation invalidates campaign evidence for promotion.

This preserves strict consistency between mathematical validity scope and autonomy-governance decisions.

### 9.3 Non-compensability and monotonic safety rule

Gate outcomes are **non-compensable**: no single strong metric can offset another failed gate.

- If any $g_i=0$, then $\Pi=0$ by definition.
- Requalification requires rerunning the failed gate and regenerating the decision package with updated immutable keys.
- Historical pass records cannot be reused when model/controller build IDs change.

The rule enforces monotonic safety: evidence accumulation can enable promotion, but partial evidence cannot justify override of a failed gate.

## 10. Reviewer-B driven implementation-readiness refinements (iteration 7)

### 10.1 Shift-level execution protocol

To ensure gate logic is executable by field teams, WSAL-2→3 trial activation is constrained by a shift-level protocol:

1. pre-shift configuration lock (model/controller build IDs frozen),
2. gate package integrity check (`dataset_checksum`, `replay_hash`, `package_id`),
3. on-shift dry-run of override and rollback paths,
4. activation window with live safety monitor escalation,
5. post-window debrief with signed exception log.

If any step is incomplete, activation is cancelled and the system remains in assisted mode.

### 10.2 Communication degradation stress envelope

To align with engineering operations, communication degradation is assessed under a stress envelope with three conditions:

- latency spikes within ODD upper bound,
- intermittent packet loss within tolerated ratio,
- brief telemetry blackout requiring safe downgrade.

A candidate WSAL-3 trial is rejected if any stress-envelope test produces unresolved alarm-state ambiguity.

### 10.3 Campaign closure criteria for operational acceptance

A campaign is closed as **operationally acceptable** only when all conditions hold:

- Eq. (3) promotion predicate satisfied in qualified scenarios,
- zero hard-constraint violation across required classes,
- rollback completion latency within declared threshold,
- signed operator checklist and audit package archived.

Otherwise the campaign status is **open**, with failed items assigned corrective actions and mandatory revalidation.

## 11. Reviewer-C driven governance-scale and transparency refinements (iteration 8)

### 11.1 Multi-stakeholder decision transparency layer

To improve cross-domain legitimacy of WSAL transition decisions, each promotion package should include a transparency layer summarizing:

- gate outcomes and unresolved risks in non-technical language,
- operator actions taken during activation window,
- rationale for promote / hold / downgrade outcomes.

This layer does not replace technical evidence, but enables accountable review by operators, managers, and safety regulators.

### 11.2 Bounded transferability statement

P2E transferability is explicitly bounded by three prerequisites:

1. local ODD is re-identified with site-specific disturbance envelopes,
2. fallback authority and override chain are formally assigned,
3. deterministic replay and immutable audit artifacts are reproducible in the target stack.

Without these prerequisites, the manuscript recommends retaining WSAL-2 assisted operation.

### 11.3 Public-interest risk communication note

For pilot deployments with public-service implications, event reports should classify outcomes into:

- **safe success** (all gates pass, no hard-constraint breach),
- **safe hold** (promotion denied, assisted mode retained),
- **safe downgrade** (autonomy trial terminated and fallback executed).

This classification keeps safety-first semantics visible and prevents misinterpretation of “non-promotion” as system failure.

