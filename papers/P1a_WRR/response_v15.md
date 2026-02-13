# Revision Response — P1a WRR v14 → v15

**Iteration**: 6
**Reviewer**: A (Control Theorist)
**Verdict**: Accept (first consecutive accept)
**Date**: 2026-02-13

---

## Response to Major Issues

### M1. Theorem 2 Open Problem — Model Reduction Connection

**Response**: Accepted. Connecting to classical model reduction theory sharpens the research direction.

**Action taken**: Expanded Remark 1 with: "In the language of classical model reduction theory, the open problem is: under what minimal axioms on the linearized Saint-Venant partial differential equations does the three-parameter family {Aₛ, τᵈ, τₘ} emerge as the unique low-order SISO LTI approximation in the sense of balanced truncation (Antoulas, 2005) or moment matching (Gugercin et al., 2008)? Establishing this connection would elevate Theorem 2 from a verified classification to a derived necessity."

Added Antoulas (2005) to the reference list.

### M2. Propose-Validate Tuple — Dimensional Consistency

**Response**: Accepted. The MPC parameterization should be more precise.

**Action taken**: Revised the tuple specification: "Formally, the candidate tuple C = {(Q_new, R_new, x_ref) ∈ ℝⁿˣⁿ × ℝᵖˣᵖ × ℝⁿ, (x_min, x_max, u_min, u_max) ∈ ℝⁿ × ℝⁿ × ℝᵖ × ℝᵖ, ODD_status ∈ {within, approaching, outside}} encodes the proposed cost function parameterization (state weight, input weight, reference trajectory), the modified constraint bounds, and ODD proximity assessment."

### M3. Scaling Law — Qualifying Condition

**Response**: Accepted. The scaling argument needs an explicit condition.

**Action taken**: Added qualifying sentence in Section 5.3: "The scaling Aₛ·Δyₘₐₓ/ΔQ ~ τᵈ holds for pools where the backwater length is comparable to the pool length—a condition satisfied by most operational canal pools designed for gravity-fed delivery, where the pool geometry is sized to the design flow and the transport delay is determined by the same pool length and wave celerity."

### M4. DMPC Convergence Assumption

**Response**: Accepted. The convergence conditions should be stated explicitly.

**Action taken**: Added to Section 6.2: "The convergence of the iterative DMPC protocol depends on the coupling strength between adjacent pools. For pools where the decoupling time horizon Tₛᵤᶠ = Aₛ·Δyₘₐₓ/ΔQ exceeds the coordination update interval T_comm—equivalently, where the buffer fraction f_b is sufficiently large—the inter-pool coupling is weak enough for convergence within 3-5 iterations. This connects directly to the P2-P6 tradeoff: stronger decoupling (larger f_b) not only improves local disturbance rejection but also improves DMPC convergence reliability. When coupling is too strong for convergence within the allocated iterations, the protocol defaults to the last converged solution—a safe fallback that may sacrifice optimality but maintains constraint satisfaction."

### M5. Differentiable IDZ — Identifiability Caveat

**Response**: Accepted. Parameter identifiability is a genuine concern.

**Action taken**: Added note to Section 8.4 differentiable modeling paragraph: "Parameter identifiability of the three-parameter family {Aₛ, τᵈ, τₘ} from operational data requires sufficiently rich excitation signals; correlation between τₘ and τᵈ under low-frequency disturbances may necessitate constrained identification procedures, as demonstrated by Horváth et al. (2024) for the IDZ model."

---

## Response to Minor Issues

### m1. Equation Numbering
**Action**: Noted for final manuscript preparation. All equations will be converted from embedded images to LaTeX with sequential numbering in the submission-ready version. This is a formatting task independent of content revisions.

### m2. Remark 1 Forward Reference
**Action**: Added forward reference in the Theorem 2 statement: "(proved by enumeration; see Remark 1 for discussion of proof methodology)."

### m3. Table 3 Quantitative Metric Column
**Action**: Added a "Quantitative Metric" column to Table 3. Only P2-P6 is populated: "f_b* ≈ min(1, τᵈ/T_comm)". Other rows show "—" with a table footnote: "Quantitative metrics for remaining tradeoffs are identified as open problems."

### m4. van Overloop et al. (2010) Full Reference
**Action**: Verified and added full reference: van Overloop, P.J., Clemmens, A.J., Strand, R.J., Wagemaker, R.M., & Bautista, E. (2010). Real-time implementation of model predictive control on Maricopa-Stanfield Irrigation and Drainage District's WM Canal. ASCE Journal of Irrigation and Drainage Engineering, 136(11), 747-756.

### m5. W Notation Collision Check
**Action**: Verified. The Kalman filter process noise covariance is not explicitly parameterized anywhere in the paper (Table 3 mentions "Kalman filtering" as a mathematical tool but does not use the covariance symbol). The W notation for LQR state weight is unambiguous within the paper's scope.

---

## Version Summary

- **v14 → v15 changes**: Connected Theorem 2 open problem to classical model reduction theory (Antoulas, 2005) (M1); revised propose-validate tuple with standard MPC parameterization (Q_new, R_new, x_ref, bounds) (M2); added scaling law qualifying condition for backwater-length comparability (M3); added DMPC convergence conditions and P2-P6 tradeoff connection (M4); added IDZ parameter identifiability caveat (M5); added Theorem 2 forward reference to Remark 1 (m2); added quantitative metric column to Table 3 (m3).
- **Self-citation rate**: Unchanged at ~16%.
- **Consecutive accepts**: 1 (Reviewer A, iteration 6).
