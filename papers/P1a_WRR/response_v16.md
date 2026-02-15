# Revision Response — P1a WRR v15 → v16

**Iteration**: 7
**Reviewer**: B (Engineering Practitioner)
**Verdict**: Accept (second consecutive accept)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Shadow-Mode Transition — Duration and Intervention Classification

**Response**: Accepted. Both refinements are operationally important.

**Action taken**: Revised shadow-mode specification in Section 7.5: "90 calendar days of continuous operation within the certified ODD, excluding scheduled maintenance downtime and planned system shutdowns. An 'intervention' counts only operator-initiated overrides where the operator disagrees with the automated action; operator-triggered mode switches at ODD boundaries (where the system correctly transitions to manual per design) are classified as 'boundary events' and tracked separately."

### M2. DMPC Computational Benchmark

**Response**: Accepted.

**Action taken**: Added note to Section 7.5: "For the 64-pool DMPC case (Section 6.2), the coordination protocol requires 3-5 sequential communication-computation cycles. With realistic SCADA polling latencies (50-200 ms per round-trip) and per-pool QP solve times (<100 ms), the total coordination overhead is approximately 0.5-1.5 seconds per sampling interval—well within the 300 s budget, leaving >99% of each interval for data acquisition, logging, and operator interface updates."

### M3. Cybersecurity — Architecture-Specific Attack Surface

**Response**: Accepted. The Area Agent coordination interface is indeed the most architecture-specific threat vector.

**Action taken**: Added to Section 7.5 cybersecurity paragraph: "The most architecture-specific cybersecurity risk is compromise of the Area Agent's coordination data exchange, which could inject false boundary conditions into neighboring pools' DMPC. Anomaly detection on exchanged boundary trajectories—flagging physically implausible discharge profiles or sudden departures from historical patterns—is recommended as a mitigation measure alongside the standard IEC 62443 network segmentation."

### M4. Prediction 2 — Transient Behavior Qualification

**Response**: Accepted. Transient performance matters to operators.

**Action taken**: Added to Prediction 2: "The settling time tolerance does not constrain transient behavior (overshoot, oscillation count); practical cross-sector deployment would require weight matrix tuning for acceptable transient performance, which is expected and does not invalidate the algorithmic transferability claim."

### M5. WSAL-3 Deployment Candidate

**Response**: Accepted. Identifying a concrete candidate adds practical gravity.

**Action taken**: Added to WSAL assessment paragraph: "The South-to-North Water Diversion Middle Route, with its 64 remotely controllable gates and extensive SCADA infrastructure, represents the most advanced candidate for the world's first WSAL-3 certification pilot."

---

## Response to Minor Issues

### m2. Open Research Timeline
**Action**: Added: "Code deposit will occur within 60 days of acceptance."

### m3. DMPC Convergence Fallback — Stale Solution Risk
**Action**: Added note: "If system state has changed significantly since the last convergence (e.g., due to a large disturbance during the coordination cycle), the stale solution may approach constraint boundaries. The Layer 0 safety floor provides the ultimate backstop: PLC interlocks enforce hard constraints independently of the DMPC solution quality."

### m4. Acknowledgments
**Action**: Noted. Grant numbers pending final confirmation.

---

## Version Summary

- **v15 → v16 changes**: Clarified shadow-mode measurement (M1); added DMPC computational budget (M2); specified Area Agent cybersecurity threat vector (M3); qualified Prediction 2 transient behavior (M4); added WSAL-3 pilot candidate (M5); added code deposit timeline (m2); added DMPC stale solution backstop (m3).
- **Consecutive accepts**: 2 (Reviewer A iter 6, Reviewer B iter 7). Need 1 more.
