*Manuscript submitted to Journal of Water Resources Planning and Management*

__Parallel Quadratic Programming for Distributed Model Predictive Control of Water Conveyance Networks__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Distributed Model Predictive Control (DMPC) enables scalable real-time control of multi-pool water conveyance networks by decomposing a centralized optimization into coupled local Quadratic Programs (QPs). However, sequential solution of these QPs on standard Programmable Logic Controllers (PLCs) creates a computational bottleneck that limits practical deployment beyond approximately 20 pools. This paper presents ParaQP, a parallel QP solver architecture for DMPC that exploits the block-separable structure of water network optimization problems. The algorithm decomposes the global DMPC problem along pool boundaries, solves local QPs concurrently on a multi-core platform, and coordinates inter-agent coupling through an Alternating Direction Method of Multipliers (ADMM) consensus layer with guaranteed convergence. Three decomposition strategies are developed—serial relaxation, Jacobi parallel, and ADMM consensus—with formal convergence proofs for the water network QP structure. Validation on four benchmark systems (3-pool laboratory flume, 10-pool Jiaodong irrigation district, 30-pool synthetic branching network, and 50-pool South-to-North Water Diversion proxy) demonstrates that ParaQP achieves 5.8–18.4× speedup over sequential DMPC on a 16-core industrial PC, reducing worst-case computation time from 4.8 s to 0.26 s for the 50-pool system (well within the 60 s sampling interval). Comparison with general-purpose solvers (OSQP, Gurobi) shows that ParaQP is competitive in speed while using 7× less memory and requiring no commercial license. Hardware-in-the-loop validation on a 3-pool laboratory flume confirms real-time feasibility with 4.3 mm RMSE. Integration with the cuSVE GPU solver (Huang et al., 2026) enables full-fidelity Software-in-the-Loop verification at 210,000× real-time. The solver is released as open-source software (MIT license) compatible with the CHS HydroRTP toolbox.

__Keywords:__ distributed model predictive control; quadratic programming; parallel computing; water conveyance; canal automation; ADMM; CHS

__1  Introduction__

Autonomous operation of water conveyance networks requires real-time control algorithms that scale to systems comprising tens to hundreds of canal pools (Lei, 2025a). The Cybernetics of Hydro Systems (CHS) framework unifies water network control by treating each canal pool as a Plant element characterized by a Family α (integrating) transfer function $G(s) = (1 + \tau_m s) e^{-\tau_d s} / (A_s \cdot s)$, connected by Actuator elements (gates, pumps) that regulate flow between pools (Lei, 2025a; Lei et al., 2025b). Model Predictive Control (MPC) is the preferred control strategy at the CHS Edge Agent level, solving a constrained Quadratic Program (QP) at each sampling step to compute optimal gate trajectories over a finite prediction horizon (Malaterre et al., 1998; van Overloop, 2006; Rawlings et al., 2017).

For multi-pool systems, Distributed MPC (DMPC) decomposes the global optimization into local QPs—one per pool agent—that exchange boundary information with neighboring agents (Negenborn et al., 2009; Scattolini, 2009; Christofides et al., 2013). This decomposition offers three advantages: (a) computational load scales linearly rather than cubically with system size, (b) each agent requires only local model parameters, and (c) the architecture maps naturally onto the CHS multi-agent hierarchy where Edge Agents control individual pools and Area Agents coordinate groups (Lei et al., 2025b). Several studies have applied DMPC to canal systems (Lemos et al., 2012; Conte et al., 2016; Stewart et al., 2010), while plug-and-play architectures (Riverso et al., 2013) enable dynamic reconfiguration of the agent network. Robust formulations (Trodden & Richards, 2013) address model uncertainty, and ADMM-based approaches (Zheng et al., 2021) have shown promise for water distribution optimization.

However, a critical computational bottleneck remains. In current DMPC implementations for water networks, local QPs are solved sequentially—agent 1 solves its QP, passes boundary values to agent 2, which solves its QP, and so on (Negenborn et al., 2009). For a system of $N_p$ pools with prediction horizon $N_h$ and control horizon $N_u$, each local QP has $O(N_u)$ decision variables and $O(N_h)$ constraints, solved in $O(N_u^2 N_h)$ operations. Sequential execution requires $N_p$ such solves per DMPC iteration, plus multiple outer iterations for inter-agent convergence, yielding total computation time:

$$
T_{\text{seq}} = K_{\text{outer}} \cdot N_p \cdot T_{\text{QP}} \tag{1}
$$

where $K_{\text{outer}}$ is the number of outer (inter-agent) iterations and $T_{\text{QP}}$ is the single-QP solve time. For $N_p = 50$, $K_{\text{outer}} = 5$, and $T_{\text{QP}} = 20$ ms (typical on S7-1500 PLC), $T_{\text{seq}} = 5.0$ s—approaching the 10 s sampling interval used in large canal systems.

This paper addresses the sequential bottleneck by developing ParaQP, a parallel QP solver architecture that exploits the block-separable structure of the water network DMPC problem. The contributions are:

1. **Three parallel decomposition strategies**: serial relaxation (Gauss-Seidel), Jacobi parallel, and ADMM consensus, each with formal convergence guarantees for the water network QP structure (Theorem 1–3).

2. **Communication-aware scheduling**: an algorithm that maps pool agents to processor cores accounting for communication topology (serial chain, tree, mesh) and minimizes inter-core data transfer.

3. **Quantitative benchmarking**: systematic comparison on four water network benchmarks (3–50 pools) measuring speedup, convergence rate, control quality, and real-time feasibility, including comparison with general-purpose QP solvers (OSQP, Gurobi).

4. **Full-fidelity integration**: coupling with cuSVE (Huang et al., 2026) for SiL verification at Saint-Venant fidelity, and with HydroRTP (Yin et al., 2026) for PLC code generation.

5. **Fault tolerance**: graceful degradation analysis under core failure, communication loss, and sensor fault scenarios.

__2  Problem Formulation__

__2.1  DMPC for Water Conveyance Networks__

Consider a water conveyance network with $N_p$ pools connected in a directed graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where $\mathcal{V} = \{1, \ldots, N_p\}$ represents pools and $\mathcal{E}$ represents hydraulic connections via gates. Each pool $i$ is modeled by the IDZ (Integrator-Delay-Zero) discrete-time state-space representation (Schuurmans et al., 1999; Litrico & Fromion, 2009):

$$
x_i(k+1) = A_i x_i(k) + B_i u_i(k) + E_i d_i(k) \tag{2}
$$

$$
y_i(k) = C_i x_i(k) \tag{3}
$$

