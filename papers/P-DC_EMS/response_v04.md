# Response to Reviewer A — Paper P-DC (EMS v03 → v04)

We thank Reviewer A for the rigorous control-theoretic scrutiny. The three major issues—Gramian evaluation specification, five-level hierarchy mapping, and IDZ identification methodology—all sharpen the mathematical precision of the paper. All are addressed below.

---

## Major Issues

### M1. DfO Metric Specification: Gramian Evaluation over ODD

**Response**: We have revised the P1 and P2 formulations in §2.2 to specify:
- **Evaluation method**: Worst-case over ODD vertices (corners of the discrete ODD grid), as recommended. Specifically: $\sigma_{min}(W_c) = \min_{p \in \mathcal{V}(ODD)} \sigma_{min}(W_c(p))$ where $\mathcal{V}(ODD)$ denotes the vertex set of the Cartesian product ODD.
- **Threshold selection**: $\gamma_c$ is defined relative to the control objective: $\gamma_c = Q_{max}^2 / (N \cdot \Delta t)$ where $Q_{max}$ is the maximum required flow change and $N \cdot \Delta t$ is the prediction horizon, representing the minimum energy needed to achieve the design control authority within the MPC horizon.
- **Balanced realization**: For P2, the observability Gramian is computed from the balanced realization to ensure scale-independent conditioning. This is now stated explicitly.

### M2. MBD Layers and the CHS Five-Level Model Hierarchy

**Response**: Excellent observation. We have added a paragraph in §3.1 with a mapping table:

| MBD Layer | CHS Model Level (P1a §4.6) | Content |
|-----------|---------------------------|---------|
| Layer 7 | LSV (Saint-Venant) | Full PDE; reference-fidelity simulation |
| Layer 6 (full) | IDZ (Integrator-Delay-Zero) | Primary control model for MPC |
| Layer 6 (simplified) | ID / I | Reduced models for preliminary design or real-time |
| Layer 6 (static) | SS (Steady-State) | Capacity planning; not for dynamic control |

The Layer 7→6 transition is now explicitly identified as the LSV→IDZ reduction pathway described in Lei (2025a, §4.7), with Theorem 3 (Model-Layer Correspondence) cited for the formal basis of this reduction.

### M3. Reference Workflow: IDZ Identification Methodology

**Response**: We have added a paragraph in §6.3 specifying:
- **Fitting method**: Nonlinear least-squares (Levenberg-Marquardt) minimizing the time-domain RMSE between the IDZ step response and the Saint-Venant step response over a 3-hour simulation window.
- **Identification criterion**: Minimize $J = \sum_{k=1}^{N} (h_{SV}(k\Delta t) - h_{IDZ}(k\Delta t))^2$ where $h_{SV}$ is the Saint-Venant water level response and $h_{IDZ}$ is the IDZ model response.
- **Confidence**: The 95% confidence intervals on identified parameters are ±3% for $A_s$, ±5% for $\tau_d$, and ±8% for $\tau_m$ (wider for $\tau_m$ because the non-minimum-phase zero is harder to identify from step data).
- **Sensitivity**: A ±10% perturbation in $A_s$ increases the worst-case RMSE from 0.042 m to 0.048 m—still below the 0.05 m threshold, confirming robustness.
- Litrico & Fromion (2009, Ch. 3) is cited for the IDZ identification methodology.

---

## Minor Issues

### m1. Preissmann Parameter

**Response**: Added: "Preissmann implicit scheme with θ = 0.6 and Δx = 100 m." The choice θ = 0.6 follows standard practice for canal applications (Litrico & Fromion, 2009) and provides adequate numerical diffusion control.

### m2. ODD Coverage Ratio: Measure Specification

**Response**: Revised to define $R_{ODD}$ as the fraction of a discrete test grid: $R_{ODD} = N_{pass} / N_{grid}$ where $N_{grid}$ is the number of grid points in the discretized ODD and $N_{pass}$ is the number passing all acceptance criteria. This avoids the dimensional inconsistency of the continuous measure and is consistent with the 12-scenario MiL test approach in §6.

### m3. MPC Prediction Horizon Rationale

**Response**: Revised to acknowledge the rule-of-thumb nature and cite the formal basis: "The prediction horizon N·Δt = 1,200 s exceeds twice the longest delay (τ_d ≈ 440 s), satisfying the delay-compensation condition for integrating systems (Litrico & Fromion, 2009, Ch. 5; van Overloop, 2006). For Family α systems, the open-loop settling time is theoretically infinite; the practical criterion is that N·Δt must allow the MPC to observe the full delayed effect of its first control action, validated here by the MiL results showing convergence within 3 DMPC iterations."

### m4. Data-Driven Safety Guarantees

**Response**: Revised the statement to: "data-driven controllers can be admitted within well-characterized ODD boundaries where their performance has been statistically validated through extensive xIL testing—providing probabilistic confidence rather than the formal guarantees (feasibility ⇒ constraint satisfaction) that model-based MPC offers. This testing-based certification is analogous to software verification: necessary for deployment confidence but not a substitute for formal safety analysis. For safety-critical water systems, the recommended architecture pairs a data-driven performance layer with a model-based safety fallback."

---

## Summary of Changes (v03 → v04)

| Change | Section | Type |
|--------|---------|------|
| Gramian worst-case evaluation + threshold definition | §2.2 (P1, P2) | Major |
| Five-level hierarchy ↔ MBD layer mapping table | §3.1 | Major |
| IDZ identification method, confidence intervals, sensitivity | §6.3 | Major |
| Preissmann θ = 0.6 | §6.2 | Minor |
| ODD ratio as discrete grid fraction | §2.2 (P3) | Minor |
| MPC horizon formal citation | §6.3 / Table 5 | Minor |
| Data-driven safety qualification | §7.5 | Minor |
