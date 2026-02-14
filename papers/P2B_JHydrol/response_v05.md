# Response to Reviewer B — P2B Iteration 4

## m1. Operator training

**Response**: Added a paragraph in §6.1: Preliminary operator trials (2 weeks, 4 operators) at Shaoping revealed that: (a) operators adapted to the HDMPC recommendation interface within 2 days, (b) operator override rate decreased from 45% (day 1) to 8% (day 14), and (c) operators valued the ODD distance indicator $\rho(\mathbf{x})$ as a "situational awareness" tool. A formal training program (2-day classroom + 1-week supervised operation) is planned for the WSAL-2 deployment.

## m2. Maintenance scheduling

**Response**: Added to §6.1 future work (item 5): Proactive maintenance scheduling can be integrated into the Area Agent's 24-hour look-ahead by encoding planned outages as time-varying constraints. This converts the MIQP to a time-varying formulation with known binary schedules, actually simplifying the optimization (no branch-and-bound needed for scheduled outages). Implementation is planned for the WSAL-3 transition phase.
