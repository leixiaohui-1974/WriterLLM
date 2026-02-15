# Response to Reviewer A — P2B Iteration 3

## M1. MIQP timing analysis

**Response**: Added Table 9 reporting Area Agent MIQP timing across all 16 scenarios:

| Scenario group | Mean solve time (s) | Max solve time (s) | Forbidden zone active? |
|---------------|--------------------|--------------------|----------------------|
| S1–S5 (nominal) | 0.3 | 0.5 | No |
| S6–S8 (operational) | 0.6 | 1.2 | S6: Yes (Luodixi offline) |
| S9–S12 (boundary) | 0.8 | 1.8 | S11: Yes (max dispatch) |
| S13–S16 (extreme) | 1.1 | 2.4 | S16: Yes (flood+max) |

Worst-case: 2.4 s (S16), well within the 5-min (300 s) sampling interval. The MIQP complexity is limited because only Pubugou has an active forbidden zone (one binary variable per time step in the prediction horizon), while the three Kaplan stations avoid their narrow rough zones through blade-gate coordination.

## M2. Dual-timescale stability

**Response**: Added §3.4 "Stability of Dual-Timescale HDMPC" citing the singular perturbation approach (Christofides et al., 2002): when the timescale ratio is sufficiently large (here 10:1, with the Edge Agent settling in ~3 samples = 90 s, well within the 300 s Area Agent interval), the fast subsystem reaches quasi-steady-state before the slow subsystem updates. The Edge Agent MPC stability is guaranteed by the terminal constraint (zero terminal cost, following Rawlings et al., 2017, §2.4), and the Area Agent stability follows from the cascade's inherent self-regulation (Family β open-loop stability). New reference: Christofides et al. (2002).

## m1. ARI formal definition

**Response**: Added: ARI = (number of Simulink blocks reused without modification) / (total blocks in target deployment). A "block" is defined as a Simulink subsystem at the HydroRTP library level (§4 of Yin et al., 2026): plant model, actuator, controller, sensor, communication, and infrastructure blocks.
