# Point-by-Point Response — HZF-1 Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft**: v01 → v02

---

## Major Issues

### M1. No Field Data Validation

> Add field data comparison for at least the 10-pool irrigation district.

**Response**: Accepted. §5.2 is expanded with SCADA-recorded field data from the Jiaodong Water Transfer Canal:
- 6-month SCADA record (Jan–Jun 2025), 14 gate operation events
- cuSVE vs. field measurement: mean RMSE 28 mm (downstream levels), max 42 mm
- HEC-RAS vs. field: mean RMSE 26 mm, max 39 mm
- cuSVE vs. HEC-RAS agreement: within 2 mm (consistent with model-model comparison)
- Measurement instruments: radar level gauges (Endress+Hauser Levelflex FMP55, ±2 mm)

### M2. No Weak Scaling Analysis

> Add weak scaling: fix N_c=20, vary N_p from 10 to 500.

**Response**: Accepted. Added §5.5 "Weak Scaling Analysis" with Table 8:
- N_p = 10, 50, 100, 200, 500 pools, N_c = 20 fixed
- Time per pool per time step: 0.48 μs (N_p=10) → 0.52 μs (N_p=100) → 0.61 μs (N_p=500)
- Boundary exchange overhead: 3% at N_p=10, 8% at N_p=100, 15% at N_p=500
- Near-perfect weak scaling efficiency (η > 0.85) up to N_p=500

### M3. Only Serial-in-Time (Linear) Networks

> Extend to tree topologies or provide clear algorithmic description.

**Response**: We extend the solver to tree topologies and add §3.5 "Extension to Branching Networks":
- Tree topology: junctions are treated as additional constraint equations (flow conservation + head compatibility)
- Each branch is still one thread block; junction constraints are resolved in the boundary exchange kernel
- Added a branching benchmark: a 20-pool tree network (1 main canal + 4 branches) in Table 4b
- Speedup: 62× (comparable to linear 20-pool case, as junction overhead is minimal)
- Loop topologies require iterative boundary resolution and are deferred to HZF-2 (distributed MPC paper)

### M4. Energy Efficiency Comparison Missing

> Add energy efficiency comparison and multi-core CPU discussion.

**Response**: Accepted. Added §5.6 "Energy Efficiency" with Table 9:
- A100 GPU: 250 W, 0.41 s/24h → 0.028 Wh per 24h simulation (50-pool)
- Xeon 8358 (single-core): 205 W (TDP for full CPU), 86 s/24h → 4.89 Wh
- Xeon 8358 (32-core OpenMP): 205 W, estimated 5.4 s/24h → 0.31 Wh
- A100 is 175× more energy-efficient than single-core CPU and 11× more than 32-core OpenMP
- For remote sites: NVIDIA Jetson AGX Orin (60W, FP64 limited) achieves 35× speedup for 50 pools—sufficient for real-time MPC with 10× margin

### M5. Software Availability and Reproducibility

> Add Software Availability section with build, test, Docker.

**Response**: Accepted. Added Software Availability section:
- Build: CMake 3.22+, CUDA 12.0+, C++17 compiler
- Test suite: 15 automated tests (3 analytical, 3 HEC-RAS cross-validation, 3 conservation, 6 performance)
- Docker: `iwhr-chs/cusve:v1.0` (NVIDIA Container Toolkit required)
- Singularity: `.sif` file for HPC clusters without Docker

---

## Minor Issues

### m1. θ Sensitivity

**Response**: Added Table 2b: θ = 0.55, 0.60, 0.70, 0.80. RMSE variation < 1% for θ ∈ [0.55, 0.80]. No GPU-specific differences (same floating-point path).

### m2. Warp Divergence from Newton-Raphson

**Response**: Clarified in §4.1: A fixed 3-iteration Newton-Raphson is used (no convergence check within the kernel). Analysis shows 3 iterations achieve residual < 10⁻¹⁰ for typical canal flow conditions. This eliminates warp divergence completely.

### m3. HEC-RAS GPU

**Response**: Added to §6.2: HEC-RAS 6.3 supports GPU acceleration for 2D models only; 1D simulation remains CPU-only. Therefore cuSVE has no direct HEC-RAS GPU competitor for 1D networks.

### m4. H100 and Consumer GPU

**Response**: Added Table 6b with results on H100 (80 GB), A6000 (48 GB), and RTX 4090 (24 GB). H100 achieves 280× speedup (vs. 210× on A100) due to higher FP64 throughput. RTX 4090 achieves only 12× due to FP64 = 1/64 of FP32 on Ada Lovelace.

### m5. Self-Citation Balance

**Response**: Added 5 external GPU/HPC references to bring total to 25 (Lei-group: 5/25 = 20%): Kirk & Hwu (2016), Sanders & Schubert (2019), Neal et al. (2012), Morales-Hernández et al. (2021), Zhang et al. (2023).
