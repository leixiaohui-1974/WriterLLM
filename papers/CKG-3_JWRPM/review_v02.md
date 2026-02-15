# Review Report — CKG-3 v01 → v02

**Reviewer**: B (Engineering Practitioner — US Water Utility CTO)
**Iteration**: 1
**Date**: 2026-02-15

## Overall Assessment

This paper makes a solid engineering contribution by completing the xIL verification chain with industrial-grade PLC hardware and introducing adaptive MPC. The multi-platform comparison (dual-tank, five-pool, 10-pool) is a welcome progression from the single-platform demonstrations in CKG-1 and CKG-2. However, several engineering and practical gaps need to be addressed before publication.

**Score**: 6.5 / 10
**Verdict**: **Major Revision**

## Dimension Scores

| Dimension | Score | Comment |
|-----------|-------|---------|
| Novelty | 7 | Adaptive MAS + PLC HiL is a genuine advance over CKG-1/2 |
| Math Rigor | 6 | RLS derivation is standard; lacks convergence analysis |
| Reproducibility | 5 | Five-pool flume details insufficient for replication |
| Case Validation | 6 | Good multi-platform, but five-pool data not shown in detail |
| Literature | 6 | Missing key adaptive MPC and PLC deployment references |
| Writing Quality | 7 | Clear and well-structured |
| System Differentiation | 7 | Good progression from CKG-1/2 |

## Major Issues

**M1. Five-pool canal flume description is insufficient for reproducibility.**
Section 2.3 provides basic dimensions but lacks critical information: gate geometry (undershot/overshot, opening range), pump head-flow curve, downstream boundary condition (free overfall vs. submerged), Manning's n for the flume material, and the IDZ identification results for each pool. Without these, the five-pool results cannot be independently reproduced. Provide a complete Table analogous to CKG-1 Table 2 with IDZ parameters for all five pools.

**M2. No individual scenario results shown for five-pool and 10-pool.**
Tables 6 and 7 report only aggregate statistics. The paper should include at least one representative time-series plot for the five-pool HiL showing: (a) water levels in all five pools, (b) gate positions, (c) RLS parameter estimates over time, and (d) ODD status. Similarly, for the 10-pool benchmark, a cascading disturbance scenario showing the MAS coordination response would be valuable.

**M3. RLS convergence and stability analysis is missing.**
The RLS estimator (Eqs. 5–7) with forgetting factor $\lambda = 0.98$ is standard but the paper does not analyze: (a) convergence conditions — what is the minimum persistent excitation requirement? (b) What happens during steady-state operation when excitation is low? (c) What is the effect of forgetting factor choice on tracking speed vs. noise? A sensitivity analysis of $\lambda$ (e.g., 0.95, 0.98, 0.99) on both tracking performance and estimation noise would strengthen the adaptive control contribution.

**M4. Cost-benefit analysis of the PLC upgrade is absent.**
The Arduino costs ~$25; the S7-1200 costs ~$500–800 plus TIA Portal licensing (~$3,000/seat). For field deployment, the PLC cost is negligible relative to infrastructure, but for laboratory research and education, the cost difference matters. A brief cost-benefit table comparing Arduino vs. PLC platforms (cost, performance, scalability, industrial compliance) would help practitioners make informed decisions.

**M5. Cybersecurity discussion is superficial.**
Section 7.4 mentions IEC 62443 but provides no details. OPC-UA with TLS 1.2 is necessary but not sufficient for cybersecurity compliance. What authentication mechanism is used? Are there access control policies? How is the PLC protected from unauthorized firmware modification? At minimum, a table mapping IEC 62443 security levels to the current implementation and identifying gaps would be appropriate.

## Minor Issues

**m1.** Table 1: Add the cost row (Arduino ~$25, S7-1200 ~$700 + TIA Portal ~$3,000).

**m2.** Section 4.2: The discrete delay $d = \lceil \tau_d / \Delta t \rceil$ should be estimated online rather than fixed, especially when $\tau_d$ varies across operating points (Table 3 shows $\tau_d$ ranging from 6.2 to 12.1 s, giving $d$ = 2 or 3).

**m3.** Section 4.3: The bumpless transfer "exponential transition over 5 samples" needs more detail — what is the blending function? Is it applied to the control output or the model matrices?

**m4.** Eq. (4): The formula $A_s = \Delta t / (1 - a_1 - a_2)$ assumes the ARX model is at steady state. State the assumption explicitly.

**m5.** Section 6.5: The ODD expansion from [10, 40] to [8.5, 41.5] cm is a 12% range increase — but this is 12% of the operational range, which is only 3 cm on each side. Discuss whether such a small expansion is meaningful for field-scale systems where the range might be meters.

## Reference Audit

- All CHS self-references (Lei 2025a/b/c, Chen 2026a/b, Liu 2026, Huang 2026) are appropriate
- Missing: Astrom & Wittenmark (2008) for adaptive control theory
- Missing: van Overloop et al. (2010) already included — good
- Missing: Wahlin & Clemmens (2006) for canal automation with PLC
- Missing: Lemos et al. (2004) or similar for adaptive MPC in process control
- Ye et al. (2026) reference — is this P2B? Clarify the paper identity

## Recommendation

Major revision addressing the five-pool reproducibility (M1), individual scenario results (M2), RLS analysis (M3), and cost-benefit (M4) issues. The cybersecurity gap (M5) can be addressed with a focused subsection. The core contributions are sound; the revisions will strengthen the engineering credibility.