where $x_i \in \mathbb{R}^{n_i}$ is the state vector (water levels at downstream and intermediate nodes), $u_i \in \mathbb{R}^{m_i}$ is the control input (gate openings), $d_i \in \mathbb{R}^{p_i}$ is the disturbance (offtakes, lateral inflow), and $y_i \in \mathbb{R}^{q_i}$ is the measured output (downstream water level). The matrices $A_i, B_i, E_i, C_i$ are derived from IDZ model parameters $(A_{s,i}, \tau_{d,i}, \tau_{m,i})$ with sampling period $\Delta t$.

Inter-pool coupling arises through shared boundary conditions: the downstream gate flow of pool $i$ equals the upstream inflow of pool $i+1$ (for serial topology). Defining $u_i^{\text{dn}}$ as pool $i$'s downstream gate opening and $d_{i+1}^{\text{up}}$ as pool $i+1$'s upstream inflow:

$$
d_{i+1}^{\text{up}}(k) = f_{\text{gate}}(u_i^{\text{dn}}(k), y_i(k), y_{i+1}(k)) \tag{4}
$$

where $f_{\text{gate}}$ is the linearized gate equation (Lei, 2025a, Lemma 3).

The centralized MPC formulates a single QP over all pools:

$$
\min_{\Delta \mathbf{U}} J = \sum_{i=1}^{N_p} \sum_{k=0}^{N_h-1} \left[ \| y_i(k) - r_i(k) \|^2_{Q_i} + \| \Delta u_i(k) \|^2_{R_i} \right] \tag{5}
$$

subject to:

$$
u_{i,\min} \leq u_i(k) \leq u_{i,\max}, \quad |\Delta u_i(k)| \leq \Delta u_{i,\max}, \quad y_{i,\min} \leq y_i(k) \leq y_{i,\max} \tag{6}
$$

where $\Delta \mathbf{U} = [\Delta u_1^T, \ldots, \Delta u_{N_p}^T]^T$ is the stacked control increment vector, $r_i(k)$ is the reference trajectory, and $Q_i, R_i$ are weighting matrices.

__2.2  Block-Separable QP Structure__

The centralized QP (Eq. 5–6) can be written in compact form:

$$
\min_{\Delta \mathbf{U}} \frac{1}{2} \Delta \mathbf{U}^T \mathbf{H} \Delta \mathbf{U} + \mathbf{f}^T \Delta \mathbf{U} \quad \text{s.t.} \quad \mathbf{G} \Delta \mathbf{U} \leq \mathbf{w} \tag{7}
$$

The Hessian $\mathbf{H}$ has block-arrow structure:

$$
\mathbf{H} = \begin{bmatrix} H_1 & H_{12} & & \\ H_{21} & H_2 & H_{23} & \\ & \ddots & \ddots & \ddots \\ & & H_{N_p-1,N_p} & H_{N_p} \end{bmatrix} \tag{8}
$$

where diagonal blocks $H_i \in \mathbb{R}^{N_u \times N_u}$ represent local costs and off-diagonal blocks $H_{ij}$ represent inter-pool coupling through shared gate variables. For serial canal topologies, the coupling is tridiagonal (each pool couples only with its immediate upstream and downstream neighbors). For branching networks, the sparsity pattern follows the network adjacency graph.

**Key structural property**: The coupling blocks $H_{ij}$ have rank at most $m_i$ (the number of shared gate variables), which is typically 1–2 for water networks. This low-rank coupling enables efficient decomposition.

__2.3  Coupling Strength Parameter__

We define the coupling strength as:

$$
\kappa = \max_{i} \frac{\|H_{i,i+1}\|_F}{\|H_i\|_F} \tag{9}
$$

For water conveyance networks, $\kappa$ is determined by the ratio of gate-coupling cost to local tracking cost. Typical values are $\kappa \in [0.05, 0.3]$: lower for long pools with large $A_s$ (dominant local dynamics), higher for short pools with strong hydraulic coupling. This parameter governs the convergence rate of all three decomposition strategies.

__2.4  Physical Interpretation of Coupling Strength__

The coupling strength $\kappa$ has a direct physical interpretation for water engineers. For a canal pool with surface area $A_s$, delay time $\tau_d$, and sampling period $\Delta t$, the coupling strength is approximately:

$$
\kappa \approx \frac{\alpha \cdot \Delta t}{A_s \cdot \Delta h_{\text{ref}}} \cdot \frac{\|Q_i\|}{R_i} \tag{10}
$$

where $\alpha$ is the gate linearization coefficient, $\Delta h_{\text{ref}}$ is the reference head difference, and $\|Q_i\|/R_i$ is the tracking-to-control weight ratio. Figure 6 shows $\kappa$ as a function of pool length $L$ for typical canal parameters. For pools longer than 5 km ($A_s > 200$ m²), $\kappa < 0.1$ and all three strategies converge rapidly. For short pools ($L < 2$ km, $\kappa > 0.3$), ADMM is preferred due to its unconditional convergence guarantee.

__*[Figure 6 about here]*__

__3  Parallel QP Decomposition Strategies__

__3.1  Strategy 1: Serial Relaxation (Gauss-Seidel DMPC)__

The classical DMPC approach solves local QPs sequentially in upstream-to-downstream order:

$$
\Delta u_i^{(\ell+1)} = \arg\min_{\Delta u_i} J_i(\Delta u_i; \Delta u_{i-1}^{(\ell+1)}, \Delta u_{i+1}^{(\ell)}) \quad \text{s.t.} \quad g_i(\Delta u_i) \leq 0 \tag{11}
$$

where superscript $(\ell)$ denotes the outer iteration index and $J_i$ is the local cost including coupling terms from neighbors. This Gauss-Seidel iteration uses the most recent information from upstream (iteration $\ell+1$) and the previous iterate from downstream (iteration $\ell$).

**Theorem 1** (Convergence of serial relaxation). *For the water network QP (Eq. 7) with coupling strength $\kappa < 1$, the serial relaxation iteration (Eq. 11) converges to the centralized optimum at rate $\rho_{\text{GS}} \leq \kappa^2$.*

*Proof sketch*. The iteration matrix for the Gauss-Seidel splitting of $\mathbf{H}$ has spectral radius bounded by $\kappa^2$ (Bertsekas & Tsitsiklis, 1989, Proposition 2.3). Since $\kappa < 0.3$ for typical water networks, $\rho_{\text{GS}} < 0.09$, giving rapid convergence (3–5 iterations).  $\square$

Serial relaxation achieves excellent convergence (fewest outer iterations) but does not exploit parallelism: computation time per outer iteration is $N_p \cdot T_{\text{QP}}$.

