# Review Report — Paper P-DC (EMS v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

This paper proposes Design for Operation (DfO) as a paradigm shift for water engineering, formalizes a seven-layer Model-Based Definition (MBD) framework, and presents an educational software infrastructure for Cybernetics of Hydro Systems (CHS). The revision (v02) has significantly strengthened the reference workflow with quantitative MiL results and introduced formal DfO metrics—both welcome improvements. However, from a cross-disciplinary and impact perspective, the paper has three significant gaps that prevent it from reaching its potential in *Environmental Modelling & Software*.

First, the paper is almost entirely classical control-centric. For an EMS audience, the absence of any discussion of data-driven and machine learning approaches within the MBD framework is a major omission. Modern water systems increasingly leverage hybrid physics-ML models, and the MBD framework should explicitly address where and how these approaches fit. Second, the paper positions DfO as transformative but does not engage with the digital twin literature that dominates the smart water sector—how does DfO relate to, subsume, or extend digital twin frameworks? Third, the educational contribution would be strengthened by an assessment framework: what competencies should CHS graduates demonstrate, and how are these measured?

The paper is well-structured and technically sound within its scope. The cross-domain MBD comparison (Table 1b) is a valuable addition. The reference workflow with quantitative results (Table 6) is convincing. The writing is clear and professional. With the revisions suggested below, this could become a strong contribution to EMS.

**Score: 7.0/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7 | DfO paradigm is genuinely novel for water; MBD adaptation is solid |
| Mathematical Rigor | 7 | DfO metrics well-formalized; reference workflow quantitative |
| Reproducibility | 7 | Software Availability improved; FMI workflow explicit |
| Case Validation | 7 | Single reference workflow; diverse infrastructure types needed |
| Literature Completeness | 6 | Major gap in data-driven/ML literature; digital twin absent |
| Writing Quality | 7.5 | Clear and professional; abstract slightly long |
| System Differentiation | 7 | Cross-domain comparison helpful; digital twin positioning missing |

---

## Major Issues

### M1. Data-Driven and Machine Learning Integration in the MBD Framework

The seven-layer MBD framework is entirely classical: physics-based models (L7), linearized transfer functions (L6), and model-based control (MPC). However, the EMS community—and the water sector more broadly—is rapidly adopting data-driven approaches: neural network surrogate models, physics-informed neural networks (PINNs), reinforcement learning (RL) for reservoir operations, and graph neural networks for pipe network state estimation.

The paper should address:
- Where do data-driven models sit in the MBD hierarchy? Are they Layer 7 surrogates, Layer 6 alternatives, or a parallel pathway?
- How does the MBD framework accommodate hybrid physics-ML models (e.g., physics-constrained neural ODEs as Layer 6 models)?
- What are the implications for safety certification (Layer 4)? Data-driven models pose unique verification challenges.
- The CHS reference implementation uses do-mpc (model-based); what about RL or data-driven MPC?

This is not asking the authors to implement ML—it is asking them to explicitly position the MBD framework relative to the data-driven paradigm, which is the dominant trend in EMS. A subsection in §7 (Discussion) would suffice.

### M2. Digital Twin Positioning

The paper mentions digital twins briefly in §7.4 but only as a related concept. The digital twin framework is the dominant paradigm for operational intelligence in water systems (Rashidi et al., 2020; Conejos Fuertes et al., 2020) and smart infrastructure broadly. The DfO-MBD framework has a natural relationship to digital twins:
- Layer 7 physical models are essentially the digital twin's simulation core
- The MBD pipeline structures the digital twin development process
- DfO extends digital twins by embedding operational intelligence at design time rather than retrofitting

The paper should include a dedicated subsection positioning DfO-MBD relative to digital twins, explaining how DfO subsumes and extends the digital twin concept. This would significantly increase the paper's impact with the EMS readership, for whom "digital twin" is a key frame of reference.

### M3. Educational Competency Framework

The curriculum section (§5) describes software infrastructure but lacks a competency framework. For a paper in EMS that claims to establish a discipline, the educational contribution should be more rigorous:
- What are the expected learning outcomes for each MBD layer?
- What competency levels (e.g., Bloom's taxonomy) should graduates achieve?
- How are competencies assessed? (e.g., can the student derive an IDZ model from Saint-Venant? Can they configure an MPC? Can they run an xIL campaign?)
- How does the proposed curriculum compare with existing water engineering or control engineering curricula?

A competency matrix (MBD Layer × Bloom's level × assessment method) would make this contribution concrete and actionable for other institutions.

---

## Minor Issues

### m1. Abstract Length and Focus

The abstract exceeds 300 words and reads more like a detailed summary than a focused abstract. For EMS, the abstract should emphasize the software/methodological contribution. Consider condensing the MBD layer-by-layer enumeration into a single sentence and allocating more space to the key findings (DfO metrics, reference workflow results, toolchain gaps).

### m2. Self-Citation Balance

The self-citation rate is ~11% (3/28). While within acceptable bounds, for a discipline-construction paper that explicitly builds on the CHS theoretical foundation (P1a, P1c), the connection to the parent theory should be more explicit. Consider citing Lei (2025a) more specifically when referencing theoretical results (e.g., Theorem 2 for unified transfer functions, Proposition 1 for structural isomorphism) rather than generic references.

### m3. Global Context: SDG 6 and Climate Adaptation

The paper frames DfO through a technical lens but does not connect to the broader global context. UN Sustainable Development Goal 6 (Clean Water and Sanitation) and the climate adaptation imperative provide the societal motivation for operational intelligence in water systems. A brief connection in the Introduction or Discussion would strengthen the paper's relevance framing for a global readership.

### m4. Open-Source Emphasis for EMS

EMS has a strong culture of open-source software and reproducibility (Hutton et al., 2016 is already cited). The paper should more explicitly emphasize the open-source philosophy: which MBD layers can be fully supported by open-source tools? What is the pathway to eliminating commercial dependencies (MATLAB, CODESYS)? The reference workflow uses OpenModelica + Python—this open-source pathway should be highlighted as a key contribution for the EMS community.

### m5. Fourth Figure Opportunity

The paper has only 3 figures for ~8,000 words. A fourth figure showing the DfO competency matrix or the MBD-layer educational pathway would enhance the curriculum contribution and improve visual balance.

---

## Summary

This paper makes a genuine contribution in proposing DfO and MBD for water systems control. The v02 revision has substantially improved the reference workflow with quantitative results. The three major revisions requested—ML/data-driven positioning, digital twin framing, and educational competency framework—are all additive rather than structural: they extend the paper's scope without requiring reorganization. Addressing these would elevate the paper from a solid technical contribution to a comprehensive discipline-construction paper that speaks to the full EMS readership. I recommend minor revision.
