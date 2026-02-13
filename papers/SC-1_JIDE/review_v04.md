# Review Report — Paper SC-1 (J. Irrig. Drain. Eng. v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

This paper experimentally validates the CHS unified transfer function family on a three-pool canal flume, with a novel Muskingum–IDZ duality verification and DMPC demonstration. The v03 revision adds valuable digital water connections and benchmark protocol. From a control-theoretic perspective, two issues remain: the IDZ identification should account for inter-pool coupling during identification (not just during control), and the DMPC stability analysis is missing.

**Score: 8.0/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | Duality verification + multi-OP IDZ validation |
| Mathematical Rigor | 7 | Missing DMPC stability discussion |
| Reproducibility | 8.5 | Benchmark protocol well-defined |
| Case Validation | 8.5 | 25 scenarios, 15 OPs, cross-validation, backwater |
| Literature Completeness | 8 | Good after v02-v03 additions |
| Writing Quality | 8 | Well-structured |
| Technical Correctness | 7.5 | IDZ coupling during identification needs discussion |

---

## Major Issues

### M1. IDZ Identification: Inter-Pool Coupling

The IDZ parameters are identified independently for each pool using step-response analysis with one gate at a time. During identification of Pool 2, Gate G1 is held fixed but Pool 1 level changes (due to backwater from G2 step), meaning the "disturbance" input to Pool 2 is not truly constant. Please:
- Quantify the level change in Pool 1 during Pool 2 identification experiments
- Discuss whether this couples the identification (does Pool 1 level variation affect Pool 2 IDZ estimates?)
- If significant, discuss simultaneous multi-input identification as an alternative

### M2. DMPC Stability

The non-iterative sequential DMPC is demonstrated to work well empirically but lacks a stability analysis. For a journal paper:
- Under what conditions is the non-iterative sequential scheme guaranteed to be stable?
- The backwater coupling ratio (14%) is a useful practical metric, but is there a formal stability margin?
- At minimum, cite the relevant DMPC stability literature (e.g., Rawlings et al., 2017) and relate the flume results to known conditions.

---

## Minor Issues

### m1. Table 6 — Add Confidence Intervals

Table 6 shows Muskingum vs. IDZ parameter correspondence but does not include confidence intervals on the Muskingum estimates. The CI was discussed in the text (±4–7% for K, ±8–12% for X) but should appear in the table for direct comparison with IDZ CIs.

### m2. §7.5 — RLS for Online IDZ

The suggestion of recursive least squares for online IDZ updating is good but should note the persistence of excitation requirement: gate movements must provide sufficient excitation for the three IDZ parameters. During steady-state operation (no gate changes), RLS cannot update parameters.

---

## Summary

The paper is nearing publication quality. The two major issues (inter-pool coupling during identification and DMPC stability) require additional analysis paragraphs but no new experiments.
