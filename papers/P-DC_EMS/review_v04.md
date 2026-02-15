# Review Report — Paper P-DC (EMS v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

This paper proposes Design for Operation (DfO) with five quantitative principles, a seven-layer Model-Based Definition (MBD) framework, and a competency-based curriculum for Cybernetics of Hydro Systems. The v03 revision has added useful cross-disciplinary content (digital twin positioning, ML discussion, competency framework). However, from a control-theoretic perspective, several formal definitions require tightening, and the connection between the MBD framework and the established CHS model hierarchy (Lei, 2025a) needs explicit formalization.

The paper's strength is its ambition: it attempts to bridge the gap between CHS theory and engineering practice through a structured framework. The DfO principles with quantitative metrics (P1–P5) are a good conceptual contribution. The reference workflow with quantitative MiL results (Table 6) provides credible validation. However, the mathematical specification of the DfO metrics is incomplete in several respects, and the relationship between MBD layers and the CHS five-level model hierarchy is left implicit rather than formalized.

These issues are addressable without major restructuring. The paper is approaching publication quality.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7.5 | DfO paradigm is a genuine contribution; MBD adaptation solid |
| Mathematical Rigor | 6.5 | DfO metrics incompletely specified; Gramian evaluation unclear |
| Reproducibility | 7.5 | Reference workflow detailed; FMI co-simulation explicit |
| Case Validation | 7.5 | Quantitative MiL results convincing for single case |
| Literature Completeness | 7.5 | Good cross-domain coverage after v03 additions |
| Writing Quality | 8 | Clear, well-structured, professional |
| System Differentiation | 7.5 | Digital twin positioning effective; P1a connection needs work |

---

## Major Issues

### M1. DfO Metric Specification: Gramian Evaluation over ODD

Principles P1 and P2 define metrics based on the controllability Gramian $W_c$ and observability Gramian $W_o$ of the Layer 6 state-space model, "evaluated over the target ODD." This is mathematically incomplete:

(a) The Gramians are defined for a specific linearization point. Over the ODD, the operating point varies (e.g., Q ∈ [2, 8] m³/s), and the linearized model changes. How are the Gramians aggregated? Options include:
- Worst-case: $\sigma_{min}(W_c) = \min_{p \in ODD} \sigma_{min}(W_c(p))$ — conservative but computationally expensive
- Average: $\bar{W}_c = \mathbb{E}_p[W_c(p)]$ — less conservative but requires a probability measure over ODD
- Vertex evaluation: compute at ODD vertices (corners of the Cartesian product) — practical but may miss interior minima

(b) The threshold $\gamma_c$ in P1 is stated but not defined: how should it be chosen? Is it system-specific? What are the units?

(c) For P2, the condition number $\kappa(W_o)$ depends on the scaling of states and outputs. Is the Gramian computed from the balanced realization?

Please specify the evaluation method (I recommend worst-case over ODD vertices as a practical default) and provide guidelines for threshold selection.

### M2. MBD Layers and the CHS Five-Level Model Hierarchy

Lei (2025a, §4.6) establishes a five-level model hierarchy: LSV → IDZ → ID → I → SS (from full Saint-Venant to steady-state). The MBD framework has Layer 7 (Physical Model) and Layer 6 (Control Model), but the correspondence between these two layers and the five CHS model levels is not formalized.

Specifically:
- Does Layer 7 correspond to the LSV level? The paper suggests yes, but the physical model could also include numerical approximations that are not strictly "full Saint-Venant."
- Does Layer 6 correspond to the IDZ level? The reference workflow uses IDZ, but Layer 6 could also use the ID or I levels depending on the control design needs.
- The Layer 7→6 transition (§3.3) describes "linearization, discretization, Padé approximation" — this is the LSV→IDZ reduction described in P1a §4.7. Making this correspondence explicit (citing Theorem 3: Model-Layer Correspondence) would strengthen the theoretical grounding.

Please add a paragraph or table explicitly mapping the five CHS model levels to MBD Layers 7–6, citing P1a Theorem 3.

### M3. Reference Workflow: IDZ Identification Methodology

The IDZ parameters in Table 4 are identified "from step-response analysis" of the Layer 7 model. The mathematical identification procedure is not specified:
- What fitting method? (Least-squares? Moments matching? Frequency-domain?)
- What is the identification criterion? (Minimize time-domain RMSE? Frequency-domain $H_\infty$ error?)
- What are the confidence intervals on the identified parameters? The IDZ model is a three-parameter model ($A_s$, $\tau_d$, $\tau_m$); with a clean step response from a simulation, the identification should be well-conditioned, but this should be stated.
- How sensitive is the MPC performance (Table 6) to parameter uncertainty? If $A_s$ is misidentified by ±10%, does the RMSE remain below 0.05 m?

Even a brief paragraph specifying the identification method and noting the sensitivity would satisfy this concern. The Litrico & Fromion (2009) methodology for IDZ identification could be cited.

---

## Minor Issues

### m1. Saint-Venant Discretization: Preissmann Parameter

Equations (1)–(2) present the continuous Saint-Venant equations, and the text states "Preissmann implicit scheme with Δx = 100 m." The Preissmann scheme requires a weighting parameter θ ∈ [0.5, 1.0] that controls numerical diffusion. Please state the value used (typically θ = 0.6 for canal applications). This is relevant because the choice of θ affects the numerical wave speed and hence the accuracy of the Layer 7 model against which Layer 6 is validated.

### m2. ODD Coverage Ratio: Measure Specification

Principle P3 defines $R_{ODD} = |ODD_{achievable}| / |ODD_{target}|$ where $|·|$ is "the measure (volume) of the ODD set." For a Cartesian product ODD $S_{flow} \times S_{level} \times S_{equip} \times S_{comm}$, the dimensions have different units and scales. The measure should be normalized (e.g., using the Lebesgue measure of the normalized hypercube) to avoid dimensional inconsistency. Alternatively, define $R_{ODD}$ as the fraction of a discrete test grid that passes—consistent with the 12-scenario MiL test in §6.

### m3. MPC Prediction Horizon Rationale

Table 5 states N = 20 steps with rationale "≥ 2× longest delay (τ_d ≈ 440 s)." This is a common rule of thumb (van Overloop, 2006) but not a formal criterion. For MPC stability, the prediction horizon must exceed the settling time of the open-loop system, which for an integrating (Family α) system is theoretically infinite. The practical criterion is that N·Δt must be long enough for the MPC to "see" the delayed effect of its control action. Please either cite the formal basis (e.g., the delay-compensation condition in Litrico & Fromion, 2009, Ch. 5) or acknowledge this as a practical design choice validated by the MiL results.

### m4. Data-Driven §7.5: Safety Guarantees

The new §7.5 on data-driven approaches is welcome but makes a claim that deserves qualification: "data-driven controllers can be admitted within well-characterized ODD boundaries where their performance has been verified through extensive xIL testing." Verification through testing provides statistical confidence but not formal guarantees. This should be stated explicitly—testing-based certification is analogous to software testing (necessary but not sufficient for safety), whereas model-based MPC with constraint handling provides formal guarantees (feasibility ⇒ constraint satisfaction). The distinction matters for safety-critical water systems.

---

## Summary

This paper is developing well. The DfO paradigm and MBD framework are genuine contributions that will serve the CHS community. The three major issues (Gramian specification, five-level hierarchy mapping, IDZ identification) are all precision issues that can be resolved with additional paragraphs rather than structural changes. The writing quality and cross-disciplinary coverage (digital twins, ML, competency framework) are strong. I recommend minor revision.
