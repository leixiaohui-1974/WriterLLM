# Review Report — Paper CKG-2 (Control Eng. Practice v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+Water researcher, Nature editorial board
**Date**: 2026-02-13

---

## Overall Assessment

The revised manuscript has substantially improved. The IEC 61511 alignment, false alarm analysis, and 10-pool scaling demonstration address the major practical concerns raised by Reviewer B. The ODD polytope formalization with the distance-to-boundary function is technically sound and the 32-scenario SiL verification is thorough. However, from a cross-disciplinary and impact perspective, two significant gaps remain.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. No Learning-Based ODD Expansion Pathway

The paper treats the ODD as a static, manually specified polytope. In practice, autonomous systems should expand their ODD over time as more operational experience is accumulated (analogous to how autonomous vehicles expand their ODD through fleet learning). The paper mentions "ODD expansion via xIL campaigns" (Table 1b, Phase 5) but provides no methodology for how ODD boundaries should be updated based on accumulated SiL or HiL data. A brief section on data-driven ODD refinement—perhaps using Bayesian inference to tighten or relax safety margins based on observed violation rates—would significantly strengthen the contribution and align with the AI/ML community's expectations for adaptive safety frameworks (Garcia & Fernandez, 2015).

### M2. Digital Twin Positioning Missing

The SiL architecture (§4.1) effectively creates a digital twin of the dual-tank system—a virtual replica that runs in parallel with the physical system's control software. Yet the paper never uses the term "digital twin" or positions the work within the rapidly growing digital twin literature for water systems. This is a missed opportunity: the ODD-monitored SiL can be reframed as a "safety-certified digital twin" that not only replicates system behavior but also continuously monitors operational safety boundaries. This positioning would broaden the paper's appeal to the digital twin community and increase citations.

---

## Minor Issues

### m1. No Comparison with Robust MPC / Tube MPC

The MPC controller uses a nominal model without explicit robustness guarantees. The robust MPC literature (e.g., tube MPC by Mayne et al., 2005) provides constraint-satisfaction guarantees for bounded disturbances—precisely the type of guarantee that the ODD framework seeks to provide at a higher level. A brief discussion of how ODD monitoring relates to (and potentially replaces or complements) robust MPC constraint tightening would clarify the methodological contribution.

### m2. FAIR Data Compliance

The Data Availability section lists a GitHub repository but does not mention persistent identifiers (DOI via Zenodo), license, or metadata standards. For a Control Engineering Practice paper, FAIR compliance (Findable, Accessible, Interoperable, Reusable) is increasingly expected.

### m3. ODD Visualization

The paper describes a polytope in $\mathbb{R}^7 \times \{0,1\}$ but provides no visualization of the ODD boundary or the $\rho$ landscape. A 2D projection (e.g., $h_1$ vs. $h_2$ with ODD boundary contours and color-coded $\rho$ values) would make the abstract polytope concept tangible for practitioners.

### m4. Broader Impact Statement

Control Engineering Practice increasingly values broader impact discussions. A brief statement on how ODD formalization contributes to water security, climate adaptation (operating under more extreme conditions), and the UN SDG 6 (Clean Water and Sanitation) would strengthen the paper's positioning.

### m5. Table 1c Extrapolation

The 50-pool and 500-pool entries in Table 1c are marked as "estimated." The basis for extrapolation (linear scaling with constraint count?) should be stated explicitly.

---

## Summary

The paper is close to acceptance. The two major revisions—learning-based ODD expansion and digital twin positioning—are both additive (new subsections) rather than restructuring. The minor issues are straightforward. After these revisions, the paper should be ready for publication.