__3.2  Strategy 2: Jacobi Parallel DMPC__

The Jacobi strategy solves all local QPs simultaneously using the previous iteration's neighbor values:

$$
\Delta u_i^{(\ell+1)} = \arg\min_{\Delta u_i} J_i(\Delta u_i; \Delta u_{i-1}^{(\ell)}, \Delta u_{i+1}^{(\ell)}) \quad \forall i \in \{1, \ldots, N_p\} \tag{12}
$$

All $N_p$ QPs can be solved concurrently, reducing computation time per outer iteration to $T_{\text{QP}}$ (on $N_p$ cores) or $\lceil N_p / P \rceil \cdot T_{\text{QP}}$ (on $P < N_p$ cores).

**Theorem 2** (Convergence of Jacobi parallel DMPC). *For the water network QP with coupling strength $\kappa < 1/\sqrt{2}$, the Jacobi iteration (Eq. 12) converges at rate $\rho_J \leq 2\kappa^2$.*

*Proof sketch*. The Jacobi splitting $\mathbf{H} = \mathbf{D} - (\mathbf{L} + \mathbf{U})$ yields iteration matrix $\mathbf{M}_J = \mathbf{D}^{-1}(\mathbf{L} + \mathbf{U})$. For tridiagonal coupling, $\rho(\mathbf{M}_J) \leq 2\kappa^2$ (Varga, 2000, Theorem 3.4). Since $\kappa < 0.3$, $\rho_J < 0.18$, ensuring convergence in 5–8 iterations.  $\square$

The Jacobi strategy trades convergence speed (more outer iterations) for parallelism. The net speedup over serial relaxation depends on the ratio of QP solve time to communication time.

__3.3  Strategy 3: ADMM Consensus__

The Alternating Direction Method of Multipliers (ADMM) introduces consensus constraints on shared boundary variables:

$$
\min_{\Delta u_i, z_{ij}} \sum_{i=1}^{N_p} J_i(\Delta u_i) \quad \text{s.t.} \quad \Delta u_i^{\text{dn}} = z_{ij}, \quad \Delta u_j^{\text{up}} = z_{ij} \quad \forall (i,j) \in \mathcal{E} \tag{13}
$$

where $z_{ij}$ is the consensus variable for the shared gate between pools $i$ and $j$. The augmented Lagrangian is:

$$
\mathcal{L}_\rho = \sum_{i=1}^{N_p} J_i(\Delta u_i) + \sum_{(i,j) \in \mathcal{E}} \left[ \lambda_{ij}^T (\Delta u_i^{\text{dn}} - z_{ij}) + \frac{\rho}{2} \|\Delta u_i^{\text{dn}} - z_{ij}\|^2 \right] \tag{14}
$$

The ADMM iteration alternates between:

**Step 1** (parallel local QPs):
$$
\Delta u_i^{(\ell+1)} = \arg\min_{\Delta u_i} J_i(\Delta u_i) + \frac{\rho}{2} \|\Delta u_i^{\text{dn}} - z_{ij}^{(\ell)} + \mu_{ij}^{(\ell)}\|^2 \quad \forall i \tag{15}
$$

**Step 2** (consensus update):
$$
z_{ij}^{(\ell+1)} = \frac{1}{2} \left( \Delta u_i^{\text{dn},(\ell+1)} + \Delta u_j^{\text{up},(\ell+1)} \right) + \frac{1}{2} \left( \mu_{ij}^{(\ell)} + \mu_{ji}^{(\ell)} \right) \tag{16}
$$

**Step 3** (dual update):
$$
\mu_{ij}^{(\ell+1)} = \mu_{ij}^{(\ell)} + \Delta u_i^{\text{dn},(\ell+1)} - z_{ij}^{(\ell+1)} \tag{17}
$$

**Theorem 3** (ADMM convergence). *For the water network QP with positive definite local Hessians $H_i \succ 0$ and ADMM penalty $\rho > 0$, the ADMM iteration (Eqs. 15–17) converges to the centralized optimum. The optimal penalty is $\rho^* = \sqrt{\lambda_{\min}(H_i) \cdot \lambda_{\max}(H_i)}$.*

*Proof*. Follows from Boyd et al. (2011, §3.2) applied to the convex QP. The water network QP has $H_i \succ 0$ because $R_i \succ 0$ (control effort penalty is positive definite). The optimal $\rho$ minimizes the condition number of the augmented system (Ghadimi et al., 2015).  $\square$

ADMM combines parallelism (Step 1 is fully parallel) with robust convergence (guaranteed for any $\rho > 0$, though convergence rate depends on $\rho$ tuning).

__3.4  Communication-Aware Core Mapping__

Given $P$ processor cores and $N_p$ pool agents, the core mapping assigns agents to cores to minimize inter-core communication. For serial canal topology, this reduces to a 1D partitioning problem:

$$
\text{minimize} \quad \sum_{c=1}^{P} \sum_{\substack{(i,j) \in \mathcal{E} \\ \pi(i) \neq \pi(j)}} w_{ij} \tag{18}
$$

where $\pi(i)$ is the core assignment of agent $i$ and $w_{ij}$ is the communication weight (proportional to the number of shared variables). For serial topology, the optimal mapping assigns contiguous blocks of $\lceil N_p / P \rceil$ pools to each core. For tree topologies, we use a recursive bisection based on the network adjacency graph (Karypis & Kumar, 1998).

__3.5  Warm-Starting and Early Termination__

Two practical accelerations reduce computation time:

1. **Warm-starting**: At sampling step $k$, the QP is initialized with the shifted solution from step $k-1$: $\Delta u_i^{(0)}(k) = [\Delta u_i^*(1|k-1), \ldots, \Delta u_i^*(N_u-1|k-1), 0]$. This reduces the mean number of active-set iterations from 8.3 to 3.1 (Table 5).

2. **Early termination**: The outer iteration terminates when the primal residual (boundary mismatch) falls below a threshold $\epsilon_p$:

$$
r_{\text{primal}} = \max_{(i,j) \in \mathcal{E}} |\Delta u_i^{\text{dn}} - \Delta u_j^{\text{up}}| < \epsilon_p \tag{19}
$$

For water networks, $\epsilon_p = 10^{-3}$ m$^3$/s (corresponding to <0.1 mm water level impact) provides sufficient accuracy with 30–50% fewer iterations than convergence to machine precision.

__3.6  Junction Handling for Branching Networks__

For tree (branching) topologies, junction nodes $j$ introduce multi-way coupling constraints. Define $\mathcal{U}(j) = \{i \in \mathcal{V} : (i,j) \in \mathcal{E}\}$ as the upstream pool set and $\mathcal{D}(j) = \{k \in \mathcal{V} : (j,k) \in \mathcal{E}\}$ as the downstream pool set. At junction $j$:

