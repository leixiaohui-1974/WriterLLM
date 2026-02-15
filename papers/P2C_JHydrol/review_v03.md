# Review — P2C Iteration 2

**Reviewer**: C (Cross-Disciplinary Scholar)
**Draft reviewed**: v02
**Score**: 7.5 / 10
**Verdict**: Minor Revision

---

## Summary

The paper has improved significantly with the addition of water hammer analysis, VFD specifications, baseline characterization, and pump scheduling comparison. The three-layer HDMPC for Jiaodong is a compelling contribution. However, two issues require attention before acceptance.

## Major Issues

### M1. No discussion of learning-based alternatives
The pump scheduling comparison (Table 11) includes DP, GA, and LP but omits the rapidly growing body of work on reinforcement learning (RL) and neural network-based control for water systems (Castelletti et al., 2012; Kong et al., 2020). Given that the paper's own reference list includes Wang et al. (2022), a systematic positioning against RL-based approaches is needed. What are the relative advantages of model-based HDMPC vs. model-free RL for this application?

### M2. No demand forecasting discussion
The System Agent's 24-hour optimization (Eq. 8) implicitly assumes perfect demand knowledge. The paper mentions that offtake demand profiles are "provided 24 h ahead" (§2.6) with ±15% uncertainty, but does not discuss the demand forecasting methodology or its accuracy. For a practical system, demand forecast quality critically affects energy optimization performance. How sensitive is the 7.2% energy saving to demand forecast errors?

## Minor Issues

### m1. No economic analysis
The 7.2% energy saving is expressed in kWh but not translated to annual economic impact (¥/year). Unlike P2B (Ye et al., 2026) which provides a full economic analysis (Table 8), P2C lacks explicit cost-benefit quantification.

### m2. Structural isomorphism could be deeper
Table 8 provides a useful comparison but the ARI of 0.78 is stated without the formal definition used in Ye et al. (2026). The comparison would benefit from a block-by-block accounting of what is reused vs. what is new.

### m3. No environmental flow constraints
The paper focuses on water delivery and energy optimization but does not mention minimum environmental flow requirements at offtake points or in the pipeline itself. Are there ecological constraints?

## Reference Audit

- Fooladivanda & Taylor (2018): Confirmed IEEE TCNS paper.
- Mala-Jetmarova et al. (2017): Confirmed EMS review paper.
- Menke et al. (2016): Confirmed Applied Energy paper.
- Clemmens et al. (2005): Confirmed JIDE paper.
- Malaterre et al. (1998): Confirmed JIDE classification paper.
