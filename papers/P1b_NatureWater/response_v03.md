# Revision Response — P1b Nature Water v02 → v03

**Iteration**: 2
**Reviewer**: C (Cross-disciplinary Scholar)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Narrative Structure — Automotive Analogy Placement

**Response**: Accepted. The reviewer's structural insight is correct — the analogy limitations paragraph will be more effective after readers have seen the WSAL classification.

**Action taken**:
- Moved the automotive analogy limitations paragraph from "The infrastructure–intelligence gap" section to immediately after the WSAL level descriptions, reframed as "How WSAL differs from SAE J3016." The three differences (standardization, market incentives, consequence scale) now directly follow the reader's first encounter with both classification systems, making the comparison concrete.

### M2. Climate Non-stationarity — Central Argument

**Response**: Accepted. This is the paper's strongest argument for Nature Water and was underexploited.

**Action taken**:
- Added to "From allocation to control" section: "The urgency of this transition is compounded by a foundational crisis in the planning paradigm. Classical WRSA assumed hydrological stationarity — that historical statistics reliably predict future conditions. Climate change has invalidated this assumption: as Milly et al. (2008) argued, 'stationarity is dead'[57]. Non-stationarity means that even optimal static allocations become progressively mismatched to actual conditions. The hydrological community has recognized this paradigm shift through the IAHS 'Panta Rhei' decade on change in hydrology and society (Montanari et al., 2013)[67]. Real-time adaptive control is therefore not merely an efficiency gain — it is becoming a necessity as the planning-based paradigm's foundational assumption erodes."
- Added one clause to the Abstract: "compounded by climate non-stationarity that undermines planning-based approaches" (also addresses m1).
- Added Montanari et al. (2013) as reference [67].

### M3. Physical AI–Cognitive AI Interaction — Concrete Example

**Response**: Accepted. The propose-validate loop needs a tangible illustration.

**Action taken**:
- Added after the abstract description of the interaction loop: "To illustrate: during an unexpected drought, Cognitive Intelligence might recognize the scenario from historical precedents and knowledge graphs, and propose revised delivery targets — reducing allocations to lower-priority demand nodes while maintaining minimum supply to hospitals and critical facilities. Physical AI would then simulate the proposed operating plan against the network's hydraulic model, verifying that the reduced allocations are physically feasible without violating minimum pressure constraints, pipe velocity limits, or reservoir safety levels. Only after this physics-based validation would the validated schedule be presented to the operator for confirmation (WSAL-2) or executed directly (WSAL-3 and above)."

### M4. "Operational Singularity" Terminology

**Response**: Accepted. Given the extensive AI discussion in this paper, the disambiguation is necessary.

**Action taken**:
- Added parenthetical clarification: "We term this combination 'operational singularity' — using 'singularity' in its original sense of uniqueness, distinct from the mathematical or AI-discourse meanings — : the co-occurrence of these five properties makes water systems fundamentally different from other controlled processes and necessitates a dedicated theoretical framework."

### M5. Positioning Against Smart Water and Digital Twin Initiatives

**Response**: Accepted. Explicit differentiation will strengthen the novelty claim.

**Action taken**:
- Added to the CHS framework section: "Current smart water and digital twin initiatives have advanced monitoring, data analytics, and decision support capabilities significantly[53,54,66]. CHS complements these advances by providing three elements that existing approaches typically lack: a unified mathematical framework connecting models across water sub-disciplines (the transfer function family unification), a formal autonomy classification (WSAL) with testable entry criteria and defined operational design domains, and a safety architecture (the propose-validate loop) ensuring that AI-augmented decisions respect physical constraints before reaching actuators."

---

## Response to Minor Issues

### m1. Abstract — Climate Motivation
**Action**: Added clause to Abstract (see M2 above): "compounded by climate non-stationarity that undermines planning-based approaches."

### m2. Chinese-Language Sources
**Action**: Added note: "References 14-16 and 19 are Chinese-language publications; the CHS framework is being developed for English-language publication in Water Resources Research (companion paper in preparation)."

### m3. Figure Captions
**Action**: Expanded Figure 2 caption to include propose-validate loop description. Expanded Figure 3 caption to include example L2→L3 criterion: "For instance, an L2→L3 transition requires demonstrating, through systematic model-in-the-loop and software-in-the-loop testing, that the control system maintains safe operation across all scenarios within the defined ODD without human intervention."

### m4. "Cybernetics" Term
**Action**: Added brief justification: "We adopt 'cybernetics' deliberately, connecting to Wiener's (1948) original definition of feedback control in complex systems — a framework that, after decades of fragmented development, is experiencing renewed relevance as water systems integrate sensing, computation, and actuation at network scale."

### m5. Paragraph Length in Challenges Section
**Action**: Split the governance and equity paragraph into two: the first covering liability frameworks and ODD-based responsibility allocation; the second covering the three equity mechanisms and SDG alignment.

---

## Version Summary

- **v02 → v03 changes**: Moved automotive analogy limitations to after WSAL (M1); added climate non-stationarity as central argument with Montanari et al. (M2); added concrete drought scenario for propose-validate loop (M3); clarified "operational singularity" terminology (M4); added explicit CHS vs. smart water differentiation (M5); expanded figure captions (m3); added cybernetics justification (m4); split equity paragraph (m5).
- **New references**: Montanari et al. (2013) [67].
- **Self-citation rate**: ~17% (67 total references, ~11 self-citations).
