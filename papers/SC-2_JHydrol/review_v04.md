# Review Report — SC-2 v03 → v04

**Reviewer**: A (Theory Rigorous)
**Iteration**: 3

**Score**: 8.0 / 10
**Verdict**: **Minor Revision**

## Major Issues

**M1. FMI coupling stability not analyzed.** The Co-Simulation coupling (1.0 s step, variable-step FMU + fixed-step Simulink) may introduce numerical instability for stiff systems. Provide a stability analysis: what is the maximum communication step size that preserves stability? Reference Gomes et al. (2018, §4.3) on co-simulation stability.

**M2. IDZ identification error propagation to DMPC.** The IDZ parameters have ±5% confidence intervals (Table 3). Quantify how this uncertainty propagates to DMPC performance: what is the worst-case RMSE degradation if all IDZ parameters are simultaneously at their 95% CI bounds?

## Minor Issues

**m1.** ADMM convergence guarantee: state the sufficient condition (Lipschitz continuity + strong convexity) and verify it holds for the five-pool DMPC.
**m2.** Table 5b: report the FMU evaluation time (ms per step) for each communication step size.
