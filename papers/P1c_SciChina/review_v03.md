# Review Report — Paper P1c (中国科学 v2)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water systems CTO
**Date**: 2026-02-13

---

## Overall Assessment

This is a comprehensive Chinese-language review paper (~17,000 words) positioning Cybernetics of Hydro Systems (CHS, 水系统控制论) as the disciplinary bridge between traditional Water Resources Systems Analysis (WRSA) and dynamic operation control. The paper is ambitious in scope: it covers the full arc from disciplinary evolution (§2), theoretical framework (§3), key technologies (§4), engineering practice (§5), to a development roadmap (§6).

From an engineering practitioner's perspective, the paper has genuine strengths: the six-element architecture (§3.2) provides a clean formalization; the unified transfer function families (§3.3) and the five-level model hierarchy are elegant and useful; and the Shaping hydropower case (§5.1) demonstrates real engineering credibility with quantitative MIL results. The concept of "MAS = HDC + ODD + Cognitive Intelligence" is a compelling architectural vision.

However, several significant concerns reduce the paper's credibility for practitioners. The heavy reliance on a specific proprietary product ("天河大模型") without peer-reviewed evidence of its capabilities, the uncritical framing of LLM-based cognitive intelligence for safety-critical water systems, the absence of cybersecurity considerations in the MAS architecture, and the lack of quantitative performance metrics for the Jiaodong case all need substantive revision. These are not minor polish items — they affect the paper's core credibility claim that CHS is ready to guide water network automation.

**Score: 7/10**
**Verdict: Major Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | CHS framework + unified transfer function families are genuine contributions |
| Mathematical Rigor | 7.5 | Transfer function families and actuator theorem are well-presented; dual principles lack formal grounding |
| Reproducibility | 6 | Shaping has MIL numbers; Jiaodong lacks quantitative metrics; "天河大模型" not reproducible |
| Case Validation | 6.5 | Shaping good; Jiaodong qualitative only; no operational (PIL) validation |
| Literature Completeness | 7 | 50 references; self-citation rate ~22% (high); international canal automation community underrepresented |
| Writing Quality | 8 | Clear, well-organized, engaging Chinese prose |
| System Differentiation | 7 | HDC vs MAS clearly differentiated; CHS vs existing smart water/digital twin insufficient |

---

## Major Issues

### M1. "天河大模型" (Tianhe Large Model) — Unverified Proprietary Product

§4.4 names "天河大模型" as the technical vehicle for Cognitive Intelligence, listing three specific capabilities (knowledge retrieval, scenario recognition, physical constraint verification). However:
- No reference is provided for "天河大模型" — it appears neither in the reference list nor in any publicly available literature.
- The three capabilities described are aspirational, not demonstrated. No benchmark results, no comparison with alternatives, no deployment evidence.
- Naming a specific proprietary product in a disciplinary review paper risks making the paper read as product promotion rather than scholarly contribution.

**Recommendation**: Either (a) remove the "天河大模型" name entirely and describe Cognitive Intelligence in technology-neutral terms (e.g., "the cognitive intelligence engine under development by the authors' team"), with capabilities framed as design goals rather than claimed features; or (b) provide a peer-reviewed reference with documented results. Option (a) is strongly preferred for a 中国科学 disciplinary review.

### M2. LLM Credibility in Safety-Critical Water Systems

§4.4 states that Cognitive Intelligence is based on "大语言模型(LLM)、知识图谱和检索增强生成(RAG)." For safety-critical water infrastructure, this framing raises serious practitioner concerns:
- LLMs are known to hallucinate — producing plausible but factually incorrect outputs. In a system controlling dams and pumping stations, hallucinated control decisions could cause flooding or infrastructure failure.
- The paper mentions that "物理约束校验" verifies LLM outputs against physical models, but no formal guarantee mechanism is described. What happens when the LLM and the physical model disagree? What is the default-safe behavior?
- The broader AI safety community has extensively documented the challenges of deploying LLMs in safety-critical systems (Amodei et al., ref [48]).

**Recommendation**: (a) Revise the framing from "LLM-based" to "hybrid AI methods including knowledge graphs, retrieval-augmented generation, and large language models" — positioning LLMs as one component among several, not the primary engine. (b) Add an explicit "propose-validate" safety architecture: Cognitive AI proposes, Physical AI validates, and any proposal that violates physical constraints is automatically rejected. (c) Reference the safety concerns explicitly and explain how the architecture addresses them.

