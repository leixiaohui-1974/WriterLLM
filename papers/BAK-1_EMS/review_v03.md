# Review Report — Paper BAK-1 (Environ. Model. Softw. v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

The revised manuscript is substantially improved. The addition of testing infrastructure (§4.4), reproducibility artifacts (§4.5), component-level validation (§5.4), and computational benchmarks (§5.5) addresses the major concerns from the previous review. The self-citation rate is now appropriate (~22%). However, the paper remains narrowly framed as a CHS-specific tool and misses an opportunity to position HydroComponents within the broader digital twin and AI-for-water ecosystems. Additionally, the relationship between this library and emerging data-driven/ML approaches to hydraulic modeling is not discussed, which is a significant gap given the target audience of *Environmental Modelling & Software*.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. No Discussion of Data-Driven/ML Model Integration

The library provides physics-based models only (Saint-Venant and transfer functions). However, the EMS audience increasingly uses hybrid physics-ML approaches (physics-informed neural networks, neural ODEs, surrogate models). The paper should discuss:
- How can HydroComponents interface with ML-based surrogate models? (e.g., a trained neural network replacing the LSV solver for real-time applications)
- Can the FMI interface accommodate ML models exported from TensorFlow/PyTorch via ONNX?
- How does the multi-fidelity hierarchy relate to data-driven model reduction?

This is not asking for implementation—just a discussion in §7 about the pathway for hybrid modeling.

**Recommendation**: Add a §7.4 "Towards Hybrid Physics-ML Modeling" discussing how the FMI interface and multi-fidelity architecture create natural extension points for ML surrogate integration.

### M2. Digital Twin Framing Missing

HydroComponents is, in essence, the modeling backbone of a digital twin for water conveyance systems. The paper never uses the term "digital twin" or discusses how the library fits into the broader digital twin ecosystem (Azure Digital Twins, FIWARE, OGC SensorThings). For the EMS audience, this framing would significantly increase impact and discoverability.

**Recommendation**: Add a paragraph in §7.1 connecting HydroComponents to the digital twin concept. The FMI export + real-time simulation capability (3,273× real-time for 50 pools) directly enables digital twin applications. Cite relevant digital twin reviews for water systems (e.g., Pedersen et al., 2021; Ramos et al., 2022).

---

## Minor Issues

### m1. FAIR Data Principles Not Mentioned

EMS strongly encourages compliance with FAIR (Findable, Accessible, Interoperable, Reusable) data principles. The Software Availability section should explicitly map to FAIR: the GitHub repository is Findable (DOI via Zenodo?), Accessible (MIT license), Interoperable (FMI standard), Reusable (Docker, tests).

### m2. No Zenodo DOI or Archived Release

The GitHub URL may change or become unavailable. EMS best practice is to archive a specific release on Zenodo with a DOI. This should be mentioned in the Software Availability section.

### m3. Example Notebooks Not Described

§4.5 mentions "three Jupyter notebook tutorials" but their content is not described. What do users learn from each? This would help readers assess the library's usability.

### m4. Comparison with OpenWaterAnalytics

The EPANET/WNTR (Water Network Tool for Resilience) ecosystem from OpenWaterAnalytics is the most widely used open-source water network modeling toolkit. While it focuses on pressurized networks rather than open channels, its omission from the discussion may seem like an oversight to EMS readers. A brief mention of how HydroComponents complements WNTR would strengthen positioning.

### m5. Sustainability Plan for Open-Source Project

EMS reviewers increasingly ask about long-term sustainability of research software. Who will maintain HydroComponents after the project funding ends? Is there a community governance plan? A brief statement in §7 would address this.

---

## Reference Verification

All 21 references verified. The new additions (Buyalski, Capart & Zech, Elmqvist et al., Henry, Malaterre et al., Malaterre & Baume, Schuurmans, Swamee) are appropriate and correctly cited.

Self-citation rate: 5 Lei-group / 21 total = 24%. Acceptable but at the upper boundary. Adding the 2 recommended new references (digital twin reviews) will bring this to 22%.

## Summary

Minor revision. The software engineering aspects are now solid. The two remaining gaps—ML integration pathway and digital twin framing—are discussion-level additions that would significantly increase the paper's impact and relevance to the EMS readership.
