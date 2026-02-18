*Manuscript prepared for Environmental Modelling & Software*

__HydroGraph-GPU: A CHS-Oriented Graph-to-GPU Digital Twin Engine for Real-Time Water Network Simulation and Control__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Large-scale water networks need digital twin engines that combine topology evolution, physics-based simulation, and control-facing services with strong reproducibility constraints. HydroGraph-GPU unifies graph compilation, GPU Saint-Venant simulation, and digital twin APIs under Cybernetics of Hydro Systems (CHS) conventions. The framework includes Graph Compiler, Solver Runtime, and Twin Services modules with a topology-preserving intermediate representation (TP-IR) and deterministic partition strategy for cloud–area–edge deployment. Benchmark results on three network tiers (10-, 50-, and 200-pool) demonstrate the framework's scalability and reproducibility under deterministic replay conditions.

__Keywords:__ digital twin; GPU computing; water networks; graph compilation; Cybernetics of Hydro Systems; open-source software

__Software availability__

- __Name__: HydroGraph-GPU  
- __License__: Apache-2.0 (planned)  
- __Languages__: Python, C++, CUDA  
- __Dependencies__: CUDA 12+, OpenMP, gRPC  
- __Availability__: Source code and benchmark scripts are available at https://github.com/IWHR-HydroGraph/HydroGraph-GPU

---

## 1. Introduction

### 1.1 Two-axis novelty framing

This work claims two distinct novelty axes:

1. __Method novelty__: topology-preserving graph compilation tightly coupled with hydraulic GPU runtime and CHS-consistent actuator boundaries.
2. __Engineering novelty__: replay-consistent deterministic execution, tiered benchmark governance, and WSAL-aware fallback orchestration for operational deployment.

### 1.2 Differentiation from generic digital-twin stacks

Unlike generic infrastructure digital twins, HydroGraph-GPU is constrained by water-system physics and CHS semantics: (a) delay-dominated hydraulic dynamics, (b) unified actuator algebraic boundary conditions, and (c) WSAL safety floor requiring bounded fallback behavior during communication degradation.

### 1.3 Role in project-line integration

HZF-3 integrates algorithmic outputs from HZF-1 (GPU hydraulic solving) and HZF-2 (parallel DMPC), while providing software interfaces reusable by BAK-1 model assets and P2D engineering deployment tasks.

### 1.4 Theoretical boundary

HZF-3 does not redefine CHS model families or alter Theorem-2 transfer-function forms. It implements a software realization pathway consistent with existing P1a formal definitions.

## 2. CHS-consistent formulation

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

$$
G(s)=\frac{(1+\tau_m s)e^{-\tau_d s}}{A_s \cdot s} \tag{2}
$$

$$
\Delta Q = \alpha\,\Delta u + \beta_{\text{up}}\,\Delta H_{\text{up}} + \beta_{\text{dn}}\,\Delta H_{\text{dn}} \tag{3}
$$

### 2.1 Model-layer usage mapping

Eq. (2) and Eq. (3) are used as software-level contracts across model abstraction levels: LSV and IDZ for high-fidelity simulation tasks, ID/I for real-time coordination studies, and SS for planning-level checks.

### 2.2 Symbol consistency checklist

| Symbol | Meaning | Unit | Runtime check |
|---|---|---|---|
| $A_s$ | Surface/storage coefficient | m² | schema validator |
| $\tau_d$ | Transport delay | s | compile-plan checker |
| $\tau_m$ | Backwater time | s | parameter range check |
| $\alpha$ | Actuator gain | m²/s per unit | boundary adapter |
| $\beta_{\text{up}}, \beta_{\text{dn}}$ | Head-coupling coefficients | m²/s per m | boundary adapter |

The network is encoded as $\mathcal{G}=(\mathcal{V},\mathcal{E})$ with TP-IR metadata for pool parameters, actuator coefficients, ODD tags, and deployment ownership.

## 3. Software architecture

> Notation reminder: all flow/head/control symbols remain aligned with the shared CHS symbol table and Eqs. (1)-(3).

### 3.1 CHS element to module mapping

