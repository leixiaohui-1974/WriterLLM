# Response to Reviewer B (2nd review) — Paper P-DC (EMS v04 → v05)

We thank Reviewer B for confirming that the previous major concerns have been addressed and for the two practical suggestions that strengthen the paper's utility for the water engineering community.

---

## Minor Issues

### m1. Industry Adoption Pathway

**Response**: Added a paragraph in §7.1 describing an incremental adoption pathway:
- **Stage 1 (Immediate)**: Introduce a "DfO Design Review Checklist" as a supplementary requirement in existing procurement processes—5–10 additional design review questions covering controllability, observability, and ODD achievability.
- **Stage 2 (2–5 years)**: Pilot DfO requirements in specific project types with high automation potential: inter-basin water transfers, automated irrigation districts, and urban pump station networks.
- **Stage 3 (5–10 years)**: Formalize DfO as a design standard (analogous to ISO 26262 in automotive), with WSAL-level requirements embedded in regulatory frameworks.

This graduated pathway mirrors the industry adoption trajectory of model-based design in automotive (ISO 26262 took ~15 years from concept to mandatory standard).

### m2. Cost-Benefit Framing

**Response**: Added a parametric cost-benefit estimate in §7.1 based on the reference workflow:
- **Design-phase cost**: Adding DfO provisions (sensor placement optimization, actuator co-sizing, ODD specification, xIL test plan) adds an estimated 5–8% to the design engineering budget—approximately ¥500K–800K for a ¥10M canal control project.
- **Retrofit cost**: Post-construction sensor and actuator additions typically cost 3–5× the equivalent design-phase provisions due to civil works, system shutdown, and re-commissioning.
- **Operational savings**: Autonomous control (WSAL-2+) reduces operational labor by 40–60% and improves water delivery efficiency by 5–15% compared to manual SCADA operation, based on early results from the Shaping hydropower and Jiaodong transfer projects (Lei et al., 2025c).
- **Lifecycle ratio**: Over a 30-year operational lifecycle, the design-phase DfO investment represents <0.5% of cumulative operational costs, while the operational savings are 10–20× the DfO investment.

These are order-of-magnitude estimates acknowledged as such; precise cost-benefit analysis requires project-specific data and is identified as a research need.

---

## Summary of Changes (v04 → v05)

| Change | Section | Type |
|--------|---------|------|
| Industry adoption pathway (3 stages) | §7.1 | Minor |
| Cost-benefit parametric estimate | §7.1 | Minor |
