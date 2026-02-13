# Review Report — Paper P1a (WRR v15)

**Iteration**: 7 of 20+
**Reviewer**: B (Engineering Practitioner) — Water Utility CTO, USA
**Date**: 2026-02-13

---

## Overall Assessment

I have now reviewed this manuscript three times (v9, v12, v15). The transformation has been remarkable. My v12 review (iteration 4) raised concerns about validation, SCADA integration depth, cross-sector transfer qualification, WSAL measurement protocols, and the Open Research statement. All five have been addressed substantively:

- The validation limitations paragraph (v13) is refreshingly honest and appropriately scopes the paper as theoretical framework.
- Section 7.5 now covers threshold reconciliation, cybersecurity (IEC 62443, NIST SP 800-82), and the shadow-mode operator transition protocol — all operationally credible.
- Cross-sector transfer qualifications (time-scale, reservoir nonlinearity, transferability definition) are precise and honest.
- WSAL measurement protocol (90-day period, intervention definition, statistical confidence) is well-specified.
- Open Research commitment (MIT License, Zenodo DOI) is strong.

The v14-v15 revisions (from Reviewers A and C) have further strengthened the paper: the propose-validate interface now uses standard MPC parameterization, DMPC convergence conditions are stated with the elegant P2-P6 connection, Prediction 1 is grounded in published performance numbers, and the differentiable modeling connection positions CHS at the frontier of physics-AI integration.

From an engineering practitioner's perspective, this paper now provides a credible theoretical foundation for water automation. The remaining issues are genuinely minor.

**Score: 9.5/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 9.5 | Unified TF family, MAS architecture, WSAL — each addresses a real operational need |
| Mathematical Rigor | 9 | Substantially matured; Remark 1 + model reduction connection is exemplary |
| Reproducibility | 7.5 | MIT License + Zenodo commitment credible; validation limitations honestly stated |
| Case Validation | 6.5 | Published performance numbers now cited; companion paper framework appropriate for theory paper |
| Literature Completeness | 9.5 | Comprehensive across control theory, AI/ML, cybersecurity, and operational practice |
| Writing Quality | 9.5 | Excellent throughout; notation consistent; limitations honestly acknowledged |
| System Differentiation | 9.5 | Navier-Stokes analogy, differentiable modeling, dual-engine architecture — compelling positioning |

---

## Major Issues

### M1. Shadow-Mode Transition Protocol — Duration and Success Criteria

The shadow-mode operator transition protocol (added in v13, Section 7.5) specifies "operator intervention rate <5% over a minimum 90-day evaluation period within the certified ODD." This is a good start. Two refinements would make it deployment-ready:

(a) The 90-day period should be specified as "90 calendar days of continuous operation within the certified ODD, excluding scheduled maintenance downtime and planned system shutdowns." Without this exclusion, a 90-day evaluation at a system with frequent maintenance could be dominated by non-operational periods.

(b) The <5% threshold should distinguish between operator-initiated overrides (where the operator disagrees with the automation) and operator-triggered mode switches (where the ODD boundary is approached and the system correctly transitions to manual). Only the former should count as "intervention" for WSAL evaluation purposes.

**Recommendation**: Add one sentence clarifying the measurement exclusions and intervention classification. This is a minor specification detail.

### M2. Computational Benchmarks for Real-Time MPC — Hardware Specificity

Section 7.5 states: "Modern field-grade industrial PCs (e.g., Intel Atom-class processors) solve such QPs in <100 ms using open-source solvers (OSQP, qpOASES), well within the 300 s sampling interval." This is a reasonable estimate but should note that the benchmark assumes a single-pool QP. For the 64-gate DMPC case (Section 6.2), the per-pool QP is the same, but the coordination protocol requires 3-5 sequential communication-computation cycles within each 300 s interval. With realistic communication latencies (50-200 ms for SCADA polling), the total coordination time could approach 1-2 seconds — still well within budget, but worth stating.

**Recommendation**: Add a brief note in Section 7.5 confirming that the DMPC coordination overhead (3-5 iterations × communication + computation) remains within the sampling budget for the stated hardware and communication assumptions.

### M3. Cybersecurity Acknowledgment — Attack Surface Specificity

