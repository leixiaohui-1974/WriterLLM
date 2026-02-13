# Review Report — Paper P-DC (EMS v04)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO, 2nd review
**Date**: 2026-02-13

---

## Overall Assessment

This is my second review of this paper (first review: iteration 1, score 6.5/10, Major Revision). My previous concerns have been comprehensively addressed:

- **DfO metrics quantification**: Principles P1–P5 now have formal metrics with worst-case ODD vertex evaluation, balanced realization for observability, and discrete ODD coverage ratio. The mathematical specification is now rigorous and computable. ✓
- **Reference workflow**: Expanded from a sketch to a substantive ~1,500-word section with Saint-Venant equations, IDZ identification (Levenberg-Marquardt, confidence intervals), MPC configuration table, quantitative MiL results (Table 6), and parameter sensitivity. This is now a credible engineering workflow. ✓
- **Curriculum scope for EMS**: Reframed as "Educational Software Infrastructure" with competency framework (Table 3b) using Bloom's taxonomy. The vertical integration argument is compelling. ✓
- **Software Availability**: Now describes a genuine artifact (OpenModelica library + Python MPC + FMI scripts) with a plausible repository structure. ✓
- **Literature**: Expanded significantly with cross-domain MBD comparison, digital twin positioning, ML discussion, and 14+ new references since v01. ✓

Additionally, Reviewers A and C have driven valuable improvements: the five-level hierarchy mapping (Table 0) connects MBD to the CHS theoretical foundation, the digital twin positioning clarifies the relationship to the dominant smart water paradigm, and the ML discussion addresses the EMS audience's expectations.

From a practitioner perspective, the paper now provides a credible roadmap for translating CHS theory into engineering practice. The DfO principles are actionable (an engineer can compute $\sigma_{min}(W_c)$ and $R_{ODD}$ for a real project), the MBD framework is structured enough to guide a design project, and the reference workflow demonstrates feasibility. Two minor refinements would further strengthen the paper's practical utility.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | DfO paradigm is a genuine and needed contribution |
| Mathematical Rigor | 8 | Gramian specifications tightened; IDZ methodology rigorous |
| Reproducibility | 8.5 | Reference workflow now fully reproducible; open-source emphasis |
| Case Validation | 8 | Single case but detailed and quantitative; sensitivity included |
| Literature Completeness | 8.5 | Excellent cross-domain coverage; digital twin and ML addressed |
| Writing Quality | 8.5 | Clear, well-organized, professional throughout |
| System Differentiation | 8.5 | Digital twin, cross-domain MBD, and five-level hierarchy mapping all effective |

---

## Major Issues

None.

---

## Minor Issues

### m1. Industry Adoption Pathway

The paper discusses DfO as a paradigm shift but does not address the practical pathway for industry adoption. Water infrastructure projects are governed by procurement processes, design standards, and regulatory requirements that are deeply entrenched in the DfC paradigm. A brief discussion of how DfO could be introduced incrementally—perhaps starting with a "DfO checklist" for existing design review processes, or pilot requirements in specific project types (e.g., inter-basin transfers, automated pump stations)—would make the paradigm shift more actionable for utilities and design consultants. §7.1 would be a natural location.

### m2. Cost-Benefit Framing

The paper states that "the capital cost of embedding control intelligence during design is small relative to the operational savings over the infrastructure lifecycle" (§7.1) but provides no quantitative basis for this claim. Even an order-of-magnitude estimate would strengthen the argument—for example, the cost of adding sensor and actuator provisions during design versus the cost of retrofitting them during operation, or the operational savings from autonomous versus manual control over a 30-year lifecycle. This need not be precise; a parametric example based on the reference workflow would suffice.

---

## Summary

This paper has matured significantly over four iterations. The DfO paradigm, MBD framework, and competency-based curriculum collectively provide a comprehensive foundation for CHS as an interdisciplinary discipline. The two remaining suggestions (adoption pathway and cost-benefit framing) are minor enhancements that would increase practical impact. I am confident that one more revision will bring this paper to acceptance quality.
