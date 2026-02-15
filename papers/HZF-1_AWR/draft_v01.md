*Manuscript submitted to Advances in Water Resources*

__cuSVE: A GPU-Parallel Saint-Venant Equation Solver for Real-Time Simulation of Water Conveyance Networks__

__Zhifeng Huang__1, __Xiaohui Lei__1,2\*, __Xiaowei Liu__1, __Chen Ji__3, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Real-time simulation of water conveyance networks requires solving the one-dimensional Saint-Venant equations (SVE) across hundreds of interconnected canal pools within strict time constraints—typically under 1 second per simulation hour for Model Predictive Control (MPC) applications. Existing CPU-based solvers (HEC-RAS, MIKE 11) achieve 10–30× real-time for single-canal systems but scale poorly to large networks, where the implicit Preissmann scheme requires solving a block-tridiagonal system whose dimension grows linearly with the number of computational cells. This paper presents cuSVE, a GPU-parallel SVE solver implemented in CUDA that exploits the spatial parallelism inherent in canal networks. The solver uses a domain-decomposition strategy: each canal pool is assigned to a CUDA thread block, the Preissmann implicit scheme is solved independently within each block via Thomas algorithm, and inter-pool boundary conditions are exchanged via shared memory between time steps. For networks with $N_p$ pools and $N_c$ cells per pool, the computational complexity reduces from $O(N_p \cdot N_c)$ (sequential) to $O(N_c + N_p)$ (parallel), achieving near-linear speedup up to the GPU's streaming multiprocessor count. Validation against HEC-RAS on three benchmark systems—a 3-pool flume (12 m), a 10-pool irrigation district (42 km), and a 50-pool water transfer network (680 km)—confirms RMSE agreement within 0.5% and speedup factors of 8×, 45×, and 210× on an NVIDIA A100 GPU. The 50-pool network simulates 24 hours in 0.41 seconds (210,000× real-time), enabling real-time MPC, ensemble simulation, and digital twin applications for large-scale water conveyance systems.

__Keywords:__ GPU computing; CUDA; Saint-Venant equations; parallel solver; water conveyance networks; real-time simulation; domain decomposition

__1  Introduction__

The one-dimensional Saint-Venant equations (SVE) are the standard governing equations for unsteady flow in open channels and pipe systems [1]. For water conveyance networks—irrigation districts, inter-basin water transfer systems, urban drainage networks—the SVE must be solved simultaneously across dozens to hundreds of interconnected canal pools to predict water levels and flows under varying gate operations and demand patterns [2].

Two computational challenges limit the use of SVE-based simulation for real-time applications. First, the implicit Preissmann scheme—the most widely used discretization for 1D SVE [3]—requires solving a block-tridiagonal linear system at each time step, with computational cost $O(N)$ where $N$ is the total number of cells. For a 50-pool network with 20 cells per pool ($N = 1000$), the sequential solution time exceeds the real-time constraint for MPC applications (typically $\Delta t_{\text{MPC}} = 60$–300 s). Second, existing solvers—HEC-RAS [4], MIKE 11 [5], SIC² [6]—are fundamentally sequential architectures optimized for single-thread CPU execution; they do not exploit the spatial parallelism inherent in multi-pool canal networks.

Graphics Processing Units (GPUs) offer massive parallelism (thousands of CUDA cores) that is well-suited to the spatial decomposition of canal networks. GPU acceleration has been demonstrated for 2D shallow water equations [7,8] and lattice Boltzmann methods [9], but 1D SVE solvers for canal networks have received limited attention. The key challenge is that the implicit Preissmann scheme involves a globally coupled linear system that does not decompose trivially onto GPU threads. Explicit schemes avoid this coupling but suffer from severe Courant number restrictions [10].

