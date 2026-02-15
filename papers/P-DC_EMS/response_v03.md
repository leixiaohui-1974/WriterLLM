# Response to Reviewer C — Paper P-DC (EMS v02 → v03)

We thank Reviewer C for the insightful cross-disciplinary perspective. The three major suggestions—data-driven/ML positioning, digital twin framing, and educational competency framework—strengthen the paper's relevance for the EMS readership. All are addressed below.

---

## Major Issues

### M1. Data-Driven and Machine Learning Integration in the MBD Framework

**Response**: Excellent point. We have added §7.5 "Data-Driven and Machine Learning Approaches within the MBD Framework" addressing:
- **Layer positioning**: Data-driven models are positioned as Layer 7 surrogates (for real-time simulation speedup), Layer 6 alternatives (when linearization is inadequate), and Layer 4 challenges (verification of black-box models).
- **Hybrid physics-ML**: Physics-informed neural networks (PINNs) and neural ODEs are discussed as emerging Layer 6 alternatives that preserve physical structure while learning residual dynamics.
- **RL for operations**: Reinforcement learning is positioned as a CI (Cognitive Intelligence) approach at HDC Layer 3, operating above the MPC/MBD stack.
- **Safety implications**: The fundamental challenge of certifying data-driven controllers under WSAL is acknowledged: explainability, distributional shift, and adversarial robustness remain open problems that the ODD framework can structure.
- Two new references added (Razavi et al., 2021; Tsai et al., 2021).

### M2. Digital Twin Positioning

**Response**: We have expanded §7.4 into a dedicated subsection "DfO, MBD, and Digital Twins" that:
- Positions the MBD Layer 7 model as the digital twin's simulation core, with Layers 6–3 providing the controller twin
- Frames DfO as extending the digital twin concept: digital twins mirror existing infrastructure, while DfO embeds operational intelligence at design time—creating an infrastructure that is "born digital twin-ready"
- Distinguishes descriptive digital twins (monitoring) from prescriptive digital twins (control), positioning DfO-MBD as enabling the prescriptive variant
- Added Rashidi et al. (2020) reference for digital twins in water systems

### M3. Educational Competency Framework

**Response**: We have added §5.5 "Competency Framework and Assessment" with:
- A competency matrix (Table 3b) mapping MBD layers to Bloom's taxonomy levels (Remember → Create) with specific learning outcomes
- Assessment methods per layer: written exams (L7–L6 theory), laboratory reports (L6→L7 validation), design projects (L5–L4), code review (L3), and capstone xIL campaigns (L2–L1)
- Comparison with existing curricula: the unique differentiator is the vertical integration from physics to deployment, which neither water engineering nor control engineering programs currently provide
- A brief note on accreditation alignment (ABET Engineering Criteria)

---

## Minor Issues

### m1. Abstract Length and Focus

**Response**: The abstract has been condensed to ~280 words. The layer-by-layer enumeration is replaced with a single sentence summarizing the MBD progression. Space is reallocated to emphasize the reference workflow results and open-source toolchain contribution.

### m2. Self-Citation Balance

**Response**: We have added more specific citations to Lei (2025a) when referencing Theorem 2 (unified transfer function family) and Proposition 1 (structural isomorphism), and to Lei et al. (2025b) when referencing MAS architecture and WSAL. Self-citation rate is now ~14% (4/29), appropriate for a discipline-construction paper.

### m3. Global Context: SDG 6 and Climate Adaptation

**Response**: Added a paragraph in §1 connecting DfO to UN SDG 6, Target 6.4 (water-use efficiency) and the IPCC AR6 emphasis on climate-adaptive infrastructure. This provides the societal motivation for the paper's technical contributions.

### m4. Open-Source Emphasis for EMS

**Response**: Added a paragraph in §4.3 explicitly highlighting the open-source pathway: OpenModelica (L7) + Python/do-mpc (L6) + FMI (coupling) provides a fully open-source MBD pipeline for Layers 7–6. The remaining commercial dependencies (Simulink PLC Coder for L3, CODESYS for L2) are noted, with the open-source alternative pathway (OpenModelica code generation → IEC 61131-3 → open PLC platforms like OpenPLC) discussed as an active research direction.

### m5. Fourth Figure Opportunity

**Response**: Added Figure 4: "CHS Competency Matrix: MBD Layer × Bloom's Taxonomy Level" showing the expected progression from foundational knowledge (L7 physics) through application (L6 control design) to synthesis (L5–L4 architecture and certification) and evaluation (L1 deployment assessment).

---

## Summary of Changes (v02 → v03)

| Change | Section | Type |
|--------|---------|------|
| Data-driven/ML positioning | §7.5 (new) | Major |
| Digital twin positioning | §7.4 (expanded) | Major |
| Competency framework + matrix | §5.5 (new) + Table 3b | Major |
| Abstract condensed | Abstract | Minor |
| SDG 6 connection | §1 | Minor |
| Open-source emphasis | §4.3 | Minor |
| Figure 4: Competency matrix | New figure | Minor |
| Self-citation specificity | Throughout | Minor |
| +3 new references | References | Minor |
