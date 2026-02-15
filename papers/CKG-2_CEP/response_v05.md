# Point-by-Point Response — CKG-2 Iteration 4

**Reviewer**: B (Engineering Practitioner)
**Draft**: v04 → v05

---

## Minor Issues

### m1. PLC Implementation Guidance

**Response**: Added paragraph in §4.1 after Table 1c:
- Benchmark PLC: Siemens S7-1500 (CPU 1515-2 PN) with 300 ns/instruction
- ODD monitor fits within a single 10-ms cyclic task (even for 500-pool: 120 ms ODD + 200 ms MPC < 5000 ms sampling)
- Memory footprint: 14 constraints × 16 bytes (double precision) × 2 (A matrix + b vector) = 448 bytes for dual-tank; ~67 KB for 500-pool — well within S7-1500's 1 MB work memory
- For SIL-1 certified deployment: Siemens F-CPU (1516F-3 PN/DP) with safety program blocks in SCL
- Allen-Bradley ControlLogix 5580 achieves comparable performance (estimated 130 ms for 500-pool)

### m2. Permanent Communication Loss (S28) Behavior

**Response**: Added paragraph in §5.3 after S31 analysis:
- S28 (permanent loss): Layer 0 interlock holds valve at safe position (50% open for balanced flow)
- Tank 1 converges to a steady-state level determined by the pump flow rate and valve opening: $h_{ss} = Q_{\text{pump}} \cdot R_{v}(u=0.5)$, approximately 27 cm for nominal pump flow
- After 300 s (60 intervals), the system reaches steady state with $h_1 = 27.2$ cm (within ODD)
- The system can remain in this safe steady state indefinitely—it does not drain because the pump continues providing inflow
- SCADA alarm triggers operator intervention; design intent is manual override within 15 minutes
- For field systems: permanent comm loss triggers escalation to backup controller (redundant PLC on separate network path)
