# Review — HZF-2 Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v01
**Score**: 6.5 / 10
**Verdict**: Major Revision

---

## Summary

This manuscript presents ParaQP, a parallel QP solver for distributed MPC of water conveyance networks. The paper develops three decomposition strategies (serial relaxation, Jacobi, ADMM) and benchmarks them on four systems from 3 to 50 pools. The algorithmic contribution is solid, but significant gaps exist in practical deployment guidance, comparison with commercial solvers, fault tolerance, and real-world validation.

## Major Issues

### M1. No comparison with commercial DMPC/QP solvers
The paper compares three in-house decomposition strategies against each other and against sequential execution, but does not compare against any existing commercial or open-source DMPC solver. Specifically:
- **Gurobi** with warm-starting and multi-threaded QP solving
- **CPLEX** with distributed optimization capabilities
- **OSQP** (open-source, ADMM-based) which is specifically designed for embedded/real-time QP
- **qpOASES** is cited but only as the internal engine—no standalone comparison

Without these comparisons, it is impossible to assess whether ParaQP offers genuine advantages beyond being domain-specific.

**Required**: Add a comparison table against at least OSQP and Gurobi on the B4 benchmark, reporting solve time, memory, and solution quality.

### M2. No fault tolerance or agent failure analysis
Real water networks experience hardware failures (PLC crashes, communication drops, sensor faults). The paper assumes all $N_p$ agents are always available. What happens when:
- One core crashes mid-computation?
- Communication between two agents is lost for one or more sampling steps?
- A sensor provides erroneous data to one agent?

The CKG-2 paper (Chen et al., 2026b) provides ODD-based fault detection, but this paper does not discuss how ParaQP degrades gracefully under partial failure.

**Required**: Add analysis of ParaQP behavior under agent failure scenarios, including fallback to sequential operation or reduced-agent DMPC.

### M3. No field validation data
All four benchmarks are either laboratory-scale (B1), model-based (B2, B3, B4), or synthetic. The B2 Jiaodong benchmark uses a model calibrated from field data, but the DMPC controller itself was not deployed and tested on the real canal. For a JWRPM audience, field deployment evidence—even preliminary—is essential.

**Required**: Either provide field data from a real DMPC deployment or clearly acknowledge this as a limitation and describe the planned field validation pathway.

### M4. Memory footprint and resource analysis missing
The paper reports wall-clock time and speedup but omits:
- Memory usage per agent (RAM, stack)
- Total memory footprint on the CX2062 IPC
- CPU utilization breakdown (QP solve vs. communication vs. overhead)
- Power consumption comparison (relevant for remote/solar-powered sites)

**Required**: Add a resource utilization table for all four benchmarks on the CX2062.

### M5. Self-citation rate too high
Counting references: out of 25 references, approximately 11 are self-citations (Lei 2025a, Lei & Wang 2025, Lei et al. 2025b, Lei et al. 2025c, Bai 2026, Chen 2026a, Chen 2026b, Huang 2026, Su 2026, Yin 2026, Schuurmans 1999 is borderline). This yields ~44% self-citation rate, well above the 15–25% target.

**Required**: Add 8–10 additional external references on DMPC for water systems, parallel optimization, and embedded real-time control to bring self-citation rate below 25%.

## Minor Issues

### m1. Coupling strength analysis incomplete
The coupling strength $\kappa$ (Eq. 9) is defined but its physical interpretation for water engineers is unclear. How does $\kappa$ relate to pool length, flow rate, or gate configuration? A plot of $\kappa$ vs. pool length / $A_s$ would help practitioners assess whether their system is suitable for Jacobi decomposition.

### m2. ADMM penalty auto-tuning not validated
Section 4.1 mentions spectral auto-tuning (Wohlberg, 2017) for the ADMM penalty $\rho$, but Table 1 uses $\rho = \rho^*$ (optimal). How does auto-tuning compare with fixed $\rho$? Sensitivity analysis is needed.

### m3. Branching network benchmark underdeveloped
B3 (30-pool branching) is synthetic. The junction handling (how QPs couple at branching points) deserves more detailed exposition, as this extends beyond the tridiagonal Hessian structure assumed in the convergence proofs.

### m4. No discussion of cybersecurity
Multi-core industrial PCs connected via Profinet/EtherNet are vulnerable to cyber-attacks. A brief mention of communication security for the inter-agent data exchange is warranted.

### m5. Code availability incomplete
The GitHub repository and Zenodo DOI are listed but with placeholder DOI. The paper should specify what exactly is included: source code only, or also benchmark models, test scripts, and documentation?

## Recommendation

**Major Revision**. The algorithmic contribution is solid, but the paper needs commercial solver comparison, fault tolerance analysis, resource utilization data, and reduced self-citation rate. Field validation data would significantly strengthen the manuscript.
