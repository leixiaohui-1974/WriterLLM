# Review Report — Paper CKG-2 (Control Eng. Practice v01)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The paper addresses an important gap: formalizing the Operational Design Domain for water systems and providing a systematic SiL verification methodology. The polytope-based ODD formalization with IDZ-derived safety margins is a solid contribution. However, several issues need attention before the paper is ready for publication in Control Engineering Practice, which has a strong practice orientation.

**Score: 6.5/10**
**Verdict: Major Revision**

---

## Major Issues

### M1. No Comparison with Industrial Safety Standards (IEC 61511 / IEC 62443)

The paper mentions IEC 61511 in passing (§2.3) but never systematically compares the proposed ODD framework with established industrial safety practices. Control Engineering Practice readers expect alignment with Safety Integrity Level (SIL) concepts from IEC 61511. How does the ODD monitor's reliability (100% detection in 16 scenarios) relate to SIL-1/SIL-2 requirements? What is the target SIL for the Layer 0 interlock? The fallback protocol (§3.4) is described informally—an IEC 61511 practitioner would expect a Safety Instrumented Function (SIF) specification with probability of failure on demand (PFD).

### M2. No False Alarm Analysis

The paper reports 100% detection rate (16/16) but provides no false alarm analysis. In a real water utility, false alarms are extremely costly: each spurious ODD VIOLATION triggers the fallback protocol (freeze valve → Layer 0 interlock), disrupting normal operations and requiring operator intervention to reset. What is the false positive rate? How many WARNING events occurred that did not lead to actual violations? Table 3 shows "2 warnings in S11" that were correct warnings (system near boundary), but what about sensor-noise-induced false warnings? This analysis is critical for practical deployment.

### M3. Dual-Tank System Too Simplified for ODD Claims

The dual-tank system has only 7+1 ODD dimensions and 14 linear constraints. The paper acknowledges the scaling challenge (§6.4) but provides no concrete evidence that the formalization works beyond the toy system. At minimum, a simulation-based demonstration on a 10-pool canal system (which is available from CKG-1/HZF-1 validation infrastructure) would strengthen the claims significantly. The polytope representation, distance function, and monitor must be shown to scale.

### M4. ODD Monitor Computational Cost Not Quantified

The ODD monitor (Eqs. 10–12) evaluates 14 constraints at each sampling instant. For the dual-tank system this is trivial, but for a 10-pool system (40+ continuous constraints), the computation time may be significant relative to the MPC solve time, especially on embedded hardware (Arduino or PLC). What is the ODD monitor execution time? How does it scale with the number of constraints?

### M5. No Systematic Sensitivity Analysis for Safety Margin

The safety margin $\delta_h = 5$ cm is derived from Eq. (8–9) with a safety factor of 1.5. But this safety factor is not justified: why 1.5 and not 1.2 or 2.0? A sensitivity analysis showing how the ODD violation rate changes with the safety factor (and the tradeoff with operational range reduction) would be valuable. The 25% reduction in operational range ([5,45] → [10,40]) is substantial—a utility operator would want to know the minimum acceptable margin.

---

## Minor Issues

### m1. Notation Table Incomplete

Control Engineering Practice requires a comprehensive notation table. The current table is missing several symbols used in the paper: $\Delta t$ (sampling time), $N_p$ / $N_u$ are listed but not $A_d$, $B_d$, $C_d$ (state-space matrices). The Kalman filter symbols from Chen et al. (2026a) are used in §6.3 but not defined here.

### m2. ODD for Multi-Agent Systems

§3.1 defines ODD for a single-agent (single-controller) system. For multi-agent systems (the target of CKG-3), how do individual agent ODDs compose? Is the system ODD the intersection of individual agent ODDs? This question is mentioned in §7.8 of Chen et al. (2026a) but not addressed here—yet the paper claims to provide "the methodological foundation for the WSAL-2→3 transition," which inherently involves multi-agent coordination.

### m3. Recovery Protocol Timing

The recovery protocol (§3.4, point 5) requires "5 consecutive intervals with ρ > 0.13" before MPC resumes. This means a 25-s delay after violation clearance. Is this appropriate? What if the violation is transient (e.g., a sensor spike)? The recovery timing should be discussed and potentially made adaptive.

### m4. Reference Formatting

Several references are incomplete or inconsistent. Althoff et al. (2021) is cited as a 2021 paper but the DOI points to a 2010 CDC paper. Macenski et al. (2023) appears misplaced—it is about robot path tracking, not ODD concepts. The SAE J3016 and BSI PAS 1883 citations need full bibliographic details.

### m5. Self-Citation Rate

The paper cites 4 Lei-group papers (Lei 2025a, Lei & Wang 2025, Lei et al. 2025b, Lei et al. 2025c) plus Chen et al. (2026a) = 5 out of 19 total = 26%. This exceeds the 25% guideline. Add 1–2 external references.

---

## Summary

The ODD formalization is a genuine contribution, but the paper needs: (1) systematic comparison with IEC 61511 safety standards, (2) false alarm analysis, (3) scaling evidence beyond the dual-tank toy system, (4) computational cost quantification, and (5) safety margin sensitivity analysis. Addressing these would elevate the paper from a conceptual demonstration to a practical methodology suitable for Control Engineering Practice.