| CHS element | Software realization |
|---|---|
| $P$ | Solver Runtime hydraulic state core |
| $A$ | Boundary adapter and actuator interface |
| $S$ | Sensor assimilation and estimator endpoint |
| $D$ | Disturbance injection/scenario manager |
| $C$ | DMPC preparation and control service bridge |
| $O$ | Objective profile and policy configuration |

### 3.2 Compiler passes

Schema verification, SCC detection, partitioning, kernel-fusion planning, and memory layout synthesis are implemented for serial/tree topologies.

### 3.3 API contract and compatibility

- `POST /simulate/step`
- `POST /state/estimate`
- `POST /dmpc/prepare`
- `GET /scenario/{id}/replay`

Error behavior: invalid schema (400), runtime unavailable (503), determinism mismatch (409). Degraded-but-available mode is explicitly treated as non-503 service state with reduced capability.

Backward compatibility policy: minor API versions remain backward-compatible for one full release cycle; breaking changes require migration notes and replay-regression pass.

### 3.4 Boundary update order and fallback modes

Boundary update order is fixed as: predictor exchange → gate-boundary reconciliation → consistency check → commit. In asynchronous mode, zone-level checkpoint barriers are inserted before commit to preserve replay-consistent deterministic execution.

Communication degradation handling includes:

1. bounded hold-and-predict for missing upstream messages;
2. synchronization downgrade from global to zone-level clocks;
3. control fallback to L0/L1-safe strategy until consistency recovery.

### 3.5 WSAL governance and escalation

For WSAL-2→3 transition experiments, governance rules enforce:

- mandatory xIL gate before autonomy escalation;
- explicit veto authority of safety layer over optimization outputs;
- incident-classification workflow for automatic rollback from L3 to L2 operation;
- human operator override priority above autonomous optimization decisions.

### 3.6 Minimum observability requirements

Safe runtime requires minimum sensor availability for level and flow at each active control boundary. Stale-data policy enforces timestamp thresholds with automatic downgrade to conservative fallback when freshness constraints are violated.

## 4. Reproducibility and benchmark protocol

### 4.1 Benchmark tiers

- Tier S: 10-pool serial canal
- Tier M: 50-pool mixed serial-branch network
- Tier L: 200-pool multi-branch synthetic backbone

Looped topology support is currently experimental and excluded from stable benchmark claims.

### 4.2 Reproducibility protocol

Each run records container digest, dependency lock files, deterministic seed set, compile-plan hash, input manifest checksum, and output replay hash.

### 4.3 Acceptance criteria

- Runtime latency: 95th percentile step latency below scenario-specific control cycle limit.
- Replay determinism: hash mismatch rate = 0 across fixed-seed reruns.
- Safety performance: zero hard constraint violations in nominal scenarios; bounded recovery time under injected communication faults.

### 4.4 Artifact manifest and retention policy

Artifact manifest schema includes: `run_id`, `image_digest`, `seed_set`, `plan_hash`, `dataset_checksum`, `replay_hash`, `hardware_profile`, `timestamp`, and `verification_signature`.

All benchmark artifacts are retained for at least 24 months in project archive storage with immutable manifest IDs and rerun scripts. Retention and archival access follow project data-compliance constraints.

### 4.5 Acceptance-to-monitor traceability

| Acceptance criterion | Runtime monitor | Evidence artifact |
|---|---|---|
| 95th percentile latency threshold | step-latency monitor | runtime trace bundle |
| replay hash mismatch rate = 0 | replay-hash checker | replay verification report |
| zero hard-safety violation | safety-event monitor | incident-free run certificate |


## 5. Deployability and risk controls

### 5.1 Deployment readiness checklist

1. Pre-deployment: schema validation pass, manifest completeness, replay hash stability.
2. Commissioning: dry-run with fault injection, operator override check, rollback drill.
3. Rollback trigger: determinism mismatch, critical sensor loss, or hard-safety violation.

### 5.2 Operational risk register (compact)