$$
\sum_{i \in \mathcal{U}(j)} Q_i^{\text{dn}} = \sum_{k \in \mathcal{D}(j)} Q_k^{\text{up}} \tag{20}
$$

$$
h_i^{\text{dn}} = h_j = h_k^{\text{up}} \quad \forall i \in \mathcal{U}(j), k \in \mathcal{D}(j) \tag{21}
$$

The ADMM consensus (Eq. 13) extends naturally: each junction introduces $m_j = |\mathcal{U}(j)| + |\mathcal{D}(j)| - 1$ additional consensus variables and dual multipliers. The consensus update (Step 2) becomes a weighted average over all pools connected at the junction. This preserves full parallelism of Step 1 (local QPs remain independent) at the cost of slightly more communication per iteration.

__4  Implementation__

__4.1  Software Architecture__

ParaQP is implemented in C++ with OpenMP for shared-memory parallelism. The architecture comprises three layers:

- **QP Engine**: Active-set solver for individual pool QPs, using fixed-size arrays (no dynamic allocation) compatible with real-time constraints. Based on the qpOASES parametric active-set algorithm (Ferreau et al., 2014) with modifications for bounded array sizes.

- **Coordination Layer**: Implements the three decomposition strategies (§3.1–3.3) with configurable convergence criteria. ADMM penalty $\rho$ is auto-tuned using the spectral method of Wohlberg (2017). Comparison of auto-tuned $\rho$, fixed $\rho$ (from theory), and oracle-optimal $\rho$ (grid search over 100 values) shows that auto-tuning achieves within 8% of oracle-optimal wall-clock time, while fixed $\rho$ is within 15%. Auto-tuning is recommended as default.

- **Communication Layer**: Inter-core data exchange via shared memory (OpenMP) or MPI for distributed systems. Message size: 2 doubles per shared gate per iteration (flow and water level). All inter-agent communication uses TLS-encrypted channels when deployed on networked hardware (Profinet/EtherNet/IP); the ODD Monitor (Chen et al., 2026b) can detect anomalous boundary values potentially caused by data integrity issues.

__4.2  Hardware Platforms__

Three target platforms are evaluated:

| Platform | Cores | Clock (GHz) | Memory | Use Case |
|----------|-------|-------------|--------|----------|
| Siemens S7-1516 PLC | 2 | 0.6 | 1 MB | Field deployment (baseline) |
| Beckhoff CX2062 IPC | 16 | 2.1 | 8 GB | Edge computing |
| Intel Xeon 8358 | 32 | 2.6 | 128 GB | Central control room |

The Beckhoff CX2062 industrial PC is the primary target for ParaQP, as it provides 16 cores in a DIN-rail-mount form factor suitable for control room installation. The Siemens S7-1516 serves as the sequential baseline (HydroRTP-generated code, single-core execution).

__4.3  Integration with CHS Tool Chain__

ParaQP integrates with the CHS tool chain at two levels:

1. **HydroRTP integration** (Yin et al., 2026): The ParaQP solver is available as a Simulink S-function block in HydroRTP v1.2. Code generation produces multi-threaded C code with OpenMP pragmas, targeting the Beckhoff CX2062 via TwinCAT 3 runtime.

2. **cuSVE integration** (Huang et al., 2026): For SiL verification, ParaQP runs the DMPC controller while cuSVE provides the plant simulation at full Saint-Venant fidelity. The GPU solver's 210,000× real-time factor ensures that verification runs complete in seconds rather than hours.

__5  Benchmark Results__

__5.1  Benchmark Systems__

Four benchmark systems of increasing complexity are used:

**B1 — 3-pool laboratory flume** (Su et al., 2026): Three cascaded rectangular channels (4.0 m × 0.3 m × 0.5 m each) with motorized sluice gates. IDZ parameters from Su et al. (2026). DMPC: $N_h = 10$, $N_u = 3$, $\Delta t = 10$ s.

**B2 — 10-pool Jiaodong irrigation district**: Ten trapezoidal canal pools (total 42 km) from the Jiaodong Water Transfer Project. Pool lengths 2.8–6.2 km, design flow 15 m$^3$/s. DMPC: $N_h = 20$, $N_u = 5$, $\Delta t = 60$ s.

**B3 — 30-pool branching network**: Synthetic network with main canal (20 pools) and two lateral branches (5 pools each), 4 junctions. Pool lengths 3–8 km. DMPC: $N_h = 20$, $N_u = 5$, $\Delta t = 60$ s.

**B4 — 50-pool South-to-North proxy**: Based on the Middle Route of South-to-North Water Diversion Project geometry. Fifty pools (total 680 km), pool lengths 4–28 km, design flow 70–120 m$^3$/s. DMPC: $N_h = 30$, $N_u = 8$, $\Delta t = 60$ s.

__5.2  Convergence Comparison__

__*Table 1. Outer Iteration Count (Mean ± Std, 500 Sampling Steps)*__

| System | $\kappa$ | Serial (GS) | Jacobi | ADMM ($\rho = \rho^*$) |
|--------|----------|-------------|--------|----------------------|
| B1 (3-pool) | 0.08 | 2.1 ± 0.3 | 3.4 ± 0.5 | 4.2 ± 0.6 |
| B2 (10-pool) | 0.14 | 3.2 ± 0.4 | 5.8 ± 0.7 | 6.5 ± 0.9 |
| B3 (30-pool) | 0.18 | 3.8 ± 0.5 | 7.2 ± 0.8 | 8.3 ± 1.1 |
| B4 (50-pool) | 0.22 | 4.1 ± 0.6 | 8.6 ± 1.0 | 9.8 ± 1.3 |

Serial relaxation converges fastest (fewest iterations) because it uses the most recent upstream information. Jacobi requires 70–110% more iterations but executes each iteration in parallel. ADMM requires the most iterations but guarantees convergence without the coupling strength restriction $\kappa < 1/\sqrt{2}$ needed by Jacobi.

__*Table 12. Theoretical vs. Observed Convergence Rates*__

| System | $\kappa$ | $\rho_{\text{GS,theory}}$ | $\rho_{\text{GS,observed}}$ | $\rho_{J,\text{theory}}$ | $\rho_{J,\text{observed}}$ |
|--------|---------|--------------------------|----------------------------|--------------------------|---------------------------|
| B1 | 0.08 | 0.006 | 0.004 | 0.013 | 0.009 |
| B2 | 0.14 | 0.020 | 0.015 | 0.039 | 0.028 |
| B3 | 0.18 | 0.032 | 0.026 | 0.065 | 0.048 |
| B4 | 0.22 | 0.048 | 0.038 | 0.097 | 0.072 |

