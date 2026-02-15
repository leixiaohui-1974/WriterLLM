# Review Report — Paper P1a (WRR v11)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European IEEE Fellow, distributed control systems
**Date**: 2026-02-13

---

## Overall Assessment

This manuscript is an ambitious theoretical contribution proposing a unified control-theoretic framework (CHS) for water network operations. After two rounds of revision, the paper has improved considerably: the Key Points and Abstract now meet WRR formatting standards, Section 7.5 addresses SCADA integration, Section 8.4 positions CHS relative to data-driven approaches, and the Proposition 1 scope/limits paragraph is a welcome addition.

The core mathematical contributions—particularly Theorem 2 (unified transfer function family) and Corollary 1 (Muskingum-IDZ duality)—are the paper's strongest elements and represent genuine advances. However, as a control theorist, I identify several issues of mathematical precision and notation consistency that should be addressed before the paper can serve as the foundational reference it aspires to be.

**Score: 8/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 9 | Unified TF family is a genuine contribution to the field |
| Mathematical Rigor | 7.5 | Theorem 2 is solid but notation inconsistencies need fixing |
| Reproducibility | 5.5 | Analytical examples are clear; code availability commitment is positive |
| Case Validation | 4.5 | Still no numerical validation; acknowledged as limitation |
| Literature Completeness | 8 | Significantly improved with v11 additions (Kratzert, Castelletti, Bommasani) |
| Writing Quality | 8.5 | Excellent clarity for this level of mathematical density |
| System Differentiation | 8.5 | Scope/limits paragraph and Section 8.4 substantially improve positioning |

---

## Major Issues

### M1. Notation Inconsistency Between Family α and Family β Parameters

