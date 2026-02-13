# Response to Review — Paper P2A Iteration 2

**Reviewer**: C (Cross-disciplinary Scholar)
**Review Score**: 7.5/10 — Minor Revision

---

## Major Issues

### M1. Digital Twin Relationship
**Response**: Accepted. This is an important positioning gap. We will add a paragraph in §8.1 explicitly distinguishing MAS-WSAL from digital twins: digital twins are descriptive/predictive mirrors; MAS is prescriptive/autonomous agents. The digital twin serves as the simulation substrate for xIL verification that certifies the ODD. Thus digital twins are necessary but insufficient for autonomous operation — a digital twin without MAS cannot act; MAS without a digital twin equivalent cannot be certified. Will add Pedersen et al. (2021) reference.

### M2. Human Factors in Automation Transitions
**Response**: Accepted. The aviation automation literature on automation complacency and skill degradation is directly relevant. We will add a paragraph in §7.2 or §8 covering: (a) mandatory periodic manual-mode exercises during WSAL-3 operation to prevent skill atrophy; (b) transparent system-status displays designed to maintain operator situational awareness; (c) the "automation surprise" risk and its implications for MRC response time assumptions. Will add Parasuraman & Riley (1997) reference.

### M3. Resilience and Compound Events
**Response**: Accepted. Reframing MAS-WSAL as a resilience enabler is a valuable improvement. We will add a paragraph in §8.1 noting: (a) ODD explicitly addresses degraded/failure scenarios; (b) island-autonomy mode provides communication-loss resilience; (c) Layer 0 ensures invariant protection during cascading failures; (d) the multi-layer architecture provides graceful degradation rather than binary fail/succeed. Will reference Hashimoto et al. (1982) for resilience metrics.

---

## Minor Issues

### m1. Abstract length: Will condense to ~200 words per JWRPM guidelines
### m2. Self-citation: Will add 5+ non-self references (Pedersen, Parasuraman, Hashimoto, McArthur, IMO/IEC cross-domain)
### m3. Broader autonomous infrastructure: Will add brief cross-infrastructure paragraph citing smart grid and autonomous shipping parallels
### m4. Table 2 WSAL-3 cybersecurity: Will add IEC 62443 compliance to admission criteria
### m5. Equation (7b): Will renumber to (8) and adjust subsequent numbering
### m6. MiL terminology: Will use "MiL-validated" in abstract and conclusions
