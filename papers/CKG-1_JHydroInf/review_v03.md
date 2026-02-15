# Review Report — Paper CKG-1 (J. Hydroinformatics v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

This paper demonstrates the seven-layer MBD framework on a dual-tank laboratory platform, completing the MiL→SiL→HiL verification chain. The v02 revision has substantially improved the paper with a scaling roadmap, industrial deployment discussion, MBD vs. traditional comparison, Kalman filter, and expanded literature. The cross-layer fidelity analysis (Table 9) remains the paper's most distinctive contribution—it provides the first empirical quantification of model accuracy degradation across the MBD pipeline in a water systems context.

From a cross-disciplinary perspective, the paper makes a solid methodological contribution but could be strengthened in two areas: (1) the connection to the broader digital twin and Industry 4.0 agenda is absent—positioning the MBD pipeline as a digital twin development methodology would increase impact; (2) the reproducibility contribution could be amplified by more explicitly framing the dual-tank platform as a community benchmark. These are additive suggestions that do not require restructuring.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7.5 | Complete MBD pipeline + cross-layer fidelity analysis is novel |
| Mathematical Rigor | 7 | MPC formulation now explicit; Kalman filter well-motivated |
| Reproducibility | 8 | Data availability statement; platform well-described |
| Case Validation | 7.5 | 16 ODD scenarios; MiL/SiL/HiL all quantified |
| Literature Completeness | 7.5 | Good after v02 additions; digital twin literature still missing |
| Writing Quality | 7.5 | Clear and well-organized |
| System Differentiation | 7.5 | Prior work differentiation improved; scaling roadmap helpful |

---

## Major Issues

### M1. Digital Twin Connection

The MBD pipeline is, in essence, a structured methodology for building digital twins of water systems. The paper does not use the term "digital twin" at all. For the J. Hydroinformatics readership—where digital twin is a major research theme—this is a missed opportunity. A brief subsection connecting the MBD pipeline to the digital twin paradigm would significantly increase the paper's visibility and citation potential:
- The Layer 7 OpenModelica model, when connected to real-time sensor data, becomes a descriptive digital twin
- The complete MBD pipeline produces a prescriptive digital twin (one that not only monitors but controls)
- The FMI standard provides the interoperability layer that digital twin frameworks need
- Liu et al. (2026) already positioned DfO-MBD relative to digital twins; this paper should reference that positioning and demonstrate it concretely

### M2. Community Benchmark Framing

The paper mentions the dual-tank platform as "analogous to OpenAI Gym benchmarks" (§8) but does not develop this idea. For maximum impact, the paper should explicitly frame the dual-tank platform as a proposed community benchmark for MBD methodology:
- Define a standardized benchmark protocol (the 16 ODD scenarios as a baseline test suite)
- Specify what metrics should be reported (RMSE, constraint violations, solve time, cross-layer degradation)
- Invite the community to reproduce the results and extend the benchmark
- This positions the paper not just as a one-off demonstration but as a foundation for systematic comparison of MBD approaches

---

## Minor Issues

### m1. Abstract: Mention Kalman Filter

The abstract reports HiL RMSE of 2.3 mm, but the revised paper now achieves 2.0 mm with the Kalman filter. Update the abstract to reflect the improved results.

### m2. Cross-Layer Fidelity: Visualization

Table 9 is informative but a waterfall chart showing cumulative RMSE buildup from Layer 7 → Layer 6 → MiL → SiL → HiL would be more visually impactful. Consider adding this as a panel in Figure 4.

### m3. Broader Impact Statement

J. Hydroinformatics values practical impact. A brief statement on what this MBD methodology means for the water sector workforce (training needs, skill requirements, organizational change) would connect to the broader digital transformation conversation.

---

## Summary

This paper makes a solid methodological contribution demonstrating the MBD pipeline on physical hardware. The cross-layer fidelity analysis is the key differentiator. Adding the digital twin connection and community benchmark framing would elevate the paper from a demonstration paper to a foundational methodology paper. I recommend minor revision.
