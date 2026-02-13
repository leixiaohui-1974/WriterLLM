# Review Report — Paper P2A (JWRPM v2)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water systems CTO
**Date**: 2026-02-13

---

## Overall Assessment

This paper presents the MAS architecture (MAS = HDC + ODD + CI) and WSAL classification for autonomous water networks, targeting JWRPM (ASCE). The paper is well-structured and addresses a genuine gap: the water sector lacks a shared autonomy classification and a formal system architecture for automation. The three WSAL design principles (bucket principle, non-negotiable safety floor, ODD-bounded autonomy) are well-formulated and water-specific. The formal ODD definition (Definition 1) is useful and actionable. The four-layer HDC architecture is clearly specified with equations.

However, the paper has several critical weaknesses that undermine its engineering credibility. Most significantly, the case study sections (§5 and §6) contain extensive placeholders ([XX]% values) with no actual quantitative data — this makes the paper incomplete for peer review. The author list discrepancy (status.json lists 7 authors but the draft shows only 4) needs resolution. The CI module is described architecturally but acknowledged as unimplemented, which weakens the "validated through operational case studies" claim. The cybersecurity gap seen in earlier papers (P1b, P1c) persists here. And the paper does not differentiate itself from the existing body of work by the same authors (Lei 2025a-d, P1a, P1b, P1c).

**Score: 6.5/10**
**Verdict: Major Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7.5 | WSAL classification and formal ODD are genuine contributions |
| Mathematical Rigor | 7.5 | MPC formulation, ODD definition, DMPC correct and well-specified |
| Reproducibility | 4 | Case studies have placeholder data; cannot evaluate |
| Case Validation | 4 | [XX]% placeholders throughout §5.3 and §6.3; incomplete |
| Literature Completeness | 7 | Good international coverage; some key references missing |
| Writing Quality | 8 | Clear, professional academic English |
| System Differentiation | 6 | Insufficient differentiation from P1a/P1b/P1c; overlap concerns |

---

## Major Issues

### M1. Case Study Data Placeholders — Paper Incomplete

Both case studies (§5 Shaoping, §6 Jiaodong) contain extensive placeholders that render the paper un-reviewable in its current form:
- §5.1: "[River name]", "[N] cascaded reservoirs", "[XX] MW", "[XX] million m³"
- §5.3: "[XX]% improvement", "[XX]% reduction", "[time period]"
- §6.1: "[XX] km", "[XX] pump stations", "[XX] regulating reservoirs", "[XX] control gates"
- §6.3: All performance metrics are placeholder

A JWRPM paper claiming validation through "operational engineering case studies" must provide actual operational data. The entire credibility of the paper depends on these numbers.

**Recommendation**: Fill all placeholders with actual project data. For Shaping: river name (Dadu River), cascade parameters, installed capacity (360 MW per P1c), MIL results (2-3% efficiency gain, 40% water level violation reduction per P1c data). For Jiaodong: total length (~500 km), number of pump stations, MIL results (5-8% energy reduction, ±0.10m RMSE per P1c data). If some data is not yet available, explicitly state what has been validated and what remains prospective.

### M2. Author List Discrepancy

The status.json lists 7 authors: "Xiaohui Lei, Lei Zhang, Shangjun Ye, Chen Ji, Xiaowei Liu, Chao Wang, Hao Wang." The draft manuscript (line 9) lists only 4: "Xiaohui Lei, Chao Su, Yun Long, Hao Wang." This must be reconciled before review can proceed.

**Recommendation**: Resolve the author list to match the intended authorship. The CLAUDE.md specs list "雷/张/叶/姬/刘/王/王" (7 authors) which aligns with status.json.

### M3. CI Module Unimplemented — Validation Claim Overreach

§8.4 honestly acknowledges: "the CI component (Section 3.3) is described architecturally but has not been implemented in either case study." However, the abstract and introduction claim the framework is "validated through two operational case studies." This is misleading — the case studies validate HDC + ODD (the Physical AI engine) at WSAL-2, not the full MAS = HDC + ODD + CI architecture.

**Recommendation**: Revise the abstract and introduction to accurately state what is validated: "The HDC and ODD components of the MAS architecture are validated through two operational case studies at WSAL-2; the CI component is described architecturally and its integration pathway at WSAL-3+ is analyzed." This is more honest and actually strengthens the paper by showing a credible staged validation approach.

### M4. Cybersecurity Not Addressed

The MAS architecture describes Edge Agents communicating with Area Agents via heartbeat protocols, and Area Agents communicating with Cloud Agents — a distributed networked system controlling safety-critical water infrastructure. Yet there is no discussion of:
- Network security for the Edge-Area-Cloud communication channels
- IT/OT segmentation requirements
- What happens if an agent is compromised
- IEC 62443 or equivalent security standard compliance

