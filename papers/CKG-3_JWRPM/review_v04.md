# Review Report — CKG-3 v03 → v04

**Reviewer**: A (Theory Rigorous — European Control Theory Professor)
**Iteration**: 3
**Date**: 2026-02-15

## Overall Assessment

The paper has improved considerably across iterations. The multi-platform demonstration is solid, the adaptive method comparison (Table 12) is helpful, and the digital twin framing adds impact. From a theoretical perspective, two issues remain: the stability guarantee for the gain-scheduled MPC during transitions, and the formal relationship between the RLS convergence rate and the ODD safety margin.

**Score**: 8.0 / 10
**Verdict**: **Minor Revision**

## Dimension Scores

| Dimension | Score | Comment |
|-----------|-------|---------|
| Novelty | 8 | Good integration of adaptive control with CHS framework |
| Math Rigor | 7.5 | Improved but gain scheduling stability needs treatment |
| Reproducibility | 8.5 | Five-pool details now excellent |
| Case Validation | 8.5 | Multi-platform demonstration convincing |
| Literature | 8 | Self-citation rate now acceptable |
| Writing Quality | 8 | Well-organized |
| System Differentiation | 8.5 | Clear CKG-1→2→3 progression |

## Major Issues

**M1. Gain-scheduled MPC stability during transition.**
Section 4.3 describes a bumpless transfer mechanism but does not provide a formal stability argument. When the MPC matrices change (due to RLS-triggered update), the closed-loop system is effectively switching between two LTI controllers. Standard results from switched systems theory (Liberzon, 2003) require either (a) a common Lyapunov function, or (b) a minimum dwell time between switches. The significance threshold $\delta_{\text{sig}} = 0.10$ implicitly provides a dwell time (because 10% parameter changes require sufficient operating point shift), but this should be formalized. At minimum, state the dwell time condition and verify it empirically: what is the minimum time between successive MPC updates observed in the experiments?

**M2. Relationship between RLS convergence rate and ODD safety margin.**
The paper presents RLS adaptation (§4.2) and ODD monitoring (§4.5) as separate mechanisms. However, they are coupled: during the RLS convergence period (5–8 samples), the MPC operates with a partially outdated model, which may temporarily reduce the effective ODD margin. Quantify this: during a gain-scheduled transition, what is the maximum transient reduction in $\rho(\mathbf{x})$? Does the ODD safety margin account for this transient model inaccuracy?

## Minor Issues

**m1.** Eq. (3): The ARX model order (2,2) should be justified. Why not (1,1) or (3,3)? Brief model order selection analysis (AIC/BIC criterion) would be helpful.

**m2.** Table 3b ($\lambda$ sensitivity): Report the 95% confidence intervals for the RMSE values, not just mean ± std.

**m3.** Section 7.6 (Digital Twin): The distinction between "self-calibrating" and "self-adaptive" digital twins should be clarified — both terms appear in the literature with overlapping meanings.

**m4.** The ADMM convergence criterion for DMPC is not specified. What stopping tolerance is used? How does it affect the coordination quality?

## Reference Audit

- Self-citation rate 24% — acceptable
- Missing: Liberzon, D. (2003). Switching in Systems and Control. Birkhäuser — needed for M1.
- Missing: Hespanha, J. P., & Morse, A. S. (1999). Stability of switched systems with average dwell-time — needed for the formal dwell time argument.
- All existing references verified as appropriate.

## Recommendation

Minor revision addressing the gain scheduling stability (M1) and RLS-ODD coupling (M2). Both can be resolved with a brief theoretical analysis and empirical verification from the existing experimental data. The paper is close to acceptance quality.
