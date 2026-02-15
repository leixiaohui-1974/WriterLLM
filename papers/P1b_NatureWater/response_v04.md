# Revision Response — P1b Nature Water v03 → v04

**Iteration**: 3
**Reviewer**: A (Control Theorist)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. "Proving" Qualification

**Response**: Accepted. The claim was imprecise for a Perspective.

**Action taken**:
- Replaced "by proving" with: "by showing, through systematic linearization around steady-state operating points and low-frequency spatial mode truncation (details in [14]), that the low-order control models of all one-dimensional water systems..."
- This makes the proof method transparent without requiring formal exposition.

### M2. Model Hierarchy Assumption Transparency

**Response**: Accepted. Naming the approximation steps strengthens intellectual honesty.

**Action taken**:
- Added after the model hierarchy description: "Each simplification step involves specific approximations — linearization around an operating point, spatial mode truncation, and ultimately frequency truncation to the zero-frequency (steady-state) limit — whose validity must be verified for each specific system configuration through the in-the-loop testing framework described below."

### M3. WSAL Quantitative Discriminants

**Response**: Accepted. Illustrative metrics make WSAL actionable.

**Action taken**:
- Added a brief paragraph after the WSAL level descriptions: "To make WSAL operationally actionable, each transition requires quantitative discriminants — illustrative examples that future standardization should formalize. L1→L2: >50% of routine operating decisions executed by HDC algorithms under human confirmation. L2→L3: ≥90% of defined ODD scenarios verified through systematic xIL testing with no safety violations. L3→L4: the system demonstrates successful autonomous handling of ≥3 novel scenarios not in the original ODD specification. L4→L5: continuous ODD self-expansion with zero safety-critical failures over a defined operational period."

### M4. Supervisory Control Theory Connection

**Response**: Accepted. This connection grounds the architecture in established theory.

**Action taken**:
- Added to the propose-validate description: "This architecture is formally analogous to supervisory control of discrete-event systems[68], where the physics-based validator acts as a supervisor constraining the cognitive planner's actions to remain within the hydraulically feasible set."
- Added Ramadge & Wonham (1989) as reference [68].

### M5. Dual Principle Grounding

**Response**: Accepted. The two less-standard pairings need justification.

**Action taken**:
- Added justifications for model-reduction–emergence and robustness–coordination: "Model reduction simplifies dynamics to enable tractable control, but emergence — system-level behaviours not present in subsystem models, such as inter-pool resonance in long canals — can only be captured by retaining sufficient model complexity, creating a fundamental trade-off between computational tractability and behavioural fidelity. Similarly, robustness (designing each sub-controller to withstand worst-case disturbances independently) inherently conflicts with coordination (sharing real-time information to achieve collective optimality), because robust margins consume control authority that coordinated strategies could use more efficiently."

---

## Response to Minor Issues

### m1. Operational Singularity Grammar
**Action**: Revised to: "We term this combination 'operational singularity' (here meaning uniqueness of combination, not the mathematical or AI-discourse senses): the co-occurrence of these five properties..."

### m2. Missing Wiener Reference
**Action**: Added: Wiener, N. Cybernetics: Or Control and Communication in the Animal and the Machine (MIT Press, 1948) as reference [69]. Updated in-text citation.

### m3. IDZ Model Terminology
**Action**: Added parenthetical: "integrator-delay-zero models (capturing the level-accumulating, wave-propagating, and backwater dynamics of canal pools[20])."

### m4. DMPC Convergence
**Action**: Added to "Challenges" theory paragraph: "Distributed MPC convergence to coordinated solutions remains an open problem, particularly for non-convex objectives and time-varying communication topologies[28], requiring further theoretical development before DMPC can guarantee network-wide optimality."

### m5. ODD Boundary Approach
**Action**: Added clarification: "When conditions approach ODD boundaries — quantified by safety margins on each ODD parameter, triggering degradation when any parameter enters a predefined buffer zone — the system automatically degrades to human-supervised mode."

---

## Version Summary

- **v03 → v04 changes**: Qualified "proving" claim with approximation method (M1); added model hierarchy assumption sentence (M2); added WSAL quantitative discriminants (M3); connected propose-validate to supervisory control theory (M4); grounded dual-principle tensions with justifications (M5); fixed operational singularity grammar (m1); added Wiener and Ramadge & Wonham references (m2, M4); explained IDZ terminology (m3); added DMPC convergence caveat (m4); clarified ODD boundary mechanism (m5).
- **New references**: Ramadge & Wonham (1989) [68], Wiener (1948) [69].
- **Self-citation rate**: ~16% (69 total references, ~11 self-citations).
