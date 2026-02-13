# Revision Response — P1a WRR v13 → v14

**Iteration**: 5
**Reviewer**: C (Cross-disciplinary Scholar)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Cognitive Intelligence–HDC Interaction Formal Specification

**Response**: Accepted. The propose-validate interface deserves tighter specification.

**Action taken**: Added formalization to Section 7.3 after the drought escalation example:
- Specified the candidate tuple: "Formally, the candidate tuple C = {J_new ∈ ℝ^(n×n), g_new ∈ ℝ^m, ODD_status ∈ {within, approaching, outside}} encodes the proposed quadratic cost matrix, the constraint vector, and ODD proximity assessment. The HDC feasibility validator returns either ACCEPT (a feasible control trajectory exists) or REJECT with a diagnostic vector indicating which constraints are infeasible, enabling Cognitive Intelligence to iteratively relax its proposal."
- Added confidence calibration: "The confidence threshold for Cognitive Intelligence recommendations is defined as the calibrated posterior probability of the dominant scenario class. Following Guo et al. (2017), calibration requires that predicted confidence align with empirical accuracy—a 90% confidence classification should be correct 90% of the time. When confidence falls below a site-specific threshold (default 0.7, adjustable during xIL commissioning), the system defaults to the last-validated HDC configuration."
- Added watchdog mechanism: "A persistent misclassification watchdog monitors the cumulative discrepancy between Cognitive Intelligence scenario predictions and observed system behavior over a rolling 24-hour window. If the discrepancy exceeds a configurable threshold, the watchdog triggers an automatic revert to the baseline HDC configuration and flags the event for operator review."

### M2. Differentiable Modeling Frontier

**Response**: Accepted. This is an excellent observation connecting CHS to the emerging physics-AI hybrid paradigm.

**Action taken**: Added paragraph to Section 8.4:
"An emerging paradigm that directly realizes the CHS philosophy of 'structure from physics, parameters from data' is differentiable modeling—where physics-based model structures are made differentiable and their parameters learned end-to-end from operational data using gradient-based optimization (Shen et al., 2023). The CHS model hierarchy provides an ideal structural backbone for this paradigm: differentiable IDZ models would enable automatic calibration of {Aₛ, τᵈ, τₘ} from operational time series, bypassing traditional system identification procedures. Furthermore, neural operators (Li et al., 2021) could provide fast differentiable surrogates of the Saint-Venant equations for Layer 3 planning, maintaining structural constraints while accelerating computation by orders of magnitude. The five-level model hierarchy (LSV→IDZ→ID→I→SS) naturally suggests a curriculum learning strategy: train on steady-state data first, progressively incorporating higher-frequency dynamics as model complexity increases."

### M3. Prediction 1 Grounding in Published Results

**Response**: Accepted. Published MPC performance results provide direct grounding.

**Action taken**: Added supporting evidence to Prediction 1: "This target is conservative relative to published results: Horváth et al. (2024) report 40–60% RMS improvement for IDZ-MPC over PI control on the Terneuzen canal, and van Overloop et al. (2010) report 30–50% improvement for centralized MPC on Arizona canal pools. The 30% threshold represents the minimum expected improvement, accounting for the additional complexity of distributed rather than centralized implementations."

Added van Overloop et al. (2010) to the reference list.

### M4. Operational Singularity Naming — AI Community Disambiguation

**Response**: Partially accepted. The footnote now addresses both mathematical and AI-community usages.

**Action taken**: Expanded the existing footnote (from v12, addressing mathematical singularity) to add: "Nor should it be confused with the 'technological singularity' concept from AI futurism (Kurzweil, 2005); the CHS operational singularity is a characterization of existing physical constraints, not a prediction about future capability thresholds."

### M5. Impact Statement

**Response**: Accepted. An Impact Statement enhances discoverability.

