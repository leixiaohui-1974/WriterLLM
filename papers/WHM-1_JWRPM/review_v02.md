# Review — WHM-1 Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v01
**Score**: 6.5 / 10
**Verdict**: Major Revision

---

## Summary

The three-agent MAS for Miyun Reservoir is a promising contribution. The functional decomposition is well-justified, and the 10-year MiL verification provides statistical robustness. However, several critical engineering aspects require strengthening.

## Major Issues

### M1. No water quality integration
Miyun is Beijing's primary drinking water source. The paper mentions water quality sensors (§2.1) but the MAS does not consider water quality in any optimization objective or constraint. Turbidity spikes during flood events, algal blooms during summer stratification, and temperature-driven quality changes are operationally critical. How would the MAS handle a scenario where ecological flow competes with water quality objectives?

### M2. Self-citation rate too high
Count: 11 of 20 references (55%) are self-citations (Lei/IWHR group). This far exceeds the 25% target. Need substantially more third-party references for: reservoir optimization (only 3 external), multi-agent systems in water resources (0 external), ensemble forecasting for reservoir operations (0 external), and Miyun-specific studies.

### M3. No sediment and ice management
Miyun experiences significant sediment deposition (reducing effective storage) and ice formation (December–March, affecting gate operations and water level measurement). These are operationally critical but entirely absent from the paper.

### M4. No comparison with stochastic optimization
The Reservoir Agent uses deterministic MPC with robust constraint tightening. How does this compare with stochastic programming (SDP/SDDP) or robust optimization approaches that explicitly model uncertainty? The literature on reservoir stochastic optimization is extensive (Celeste & Billib, 2009; Faber & Stedinger, 2001) and must be addressed.

### M5. Operator interaction model missing
At WSAL-2, operators confirm MAS recommendations. How are recommendations presented? What is the override mechanism? What happens when operators reject a recommendation—does the MAS adapt? This human-machine interaction is critical for WSAL-2 operations.

## Minor Issues

### m1. SNWD coordination details sparse
The paper acknowledges SNWD intake is outside Miyun's control but the coordination protocol is vague. What happens when SNWD reduces intake unexpectedly?

### m2. Evaporation model simplistic
Evaporation is treated as a constant (0.8–1.2 m/year). In practice, evaporation varies significantly with season, wind, temperature, and reservoir surface area. A Penman-Monteith or energy-budget model would be more appropriate for a 183 km² surface.

### m3. No downstream flood routing
The paper constrains downstream discharge but does not model flood routing below the dam. The $\Delta Q_{\max} = 50$ m³/s/h rate limit is stated without justification from downstream channel capacity analysis.

### m4. Pareto analysis methodology unclear
Table 4 shows 4 operating points but the Pareto frontier generation method (ε-constraint? weighted sum?) is not described. How many points were explored?

### m5. No cost-benefit analysis
Unlike P2B and P2C which provide explicit economic quantification, WHM-1 lacks any economic analysis of the MAS deployment.

## Reference Audit

- Ehteram et al. (2018): Confirmed J. Cleaner Production paper but this is about energy optimization, not reservoir supply.
- Zhang et al. (2016): Confirmed Hydrology Research paper on SNWD effects on Miyun.
- Zhao (1992): Confirmed classic Xinanjiang model paper.
