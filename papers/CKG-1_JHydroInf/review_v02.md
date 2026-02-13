# Review Report — Paper CKG-1 (J. Hydroinformatics v01)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

This paper demonstrates the seven-layer MBD framework on a dual-tank laboratory platform, executing the MiL→SiL→HiL verification chain. The concept is sound and timely—the water sector badly needs a structured methodology for translating models to deployed controllers. The cross-layer fidelity analysis (Table 9) is a genuinely useful contribution. However, several gaps reduce the paper's practical impact: the dual-tank system is overly simple (only 4 states, single actuator), the Arduino platform is not representative of industrial deployment, the IDZ identification does not adequately discuss the transition from "laboratory toy" to "engineering tool," and the literature positioning needs strengthening.

**Score: 6.5/10**
**Verdict: Major Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7 | Complete MBD pipeline is novel; cross-layer fidelity analysis new |
| Mathematical Rigor | 6.5 | IDZ derivation adequate; MPC formulation standard |
| Reproducibility | 7 | Platform well-described; ODD scenarios explicit |
| Case Validation | 6 | Single simple system; no comparison with alternative approaches |
| Literature Completeness | 5.5 | Missing key lab-scale control references; thin on FMI literature |
| Writing Quality | 7 | Clear and well-organized; some sections too brief |
| System Differentiation | 6.5 | Prior work section needs expansion; differentiation from van Overloop unclear |

---

## Major Issues

### M1. Dual-Tank Simplicity and Scalability Argument

The dual-tank system has only 4 states and 1 actuator—far simpler than any real water system. While the paper acknowledges this in §7.4, the scalability argument in §7.3 is hand-waving ("the multi-agent extension is the subject of companion work"). The paper should:
- Provide a concrete complexity comparison: how many states/actuators would a typical canal system have? (e.g., 3-pool canal: ~60+ states, 3 actuators; 10-pool system: 200+ states)
- Discuss what MBD challenges arise at scale that the dual-tank demonstration does not capture (e.g., distributed computation, communication latency, multi-FMU co-simulation performance)
- Consider adding a brief "scaling roadmap" showing how each MBD layer would change from dual-tank to 3-pool canal to field system

### M2. Arduino vs. Industrial Hardware

The Arduino Mega 2560 is an educational microcontroller, not an industrial-grade PLC. Using it undermines the claim that the MBD pipeline is relevant to real water system deployment:
- The 320 ms MPC solve time is only acceptable because the sampling time is 5 s; for a canal system with 60 s sampling, this would scale to ~10+ s on an Arduino for a 60-state system—infeasible
- Industrial PLCs (e.g., Siemens S7-1500, Schneider M340) have different programming environments (Structured Text, not C), different real-time constraints, and different communication protocols (OPC-UA, not serial)
- The paper should either: (a) acknowledge the Arduino as a proof-of-concept platform and discuss what would change for industrial PLC deployment; or (b) demonstrate at least a basic PLC deployment (even a CODESYS soft-PLC on Raspberry Pi would be more representative)

### M3. Comparison with Alternative Approaches

The paper demonstrates the MBD pipeline but does not compare it with the traditional "ad hoc" approach it claims to replace. How much time/effort does MBD save compared to manual controller implementation? What errors does MBD prevent? A concrete comparison—even qualitative—would significantly strengthen the motivation:
- Time comparison: MBD pipeline (model→code generation→verify) vs. manual implementation (design→hand-code→debug→test)
- Error comparison: types of errors caught by MiL/SiL that would not be caught by manual testing
- This could be a brief subsection in §7

### M4. Literature Gaps

The literature review is too thin for a J. Hydroinformatics paper:
- Missing: Clemmens et al. (2005) on canal automation; Weyer (2006) on linearization of canal systems; Xu et al. (2012) on MPC for canal pools; Horváth et al. (2015) on FMI in water systems
- The FMI literature (Gomes et al., 2018 is cited) should include practical applications: Schweiger et al. (2019) on FMI challenges in practice
- van Overloop (2006) is cited but not adequately differentiated—what specifically does this paper do that van Overloop did not?

### M5. Sensor Noise Treatment

The HiL results show 0.5 mm MiL→HiL degradation attributed to "sensor noise, actuator quantization, unmodeled dynamics." This attribution is too vague:
- What is the actual sensor noise spectrum? (Random? Systematic bias? Drift?)
- Is there a state estimator (Kalman filter) in the MPC implementation? If not, why not—and how does raw noisy measurement affect MPC performance?
- The MPC literature for water systems universally includes state estimation; its absence here should be justified or corrected

---

## Minor Issues

### m1. Table 2 Units

Table 2 reports $A_s$ in m² for the dual-tank system. For a 40×30 cm tank, $A_s = 0.12$ m² = 1,200 cm². Please verify that the units and physical interpretation are consistent: $A_s$ in the IDZ model is the storage area (water surface area), which for a prismatic tank equals the cross-sectional area.

### m2. FMI Communication Step Size

§5.3 states "Communication step size: 1 s (5 exchanges per MPC step)." Justify why 1 s rather than matching the MPC step (5 s). Does the 1-s coupling step size affect co-simulation accuracy?

### m3. Missing Equation Numbers

The MPC optimization problem (minimize tracking error subject to constraints) is described in Table 3 parameters but the actual QP formulation is not stated. Please include the MPC cost function and constraint formulation as numbered equations.

### m4. Reproducibility: Data Availability

J. Hydroinformatics encourages open data. Please state whether the OpenModelica model, Simulink controller, experimental data, and Arduino code will be made available (e.g., GitHub repository).

---

## Summary

The paper presents a useful proof-of-concept for the MBD framework in water systems control. The cross-layer fidelity analysis is the strongest contribution. However, the overly simple platform, non-industrial hardware, missing comparisons, and thin literature weaken the paper's impact. Addressing these issues—particularly the scalability argument, Arduino-to-PLC discussion, and comparison with alternative approaches—would significantly strengthen the contribution.
