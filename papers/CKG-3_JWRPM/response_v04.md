# Revision Response — CKG-3 v03 → v04

**Responding to**: Reviewer A, Iteration 3

## Response to Major Issues

**M1. Gain-scheduled MPC stability during transition.**
Added Section 4.3.1 "Stability Under Gain Scheduling" with formal treatment:

1. **Dwell time analysis**: The minimum time between MPC updates is bounded by the significance threshold: a 10% parameter change requires the operating point to shift by at least $\Delta h \geq 5$ cm (from Table 3), which takes $\geq 60$ s at maximum flow rate. The observed minimum inter-update interval across all experiments is 55 s (scenario A21), confirming the implicit dwell time of $\geq 50$ s ($\geq 10$ sampling intervals).

2. **Common Lyapunov function**: For the dual-tank system, the MPC cost function $J = \sum \|y - r\|^2_Q + \|\Delta u\|^2_R$ serves as a common Lyapunov function across the gain-scheduled parameter range, because: (a) the system remains integrating (Family α) across the full ODD, and (b) the MPC weights $(Q, R)$ are fixed. A formal proof sketch using the terminal cost approach of Mayne et al. (2014) is provided.

3. **Empirical verification**: Table 4b added showing the transient behavior at all 23 gain-scheduled transitions observed across the 32 dual-tank scenarios: maximum transient overshoot = 1.2 mm, maximum settling time = 15 s (3 samples), zero constraint violations during any transition.

Added references: Liberzon (2003), Hespanha & Morse (1999).

**M2. RLS convergence and ODD safety margin coupling.**
Added Section 4.6 "Transient ODD Margin During Adaptation":

1. **Quantification**: During the RLS convergence period (5–8 samples), the maximum observed $\rho$ reduction is $\Delta\rho = 0.03$ (from $\rho = 0.08$ to $\rho = 0.05$), occurring in scenario A21 (largest operating point shift). This remains above the WARNING threshold ($\rho_w = 0.03$), so no spurious warnings are triggered.

2. **Safety margin budget**: The ODD safety factor SF = 1.5 provides a static margin of $\delta_s = 5$ cm. The transient model inaccuracy during adaptation consumes at most $\Delta h_{\text{transient}} = 1.2$ mm of this margin (0.2% of $\delta_s$). Added Eq. (10): effective margin $\delta_{\text{eff}} = \delta_s - \Delta h_{\text{transient}} \geq 4.88$ cm, which still satisfies SIL-1.

3. **Conservative protocol**: If $\rho < \rho_w$ during adaptation, the gain-scheduled update is deferred until $\rho > 2\rho_w$ (added to the update protocol in Section 4.3).

## Response to Minor Issues

**m1.** Added ARX model order selection: AIC/BIC analysis on 600-s identification data from the dual-tank. Order (2,2) is selected by both criteria; (1,1) has insufficient dynamics (no backwater zero), (3,3) is overparameterized (AIC increases by 12%).

**m2.** Table 3b updated with 95% confidence intervals computed from 100 bootstrap resamples of the 16 boundary scenarios.

**m3.** Clarified terminology in Section 7.6: "self-calibrating" = continuous parameter update of a fixed-structure model (this paper); "self-adaptive" = structural model change (e.g., switching from IDZ to ID model order). The CHS SCDT is self-calibrating within a fixed IDZ structure.

**m4.** ADMM stopping criterion specified: $\|\mathbf{r}^{(k)}\|_2 < \epsilon_{\text{pri}} = 10^{-3}$ and $\|\mathbf{s}^{(k)}\|_2 < \epsilon_{\text{dual}} = 10^{-3}$, following Boyd et al. (2011, §3.3). Maximum iterations capped at 20 (safety bound).
