# Review Report — Paper P1a (WRR v14)

**Iteration**: 6 of 20+
**Reviewer**: A (Control Theorist) — European Professor, Automatic Control
**Date**: 2026-02-13

---

## Overall Assessment

I have now reviewed this manuscript three times (v11, v12, v14). The trajectory of improvement has been exemplary. My v12 review raised five major mathematical concerns; all were addressed substantively. The v13-v14 revisions, responding to Reviewers B and C, have further strengthened the paper by adding validation limitations honesty, SCADA integration depth, cross-sector transfer qualifications, propose-validate formalization, differentiable modeling connections, and published performance grounding for Prediction 1.

From a control-theoretic perspective, the paper is now mathematically sound within its explicitly stated scope. Remark 1 (Theorem 2 proof by enumeration) demonstrates intellectual honesty. The Taylor expansion validity bounds for Lemma 3 are rigorous. The robustness margin discussion after Theorem 3, citing published frequency-domain results, provides quantitative support. The P2-P6 scaling law, reframed from "optimality" to "characteristic behavior," is now correctly positioned. The propose-validate interface formalization with the candidate tuple C, confidence calibration, and watchdog mechanism is a well-specified architectural contribution.

My remaining concerns are minor and addressable. The paper has reached the quality threshold for WRR publication.

**Score: 9/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 9.5 | Unified TF family and Muskingum-IDZ duality are significant theoretical contributions |
| Mathematical Rigor | 8.5 | Substantially improved; Remark 1 honesty, Taylor bounds, robustness margins all strong |
| Reproducibility | 7 | MIT License commitment, Zenodo DOI, validation limitations paragraph — appropriate for theory paper |
| Case Validation | 6 | Validation limitations paragraph is the correct approach; published results cited for support |
| Literature Completeness | 9 | Comprehensive and well-integrated across control theory, AI/ML, and hydraulic engineering |
| Writing Quality | 9.5 | Notation consistent, mathematical exposition clear, honest about limitations throughout |
| System Differentiation | 9 | Strong positioning via Navier-Stokes analogy, differentiable modeling connection, and dual-engine architecture |

---

## Major Issues

### M1. Theorem 2 Proof Method — Open Problem Framing Could Be Sharper

Remark 1 (added in v12) honestly acknowledges that the Theorem 2 proof is verification by enumeration rather than derivation from first principles, and identifies the constructive proof as an open problem. This is the correct intellectual position. However, the framing of the open problem could be sharpened:

The open problem is essentially: "Under what minimal axioms on the Saint-Venant equations (or their pressurized equivalent) does the three-parameter family {A_s, τ_d, τ_m} emerge as the unique low-order SISO LTI approximation?" This is a model reduction problem in the classical sense of balanced truncation or moment matching. If the paper could state the open problem in these terms—connecting to established model reduction theory (Antoulas, 2005; Gugercin et al., 2008)—it would both sharpen the research direction and connect CHS to the broader systems and control community.

**Recommendation**: Add 1-2 sentences to Remark 1 connecting the open problem to classical model reduction theory. This is a minor refinement, not a structural change.

### M2. Propose-Validate Tuple Formalization — Dimensional Consistency

The v14 formalization specifies C = {J_new ∈ ℝⁿˣⁿ, g_new ∈ ℝᵐ, ODD_status ∈ {within, approaching, outside}}. Two small issues:

(a) J_new is described as a "quadratic cost matrix" but in standard MPC formulation, the cost function involves both a state weight matrix Q ∈ ℝⁿˣⁿ and an input weight matrix R ∈ ℝᵖˣᵖ. The tuple should either specify both matrices or clarify that J_new represents the full parameterization of the cost function (including reference trajectories, prediction horizon, etc.).

(b) g_new ∈ ℝᵐ is described as "the constraint vector," but constraints in MPC are typically inequality constraints g(x,u) ≤ 0, not a single vector. The constraint modification should specify which bounds are being changed (state bounds, input bounds, output bounds) and their structure.

These are precision issues, not conceptual errors. The propose-validate architecture itself is well-conceived.

**Recommendation**: Revise the tuple specification to either (a) use standard MPC notation (Q, R, x_ref, N, x_min, x_max, u_min, u_max) or (b) define J_new and g_new more carefully as parameterizations of the full cost and constraint functions.

### M3. Scaling Law f_b* and Prediction 3 — Reconciliation Now Adequate but Derivation Could Be Tighter

The v13 scaling law derivation in Section 5.3 and the v14 clarification of Prediction 3 thresholds are substantial improvements over earlier versions. The acknowledgment that the scaling law applies to a single isolated pool while Prediction 3 accounts for multi-pool coupling is the correct explanation for the discrepancy.

One remaining refinement: the derivation uses "A_s · Δy_max / ΔQ has dimensions of time and scales with τ_d for a pool operating near its design capacity." The scaling argument "scales with τ_d" is the weakest link—it is physically plausible but not derived. The relationship between A_s · Δy_max / ΔQ and τ_d depends on the specific canal geometry and operating point. For the scaling law to be rigorous, an explicit statement of the conditions under which this scaling holds (e.g., "for pools where the backwater length is comparable to the pool length") would close the logical gap.

**Recommendation**: Add a brief qualifying condition to the scaling argument, specifying when A_s · Δy_max / ΔQ ~ τ_d holds. This is a one-sentence addition.

### M4. DMPC Stability and Convergence Guarantees — Implicit Assumption

