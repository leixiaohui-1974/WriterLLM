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
