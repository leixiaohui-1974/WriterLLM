# Review Report — Paper P2A (JWRPM v5)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water systems CTO
**Date**: 2026-02-13

---

## Overall Assessment

This is my second review of this paper (first review: iteration 1, score 6.5/10, Major Revision). Every major concern I raised has been substantively addressed:

- **Case study data placeholders**: Completely filled with specific data. Shaping: Dadu River, 4-stage, 360 MW, 2–3% efficiency, 40% water level reduction, MiL 2015–2017. Jiaodong: 500+ km, 13 pumps, 5–8% energy reduction, ±0.10 m RMSE, MiL 2018–2020. ✓
- **Author list**: Corrected to 7 authors per specifications. ✓
- **CI validation overreach**: Honestly scoped to HDC+ODD at WSAL-2; CI described prospectively. ✓
- **Cybersecurity**: IEC 62443, IT/OT segmentation, L0 air-gap, authenticated communication. ✓
- **Prior work differentiation**: Explicit "Relationship to Prior Work" paragraph with clear delineation. ✓
- **MRC specificity**: Formalized with τ_coast formula, case-specific procedures for both systems, kinematic vs dynamic wave speed clarification. ✓

Additionally, Reviewers C and A have driven improvements that strengthen the paper from perspectives I would not have raised: digital twin positioning, resilience framing, human factors, hierarchical optimality discussion, propose-validate feasibility definition, and cross-domain infrastructure context. The paper now reads as a mature, well-justified engineering architecture specification.

From a practitioner's perspective, the paper now provides what a utility CTO needs: a clear system architecture (MAS = HDC + ODD + CI), a concrete agent deployment framework (Edge–Area–Cloud), a maturity classification with measurable criteria (WSAL), and a verification roadmap (xIL). The honest scoping of validation to MiL, the acknowledgment that WSAL-3+ is prospective, and the human factors discussion demonstrate genuine engineering awareness.

I have two remaining concerns, both minor.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | WSAL with quantitative criteria is a practical contribution for the sector |
| Mathematical Rigor | 8 | Well-qualified; hierarchical consistency discussed; feasibility defined |
| Reproducibility | 8 | MPC parameters specific; MiL methodology clear; topology contrast sharp |
| Case Validation | 8 | Complete MiL data; honestly positioned; dual-topology design effective |
| Literature Completeness | 8.5 | 35 references; good cross-domain coverage |
| Writing Quality | 8.5 | Clear, professional, well-structured |
| System Differentiation | 9 | Prior work, digital twin, and resilience positioning all effective |

---

## Major Issues

None.

---

## Minor Issues

### m1. Shadow-Mode Deployment Pathway

The case studies are MiL-validated using retrospective data (2015–2017 and 2018–2020). While this is appropriate for a first validation and is honestly labeled, the practical pathway from MiL to field deployment would benefit from a brief discussion of "shadow mode" operation—where the MAS runs in parallel with human operators, generating control recommendations that are logged and compared against actual human decisions but not executed. Shadow mode is standard practice in power system automation and autonomous vehicle testing before commissioning. Adding 2–3 sentences in §7.1 or §8 describing shadow-mode as an intermediate step between MiL and SiL would make the xIL roadmap more actionable for utilities planning their WSAL-2→3 pathway.

### m2. Interoperability and Open Standards

§8.3 mentions that "Edge Agents from different vendors must implement the same Layer 0 safety logic and the same heartbeat protocol." This raises the interoperability question: is there an open standard or specification that vendors should implement, or is this proprietary to each MAS deployment? For WSAL to serve as a genuine industry standard (analogous to SAE J3016), the communication protocols, agent interfaces, and ODD specification format should ideally be standardized. A brief note acknowledging this need and suggesting a pathway (e.g., developing an open WSAL specification under IAHR/IWA auspices) would strengthen the governance discussion.

---

## Summary

This paper has undergone a comprehensive transformation from its initial draft. The two core contributions—MAS architecture and WSAL classification—are now supported by complete case study data, honest validation scoping, rigorous mathematical qualification, and broad cross-disciplinary positioning. The remaining issues are minor: shadow-mode deployment and interoperability standardization. The paper is approaching publication quality.