**Recommendation**: Add a paragraph in §3.4 or §8 addressing cybersecurity: reference IEC 62443, state that L0 safety interlocks must be air-gapped from networked layers, and require that all agent-to-agent communication uses authenticated and encrypted channels. Position cybersecurity as a critical WSAL-3 certification requirement.

### M5. Overlap with P1a/P1b/P1c — Differentiation Needed

This paper shares substantial architectural content with P1a (WRR), P1b (Nature Water), and P1c (中国科学), all by the same lead author. Specifically:
- The MAS = HDC + ODD + CI formula appears in all four papers
- The four-layer HDC architecture is described in P1a, P1c, and here
- The WSAL classification appears in P1b, P1c, and here
- The Shaping and Jiaodong cases are discussed in P1c and here

JWRPM reviewers may flag this as excessive self-overlap, especially if P1a or P1c is published first.

**Recommendation**: Add an explicit "Relationship to Prior Work" paragraph in §1 or §2 stating: "The CHS theoretical framework (Lei, 2025a) provides the mathematical foundations; the present paper's contribution is the formal system architecture specification (MAS agent hierarchy with communication protocols, ODD formal definition, WSAL quantitative admission criteria) and operational validation through engineering case studies — neither of which is provided in the theoretical paper." This clearly delineates the contributions.

### M6. MRC (Minimum Risk Condition) Needs More Specificity

The MRC concept (§3.2) is well-motivated but under-specified. The paper states MRC means "maintain current actuator positions (freeze gates), activate Layer 0 safety floor, alert operators." But:
- "Freeze gates" is not always safe — in a filling canal, freezing the upstream gate while downstream demand continues will cause overtopping. MRC must account for the hydraulic state at the moment of activation.
- The "coast time" τ_coast is mentioned but no formula or estimation method is provided.
- No formal MRC procedure is defined for each case study.

**Recommendation**: Formalize MRC with a water-specific definition. At minimum: (a) define MRC as "transition to a predefined safe steady-state that is reachable from any state within the ODD, within τ_coast"; (b) provide τ_coast estimation based on system hydraulic parameters; (c) specify the MRC procedure for both Shaoping (e.g., ramp turbines to minimum and open spillway) and Jiaodong (e.g., close upstream pump stations, maintain downstream gates at current position, drain excess to emergency storage).

---

## Minor Issues

### m1. "Shaoping" vs "Shaping"
The paper uses "Shaoping" throughout (沙坪 in P1c), but the pinyin romanization of 沙坪 should be "Shaping" (not "Shaoping" which would be 沙坡). Verify and use correct romanization consistently.

### m2. Layer 0 SIL Rating
§3.1 describes Layer 0 PLC safety interlocks but does not specify the Safety Integrity Level (SIL) per IEC 61508. For safety-critical water infrastructure, L0 should specify SIL 2 or SIL 3.

### m3. DMPC Convergence Guarantee
§3.1 states "Convergence to a feasible coordinated solution is guaranteed under standard convexity assumptions." Add a caveat for non-convex cases and acknowledge that convergence may not hold under strong coupling.

### m4. Equation (7) — ODD Monitor
The conjunction ⋀ in Equation 7 means ODD is violated if ANY dimension exits its range. Consider whether this is too conservative — should there be a tolerance or hysteresis to prevent oscillation between in-ODD and out-of-ODD states?

### m5. Figure 5 Missing Reference
The paper describes 5 figure captions but §7 references "Figure 5" which is not in the figure captions list. Add Figure 5 (xIL verification roadmap or WSAL-2→3 transition diagram).

### m6. Climate Change Driver
The introduction lists "advances in sensing, communication, and computing" as motivators but does not mention climate non-stationarity as a driver for autonomous control. This was a key argument in P1b and P1c; its absence here is conspicuous.

### m7. Equity and Accessibility
The paper proposes WSAL as a global standard but does not discuss how smaller utilities or developing countries — which lack xIL verification infrastructure — can participate. A brief note on scalability and accessibility would strengthen the governance discussion (§8.3).

---

## Reference Audit

- **Lei (2025a)**: Listed as "Manuscript submitted to Water Resources Research" — update if published.
- **Savic (2022)**: Valid reference for digital water comparison.
- **Missing references**: IEC 62443 (cybersecurity), IEC 61508 (functional safety), Milly et al. 2008 (climate non-stationarity), Richards et al. 2023 (AI in water systems — Nature Water).
- Overall: 20 references is low for a JWRPM paper; typical is 30-50. Add references for cybersecurity, climate drivers, AI safety, and broader smart water literature.

---

## Summary

This paper addresses a genuine and important gap — the water sector needs a formal automation architecture and maturity classification. The MAS architecture and WSAL classification are well-conceived contributions. However, the paper is currently incomplete: case study data placeholders must be filled, the author list must be resolved, the validation claim must be scoped accurately (HDC+ODD at WSAL-2, not full MAS), cybersecurity must be addressed, and differentiation from the authors' own prior publications must be explicit. These are substantial revisions but the core framework is sound.
