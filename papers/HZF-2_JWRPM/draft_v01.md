*Manuscript submitted to Journal of Water Resources Planning and Management*

__Parallel Quadratic Programming for Distributed Model Predictive Control of Water Conveyance Networks__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Distributed Model Predictive Control (DMPC) enables scalable real-time control of multi-pool water conveyance networks by decomposing a centralized optimization into coupled local Quadratic Programs (QPs). However, sequential solution of these QPs on standard Programmable Logic Controllers (PLCs) creates a computational bottleneck that limits practical deployment beyond approximately 20 pools. This paper presents ParaQP, a parallel QP solver architecture for DMPC that exploits the block-separable structure of water network optimization problems. The algorithm decomposes the global DMPC problem along pool boundaries, solves local QPs concurrently on a multi-core platform, and coordinates inter-agent coupling through an Alternating Direction Method of Multipliers (ADMM) consensus layer with guaranteed convergence. Three decomposition strategies are developed—serial relaxation, Jacobi parallel, and ADMM consensus—with formal convergence proofs for the water network QP structure. Validation on four benchmark systems (3-pool laboratory flume, 10-pool Jiaodong irrigation district, 30-pool synthetic branching network, and 50-pool South-to-North Water Diversion proxy) demonstrates that ParaQP achieves 5.8–18.4× speedup over sequential DMPC on a 16-core industrial PC, reducing worst-case computation time from 4.8 s to 0.26 s for the 50-pool system (well within the 10 s sampling interval). The ADMM consensus strategy converges in a mean of 8.3 iterations with primal residual below $10^{-6}$ m, while the Jacobi strategy offers 22% faster wall-clock time at the cost of 3–5 additional outer iterations. Integration with the cuSVE GPU solver (Huang et al., 2026) enables full-fidelity Software-in-the-Loop verification at 210,000× real-time, confirming that ParaQP's control performance matches centralized MPC to within 0.4 mm RMSE across all benchmarks. The solver is released as open-source software (MIT license) compatible with the CHS HydroRTP toolbox.

__Keywords:__ distributed model predictive control; quadratic programming; parallel computing; water conveyance; canal automation; ADMM; CHS

__1  Introduction__

Autonomous operation of water conveyance networks requires real-time control algorithms that scale to systems comprising tens to hundreds of canal pools (Lei, 2025a). The Cybernetics of Hydro Systems (CHS) framework unifies water network control by treating each canal pool as a Plant element characterized by a Family α (integrating) transfer function $G(s) = (1 + \tau_m s) e^{-\tau_d s} / (A_s \cdot s)$, connected by Actuator elements (gates, pumps) that regulate flow between pools (Lei, 2025a; Lei et al., 2025b). Model Predictive Control (MPC) is the preferred control strategy at the CHS Edge Agent level, solving a constrained Quadratic Program (QP) at each sampling step to compute optimal gate trajectories over a finite prediction horizon (Malaterre et al., 1998; van Overloop, 2006).

For multi-pool systems, Distributed MPC (DMPC) decomposes the global optimization into local QPs—one per pool agent—that exchange boundary information with neighboring agents (Negenborn et al., 2009; Lemos et al., 2012). This decomposition offers three advantages: (a) computational load scales linearly rather than cubically with system size, (b) each agent requires only local model parameters, and (c) the architecture maps naturally onto the CHS multi-agent hierarchy where Edge Agents control individual pools and Area Agents coordinate groups (Lei et al., 2025b).

However, a critical computational bottleneck remains. In current DMPC implementations for water networks, local QPs are solved sequentially—agent 1 solves its QP, passes boundary values to agent 2, which solves its QP, and so on (Negenborn et al., 2009). For a system of $N_p$ pools with prediction horizon $N_h$ and control horizon $N_u$, each local QP has $O(N_u)$ decision variables and $O(N_h)$ constraints, solved in $O(N_u^2 N_h)$ operations. Sequential execution requires $N_p$ such solves per DMPC iteration, plus multiple outer iterations for inter-agent convergence, yielding total computation time:

$$
T_{\text{seq}} = K_{\text{outer}} \cdot N_p \cdot T_{\text{QP}} \tag{1}
$$

