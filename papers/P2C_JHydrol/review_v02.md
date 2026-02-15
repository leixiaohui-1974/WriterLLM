# Review — P2C Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v01
**Score**: 6.5 / 10
**Verdict**: Major Revision

---

## Summary

This paper presents a three-layer HDMPC for the Jiaodong inter-basin water transfer system. The multi-timescale decomposition is well-motivated, and the SiL results are promising. However, several critical engineering aspects are missing or insufficiently addressed.

## Major Issues

### M1. No water hammer analysis
The paper mentions water hammer in passing (§4.2 emergency protocol, §3.1 switching penalty) but provides no transient analysis. A 302 km pipeline with 8 pump stations is highly susceptible to water hammer during pump trips, valve closures, and check gate operations. What are the maximum transient pressures? How does the 2 s sampling rate relate to the pipeline's characteristic wave speed? This is a critical safety concern for any real pipeline controller.

### M2. No comparison with existing Jiaodong dispatch
The paper compares HDMPC against generic "rule-based dispatch" (Tables 6, 7) but does not describe the actual dispatch rules currently used at Jiaodong. What specific rules are being outperformed? What are the operators' current pain points? Without this baseline characterization, the 7.2% energy improvement is difficult to contextualize.

### M3. Self-citation rate too high
Counting references: 10 of 23 references (43%) are self-citations (Lei/IWHR group). This exceeds the 25% target. The paper needs substantially more third-party references, particularly for: pipeline MPC (only 2 external refs), inter-basin transfer operations (only 2 external refs), and pump scheduling optimization (0 external refs).

### M4. No pump scheduling comparison
The energy optimization (§3.3 System Agent) is compared only against rule-based dispatch. How does it compare against established pump scheduling methods: dynamic programming, genetic algorithms, linear programming relaxation? These are mature methods widely used in water distribution pump scheduling (Mala-Jetmarova et al., 2017; Fooladivanda & Taylor, 2018).

### M5. Missing VFD dynamics and power quality
The paper assumes ideal VFD behavior ($\omega_j \in [0.6, 1.0]$, continuous). Real VFDs introduce: (a) harmonic distortion at partial speeds, (b) motor heating at low speeds (reduced cooling), (c) torque pulsation near natural frequencies. What are the VFD specifications? Are there speed exclusion zones?

## Minor Issues

### m1. Pipeline profile not described
The paper states free-surface flow transitioning to pressurized flow through pump stations, but no longitudinal profile is provided. What sections are open-channel vs. pressurized? What are the pipe diameters and materials?

### m2. Check gate dynamics omitted
Check gates appear as decision variables ($g_k$) but their dynamics (opening speed, flow coefficient) are not specified. Gate stroke time affects achievable control bandwidth at Layer 2.

### m3. Offtake model missing
Six en-route offtakes are mentioned but not modeled. Are they demand-driven (uncontrolled)? Pressure-dependent? Scheduled? This affects the disturbance model in Layer 2.

### m4. Communication architecture unclear
Table 4 lists Profinet and OPC UA but the physical communication infrastructure (fiber optic, cellular, satellite) for a 302 km system is not described. What are the redundancy provisions?

### m5. cuSVE validation details sparse
The cuSVE model validation ($R^2 = 0.96$) is stated but not documented. What validation period? What scenarios? How were boundary conditions handled?

## Reference Audit

- All CHS group references verified as consistent with prior papers.
- Ocampo-Martinez et al. (2013): Confirmed IEEE CSM paper on Barcelona DWN.
- Grosso et al. (2017): Confirmed JPC paper on chance-constrained MPC for DWN.
- Wang et al. (2022): Cannot verify exact title and journal match — please check.
- Zheng et al. (2013): This is a graph decomposition paper, not directly about pipeline control. Relevance?
