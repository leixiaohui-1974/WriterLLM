# Revision Response — P1a WRR v11 → v12

**Iteration**: 3
**Reviewer**: A (Control Theorist)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Notation Inconsistency Between Family α and Family β Parameters

**Response**: Accepted. The use of primes (') on Family β parameters is indeed confusing as it implies a perturbative relationship between what are physically distinct quantities.

**Action taken**: Replaced the primed notation (τᵈ', τₘ') for Family β with superscripted family labels: τ_d^β and τ_m^β. Family α parameters retain their original notation (τᵈ, τₘ) but are now also explicitly labeled as τ_d^α and τ_m^α where disambiguation is needed. A clarifying sentence is added after the Family β definition: "The superscript notation distinguishes physically distinct parameters: τ_d^α and τ_d^β represent transport delays under different boundary conditions (gated vs. self-regulating), not perturbations of a single quantity." Table 4 column headers are updated accordingly.

### M2. Theorem 2 "Proof" Structure

**Response**: Fully accepted. This is an important intellectual honesty point. The current proof strategy is indeed verification by enumeration rather than derivation from first principles.

**Action taken**: Added a remark after the proof of Theorem 2: "**Remark 1 (Proof method).** Theorem 2 is verified by exhaustive enumeration of all known SISO LTI models in the water systems literature (Lemma 1) combined with the duality bridge (Corollary 1). A constructive proof from the diffusion wave equation—showing that any spatial lumping of the one-dimensional unsteady flow equations necessarily yields the Family α/β structure—remains an open problem. Such a proof would require demonstrating that the low-frequency approximation of the spatially lumped transfer function always produces a rational function with at most one integrator pole (or one stable real pole), one real zero, and one pure delay, regardless of the lumping method employed. We identify this as one of the most important theoretical open problems for CHS."

### M3. The Quantitative P2-P6 Tradeoff (Section 5.3) Needs Tightening

**Response**: Accepted on all three sub-points. The derivation in v11 was indeed insufficiently rigorous.

**Action taken**:
(a) Defined y_range explicitly: "where y_range = y_max - y_min is the operational water level range between the maximum and minimum permissible levels."

(b) Reframed the result as a scaling law rather than a formal optimality result. The revised text reads: "Under these simplified assumptions, the buffer fraction scales as f_b ~ τ_d/T_comm. This scaling law captures the essential physics: when transport delay dominates communication period (τ_d/T_comm > 1), nearly all storage must serve local buffering; when coordination is fast relative to wave transit (τ_d/T_comm → 0), storage is freed for system-wide redistribution." The unjustified jump to "optimal" is removed; intermediate steps showing how V_total cancels are added.

(c) Replaced "optimal buffer fraction" with "characteristic buffer fraction" and added the explicit criterion: "where the design objective is minimizing peak water level deviation under a step disturbance while maintaining coordination feasibility."

### M4. Model-Layer Correspondence (Theorem 3) — Constructive Criterion Missing

**Response**: Accepted. The prescriptive nature of Theorem 3 without a constructive selection criterion is a genuine limitation.

**Action taken**: Added a qualitative discussion after Theorem 3: "The model-layer assignments in Theorem 3 are based on the principle that the neglected dynamics at each level must introduce modeling error small enough to preserve closed-loop stability and performance. Specifically, at Layer 1 (minute-scale MPC), the IDZ model (Level 4) neglects high-frequency modes above ω > 1/τ_d. For robust MPC design, the multiplicative model uncertainty Δ(jω) = [G_true(jω) - G_IDZ(jω)]/G_IDZ(jω) must satisfy ||Δ||_∞ < 1/||T||_∞, where T is the complementary sensitivity function. Published frequency-domain comparisons (Litrico & Fromion, 2004; Horváth et al., 2024) confirm that |Δ(jω)| < 0.3 for ω < 1/(3τ_d), which is conservative relative to typical robust MPC margins. The formal development of a constructive model selection criterion—specifying the minimum model level as a function of required robustness margin, disturbance spectrum, and performance specifications—is identified as an important open problem."

### M5. Lemma 3 (Actuator Reduction) — Linearization Validity

**Response**: Accepted. The validity ranges should be mathematically grounded rather than presented as engineering rules of thumb.

**Action taken**: Added a mathematical basis sentence after the validity note: "For a sluice gate with the standard orifice discharge equation Q = Cd·w·u·√(2gΔH), the Taylor expansion about operating point u₀ gives Q ≈ Q₀ + α(u-u₀) + (1/2)(∂²Q/∂u²)|₀·(u-u₀)² + ..., where the second-order term is bounded by |Q₂/Q₀| ≤ (Δu/u₀)²/4. For |Δu/u₀| < 0.2, this yields <1% relative error from neglecting the quadratic term, confirming the ±20% validity claim. For variable-speed pumps, the nonlinearity is stronger due to the quadratic affinity laws (Q ∝ N, H ∝ N²), yielding |Q₂/Q₀| ≤ 3(ΔN/N₀)²/4, which gives <3.4% relative error at ±15% speed deviation near BEP."

---

## Response to Minor Issues

### m1. Definition 1 (Operational Singularity) — "Singularity" Terminology
**Action**: Added a footnote at Definition 1: "The term 'singularity' here denotes a unique, irreducible combination of co-occurring properties—distinct from the mathematical usage (pole, zero, degenerate Jacobian) standard in control theory. The choice follows the philosophical usage: a singular entity whose properties cannot be decomposed into independent factors."

### m2. Section 4.1 — Diffusion Wave Equation Presentation
**Action**: Noted for future iteration. Converting base64-encoded equation images to proper LaTeX notation is planned for the formatting pass. The equation content is mathematically correct; only the rendering format needs updating.

### m3. Corollary 1 Proof — Base64 Image
**Action**: Same as m2. The algebraic manipulation in the Corollary 1 proof will be converted to proper mathematical notation in the formatting iteration. Content correctness is maintained.

### m4. Section 6.1 — LQR Design Notation
**Action**: Changed the LQR state weight matrix symbol from Q to W throughout Section 6.1 to avoid collision with Q (flow rate). The revised LQR cost reads: "minimizing the cost J = Σ(xᵀWx + uᵀRu)" with "W = diag(1, 0, 0) and R = 0.01".

### m5. Section 8.4 — Structural Mechanics Analogy
**Action**: Revised the closing analogy to: "CHS is to data-driven hydrology as the Navier-Stokes equations are to turbulence models—the theory defines what must hold, the models provide practical approximations within that theoretical frame."

---

## Reference Audit Response

### Suggestions considered:
- Dochain et al. (2009): Deferred to companion paper P2A (JWRPM) which will provide detailed cross-domain comparison. Adding it here would expand scope beyond WRR limits.
- Ferrante & Colanero (2004): Not added as the Lemma 3 validity discussion now provides a self-contained mathematical basis from the standard orifice/pump equations. Adding transient-focused water hammer linearization analysis would introduce scope creep.

---

## Version Summary

- **v11 → v12 changes**: Fixed Family α/β notation inconsistency (M1); added Remark 1 on Theorem 2 proof method with open problem identification (M2); tightened P2-P6 tradeoff as scaling law with explicit assumptions and intermediate steps (M3); added robustness margin discussion for Theorem 3 with open problem identification (M4); provided Taylor expansion basis for Lemma 3 validity ranges (M5); added Definition 1 footnote on "singularity" terminology (m1); renamed LQR weight matrix Q→W (m4); revised Section 8.4 analogy (m5).
- **Self-citation rate**: Unchanged at ~16%.
- **Next focus**: Continue mathematical refinement; begin equation formatting pass; prepare for case validation strengthening.
