# Review Report — Paper P2A (JWRPM v3)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

This paper presents a Multi-Agent System (MAS) architecture and Water Systems Autonomy Levels (WSAL) classification for autonomous water networks, validated through two contrasting case studies. The v02→v03 revision has substantially improved the paper: the case study data placeholders—previously the most critical weakness—are now filled with specific quantitative data (Shaping: 2–3% efficiency gain, 40% water level reduction; Jiaodong: 5–8% energy reduction, ±0.10 m RMSE). The author list is corrected, the validation claim is honestly scoped to HDC+ODD at WSAL-2, cybersecurity is addressed (IEC 62443), the MRC is formalized with τ_coast, and the relationship to prior CHS publications is explicitly delineated.

The paper's core contributions are solid: the formal ODD definition (Definition 1), the three WSAL design principles, and the dual-case topology contrast are all well-conceived. However, as a cross-disciplinary reader, I find several opportunities to strengthen the paper's positioning and broaden its appeal to the JWRPM audience.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7.5 | WSAL and formal ODD are genuine; MAS architecture is more systematization than novelty |
| Mathematical Rigor | 7.5 | MPC/DMPC correctly formulated; ODD definition clean; τ_coast useful |
| Reproducibility | 7 | MiL data now present; but retrospective validation only—no field deployment metrics |
| Case Validation | 7.5 | Significantly improved; both cases now have specific numbers; MiL positioning honest |
| Literature Completeness | 7 | Core water control well-covered; cross-domain gaps remain (see below) |
| Writing Quality | 8 | Clear, professional, well-organized |
| System Differentiation | 8 | Prior work paragraph effective; dual-topology design deliberate and well-argued |

---

## Major Issues

### M1. Digital Twin Relationship Not Addressed

The dominant digitalization paradigm in the water sector is the "digital twin" — a concept that many utilities, consultancies, and government agencies are actively investing in (Conejos et al., 2020; Pedersen et al., 2021). The paper mentions "smart water systems" briefly in the introduction but does not address how the MAS-WSAL framework relates to, differs from, or subsumes the digital twin concept. JWRPM reviewers and readers will immediately ask: "How does this relate to the digital twin work we've been doing?"

**Recommendation**: Add a paragraph in §8.1 or §2.2 explicitly positioning MAS-WSAL relative to digital twins. The key distinction is that digital twins are primarily descriptive and predictive (a model that mirrors the physical system), while MAS is prescriptive and autonomous (agents that act on the physical system). The ODD concept bridges this gap: a digital twin provides the simulation environment for xIL verification, which certifies the ODD within which autonomous MAS operation is permitted. This positions the digital twin as a necessary but insufficient component of WSAL-3+, rather than a competing paradigm.

### M2. Human Factors in Automation Transitions Underexplored

The WSAL-2→3 transition discussion (§7) focuses on technical requirements (xIL verification, ODD monitoring, MRC) but underemphasizes human factors that have been extensively documented in other automation domains. In aviation, automation-induced skill degradation ("automation complacency") has been identified as a major safety concern (Parasuraman & Riley, 1997; Endsley, 2017). When operators shift from WSAL-2 ("in the loop") to WSAL-3 ("on the loop"), their situational awareness of the physical system may decline because they are no longer actively making every control decision. If the system then exits the ODD and reverts to human control, the operator may lack the skills and situational awareness to intervene effectively.

**Recommendation**: Add a discussion of human factors in §7 or §8, covering: (a) operator training requirements for the WSAL-2→3 transition, including regular manual-mode exercises to maintain skills; (b) the "automation surprise" phenomenon and its implications for MRC design; (c) the need for transparent system status displays that maintain operator situational awareness during autonomous operation. Reference the aviation and automotive human factors literature.

### M3. Resilience and Compound Events

The paper frames the motivation primarily in terms of operational efficiency (energy savings, water level tracking). For a JWRPM audience, the resilience perspective—how the system responds to extreme events, cascading failures, and compound hazards (concurrent flood + equipment failure + communication loss)—is equally important and arguably more compelling. The 2021 Texas water crisis, the 2023 Libya dam failures, and increasing compound climate-hydrological events all underscore that water infrastructure resilience is a first-order concern.

**Recommendation**: Add a paragraph in §1 or §8 framing MAS-WSAL as a resilience enabler, not only an efficiency optimizer. Specifically: (a) the ODD framework explicitly addresses degraded conditions and equipment failure scenarios; (b) island-autonomy mode ensures continued operation during communication loss; (c) the Layer 0 safety floor provides invariant protection during cascading failures. This reframing would significantly broaden the paper's appeal.

---

## Minor Issues

### m1. Abstract Length
The abstract is approximately 300 words. JWRPM guidelines specify a maximum of 200 words. The abstract should be condensed—consider removing the detailed case study numbers and focusing on the two contributions (MAS architecture + WSAL classification) and the dual-case validation approach.

### m2. Self-Citation Rate
The reference list contains 28 references, of which 6 are Lei et al. (2025a-d, 2025a English, and Ye et al. 2023 with Lei as co-author) = 21%. While the "Relationship to Prior Work" paragraph provides good justification, adding 5–8 additional non-self references would bring the rate below 15% and strengthen the literature coverage. Suggested additions: Conejos et al. (2020) or Pedersen et al. (2021) for digital twins; Parasuraman & Riley (1997) for human factors; Hashimoto et al. (1982) for reliability/resilience metrics in water systems; and broader MAS literature from power systems (e.g., McArthur et al., 2007) to strengthen the cross-domain parallel.

### m3. Broader Autonomous Infrastructure Context
§2.2 discusses automotive and power systems but does not mention other infrastructure domains that are developing similar autonomy level frameworks: smart grids (IEC 62351, grid automation levels), autonomous shipping (IMO MASS levels), and smart manufacturing (Industry 4.0 automation pyramid). Citing one or two of these would strengthen the argument that water is lagging behind a broad cross-infrastructure trend, not just behind cars.

### m4. Table 2 — WSAL-3 Cybersecurity Criterion
The cybersecurity architecture (§3.4.1) correctly positions cybersecurity certification as a WSAL-3 prerequisite, but Table 2 does not include cybersecurity in the WSAL-3 admission criteria. Add "IEC 62443 compliance" or equivalent to the WSAL-3 criteria column.

### m5. Equation Numbering — (7b)
Equation (7b) for τ_coast uses non-standard numbering. ASCE/JWRPM convention is sequential numbering. Consider renaming to (8) and renumbering subsequent equations accordingly, or labeling it as part of the MRC definition rather than a standalone equation.

### m6. MiL vs. Field Deployment Terminology
The paper uses "operational case studies" and "validated" language that could be misread as field deployment. While §8.4 acknowledges the MiL limitation, the abstract and conclusions should explicitly use "MiL-validated" rather than simply "validated" to prevent ambiguity.

---

## Reference Audit

- 28 references total; reasonable but on the low side for JWRPM
- Self-citation rate: ~21% (6/28) — borderline; adding non-self references recommended
- Missing cross-domain references: digital twin, human factors, resilience, broader autonomous infrastructure
- IEC 61508 and IEC 62443 now included — good

---

## Summary

The v03 revision has addressed the most critical weaknesses of the original draft — case study data is now complete, the validation claim is honestly scoped, and differentiation from prior work is explicit. The remaining issues are primarily about cross-disciplinary positioning (digital twin relationship, human factors, resilience framing) and paper formatting (abstract length, equation numbering, self-citation rate). These are minor revisions that can be addressed in a single round. The core framework is sound and makes a genuine contribution to the water engineering literature.
