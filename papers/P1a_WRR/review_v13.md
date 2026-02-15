# Review Report — Paper P1a (WRR v12)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — Water Utility CTO, USA
**Date**: 2026-02-13

---

## Overall Assessment

The manuscript has improved substantially since my first review (v9). The Key Points and Abstract now meet WRR formatting standards. The SCADA integration discussion in Section 7.5 addresses my earlier concern about practical deployment pathways. The notation cleanup (Family α/β superscripts), the honest Remark 1 about the Theorem 2 proof method, and the tightened P2-P6 scaling law all demonstrate responsiveness to reviewers. The paper is clearly moving toward a publishable state.

However, as an engineering practitioner, I remain concerned about the gap between theoretical elegance and field deployability. Three iterations in, the paper still contains zero numerical validation—every "illustrative application" (Section 6) uses analytical predictions from linearized models with no comparison against nonlinear benchmarks. For a framework paper that makes four quantitative predictions, this continues to be the most significant weakness. Additionally, the SCADA integration discussion, while welcome, remains at a conceptual level without addressing concrete failure scenarios that any field engineer would immediately ask about.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 9 | Unified TF family and Muskingum-IDZ duality remain genuinely significant |
| Mathematical Rigor | 8 | Substantially improved with Remark 1 honesty, scaling law reframing, and Taylor expansion bounds |
| Reproducibility | 6 | Code commitment improved; but still no numerical results to reproduce |
| Case Validation | 5 | Improved from 4→5 with the Taylor expansion validity bounds and robustness margin discussion; still no simulation data |
| Literature Completeness | 8.5 | Kratzert, Castelletti, Bommasani additions well-placed; cross-domain positioning strong |
| Writing Quality | 9 | Notation now consistent; mathematical density well-managed; structure excellent |
| System Differentiation | 9 | Section 8.4 complementarity argument is compelling; Navier-Stokes analogy effective |

---

## Major Issues

### M1. Persistent Absence of Numerical Validation — The Central Remaining Weakness

This was my M1 in the v9 review. Three iterations later, the paper still contains no numerical simulation results. Section 6 states: "The results presented are analytical predictions derived from the linear reduced-order models of Section 4; full nonlinear simulation validation against Saint-Venant benchmarks is deferred to a companion computational paper."

I understand the scope management argument—this is a theoretical framework paper, not a computational paper. However, the disconnect between theory and evidence has now become the paper's defining limitation:

- Prediction 1 claims "at least 30% RMS improvement." The justification now references published canal control benchmarks (Clemmens & Schuurmans, 2004), which is better than v9, but no CHS-specific result supports this figure.
- The Taylor expansion validity bounds for Lemma 3 (v12 addition) are mathematically sound (<1% error for gates at ±20%, <3.4% for pumps at ±15%), but these are *local* linearization errors. They do not demonstrate that the *integrated system behavior*—MPC operating over multiple steps with cascading disturbances—remains within these bounds.
- The robustness margin discussion after Theorem 3 cites published frequency-domain comparisons (Litrico & Fromion, 2004; Horváth et al., 2024) showing |Δ(jω)| < 0.3 for ω < 1/(3τ_d). This is the closest the paper comes to quantitative validation, but it relies entirely on others' results for different specific systems.

**Recommendation**: At minimum, include a single time-domain simulation comparison for the single-pool LQR case (Section 6.1): compute the step response of the IDZ-LQR controller applied to a full Saint-Venant model of the same trapezoidal channel (using any open-source solver—SIC, OpenFOAM, HEC-RAS), and compare the settling time and overshoot against the IDZ model prediction. Even a rough comparison showing qualitative agreement would significantly strengthen the paper. If this truly cannot be included, add an explicit "Validation Limitations" paragraph at the end of Section 6 acknowledging the gap and specifying what companion papers will address.

### M2. SCADA Integration (Section 7.5) — Conceptual but Not Operational

The v11 addition of Section 7.5 is a welcome step. However, the discussion remains at the level of architecture description rather than operational engineering. Three gaps from a field deployment perspective:

