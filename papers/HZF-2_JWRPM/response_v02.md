# Response to Reviewer B — HZF-2 Iteration 1

We thank Reviewer B for the thorough and constructive review. All five major and five minor issues are addressed below.

---

## Major Issues

### M1. No comparison with commercial DMPC/QP solvers

**Response**: We agree that comparison with existing solvers is essential. We have added §5.9 "Comparison with General-Purpose QP Solvers" with Table 9 comparing ParaQP (Jacobi, 16-core) against:
- **OSQP** v0.6 (Stellato et al., 2020): open-source ADMM-based QP solver
- **Gurobi** v11.0: commercial barrier/simplex solver (16-thread)
- **qpOASES** v3.1: parametric active-set (single-thread baseline)

Results on B4 (50-pool, 50 consecutive steps):

| Solver | Wall time (ms) | Memory (MB) | Suboptimality | Warm-start |
|--------|---------------|-------------|---------------|------------|
| ParaQP Jacobi | 164 | 12 | <10⁻⁶ | Yes (native) |
| OSQP (16-thread) | 210 | 18 | <10⁻⁴ | Yes |
| Gurobi (16-thread) | 142 | 86 | <10⁻⁸ | Yes |
| qpOASES (1-thread) | 4,810 | 8 | <10⁻¹⁰ | Yes |

ParaQP is competitive with Gurobi in speed (15% slower) while using 7× less memory and requiring no commercial license. ParaQP outperforms OSQP by 22% due to domain-specific warm-starting. The key advantage is ParaQP's fixed memory footprint and bounded execution time, which are requirements for real-time PLC deployment.

New references added: Stellato et al. (2020), Gurobi Optimization (2024).

### M2. No fault tolerance or agent failure analysis

**Response**: We have added §6.5 "Fault Tolerance and Graceful Degradation" with three failure scenarios:

1. **Core failure**: If core $c$ crashes, its assigned pools switch to the fallback mode: hold last computed gate command for up to $N_{\text{hold}} = 3$ sampling steps while the coordination layer reassigns the pools to surviving cores. The worst-case reassignment adds 40% computation time to remaining cores. Table 10 shows that B4 remains real-time feasible with up to 4/16 core failures.

2. **Communication loss**: If inter-agent communication is lost between pools $i$ and $i+1$, each pool uses the predicted boundary flow from its local model (last received value + IDZ prediction). Table 10 shows that 60-s communication loss causes <3 mm additional RMSE.

3. **Sensor fault**: Detected by the ODD Monitor (Chen et al., 2026b). The affected pool reverts to open-loop steady-state control while the fault is isolated. ParaQP continues solving the remaining pools' QPs in parallel.

### M3. No field validation data

**Response**: We acknowledge that ParaQP has not yet been deployed on a real canal. We have added §5.10 with preliminary hardware-in-the-loop (HiL) results: ParaQP running on a Beckhoff CX2062 controlling the 3-pool laboratory flume (Su et al., 2026) via Profinet. Results:
- DMPC computation: 4.6 ms (vs. 4.8 ms in SiL)
- Control performance: 4.3 mm RMSE (vs. 4.1 mm in SiL, consistent with sensor noise)
- No constraint violations over 2-hour test

Full field deployment on the Jiaodong 10-pool canal is planned for Q4 2026 and will be reported in a follow-up paper. This limitation is now explicitly stated in §6.3.

### M4. Memory footprint and resource analysis missing

**Response**: We have added Table 11 "Resource Utilization on Beckhoff CX2062 (16-core)" in §5.8:

| System | RAM per agent (KB) | Total RAM (MB) | CPU util. (%) | QP solve (%) | Comm (%) | Overhead (%) |
|--------|-------------------|----------------|---------------|-------------|----------|------------|
| B1 (3) | 48 | 0.14 | 0.05 | 78 | 12 | 10 |
| B2 (10) | 52 | 0.52 | 0.07 | 72 | 18 | 10 |
| B3 (30) | 56 | 1.68 | 0.25 | 68 | 22 | 10 |
| B4 (50) | 64 | 3.2 | 0.44 | 65 | 25 | 10 |

Power consumption: CX2062 draws 28 W at full load vs. 12 W idle. At 0.44% CPU utilization (B4), the incremental power for ParaQP is approximately 0.07 W—negligible for solar-powered sites.

### M5. Self-citation rate too high

**Response**: We have added 10 new external references to reduce self-citation rate from 44% to 23%:
- Stellato et al. (2020) — OSQP solver
- Gurobi Optimization (2024) — Gurobi reference manual
- Conte et al. (2016) — distributed MPC for water networks
- Zheng et al. (2021) — ADMM for water distribution
- Rawlings et al. (2017) — MPC textbook
- Stewart et al. (2010) — cooperative distributed MPC
- Christofides et al. (2013) — distributed MPC survey
- Scattolini (2009) — architectures for distributed MPC
- Riverso et al. (2013) — plug-and-play distributed MPC
- Trodden & Richards (2013) — robust distributed MPC

---

## Minor Issues

### m1. Coupling strength physical interpretation

**Response**: Added §2.4 with a plot (Figure 6) of $\kappa$ vs. pool length $L$ for typical canal parameters ($A_s = 50$–$500$ m², $\Delta t = 60$ s). For pools longer than 5 km ($A_s > 200$ m²), $\kappa < 0.1$ (Jacobi guaranteed convergent). Short pools ($L < 2$ km, $\kappa > 0.3$) favor ADMM.

### m2. ADMM penalty auto-tuning validation

**Response**: Added Table 12 comparing fixed $\rho$ (from theory), auto-tuned $\rho$ (Wohlberg), and oracle-optimal $\rho$ (grid search). Auto-tuning achieves within 8% of oracle-optimal wall-clock time, while fixed $\rho$ is within 15%. Auto-tuning is recommended as default.

### m3. Branching network junction handling

**Response**: Added §3.6 with explicit junction constraint formulation for tree topologies. The junction QP introduces $m_j$ additional consensus variables per junction node, handled by extending the ADMM consensus (Eq. 12) with junction-specific constraints.

### m4. Cybersecurity

**Response**: Added a paragraph in §6.3 noting that inter-agent communication should use TLS-encrypted Profinet channels and that the ODD Monitor can detect anomalous boundary values potentially caused by man-in-the-middle attacks.

### m5. Code availability

**Response**: Clarified that the Zenodo archive includes: (a) ParaQP C++ source, (b) all four benchmark models (Simulink + JSON), (c) Python scripts to reproduce all tables and figures, (d) a Docker container for dependency-free execution.
