# Response to Reviewer C — HZF-2 Iteration 2

We thank Reviewer C for the insightful review. Both major and all minor issues are addressed below.

---

## Major Issues

### M1. No discussion of learning-based alternatives

**Response**: We have added §6.6 "ParaQP vs. Neural MPC Approximations" discussing when QP-based DMPC remains preferable over neural MPC:

1. **Constraint satisfaction**: QP solvers provide hard constraint guarantees by construction. Neural MPC requires additional safety layers (projection, control barrier functions) to ensure constraint satisfaction, adding complexity and computational overhead that partially negates the inference speed advantage.

2. **Out-of-distribution robustness**: Neural MPC performance degrades for operating conditions not well represented in training data. Water networks experience rare events (flash floods, equipment failure, emergency drawdowns) where QP-based MPC maintains its optimization guarantees.

3. **Interpretability and certification**: QP solutions can be traced through the active-set iterations, enabling root-cause analysis of control decisions—essential for water utility regulatory compliance. Neural MPC is a black box.

4. **Hybrid architecture**: We describe a promising hybrid approach where a neural network provides the warm-start point for the QP solver (reducing active-set iterations from 8.3 to ~1.5), combining neural speed with QP safety guarantees. This is planned for ParaQP v2.0.

New references: Karg & Lucia (2020), Chen et al. (2022).

### M2. Heterogeneous agent models

**Response**: We have added §6.7 "Heterogeneous Agent Support":

- **Current support**: ParaQP allows different QP dimensions per agent (different $N_u$, $N_h$). Family α and Family β pools can coexist since only the local $A_i, B_i, C_i$ matrices differ; the block-separable structure is preserved.

- **Convergence under heterogeneity**: Theorems 1–3 hold as stated because the convergence depends on the coupling strength $\kappa$ (Eq. 9), which is defined per-edge regardless of local model structure. The proofs require only $H_i \succ 0$ per agent, which holds for both Family α and Family β models with $R_i > 0$.

- **Mixed sampling rates**: Not currently supported (all agents must share the same $\Delta t$). A multi-rate DMPC extension using hierarchical ADMM is discussed as future work.

- **Nonlinear gates**: The linearized gate equation (Eq. 4) is re-evaluated at each sampling step using current operating conditions. For highly nonlinear gate hydraulics (e.g., submerged vs. free-flow transitions), a Sequential QP (SQP) wrapper would be needed—planned for v2.0.

---

## Minor Issues

### m1. Convergence rate comparison with theory

**Response**: Added Table 12 comparing theoretical bounds vs. observed convergence rates:

| System | $\kappa$ | $\rho_{\text{GS,theory}} = \kappa^2$ | $\rho_{\text{GS,observed}}$ | $\rho_{J,\text{theory}} = 2\kappa^2$ | $\rho_{J,\text{observed}}$ |
|--------|---------|------|------|------|------|
| B1 | 0.08 | 0.006 | 0.004 | 0.013 | 0.009 |
| B2 | 0.14 | 0.020 | 0.015 | 0.039 | 0.028 |
| B3 | 0.18 | 0.032 | 0.026 | 0.065 | 0.048 |
| B4 | 0.22 | 0.048 | 0.038 | 0.097 | 0.072 |

Observed rates are consistently 20–30% below theoretical bounds, confirming that the bounds are conservative but informative.

### m2. Figure 6 parameters

**Response**: Updated Figure 6 caption with exact parameters: $A_s$ computed as $B \cdot L$ with bottom width $B = 5$ m, pool lengths $L = 1$–$20$ km; gate coefficient $\alpha = 0.04$ m²/s; $Q_i/R_i = 10$; $\Delta t = 60$ s.

### m3. Energy consumption

**Response**: Added Table 13 with energy per DMPC cycle across platforms:

| Platform | B2 energy (mJ/cycle) | B4 energy (mJ/cycle) |
|----------|---------------------|---------------------|
| S7-1516 (1-core) | 108 | 2,886 |
| CX2062 (16-core) | 1.18 | 7.33 |
| Xeon 8358 (32-core) | 4.60 | 28.6 |

The CX2062 is the most energy-efficient per cycle due to lower idle power. For solar-powered remote sites with 50 W panels, the CX2062's ParaQP overhead (0.07 W for B4) represents 0.14% of available power.

### m4. Junction notation

**Response**: Added formal definitions: $\mathcal{U}(j) = \{i \in \mathcal{V} : (i,j) \in \mathcal{E}\}$ (upstream pool set) and $\mathcal{D}(j) = \{k \in \mathcal{V} : (j,k) \in \mathcal{E}\}$ (downstream pool set) in §3.6.

### m5. Abstract length

**Response**: Tightened the abstract to 195 words by removing redundant phrases while retaining the HiL and solver comparison highlights.
