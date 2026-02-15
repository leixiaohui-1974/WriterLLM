*Manuscript prepared for Environmental Modelling & Software*

__HydroGraph-GPU: A Graph-to-GPU Digital Twin Engine for Real-Time Water Network Simulation and Control__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Large-scale water networks need digital twin engines that can combine topology evolution, physics-based simulation, and control-facing services in one reproducible software stack. Existing implementations are often fragmented across disconnected graph, solver, and control tools, which raises integration cost and weakens reproducibility. This paper presents HydroGraph-GPU, an open framework that unifies graph compilation, GPU Saint-Venant simulation, and digital twin APIs under Cybernetics of Hydro Systems (CHS) conventions. The framework includes three modules: Graph Compiler (schema to computational graph), Solver Runtime (CUDA execution for Family $\alpha$ dynamics with actuator algebraic boundaries), and Twin Services (state estimation, replay, DMPC interface). We define a topology-preserving intermediate representation (TP-IR) for serial and branching networks and a deterministic partition strategy for cloud–area–edge deployment. This v02 manuscript focuses on architecture and reproducibility protocol; quantitative results are reported as benchmark protocol outputs to be finalized after full artifact verification.

__Keywords:__ digital twin; GPU computing; water networks; graph compilation; Cybernetics of Hydro Systems; open-source software

__Software availability__

- __Name__: HydroGraph-GPU  
- __License__: Apache-2.0 (planned)  
- __Languages__: Python, C++, CUDA  
- __Dependencies__: CUDA 12+, OpenMP, gRPC  
- __Availability__: repository URL will be released after internal artifact packaging and verification

---

## 1. Introduction

Hydraulic digital twins are moving from offline analysis into online operation. In CHS terms, they are runtime elements in the closed loop $\Sigma=(P,A,S,D,C,O)$, where simulation latency and fidelity affect operational safety and control quality. Existing engineering deployments still rely on heterogeneous software chains, causing duplicated model transformations and weak repeatability.

Within this project line, HZF-1 addressed hydraulic simulation acceleration and HZF-2 addressed DMPC optimization acceleration. HZF-3 targets software integration: graph topology ingestion, GPU solver compilation, and digital twin services in a single reproducible framework.

Contributions:

1. Topology-preserving intermediate representation (TP-IR) for pools, actuators, junctions, and constraints.
2. Graph-to-GPU compile pipeline that preserves hydraulic adjacency and coupling semantics.
3. Twin services for state estimation, deterministic replay, and DMPC coupling.
4. Reproducibility-first software packaging and benchmark protocol.

## 2. CHS-consistent formulation

### 2.1 Controlled-system core

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

Primary plant dynamics follow Family $\alpha$:

$$
G(s)=\frac{(1+\tau_m s)e^{-\tau_d s}}{A_s \cdot s} \tag{2}
$$

where $A_s$ [m²], $\tau_d$ [s], and $\tau_m$ [s].

Unified actuator boundary relation:

$$
\Delta Q = \alpha\,\Delta u + \beta_{\text{up}}\,\Delta H_{\text{up}} + \beta_{\text{dn}}\,\Delta H_{\text{dn}} \tag{3}
$$

where $\Delta Q$ [m³/s], $\Delta H$ [m], and $\alpha,\beta_{\text{up}},\beta_{\text{dn}}$ follow P1a symbol conventions.

### 2.2 TP-IR graph model

The network is encoded as directed graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$.

- Nodes: pools/storage units with hydraulic parameters.
- Edges: actuators/junction couplings with algebraic boundary metadata.
- Constraints: rate limits, safety envelopes, ODD tags.
- Deployment tags: cloud/area/edge ownership and timing layer.

TP-IR acts as the canonical contract between simulation and control modules.

## 3. Software architecture

### 3.1 Three-layer architecture

- __Graph Compiler__: schema validation, topology checks, partition planning.
- __Solver Runtime__: CUDA kernels, boundary exchange, synchronization policy.
- __Twin Services__: API gateway, replay manager, estimator/control connectors.

### 3.2 Compiler passes

Main passes include schema verification, strongly connected component detection, partitioning, kernel-fusion planning, and memory layout synthesis. Current stable scope is serial and tree topologies.

### 3.3 API contract (minimum)

- `POST /simulate/step`: advances one simulation step.
- `POST /state/estimate`: assimilates sensor snapshot.
- `POST /dmpc/prepare`: builds control-ready state package.
- `GET /scenario/{id}/replay`: deterministic replay endpoint.

Error behavior: invalid schema (400), unavailable runtime resource (503), determinism check mismatch (409).

### 3.4 Engineering fallback modes

When communication quality degrades (packet loss/jitter/clock drift), the runtime applies:

1. bounded hold-and-predict for missing upstream messages;
2. synchronization downgrade from global to zone-level clocks;
3. control fallback routing to lower safety layers (L0/L1) until consistency recovers.

## 4. Reproducibility and benchmark protocol

### 4.1 Benchmark tiers

- Tier S: 10-pool serial canal;
- Tier M: 50-pool mixed serial-branch transfer network;
- Tier L: 200-pool multi-branch synthetic backbone.

### 4.2 Reproducibility protocol

Each benchmark run records:

- container image digest and dependency lock files;
- deterministic seed set and compile plan hash;
- input dataset manifest and scenario checksum;
- output artifact bundle (logs, traces, replay hash).

Statistics protocol: each configuration runs 30 repeats, reporting median, interquartile range, and 95% confidence interval.

## 5. Current status of quantitative evidence (v02)

At this stage, architecture integration is complete for benchmark orchestration, while final quantitative tables are pending artifact verification and independent rerun checks. Therefore, this version reports the measurement protocol and evaluation endpoints rather than finalized headline numbers.

## 6. Limitations

1. Looped topologies are currently experimental and excluded from stable benchmark claims.
2. Cross-vendor PLC deployment is limited to interface-level compatibility tests in this version.
3. Large-fault cascading scenarios are defined but not yet fully validated in closed-loop experiments.

## 7. Conclusion

HydroGraph-GPU defines a CHS-consistent path from topology graph to control-ready digital twin runtime with explicit reproducibility constraints. The next revision will add externally verifiable quantitative results based on the benchmark protocol defined here.

## References note

`references.bib` currently stores internal manuscript records and mandatory project references. Full external bibliographic verification will be completed in the next revision round.
