# Review — P2C Iteration 3

**Reviewer**: A (Control Theorist)
**Draft reviewed**: v03
**Score**: 8.0 / 10
**Verdict**: Minor Revision

---

## Summary

The paper presents a well-formulated three-layer HDMPC with clear multi-timescale decomposition, appropriate use of the CHS Family α framework, and convincing SiL results. The RL positioning (§6.6) and demand sensitivity analysis (§6.7) are valuable additions. Two theoretical issues remain.

## Major Issues

### M1. Stability analysis incomplete
The paper invokes the singular perturbation argument (Christofides et al., 2002) for the 30:1 and 60:1 timescale ratios but does not formally verify the conditions. Specifically: (a) the Station Agent MPC uses MIQP (binary pump switching)—how does integer switching interact with the singular perturbation stability guarantee, which assumes continuous dynamics? (b) the integrating dynamics of Family α ($1/(A_s s)$) mean that the open-loop system is marginally unstable—what ensures closed-loop stability of each MPC layer independently?

### M2. Consensus convergence under transport delay
The Gauss-Seidel consensus protocol (Eq. 7) achieves $\epsilon \leq 0.02$ m within 3 communication rounds. However, the Family α transport delays (24–45 min) mean that the actual water level response to a Segment Agent action is delayed. How does transport delay affect consensus convergence? The Huang et al. (2026b) validation was for canal systems with shorter delays. Is the convergence guarantee preserved for 45-minute delays?

## Minor Issues

### m1. Table 4 solver column inconsistency
Table 4 lists "MIQP (< 50 ms)" for Station Agent but §3.1 states the MIQP applies only when pump switching occurs; during steady operation it reduces to continuous QP. The table should clarify this distinction.

### m2. Notation: $N_1, N_2, N_3$ vs. $N_u$
The prediction horizons use $N_1, N_2, N_3$ but the control horizons are not consistently named. Suggest using $N_{p,i}$ and $N_{u,i}$ for prediction and control horizons at layer $i$.

## Reference Audit

- Christofides et al. (2002): Confirmed CChE paper on two-time-scale control.
- Rawlings et al. (2017): Confirmed Nob Hill textbook.
- All other references verified.
