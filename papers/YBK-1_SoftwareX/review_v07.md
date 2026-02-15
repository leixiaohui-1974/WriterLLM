# Review — YBK-1 Iteration 6

**Reviewer**: A (Control Theorist)
**Draft reviewed**: v05
**Score**: 9.0 / 10
**Verdict**: Accept

---

## Summary

This paper presents HydroRTP, a Simulink-based rapid prototyping toolbox for automatic code generation of water network controllers. The toolbox generates IEC 61131-3 Structured Text from Simulink models containing CHS-specific blocks (IDZ plant models, MPC/DMPC controllers, actuator interfaces) and deploys to Siemens S7 and Allen-Bradley ControlLogix PLCs. The manuscript has been substantially improved through four revision iterations and now provides a complete, technically sound software description.

## Strengths

1. **Technically rigorous MPC implementation**: The QP solver description (§2.2) now includes proper convergence criteria (primal infeasibility < 1e-6, 20-iteration cap), warm-start fallback, and safe degradation (hold last command + ODD WARNING). The statistical evidence (mean 4.2 iterations, max 12 across 87 tests) is reassuring.

2. **State estimation options**: The steady-state Kalman filter with optional EKF upgrade (§2.2) provides the right engineering trade-off. The 40% WCET overhead quantification (5.9 ms vs. 4.2 ms) gives practitioners the information needed for resource planning. The guidance on when to use each variant is practical and well-reasoned.

3. **Code generation determinism**: The note on cross-version determinism is important and correctly identifies the source of variation (internal Embedded Coder optimization changes) while pointing to the verification test as the mitigation. This is honest and appropriate.

4. **Scalability with clear limits**: Table 5 provides honest scaling data including the acknowledgment that >80 pools becomes marginal on S7-1516. The recommendation to decompose into Area Agent groups or use faster platforms (Beckhoff TwinCAT) is practical advice.

5. **Integration coherence**: HydroRTP, HydroComponents (Bai et al.), ODD Monitor (Chen et al.), and the xIL pipeline (Lei et al.) form a coherent tool chain. This paper clearly articulates HydroRTP's role within that ecosystem without overclaiming.

6. **License clarity**: The explicit cost breakdown for MATLAB licenses and the simulation-only fallback mode ensure that potential users understand the total cost of adoption. The MIT license for the toolbox itself maximizes accessibility.

## Minor Comments (Non-Blocking)

1. The QP solver is described as an active-set method. For completeness, a citation to the specific algorithm variant (e.g., if based on qpOASES or a custom implementation) would help readers assess computational properties, though qpOASES is already cited in the references.

2. The DMPC communication latency (2.1 ms for 3 pools) is measured on Profinet; it would be helpful to note the Profinet cycle time configuration used, though this is a deployment detail rather than a software description issue.

## Decision

**Accept**. The manuscript presents a well-engineered, well-documented software tool that addresses a genuine need in the water systems control community. The MPC implementation is technically sound with appropriate failsafes, the validation is thorough, and the software quality metrics meet industrial standards. The paper satisfies all SoftwareX requirements for a software description article.
