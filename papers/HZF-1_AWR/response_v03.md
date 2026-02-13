# Point-by-Point Response — HZF-1 Iteration 2

**Reviewer**: C (Cross-disciplinary Scholar)
**Draft**: v02 → v03

---

## Major Issues

### M1. ML-Based Surrogate Comparison

**Response**: Added §6.4 "Physics-Based GPU vs. ML Surrogates" discussing:
- cuSVE provides guaranteed mass conservation and known error bounds; ML surrogates do not.
- cuSVE is complementary: it generates high-fidelity training data for surrogates; the 210,000× real-time factor means millions of training scenarios can be generated in hours.
- For extrapolation beyond training distribution (novel gate schedules, extreme events), cuSVE remains robust while surrogates may degrade.
- Cited: Lu et al. (2021) DeepONet, Li et al. (2021) Fourier Neural Operator.

### M2. Multi-GPU and Cloud Deployment

**Response**: Added §6.5 "Scaling to Multi-GPU and Cloud":
- Multi-GPU: the pool-level decomposition extends naturally to multi-GPU via NCCL, with pools distributed across GPUs. Inter-GPU boundary exchange replaces intra-GPU global memory exchange.
- Cloud: cuSVE runs on AWS p4d instances (A100), Azure NDv4 (A100), enabling pay-per-use deployment for utilities without GPU hardware.
- Estimated: 4× A100 (AWS p4d.24xlarge) can handle ~800 pools in real-time.

---

## Minor Issues

### m1. Roofline Analysis

**Response**: Added to §5.5: cuSVE is compute-bound (arithmetic intensity 8.2 FLOP/byte, above the A100's roofline knee at 4.5 FLOP/byte). This means further optimization should focus on algorithmic improvements (fewer iterations) rather than memory bandwidth.

### m2. Speedup Baseline

**Response**: Table 9 already includes 32-core OpenMP CPU comparison. Added a note in §5.5 clarifying that the primary speedup is reported vs. HEC-RAS (industry standard, single-thread) for practical relevance, with multi-core CPU comparison provided separately for fairness.