### M3. Jiaodong Case Study Lacks Quantitative Performance Metrics

§5.2 describes the Jiaodong Water Transfer Project SCADA+HDC system in rich qualitative detail (four core modules, multi-timescale planning, etc.), but provides zero quantitative performance metrics:
- No improvement in pumping energy efficiency (cf. Shaping's 2-3% efficiency gain)
- No reduction in water level violations
- No comparison with manual dispatch performance
- No MIL/SIL test results for the cascading pump station optimization

This creates an asymmetry with §5.1 (Shaping), which reports specific MIL results (2-3% efficiency gain, 40% reduction in water level violations, ±15% robustness to forecast errors). An engineering practitioner reading §5.2 would ask: "If the system works, where are the numbers?"

**Recommendation**: Add quantitative MIL/SIL test results for the Jiaodong system. At minimum: (a) energy cost reduction under the optimized pumping schedule vs. historical manual dispatch; (b) water level tracking performance (RMSE or MAE) under the coordinated control; (c) robustness test results under demand forecast uncertainty. If quantitative results are not yet available, state this honestly and explain why (e.g., "the system is in commissioning phase; MIL validation results will be reported in [companion paper reference]").

### M4. Cybersecurity Gap in MAS Architecture

§4.4 describes a multi-layered MAS architecture with Edge Agents on local controllers, Area Agents for regional coordination, and Cloud Agents in IT networks — with bidirectional information flows between layers. This is precisely the architecture topology that is vulnerable to cyberattack:
- Cloud-to-Edge command channels could be compromised to inject malicious control commands
- Edge-to-Cloud state reporting could be spoofed to trigger inappropriate coordinated responses
- The "双向信息流" between layers creates attack surfaces at every interface

Yet the paper contains no discussion of cybersecurity — no reference to IEC 62443 (industrial cybersecurity), no defense-in-depth strategy, no mention of IT/OT network segmentation.

**Recommendation**: Add a dedicated paragraph (in §4.4 or §6.2) addressing cybersecurity in the MAS architecture. At minimum: (a) reference IEC 62443 zone-conduit model for IT/OT segmentation; (b) state that L0 safety interlocks must be physically isolated from network-accessible layers (defense-in-depth); (c) acknowledge cybersecurity as a critical challenge in the development roadmap. For a paper proposing cloud-connected autonomous control of water infrastructure, ignoring cybersecurity is a significant omission.

### M5. Self-Citation Concentration and International Coverage

The reference list contains approximately 50 references. Self-citations (Lei et al.) include refs [2, 7, 8, 9, 10, 17, 18, 19, 20, 21] — approximately 11 references (~22%). While not extreme, the self-citations are heavily concentrated in the introduction (§1) and engineering practice (§5) sections, creating an impression that the work exists in isolation.

More significantly, the international canal automation community is underrepresented. The paper cites Litrico & Fromion [13], Clemmens & Schuurmans [26], van Overloop [27], and Negenborn et al. [16], but omits:
- Malaterre's seminal classification of canal control algorithms [ref 25 is Malaterre but only for classification]
- Horváth et al.'s work on operational control of irrigation canals
- The Dutch and Australian contributions to real-time canal control (e.g., ACMI, IIASA canal control workshops)
- The broader SCADA/telemetry community's work on water system automation

**Recommendation**: (a) Add 5-8 international references to dilute self-citation rate below 20%; (b) explicitly acknowledge the canal automation community in §2 or §4 as predecessors whose work on individual canal control forms the foundation that CHS extends to network-scale coordination.

### M6. "分层分布式群体智能" Terminology Concern

The paper uses "分层分布式群体智能" (hierarchical distributed swarm intelligence) as the endpoint vision. In computer science, "swarm intelligence" (群体智能) has a specific technical meaning — it refers to collective behavior of decentralized, self-organized systems (ant colony optimization, particle swarm optimization, etc.) where intelligence emerges from simple local rules without central coordination.

The MAS architecture described in §4.4 is actually the opposite: it has explicit hierarchical coordination (L0→L1→L2), centralized cloud agents, and top-down goal setting. This is much closer to "hierarchical multi-agent coordination" than "swarm intelligence." Using "群体智能" risks misleading readers with AI/CS backgrounds and inviting criticism that the authors misunderstand the term.

**Recommendation**: Replace "分层分布式群体智能" with a more accurate term such as "分层分布式多智能体协同" (hierarchical distributed multi-agent coordination) or "分层分布式自主协同" (hierarchical distributed autonomous coordination). Reserve "群体智能" only if the architecture truly exhibits emergent collective behavior without central coordination.

---

## Minor Issues

### m1. Communication Resilience for MAS Agents
§4.4 describes a rich inter-agent communication architecture but does not address communication failure. What happens when an Area Agent loses contact with its Edge Agents? When Cloud-to-Area communication is interrupted? A brief discussion of graceful degradation (e.g., "each agent maintains a local fallback policy that activates when communication is lost for more than T seconds") would strengthen practical credibility.

### m2. Operator Trust and Human Factors
The paper focuses entirely on algorithmic architecture but does not discuss how human operators would interact with the MAS system. Operator trust is a critical barrier to adoption: the "80/20 phenomenon" (§5.2) suggests operators spend 50% of effort on 10% of scenarios, but the paper does not discuss how operators would supervise autonomous operation during the 90% of routine scenarios. Consider adding a brief paragraph on human-machine interface requirements and operator training.

### m3. WSAL L3 Timeline Needs Concrete Milestones
Table 2 gives "目标: 2025-2030示范" for L3 but no specific milestones. Which engineering demonstration projects are planned? What constitutes "achieving L3"? Without concrete milestones, the roadmap remains aspirational rather than actionable.

### m4. South-to-North Middle Route Framing
§1 references the South-to-North Middle Route as an example of the "建得好、管不好" problem, which is appropriate background context. However, the current framing ("日常运行仍以人工经验为主, 调度响应时间长达数小时甚至数天") should include a citation for this operational characterization. Without attribution, it could be read as an unfounded criticism of an operating national project.

### m5. Eight Principles — Engineering Grounding
The four dual-principle tensions (§3.4) are well-illustrated with engineering examples, but the principles themselves (P1-P8) are presented as axiomatic without formal justification. For a 中国科学 disciplinary review, it would strengthen the paper to briefly connect each pair to established control theory concepts: P1-P2 to classical feedback/decoupling trade-off, P5-P6 to robust control theory (H∞/μ-synthesis), P7-P8 to supervisory control theory (Ramadge & Wonham).

### m6. Reference [37] Brown et al. (2020) Outdated
Brown et al. (2020) is cited for LLM/foundation model capabilities. This reference predates the major advances in LLM technology (GPT-3 was 2020, but GPT-4, Claude, and specialized scientific models came 2023-2025). A more recent survey of foundation models in scientific/engineering applications would better support the claims in §4.4.

### m7. WSAL Discriminant Thresholds Missing
Table 2 provides qualitative descriptions for each WSAL level but no quantitative discriminants. What metrics distinguish L2 from L3? (e.g., "ODD coverage > X% of annual operating hours"? "Constraint violation rate < Y per 1000 operating hours"?) Without quantitative thresholds, the WSAL classification cannot be operationally applied.

### m8. Equity and Accessibility of HydroOS
§6.4 positions HydroOS as an "open platform for the whole industry" and references Autoware (open-source autonomous driving). But the paper never states whether HydroOS will be open-source. If the vision is a proprietary platform controlled by one institution, the Autoware analogy is misleading. Clarify the intended licensing model.

---

## Reference Audit

- **Refs [7-10]** (Lei et al. 2025a-d): These four references from 南水北调与水利科技 are the authors' own recent publications establishing CHS. They appear to be published (2025, 23(4)) and are appropriately cited.
- **Ref [37]** (Brown et al. 2020): Outdated for current LLM state-of-the-art. Consider updating.
- **Ref [38]** (Lewis et al. 2020): Valid RAG reference.
- **"天河大模型"**: No reference provided. Requires citation or removal.
- **Missing**: IEC 62443 (cybersecurity), Horváth et al. (canal control), recent foundation model surveys (2023-2025).

---

## Summary

This paper presents an ambitious and largely well-structured disciplinary review of CHS for a Chinese audience. The theoretical framework (§3) is strong, and the Shaping case study demonstrates real engineering credibility. However, the cognitive intelligence section (§4.4) suffers from product-specific naming without evidence ("天河大模型"), uncritical LLM framing for safety-critical systems, and missing cybersecurity considerations. The Jiaodong case needs quantitative metrics to match Shaping's level of evidence. The terminology "群体智能" is technically inaccurate for the described architecture. Addressing these issues would transform the paper from a good overview into a definitive disciplinary reference for 中国科学.
