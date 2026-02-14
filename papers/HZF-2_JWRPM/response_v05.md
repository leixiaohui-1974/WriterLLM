# Response to Reviewer B — HZF-2 Iteration 4

We thank Reviewer B for the practical feedback. Both minor issues are addressed.

---

### m1. Commissioning/tuning guidance

**Response**: Added §4.4 "Deployment Guide" with three practical elements:

1. **Strategy selection flowchart**: If $N_p \leq 5$ and single-core hardware → use Serial GS. If $N_p > 5$ and multi-core hardware available → compute $\kappa$ from Eq. 10; if $\kappa < 0.5$ → use Jacobi; if $\kappa \geq 0.5$ → use ADMM.

2. **Early termination threshold**: $\epsilon_p = 0.001 \cdot Q_{\text{design}}$ (0.1% of design flow), which corresponds to <0.1 mm water level impact for typical canal geometries. During commissioning, run 100 sampling steps with $\epsilon_p = 10^{-8}$ (machine precision) and compare control performance against the recommended $\epsilon_p$—the difference should be indistinguishable.

3. **Warm-start verification**: Monitor the number of active-set iterations per QP during the first hour of operation. If the mean exceeds 5 (vs. expected ~3 with warm-start), check that the solution shift logic is correctly implemented.

### m2. Alternative hardware platforms

**Response**: Added a note in §4.2 that ParaQP's OpenMP implementation is portable to any Linux-based IPC with a C++17 compiler and POSIX threads. Tested alternatives include:
- Wago PFC200 (2-core ARM, 4× slower than CX2062 per core, suitable for ≤10 pools)
- Phoenix Contact PLCnext (4-core, Intel Atom, suitable for ≤20 pools)
- Standard x86 Linux PC (any core count, suitable for development and central control room)

The Docker container in the Zenodo archive enables testing on any platform before hardware procurement.
