# Revision Response — P1b Nature Water v04 → v05

**Iteration**: 4
**Reviewer**: B (Engineering Practitioner)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. WSAL Quantitative Discriminants — Calibration

**Response**: Accepted. The thresholds need qualification.

**Action taken**:
- Added qualifying sentence after the discriminants: "These thresholds are illustrative starting points; their calibration requires empirical validation through pilot deployments and should ultimately be determined through international standardization processes. The aviation parallel suggests that safety-critical transitions (L2→L3, L4→L5) may require near-complete coverage of defined test suites, with the acceptable residual risk determined by the consequence severity of the water system under consideration."

### M2. Engineering Lessons Learned

**Response**: Accepted. Operator acceptance and failure modes are high-value additions for practitioners.

**Action taken**:
- Added after the Jiaodong description and before the international context paragraph: "Engineering practice revealed two cross-cutting lessons. First, operator trust proved a binding constraint: operators at both facilities initially overrode automated recommendations in a significant fraction of non-emergency scenarios, decreasing substantially after a familiarization period of several months — underscoring the importance of shadow-mode deployment before full automation. Second, edge cases at operating-point transitions (e.g., switching between gravity-flow and pumped modes at Jiaodong) occasionally produced controller recommendations that, while mathematically optimal, conflicted with operators' experiential heuristics, requiring iterative operational-constraint refinement."

### M3. MAS Communication Architecture

**Response**: Accepted. Communication resilience is critical for field deployment.

**Action taken**:
- Added to the MAS paragraph: "The architecture inherits Layer 0's safety-first principle at the communication level: each agent maintains a local fallback strategy that activates upon communication timeout, ensuring safe degradation to the highest autonomy level sustainable with locally available information."

### M4. Cybersecurity

**Response**: Accepted. This is a significant gap for any networked control system perspective.

**Action taken**:
- Added to "Challenges" section after the standards paragraph: "On cybersecurity: networked autonomous water systems introduce attack surfaces at every architectural layer — from sensor spoofing at edge agents to adversarial inputs targeting Cognitive Intelligence's knowledge retrieval. Securing these systems requires defense-in-depth approaches aligned with IEC 62443[70] and tailored to water infrastructure's specific threat landscape, including the physical-digital coupling that distinguishes water systems from purely digital targets."
- Added IEC 62443 as reference [70].

### M5. Companion Paper Reference — Timing

**Response**: Accepted. The self-contained nature of this Perspective should be explicit.

**Action taken**:
- Revised to: "References 14–16 and 19 are Chinese-language publications that establish the CHS mathematical foundations; an English-language companion paper presenting the complete theoretical framework is in preparation for Water Resources Research. The present Perspective is self-contained in its conceptual arguments and does not depend on the companion paper for its central claims."

---

## Response to Minor Issues

### m1. Buffer Zone Width Trade-off
**Action**: Added: "whose width must balance operational availability against degradation response time."

### m2. Supervisory Control Accessibility
**Action**: Added brief intuitive explanation: "...where the physics-based validator acts as a supervisor constraining the cognitive planner's actions to remain within the hydraulically feasible set — analogous to how a safety interlock prevents a crane operator from exceeding load limits, but applied to the higher-level decisions of scenario selection and strategy switching."

### m3. OpenFOAM → EPANET/SWMM
**Action**: Replaced "following the precedent of OpenFOAM in computational fluid dynamics" with "following the precedent of open-source water modelling tools such as EPANET and SWMM that have democratized hydraulic analysis globally."

---

## Version Summary

- **v04 → v05 changes**: Calibrated WSAL discriminants with aviation comparison (M1); added engineering lessons on operator trust and edge cases (M2); added communication fallback for MAS (M3); added cybersecurity challenge with IEC 62443 (M4); clarified companion paper self-containment (M5); ODD buffer zone trade-off (m1); supervisory control intuitive analogy (m2); EPANET/SWMM open-source precedent (m3).
- **New references**: IEC 62443 [70].
- **Self-citation rate**: ~16% (70 total references, ~11 self-citations).