Observed convergence rates are consistently 20–30% below the theoretical bounds ($\rho_{\text{GS}} = \kappa^2$, $\rho_J = 2\kappa^2$), confirming that the bounds are conservative but informative for practitioners selecting a decomposition strategy.

__5.3  Wall-Clock Time and Speedup__

__*Table 2. DMPC Computation Time (ms) on Beckhoff CX2062 (16 cores)*__

| System | Sequential (1 core) | Serial GS | Jacobi (16 cores) | ADMM (16 cores) |
|--------|--------------------|-----------|--------------------|-----------------|
| B1 (3-pool) | 12.4 | 12.4 | 4.8 | 6.2 |
| B2 (10-pool) | 180 | 180 | 42 | 56 |
| B3 (30-pool) | 1,420 | 1,420 | 148 | 186 |
| B4 (50-pool) | 4,810 | 4,810 | 262 | 340 |

__*Table 3. Speedup over Sequential DMPC*__

| System | Jacobi | ADMM | Ideal ($N_p$ cores) |
|--------|--------|------|---------------------|
| B1 (3-pool) | 2.6× | 2.0× | 3.0× |
| B2 (10-pool) | 4.3× | 3.2× | 10.0× |
| B3 (30-pool) | 9.6× | 7.6× | 30.0× |
| B4 (50-pool) | 18.4× | 14.1× | 50.0× |

The Jacobi strategy consistently outperforms ADMM in wall-clock time despite requiring more outer iterations, because each iteration is fully parallel (no sequential consensus step). The sub-linear speedup relative to ideal is caused by: (a) communication overhead between cores (15–25% of total time for B4), (b) load imbalance from variable pool sizes, and (c) the additional outer iterations compared to serial execution.

__5.4  Real-Time Feasibility__

__*Table 4. Real-Time Feasibility Assessment*__

| System | $\Delta t$ (s) | $T_{\text{seq}}$ (ms) | $T_{\text{Jacobi}}$ (ms) | Margin | Feasible? |
|--------|---------------|----------------------|--------------------------|--------|-----------|
| B1 (3-pool) | 10 | 12.4 | 4.8 | 99.95% | Yes |
| B2 (10-pool) | 60 | 180 | 42 | 99.93% | Yes |
| B3 (30-pool) | 60 | 1,420 | 148 | 99.75% | Yes |
| B4 (50-pool) | 60 | 4,810 | 262 | 99.56% | Yes |

All systems are real-time feasible with Jacobi parallel DMPC. The 50-pool system uses only 0.44% of the sampling interval, leaving ample margin for communication, I/O, and other tasks.

__5.5  Warm-Start Effectiveness__

__*Table 5. Effect of Warm-Starting (B4, Jacobi Strategy)*__

| Metric | Cold Start | Warm Start | Improvement |
|--------|-----------|------------|-------------|
| Active-set iterations per QP | 8.3 ± 2.1 | 3.1 ± 0.8 | 63% fewer |
| Outer iterations | 8.6 ± 1.0 | 6.2 ± 0.7 | 28% fewer |
| Wall-clock time (ms) | 262 | 164 | 37% faster |

Warm-starting significantly reduces computation by providing a near-optimal initial point. The warm-started Jacobi DMPC for 50 pools completes in 164 ms—a 29.3× speedup over sequential cold-start execution.

__5.6  Control Performance Comparison__

To verify that parallel decomposition does not degrade control quality, we compare ParaQP (Jacobi) against centralized MPC (single QP solving the full problem) on benchmark B2 (10-pool Jiaodong) for a 24-hour scenario including step changes, disturbance rejection, and gate maintenance events.

__*Table 6. Control Performance: ParaQP Jacobi vs. Centralized MPC (B2)*__

| Metric | Centralized MPC | ParaQP Jacobi | Difference |
|--------|----------------|---------------|------------|
| Mean RMSE (mm) | 8.2 | 8.6 | +0.4 |
| Max deviation (mm) | 42.1 | 43.5 | +1.4 |
| Settling time (s) | 240 | 248 | +8 |
| Constraint violations | 0 | 0 | 0 |
| Total gate movement (m) | 14.8 | 15.1 | +2.0% |
| Computation time (ms) | 3,200 | 42 | −98.7% |

The control performance difference is negligible: 0.4 mm RMSE increase corresponds to 4.9% degradation, well within the uncertainty of the IDZ model itself.

__5.7  SiL Verification with cuSVE__

ParaQP is coupled with the cuSVE GPU solver (Huang et al., 2026) for Software-in-the-Loop verification at full Saint-Venant fidelity.

__*Table 7. SiL Verification: ParaQP + cuSVE (B4, 50-pool, 24-hour scenario)*__

| Metric | IDZ model (ParaQP) | SVE model (ParaQP + cuSVE) | Difference |
|--------|--------------------|-----------------------------|------------|
| Mean RMSE (mm) | 8.6 | 12.4 | +3.8 |
| Max deviation (mm) | 43.5 | 58.2 | +14.7 |
| Settling time (s) | 248 | 285 | +37 |
| Constraint violations | 0 | 0 | 0 |
| SiL execution time (s) | — | 0.41 | — |
| Real-time factor | — | 210,000× | — |

The IDZ-to-SVE degradation (3.8 mm RMSE increase) is consistent with the known linearization error of the IDZ model for large flow excursions. No constraint violations occur, confirming that the safety margins in the ODD formulation (Chen et al., 2026b) adequately account for model mismatch.

__5.8  Resource Utilization__

__*Table 8. Resource Utilization on Beckhoff CX2062 (16-core)*__

| System | RAM/agent (KB) | Total RAM (MB) | CPU util. (%) | QP solve (%) | Comm (%) | Overhead (%) |
|--------|---------------|----------------|--------------|-------------|---------|-------------|
| B1 (3) | 48 | 0.14 | 0.05 | 78 | 12 | 10 |
| B2 (10) | 52 | 0.52 | 0.07 | 72 | 18 | 10 |
| B3 (30) | 56 | 1.68 | 0.25 | 68 | 22 | 10 |
| B4 (50) | 64 | 3.2 | 0.44 | 65 | 25 | 10 |

Memory footprint is minimal: even the 50-pool system requires only 3.2 MB of RAM, well within the CX2062's 8 GB capacity.

__*Table 13. Energy per DMPC Cycle (mJ/cycle)*__

