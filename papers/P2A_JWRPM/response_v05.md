# Response to Review — Paper P2A Iteration 3

**Reviewer**: A (Control Theorist)
**Review Score**: 8/10 — Minor Revision

---

## Major Issues

### M1. "Mathematically Provable Constraint Satisfaction"
**Response**: Accepted. The claim was overstated. We will qualify it by explicitly noting that constraint satisfaction depends on model accuracy within the ODD and recursive feasibility. More importantly, we will add the stronger argument that the reviewer suggests: Layer 0 serves as a hard backup that catches any constraint violation arising from model mismatch or MPC infeasibility. This dual-layer guarantee (MPC optimization + L0 safety floor) is actually the paper's key safety argument and should be stated explicitly. Will add Mayne et al. (2000) reference.

### M2. Hierarchical Optimality and Consistency
**Response**: Accepted. We will add a paragraph in §3.1 (after Layer 3) acknowledging: (a) hierarchical decomposition introduces suboptimality relative to monolithic optimization — the standard scalability-optimality tradeoff; (b) time-scale separation ensures that steady-state Layer 3 references are dynamically achievable by Layer 1; (c) Layer 1 MPC handles temporary reference infeasibility through constraint softening, with discrepancies propagating upward through the DMPC update cycle. This is a well-understood tradeoff in hierarchical MPC and should be stated transparently.

### M3. Feasibility Definition in Propose-Validate Loop
**Response**: Accepted. We will add an explicit definition: HDC validates a CI proposal by solving the constrained optimization (Equations 2–4) with proposed parameters over a verification horizon. Acceptance requires a feasible solution satisfying all hard constraints. This is computationally tractable because it reuses the operational MPC solver.

---

## Minor Issues

### m1. Padé order: Will specify second-order Padé (standard for IDZ/ID models in canal control)
### m2. τ_coast wave celerity: Will clarify that Jiaodong uses kinematic wave speed (~1 m/s) as the relevant disturbance propagation speed for operational planning, while dynamic wave speed (~4-5 m/s) would give a shorter τ_coast
### m3. Equation (6): Will relabel as a protocol specification rather than equation
### m4. DMPC topology: Will clarify that Shaping uses cascade-serial topology (identical to Jiaodong) since the cascade stages are connected in series
### m5. Terminal cost: Will add a note explaining that Layer 0 backup provides robust constraint satisfaction without formal terminal conditions
