# Revision Response — CKG-3 v02 → v03

**Responding to**: Reviewer C, Iteration 2

## Response to Major Issues

**M1. Digital twin and Industry 4.0 connection.**
Added Section 7.6 "Self-Calibrating Digital Twin for Water Networks" framing the adaptive MAS as a self-calibrating digital twin (SCDT). The RLS estimator continuously updates the IDZ model to match the physical plant, making the MPC's internal model a live digital replica. Connected to Rasheed et al. (2020) and Grieves & Vickers (2017). Distinguished from static digital twins (fixed model) and data-driven twins (black-box ML): the CHS SCDT maintains an interpretable physics-based model (IDZ) that is continuously calibrated, preserving certifiability.

**M2. Scalability extrapolation.**
Added Table 11 with computational scaling estimates for 50, 100, and 500 pools based on observed trends. Edge Agent computation scales linearly (0.5 ms/pool); DMPC coordination scales as O(N²) with ADMM (0.1 ms × N² for coupling). Crossover to GPU requirement estimated at ~80 pools (total MAS time exceeding 1 s). For 500 pools, GPU-parallel ADMM (Huang et al., 2026) reduces coordination to ~50 ms. Added discussion of hierarchical decomposition (5 Area Agents × 100 Edge Agents) as an alternative.

**M3. Comparison with alternative adaptive approaches.**
Added Table 12 comparing four adaptive approaches: (1) RLS + gain-scheduled MPC (this paper), (2) Multiple-Model Adaptive Control (MMAC), (3) L1 adaptive control, (4) Gaussian Process MPC. Comparison dimensions: computational cost, interpretability, convergence speed, safety certifiability, implementation on IEC 61131-3 PLC. RLS + gain-scheduled MPC selected for: lowest computational cost (5.1 ms), highest interpretability (explicit IDZ parameters), and PLC implementability (no matrix inversion beyond 4×4). MMAC requires pre-computed model bank (storage-limited on PLC); L1 lacks explicit model for ODD certification; GP-MPC is too computationally expensive for PLC (estimated 200+ ms).

## Response to Minor Issues

**m1.** Abstract tightened to 195 words. Removed Bayesian ODD expansion detail, focused on PLC HiL + adaptive MAS contributions.

**m2.** Added formal CI definition in Section 4.4: "Cognitive Intelligence (CI) encompasses the agent's ability to monitor its own model accuracy through parameter tracking, adapt to changing conditions through gain-scheduled control, and expand its verified operating envelope through evidence-based ODD refinement."

**m3.** Added analytical explanation after Figure 5 caption: error propagation through N coupled pools scales as O(√N) for uncorrelated mismatch and O(N) for systematic mismatch, explaining the increasing adaptive advantage.

**m4.** Justified 8-scenario exploratory phase: the exploratory campaign tests only the expanded region (SF_new boundary), which is a strict subset of the full ODD boundary. The 8 scenarios cover the 4 expanded boundary segments × 2 flow conditions. The full 16-scenario confirmation campaign then validates the complete expanded ODD.

## Self-Citation Rate Reduction

Reduced self-citations from 10/25 (40%) to 8/33 (24%) by:
- Adding 8 new third-party references (Grieves & Vickers 2017, Boyd et al. 2011, Bemporad et al. 2002, Mayne et al. 2014, Schuurmans et al. 1999, Negenborn et al. 2009, Horváth et al. 2015, Tao et al. 2019)
- Removing Ye et al. (2026) — now referenced only in the citation network, not in the reference list
- Self-citation rate now 24%, within the 25% threshold