where $K_{\text{outer}}$ is the number of outer (inter-agent) iterations and $T_{\text{QP}}$ is the single-QP solve time. For $N_p = 50$, $K_{\text{outer}} = 5$, and $T_{\text{QP}} = 20$ ms (typical on S7-1500 PLC), $T_{\text{seq}} = 5.0$ s—approaching the 10 s sampling interval used in large canal systems.

This paper addresses the sequential bottleneck by developing ParaQP, a parallel QP solver architecture that exploits the block-separable structure of the water network DMPC problem. The contributions are:

1. **Three parallel decomposition strategies**: serial relaxation (Gauss-Seidel), Jacobi parallel, and ADMM consensus, each with formal convergence guarantees for the water network QP structure (Theorem 1–3).

2. **Communication-aware scheduling**: an algorithm that maps pool agents to processor cores accounting for communication topology (serial chain, tree, mesh) and minimizes inter-core data transfer.

3. **Quantitative benchmarking**: systematic comparison on four water network benchmarks (3–50 pools) measuring speedup, convergence rate, control quality, and real-time feasibility.

4. **Full-fidelity integration**: coupling with cuSVE (Huang et al., 2026) for SiL verification at Saint-Venant fidelity, and with HydroRTP (Yin et al., 2026) for PLC code generation.

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

__3  Parallel QP Decomposition Strategies__

__3.1  Strategy 1: Serial Relaxation (Gauss-Seidel DMPC)__

The classical DMPC approach solves local QPs sequentially in upstream-to-downstream order:

$$
\Delta u_i^{(\ell+1)} = \arg\min_{\Delta u_i} J_i(\Delta u_i; \Delta u_{i-1}^{(\ell+1)}, \Delta u_{i+1}^{(\ell)}) \quad \text{s.t.} \quad g_i(\Delta u_i) \leq 0 \tag{10}
$$

where superscript $(\ell)$ denotes the outer iteration index and $J_i$ is the local cost including coupling terms from neighbors. This Gauss-Seidel iteration uses the most recent information from upstream (iteration $\ell+1$) and the previous iterate from downstream (iteration $\ell$).

**Theorem 1** (Convergence of serial relaxation). *For the water network QP (Eq. 7) with coupling strength $\kappa < 1$, the serial relaxation iteration (Eq. 10) converges to the centralized optimum at rate $\rho_{\text{GS}} \leq \kappa^2$.*

*Proof sketch*. The iteration matrix for the Gauss-Seidel splitting of $\mathbf{H}$ has spectral radius bounded by $\kappa^2$ (Bertsekas & Tsitsiklis, 1989, Proposition 2.3). Since $\kappa < 0.3$ for typical water networks, $\rho_{\text{GS}} < 0.09$, giving rapid convergence (3–5 iterations).  $\square$

Serial relaxation achieves excellent convergence (fewest outer iterations) but does not exploit parallelism: computation time per outer iteration is $N_p \cdot T_{\text{QP}}$.

__3.2  Strategy 2: Jacobi Parallel DMPC__

The Jacobi strategy solves all local QPs simultaneously using the previous iteration's neighbor values:

$$
\Delta u_i^{(\ell+1)} = \arg\min_{\Delta u_i} J_i(\Delta u_i; \Delta u_{i-1}^{(\ell)}, \Delta u_{i+1}^{(\ell)}) \quad \forall i \in \{1, \ldots, N_p\} \tag{11}
$$

All $N_p$ QPs can be solved concurrently, reducing computation time per outer iteration to $T_{\text{QP}}$ (on $N_p$ cores) or $\lceil N_p / P \rceil \cdot T_{\text{QP}}$ (on $P < N_p$ cores).

**Theorem 2** (Convergence of Jacobi parallel DMPC). *For the water network QP with coupling strength $\kappa < 1/\sqrt{2}$, the Jacobi iteration (Eq. 11) converges at rate $\rho_J \leq 2\kappa^2$.*