**Action taken**: Added an Impact Statement section after the Key Points:
"**Impact Statement**: This paper introduces the first unified control-theoretic framework for water network operations, proving that all existing low-order hydrodynamic models are special cases of a single transfer function family. The proposed Multi-Agent System architecture and Water Systems Autonomy Levels classification provide the theoretical foundation and shared vocabulary for transitioning water infrastructure from manual operation toward autonomous control."

---

## Response to Minor Issues

### m1. MAS Agent Communication Topology
**Action**: Added to Section 7.3: "The communication topology is hierarchical by default: Edge Agents report to their Area Agent (star topology within each area), and Area Agents exchange boundary information with neighboring Area Agents and report to the Cloud Agent. For hydraulically coupled adjacent pools requiring fast disturbance propagation signals (timescale < Layer 2 coordination cycle), direct Edge-to-Edge lateral communication is permitted within the same Area, forming a local mesh within the hierarchical backbone."

### m2. Priority 5 (Institutional and Human Factors)
**Action**: Expanded Section 9.1 Priority 5 by two sentences: "The institutional dimension is likely the binding constraint on WSAL advancement: regulatory frameworks for autonomous water system operation do not yet exist in most jurisdictions, and operator labor agreements may need renegotiation. A dedicated companion paper will address the sociotechnical analysis of WSAL adoption, including regulatory pathway mapping, workforce transition strategies, and public trust calibration."

### m3. Prediction 3 Numerical Thresholds vs. Scaling Law
**Action**: Added clarifying sentence to Prediction 3: "The scaling law f_b* ≈ min(1, τᵈ/T_comm) provides the theoretical limiting behavior. The stated thresholds (80% for τᵈ/T_comm > 5; 30% for τᵈ/T_comm < 1) account for practical factors not captured in the simplified single-pool derivation: multi-pool coupling introduces additional buffering requirements that shift the curve upward, while fast coordination reduces the effective buffer need below the single-pool prediction."

### m4. Cross-Referencing Between Predictions and Theory
**Action**: Added explicit section cross-references: Prediction 1 → Section 6.1-6.2; Prediction 2 → Section 6.3; Prediction 3 → Section 5.3, eq. f_b* ≈ min(1, τᵈ/T_comm); Prediction 4 → Section 7.4, Table 6 measurement protocol.

### m5. Solo Author Context
**Action**: Expanded Acknowledgments: "The CHS framework was developed as a personal theoretical synthesis; the author thanks colleagues in the IAHR Working Group on Water System Operations, the doctoral research team at Hebei University of Engineering, and Academician Hao Wang for mentorship and critical discussions that refined the ideas presented here. The multi-disciplinary scope of this solo-authored synthesis reflects the integrative nature of the CHS project, which draws on the author's two decades of experience spanning hydraulic engineering, control systems, and water network operations."

---

## Reference Audit Response

### Added References:
- Li, Z., et al. (2021). Fourier Neural Operator for Parametric Partial Differential Equations. ICLR. — for differentiable modeling discussion
- van Overloop, P.J., et al. (2010). Multiple-Model Optimization of Proportional Integral Controllers on Canals. ASCE JWRPM. — for Prediction 1 grounding
- Guo, C., et al. (2017). On Calibration of Modern Neural Networks. ICML. — for Cognitive Intelligence confidence calibration

### Self-citation rate: Unchanged at ~16% (3 new non-self references added).

---

## Version Summary

- **v13 → v14 changes**: Formalized propose-validate interface with tuple specification, HDC binary response, confidence calibration (Guo et al., 2017), and persistent misclassification watchdog (M1); added differentiable modeling paragraph to Section 8.4 with neural operator connection (Li et al., 2021) (M2); grounded Prediction 1 with published MPC performance numbers (Horváth et al., 2024; van Overloop et al., 2010) (M3); expanded operational singularity footnote for AI community disambiguation (M4); added Impact Statement after Key Points (M5); specified MAS communication topology (m1); expanded institutional barriers discussion (m2); explained Prediction 3 threshold discrepancy (m3); added theory-prediction cross-references (m4); expanded Acknowledgments for solo author context (m5).
