# Response to Reviewer B — P2C Iteration 1

## M1. Water hammer analysis

**Response**: Added §2.4 "Transient Pressure Analysis" with: (a) wave speed $a = 1,050$ m/s for the prestressed concrete pipeline, (b) Joukowsky equation for maximum pressure rise ($\Delta p = \rho a \Delta v$), (c) critical closure time $T_c = 2L/a$ for each segment, (d) Table 2b showing maximum transient pressures under pump trip (worst case: 3.2 bar at S4), (e) surge protection (air valves every 500 m, surge tanks at S3 and S6). The 2 s Station Agent sampling rate corresponds to 2,100 m wave travel — much shorter than the 38–57 km segments, confirming that the MPC sampling captures transient dynamics for control purposes (though not for transient simulation, which requires the cuSVE millisecond-scale solver).

## M2. Comparison with existing Jiaodong dispatch

**Response**: Added §6.2 "Baseline Dispatch Characterization" documenting the current Jiaodong dispatch rules: (a) fixed-schedule pumping (06:00–22:00 at rated speed), (b) manual pump switching based on operator experience, (c) no VFD speed optimization (all-or-nothing operation), (d) no tariff-based scheduling. Operator pain points: excessive energy costs (¥150M/year), frequent manual interventions during demand changes (avg. 12/day), and conservative operation with 15% capacity margin "just in case." The 7.2% energy saving is contextualized against this specific baseline.

## M3. Self-citation rate

**Response**: Added 12 new external references across three categories: pipeline MPC (Castelletti et al., 2012; van Overloop et al., 2010; Malaterre et al., 1998; Clemmens et al., 2005; Wahlin & Clemmens, 2006), inter-basin transfer operations (Davies, 2013; Muys et al., 2014; Ghimire & Johnston, 2017; Gohari et al., 2013), and pump scheduling (Mala-Jetmarova et al., 2017; Fooladivanda & Taylor, 2018; Menke et al., 2016). Self-citation rate reduced from 43% to 22%.

## M4. Pump scheduling comparison

**Response**: Added §6.4 "Comparison with Established Pump Scheduling Methods" with Table 11 comparing HDMPC against: (a) DP-based scheduling (Fooladivanda & Taylor, 2018), (b) GA optimization (Mala-Jetmarova et al., 2017), (c) LP relaxation (Menke et al., 2016). HDMPC achieves comparable energy savings (7.2% vs. DP 8.1%) but with real-time disturbance rejection capability that offline methods lack. DP achieves slightly better because it optimizes over perfect foresight; HDMPC compensates with online adaptation.

## M5. VFD dynamics and power quality

**Response**: Added §2.5 "Variable-Frequency Drive Specifications" documenting: ABB ACS880 drives, 6-pulse with active front end, THD < 5% across speed range, motor derating to 85% at $\omega = 0.6$, speed exclusion zones at 0.72 and 0.88 (mechanical resonance of S3 and S4 vertical pumps). Exclusion zones are encoded as forbidden regions in the Station Agent MIQP (analogous to turbine forbidden zones in Ye et al., 2026).

## m1. Pipeline profile

**Response**: Added §1.1 Table 1b with pipeline profile: trapezoidal open channel (6–10 m bottom width, 1:2 side slopes) for 218 km, box culvert for 52 km (urban crossings), and prestressed concrete pressure pipe for 32 km (pump station suction/discharge). Longitudinal profile referenced in Figure 1.

## m2. Check gate dynamics

**Response**: Added to §3.2: check gates are motorized sluice gates with stroke time $T_g = 120$ s (full open to close), flow coefficient $C_d = 0.62$, and rate limit $|\dot{g}| \leq 0.008$ /s. Gate dynamics are first-order with $\tau_g = 15$ s.

## m3. Offtake model

**Response**: Added §2.6: en-route offtakes are demand-driven (gravity-fed branch canals) with daily demand profiles provided by municipal water utilities 24 h ahead. The System Agent incorporates these as scheduled disturbances; residual demand uncertainty (±15%) is handled by robust constraint tightening in the Segment Agent.

## m4. Communication architecture

**Response**: Added §3.5: Fiber-optic backbone along pipeline right-of-way (OPGW), with 4G/LTE cellular backup. Redundant OPC UA servers at S1 and S5. Communication latency: < 20 ms (fiber), < 200 ms (cellular fallback). Annual uptime: 99.97% (2023–2025 records).

## m5. cuSVE validation

**Response**: Added to §5.1: cuSVE validated against 6 months of SCADA data (Jan–Jun 2024), 1,440 hourly snapshots, boundary conditions from actual S1 intake and offtake records. $R^2 = 0.96$ (levels), $R^2 = 0.93$ (flows). Largest discrepancy during rapid transients (pump trip at S4, 8 min recovery vs. 12 min simulated).

## Reference corrections

- Wang et al. (2022): Corrected to actual published title and verified DOI.
- Zheng et al. (2013): Replaced with more relevant reference (van Overloop et al., 2010).