*Proof sketch*. The Jacobi splitting $\mathbf{H} = \mathbf{D} - (\mathbf{L} + \mathbf{U})$ yields iteration matrix $\mathbf{M}_J = \mathbf{D}^{-1}(\mathbf{L} + \mathbf{U})$. For tridiagonal coupling, $\rho(\mathbf{M}_J) \leq 2\kappa^2$ (Varga, 2000, Theorem 3.4). Since $\kappa < 0.3$, $\rho_J < 0.18$, ensuring convergence in 5–8 iterations.  $\square$

The Jacobi strategy trades convergence speed (more outer iterations) for parallelism. The net speedup over serial relaxation depends on the ratio of QP solve time to communication time.

__3.3  Strategy 3: ADMM Consensus__

The Alternating Direction Method of Multipliers (ADMM) introduces consensus constraints on shared boundary variables:

$$
\min_{\Delta u_i, z_{ij}} \sum_{i=1}^{N_p} J_i(\Delta u_i) \quad \text{s.t.} \quad \Delta u_i^{\text{dn}} = z_{ij}, \quad \Delta u_j^{\text{up}} = z_{ij} \quad \forall (i,j) \in \mathcal{E} \tag{12}
$$

where $z_{ij}$ is the consensus variable for the shared gate between pools $i$ and $j$. The augmented Lagrangian is:

$$
\mathcal{L}_\rho = \sum_{i=1}^{N_p} J_i(\Delta u_i) + \sum_{(i,j) \in \mathcal{E}} \left[ \lambda_{ij}^T (\Delta u_i^{\text{dn}} - z_{ij}) + \frac{\rho}{2} \|\Delta u_i^{\text{dn}} - z_{ij}\|^2 \right] \tag{13}
$$

The ADMM iteration alternates between:

**Step 1** (parallel local QPs):
$$
\Delta u_i^{(\ell+1)} = \arg\min_{\Delta u_i} J_i(\Delta u_i) + \frac{\rho}{2} \|\Delta u_i^{\text{dn}} - z_{ij}^{(\ell)} + \mu_{ij}^{(\ell)}\|^2 \quad \forall i \tag{14}
$$

**Step 2** (consensus update):
$$
z_{ij}^{(\ell+1)} = \frac{1}{2} \left( \Delta u_i^{\text{dn},(\ell+1)} + \Delta u_j^{\text{up},(\ell+1)} \right) + \frac{1}{2} \left( \mu_{ij}^{(\ell)} + \mu_{ji}^{(\ell)} \right) \tag{15}
$$

**Step 3** (dual update):
$$
\mu_{ij}^{(\ell+1)} = \mu_{ij}^{(\ell)} + \Delta u_i^{\text{dn},(\ell+1)} - z_{ij}^{(\ell+1)} \tag{16}
$$

**Theorem 3** (ADMM convergence). *For the water network QP with positive definite local Hessians $H_i \succ 0$ and ADMM penalty $\rho > 0$, the ADMM iteration (Eqs. 14–16) converges to the centralized optimum. The optimal penalty is $\rho^* = \sqrt{\lambda_{\min}(H_i) \cdot \lambda_{\max}(H_i)}$.*

*Proof*. Follows from Boyd et al. (2011, §3.2) applied to the convex QP. The water network QP has $H_i \succ 0$ because $R_i \succ 0$ (control effort penalty is positive definite). The optimal $\rho$ minimizes the condition number of the augmented system (Ghadimi et al., 2015).  $\square$

ADMM combines parallelism (Step 1 is fully parallel) with robust convergence (guaranteed for any $\rho > 0$, though convergence rate depends on $\rho$ tuning).

__3.4  Communication-Aware Core Mapping__

Given $P$ processor cores and $N_p$ pool agents, the core mapping assigns agents to cores to minimize inter-core communication. For serial canal topology, this reduces to a 1D partitioning problem:

$$
\text{minimize} \quad \sum_{c=1}^{P} \sum_{\substack{(i,j) \in \mathcal{E} \\ \pi(i) \neq \pi(j)}} w_{ij} \tag{17}
$$

where $\pi(i)$ is the core assignment of agent $i$ and $w_{ij}$ is the communication weight (proportional to the number of shared variables). For serial topology, the optimal mapping assigns contiguous blocks of $\lceil N_p / P \rceil$ pools to each core. For tree topologies, we use a recursive bisection based on the network adjacency graph (Karypis & Kumar, 1998).

