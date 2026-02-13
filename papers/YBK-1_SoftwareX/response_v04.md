# Point-by-Point Response — YBK-1 Iteration 3

**Reviewer**: A (Control Theorist)
**Draft**: v03 → v04

---

## Major Issues

### M1. QP Solver Convergence

**Response**: Added paragraph in §2.2:
- Convergence criterion: primal infeasibility < 1e-6 or 20 iterations reached
- Failure handling: if not converged after 20 iterations, return last feasible iterate (warm-started from previous step). If no feasible iterate exists (constraint conflict), apply safe fallback (hold last command, trigger ODD WARNING)
- In practice: across all 87 unit tests and 3-pool flume validation, convergence achieved in mean 4.2 iterations (max 12). 20-iteration cap never reached

### M2. State Estimation Robustness

**Response**: Added paragraph in §2.2:
- Steady-state Kalman filter valid when operating near linearization point (IDZ model assumption: ±20% of nominal flow)
- For large excursions: HydroRTP includes an optional EKF block (Layer 2 assembly option) that re-linearizes at each step
- Guidance: use steady-state KF for normal operation within ODD; switch to EKF for ODD boundary scenarios or commissioning with unknown initial conditions
- EKF adds ~40% computational overhead (WCET 5.9 ms vs. 4.2 ms for 3-pool)

---

## Minor Issues

### m1. Code Generation Determinism

**Response**: Added note in §2.5: Code generation output is deterministic for identical Simulink model, Embedded Coder version, and code generation settings. Cross-version differences (R2023b vs R2024b) may produce functionally equivalent but textually different ST due to internal optimization changes. The built-in verification test catches any behavioral differences.
