# Review Report — Paper P1c (中国科学 v5)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water systems CTO
**Date**: 2026-02-13

---

## Overall Assessment

This is my second review of this paper (first review: iteration 1, score 7/10, Major Revision). The revisions have been substantial and responsive. Every major concern I raised has been addressed:

- **"天河大模型" removed**: Replaced with technology-neutral description. The cognitive intelligence section is now credible and non-promotional. ✓
- **LLM credibility**: Revised to "hybrid AI methods" with explicit propose-validate safety architecture. The AI safety caveat (ref [48]) is well-placed. ✓
- **Jiaodong quantitative metrics**: Added MIL results (5-8% energy reduction, ±0.10m RMSE, ±3% water allocation deviation). Honestly qualified as simulation-based. ✓
- **Cybersecurity**: IEC 62443, defense-in-depth, L0 air-gap isolation, communication resilience all added. ✓
- **Self-citation and international coverage**: Canal automation community acknowledged; international research schools surveyed. ✓
- **"群体智能" → "自主协同"**: Terminology corrected. ✓

The v04→v05 revisions by Reviewer A have further strengthened the paper: proof claims qualified, DMPC convergence caveats added, multi-timescale optimality gap acknowledged, equation numbers added. These are all appropriate for a 中国科学 paper.

From an engineering practitioner's perspective, the paper now provides a credible, well-grounded, and honest account of both the theoretical framework and the engineering practice. The WSAL classification with quantitative discriminants and calibration caveats gives utilities a concrete reference. The shadow-mode deployment concept and operator trust discussion address real adoption barriers.

I have two remaining minor concerns but no major issues.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | CHS, unified transfer functions, WSAL are genuine contributions |
| Mathematical Rigor | 8 | Assumptions now transparent; caveats well-placed |
| Reproducibility | 7.5 | MIL results provided; formulas specified with equation numbers |
| Case Validation | 7.5 | Both cases have quantitative metrics; honestly positioned as preliminary |
| Literature Completeness | 8.5 | 59 references; international schools acknowledged; good cross-disciplinary |
| Writing Quality | 8.5 | Excellent scholarly Chinese; clear structure |
| System Differentiation | 8.5 | CHS vs smart water/digital twin now explicitly and clearly differentiated |

---

## Major Issues

None.

---

## Minor Issues

### m1. WSAL L2→L3 Transition — Engineering Readiness Indicators
The WSAL quantitative discriminants (L3: "ODD场景覆盖率>80%") are now accompanied by calibration caveats, which is good. However, from a utility manager's perspective, the transition from L2 to L3 also requires non-technical readiness indicators: operator training completion rates, regulatory approval milestones, insurance/liability frameworks. Consider adding a brief note in §6.1 or §6.4: "从L2到L3的工程实施还需要完成操作人员培训认证、主管部门备案审批和运行责任保险安排等配套工作."

### m2. PIL (Plant-in-the-Loop) Risk Management
§4.3 describes PIL as "在实际工程的非关键工况下进行有限度的在线测试." From an operational safety perspective, even "non-critical" PIL testing on actual water infrastructure carries risk. Consider adding: "PIL测试须事先制定详细的测试方案和应急预案, 并经工程管理单位安全审批; 测试期间应有人员现场值守, 随时准备接管手动控制."

### m3. Companion Paper Reference Update
Several sections reference forthcoming companion papers (e.g., the WRR companion for the full mathematical proof). If any of these papers have been submitted or published since the draft was written, update the references accordingly.

---

## Summary

This paper has undergone a thorough three-iteration revision that has addressed all of my original major concerns. The theoretical framework is now presented with appropriate assumptions and caveats. The engineering practice sections provide honest quantitative evidence. The CHS positioning against smart water and digital twin paradigms is clear. The cybersecurity, safety, and operator trust discussions demonstrate practical awareness. I have only minor suggestions remaining. The paper is approaching publication quality for 中国科学.
