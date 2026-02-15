# Point-by-Point Response — HZF-1 Iteration 4

**Reviewer**: B (Engineering Practitioner)
**Draft**: v04 → v05

---

### m1. CUDA Compute Capability

**Response**: Clarified in Software Availability: CC 7.0 (Volta) is required for cooperative groups (used in the predictor-corrector synchronization). Pascal GPUs (CC 6.0) can run the solver with cooperative groups disabled (fallback to __syncthreads), but at ~10% performance penalty. Added note.

### m2. JSON Input Format

**Response**: Added an example JSON snippet in §4.4 showing a 3-pool serial network configuration. Full schema documentation is provided in the repository's `docs/input_format.md`.
