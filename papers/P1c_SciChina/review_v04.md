# Review Report — Paper P1c (中国科学 v3)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher, Nature editorial board
**Date**: 2026-02-13

---

## Overall Assessment

This is my first review of this comprehensive Chinese-language paper (~17,000 words) positioning CHS as a disciplinary bridge between traditional Water Resources Systems Analysis and dynamic autonomous operation. The paper has clearly benefited from a previous round of revision — the "提议—验证" safety architecture for cognitive AI, the cybersecurity discussion (IEC 62443), the quantitative Jiaodong metrics, and the international canal automation acknowledgment all show responsiveness to practitioner concerns.

From a cross-disciplinary perspective, the paper's greatest strengths are: (1) the intellectual honesty of positioning Shaping and Jiaodong as "前期探索" rather than success stories; (2) the elegant unification of diverse water systems through the parametric transfer function families; and (3) the clear articulation of the theory gap between WRSA and operational control (§2.2). The "MAS = HDC + ODD + Cognitive Intelligence" formula is a compelling synthesis.

However, I have several substantive concerns regarding the paper's cross-disciplinary framing and its positioning within the broader international landscape. The paper's narrative structure places too much emphasis on the authors' own work at the expense of situating CHS within the broader intelligent infrastructure discourse. The climate non-stationarity argument — a primary driver of the shift from static to dynamic control — is underexploited. The differentiation between CHS and existing "smart water" or "digital twin" paradigms is insufficient. And the paper misses an opportunity to connect to the broader autonomous systems discourse across transportation, energy, and manufacturing.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | Unified transfer function families and WSAL classification are genuine contributions |
| Mathematical Rigor | 7.5 | Transfer functions well-presented; dual principles now grounded in control theory |
| Reproducibility | 7 | MIL results provided for both cases; cognitive intelligence still aspirational |
| Case Validation | 7 | Shaping and Jiaodong now both have quantitative metrics; positioned as preliminary |
| Literature Completeness | 7 | 58 references; international coverage improved but still missing key cross-disciplinary connections |
| Writing Quality | 8 | Excellent Chinese prose; well-organized |
| System Differentiation | 6.5 | CHS vs "smart water" / "digital twin" distinction not explicit |

---

## Major Issues

### M1. Insufficient Differentiation from "Smart Water" and "Digital Twin" Paradigms

The paper positions CHS as a new theoretical framework but never explicitly distinguishes it from two widely adopted paradigms in the water industry:
- **Smart water networks** (Savic et al. [56]): SWAN (Smart Water Networks Forum) has promoted sensor-driven, data-analytics-based water system optimization for over a decade. How is CHS different from "smart water" — is it the control-theoretic formalization? The emphasis on closed-loop feedback? The unified model hierarchy?
- **Digital twins** (ref [39]): Many water utilities are deploying "digital twins" for real-time operation. The paper mentions digital twins only in the xIL context (§4.3). How does HydroOS relate to commercial digital twin platforms? Is it a specialized instance, a competing paradigm, or a complementary framework?

Without this differentiation, readers from the broader water-AI community may not understand what CHS adds beyond existing approaches.

**Recommendation**: Add a dedicated paragraph (in §1 or §2.2) explicitly positioning CHS against smart water and digital twin paradigms. Suggest framing: "Smart water approaches primarily focus on data-driven analytics and anomaly detection; digital twin platforms provide simulation environments for scenario analysis; CHS uniquely provides a control-theoretic foundation with formal model hierarchies and guaranteed stability properties for closed-loop autonomous operation."

### M2. Climate Non-Stationarity Argument Underexploited

§2.1 mentions "气候变化加剧了水文过程的不确定性" as one of three drivers for the paradigm shift, but this is a single sentence. Climate non-stationarity (Milly et al. 2008 [42]) is arguably the strongest argument for why static WRSA methods are fundamentally insufficient — if the statistical properties of hydrological inputs are changing, any allocation scheme based on historical frequency analysis will become progressively invalid.

This is not just a background motivator — it strikes at the core justification for CHS. Under non-stationarity, the "water balance" paradigm (Phase 1) and the "optimal allocation" paradigm (Phase 2) both assume stationarity. Only real-time feedback control (Phase 3 / CHS) can adapt to a non-stationary world. This should be a central argument, not a passing mention.

**Recommendation**: Expand the climate non-stationarity argument in §2.1 or §2.2: (a) cite Milly et al. (2008) [42] and Montanari et al. (2013) more prominently; (b) explicitly state that stationarity assumptions underpin WRSA Phases 1 and 2; (c) frame CHS as the necessary response to a non-stationary world, where real-time feedback control replaces offline optimization.

### M3. Cross-Domain Autonomous Systems Connection Missing

