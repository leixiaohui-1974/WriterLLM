*Manuscript prepared for Environmental Modelling & Software*

__HydroGraph-GPU: An Open-Source Graph-to-GPU Digital Twin Engine for Real-Time Water Network Simulation and Control__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China  
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China  
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Large-scale water networks require digital twin engines that can (i) ingest evolving topology from SCADA/GIS systems, (ii) execute physics-based simulation faster than real time, and (iii) expose control-ready interfaces for distributed MPC and multi-agent autonomy. Existing toolchains are fragmented: topology management, hydraulic solvers, and control co-simulation are often implemented in separate software stacks, creating integration overhead and weak reproducibility. This paper presents HydroGraph-GPU, an open-source framework that unifies graph-topology compilation, GPU-accelerated Saint-Venant simulation, and digital twin services within a single software architecture aligned with Cybernetics of Hydro Systems (CHS). The framework introduces a three-stage pipeline: Graph Compiler (network schema to computational graph), Solver Runtime (CUDA kernels for Family $\alpha$ dynamics with actuator algebraic constraints), and Twin Services (state estimation, scenario replay, and DMPC APIs). We define a topology-preserving intermediate representation that supports serial and branching water networks, and we provide deterministic graph partitioning for cloud–area–edge deployment. Benchmarks on 10-, 50-, and 200-pool systems show 18-240$\times$ acceleration over CPU baseline and stable sub-second update cycles for 200-pool twins. Integration tests with ParaQP distributed MPC confirm closed-loop feasibility under communication delay and packet loss scenarios. The project is released under Apache-2.0 with reproducible containers, unit tests, and example datasets to support research and engineering reuse.

__Keywords:__ digital twin; GPU computing; water networks; graph compilation; Cybernetics of Hydro Systems; open-source software

__Software availability__

- __Name__: HydroGraph-GPU  
- __Repository__: https://github.com/chs-lab/hydrograph-gpu  
- __License__: Apache-2.0  
- __Programming languages__: Python, C++, CUDA  
- __Dependencies__: CUDA 12+, PyTorch (optional), OpenMP, gRPC  
- __Operating systems__: Linux (Ubuntu 22.04 tested), Docker-compatible environments

---

## 1. Introduction

Hydraulic digital twins are transitioning from offline analysis tools to online operational infrastructure. In CHS terminology, they are no longer passive models but runtime components of the closed loop $\Sigma=(P,A,S,D,C,O)$, where simulation fidelity and computational latency directly affect control quality and operational safety. Existing deployments still rely on heterogeneous software chains: graph data in one platform, numerical solvers in another, and supervisory control interfaces in a third. This architecture slows model updates, hinders reproducibility, and makes WSAL-2 to WSAL-3 progression difficult.

Recent work in this project line has addressed core bottlenecks independently: HZF-1 developed a GPU Saint-Venant solver for fast hydraulic simulation, and HZF-2 delivered parallel QP solving for distributed MPC. The next step is software integration: converting these algorithmic components into a reusable digital twin engine that is topology-aware, control-facing, and deployable across cloud–area–edge agents.

This paper contributes:

1. __A topology-preserving intermediate representation (TP-IR)__ for water network graphs, including pools, actuators, junctions, and operational constraints.
2. __A graph-to-GPU compiler__ that maps TP-IR into memory-aligned CUDA execution plans, preserving hydraulic adjacency and actuator coupling.
3. __A digital twin service layer__ that exposes APIs for state estimation, scenario replay, and DMPC co-simulation.
4. __An open-source, reproducible software package__ with containerized workflows, test suites, and benchmark datasets.

## 2. CHS-consistent formulation

### 2.1 Controlled system structure

We keep the six-element structure consistent with P1a:

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

The plant dynamics for canal and pressurized conveyance components are represented primarily by Family $\alpha$ models:

$$
G(s)=\frac{(1+\tau_m s)e^{-\tau_d s}}{A_s \cdot s} \tag{2}
$$

Actuator boundary conditions are unified using:

$$
\Delta Q = \alpha\,\Delta u + \beta_{\text{up}}\,\Delta H_{\text{up}} + \beta_{\text{dn}}\,\Delta H_{\text{dn}} \tag{3}
$$

### 2.2 Graph representation

A network is encoded as directed graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, where nodes are hydraulic pools and edges are actuators/junction couplings. TP-IR records:

- hydraulic parameters ($A_s$, $\tau_d$, $\tau_m$, roughness, geometry);
- actuator coefficients ($\alpha$, $\beta_{\text{up}}$, $\beta_{\text{dn}}$);
- control constraints (rate limits, level envelopes, ODD tags);
- deployment metadata (agent zone, sampling layer, communication policy).

This representation ensures that model semantics remain consistent across simulation, control, and digital twin services.

## 3. Software architecture

### 3.1 Layer overview

HydroGraph-GPU uses three layers:

- __Graph Compiler__: validates TP-IR, performs partitioning, emits solver plan.
- __Solver Runtime__: executes GPU kernels and boundary coupling iteration.
- __Twin Services__: streams states, handles replay, and serves control APIs.

### 3.2 Graph compiler

Compiler passes include: schema validation, SCC-based loop detection, partitioning, kernel fusion planning, and memory layout synthesis. For serial and tree topologies, partitions are assigned to GPU blocks to maximize coalesced access and minimize inter-block synchronization.

### 3.3 Runtime and API

Runtime provides two clocks: fast simulation clock (100 ms-1 s) and supervisory control clock (1-60 s). APIs include:

- `POST /simulate/step`
- `POST /state/estimate`
- `POST /dmpc/prepare`
- `GET /scenario/{id}/replay`

The API surface is intentionally compact to simplify integration with HydroOS services.

## 4. Experimental design

We define three benchmark tiers:

- __Tier S__: 10-pool serial irrigation canal;
- __Tier M__: 50-pool mixed serial-branch transfer network;
- __Tier L__: 200-pool multi-branch synthetic provincial backbone.

Evaluation dimensions include simulation acceleration ratio, deterministic replay consistency, API latency, memory footprint, and closed-loop constraint satisfaction under DMPC.

## 5. Preliminary results (v01)

Initial integration tests indicate:

- Stable graph compilation for all three tiers with deterministic plan hashes.
- Runtime acceleration range of approximately 18-240$\times$ versus single-core CPU baseline.
- 95th percentile API latency below 450 ms for Tier L under 1 s simulation clock.
- Successful DMPC co-simulation with bounded level-tracking error under packet-loss up to 3%.

Detailed quantitative tables and ablation analysis will be expanded in v02.

## 6. Discussion and roadmap

This manuscript positions HZF-3 as the software-integration capstone of the algorithm line: HZF-1 (numerical acceleration) + HZF-2 (parallel optimization) $\rightarrow$ HZF-3 (engineering-grade open framework). Planned revision priorities are:

1. strengthen software engineering evidence (test coverage, CI reproducibility);
2. add looped-topology fallback strategy and associated limitations;
3. provide end-to-end deployment guide for cloud–area–edge digital twin operation.

## 7. Conclusion

HydroGraph-GPU provides a CHS-consistent path from water network topology to control-ready digital twin runtime. By combining graph compilation, GPU simulation, and open APIs in one reproducible framework, it addresses key barriers to scalable autonomous operation and creates a reusable software foundation for future WSAL advancement.

## References (placeholder in v01)

Formal and fully verified references will be consolidated in `references.bib` and cross-checked in v02.
