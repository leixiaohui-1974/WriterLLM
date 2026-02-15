# Review Report — Paper P1a (WRR v9)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — Water Utility CTO, USA
**Date**: 2026-02-13

---

## Overall Assessment

This paper proposes Cybernetics of Hydro Systems (CHS) as a unified control-theoretic framework for water network operations. The ambition is extraordinary: to provide a single theoretical foundation spanning irrigation canals, hydropower cascades, urban water distribution, inland waterways, and inter-basin transfers. The paper is well-structured, technically dense, and clearly written. The author demonstrates deep command of both control theory and hydraulic engineering.

**Score: 7/10**
**Verdict: Major Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | The unification of IDZ and Muskingum as dual representations is genuinely original and theoretically significant |
| Mathematical Rigor | 7 | Theorem 2 is well-formulated; however, Proposition 1's "structural isomorphism" needs tighter formal treatment |
| Reproducibility | 5 | The illustrative applications (Section 6) rely entirely on analytical predictions without any numerical validation |
| Case Validation | 4 | No real-world case data; all examples are hypothetical parametric demonstrations |
| Literature Completeness | 7 | Comprehensive for the core domains, but gaps exist (see below) |
| Writing Quality | 8 | Excellent academic writing, clear structure, effective use of tables |
| System Differentiation | 7 | Good positioning vs. prior work, though Section 8 could be sharper |

---

## Major Issues (≥5)

### M1. Absence of Numerical Validation Against Saint-Venant Benchmarks
The paper explicitly states (Section 6, line 994): "full nonlinear simulation validation against Saint-Venant benchmarks is deferred to a companion computational paper." For a WRR paper proposing a **unified theoretical framework**, this deferral is problematic. At minimum, one of the three illustrative applications (preferably the multi-pool DMPC of Section 6.2) should include a comparison of the linear reduced-order IDZ model predictions against a full Saint-Venant simulation to demonstrate that the order reduction is quantitatively valid under the stated operating conditions. Without this, Prediction 1 (30% RMS improvement) and Prediction 2 (cross-sector transfer within stated tolerances) remain unsubstantiated claims.

**Recommendation**: Add at least one nonlinear simulation benchmark comparison for the multi-pool case. If the companion paper is not yet published, include a simplified validation as supplementary material.

### M2. SCADA/PLC Integration Feasibility Not Addressed
Section 7 introduces a four-layer HDC architecture with Layer 0 safety interlocks on PLCs, Layer 1 MPC regulation, Layer 2 DMPC coordination, and Layer 3 planning. However, there is no discussion of how this architecture interfaces with existing SCADA/RTU/PLC infrastructure. From an operational perspective:
- How does the MPC at Layer 1 communicate with existing SCADA systems?
- What communication protocols are assumed (OPC-UA, IEC 61131-3, Modbus)?
- What are the computational requirements for real-time MPC at 300s sampling on field-grade hardware?
- How does the "Layer 0 veto" interact with existing PLC safety logic that may use different threshold definitions?

**Recommendation**: Add a subsection to Section 7 (or an appendix) discussing the practical integration pathway with existing SCADA infrastructure, including communication protocols, computational platforms, and failure mode handling.

### M3. The Muskingum-IDZ Duality Proof (Section 4.3) Needs Stronger Conditions Statement
Corollary 1 claims that the Muskingum transfer function is the "first-order MacLaurin approximation of a self-regulating IDZ." While the mathematical manipulation appears sound, the conditions under which this approximation is valid are not explicitly stated. Specifically:
- What is the frequency range over which the approximation holds?
- What is the maximum acceptable error in gain and phase at the control-relevant frequencies?
- The Muskingum method is inherently a lumped-parameter routing model; the IDZ is a frequency-domain canal pool model. The claim that they are "dual representations of the same physics" requires more careful treatment of the different physical assumptions (e.g., downstream boundary conditions, lateral inflow treatment).

**Recommendation**: Add explicit error bounds or validity conditions for the Muskingum-IDZ duality, ideally with a Bode plot comparison showing the frequency range where the approximation is accurate.