| Platform | B2 (10-pool) | B4 (50-pool) |
|----------|-------------|-------------|
| S7-1516 (1-core, 12 W) | 108 | 2,886 |
| CX2062 (16-core, 28 W) | 1.18 | 7.33 |
| Xeon 8358 (32-core, 205 W) | 4.60 | 28.6 |

The CX2062 is the most energy-efficient per DMPC cycle due to lower idle power and efficient multi-core utilization. For solar-powered remote sites with 50 W panels, the CX2062's ParaQP overhead (0.07 W incremental for B4 at 0.44% CPU utilization) represents 0.14% of available power—negligible for off-grid installations.

__5.9  Scaling Analysis__

__*Table 9. Scaling of Jacobi ParaQP on 16-Core CX2062*__

| Pools | QPs per core | Wall time (ms) | Speedup vs. seq. | Parallel efficiency |
|-------|-------------|----------------|-------------------|---------------------|
| 3 | 1 | 4.8 | 2.6× | 87% |
| 10 | 1 | 42 | 4.3× | 43% |
| 16 | 1 | 68 | 5.8× | 36% |
| 30 | 2 | 148 | 9.6× | 32% |
| 50 | 4 | 262 | 18.4× | 37% |
| 100 | 7 | 580 | 31.2× | 31% |

Parallel efficiency decreases as the number of pools per core increases (due to sequential execution within each core) and as inter-core communication grows. For the 100-pool system, the 580 ms wall-clock time remains well within the 60 s sampling interval.

__5.10  Comparison with General-Purpose QP Solvers__

To assess ParaQP's competitiveness against established solvers, we compare on benchmark B4 (50-pool, 50 consecutive steps) using warm-starting where available.

__*Table 10. ParaQP vs. General-Purpose QP Solvers (B4, 50-pool)*__

| Solver | Wall time (ms) | Memory (MB) | Suboptimality | License |
|--------|---------------|-------------|---------------|---------|
| ParaQP Jacobi (16-core) | 164 | 3.2 | <10⁻⁶ | MIT |
| OSQP v0.6 (16-thread) | 210 | 18 | <10⁻⁴ | Apache-2.0 |
| Gurobi v11.0 (16-thread) | 142 | 86 | <10⁻⁸ | Commercial |
| qpOASES v3.1 (1-thread) | 4,810 | 8 | <10⁻¹⁰ | LGPL |

ParaQP is 22% faster than OSQP and uses 5.6× less memory, due to domain-specific warm-starting and the fixed-size array QP engine. Gurobi is 13% faster than ParaQP but requires 27× more memory and a commercial license (~$12,000/yr for a 16-core server). ParaQP's key advantages for water network deployment are: (a) fixed memory footprint suitable for embedded IPCs, (b) bounded worst-case execution time (no dynamic allocation), and (c) MIT license enabling unrestricted field deployment.

__5.11  Hardware-in-the-Loop Validation__

To bridge the gap between simulation and field deployment, ParaQP was tested in a hardware-in-the-loop (HiL) configuration: the Beckhoff CX2062 running ParaQP controlled the 3-pool laboratory flume (Su et al., 2026) via Profinet. The test scenario included step changes, disturbance rejection, and a 30-s communication dropout.

__*Table 11. HiL Validation Results (B1, 3-Pool Flume, 2-Hour Test)*__

| Metric | SiL (ParaQP + IDZ) | HiL (ParaQP + Flume) | Difference |
|--------|--------------------|-----------------------|------------|
| Mean RMSE (mm) | 4.0 | 4.3 | +0.3 |
| Max overshoot (mm) | 6.4 | 7.1 | +0.7 |
| Settling time (s) | 86 | 90 | +4 |
| DMPC computation (ms) | 4.8 | 4.6 | −0.2 |
| Constraint violations | 0 | 0 | 0 |

The SiL-to-HiL degradation is minimal (0.3 mm RMSE), consistent with sensor noise and unmodeled dynamics. Computation time on the CX2062 (4.6 ms) is slightly lower than SiL due to reduced logging overhead. Full field deployment on the Jiaodong 10-pool canal is planned for Q4 2026 and will be reported in a follow-up paper.

__6  Discussion__

__6.1  Strategy Selection Guidelines__

Based on the benchmark results, we recommend:

- **Serial relaxation (GS)**: Best for systems with ≤5 pools where single-core execution is sufficient and convergence speed is paramount. Also preferred when only 2-core hardware is available.

- **Jacobi parallel**: Best for systems with >10 pools on multi-core hardware (≥4 cores). Provides the fastest wall-clock time despite requiring more outer iterations. Recommended as the default for CHS Edge Agent deployments.

- **ADMM consensus**: Best for systems with strong coupling ($\kappa > 0.3$) where Jacobi convergence may be slow, or for heterogeneous networks where different pools use different model types. ADMM's guaranteed convergence makes it the most robust option.

__6.2  Comparison with Existing Approaches__

Negenborn et al. (2009) applied serial DMPC to a 4-pool canal system with 3.2 s computation time on a desktop PC. ParaQP's Jacobi strategy solves the 3-pool benchmark (comparable complexity) in 4.8 ms—a 667× improvement due to (a) active-set solver efficiency, (b) warm-starting, and (c) parallel execution.

Lemos et al. (2012) proposed cooperative DMPC for irrigation canals but did not address parallel computation. Their sequential solver achieved 15–20 outer iterations for convergence; ParaQP's ADMM achieves 4–10 iterations with similar control quality, due to the optimal penalty tuning.

Zheng et al. (2021) applied ADMM to water distribution network optimization but focused on steady-state problems (not MPC). ParaQP extends ADMM to the dynamic MPC setting with warm-starting and early termination specific to water conveyance control.

Conte et al. (2016) developed distributed MPC for water networks with constraint tightening for robustness. ParaQP complements this approach by providing the parallel computational engine needed to scale their formulation beyond small systems.

__6.3  Limitations and Future Work__

1. **Looped networks**: The current decomposition assumes tree topology. Urban water distribution networks with loops require additional cycle-breaking constraints or a graph-cut decomposition (addressed in HZF-3, planned).

2. **Nonlinear MPC**: ParaQP assumes a QP (linear MPC with quadratic cost). Extension to nonlinear MPC (e.g., for large flow excursions beyond the IDZ validity range) requires sequential quadratic programming (SQP) within each agent—a planned v2.0 feature.

3. **GPU acceleration**: The current implementation uses CPU multi-threading (OpenMP). Porting the active-set solver to CUDA could provide additional speedup for systems with >100 pools, leveraging the same GPU already used by cuSVE.

4. **Field deployment**: ParaQP has been validated in HiL on the 3-pool flume but not yet deployed on a full-scale canal system. Field validation on the Jiaodong 10-pool canal is planned for Q4 2026.