Section 6.2 describes the DMPC coordination protocol (local MPC + boundary exchange + iteration until convergence). The convergence criterion is stated as "practical convergence" in 3-5 iterations, citing Negenborn et al. (2009). However, the paper does not discuss under what conditions the DMPC protocol is guaranteed to converge, or whether the converged solution satisfies constraint guarantees.

This is a well-known challenge in DMPC: convergence of iterative neighbor-to-neighbor schemes depends on the coupling strength between subsystems. For strongly coupled canals (small pools with large flows), the coupling can be strong enough to prevent convergence or cause constraint violation in the converged solution. The paper's assertion that "total complexity is O(n · N³ · J)" assumes convergence within J iterations—what if it doesn't converge?

**Recommendation**: Add 2-3 sentences acknowledging the DMPC convergence assumption and the conditions under which it is expected to hold (e.g., "for pools where decoupling time horizon T_suf > T_comm, the coupling between adjacent MPC problems is sufficiently weak for convergence within 3-5 iterations"). Connect this to the P2-P6 tradeoff: stronger decoupling (larger f_b) improves DMPC convergence.

### M5. Differentiable IDZ Models — Identifiability Concern

The v14 addition on differentiable modeling is a valuable forward-looking connection. However, the claim that "differentiable IDZ models would enable automatic calibration of {A_s, τ_d, τ_m}" has an identifiability subtlety: the IDZ transfer function G(s) = (1 + τ_m·s)·e^(-τ_d·s)/(A_s·s) has three parameters, but not all three are independently identifiable from typical operational data (water level measurements under flow disturbances). Specifically, τ_m and τ_d can exhibit parameter correlation when the delay is estimated from noisy data. Horváth et al. (2024) addressed this by constraining the identification procedure. The paper should note this identifiability caveat.

**Recommendation**: Add a brief note: "Parameter identifiability of the three-parameter family {A_s, τ_d, τ_m} from operational data requires sufficiently rich excitation signals; correlation between τ_m and τ_d under low-frequency disturbances may necessitate constrained identification procedures (Horváth et al., 2024)."

---

## Minor Issues

### m1. Equation Numbering Consistency
The equations appear as embedded images (from the original docx conversion). While this is noted as an ongoing formatting issue, it prevents precise cross-referencing. The validation limitations paragraph references "Section 4.5" but the specific equations for Lemma 3 validity bounds are not numbered. For the final submission, all equations should be in LaTeX with sequential numbering.

### m2. Remark 1 Placement
Remark 1 is placed after the Theorem 2 proof, before Section 4.4. This is the mathematically correct position. However, some readers may miss it because it interrupts the flow of the model hierarchy exposition. Consider adding a forward reference in the Theorem 2 statement itself: "Theorem 2 (proved by enumeration; see Remark 1 for discussion of proof methodology)."

### m3. Table 3 (Eight Principles) — Missing Tradeoff Quantification Column
Table 3 summarizes the eight principles with a "Primary Tradeoff" column. Given that the P2-P6 tradeoff now has a quantitative scaling law, consider adding a "Quantitative Metric" column to Table 3, even if only the P2-P6 row is populated. This signals that CHS aspires to quantitative tradeoff analysis, not merely qualitative taxonomy.

### m4. Reference List — van Overloop et al. (2010)
The v14 revision added van Overloop et al. (2010) as a citation for Prediction 1 grounding. Verify that the full reference (journal, volume, pages) is included in the reference list. The most likely reference is: van Overloop, P.J., Clemmens, A.J., Strand, R.J., Wagemaker, R.M., & Bautista, E. (2010). Real-time implementation of model predictive control on Maricopa-Stanfield Irrigation and Drainage District's WM Canal. ASCE Journal of Irrigation and Drainage Engineering, 136(11), 747-756.

### m5. Notation: W vs. Q for LQR Weight
The v12 revision changed the LQR state weight from Q to W to avoid collision with flow rate Q. This is a reasonable choice, but W is sometimes used for the process noise covariance in Kalman filtering (which is mentioned in Table 3). Verify that no notational collision is introduced elsewhere in the paper.

---

## Reference Audit

### Verified:
- Litrico & Fromion (2004/2009): ✓ Frequency-domain IDZ validation — correctly cited
- Horváth et al. (2024): ✓ WRR — IDZ-MPC identification and performance
- Guo et al. (2017): ✓ ICML — confidence calibration — appropriate for Cognitive Intelligence
- Li et al. (2021): ✓ ICLR — Fourier Neural Operator — appropriate for differentiable modeling
- Negenborn et al. (2009): ✓ DMPC convergence — correctly cited

### Suggested Addition:
- Antoulas, A.C. (2005). Approximation of Large-Scale Dynamical Systems. SIAM. — For connecting the Theorem 2 open problem to classical model reduction theory (M1)

---

## Summary

This paper has reached publication quality for WRR. The core theoretical contributions—unified transfer function family (Theorem 2), Muskingum-IDZ duality (Corollary 1), eight-principle framework with quantitative tradeoffs, MAS architecture with formalized propose-validate interface, and WSAL classification with measurement protocols—are original, significant, and well-presented.

The mathematical exposition is now honest and rigorous within its stated scope. The Remark 1 acknowledgment of proof methodology, the Taylor expansion validity bounds, the robustness margin discussion, the validation limitations paragraph, and the explicit qualification of cross-sector transfer claims all demonstrate the intellectual maturity expected of a framework paper in a leading journal.

My five major issues are refinements rather than structural concerns: sharpening the open problem framing, tightening the tuple specification, adding a scaling condition, acknowledging DMPC convergence assumptions, and noting parameter identifiability. These are all addressable in a final revision pass.

**I recommend acceptance with minor revisions.**