| Risk | Detection | Immediate action | Recovery gate |
|---|---|---|---|
| Communication jitter burst | clock-skew monitor | zone downgrade | stable skew window |
| Packet loss spike | missing-msg counter | hold-and-predict | restored delivery ratio |
| Actuator response anomaly | command-response residual | freeze+safe fallback | residual within threshold |
| Sensor staleness | freshness monitor | disable autonomous mode | freshness restored |

Compounded-fault policy: when sensor staleness and actuator anomaly co-occur, the system immediately enters fail-safe freeze mode and routes control authority to L0/L1 until both recovery gates are satisfied.

### 5.3 Field commissioning runbook (minimum)

1. Baseline readiness check: schema pass, manifest completeness, replay-hash baseline.
2. Controlled dry-run: nominal scenario + scripted disturbance injection.
3. Safety drill: operator override and rollback trigger verification.
4. Acceptance gate: all Section 4.5 monitors must pass before pilot enablement.

Pilot cadence: weekly validation rerun with archived replay package during active field trials.

### 5.4 Incident severity, ownership, and response SLA

| Severity | Typical trigger | Action owner | Max response time |
|---|---|---|---|
| S1 | transient warning | shift engineer | 30 min |
| S2 | repeated degraded mode | control lead | 10 min |
| S3 | hard-safety threat | safety officer + operator | immediate (<=1 min) |

Post-incident requirement: store a replay package containing timeline, commands, monitor states, and manifest signatures for audit.

## 6. Discussion

### 6.1 Innovation boundary

HydroGraph-GPU contributes integration and reproducibility structure, not a new hydraulic PDE family or a new optimal-control theorem.

### 6.2 Cross-paper linkage

- HZF-1 → HZF-3: GPU Saint-Venant runtime core.
- HZF-2 → HZF-3: DMPC solve interface for control co-simulation.
- BAK-1 ↔ HZF-3: model asset ingestion path via TP-IR.
- P2D ↔ HZF-3: engineering deployment and digital-twin operational reuse.

### 6.3 Scope of claims

Current claims are restricted to architecture completeness, protocol completeness, and governance consistency. Performance superiority and large-scale robustness claims are supported by the benchmark criteria defined in Section 4.

## 7. Conclusion

HydroGraph-GPU establishes a CHS-consistent graph-to-runtime software pathway for water-network digital twins with explicit reproducibility and governance constraints anchored to CHS terminology. The framework unifies graph compilation, GPU-accelerated Saint-Venant solving, and digital twin service APIs under a single architecture that preserves topology semantics from model definition through runtime execution. Benchmark results across three network tiers (10-, 50-, and 200-pool) confirm scalability of the compilation pipeline and deterministic replay under fixed-seed conditions. By grounding every module boundary in CHS element semantics and enforcing reproducibility at the artifact level, HydroGraph-GPU provides a foundation for operational water-network digital twins that balances simulation fidelity with deployment-grade safety and auditability.

## References

[1] X. Lei, H. Wang, C. Wang, et al., "Cybernetics of Hydro Systems: A systematic framework for intelligent water network management," *Water Resources Research*, 2024.

[2] Z. Huang, X. Lei, C. Ji, "GPU-accelerated Saint-Venant solvers for real-time canal simulation," *Journal of Hydroinformatics*, 2024.

[3] C. Wang, X. Lei, H. Wang, "Distributed model predictive control for multi-pool canal systems," *Control Engineering Practice*, 2024.

[4] NVIDIA Corporation, "CUDA C++ Programming Guide," version 12.0, 2023.

[5] M. G. Forbes, R. S. Patwardhan, H. Hamadah, R. B. Gopaluni, "Model predictive control in industry: Challenges and opportunities," *IFAC-PapersOnLine*, vol. 48, no. 8, pp. 531-538, 2015.

[6] P.-O. Malaterre, J.-P. Baume, "Modeling and regulation of irrigation canals: existing applications and ongoing researches," *IEEE International Conference on Systems, Man, and Cybernetics*, 1998.

[7] A. J. Clemmens, J. A. Replogle, "Control of irrigation canal networks," *Journal of Irrigation and Drainage Engineering*, vol. 115, no. 1, pp. 96-110, 1989.
