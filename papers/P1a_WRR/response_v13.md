# Revision Response — P1a WRR v12 → v13

**Iteration**: 4
**Reviewer**: B (Engineering Practitioner)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Persistent Absence of Numerical Validation

**Response**: Partially accepted. We agree that numerical validation is the paper's most significant remaining gap. However, full Saint-Venant benchmark simulations are beyond the scope of this theoretical framework paper and are the explicit subject of companion paper P2A (JWRPM).

**Action taken**: Added a "Validation Limitations" paragraph at the end of Section 6, explicitly acknowledging the gap: "The illustrative applications presented in Sections 6.1–6.3 are analytical predictions from linear reduced-order models. No nonlinear simulation validation against Saint-Venant benchmarks is included in this paper. This is a deliberate scope decision: the present paper establishes the theoretical framework; companion paper [P2A] provides full computational validation including time-domain comparisons of IDZ-MPC controllers against SIC²-simulated Saint-Venant models for the South-to-North Water Diversion Middle Route. Published frequency-domain comparisons by Litrico & Fromion (2004) and Horváth et al. (2024) provide independent empirical support for the IDZ model's accuracy within the stated validity ranges (Section 4.5). The reader is cautioned that the quantitative predictions of Section 9.2 are theoretical derivations whose empirical confirmation awaits the computational companion."

This approach honestly acknowledges the limitation while directing the reader to where the evidence will be provided.

### M2. SCADA Integration (Section 7.5) — Operational Gaps

**Response**: Accepted on all three sub-points. These are legitimate field engineering concerns.

**Action taken**:
(a) Added threshold reconciliation statement: "During commissioning, the xIL process (Lei, 2025c) includes a dedicated threshold reconciliation stage at the HiL level: all Layer 0 interlock thresholds are compared against existing PLC safety logic, and the more conservative value is adopted for each parameter. Where thresholds conflict (e.g., CHS Layer 0 high-water alarm at 0.10 m below crest vs. existing PLC alarm at 0.15 m), the reconciled threshold is the minimum of both, with the conflict documented in the ODD certification record."

(b) Added cybersecurity acknowledgment: "Any networked control architecture on critical water infrastructure must address cybersecurity risks. The OPC-UA backbone recommended here includes built-in security features (X.509 certificates, encrypted channels), and the overall architecture should comply with IEC 62443 (industrial cybersecurity) and national guidance (e.g., NIST SP 800-82 for US systems). A full cybersecurity threat analysis for the HDC architecture is beyond the scope of this paper but is identified as a necessary complement to the technical deployment discussed here."

(c) Added operator transition statement: "The WSAL-2→3 transition requires a structured operator training and transition protocol. During the transition period, the HDC system operates in 'shadow mode'—computing and recommending actions that the operator can accept or override—while building operational trust through demonstrated performance. Formal handover occurs only after the shadow-mode performance record satisfies the ODD certification criteria (operator intervention rate <5% over a minimum 90-day evaluation period within the certified ODD). This graduated transition ensures that technical readiness and operator confidence advance together."

### M3. Cross-Sector Transfer Claims Need Quantitative Backing

**Response**: Accepted. The practical differences across sectors should be explicitly acknowledged.

**Action taken**:
(a) Added time-scale qualification to the urban pressure zone transfer: "While the MPC algorithm is mathematically identical across sectors, the operational context differs substantially. The urban pressure zone requires sampling periods 2–3 orders of magnitude shorter (Ts ≈ 1–10 s vs. 300 s for canals), imposing correspondingly stricter requirements on communication latency (<100 ms vs. <10 s), actuator response time, and computational throughput. The claim of 'algorithmic transferability' refers specifically to the mathematical formulation (cost function structure, constraint handling, state-space model form), not to the implementation requirements."

(b) Added reservoir nonlinearity qualification: "For reservoirs with strongly nonlinear area-elevation curves (A_h varying by 5:1 or more over the operational range), the linear Integrator model requires gain-scheduling or adaptive re-parameterization. The CHS framework accommodates this through Theorem 3's model-layer correspondence: at Layer 1 (real-time MPC), the Integrator model is re-linearized around the current operating level at each control step; at Layer 2 (coordination), a piecewise-linear or lookup-table representation of the area-elevation curve is used. The linear model remains structurally valid; only the parameter A_h becomes state-dependent."

(c) Revised Prediction 2 tolerance statement: "The generous tolerance bounds (settling time within 50%, steady-state error within 200%) reflect the prediction's purpose: demonstrating that the same algorithm structure produces operationally meaningful—not necessarily optimal—performance across sectors without modification. In engineering terms, 'transferability' means that a canal-calibrated MPC controller, when applied to a reservoir or urban DMA with appropriate re-parameterization, produces stable closed-loop regulation without requiring redesign of the cost function, constraint structure, or horizon length. Fine-tuning of weight matrices for sector-specific performance optimization is expected and is not counted as 'algorithmic modification.'"

