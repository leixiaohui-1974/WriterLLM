# Response to Reviewer A — WHM-1 Iteration 3

## M1. Stability under weight changes

**Response**: Added §3.3 Remark 1: Weight updates occur on a weekly cycle (not within MPC iterations), and changes are bounded ($|\Delta w_i| \leq 0.05$ per update). The Reservoir Agent's MPC is warm-started from the previous solution; the terminal cost formulation (Rawlings et al., 2017) guarantees feasibility and stability for each fixed weight vector. Weight changes cause a smooth transition between Pareto-optimal points (the Pareto frontier is convex in the weight space), with transient deviations bounded by $\|H(k) - H^*(k)\| \leq \epsilon_w / \lambda_{\min}(Q_h)$ where $\epsilon_w$ is the weight perturbation magnitude. Empirically, weight changes produce < 0.1 m level perturbation, settling within 3–4 Reservoir Agent cycles (3–4 hours).

## M2. Forecast integration mid-cycle

**Response**: Added to §3.2: When the Inflow Agent issues an updated forecast (every 6 h), the Reservoir Agent receives it at the next 1-hour cycle and immediately re-optimizes with the new forecast as initial condition. For significant forecast revisions (defined as $|\hat{Q}_{50\%,\text{new}} - \hat{Q}_{50\%,\text{old}}| > 20\%$), an interrupt mechanism triggers immediate Reservoir Agent re-optimization regardless of cycle timing, with latency < 2 min. This is implemented as an event-triggered update within the otherwise time-triggered MPC loop.

## m1. Lumped approximation validity

**Response**: Added to §2.2: The lumped approximation is valid when wind-driven setup $\Delta H_{\text{wind}} \ll$ operational water level range. For Miyun, maximum wind setup (Beaufort 6, 12 m/s) across the 15 km fetch produces $\Delta H \approx 0.08$ m (Zuider-Zee formula), which is 0.25% of the 31.5 m operating range. The lumped approximation breaks down only for very shallow reservoirs or extreme wind events; for Miyun, the error is negligible relative to the 1-hour MPC resolution.

## m2. Gate coordination during floods

**Response**: Added to §3.4: During flood events requiring simultaneous multi-gate operation, the Outflow Agent switches from priority-based to coordinated optimization, solving a joint QP across all four gate groups. The flood QP minimizes peak downstream discharge subject to flood storage depletion targets, with cross-gate rate coordination to prevent surge interference. This coordinated mode is triggered when $\rho(\mathbf{x}) < 0.3$ (WARNING zone approaching flood constraint).