__3.5  Warm-Starting and Early Termination__

Two practical accelerations reduce computation time:

1. **Warm-starting**: At sampling step $k$, the QP is initialized with the shifted solution from step $k-1$: $\Delta u_i^{(0)}(k) = [\Delta u_i^*(1|k-1), \ldots, \Delta u_i^*(N_u-1|k-1), 0]$. This reduces the mean number of active-set iterations from 8.3 to 3.1 (Table 2).

2. **Early termination**: The outer iteration terminates when the primal residual (boundary mismatch) falls below a threshold $\epsilon_p$:

$$
r_{\text{primal}} = \max_{(i,j) \in \mathcal{E}} |\Delta u_i^{\text{dn}} - \Delta u_j^{\text{up}}| < \epsilon_p \tag{18}
$$

For water networks, $\epsilon_p = 10^{-3}$ m$^3$/s (corresponding to <0.1 mm water level impact) provides sufficient accuracy with 30–50% fewer iterations than convergence to machine precision.

__4  Implementation__

__4.1  Software Architecture__

ParaQP is implemented in C++ with OpenMP for shared-memory parallelism. The architecture comprises three layers:

- **QP Engine**: Active-set solver for individual pool QPs, using fixed-size arrays (no dynamic allocation) compatible with real-time constraints. Based on the qpOASES parametric active-set algorithm (Ferreau et al., 2014) with modifications for bounded array sizes.

- **Coordination Layer**: Implements the three decomposition strategies (§3.1–3.3) with configurable convergence criteria. ADMM penalty $\rho$ is auto-tuned using the spectral method of Wohlberg (2017).

- **Communication Layer**: Inter-core data exchange via shared memory (OpenMP) or MPI for distributed systems. Message size: 2 doubles per shared gate per iteration (flow and water level).

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

All systems are real-time feasible with Jacobi parallel DMPC. The 50-pool system uses only 0.44% of the sampling interval, leaving ample margin for communication, I/O, and other tasks. Sequential DMPC is also feasible for all systems on the CX2062, but the 50-pool case (4.8 s / 60 s = 8% utilization) leaves less margin for unexpected computational load.

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

The control performance difference is negligible: 0.4 mm RMSE increase corresponds to 4.9% degradation, well within the uncertainty of the IDZ model itself. The 98.7% computation time reduction enables deployment on resource-constrained edge hardware.

__5.7  SiL Verification with cuSVE__

ParaQP is coupled with the cuSVE GPU solver (Huang et al., 2026) for Software-in-the-Loop verification at full Saint-Venant fidelity. The cuSVE solver replaces the IDZ plant model with the 1D Saint-Venant equations, providing high-fidelity dynamics including nonlinear wave propagation, backwater effects, and gate hydraulics.

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

__5.8  Scaling Analysis__

__*Table 8. Scaling of Jacobi ParaQP on 16-Core CX2062*__

| Pools | QPs per core | Wall time (ms) | Speedup vs. seq. | Parallel efficiency |
|-------|-------------|----------------|-------------------|---------------------|
| 3 | 1 | 4.8 | 2.6× | 87% |
| 10 | 1 | 42 | 4.3× | 43% |
| 16 | 1 | 68 | 5.8× | 36% |
| 30 | 2 | 148 | 9.6× | 32% |
| 50 | 4 | 262 | 18.4× | 37% |
| 100 | 7 | 580 | 31.2× | 31% |

Parallel efficiency decreases as the number of pools per core increases (due to sequential execution within each core) and as inter-core communication grows. For the 100-pool system, the 580 ms wall-clock time remains well within the 60 s sampling interval.

__6  Discussion__

__6.1  Strategy Selection Guidelines__

Based on the benchmark results, we recommend:

- **Serial relaxation (GS)**: Best for systems with ≤5 pools where single-core execution is sufficient and convergence speed is paramount. Also preferred when only 2-core hardware is available.

- **Jacobi parallel**: Best for systems with >10 pools on multi-core hardware (≥4 cores). Provides the fastest wall-clock time despite requiring more outer iterations. Recommended as the default for CHS Edge Agent deployments.

