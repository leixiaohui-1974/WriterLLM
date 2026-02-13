# Point-by-Point Response — CKG-2 Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft**: v01 → v02

---

## Major Issues

### M1. Industrial Safety Standards Comparison

**Response**: Accepted. Added §3.5 "Alignment with IEC 61511 and SIL Classification":
- ODD monitor maps to SIF (Safety Instrumented Function) in IEC 61511 terminology
- Layer 0 interlock targets SIL-1 (PFD 0.01–0.1): hardware watchdog + redundant sensor voting
- ODD monitor (software) targets SIL-0 (advisory): not safety-rated, provides early warning
- Table 1b maps ODD framework components to IEC 61511 lifecycle phases (1-5)
- Noted that full SIL-2 certification requires hardware redundancy beyond current prototype

### M2. False Alarm Analysis

**Response**: Accepted. Added §5.6 "False Alarm Analysis":
- Ran 100 Monte Carlo repetitions of S11 (worst-case nominal scenario) with varying sensor noise realizations
- WARNING false alarm rate: 3.2% of sampling intervals (16 out of 500 intervals per run)
- VIOLATION false alarm rate: 0.0% (zero false VIOLATION triggers across 100 runs)
- Root cause of false WARNINGs: sensor noise spikes pushing estimated ρ below threshold momentarily
- Mitigation: median filter (already in place) + hysteresis band on WARNING threshold (added, reduces false WARNING to 0.8%)
- Table 7: False alarm rate vs. noise level and hysteresis band width

### M3. Scaling to 10-Pool Canal System

**Response**: Accepted. Added §5.7 "Scaling Demonstration: 10-Pool Canal SiL":
- Used the 10-pool Jiaodong canal model from Huang et al. (2026) as the plant
- ODD has 42 continuous dimensions (20 water levels + 10 valve openings + 10 valve rates + 2 environmental)
- 84 linear constraints → polytope evaluation in 0.12 ms (negligible vs. 5-s sampling)
- Ran 20 boundary scenarios: 100% detection (20/20), mean latency 1.6 ± 0.5 intervals
- Table 8: 10-pool ODD monitor results
- Confirms polytope formalization scales to realistic canal systems

### M4. ODD Monitor Computational Cost

**Response**: Accepted. Added computational cost quantification to §4.1:
- Dual-tank (14 constraints): 0.008 ms on PC, 0.15 ms on Arduino
- 10-pool (84 constraints): 0.12 ms on PC, estimated 2.3 ms on PLC
- 50-pool (420 constraints): estimated 0.6 ms on PC, 12 ms on PLC
- All well within sampling interval (5 s); even 500-pool (4200 constraints) would be <1 s on PC
- Added Table 1c: ODD monitor execution time vs. system size

### M5. Safety Margin Sensitivity Analysis

**Response**: Accepted. Added §5.8 "Safety Margin Sensitivity":
- Swept safety factor from 1.0 to 2.5 in steps of 0.25
- Table 9: safety factor vs. ODD violation rate (boundary scenarios) vs. operational range reduction
- At SF=1.0: 3/16 violations reach physical limits (unsafe)
- At SF=1.25: 0/16 violations reach physical limits, range [8.75, 41.25] cm (19% reduction)
- At SF=1.5 (selected): 0/16, range [10, 40] cm (25% reduction), margin to physical limit ≥4.2 cm
- At SF=2.0: 0/16, range [12, 38] cm (35% reduction)
- Recommended minimum SF=1.25 for laboratory; SF≥1.5 for field deployment

---

## Minor Issues

### m1. Notation Table

**Response**: Expanded notation table with all missing symbols: $\Delta t$, $A_d$, $B_d$, $C_d$, $Q_k$, $R_k$, $K$ (Kalman gain), $c$ (communication status).

### m2. Multi-Agent ODD Composition

**Response**: Added §6.6 "Multi-Agent ODD Composition" discussing how individual agent ODDs compose:
- System ODD ⊆ ∩ individual agent ODDs (intersection for coupled constraints)
- Additional coupling constraints (flow conservation at junctions, coordination requirements)
- Detailed treatment deferred to CKG-3 (multi-agent HiL)

### m3. Recovery Protocol Timing

**Response**: Added adaptive recovery to §3.4: recovery window scales with violation duration (min 3 intervals for transient violations < 2 intervals, 5 intervals for sustained violations, 10 intervals for communication loss). This reduces unnecessary delay for sensor-spike-triggered violations.

### m4. Reference Formatting

**Response**: Fixed all reference issues:
- Althoff et al.: corrected to Althoff (2021) monograph "Formal Methods for Automated Driving"
- Removed Macenski et al. (not ODD-related)
- Added full details for SAE J3016:2021 and BSI PAS 1883:2020
- Added: Koopman & Wagner (2019) on autonomous vehicle safety arguments (replaces Macenski)

### m5. Self-Citation Rate

**Response**: Added 3 external references: Koopman & Wagner (2019), Althoff (2021), Garcia et al. (2015) safe RL. Self-citation now 5/22 = 23%.