(a) **Failure mode interaction**: The paper states "CHS Layer 0 interlocks operate in parallel with (not in replacement of) existing safety systems. The more conservative threshold prevails." This sounds clean in theory, but in practice it creates a non-trivial arbitration problem. When two independent safety systems have overlapping jurisdiction, conflicting thresholds can cause oscillatory behavior (one system opens a gate, the other closes it). How is threshold reconciliation handled during commissioning? The xIL framework is mentioned but not at sufficient detail for this specific problem.

(b) **Cybersecurity**: The paper proposes OPC-UA as the communication backbone, which is appropriate. But any networked control system on water infrastructure is a cybersecurity target (cf. the 2021 Oldsmar, Florida water treatment incident). The paper should at least acknowledge the cybersecurity implications of connecting HDC controllers to SCADA networks and reference relevant standards (IEC 62443, NIST SP 800-82).

(c) **Operator transition**: The WSAL-2→3 transition is correctly identified as the critical milestone, but the human factors dimension is underdeveloped. The paper mentions "the 'letting go' moment" but doesn't discuss how operators are trained and supported through this transition. In my experience, the technical capability is often ready before the operators are. What is the CHS position on operator training, decision support interfaces, and the transition period where both manual and automated systems coexist?

**Recommendation**: Expand Section 7.5 with 2-3 sentences on each gap: (a) threshold reconciliation protocol during commissioning; (b) cybersecurity acknowledgment and relevant standards; (c) operator transition support through the WSAL-2→3 boundary.

### M3. Cross-Sector Transfer Claims (Section 6.3) Need Quantitative Backing

Section 6.3 demonstrates cross-sector transfer through re-parameterization: canal → reservoir → urban pressure zone. The mathematical argument is elegant—the same Integrator model applies with different physical parameters. However, from an engineering standpoint, the claim "No algorithmic modification is required" hides significant practical complexity:

(a) For the urban pressure zone transfer, the transport delay τ_d = L/a drops from hours to seconds. This means the MPC sampling period must change by 2-3 orders of magnitude (from ~300s to ~1-10s). While the algorithm is "identical," the computational requirements, communication latency tolerances, and actuator response characteristics are fundamentally different. This should be acknowledged explicitly.

(b) The reservoir transfer uses A_h (surface area at operating level) as if it were constant. In practice, reservoir area-elevation curves are strongly nonlinear—for a typical V-shaped valley, A_h can vary by 5:1 over the operational range. This breaks the linear model assumption far more severely than the ±20% gate operating range. How should CHS handle reservoirs with strongly nonlinear storage characteristics?

(c) Prediction 2 states that the same MPC controller will achieve "settling time within 50% and steady-state error within 200%" across sectors. These are very generous tolerances—200% steady-state error degradation means the error could triple. Is this actually useful for operational purposes? A clearer statement of what "transferability" means in engineering terms would strengthen the prediction.

**Recommendation**: Add qualifying statements to Section 6.3 acknowledging the practical differences in time scale, nonlinearity, and performance tolerance across sectors. Revise Prediction 2's tolerance bounds with explicit engineering justification.

### M4. WSAL Transition Criteria (Table 6) — Not Yet Measurable

The v11 revision added measurable transition criteria to Table 6, which was a good step. However, some criteria remain ambiguous:

- "WSAL-2→3: Full xIL certification for normal-flow ODD; operator intervention rate <5% within certified ODD." What is the measurement period? <5% over one day is very different from <5% over one year. What constitutes an "intervention"—any manual override, or only safety-critical overrides?
- "WSAL-3→4: ODD covers >80% of operating scenarios." How are "operating scenarios" enumerated and weighted? By time duration? By frequency of occurrence? By consequence severity?
- "WSAL-4→5: Full-envelope ODD with self-expanding capability; zero human intervention under all certified scenarios." "Zero" is an absolute claim. What is the statistical confidence level? Over what time horizon?

**Recommendation**: Add a brief methodological note (2-3 sentences) specifying the measurement protocol for WSAL transition metrics: measurement period, intervention definition, scenario enumeration method, and statistical confidence requirements.