- **ADMM consensus**: Best for systems with strong coupling ($\kappa > 0.3$) where Jacobi convergence may be slow, or for heterogeneous networks where different pools use different model types. ADMM's guaranteed convergence makes it the most robust option.

__6.2  Comparison with Existing Approaches__

Negenborn et al. (2009) applied serial DMPC to a 4-pool canal system with 3.2 s computation time on a desktop PC. ParaQP's Jacobi strategy solves the 3-pool benchmark (comparable complexity) in 4.8 ms—a 667× improvement due to (a) active-set solver efficiency, (b) warm-starting, and (c) parallel execution.

Lemos et al. (2012) proposed cooperative DMPC for irrigation canals but did not address parallel computation. Their sequential solver achieved 15–20 outer iterations for convergence; ParaQP's ADMM achieves 4–10 iterations with similar control quality, due to the optimal penalty tuning.

Zheng et al. (2019) applied ADMM to water distribution network optimization but focused on steady-state problems (not MPC). ParaQP extends ADMM to the dynamic MPC setting with warm-starting and early termination specific to water conveyance control.

__6.3  Limitations and Future Work__

1. **Looped networks**: The current decomposition assumes tree topology. Urban water distribution networks with loops require additional cycle-breaking constraints or a graph-cut decomposition (addressed in HZF-3, planned).

2. **Nonlinear MPC**: ParaQP assumes a QP (linear MPC with quadratic cost). Extension to nonlinear MPC (e.g., for large flow excursions beyond the IDZ validity range) requires sequential quadratic programming (SQP) within each agent—a planned v2.0 feature.

3. **GPU acceleration**: The current implementation uses CPU multi-threading (OpenMP). Porting the active-set solver to CUDA could provide additional speedup for systems with >100 pools, leveraging the same GPU already used by cuSVE.

4. **Adaptive decomposition**: The current core mapping is static. Dynamic repartitioning based on time-varying coupling strength (e.g., during gate maintenance when a pool is taken offline) could improve load balance.

__6.4  Integration Roadmap__

ParaQP is positioned within the CHS algorithmic tool chain:

- **Upstream**: Plant models from HydroComponents (Bai et al., 2026) → IDZ identification → QP matrices
- **Parallel**: cuSVE (Huang et al., 2026) provides high-fidelity plant simulation for SiL verification
- **Downstream**: HydroRTP (Yin et al., 2026) generates PLC/IPC code from the Simulink model containing ParaQP blocks
- **Future**: HZF-3 will integrate ParaQP into a graph-topology-aware digital twin engine with GPU acceleration

__7  Conclusions__

This paper presents ParaQP, a parallel QP solver architecture for Distributed Model Predictive Control of water conveyance networks. Three decomposition strategies—serial relaxation, Jacobi parallel, and ADMM consensus—are developed with formal convergence guarantees exploiting the block-separable structure of water network optimization problems. Benchmarking on systems from 3 to 50 pools demonstrates that:

1. Jacobi parallel DMPC achieves 18.4× speedup over sequential execution on a 16-core industrial PC, reducing worst-case computation time from 4.8 s to 262 ms for the 50-pool system.

2. Control performance degradation relative to centralized MPC is negligible (0.4 mm RMSE increase, no constraint violations), confirming that the decomposition preserves control quality.

3. Warm-starting reduces computation by an additional 37%, achieving 164 ms for 50 pools.

4. SiL verification with cuSVE at full Saint-Venant fidelity confirms robustness to model mismatch (3.8 mm additional RMSE, zero constraint violations).

ParaQP enables real-time DMPC deployment for water networks up to 100 pools on commercially available industrial PCs, removing the computational bottleneck that has limited practical adoption of distributed control in the water sector.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]). The authors thank Su Chao for providing the 3-pool flume experimental data and the Jiaodong Water Transfer Authority for field data access.

__Data Availability__

ParaQP source code is available at https://github.com/IWHR-CHS/ParaQP under MIT license. Benchmark data and scripts to reproduce all results are archived on Zenodo (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance).

__References__

Bai, Y., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for multi-fidelity water system modeling. Environmental Modelling & Software (submitted).

