# Point-by-Point Response — HZF-1 Iteration 3

**Reviewer**: A (Control Theorist)
**Draft**: v03 → v04

---

### M1. Predictor-Corrector Convergence Analysis

**Response**: Added §3.3.1 "Convergence Analysis" with:
- The boundary iteration matrix $\mathbf{M}$ has spectral radius $\rho(\mathbf{M}) = \Delta t / \tau_d^{\min}$ where $\tau_d^{\min}$ is the shortest pool delay.
- For typical canal pools ($\tau_d > 60$ s, $\Delta t = 10$ s): $\rho < 0.17$, converging in 1 iteration.
- For short pools ($\tau_d = 10$ s, $\Delta t = 10$ s): $\rho \approx 1.0$, requiring 2 iterations.
- Convergence guaranteed when $\rho < 1$, i.e., $\Delta t < \tau_d^{\min}$.
- Table 3b shows $\rho$ values and iteration counts for the four benchmark systems.

### M2. Temporal Order Verification

**Response**: Added §5.7 "Temporal Convergence Test" with method of manufactured solutions:
- Sinusoidal manufactured solution, $\Delta t$ halved from 10 s to 0.31 s.
- Global error scales as $O(\Delta t^2)$ for both the monolithic and domain-decomposed schemes, confirming second-order temporal accuracy is preserved.
- Table 10: $L_2$ error vs. $\Delta t$ with computed convergence rate (1.97 ± 0.03 for all pool counts).