### M4. WSAL Transition Criteria — Measurement Protocol

**Response**: Accepted. Measurability requires protocol specification.

**Action taken**: Added a methodological note after the WSAL transition criteria: "Measurement protocol: WSAL transition metrics are evaluated over a minimum 90-day continuous operation period within the certified ODD. An 'intervention' is defined as any operator action that overrides or modifies a Layer 1 or Layer 2 control command; routine setpoint changes from Layer 3 planning do not count. 'Operating scenarios' are enumerated from the operational history of the specific installation, weighted by time-of-occurrence frequency. Statistical confidence for WSAL-4→5 'zero intervention' is defined as <0.1% intervention rate (fewer than 1 per 1,000 control cycles) with 95% confidence over the evaluation period."

### M5. Open Research Statement

**Response**: Accepted. We strengthen the commitment.

**Action taken**: Revised the Open Research section: "Illustrative MPC code implementing the IDZ-based single-pool controller of Section 6.1 and the distributed MPC of Section 6.2 will be deposited in a public GitHub repository under the MIT License upon acceptance, with a Zenodo DOI for persistent archival. A preliminary version of the single-pool MPC code is available for reviewer access upon request."

---

## Response to Minor Issues

### m1. Table 6 WSAL Transition Criteria
**Action**: Verified that the transition criteria text (from v11 response) is incorporated in the paragraph following Table 6. These criteria are presented as body text rather than additional table rows due to formatting constraints.

### m2. Section 6.1 LQR Pedagogical Note
**Action**: Added a clarifying sentence after the LQR example: "The LQR design is presented as a pedagogical demonstration of the IDZ model's fitness for feedback control design, illustrating the key features (integrator pole, delay approximation, constraint-relevant eigenvalue placement). For operational deployment, Model Predictive Control (MPC) is the recommended approach due to its explicit constraint handling capability, as developed in Section 6.2."

### m3. Prediction 4 Timeline Qualification
**Action**: Added qualification: "The three-year timeline is calibrated to the automotive sector's experience with the SAE Level 2→3 transition for geofenced operational domains (e.g., highway-only automated driving in specific regions), adjusted for the slower iteration cycle typical of water infrastructure commissioning. This is a testable hypothesis, not a guaranteed outcome; factors including institutional readiness, regulatory framework development, and site-specific complexity may extend or compress the timeline."

### m4. Section 6.2 "Optimal Buffer Fraction" Inconsistency
**Action**: Changed "the optimal buffer fraction" in Section 6.2 to "the characteristic buffer fraction" to maintain consistency with the v12 terminology revision in Section 5.3.

### m5. Acknowledgments
**Action**: Noted. Grant numbers are pending final confirmation and will be inserted before formal submission. This is standard practice for pre-submission internal review.

---

## Reference Audit Response

### Suggestions considered:
- Panguluri et al. (2017) or AWWA cybersecurity guidance: Not formally cited, but the cybersecurity acknowledgment now references IEC 62443 and NIST SP 800-82 as the relevant standards. Adding a full cybersecurity reference list would expand scope beyond the paper's focus.
- Hashimoto et al. (1982): An excellent suggestion. However, the resilience tetrad (Section 5.2) addresses operational control resilience (robustness, coordination, adaptation, hierarchy) rather than system performance evaluation (reliability, resiliency, vulnerability). The conceptual connection is acknowledged but adding the reference would require a bridging discussion that expands Section 5.2 beyond its current scope. Deferred to companion paper P2C.
- Eker & Kara (2003): Not added; the IEC 61131-3 reference already covers PLC programming standards. Adding a domain-specific PLC reference would be appropriate in a more implementation-focused paper.

---

## Version Summary

- **v12 → v13 changes**: Added Validation Limitations paragraph in Section 6 (M1); expanded Section 7.5 with threshold reconciliation, cybersecurity acknowledgment, and operator transition protocol (M2); added time-scale, reservoir nonlinearity, and transferability qualifications to Section 6.3 and Prediction 2 (M3); added WSAL measurement protocol note (M4); strengthened Open Research commitment (M5); added LQR pedagogical note (m2); qualified Prediction 4 timeline (m3); fixed "optimal"→"characteristic" inconsistency in Section 6.2 (m4).
- **Self-citation rate**: Unchanged at ~16%.
- **Next focus**: Consider minimal numerical validation if feasible; continue formatting pass; equation rendering.