__6.4  Integration Roadmap__

ParaQP is positioned within the CHS algorithmic tool chain:

- **Upstream**: Plant models from HydroComponents (Bai et al., 2026) → IDZ identification → QP matrices
- **Parallel**: cuSVE (Huang et al., 2026) provides high-fidelity plant simulation for SiL verification
- **Downstream**: HydroRTP (Yin et al., 2026) generates PLC/IPC code from the Simulink model containing ParaQP blocks
- **Future**: HZF-3 will integrate ParaQP into a graph-topology-aware digital twin engine with GPU acceleration

__6.5  Fault Tolerance and Graceful Degradation__

Real water networks experience hardware failures, communication disruptions, and sensor faults. ParaQP addresses three failure scenarios:

**Core failure**: If core $c$ crashes mid-computation, the coordination layer detects the timeout (2× expected QP solve time) and reassigns the affected pools to surviving cores. The worst-case reassignment adds up to 40% computation time to remaining cores. During reassignment (≤1 sampling step), affected pools hold their last computed gate command. Testing on B4 shows that the system remains real-time feasible with up to 4 of 16 core failures ($T_{\text{Jacobi}}$ increases from 262 ms to 436 ms, still well within the 60 s interval).

**Communication loss**: If inter-agent communication is lost between pools $i$ and $i+1$, each pool substitutes the predicted boundary flow from its local IDZ model: $\hat{d}_{i+1}^{\text{up}} = f_{\text{gate}}(u_i^{\text{dn},*}, \hat{y}_i, \hat{y}_{i+1})$ using the last received state. Testing shows that 60-s communication loss causes <3 mm additional RMSE on B2, with full recovery within 2 sampling steps after restoration.

**Sensor fault**: Detected by the ODD Monitor (Chen et al., 2026b) when $\rho(\mathbf{x}) < \rho_{\text{WARNING}}$. The affected pool reverts to open-loop steady-state control while the fault is isolated. ParaQP continues solving the remaining pools' QPs in parallel, treating the faulted pool's gate as a fixed disturbance.

__6.6  ParaQP vs. Neural MPC Approximations__

Recent work on neural network-based approximate MPC (Karg & Lucia, 2020; Chen et al., 2022) offers microsecond-level inference by learning the QP solution as a function of the current state. While attractive for computation speed, QP-based DMPC remains preferable for water networks in several respects:

1. **Hard constraint satisfaction**: QP solvers guarantee constraint satisfaction by construction. Neural MPC requires additional safety layers (projection onto feasible sets, control barrier functions) that add complexity and partially negate the speed advantage.

2. **Out-of-distribution robustness**: Neural MPC performance degrades for operating conditions not well represented in training data. Water networks experience rare events (flash floods, equipment failure, emergency drawdowns) where QP-based MPC maintains its optimization guarantees while neural approximations may produce infeasible or suboptimal actions.

3. **Interpretability**: QP solutions can be traced through the active-set iterations, enabling root-cause analysis of control decisions—essential for water utility regulatory compliance and incident investigation.

4. **Hybrid architecture (planned)**: A promising approach combines neural and QP solvers: a lightweight neural network provides the warm-start point for the QP solver, reducing active-set iterations from 8.3 to an estimated 1.5 while maintaining full constraint guarantees. This neural warm-start architecture is planned for ParaQP v2.0.

__6.7  Heterogeneous Agent Support__

Real water networks may contain pools with different model structures. ParaQP supports heterogeneity at two levels:

- **Variable QP dimensions**: Each agent can have different $N_u$ and $N_h$ values, as only the local Hessian $H_i$ and constraint matrix $G_i$ are affected. The block-separable structure (Eq. 8) is preserved regardless of individual block dimensions.

- **Mixed model families**: Family α (integrating, e.g., open canal pools) and Family β (self-regulating, e.g., pressurized pipes) pools can coexist in the same network. The convergence proofs (Theorems 1–3) depend only on the coupling strength $\kappa$ (Eq. 9) and the positive definiteness of local Hessians $H_i \succ 0$, both of which hold for either model family with $R_i > 0$.

Two aspects are not yet supported: (a) mixed sampling rates, where different agents operate at different $\Delta t$—a multi-rate DMPC extension using hierarchical ADMM is under development; and (b) highly nonlinear gate hydraulics (e.g., submerged vs. free-flow transitions) that would require an SQP wrapper around the local QP—planned for v2.0 alongside the neural warm-start.

__7  Conclusions__

This paper presents ParaQP, a parallel QP solver architecture for Distributed Model Predictive Control of water conveyance networks. Three decomposition strategies—serial relaxation, Jacobi parallel, and ADMM consensus—are developed with formal convergence guarantees exploiting the block-separable structure of water network optimization problems. Benchmarking on systems from 3 to 50 pools demonstrates that:

1. Jacobi parallel DMPC achieves 18.4× speedup over sequential execution on a 16-core industrial PC, reducing worst-case computation time from 4.8 s to 262 ms for the 50-pool system.

2. Control performance degradation relative to centralized MPC is negligible (0.4 mm RMSE increase, no constraint violations), confirming that the decomposition preserves control quality.

3. Warm-starting reduces computation by an additional 37%, achieving 164 ms for 50 pools.

4. ParaQP is competitive with Gurobi (13% slower) while using 27× less memory and requiring no commercial license.

5. Hardware-in-the-loop validation on a 3-pool flume confirms 4.3 mm RMSE with 4.6 ms computation time.

6. SiL verification with cuSVE at full Saint-Venant fidelity confirms robustness to model mismatch (3.8 mm additional RMSE, zero constraint violations).

7. Graceful degradation under core failure, communication loss, and sensor faults maintains real-time feasibility.

ParaQP enables real-time DMPC deployment for water networks up to 100 pools on commercially available industrial PCs, removing the computational bottleneck that has limited practical adoption of distributed control in the water sector.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]). The authors thank Su Chao for providing the 3-pool flume experimental data and the Jiaodong Water Transfer Authority for field data access.

__Data Availability__

ParaQP source code is available at https://github.com/IWHR-CHS/ParaQP under MIT license. The Zenodo archive (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance) includes: (a) ParaQP C++ source code, (b) all four benchmark models (Simulink + JSON configurations), (c) Python scripts to reproduce all tables and figures, and (d) a Docker container for dependency-free execution.

__References__

Bai, Y., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for multi-fidelity water system modeling. Environmental Modelling & Software (submitted).

Bertsekas, D. P., & Tsitsiklis, J. N. (1989). Parallel and Distributed Computation: Numerical Methods. Prentice Hall.

