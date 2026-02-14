# Review — P2B Iteration 3

**Reviewer**: A (Control Theorist)
**Draft reviewed**: v03
**Score**: 8.0 / 10
**Verdict**: Minor Revision

---

## Summary

The paper now presents a comprehensive case study of CHS-based cascade hydropower control with SiL verification. The Monte Carlo analysis (§5.5), DP comparison (Table 7), and climate change discussion (§6.8) strengthen the contribution. Two theoretical issues remain.

## Major Issues

### M1. Area Agent MIQP convergence not analyzed
The Area Agent uses MIQP for forbidden zone avoidance (§2.4) but the paper does not analyze worst-case computation time or solution quality. MIQP is NP-hard in general. What is the empirical worst-case solve time across the 16 scenarios? Is the 5-min sampling interval sufficient even for challenging dispatch configurations?

**Required**: Add Area Agent MIQP timing analysis.

### M2. Stability guarantee for dual-timescale HDMPC
The Edge Agent operates at 30 s and the Area Agent at 5 min (10:1 ratio). The paper does not discuss whether the dual-timescale design preserves closed-loop stability. When the Area Agent reference changes, the Edge Agent must track a step change—what is the transient behavior, and does the edge MPC stability proof account for reference updates?

**Required**: Add a stability discussion for the dual-timescale architecture or cite a relevant result.

## Minor Issues

### m1. The ARI metric (0.82) is interesting but needs a formal definition (what counts as a "component"?).

## Recommendation

**Minor Revision**. The control-theoretic aspects (MIQP timing, dual-timescale stability) need brief treatment to satisfy the optimization/control community reading J. Hydrology.
