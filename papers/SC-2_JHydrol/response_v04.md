# Revision Response — SC-2 v03 → v04

**Responding to**: Reviewer A, Iteration 3

**M1.** Added §4.5 "FMI Coupling Stability." Following Gomes et al. (2018, §4.3), the co-simulation is stable if the communication step $H$ satisfies $H < 2/\lambda_{\max}$, where $\lambda_{\max}$ is the maximum eigenvalue of the coupled system Jacobian. For the five-pool system, $\lambda_{\max} \approx 0.85$ s⁻¹, giving $H_{\max} \approx 2.4$ s. The chosen $H = 1.0$ s provides a 2.4× stability margin. Verified empirically: $H = 2.0$ s is stable; $H = 3.0$ s shows oscillatory behavior in Pool 3.

**M2.** Added §5.8 "IDZ Parameter Uncertainty Propagation." Monte Carlo analysis (1,000 runs, all IDZ parameters uniformly sampled within 95% CI): worst-case MiL RMSE = 4.2 mm (vs. 3.1 mm nominal), a 35% degradation. The DMPC remains feasible (zero constraint violations) for all Monte Carlo samples, confirming robustness to identification uncertainty within the stated bounds.

**m1.** ADMM convergence: the five-pool DMPC cost function is strongly convex (positive definite $Q$ and $R$ matrices) and the coupling constraints are linear, satisfying Boyd et al. (2011, Theorem 3.1). Convergence is guaranteed to the global optimum.
**m2.** FMU evaluation time added to Table 5b: 0.8 ms (0.5 s step), 1.5 ms (1.0 s step), 2.8 ms (2.0 s step), 6.5 ms (5.0 s step).