The paper uses the automotive analogy (SAE J3016) effectively but misses a broader opportunity to position CHS within the wider autonomous systems discourse. Autonomous operation is transforming multiple critical infrastructure sectors simultaneously:
- **Power grids**: Autonomous grid management with distributed energy resources
- **Transportation**: Beyond vehicles, autonomous air traffic management and railway signaling
- **Manufacturing**: Industry 4.0 autonomous production systems

CHS could be positioned as the water sector's parallel to these transformations. This would strengthen the paper's impact for a 中国科学 audience that includes readers beyond the water community.

**Recommendation**: Add a brief paragraph connecting CHS to the broader autonomous critical infrastructure trend. This positions the water sector's transformation within a global technological trajectory rather than as an isolated disciplinary development.

### M4. Narrative Balance — Author Self-Positioning

As a 学科传承综述 (disciplinary heritage review), the paper should balance the authors' own contributions with the broader disciplinary landscape. Currently, the narrative creates an impression that CHS is essentially the authors' framework alone:
- §1 devotes three paragraphs to the authors' series of publications [7-10]
- §5 focuses exclusively on the authors' engineering projects
- The "学科传承" from Wang Hao is positioned as leading directly to CHS

While Wang Hao's WRSA legacy is rightly acknowledged, the paper would benefit from acknowledging other groups working on real-time water system control internationally — e.g., the Delft/Dutch school (van Overloop, Negenborn), the Australian school (Mareels, Cantoni — now cited), the French school (Litrico, Malaterre), and recent Chinese contributions beyond the authors' own group.

**Recommendation**: In §2 or §4, add a brief paragraph surveying the international landscape of real-time water control research, acknowledging parallel developments by other groups. This demonstrates disciplinary maturity and strengthens the claim that CHS represents a synthesis rather than an isolated effort.

### M5. WSAL Quantitative Discriminants Need Calibration Caveat

The v03 revision added quantitative discriminants to WSAL (e.g., L3: "ODD场景覆盖率>80%"). While this is a positive addition, the specific thresholds appear arbitrary — why 80% and not 70% or 90%? Without calibration evidence or analogy to established standards, these numbers may be challenged.

**Recommendation**: Add a calibration caveat: "上述量化判据为初步建议值, 需要通过工程实践和行业共识逐步校准. 具体数值的确定应参考航空航天(DO-178C)和汽车(ISO 26262)领域安全关键系统认证的经验." This acknowledges the preliminary nature while maintaining the useful structure.

---

## Minor Issues

### m1. Wang Hao Legacy Framing
§1 refers to "王浩等[1]创立的水资源系统分析学科体系." The word "创立" (founded) may be too strong — WRSA as a discipline was established internationally by the Harvard Water Resources group (Maass et al. 1962 [11]) and Loucks et al. [5]. Wang Hao's specific contribution was the "二元水循环" theory and its Chinese application. Consider "发展" or "系统完善" instead of "创立."

### m2. English Abstract Length
The English abstract appears quite long for 中国科学 format requirements (typically ~200 words). The current abstract may exceed this. Consider condensing.

### m3. Figure Placeholders
The paper has three figure placeholders ([图1], [图2], [图3]) but the actual figures are missing. For review purposes, the text is self-contained, but the paper needs figures before submission.

### m4. "运行奇异性" Terminology
"运行奇异性" (Operational Singularity) is a striking term, but in the broader AI/technology discourse, "singularity" has a very different connotation (technological singularity). Consider whether this term might confuse interdisciplinary readers, or add a brief clarification that this refers to the unique combination of operational properties, not the AI concept.

### m5. Missing Discussion of Data Quality Challenges
The paper emphasizes sensor-driven closed-loop control (§3.2) but does not discuss the practical challenge of data quality in Chinese water infrastructure — many SCADA systems have unreliable sensors, incomplete coverage, and data transmission gaps. A brief acknowledgment of this challenge would strengthen practical credibility.

### m6. "二八现象" Citation
§5.2 mentions the "二八现象" (80/20 phenomenon) — "非典型场景在水文年平均中只占不到10%的时间, 却消耗了调度人员约50%以上的精力." This is a powerful observation but lacks citation. Is this from the authors' own survey data? Cite the source.

### m7. Reference Format Consistency
Some references use full author lists while others use "et al." Ensure consistency per 中国科学 GB/T 7714 format requirements.

---

## Summary

This is a well-structured and intellectually honest disciplinary review that successfully positions CHS within the evolution of water resources systems analysis. The v03 revisions demonstrate genuine responsiveness to practitioner concerns. The main areas for improvement are cross-disciplinary positioning: differentiating CHS from smart water/digital twin paradigms, connecting to the broader autonomous systems discourse, and balancing the narrative to acknowledge the international research landscape beyond the authors' own contributions. These are achievable within a minor revision and would elevate the paper from a strong team-specific review to a truly definitive disciplinary statement.