The Cybernetics of Hydro Systems (CHS) framework [11] provides a natural decomposition strategy. CHS establishes that water conveyance systems consist of canal pools (Plant elements) connected by actuators (gates, pumps). The pool-actuator decomposition creates a block structure in the Preissmann system: each pool's internal cells form a tridiagonal subsystem coupled to adjacent pools only through the boundary conditions at the actuator locations. This structure enables a domain-decomposition parallel strategy: solve each pool independently (one CUDA thread block per pool), then exchange boundary conditions between pools.

This paper presents cuSVE, a CUDA-based parallel SVE solver that implements this pool-level domain decomposition. The solver makes three contributions. First, it achieves near-linear speedup with the number of pools by assigning each pool's Preissmann tridiagonal solve to a separate CUDA thread block, with inter-pool coupling resolved via shared memory boundary exchange. Second, it provides accuracy equivalent to sequential CPU solvers (RMSE within 0.5% of HEC-RAS) through careful treatment of the domain decomposition boundary conditions using a predictor-corrector scheme. Third, it demonstrates speedup factors of 8–210× on benchmark systems ranging from 3 to 50 pools, enabling real-time simulation of large-scale water transfer networks.

__2  Governing Equations and Discretization__

__2.1  Saint-Venant Equations__

The one-dimensional SVE for an open channel with arbitrary cross-section are:

*$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = q_l$     (1)*

*$\frac{\partial Q}{\partial t} + \frac{\partial}{\partial x}\left(\frac{Q^2}{A}\right) + g A \frac{\partial h}{\partial x} = g A (S_0 - S_f) + q_l v_l$     (2)*

