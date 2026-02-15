*Manuscript prepared for Environmental Modelling & Software*

__HydroGraph-GPU: A CHS-Oriented Graph-to-GPU Digital Twin Engine for Real-Time Water Network Simulation and Control__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

## 0.1 Key claims and evidence status (v03)

| Claim | Type | Evidence status in v03 |
|---|---|---|
| Graph-to-GPU integrated workflow is implemented | Method | Implemented and structurally documented |
| Deterministic replay pipeline is available | Engineering | Implemented; quantitative archive verification in progress |
| Tier-S/M/L benchmark superiority | Performance | Pre-registered criteria defined; final metrics pending |
| WSAL governance/fallback protocol | Safety/governance | Specified as policy and runtime rule set |

__Abstract__

Large-scale water networks need digital twin engines that combine topology evolution, physics-based simulation, and control-facing services with strong reproducibility constraints. HydroGraph-GPU unifies graph compilation, GPU Saint-Venant simulation, and digital twin APIs under Cybernetics of Hydro Systems (CHS) conventions. The framework includes Graph Compiler, Solver Runtime, and Twin Services modules with a topology-preserving intermediate representation (TP-IR) and deterministic partition strategy for cloud–area–edge deployment. This revision emphasizes novelty separation (method vs engineering), governance rules for WSAL transition, and pre-registered benchmark acceptance criteria. Final quantitative tables remain pending independent artifact verification.

__Keywords:__ digital twin; GPU computing; water networks; graph compilation; Cybernetics of Hydro Systems; open-source software

__Software availability__

- __Name__: HydroGraph-GPU  
- __License__: Apache-2.0 (planned)  
- __Languages__: Python, C++, CUDA  
- __Dependencies__: CUDA 12+, OpenMP, gRPC  
- __Availability__: repository URL will be released after artifact packaging and verification

---

## 1. Introduction

### 1.1 Two-axis novelty framing

This work claims two distinct novelty axes:

1. __Method novelty__: topology-preserving graph compilation tightly coupled with hydraulic GPU runtime and CHS-consistent actuator boundaries.
2. __Engineering novelty__: deterministic replay, tiered benchmark governance, and WSAL-aware fallback orchestration for operational deployment.

### 1.2 Differentiation from generic digital-twin stacks

Unlike generic infrastructure digital twins, HydroGraph-GPU is constrained by water-system physics and CHS semantics: (a) delay-dominated hydraulic dynamics, (b) unified actuator algebraic boundary conditions, and (c) WSAL safety floor requiring bounded fallback behavior during communication degradation.

### 1.3 Role in project-line integration

HZF-3 integrates algorithmic outputs from HZF-1 (GPU hydraulic solving) and HZF-2 (parallel DMPC), while providing software interfaces reusable by BAK-1 model assets and P2D engineering deployment tasks.

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

where $A_s$ [m²], $\tau_d$ [s], $\tau_m$ [s], $\Delta Q$ [m³/s], and $\Delta H$ [m]. Symbols follow P1a conventions.

The network is encoded as $\mathcal{G}=(\mathcal{V},\mathcal{E})$ with TP-IR metadata for pool parameters, actuator coefficients, ODD tags, and deployment ownership.

## 3. Software architecture

> Notation reminder: all flow/head/control symbols remain aligned with shared CHS symbol table.

### 3.1 Three-layer design

- __Graph Compiler__: schema validation, topology checks, partition planning.
- __Solver Runtime__: CUDA kernels, boundary exchange, synchronization policy.
- __Twin Services__: API gateway, replay manager, estimator/control connectors.

### 3.2 Compiler passes

Schema verification, SCC detection, partitioning, kernel-fusion planning, and memory layout synthesis are implemented for serial/tree topologies.

### 3.3 API contract and compatibility

- `POST /simulate/step`
- `POST /state/estimate`
- `POST /dmpc/prepare`
- `GET /scenario/{id}/replay`

Error behavior: invalid schema (400), runtime unavailable (503), determinism mismatch (409).

Backward compatibility policy: minor API versions remain backward-compatible for one full release cycle; breaking changes require migration notes and replay-regression pass.

### 3.4 Engineering fallback modes

Communication degradation handling includes:

1. bounded hold-and-predict for missing upstream messages;
2. synchronization downgrade from global to zone-level clocks;
3. control fallback to L0/L1-safe strategy until consistency recovery.

### 3.5 WSAL governance and escalation

For WSAL-2→3 transition experiments, governance rules enforce:

- mandatory xIL gate before autonomy escalation;
- explicit veto authority of safety layer over optimization outputs;
- incident-classification workflow for automatic rollback from L3 to L2 operation.

## 4. Reproducibility and benchmark protocol

### 4.1 Benchmark tiers

- Tier S: 10-pool serial canal
- Tier M: 50-pool mixed serial-branch network
- Tier L: 200-pool multi-branch synthetic backbone

### 4.2 Reproducibility protocol

Each run records container digest, dependency lock files, deterministic seed set, compile-plan hash, input manifest checksum, and output replay hash.

### 4.3 Pre-registered acceptance criteria

- Runtime latency: 95th percentile step latency below scenario-specific control cycle limit.
- Replay determinism: hash mismatch rate = 0 across fixed-seed reruns.
- Safety performance: zero hard constraint violations in nominal scenarios; bounded recovery time under injected communication faults.

### 4.4 Artifact retention policy

All benchmark artifacts are retained for at least 24 months in project archive storage with immutable manifest IDs and rerun scripts.

## 5. Evidence status in this revision

v03 provides architecture-level and protocol-level readiness. Final quantitative benchmark tables remain pending independent rerun confirmation and externalized artifact bundle checks.

## 6. Discussion

### 6.1 Innovation boundary

HydroGraph-GPU contributes integration and reproducibility structure, not a new hydraulic PDE family or a new optimal-control theorem.

### 6.2 Cross-paper linkage

- HZF-1 → HZF-3: GPU Saint-Venant runtime core.
- HZF-2 → HZF-3: DMPC solve interface for control co-simulation.
- BAK-1 ↔ HZF-3: model asset ingestion path via TP-IR.
- P2D ↔ HZF-3: engineering deployment and digital-twin operational reuse.

## 7. Conclusion

HydroGraph-GPU establishes a CHS-consistent graph-to-runtime software pathway for water-network digital twins with reproducibility and governance constraints made explicit. The next iteration will add externally verifiable quantitative evidence under the pre-registered benchmark criteria.

## References note

`references.bib` currently stores mandatory project records and is explicitly non-final; third-party references will be added after bibliographic verification.
