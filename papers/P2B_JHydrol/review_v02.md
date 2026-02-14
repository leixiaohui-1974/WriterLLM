# Review — P2B Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v01
**Score**: 6.5 / 10
**Verdict**: Major Revision

---

## Summary

This paper applies the CHS framework to the Shaoping cascade hydropower system with SiL verification and ODD definition. The case study is interesting and the structural isomorphism comparison is novel. However, several significant issues need addressing before the paper is suitable for Journal of Hydrology.

## Major Issues

### M1. No comparison with state-of-the-art hydropower optimization
The paper compares HDMPC only against "conventional rule-based dispatch" (Table 6). The hydropower optimization literature is extensive—dynamic programming (Labadie, 2004; Zhao et al., 2012), stochastic optimization (Feng et al., 2017), and deep reinforcement learning (e.g., Xu et al., 2021) are widely used. Without comparison to at least one established optimization method, the 81% improvement claim is misleading.

**Required**: Add comparison against either DP-based scheduling or MILP-based unit commitment on at least one scenario.

### M2. Turbine cavitation and operational forbidden zones not addressed
Real cascade turbines have forbidden operating zones (rough zones) where cavitation and vibration preclude operation. These create non-convex constraints that cannot be directly handled by the QP-based MPC. The paper ignores this entirely.

**Required**: Discuss turbine forbidden zones, either as ODD constraints or as a limitation with mitigation strategy.

### M3. Self-citation rate too high
Counting references: 17 total, of which approximately 10 are self-citations (Lei 2025a, Lei & Wang 2025, Lei 2025b, Lei 2025c, Bai 2026, Chen 2026a, Chen 2026b, Huang 2026a, Huang 2026b, Su 2026, Yin 2026). This yields ~59% self-citation. The J. Hydrology community expects extensive engagement with the hydropower literature.

**Required**: Add 12–15 external references on hydropower optimization, cascade control, and model predictive control for power systems to bring self-citation below 25%.

### M4. Flood routing and sediment not discussed
For a Journal of Hydrology paper, hydrological processes must be adequately addressed. The paper focuses on power dispatch but does not discuss:
- Flood routing through the cascade (critical for Pubugou's flood control function)
- Sediment transport effects on turbine efficiency and reservoir storage
- Hydrological uncertainty in inflow forecasting

**Required**: Add a discussion of flood routing within the MPC framework and acknowledge sediment/uncertainty as limitations.

### M5. Economic analysis missing
Hydropower operators optimize for revenue, not just power tracking. The 2.8 MWh additional energy capture per ramp event (§6.2) should be contextualized:
- What is the annual economic value?
- How does HDMPC affect revenue under time-of-use pricing?
- What is the computational infrastructure cost (CX2062 IPC)?

**Required**: Add economic analysis for at least one representative month.

## Minor Issues

### m1. Table 2 model fit ($R^2$) declines downstream
The model fit decreases from 0.94 (Pubugou) to 0.87 (Shaoping). This may indicate that the Family β linearization is less appropriate for run-of-river stations. Discuss this trend.

### m2. Safety factor justification
SF = 1.5 is stated without justification. How was this value chosen? Is it based on regulatory requirements, historical incidents, or engineering judgment?

### m3. Grid coupling treated as exogenous
The paper acknowledges (§6.1) that grid frequency is treated as exogenous. For a 4,470 MW cascade (significant grid contribution), this may not be valid. Quantify the cascade's frequency response contribution.

## Recommendation

**Major Revision**. The case study is valuable but needs stronger positioning within the hydropower literature, operational realism (forbidden zones, flood routing), economic analysis, and substantially reduced self-citation.
