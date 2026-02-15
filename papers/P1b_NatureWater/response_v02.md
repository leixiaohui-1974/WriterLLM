# Revision Response — P1b Nature Water v01 → v02

**Iteration**: 1
**Reviewer**: B (Engineering Practitioner)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Broader Community Engagement

**Response**: Accepted. A Nature Water Perspective must situate CHS within a convergent community trend.

**Action taken**:
- Added Clemmens et al. (2005) ASCE test cases as the benchmark that catalyzed canal automation research
- Added van Overloop (2006) TU Delft canal MPC thesis
- Added Savic (2022) digital water developments in Engineering
- Added Horváth et al. (2024) WRR automatic IDZ model selection
- Added Kratzert et al. (2019) as data-driven hydrology benchmark
- Revised the "Structural invariants" section to acknowledge that "the canal automation community — from Schuurmans (1997) through Litrico and Fromion (2004, 2009) and van Overloop (2006) to Horváth et al. (2024) — established the control-theoretic tools for individual canal pools. CHS extends this work to a cross-sector unification and system-level architecture."
- Added a sentence in the implementation section acknowledging international canal automation efforts: "These Chinese implementations complement international efforts: the ASCE canal control test cases (Clemmens et al., 2005) established performance benchmarks; Dutch research demonstrated operational MPC on real canals (van Overloop et al., 2010; Horváth et al., 2024); and Australian irrigation modernization programs have deployed automation at scale."

### M2. Implementation Evidence Qualification

**Response**: Accepted. Simulation-based results must be clearly distinguished from operational outcomes.

**Action taken**:
- Shaping: Added explicit qualifier: "in model-in-the-loop testing with historical inflow data — simulation-based validation, not operational deployment results."
- Jiaodong: Added: "These results represent validated simulation performance; operational deployment with full closed-loop control is underway."
- Added an international example: the Dutch Maeslant Barrier (automated storm surge barrier, operational since 1997) as a precedent for fully autonomous water infrastructure control at the individual-facility level.

### M3. Automotive Analogy Limitations

**Response**: Accepted. Adding a paragraph on where the analogy breaks.

**Action taken**: Added a new paragraph after the initial automotive analogy:
"The automotive analogy is instructive but imperfect. Three differences shape the water sector's path. First, standardization: SAE J3016 emerged from broad industry collaboration; WSAL requires similar international consensus-building through organizations such as IAHR and ISO TC 224, not adoption of any single research group's classification. Second, market incentives: automotive autonomy is driven by massive private investment; water infrastructure is predominantly public, and the economic case must emphasize avoided losses (non-revenue water, energy waste, flood damage) rather than new revenue streams. Third, consequence scale: an autonomous vehicle failure affects individual passengers; a water system failure can affect an entire city or region. This asymmetry of consequences demands even more rigorous verification than automotive standards require."

### M4. Cognitive Intelligence — LLM Credibility

**Response**: Partially accepted. We maintain the architectural role of Cognitive Intelligence but strengthen the qualification.

**Action taken**:
- Revised the Cognitive Intelligence description to: "Built on scenario recognition models, knowledge graphs, and hybrid AI methods" — removing the specific LLM framing while maintaining the functional description.
- Added: "The reliability concerns inherent in probabilistic AI systems — including hallucination, distributional shift, and lack of formal verification (Richards et al., 2023) — are addressed architecturally: Cognitive Intelligence may only propose actions that Physical AI has validated against hydraulic constraints. No AI-generated decision reaches an actuator without passing through the physics-based safety filter."
- Replaced Brown et al. (2020) with Kratzert et al. (2019) and added Shen et al. (2023) for differentiable hydrology. Retained Lewis et al. (2020) as RAG is relevant for knowledge retrieval.

### M5. Equity — Concrete Mechanisms

**Response**: Accepted.

**Action taken**: Replaced the generic IAHR/SWAN statement with concrete mechanisms:
"Three specific mechanisms can ensure equitable access. First, open-source control algorithms: the MPC and DMPC implementations underlying HDC should be released under permissive licenses, following the precedent of OpenFOAM in computational fluid dynamics. Second, open verification standards: WSAL certification criteria and xIL testing protocols should be developed as ISO or IAHR open standards, freely available to all water utilities regardless of size or location. Third, capacity-building partnerships: technology transfer programs pairing advanced research institutions with developing-country water utilities — modelled on the Global Water Partnership's approach — should be integral to WSAL deployment, not an afterthought."

---

## Response to Minor Issues

### m1. Word Count
**Action**: Tightened several sections. Net effect: approximately +200 words from additions, −100 from tightening. Will further tighten in next revision if needed.

### m3. "Hierarchical Distributed Swarm Intelligence"
**Action**: Removed. The term is not sufficiently developed to justify inclusion and may confuse readers.

### m4. Reference 40 — Fuzhou
**Action**: Added brief description: "Fuzhou's smart water platform (Lei et al., 2022), which integrated real-time hydraulic monitoring with dispatch optimization across an urban water supply network."

### m5. Closing Paragraph
**Action**: Softened to: "The technical foundations are advancing rapidly, but significant challenges remain in theory, standards, governance, and equity. Meeting these challenges requires the collective commitment of the research community, industry, and policymakers."

---

## Version Summary

- **v01 → v02 changes**: Added 6 international community references (M1); qualified implementation results as simulation-based, added Maeslant Barrier international example (M2); added automotive analogy limitations paragraph (M3); revised Cognitive Intelligence framing from LLM-specific to hybrid AI, strengthened safety qualification (M4); added three concrete equity mechanisms (M5); removed "swarm intelligence" (m3); softened closing (m5).
- **Self-citation rate**: Reduced from ~25% to ~18% by adding 6 non-self references.
