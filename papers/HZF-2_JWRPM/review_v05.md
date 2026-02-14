# Review — HZF-2 Iteration 4

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v04
**Score**: 8.5 / 10
**Verdict**: Minor Revision

---

## Summary

The paper has matured substantially across four iterations. The ParaQP solver is now well-characterized with convergence theory (including the important Remark 1 on constrained QP), ADMM penalty sensitivity, commercial solver comparison, fault tolerance, HiL validation, and neural MPC positioning. Two minor practical issues remain.

## Minor Issues

### m1. No commissioning/tuning guidance
A practitioner deploying ParaQP on a new canal system needs practical guidance on:
- How to select the decomposition strategy (the §6.1 guidelines are helpful but could be made into a decision flowchart)
- How to set the early termination threshold $\epsilon_p$ for a new system
- How to verify that the warm-start is functioning correctly during commissioning
A brief "Deployment Checklist" or tuning guide paragraph would help field engineers.

### m2. Beckhoff CX2062 availability and alternatives
The CX2062 is the primary recommended platform, but it may not be available in all markets. A note on alternative 16-core IPC platforms (e.g., Wago PFC200, Phoenix Contact PLCnext, Advantech UNO) and whether ParaQP's OpenMP implementation works on these platforms would help practitioners with hardware selection.

## Recommendation

**Minor Revision**. The paper is nearly ready. Addressing the commissioning guidance and hardware alternatives will make it fully practitioner-ready.
