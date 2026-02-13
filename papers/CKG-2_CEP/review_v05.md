# Review Report — Paper CKG-2 (Control Eng. Practice v04)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The paper has undergone three rounds of substantial revision and is now a strong submission for Control Engineering Practice. The IEC 61511 alignment, false alarm analysis, 10-pool scaling, dynamics-aware weighting, and Proposition 1 for Bayesian expansion all address my original concerns thoroughly. The safety margin sensitivity analysis provides exactly the kind of practical guidance that utility operators need. Two minor items remain.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Minor Issues

### m1. PLC Implementation Guidance

Table 1c provides execution times on PC, Arduino, and PLC but does not specify which PLC platform was used for the estimates. For field deployment, utilities will want to know: (a) which PLC family (e.g., Siemens S7-1500, Allen-Bradley ControlLogix), (b) whether the ODD monitor fits within a single PLC task cycle alongside the MPC, and (c) the memory footprint. A brief note on PLC implementation considerations would be valuable.

### m2. Scenario S28 (Permanent Communication Loss) — Recovery?

Scenario S28 tests permanent communication loss, but the recovery protocol (§3.4) requires 10 consecutive intervals of $c=1$. For permanent loss, recovery never occurs—the system remains in fallback indefinitely. What happens after the Layer 0 interlock has been active for an extended period? Does the dual-tank drain completely? A brief discussion of the long-duration fallback behavior would be helpful.

---

## Summary

These are truly minor issues that can be addressed with a paragraph each. The paper is very close to acceptance.
