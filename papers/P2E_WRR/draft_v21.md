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

Expanding the Operational Design Domain (ODD) of hydropower control systems is a prerequisite for advancing Water Systems Autonomy Levels (WSAL) from L2 (assisted operation) to L3 (conditional autonomy). This paper presents a CHS-consistent framework for governing that transition in the Shaping hydropower context. The framework adopts a six-element system formalization $\Sigma=(P,A,S,D,C,O)$, preserves unified actuator boundary semantics, and maps model layers to control layers under a just-precise-enough criterion. Four deterministic go/no-go gates -- observability, determinism, safety, and fallback -- are defined to regulate ODD expansion, with each gate requiring quantitative evidence from SiL and xIL validation stages. Safety floor constraints ensure bounded operation under disturbance and communication degradation, while operator override and automatic rollback mechanisms guarantee safe downgrade when ODD boundaries are exceeded. The proposed pathway is demonstrated through the Shaping pilot case, providing a reproducible, evidence-gated procedure for conditional autonomy promotion in high-consequence water infrastructure.

__Plain Language Summary__

Many hydropower stations can recommend actions but still rely on humans to confirm every control decision. This corresponds to WSAL-2. To reach WSAL-3 safely, the system must operate autonomously only within a verified operational boundary (ODD), with reliable fallback to safe control when uncertainty increases. This paper defines that transition pathway for the Shaping case using consistent control-theoretic terms from the CHS framework and a staged verification strategy.

## 1. Introduction

Hydropower operations increasingly rely on automated decision support, yet the transition from human-confirmed control (WSAL-2) to conditional autonomy (WSAL-3) lacks a systematic, evidence-gated governance framework. Existing approaches either impose full manual oversight regardless of demonstrated system capability or adopt ad hoc automation without formal verification of operational boundaries. This paper addresses that gap by formalizing the Operational Design Domain (ODD) expansion pathway and the WSAL-2 to WSAL-3 transition for the Shaping hydropower station, within the Cyber-Hydro System (CHS) framework.

The principal contributions are: (1) a deterministic gate structure linking model fidelity, control-layer scope, and xIL evidence to ODD expansion decisions; (2) safety floor constraints that guarantee bounded fallback under disturbance and communication degradation; and (3) a staged validation workflow demonstrated through the Shaping pilot case. The formalization is consistent with the unified system representation and actuator semantics established in companion papers (P1a, P2A) and does not introduce new hydrodynamic theory.

## 2. CHS-consistent formulation

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

## 3. Scope and Paper Organization

This paper focuses on the engineering governance pathway for ODD expansion and WSAL-2 to WSAL-3 transition at the Shaping hydropower station. The scope is bounded as follows:

- All terminology and symbol conventions are consistent with the CHS foundations established in P1a and the WSAL architecture defined in P2A.
- The paper does not introduce new hydrodynamic theory; Eqs. (1) and (2) are adopted from the unified CHS formalization and applied under explicitly stated local assumptions.
- The contribution is restricted to a governed transition procedure with deterministic evidence gates, safety floor constraints, and fallback accountability for a single pilot site.

The remainder of the paper is organized as: Section 4 presents the methods and formalization of the ODD gate structure; Section 5 reports validation results from the Shaping pilot; Section 6 discusses implications and limitations; and Section 7 states conclusions.


## 4. Methods and Formalization

*[TODO: Formalize the ODD expansion gate structure and WSAL-2 to WSAL-3 transition criteria. Define observability, determinism, safety, and fallback gates with quantitative thresholds. Specify the model-layer to control-layer correspondence under the just-precise-enough criterion. Present assumptions bounding Eq. (2) validity scope.]*

## 5. Results and Validation

*[TODO: Present SiL and xIL evidence from the Shaping pilot. Report deterministic replay outcomes, safety-floor compliance statistics, and fallback latency measurements. Include scenario coverage across nominal, stress, and fault-containment classes. Provide quantitative gate-pass/fail summaries.]*

## 6. Discussion

*[TODO: Interpret results in the context of CHS-consistent autonomy transitions. Compare ODD expansion evidence against existing hydropower automation practices. Discuss limitations of the pilot scope, assumptions, and transferability to other sites. Address the role of human oversight in WSAL-3 conditional autonomy.]*

## 7. Conclusions

*[TODO: Summarize key findings on ODD expansion and WSAL-2 to WSAL-3 transition feasibility. State the principal contribution: a governed, evidence-gated pathway for conditional autonomy in hydropower operations. Identify directions for future work including multi-site replication and higher WSAL levels.]*

## Acknowledgments

*[TODO: Acknowledge funding sources, field operators at the Shaping hydropower station, and contributing institutions.]*

## References

*[TODO: Add references. Ensure inclusion of CHS framework foundations (Lei 2025a-d), ODD/autonomy-level literature, and relevant hydropower control references.]*