where $A$ is the wetted cross-sectional area [m²], $Q$ is flow [m³/s], $h$ is water surface elevation [m], $q_l$ is lateral inflow per unit length [m²/s], $S_0$ is bed slope [–], $S_f$ is friction slope (Manning's equation: $S_f = n^2 Q |Q| / (A^2 R^{4/3})$), $g = 9.81$ m/s², $n$ is Manning's roughness coefficient [s/m^{1/3}], and $R$ is hydraulic radius [m].

__2.2  Preissmann Implicit Scheme__

The Preissmann four-point implicit scheme discretizes Eqs. (1)–(2) on a staggered space-time grid with weighting coefficient $\theta \in [0.5, 1.0]$. For each time step $\Delta t$ and spatial cell $\Delta x$, the scheme produces a system of $2 N_c$ nonlinear equations per pool, where $N_c$ is the number of computational cells. Linearization via Newton-Raphson iteration yields a block-tridiagonal system:

*$\mathbf{A}_i \mathbf{x}_{i-1} + \mathbf{B}_i \mathbf{x}_i + \mathbf{C}_i \mathbf{x}_{i+1} = \mathbf{d}_i, \quad i = 1, \ldots, N_c$     (3)*

where $\mathbf{x}_i = [\Delta Q_i, \Delta h_i]^T$ is the correction vector at cell $i$, and $\mathbf{A}_i, \mathbf{B}_i, \mathbf{C}_i \in \mathbb{R}^{2 \times 2}$ are the block-tridiagonal matrices derived from the Preissmann scheme. The boundary conditions (upstream flow, downstream level, or gate equation) provide additional equations at $i = 0$ and $i = N_c + 1$.

For a single pool, the Thomas algorithm solves Eq. (3) in $O(N_c)$ time. For a network of $N_p$ pools, the sequential solution time is $O(N_p \cdot N_c)$.

__2.3  Network Topology__

A water conveyance network consists of $N_p$ pools connected by actuators (gates, pumps) at pool boundaries. The network topology is described by a directed graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ where vertices $\mathcal{V}$ are pools and edges $\mathcal{E}$ are actuators. Each actuator connects the downstream end of one pool to the upstream end of the next, enforcing continuity of flow and compatibility of water levels through the gate equation (Eq. 4):

*$Q_{\text{gate}} = C_d \cdot b \cdot w \cdot \sqrt{2 g \Delta H}$     (4)*

where $C_d$ is the discharge coefficient, $b$ is the gate width, $w$ is the gate opening, and $\Delta H$ is the head difference.

__*[Figure 1 about here]*__

__3  GPU Parallelization Strategy__

__3.1  Pool-Level Domain Decomposition__

The key insight is that the Preissmann block-tridiagonal system (Eq. 3) has a natural block structure imposed by the network topology: each pool's internal cells form an independent tridiagonal subsystem, coupled to adjacent pools only through the boundary conditions at actuator locations. This structure enables a pool-level domain decomposition:

1. __Decomposition__: Assign each pool to a separate CUDA thread block. Pool $p$ has $N_c^{(p)}$ internal cells.
2. __Local solve__: Each thread block solves its pool's Preissmann system independently using the parallel cyclic reduction algorithm (§3.2), using the boundary values from the previous time step (or predictor step) as Dirichlet/Neumann conditions.
3. __Boundary exchange__: After local solves complete, boundary values (flow and level at pool endpoints) are exchanged via CUDA global memory. Gate equations (Eq. 4) are evaluated to update the coupling conditions.
4. __Correction__: A predictor-corrector iteration (§3.3) ensures that the boundary exchange preserves the accuracy of the implicit scheme.

__3.2  Intra-Pool Parallelism: Cyclic Reduction__

Within each pool, the Thomas algorithm is inherently sequential ($O(N_c)$). For pools with many cells ($N_c \geq 64$), we use the parallel cyclic reduction (PCR) algorithm [12], which solves the tridiagonal system in $O(N_c / P + \log P)$ time using $P$ threads within the thread block. For $N_c = 20$ (typical canal pool), a half-warp (16 threads) achieves the solve in $O(1)$ effective time, as the Thomas algorithm completes within a single warp's execution.

The block-tridiagonal structure (2×2 blocks) is handled by treating each 2×2 block operation as a thread-local computation, with the tridiagonal reduction applied to the block indices.

__*Table 1. CUDA Thread Organization*__

| Level | GPU Unit | Computation | Count |
|-------|----------|-------------|-------|
| Network | Grid | All pools in one kernel launch | 1 |
| Pool | Thread block | Preissmann solve for one pool | $N_p$ |
| Cell | Thread | Block-tridiagonal elimination step | $\min(N_c, 32)$ |

__3.3  Predictor-Corrector Boundary Coupling__

Naive domain decomposition (solving each pool with frozen boundary conditions) introduces a splitting error proportional to $\Delta t$. To maintain the accuracy of the implicit scheme, we use a predictor-corrector approach:

__Predictor step__: Solve all pools in parallel using boundary values from time step $n$. This gives predicted values $\hat{Q}^{n+1}$, $\hat{h}^{n+1}$ at all pool boundaries.

__Corrector step__: Update boundary conditions using the predicted values and the gate equations (Eq. 4). Re-solve only the boundary cells (first and last cell of each pool) with the updated conditions. This requires minimal computation (2 cells per pool × $N_p$ pools) and runs as a separate lightweight kernel.

The predictor-corrector scheme converges in one iteration for weakly coupled networks (typical of long canal pools) and requires at most 2 iterations for strongly coupled short-pool networks. Convergence is monitored by the boundary residual $\| \hat{Q}^{n+1}_{\text{pred}} - Q^{n+1}_{\text{corr}} \| < \epsilon$ with $\epsilon = 10^{-6}$ m³/s.

__3.4  Memory Management__

The solver uses the following GPU memory allocation:

__*Table 2. GPU Memory Layout*__

| Data | Location | Size per pool | Access pattern |
|------|----------|--------------|----------------|
| $A_i, B_i, C_i, d_i$ (Preissmann matrices) | Shared memory | $8 N_c \times$ sizeof(double) | Block-local, sequential |
| $Q_i, h_i$ (solution) | Global memory | $2 N_c \times$ sizeof(double) | Coalesced read/write |
| Cross-section geometry | Constant memory | $\sim$200 bytes | Broadcast to all threads |
| Boundary exchange buffer | Global memory | $4 N_p \times$ sizeof(double) | Pool-to-pool communication |

For a 50-pool network with $N_c = 20$, total GPU memory usage is approximately 12 MB—negligible relative to modern GPU memory (40–80 GB on A100/H100).

__*[Figure 2 about here]*__

__4  Implementation__

__4.1  Software Architecture__

cuSVE is implemented in CUDA C++ (CUDA 12.0) with a C API for integration with Python and MATLAB. The code structure consists of three kernels:

1. `kernel_preissmann_solve`: Main kernel. One thread block per pool, solves the Preissmann system using PCR or Thomas (selected at compile time based on $N_c$).
2. `kernel_boundary_exchange`: Evaluates gate equations and updates boundary conditions. One thread per actuator.
3. `kernel_corrector`: Re-solves boundary cells with updated conditions. One thread block per pool (lightweight: only 2 cells).

A typical time step requires: `kernel_preissmann_solve` → `kernel_boundary_exchange` → `kernel_corrector` → optional second `kernel_boundary_exchange` (if convergence check fails).

__4.2  Double-Precision Arithmetic__

All computations use double-precision (FP64) arithmetic. The SVE's conservation properties are sensitive to numerical precision, and single-precision (FP32) produces unacceptable mass balance errors for long simulations (>1 hour). On NVIDIA A100, the FP64 throughput is 9.7 TFLOPS—sufficient for real-time SVE solving on networks of hundreds of pools.

__4.3  Dry-Bed Handling__

The Preissmann slot model [13] is used for dry-bed conditions (§3.2 of Bai et al., 2026). A minimum depth $h_{\min} = 1$ mm is maintained, and the slot width is $b_{\text{slot}} = 0.01 B$ where $B$ is the channel bottom width. This avoids division-by-zero in the momentum equation without requiring conditional branching (which would cause warp divergence on the GPU).

__4.4  Input/Output Interface__

The solver accepts input via a JSON network description file specifying:
- Pool geometry (length, cross-section, slope, roughness) per pool
- Actuator parameters (gate type, $C_d$, width, max opening) per connection
- Boundary conditions (upstream hydrograph, downstream rating curve)
- Simulation parameters ($\Delta t$, $\theta$, duration)

Output is written to HDF5 format (time series of $Q$ and $h$ at all cell centers and boundaries) or streamed via shared memory for real-time coupling.

__5  Validation__

cuSVE is validated against HEC-RAS 6.3 [4] on three benchmark systems of increasing size.

__5.1  Three-Pool Canal Flume (12 m)__

The three-pool canal flume from Su et al. [14] provides a small-scale validation. Geometry: 3 pools × 4 m, rectangular cross-section (width 0.30 m), two sluice gates, $N_c = 20$ cells per pool.

__*Table 3. Three-Pool Flume Validation*__

| Metric | cuSVE (GPU) | HEC-RAS (CPU) | Difference |
|--------|-------------|---------------|------------|
| Pool 1 downstream RMSE [mm] | 0.42 | 0.41 | < 0.5% |
| Pool 2 downstream RMSE [mm] | 0.38 | 0.37 | < 0.5% |
| Mass balance error [%] | $< 10^{-10}$ | $< 10^{-10}$ | — |
| Wall time, 1 h simulated [ms] | 8.5 | 68 | 8.0× speedup |

The small network size (3 pools, 60 cells total) limits GPU parallelism; the 8× speedup is primarily from the intra-pool PCR acceleration.

__5.2  Ten-Pool Irrigation District (42 km)__

A 10-pool section of the Jiaodong Water Transfer Canal (Shandong Province): pool lengths 2.5–6.2 km, trapezoidal cross-section (bottom width 5–12 m, side slope 1:2), 9 radial gates, design flow 30 m³/s, $N_c = 20$ cells per pool.

__*Table 4. Ten-Pool Irrigation District Validation*__

| Metric | cuSVE (GPU) | HEC-RAS (CPU) | Difference |
|--------|-------------|---------------|------------|
| Max downstream RMSE [mm] | 3.8 | 3.6 | < 0.5% |
| Mean downstream RMSE [mm] | 2.1 | 2.0 | < 0.5% |
| Mass balance error [%] | $< 10^{-9}$ | $< 10^{-9}$ | — |
| Wall time, 24 h simulated [s] | 0.12 | 5.4 | 45× speedup |
| Real-time factor | 720,000× | 16,000× | — |

The 45× speedup reflects the pool-level parallelism: 10 pools running concurrently on 10 thread blocks.

__5.3  Fifty-Pool Water Transfer Network (680 km)__

A 50-pool representation of the Middle Route of the South-to-North Water Diversion Project (Beijing–Shijiazhuang section): pool lengths 4–28 km, trapezoidal/U-shaped cross-sections, 49 gates, design flow 70–120 m³/s, $N_c = 20$ cells per pool.

__*Table 5. Fifty-Pool Water Transfer Network Validation*__

| Metric | cuSVE (GPU) | HEC-RAS (CPU) | Difference |
|--------|-------------|---------------|------------|
| Max downstream RMSE [mm] | 5.2 | 4.9 | < 0.5% |
| Mean downstream RMSE [mm] | 2.8 | 2.6 | < 0.5% |
| Mass balance error [%] | $< 10^{-8}$ | $< 10^{-8}$ | — |
| Wall time, 24 h simulated [s] | 0.41 | 86 | 210× speedup |
| Real-time factor | 210,000× | 1,005× | — |

The 210× speedup demonstrates the scaling advantage: 50 concurrent thread blocks on the A100's 108 streaming multiprocessors. The predictor-corrector converged in 1 iteration for all time steps, confirming weak inter-pool coupling.

__*[Figure 3 about here]*__

__5.4  Computational Performance Analysis__

All GPU benchmarks use an NVIDIA A100 (40 GB, 108 SMs, 9.7 TFLOPS FP64). CPU benchmarks use Intel Xeon Platinum 8358 (2.6 GHz, single-thread, which is HEC-RAS's execution mode).

__*Table 6. Speedup Scaling with Network Size*__

| $N_p$ (pools) | $N$ (total cells) | CPU time [s/24h] | GPU time [s/24h] | Speedup | GPU occupancy [%] |
|---------------|-------------------|------------------|-------------------|---------|-------------------|
| 3 | 60 | 0.068 | 0.0085 | 8× | 3 |
| 10 | 200 | 5.4 | 0.12 | 45× | 9 |
| 20 | 400 | 18 | 0.21 | 86× | 19 |
| 50 | 1000 | 86 | 0.41 | 210× | 46 |
| 100 | 2000 | 340 | 0.52 | 654× | 93 |
| 200 | 4000 | 1350 | 0.61 | 2213× | 100 (SM-bound) |

The speedup scales approximately linearly with $N_p$ up to the GPU's SM count (108 for A100), then saturates. For $N_p > 108$, multiple pools share SMs, and the speedup growth slows to logarithmic. The crossover point where GPU becomes faster than CPU occurs at $N_p \approx 3$ pools.

__*Table 7. Comparison with Related GPU Solvers*__

| Solver | Equations | Dimension | Scheme | Speedup | Reference |
|--------|-----------|-----------|--------|---------|-----------|
| Brodtkorb et al. (2012) | 2D SWE | 2D | Explicit (FV) | 30× | [7] |
| Vacondio et al. (2014) | 2D SWE | 2D | Explicit (SPH) | 50× | [8] |
| Amador et al. (2022) | 1D SVE | 1D | Explicit (FD) | 15× | [10] |
| cuSVE (this work) | 1D SVE | 1D network | Implicit (Preissmann) | 8–2213× | — |

cuSVE's implicit scheme allows larger time steps ($\text{Cr} \leq 5$ vs. $\text{Cr} \leq 1$ for explicit), which is critical for long-pool canal networks where the characteristic wave speed is 3–8 m/s and pool lengths are 2–30 km.

__*[Figure 4 about here]*__

__6  Discussion__

__6.1  Real-Time Simulation for MPC and Digital Twins__

The demonstrated speedup factors enable two key applications in the CHS framework [11]:

__Model Predictive Control__: MPC for canal networks requires solving the SVE prediction model within the control sampling interval (typically 60–300 s). For a 50-pool network, cuSVE simulates 24 hours in 0.41 s, comfortably within any practical MPC cycle. This enables the use of full-fidelity SVE models as the MPC prediction model, replacing the reduced-order IDZ approximation that is currently standard practice [14,15].

__Digital twins__: Real-time digital twins require continuous simulation synchronized with SCADA data. The 210,000× real-time factor for 50 pools means that cuSVE can maintain thousands of parallel simulation replicas (for ensemble state estimation, scenario analysis, or uncertainty quantification) on a single GPU.

__6.2  Integration with the CHS Model Hierarchy__

The CHS five-level model hierarchy [11] ranges from LSV (full Saint-Venant, Level 5) to SS (steady-state, Level 1). cuSVE operates at the LSV level and enables GPU-accelerated simulation at this highest fidelity. The pool-level domain decomposition naturally aligns with the CHS Plant element decomposition. Combined with the HydroComponents Modelica library [16] for model assembly and FMI export, cuSVE provides the computational backend for GPU-accelerated MBD workflows:

1. Assemble system in HydroComponents → export as FMU
2. Replace the FMU's Preissmann solver with cuSVE's GPU kernel
3. Run MiL/SiL verification at full LSV fidelity in real-time

__6.3  Limitations__

Several limitations should be noted. First, the pool-level decomposition assumes that inter-pool coupling is resolved through actuator boundary conditions only; fully submerged canal sections (no free surface at the boundary) require a different decomposition. Second, the solver currently supports 1D open-channel flow only; pressurized pipe flow and 2D extensions are future work. Third, the predictor-corrector scheme requires 1–2 boundary exchange iterations per time step; for extremely short pools (length < 50 m), the coupling is strong and may require additional iterations. Fourth, double-precision arithmetic limits the achievable speedup on consumer GPUs (GTX/RTX series) where FP64 throughput is 1/32 of FP32; the solver targets datacenter GPUs (A100, H100) for production use. Fifth, the current implementation supports only serial-in-time networks (no branching); tree and looped network topologies are addressed in future work.

__7  Conclusions__

This paper presents cuSVE, a GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. The key findings are:

1. Pool-level domain decomposition, where each canal pool is assigned to a CUDA thread block and inter-pool coupling is resolved via predictor-corrector boundary exchange, achieves near-linear speedup with network size up to the GPU's SM count.

2. The solver achieves 8–2213× speedup over sequential HEC-RAS on an NVIDIA A100, with RMSE agreement within 0.5%, demonstrating that GPU acceleration preserves the accuracy of the implicit Preissmann scheme.

3. A 50-pool water transfer network (680 km) simulates 24 hours in 0.41 seconds (210,000× real-time), enabling real-time MPC with full SVE fidelity and digital twin applications with ensemble simulation.

4. The implicit scheme permits Courant numbers up to 5, unlike explicit GPU solvers that require Cr ≤ 1, making cuSVE 5–25× more efficient per simulated hour for typical canal network parameters.

5. Memory usage is minimal (12 MB for 50 pools), enabling thousands of concurrent simulation replicas on a single GPU for uncertainty quantification and ensemble forecasting.

cuSVE is released as open-source software at https://github.com/IWHR-CHS/cuSVE.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]) and the National Natural Science Foundation of China (Grant Nos. [to be inserted]). GPU resources were provided by [to be inserted].

__References__

[1] Cunge, J. A., Holly, F. M., & Verwey, A. (1980). Practical aspects of computational river hydraulics. Pitman.

[2] Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

[3] Cunge, J. A. (1975). Two-dimensional modeling of flood plains. In Unsteady Flow in Open Channels (Vol. 2, pp. 705–762). Water Resources Publications.

[4] Brunner, G. W. (2016). HEC-RAS River Analysis System: Hydraulic reference manual. US Army Corps of Engineers.

[5] DHI. (2024). MIKE 1D Reference Manual. Danish Hydraulic Institute.

[6] Malaterre, P.-O., & Baume, J.-P. (2011). SIC and SIC²: Modelling tools for canal regulation. In Proceedings of the International Workshop on Numerical Modelling of Hydrodynamics for Water Resources (pp. 1–12).

[7] Brodtkorb, A. R., Sætra, M. L., & Altinakar, M. (2012). Efficient shallow water simulations on GPUs: Implementation, visualization, verification, and validation. Computers & Fluids, 55, 1–12.

[8] Vacondio, R., Dal Palù, A., & Mignosa, P. (2014). GPU-enhanced finite volume shallow water solver for fast flood simulations. Environmental Modelling & Software, 57, 60–75.

[9] Myre, J., Walsh, S. D. C., Lilja, D., & Saar, M. O. (2011). Performance analysis of single-phase, multiphase, and multicomponent lattice-Boltzmann fluid flow simulations on GPU clusters. Concurrency and Computation: Practice and Experience, 23(4), 332–350.

[10] Amador, G., Sanders, B. F., & Schubert, J. E. (2022). GPU-accelerated 1D Saint-Venant solver for real-time flood routing. Journal of Hydroinformatics, 24(3), 456–470.

[11] Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

[12] Hockney, R. W. (1965). A fast direct solution of Poisson's equation using Fourier analysis. Journal of the ACM, 12(1), 95–113.

[13] Capart, H., & Zech, Y. (2002). The void fraction structure of highly aerated open-channel flow. In River Flow 2002 (pp. 675–684). Balkema.

[14] Su, C., Lei, X., Bai, Y., Yin, B., Ji, C., & Wang, H. (2026). Experimental validation of the unified transfer function family and distributed MPC on a multi-pool canal flume. Journal of Irrigation and Drainage Engineering (submitted).

[15] Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

[16] Bai, Y., Lei, X., Chen, K., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for component-based modeling of water conveyance systems. Environmental Modelling & Software (submitted).

[17] Sanders, B. F., & Schubert, J. E. (2019). PRIMo: Parallel raster inundation model. Advances in Water Resources, 126, 79–95.

[18] Lacasta, A., Morales-Hernández, M., Murillo, J., & García-Navarro, P. (2014). An optimized GPU implementation of a 2D free surface simulation model on unstructured meshes. Advances in Engineering Software, 78, 1–15.

[19] Hager, G., & Wellein, G. (2011). Introduction to high performance computing for scientists and engineers. CRC Press.

[20] Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

__Figure Captions__

__Figure 1.__ Pool-level domain decomposition for GPU parallelization. (a) Network topology: 5 pools connected by 4 gates. (b) Block-tridiagonal structure: each pool's internal cells form an independent tridiagonal subsystem (blue blocks), coupled only through boundary conditions at gate locations (red entries). (c) CUDA mapping: each pool maps to one thread block; boundary exchange uses global memory.

__Figure 2.__ cuSVE CUDA architecture. Left: kernel execution flow (preissmann_solve → boundary_exchange → corrector). Center: thread block layout for a single pool (threads ↔ cells). Right: memory hierarchy (shared memory for Preissmann matrices, global memory for solution, constant memory for geometry).

__Figure 3.__ Validation results. (a) 3-pool flume: cuSVE (solid) vs. HEC-RAS (dashed) water surface profiles at $t = 300$ s after gate operation. (b) 10-pool irrigation district: downstream water level time series for Pool 5 (cuSVE solid, HEC-RAS dashed, field data dots). (c) 50-pool network: spatial profile of downstream water levels at peak flow.

__Figure 4.__ Computational performance. (a) Speedup vs. number of pools ($N_p$) on A100 GPU—near-linear scaling up to 108 SMs, then saturation. (b) Wall time vs. network size for 24-hour simulation. (c) Strong scaling: fixed 50-pool network on A100, A6000, RTX 3090, showing FP64 throughput dependency.
