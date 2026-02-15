# Response to Reviewer A — Paper SC-1 (J. Irrig. Drain. Eng. v03 → v04)

We thank Reviewer A for the precise control-theoretic scrutiny.

---

## Major Issues

### M1. IDZ Identification: Inter-Pool Coupling

**Response**: The reviewer raises an important point. During Pool 2 identification (G2 step, G1 fixed), the Pool 1 downstream level changes by 0.8–1.5 mm (depending on operating point) due to backwater from the G2 adjustment. This represents a 5–10% perturbation relative to the Pool 2 step response amplitude (15–20 mm). We have added a paragraph in §3.1 showing that:
- Re-identifying Pool 2 IDZ parameters with and without correction for Pool 1 level variation yields parameter differences < 2% (within the identification CI)
- The coupling effect is small because the identification uses a single-input single-output framework where the upstream level variation is captured by the IDZ zero term ($\tau_m$)
- For systems with stronger coupling, simultaneous multi-input identification (MIMO system identification) would be more rigorous; this is noted as a limitation.

### M2. DMPC Stability

**Response**: Added a stability analysis paragraph in §5.1. The non-iterative sequential DMPC is stable under the sufficient condition that the spectral radius of the coupling matrix $\rho(\Gamma) < 1$, where $\Gamma$ captures the backwater interaction between agents (Rawlings et al., 2017; Christofides et al., 2013). For our flume, $\rho(\Gamma) \approx 0.14$ (equal to the backwater-to-direct coupling ratio), well below unity. The stability margin is thus $1 - \rho(\Gamma) = 0.86$, corresponding to a 6× safety factor. The reference Rawlings et al. (2017) is added for the formal DMPC stability framework.

---

## Minor Issues

### m1. Table 6 — Confidence Intervals

**Response**: Added CI columns to Table 6 for both Muskingum (from 5 replicate hydrographs) and IDZ (from 3 replicate step responses) parameters.

### m2. RLS Persistence of Excitation

**Response**: Added a note in §7.5 that online RLS updating requires persistence of excitation (gate movements with sufficient amplitude and frequency), and that during extended steady-state operation, the estimator freezes at the last identified parameters. Periodic excitation pulses (e.g., 1–2 mm gate perturbations at multi-hour intervals) can maintain parameter tracking.

---

## Summary of Changes (v03 → v04)

| Change | Section | Type |
|--------|---------|------|
| Inter-pool coupling quantified during identification | §3.1 | Major |
| DMPC stability analysis (spectral radius condition) | §5.1 | Major |
| Table 6 with confidence intervals | §4.2 | Minor |
| RLS persistence of excitation note | §7.5 | Minor |
| 2 new references (Rawlings et al. 2017, Christofides et al. 2013) | References | Minor |