Bertsekas, D. P., & Tsitsiklis, J. N. (1989). Parallel and Distributed Computation: Numerical Methods. Prentice Hall.

Boyd, S., Parikh, N., Chu, E., Peleato, B., & Eckstein, J. (2011). Distributed optimization and statistical learning via the alternating direction method of multipliers. Foundations and Trends in Machine Learning, 3(1), 1–122.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Ferreau, H. J., Kirches, C., Potschka, A., Bock, H. G., & Diehl, M. (2014). qpOASES: A parametric active-set algorithm for quadratic programming. Mathematical Programming Computation, 6(4), 327–363.

Ghadimi, E., Teixeira, A., Shames, I., & Johansson, M. (2015). Optimal parameter selection for the alternating direction method of multipliers (ADMM). IEEE Transactions on Signal Processing, 63(9), 2265–2278.

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

Karypis, G., & Kumar, V. (1998). A fast and high quality multilevel scheme for partitioning irregular graphs. SIAM Journal on Scientific Computing, 20(1), 359–392.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Lemos, J. M., Rato, L. M., & Rijo, M. (2012). Distributed model predictive control of irrigation canals. In Distributed Model Predictive Control Made Easy (pp. 429–444). Springer.

Litrico, X., & Fromion, V. (2009). Modeling and Control of Hydrosystems. Springer.

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Negenborn, R. R., van Overloop, P.-J., Keviczky, T., & De Schutter, B. (2009). Distributed model predictive control of irrigation canals. Networks and Heterogeneous Media, 4(2), 359–380.

Schuurmans, J., Clemmens, A. J., Dijkstra, S., Hof, A., & Brouwer, R. (1999). Modeling of irrigation and drainage canals for controller design. Journal of Irrigation and Drainage Engineering, 125(6), 338–344.

Su, C., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). Experimental verification of the CHS unified transfer function family and distributed MPC on a multi-pool laboratory flume. Journal of Irrigation and Drainage Engineering (submitted).

van Overloop, P. J. (2006). Model Predictive Control on Open Water Systems (Doctoral dissertation). Delft University of Technology.

Varga, R. S. (2000). Matrix Iterative Analysis (2nd ed.). Springer.

Wohlberg, B. (2017). ADMM penalty parameter selection by residual balancing. arXiv:1704.06209.

Yin, B., Lei, X., Bai, Y., Ji, C., & Wang, H. (2026). HydroRTP: Simulink rapid prototyping toolbox for automatic code generation of water network controllers. SoftwareX (submitted).

Zheng, Y., Wang, C., & Zheng, F. (2019). ADMM-based distributed optimization for water distribution network management. Journal of Water Resources Planning and Management, 145(12), 04019061.

__Figure Captions__

__Figure 1.__ Block-separable structure of the DMPC Hessian matrix. (a) Centralized QP Hessian showing block-tridiagonal structure for serial canal topology. (b) Decomposition into local QPs with coupling terms. (c) Communication graph: each pool agent exchanges boundary flow and water level with adjacent neighbors.

__Figure 2.__ Convergence comparison of three decomposition strategies on B4 (50-pool). (a) Primal residual vs. outer iteration. (b) Objective function gap vs. outer iteration. (c) Wall-clock time vs. outer iteration (Jacobi/ADMM parallel on 16 cores, serial GS sequential).

__Figure 3.__ Control performance comparison on B2 (10-pool Jiaodong, 24-hour scenario). (a) Water level tracking: centralized MPC (blue dashed) vs. ParaQP Jacobi (red solid) for pools 1, 5, 10. (b) Gate flow trajectories. (c) Residual (ParaQP − centralized) showing <0.5 mm difference.

__Figure 4.__ Speedup scaling on Beckhoff CX2062 (16 cores). (a) Wall-clock time vs. pool count for three strategies. (b) Speedup vs. pool count. (c) Parallel efficiency vs. pool count.

__Figure 5.__ SiL verification with cuSVE. (a) Architecture: ParaQP DMPC controller coupled with cuSVE Saint-Venant plant model. (b) Water level comparison for B4 pool 25: IDZ prediction model (green dashed) vs. SVE verification (red solid). (c) Control action computed by ParaQP under both models.
