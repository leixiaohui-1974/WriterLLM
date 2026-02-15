# Review — WHM-1 Iteration 3

**Reviewer**: A (Control Theorist)
**Draft reviewed**: v03
**Score**: 8.0 / 10
**Verdict**: Minor Revision

---

## Summary

The paper presents a well-structured MAS for Miyun Reservoir with appropriate control formulations. The climate stress testing and multi-reservoir extension are valuable additions. Two theoretical issues remain.

## Major Issues

### M1. Stability of multi-objective MPC under weight changes
The Reservoir Agent's multi-objective MPC (Eq. 6) uses fixed weights $(w_s, w_f, w_e, w_{\text{sp}}, w_{\text{wq}})$. However, §6.6 describes Bayesian weight updating based on operator overrides. What guarantees stability when weights change? Does switching between Pareto-optimal operating points (e.g., from Point B to Point A during drought) cause transient oscillations?

### M2. Inflow Agent forecast integration with MPC
The Inflow Agent provides probabilistic forecasts every 6 hours, but the Reservoir Agent operates on 1-hour cycles. How are forecast updates integrated mid-cycle? Is there a formal mechanism for the Reservoir Agent to handle forecast revisions (e.g., a major inflow revision at hour 3 of a 6-hour forecast window)?

## Minor Issues

### m1. Lumped Family α approximation validity
The reservoir is modeled as a pure integrator ($\tau_m = 0$, $\tau_d = 0$). For a 183.6 km² basin, wind-driven circulation can create non-uniform level distributions (±0.1 m). Under what conditions does the lumped approximation break down?

### m2. Gate coordination during flood discharge
When multiple gate groups operate simultaneously (flood scenario), how does the Outflow Agent prevent interference? The priority-based allocation may not be optimal during complex flood events.

## Reference Audit

All references verified. No issues found.
