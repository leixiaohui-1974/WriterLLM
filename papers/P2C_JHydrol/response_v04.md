# Response to Reviewer A — P2C Iteration 3

## M1. Stability analysis

**Response**: Added §3.6 "Stability Analysis" with formal treatment:

(a) **Station Agent MIQP**: During pump switching (discrete events), the MIQP introduces discontinuities. However, pump switching occurs at most once per 30-minute minimum run time (Eq. 5), making it a rare event relative to the 2 s sampling period. Between switching events, the Station Agent solves a continuous QP in speed ratios with guaranteed stability via terminal cost (Rawlings et al., 2017, Theorem 2.19). The switching events are analyzed as impulse disturbances that settle within 3–5 Station Agent steps (6–10 s), well within the Segment Agent's 60 s interval. This "switching-as-disturbance" treatment is valid because pump transitions are bounded in magnitude ($|\Delta Q| \leq Q_{\text{unit,max}}$) and duration.

(b) **Family α integrator stability**: The open-loop integrator $1/(A_s s)$ is indeed marginally unstable. Closed-loop stability of the Segment Agent MPC is guaranteed by: (i) the integral action inherent in the MPC reference tracking formulation (the controller drives water level error to zero), (ii) the check gate providing a second degree of freedom for disturbance rejection, and (iii) the terminal penalty $V_f(h) = h^T P h$ where $P$ satisfies the discrete-time algebraic Riccati equation for the linearized system (Maciejowski, 2002, §3.5). Formal proof follows Rawlings et al. (2017, §2.4) for tracking MPC with integrating plants.

## M2. Consensus convergence under transport delay

**Response**: Added analysis in §3.2: The Gauss-Seidel consensus operates on the Segment Agent's internal prediction model (Eq. 2), not on the physical system directly. The consensus algorithm converges within the prediction model at each Segment Agent step, ensuring consistent boundary conditions for the next 30-minute prediction window. The physical transport delay (24–45 min) is explicitly modeled within the Family α transfer function ($e^{-\tau_d s}$ term), so the MPC prediction accounts for the delay. The consensus convergence is therefore independent of the physical delay—it depends only on the model coupling strength $\kappa$ between adjacent segments, which satisfies $\kappa < 0.25$ for all Jiaodong segments (verified via eigenvalue analysis of the coupling matrix). Added reference: Negenborn et al. (2008) for distributed MPC consensus under delay.

## m1. Table 4 solver clarification

**Response**: Updated Table 4: Station Agent solver changed to "MIQP/QP (< 50 ms); MIQP only during pump switching (< 1/30 min)".

## m2. Notation consistency

**Response**: Updated to use $N_{p,i}$ and $N_{u,i}$ consistently throughout §3 and Table 4.
