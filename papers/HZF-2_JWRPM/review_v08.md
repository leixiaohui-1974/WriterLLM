# Review — HZF-2 Iteration 7

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v05
**Score**: 9.5 / 10
**Verdict**: Accept

---

## Summary

ParaQP is a parallel QP solver for distributed MPC of water conveyance networks, providing 18.4× speedup on a 16-core industrial PC. After four revision rounds, the paper is comprehensive: convergence theory, commercial solver comparison, fault tolerance, HiL validation, deployment guide, and alternative hardware platforms. This is exactly the kind of paper that water systems engineers need to adopt distributed control.

## Strengths

1. **Deployment-ready**: The combination of the deployment guide (§4.4), alternative hardware discussion, Docker-based testing, and fault tolerance analysis makes ParaQP ready for real-world adoption. This is rare for an academic optimization paper.

2. **Honest performance comparison**: Table 10 shows that Gurobi is 13% faster—the authors don't hide this. The advantages (7× less memory, no commercial license, bounded WCET) are genuine engineering differentiators for embedded deployment.

3. **HiL validation**: Table 11 provides the crucial SiL-to-HiL bridge. The 0.3 mm RMSE increase from SiL to physical flume is minimal and builds confidence in the simulation results.

4. **Scalability clarity**: Table 9 shows honest scaling to 100 pools (580 ms, 31.2× speedup) with decreasing parallel efficiency—no overclaiming. The recommendation for Area Agent decomposition beyond 80 pools is practical.

5. **Energy analysis**: Table 13 provides the energy-per-cycle data needed for solar-powered remote site planning. The 0.14% of 50 W panel capacity is a compelling figure.

6. **Fault tolerance**: The three failure scenarios with quantified impact (core failure: 40% overhead, comm loss: <3 mm RMSE, sensor fault: ODD-detected) give operations managers the information needed for risk assessment.

## Minor Comments (Non-Blocking)

1. Future work could include integration with SCADA alarm systems—when ParaQP switches to fallback mode, the SCADA should generate appropriate alarms. This is an implementation detail, not a paper issue.

## Decision

**Accept**. This is an excellent contribution to practical distributed control for water systems. The paper combines solid theory with engineering pragmatism, and the deployment guidance makes it immediately useful for practitioners. Ready for publication in JWRPM.
