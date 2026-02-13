# Review — YBK-1 Iteration 7

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v05
**Score**: 9.5 / 10
**Verdict**: Accept

---

## Summary

HydroRTP is an open-source Simulink toolbox that automates the generation and deployment of water network MPC controllers to industrial PLCs. This SoftwareX manuscript describes the four-layer architecture (block library, model assembly, code generation, deployment/verification), demonstrates fidelity on a 3-pool laboratory flume (0.3 mm RMSE), and provides scalability analysis up to 100 pools. After four revision rounds, the paper has matured into an excellent software description.

## Strengths

1. **Practitioner-ready**: As someone who deploys controllers on real water infrastructure, I find HydroRTP's approach genuinely useful. The one-click pipeline from Simulink to TIA Portal/Studio 5000 eliminates the most painful step in field deployment: manual recoding. The vendor-specific templates (TIA Portal Openness, L5X) show that the developers understand real-world PLC workflows.

2. **Honest scalability limits**: Table 5 does not oversell—the acknowledgment that >80 pools require decomposition or faster hardware is the kind of honest engineering guidance that builds trust. The recommended path (Area Agent groups of 10–20 pools) aligns with how large canal systems are actually partitioned in practice.

3. **Software quality exceeds typical academic tools**: 87 unit tests, 91% statement coverage, MISRA-C compliance, and Polyspace analysis are unusual for academic water systems software. The 3 documented advisory deviations (with mitigation) show mature engineering judgment.

4. **License transparency**: The explicit cost breakdown (MATLAB ~$500–$5,000/yr, Embedded Coder ~$4,000) is exactly what a CTO needs when evaluating adoption. The simulation-only mode for users without Embedded Coder, and the standalone nature of generated ST files (no MATLAB runtime needed on PLC), are important practical details well articulated in v05.

5. **Semantic versioning and community**: The semver policy and release cadence (bi-annual) signal a sustainable project. The four tutorials with live Simulink models lower the barrier to entry.

6. **Complete QP failsafe chain**: The convergence → warm-start → hold-last-command → ODD WARNING chain (§2.2) is exactly the kind of defense-in-depth that water utilities require. The empirical evidence that the 20-iteration cap was never reached in practice is reassuring but the fallback exists regardless.

7. **EKF option**: Offering both steady-state KF (fast, default) and EKF (robust, optional) with quantified overhead is the right engineering approach. Field commissioning often involves unknown initial conditions where EKF would be essential.

## Minor Comments (Non-Blocking)

1. Future versions might consider adding a "deployment checklist" template (e.g., pre-deployment verification steps, I/O mapping confirmation, safety interlock test) as part of the Layer 4 workflow. This is a suggestion for the software, not the paper.

2. The Allen-Bradley 5580 WCET (5.1 ms) is ~21% slower than S7-1516 (4.2 ms). A brief note on whether this is due to hardware clock speed or compiler optimization differences would be informative, though not essential for the paper.

## Decision

**Accept**. This is a well-crafted software description that clearly communicates HydroRTP's purpose, architecture, and value proposition. The toolbox addresses a real deployment bottleneck in water systems control, provides industrial-grade software quality, and demonstrates its capabilities through rigorous validation. All previous reviewer concerns have been thoroughly addressed. The paper is ready for publication in SoftwareX.