The cybersecurity acknowledgment (v13 addition) references IEC 62443 and NIST SP 800-82. This is appropriate but generic. The specific attack surface introduced by the HDC architecture is the Layer 1-Layer 2 interface: a compromised Area Agent could inject false boundary data into neighboring pools' DMPC, causing coordinated misoperation that appears "normal" to each local controller. The island autonomy fallback (Section 7.3) provides partial mitigation, but this specific threat vector deserves one sentence of acknowledgment.

**Recommendation**: Add one sentence: "The most architecture-specific cybersecurity risk is compromise of the Area Agent's coordination data exchange, which could inject false boundary conditions into neighboring pools' DMPC; anomaly detection on exchanged boundary trajectories is recommended as a mitigation measure."

### M4. Prediction 2 — "Settling Time Within 50%" May Be Too Generous

Prediction 2 now includes the helpful engineering interpretation that "transferability means stable closed-loop regulation across sectors without requiring redesign." However, the "settling time within 50%" tolerance is asymmetric in practice: a canal controller applied to an urban DMA with 2-3 orders of magnitude faster dynamics could produce oscillatory behavior before settling, even if the final settling time metric is met. The risk is not stability failure (the closed-loop is stable by construction) but transient performance that would be unacceptable to operators (pressure oscillations in urban water supply).

**Recommendation**: Add one sentence: "The settling time tolerance does not constrain transient behavior (overshoot, oscillation count); practical deployment would require weight matrix tuning for acceptable transient performance, which is expected and does not invalidate the transferability claim."

### M5. Table 6 WSAL — Practical Deployment Examples

Table 6 now has measurable transition criteria and a measurement protocol. The cross-sector assessment (following Table 6) cites Shaoping and Jiaodong as WSAL-2 examples. To complete the picture, one sentence identifying a credible candidate for the world's first WSAL-3 deployment would add practical gravity. The South-to-North Water Diversion Middle Route (64 gates, already referenced as a benchmark) is the obvious candidate.

**Recommendation**: Add: "The South-to-North Water Diversion Middle Route, with its 64 remotely controllable gates and extensive SCADA infrastructure, represents the most advanced candidate for the world's first WSAL-3 certification pilot."

---

## Minor Issues

### m1. Section 6.1 — LQR Pedagogical Note Placement
The LQR pedagogical note (added in v13) effectively clarifies that LQR is illustrative and MPC is the operational recommendation. Good addition, no change needed.

### m2. Open Research — Timeline for Code Deposit
The Open Research section commits to MIT License and Zenodo DOI "upon acceptance." Consider specifying an estimated timeline (e.g., "within 60 days of acceptance") for clarity.

### m3. DMPC Convergence Fallback — Constraint Satisfaction Guarantee
The v15 addition states the DMPC fallback "may sacrifice optimality but maintains constraint satisfaction." Strictly, using the last converged solution maintains constraint satisfaction only if system state hasn't changed significantly since last convergence. For rapidly changing disturbances, the stale solution may violate constraints. This edge case deserves a brief note.

### m4. Acknowledgments — Grant Numbers
Still placeholder: "[to be inserted]." Standard for internal review but should be resolved before formal submission.

---

## Reference Audit

### Verified (new additions since v12):
- Antoulas (2005): ✓ SIAM — model reduction, appropriate for Theorem 2 open problem
- Guo et al. (2017): ✓ ICML — confidence calibration, well-placed
- Li et al. (2021): ✓ ICLR — Fourier Neural Operator, appropriate
- van Overloop et al. (2010): ✓ ASCE JIDE — MPC canal performance numbers, confirms 30-50% improvement

### No additional references recommended. The reference list is comprehensive and well-balanced.

---

## Summary

This paper has reached publication quality. Over seven iterations, it has evolved from a theoretically ambitious but practically underspecified manuscript (v9, score 7.0) to a mature framework paper that balances mathematical depth with engineering honesty (v15, score 9.5). The core contributions are original and significant. The validation limitations are honestly acknowledged. The practical deployment pathway (SCADA integration, shadow-mode transition, measurement protocols) is credible.

My remaining issues are specification refinements: shadow-mode duration clarification, DMPC computational budget, cybersecurity attack surface, Prediction 2 transient behavior, and WSAL-3 deployment candidate. These are addressable in a final editorial pass.

**I recommend acceptance.**