Theorem 2 defines Family α with parameters (Aₛ, τᵈ, τₘ) and Family β with parameters (Kₛ, τᵈ', τₘ'). The use of primes (') on the Family β parameters is confusing because it implies these are transformed versions of the same physical quantities—which they are not. The transport delay τᵈ in Family α and τᵈ' in Family β are physically different quantities (downstream vs. upstream wave travel time, depending on boundary conditions), yet the notation suggests they are the same parameter with a small perturbation.

**Recommendation**: Use distinct, unprimed notation for Family β parameters. For example, use Kₛ, τ_d^β, τ_m^β or introduce entirely distinct symbols. Alternatively, unify the notation by defining a single delay parameter τ with subscripts indicating direction, and show how the same physical channel yields different effective values depending on boundary type.

### M2. Theorem 2 "Proof" Structure

Theorem 2 is stated as a theorem but proved via Lemma 1 (subsumption table) and Corollary 1 (duality bridge). However, Lemma 1 is essentially a verification by enumeration—showing that known models fit the family—rather than a derivation from first principles. A true proof of Theorem 2 would require showing that *any* SISO LTI model derived from the diffusion wave equation (Equation 1) via spatial lumping necessarily takes the form of Family α or β. The current proof strategy is sufficient for a survey/framework paper, but the distinction should be acknowledged.

**Recommendation**: Add a remark after the proof of Theorem 2 explicitly stating: "Theorem 2 is verified by exhaustive enumeration of all known SISO LTI models in the water systems literature (Lemma 1) combined with the duality bridge (Corollary 1). A constructive proof from the diffusion wave equation, showing that spatial lumping necessarily yields the Family α/β structure, remains an open problem." This is intellectually honest and identifies a concrete open problem for the community.

### M3. The Quantitative P2-P6 Tradeoff (Section 5.3) Needs Tightening

The v11 addition of the quantitative P2-P6 tradeoff derivation is a good step, but the mathematical treatment has gaps:

(a) The expression "f_b ≥ ΔQ·T_comm/(V_total·Δy_max/y_range)" introduces y_range without prior definition. What is y_range? Is it hmax - hmin? This should be defined.

(b) The jump from the constraint inequality to "f_b* ≈ min(1, τ_d/T_comm)" is not justified. How does the storage capacity V_total cancel out? The intermediate steps should be shown explicitly, or the derivation should be presented as a scaling argument rather than a formal optimality claim.

(c) The statement "optimal buffer fraction follows" uses "optimal" without specifying the optimality criterion. Optimal with respect to what objective? Minimizing total water level deviation? Minimizing coordination communication? The criterion should be stated.

**Recommendation**: Either expand the derivation with full intermediate steps, or reframe it as an approximate scaling law ("the buffer fraction scales as f_b ~ τ_d/T_comm") rather than an optimality result. The latter is arguably more useful as a design heuristic and avoids overstating the rigor of the derivation.

### M4. Model-Layer Correspondence (Theorem 3) — Constructive Criterion Missing

Theorem 3 assigns model levels to control layers but does not provide a constructive criterion for determining which model level is "sufficient fidelity for its temporal scope." The current statement is prescriptive ("Layer 1 shall use Level 4") but does not explain *why* Level 4 is sufficient for Layer 1 and not Level 3 or Level 5. What is the quantitative error budget?

For example: at Layer 1 (minute-scale MPC), the IDZ model (Level 4) neglects high-frequency modes above ω > 1/τ_d. For the MPC to remain stable, the neglected dynamics must satisfy a robustness margin condition—e.g., the H∞ norm of the multiplicative uncertainty must be bounded. This kind of constructive criterion would transform Theorem 3 from a design prescription to a principled selection rule.

**Recommendation**: Add at least a qualitative discussion of the robustness margin argument, and identify the formal development of a constructive model selection criterion as an open problem.

### M5. Lemma 3 (Actuator Reduction) — Linearization Validity

Lemma 3 claims all actuators linearize to ΔQ = αΔu + β_up·ΔH_up + β_dn·ΔH_dn. The v11 revision added a note about validity ranges (±20% for gates/valves, ±15% for pumps near BEP). These numbers appear to be approximate engineering rules of thumb rather than formally derived bounds.

For a paper of this theoretical ambition, the linearization error should be characterized more precisely: what is the relative error of the linearized model as a function of operating point deviation? Even a brief sketch of the Taylor expansion argument (showing that the quadratic terms are bounded by some factor of the operating range) would strengthen the claim.

**Recommendation**: Add 1-2 sentences giving the mathematical basis for the validity range claims (e.g., "For a sluice gate with the standard Torricelli discharge equation, the second-order Taylor term is bounded by (Δu/u₀)² · Qmax/4, which yields <5% relative error for |Δu/u₀| < 0.2").

---

## Minor Issues

### m1. Definition 1 (Operational Singularity) — "Singularity" Terminology
The term "singularity" in control theory typically refers to a mathematical singularity (pole, zero, degenerate Jacobian). Using it to mean "unique combination of properties" may confuse control theory readers. A footnote distinguishing the CHS usage from the standard mathematical usage would be helpful.

### m2. Section 4.1 — Diffusion Wave Equation Presentation
Equation (1) (diffusion wave equation) is presented as an image rather than rendered LaTeX. For the foundational equation of the entire hierarchy, this should be in editable mathematical notation. The same applies to Equation (2) (hydraulic diffusivity).

### m3. Corollary 1 Proof — Base64 Image
The proof of Corollary 1 (the core Muskingum-IDZ duality result) includes the key algebraic manipulation as a base64-encoded image. This must be converted to proper mathematical notation for the final manuscript—the mathematical derivation at the heart of the paper's most novel claim should not be an opaque image.

### m4. Section 6.1 — LQR Design Notation
The LQR design in Section 6.1 uses Q for the state weight matrix, which conflicts with Q used throughout the paper for flow rate. Use a different symbol (e.g., W or Γ) for the LQR weight matrix to avoid confusion.

### m5. Section 8.4 — Structural Mechanics Analogy
The closing analogy in Section 8.4 ("CHS is to data-driven methods as structural mechanics is to FEA software") is effective but slightly imprecise. FEA is a numerical method for solving structural mechanics equations, not a competing theory. A more precise analogy might be: "CHS is to data-driven hydrology as the Navier-Stokes equations are to turbulence models—the theory defines what must hold, the models provide practical approximations."

---

## Reference Audit

### Verified:
- Bolea, Puig & Grau (2014): ✓ Confirmed; correctly identified as partial precedent for Muskingum-IDZ connection
- Horváth et al. (2024): ✓ Confirmed; excellent empirical support for model hierarchy
- Kratzert et al. (2019): ✓ Confirmed; appropriate for data-driven positioning
- Castelletti et al. (2010): ✓ Confirmed; appropriate for RL discussion

### Suggestions:
- Consider citing Dochain et al. (2009) "Automatic Control of Bioprocesses" as a cross-domain comparison for the claim that water systems are uniquely challenging among distributed parameter systems
- Consider citing Ferrante & Colanero (2004) or similar for formal analysis of linearization errors in water hammer equations, to support the Lemma 3 validity discussion

---

## Summary

The paper continues to improve with each iteration. The core mathematical contributions (Theorem 2, Corollary 1) are genuinely novel and well-presented. The main remaining issues are of mathematical precision rather than conceptual substance: notation consistency between the two families, honest characterization of the Theorem 2 proof method, tightening of the P2-P6 derivation, and a constructive criterion for model-layer selection. The equation rendering issue (base64 images instead of LaTeX) is a production concern but should be addressed before final submission.

This paper is close to acceptance. With these revisions, it will serve as a rigorous foundational reference.
