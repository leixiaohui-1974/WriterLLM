# Review Report — Paper P-DC (EMS v05)

**Iteration**: 5 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher, 2nd review
**Date**: 2026-02-13

---

## Overall Assessment

This is my second review of this paper (first review: iteration 2, score 7.0/10, Minor Revision). My previous concerns have been comprehensively addressed:

- **Data-driven/ML integration**: §7.5 provides a thoughtful positioning of data-driven models within the MBD hierarchy (L7 surrogates, L6 alternatives, CI components) and honestly acknowledges the safety certification challenge for black-box models. The distinction between statistical validation and formal guarantees is well-articulated. ✓
- **Digital twin positioning**: §7.4 now provides a dedicated, substantive treatment positioning DfO-MBD relative to digital twins. The "born digital twin-ready" framing is memorable and clarifying. The descriptive vs. prescriptive distinction is effective. ✓
- **Educational competency framework**: Table 3b with Bloom's taxonomy mapping is exactly what was needed. The vertical integration argument is now concrete and assessable. ✓
- **SDG 6 connection**: Added in §1. ✓
- **Open-source emphasis**: The open-source pathway (OpenModelica + Python/do-mpc + FMI) is now highlighted as a key contribution. ✓
- **Figure 4**: Competency matrix figure added. ✓

Additionally, Reviewers A and B have driven significant improvements since my first review: the mathematical precision of DfO metrics (worst-case Gramians, balanced realization), the five-level hierarchy mapping, the IDZ identification methodology with confidence intervals, the industry adoption pathway, and the cost-benefit framing. These collectively transform the paper from a conceptual proposal into a comprehensive discipline-construction document.

From a cross-disciplinary perspective, the paper now successfully bridges water engineering, control theory, software engineering, education, and digital twin paradigms. The positioning relative to AUTOSAR/DO-178C (Table 1b), the ML discussion, and the SDG 6 connection ensure relevance across multiple EMS readership segments. The cost-benefit framing and adoption pathway make the paradigm shift actionable.

I have no remaining substantive concerns.

**Score: 9.0/10**
**Verdict: Accept**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8.5 | DfO paradigm is a genuine and timely contribution |
| Mathematical Rigor | 8 | Gramian specs, IDZ methodology, sensitivity analysis all rigorous |
| Reproducibility | 9 | Open-source pipeline, detailed reference workflow, Software Availability |
| Case Validation | 8 | Single case but thoroughly detailed with quantitative results |
| Literature Completeness | 9 | Excellent cross-domain coverage; 32+ references spanning 6 disciplines |
| Writing Quality | 9 | Clear, well-structured, and accessible to multi-disciplinary audience |
| System Differentiation | 9 | Digital twin, cross-domain MBD, five-level hierarchy, ML positioning all effective |

---

## Major Issues

None.

---

## Minor Issues

### m1. Consider Graphical Abstract

EMS encourages graphical abstracts. A single-panel figure showing the DfO-MBD pipeline from "Design Intent" through the seven layers to "Autonomous Operation" would be highly effective for attracting readership. This is optional and at the editors' discretion.

---

## Summary

This paper has achieved publication quality through a rigorous five-iteration review process. The three contributions—DfO paradigm with quantitative metrics, seven-layer MBD framework with cross-domain positioning, and competency-based educational foundation—collectively provide the water sector with a structured pathway from CHS theory to engineering practice and education. The open-source emphasis, cost-benefit framing, and graduated adoption pathway make the contributions immediately actionable. The honest scoping (single reference workflow, pilot-stage toolchain, planned but not yet implemented curriculum) demonstrates intellectual honesty. I recommend acceptance.