### M4. Self-Citation Rate Needs Verification
The paper cites Lei (2025a-d) extensively throughout. While self-citation is appropriate when building on prior work, the rate should be verified to stay within the 15-25% target. A preliminary count suggests self-citations may be approaching the upper bound. Additionally, the four Lei (2025a-d) references are Chinese-language publications; WRR readers may not have access to these. The paper should be self-contained enough that the key ideas from those publications are adequately summarized here.

**Recommendation**: Verify and report the self-citation rate. Ensure all key concepts from Lei (2025a-d) are adequately introduced in this paper rather than relying on readers accessing Chinese-language sources.

### M5. Prediction 1 (30% RMS Improvement) Lacks Justification
Prediction 1 claims "at least 30% reduction in root-mean-square water level deviation compared to incumbent rule-based SCADA operation." This is a strong quantitative claim. What is the basis for the 30% figure? Is this based on published canal automation results (Clemmens & Schuurmans, 2004)? Or is it an aspirational target? Without a basis calculation or reference to comparable published improvements, this prediction may appear arbitrary.

**Recommendation**: Provide justification for the 30% target, citing published results from comparable MPC implementations on canal or reservoir systems.

---

## Minor Issues (≥5)

### m1. Key Points Length
The AGU Key Points guideline specifies three bullet points of ≤140 characters each. The current Key Points are substantially longer (KP1: ~280 chars, KP2: ~580 chars, KP3: ~130 chars, KP4: ~370 chars, and there are four instead of three). This needs to be reformatted to comply with WRR submission requirements.

### m2. Abstract Length
The WRR guideline specifies abstracts of ~150 words. The current abstract appears to be approximately 350-400 words. This should be shortened significantly.

### m3. Figure Placeholders
The manuscript contains five "[Figure X about here]" placeholders but the actual figure files are not provided. For review purposes, at least rough drafts of the figures should be available to assess their clarity and information content.

### m4. Acknowledgments Incomplete
The Acknowledgments section contains placeholder text: "Grant Nos. [to be inserted]." These should be filled in before submission.

### m5. Missing "Open Research" Statement
While the Open Research section exists, it simply states this is a theoretical paper. WRR requires specific data availability statements even for theoretical papers. A statement about code availability (for the MPC examples) would strengthen the paper.

### m6. Table Formatting
Several tables (particularly Tables 1, 2, and 4) appear to have lost formatting in the markdown conversion. The column alignment and readability should be verified in the final manuscript format.

### m7. Equation Rendering
Several equations appear as embedded images rather than rendered LaTeX. This makes it impossible to verify the mathematical expressions precisely. All equations should be in editable LaTeX format.

---

## Reference Audit

### Verified References (spot-check):
- Litrico & Fromion (2009): ✓ Springer, confirmed
- Cunge (1969): ✓ JHR, confirmed
- Schuurmans (1997): ✓ Delft doctoral thesis, confirmed
- Castelletti et al. (2023): ✓ Annual Reviews in Control, confirmed
- Horváth et al. (2024): ✓ WRR, confirmed
- SAE International (2021): ✓ J3016, confirmed

### References to Verify:
- Brown et al. (2020): GPT-3 paper in NeurIPS — existence confirmed, but relevance to water systems control should be justified more explicitly
- Lewis et al. (2020): RAG paper — same comment as above
- UNESCO (2024): World Water Development Report — confirm this edition exists

### Missing References:
- No reference to ISO 26262 (2018) full citation in the reference list — needs to be added (it IS referenced but appears to be in the list)
- Consider adding Rawlings & Mayne (2009/2017) MPC textbook reference alongside Rawlings et al. (2017) — already present, OK
- van Overloop (2006) is cited but could benefit from his 2014 canal control book as well

---

## Summary

This is an ambitious and largely well-executed paper that makes genuinely novel theoretical contributions, particularly the unified transfer function family and the Muskingum-IDZ duality. However, the complete absence of numerical validation — even a single benchmark comparison against Saint-Venant simulations — is a significant weakness for a framework paper targeting WRR. The practical implementation aspects (SCADA integration, computational requirements) need addressing to bridge the gap between theoretical elegance and field applicability. The Key Points and Abstract need reformatting to meet WRR specifications.

With these revisions, the paper has strong potential for acceptance at WRR.