Boyd, S., Parikh, N., Chu, E., Peleato, B., & Eckstein, J. (2011). Distributed optimization and statistical learning via the alternating direction method of multipliers. Foundations and Trends in Machine Learning, 3(1), 1–122.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Chen, Y., Shi, Y., & Zhang, B. (2022). Optimal control via neural networks: A convex approach. In International Conference on Learning Representations (ICLR).

Christofides, P. D., Scattolini, R., Muñoz de la Peña, D., & Liu, J. (2013). Distributed model predictive control: A tutorial review and future research directions. Computers & Chemical Engineering, 51, 21–41.

Conte, C., Voellmy, N., Zeilinger, M. N., Morari, M., & Jones, C. N. (2016). Distributed synthesis and stability of cooperative distributed model predictive control for linear systems. Automatica, 69, 117–125.

Ferreau, H. J., Kirches, C., Potschka, A., Bock, H. G., & Diehl, M. (2014). qpOASES: A parametric active-set algorithm for quadratic programming. Mathematical Programming Computation, 6(4), 327–363.

Ghadimi, E., Teixeira, A., Shames, I., & Johansson, M. (2015). Optimal parameter selection for the alternating direction method of multipliers (ADMM). IEEE Transactions on Signal Processing, 63(9), 2265–2278.

Gurobi Optimization. (2024). Gurobi Optimizer Reference Manual. https://www.gurobi.com

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

Karg, B., & Lucia, S. (2020). Efficient representation and approximation of model predictive control laws via deep learning. IEEE Transactions on Cybernetics, 50(9), 3866–3878.

Karypis, G., & Kumar, V. (1998). A fast and high quality multilevel scheme for partitioning irregular graphs. SIAM Journal on Scientific Computing, 20(1), 359–392.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Lemos, J. M., Rato, L. M., & Rijo, M. (2012). Distributed model predictive control of irrigation canals. In Distributed Model Predictive Control Made Easy (pp. 429–444). Springer.

Litrico, X., & Fromion, V. (2009). Modeling and Control of Hydrosystems. Springer.

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Negenborn, R. R., van Overloop, P.-J., Keviczky, T., & De Schutter, B. (2009). Distributed model predictive control of irrigation canals. Networks and Heterogeneous Media, 4(2), 359–380.

Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017). Model Predictive Control: Theory, Computation, and Design (2nd ed.). Nob Hill Publishing.

Riverso, S., Farina, M., & Ferrari-Trecate, G. (2013). Plug-and-play decentralized model predictive control for linear systems. IEEE Transactions on Automatic Control, 58(10), 2608–2614.

Scattolini, R. (2009). Architectures for distributed and hierarchical model predictive control—A review. Journal of Process Control, 19(5), 723–731.

Schuurmans, J., Clemmens, A. J., Dijkstra, S., Hof, A., & Brouwer, R. (1999). Modeling of irrigation and drainage canals for controller design. Journal of Irrigation and Drainage Engineering, 125(6), 338–344.

Stellato, B., Banjac, G., Goulart, P., Bemporad, A., & Boyd, S. (2020). OSQP: An operator splitting solver for quadratic programs. Mathematical Programming Computation, 12(4), 637–672.

Stewart, B. T., Venkat, A. N., Rawlings, J. B., Wright, S. J., & Pannocchia, G. (2010). Cooperative distributed model predictive control. Systems & Control Letters, 59(8), 460–469.

Su, C., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). Experimental verification of the CHS unified transfer function family and distributed MPC on a multi-pool laboratory flume. Journal of Irrigation and Drainage Engineering (submitted).

Trodden, P., & Richards, A. (2013). Cooperative distributed MPC of linear systems with coupled constraints. Automatica, 49(2), 479–487.

van Overloop, P. J. (2006). Model Predictive Control on Open Water Systems (Doctoral dissertation). Delft University of Technology.

Varga, R. S. (2000). Matrix Iterative Analysis (2nd ed.). Springer.

Wohlberg, B. (2017). ADMM penalty parameter selection by residual balancing. arXiv:1704.06209.

Yin, B., Lei, X., Bai, Y., Ji, C., & Wang, H. (2026). HydroRTP: Simulink rapid prototyping toolbox for automatic code generation of water network controllers. SoftwareX (submitted).

Zheng, F., Zecchin, A. C., Maier, H. R., & Simpson, A. R. (2021). Decomposition and ADMM for real-time optimal operation of water distribution systems. Water Resources Research, 57(3), e2020WR028813.

__Figure Captions__

__Figure 1.__ Block-separable structure of the DMPC Hessian matrix. (a) Centralized QP Hessian showing block-tridiagonal structure for serial canal topology. (b) Decomposition into local QPs with coupling terms. (c) Communication graph: each pool agent exchanges boundary flow and water level with adjacent neighbors.

__Figure 2.__ Convergence comparison of three decomposition strategies on B4 (50-pool). (a) Primal residual vs. outer iteration. (b) Objective function gap vs. outer iteration. (c) Wall-clock time vs. outer iteration (Jacobi/ADMM parallel on 16 cores, serial GS sequential).

__Figure 3.__ Control performance comparison on B2 (10-pool Jiaodong, 24-hour scenario). (a) Water level tracking: centralized MPC (blue dashed) vs. ParaQP Jacobi (red solid) for pools 1, 5, 10. (b) Gate flow trajectories. (c) Residual (ParaQP − centralized) showing <0.5 mm difference.

__Figure 4.__ Speedup scaling on Beckhoff CX2062 (16 cores). (a) Wall-clock time vs. pool count for three strategies. (b) Speedup vs. pool count. (c) Parallel efficiency vs. pool count.

__Figure 5.__ SiL verification with cuSVE. (a) Architecture: ParaQP DMPC controller coupled with cuSVE Saint-Venant plant model. (b) Water level comparison for B4 pool 25: IDZ prediction model (green dashed) vs. SVE verification (red solid). (c) Control action computed by ParaQP under both models.

__Figure 6.__ Coupling strength $\kappa$ as a function of pool length $L$. Parameters: bottom width $B = 5$ m, $A_s = B \cdot L$; gate linearization coefficient $\alpha = 0.04$ m²/s; tracking-to-control weight ratio $Q_i/R_i = 10$; $\Delta t = 60$ s. Dashed lines indicate convergence thresholds for Jacobi ($\kappa < 1/\sqrt{2} \approx 0.71$) and serial relaxation ($\kappa < 1$). Pools longer than 5 km have $\kappa < 0.1$; pools shorter than 2 km have $\kappa > 0.3$ (ADMM recommended).
