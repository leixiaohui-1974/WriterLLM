# Review Report — CKG-3 v02 → v03

**Reviewer**: C (Interdisciplinary — Asian AI+Water Leader, Nature Editorial Board)
**Iteration**: 2
**Date**: 2026-02-15

## Overall Assessment

The revised manuscript has substantially improved with the five-pool specifications (Table 2b), RLS convergence analysis, and cost-benefit comparison. The multi-platform demonstration is now convincing. However, the paper underexploits its broader significance: the adaptive MAS represents a paradigm shift from static model-based control to self-aware autonomous systems, and this connection to the broader CHS vision deserves more attention. Several innovation-focused improvements would elevate the paper.

**Score**: 7.5 / 10
**Verdict**: **Minor Revision**

## Dimension Scores

| Dimension | Score | Comment |
|-----------|-------|---------|
| Novelty | 7.5 | Good engineering novelty; broader significance underexploited |
| Math Rigor | 7 | RLS analysis improved; Bayesian ODD expansion could be tighter |
| Reproducibility | 8 | Five-pool details now adequate |
| Case Validation | 8 | Multi-platform comparison is strong |
| Literature | 7 | Still missing transfer learning / domain adaptation refs |
| Writing Quality | 7.5 | Clear; could be more concise in places |
| System Differentiation | 8 | Clear progression from CKG-1/2 |

## Major Issues

**M1. Missing connection to digital twin and Industry 4.0 paradigms.**
The adaptive MAS with online re-identification effectively constitutes a self-calibrating digital twin: the IDZ model continuously updates to match the physical plant. This connection to the digital twin literature (Rasheed et al., 2020; Grieves & Vickers, 2017) and Industry 4.0 concepts (cyber-physical systems) should be made explicit. A new subsection (§7.6 "Self-Calibrating Digital Twin") framing the adaptive MAS as a digital twin contribution would significantly enhance the paper's impact and citation potential.

**M2. Scalability to real irrigation districts not quantified.**
The 10-pool benchmark is still relatively small compared to real irrigation districts (50–500 pools). The paper states that GPU-parallel solvers (Huang et al., 2026) would be needed but provides no estimate of the computational scaling. Add a brief scaling analysis: extrapolate the observed computational trends (Table 7) to 50, 100, and 500 pools, and identify the crossover point where GPU acceleration becomes necessary.

**M3. Comparison with alternative adaptive approaches is missing.**
The paper compares adaptive-PLC vs. fixed-PLC but does not compare against alternative adaptive methods: (a) multiple-model adaptive control (MMAC) with a bank of pre-computed IDZ models, (b) L1 adaptive control, (c) Gaussian Process regression for model learning. At minimum, a qualitative comparison table explaining why RLS + gain-scheduled MPC was chosen over alternatives would strengthen the methodological contribution.

## Minor Issues

**m1.** Abstract is 198 words — within limit but could be tightened. Consider removing the Bayesian ODD expansion detail to focus on the two primary contributions (PLC HiL + adaptive MAS).

**m2.** Section 4.4: The MAS = HDC + ODD + CI formulation appears in the text but the CI (Cognitive Intelligence) component is not formally defined. Add a brief definition: "Cognitive Intelligence encompasses the agent's ability to monitor its own model accuracy, adapt to changing conditions, and learn from operational experience."

**m3.** Figure 5 caption mentions "increasing benefit of adaptation for larger systems" — this deserves a brief analytical explanation (e.g., error propagation through coupled subsystems).

**m4.** Table 8: The "Exploratory" campaign uses only 8 scenarios (vs. 16 for baseline and confirmation). Justify why 8 is sufficient for the exploratory phase.

## Reference Audit

- Self-citation rate: approximately 10/25 = 40% — this is ABOVE the 25% red line. Reduce self-citations to ≤ 25% by adding third-party references and removing less critical self-references.
- Missing: Grieves, M., & Vickers, J. (2017). Digital twin: Mitigating unpredictable, undesirable emergent behavior in complex systems.
- Missing: Boyd, S., et al. (2011). ADMM for distributed optimization — needed for the DMPC/ADMM claim in §4.4.
- Missing: Wahlin & Clemmens (2006) — added in v02, good.

## Recommendation

Minor revision focusing on: (1) digital twin framing, (2) scalability extrapolation, (3) adaptive method comparison, and (4) self-citation rate reduction to ≤ 25%. The core results are strong and the multi-platform demonstration is convincing.