### M5. Open Research Statement Needs Strengthening

The Open Research section states: "Illustrative MPC code implementing the IDZ-based single-pool controller of Section 6.1 and the distributed MPC of Section 6.2 will be deposited in a public repository upon acceptance." This is a conditional commitment. WRR increasingly expects code and data availability at review time, not conditional on acceptance.

**Recommendation**: If possible, deposit a preliminary version of the MPC code in a public repository (e.g., Zenodo, GitHub) now and provide the DOI. If not, specify the repository and license under which the code will be released, and provide a timeline.

---

## Minor Issues

### m1. Table 6 WSAL Transition Criteria Formatting
The WSAL transition criteria added in v11 are mentioned in the response document but not visible in the current Table 6 within the draft. Verify that the measurable criteria (operator intervention rate, ODD coverage %, etc.) are actually present in the table or in accompanying text.

### m2. Section 6.1 LQR Example — Practical Relevance
The LQR design example uses Q₀ = 30 m³/s for a 10 km trapezoidal pool. While mathematically illustrative, LQR is rarely used in operational canal control (MPC dominates due to constraint handling). The paper should note that the LQR example is pedagogical, demonstrating the IDZ model's fitness for control design, and that MPC is the recommended operational approach.

### m3. Prediction 4 Timeline Specificity
Prediction 4 states WSAL-3 certification "within three years of initial deployment." This is a remarkably specific timeline claim for a theoretical paper. What evidence supports this timeline? If it is based on automotive autonomy deployment experience, this should be stated. If it is aspirational, it should be qualified.

### m4. Section 5.3 — "Characteristic Buffer Fraction" vs. "Optimal"
The v12 revision correctly replaced "optimal buffer fraction" with "characteristic buffer fraction" (per Reviewer A's M3). However, Section 6.2 still references "the optimal buffer fraction" in the DMPC discussion (line 1032). This inconsistency should be resolved.

### m5. Acknowledgments Still Incomplete
The Acknowledgments section still contains "Grant Nos. [to be inserted]." While this may be normal for pre-submission review, it should be noted for the record.

---

## Reference Audit

### Verified:
- Clemmens & Schuurmans (2004): ✓ Confirmed; appropriate benchmark for canal MPC performance
- Negenborn et al. (2009): ✓ Confirmed; standard DMPC reference
- Maestre & Negenborn (2014): ✓ Confirmed; comprehensive DMPC overview
- Rasheed et al. (2020): ✓ Confirmed; digital twin survey, appropriate
- Karniadakis et al. (2021): ✓ Confirmed; PINN review, appropriate

### Suggestions:
- Consider citing Eker & Kara (2003) or similar for PLC safety interlock standards in water systems, to support the Layer 0 discussion
- Consider citing Panguluri et al. (2017) "Cyber-Physical Security of Water and Wastewater Infrastructure" or AWWA's cybersecurity guidance to support the cybersecurity gap identified in M2(b)
- Consider citing Hashimoto et al. (1982) "Reliability, Resiliency, and Vulnerability Criteria for Water Resource System Performance Evaluation" — the resilience tetrad discussion (Section 5.2) would benefit from connecting to this classic water systems performance framework

---

## Summary

The paper has improved significantly across four iterations. The core theoretical contributions (Theorem 2, Corollary 1) are now well-presented with honest characterization of proof methods and limitations. The mathematical revisions from iteration 3 (notation, scaling law, Taylor expansion bounds, robustness margins) are solid improvements. The writing quality is excellent.

The remaining issues are primarily of engineering substance rather than theoretical weakness: (1) the persistent absence of any numerical validation remains the paper's most significant gap for WRR readership; (2) the SCADA integration discussion needs operational depth; (3) the cross-sector transfer claims need quantitative qualification; and (4) the WSAL metrics need measurement protocol specification. These are addressable within one more revision cycle.

This paper is very close to acceptance. The theoretical framework is sound and genuinely novel. Addressing the validation gap—even minimally—would remove the last significant barrier.
