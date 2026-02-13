# Point-by-Point Response — YBK-1 Iteration 2

**Reviewer**: C (Cross-disciplinary Scholar)
**Draft**: v02 → v03

---

## Major Issues

### M1. AI/ML Integration Pathway

**Response**: Added §4.1 "Extensibility: Neural and Hybrid Controllers":
- HydroRTP's S-function architecture supports custom blocks → neural network controllers via MATLAB Deep Learning Toolbox + Embedded Coder (LSTM, fully connected)
- Hybrid physics-ML: neural network as disturbance estimator inside MPC loop (already compatible with QP structure)
- Planned v2.0 feature: RL-trained policy block (PPO/SAC) with safety wrapper referencing ODD constraints
- Reference: Willard et al. (2022) physics-informed ML for hydrology

### M2. ODD Integration with CKG-2

**Response**: Added §4.2 "ODD Monitor Block":
- New block added to CHS Block Library v1.1: ODD Monitor (implements distance-to-boundary ρ from Chen et al., 2026b)
- Deploys alongside MPC as a supervisory function block on the same PLC
- Code generation produces the ODD monitor as a separate FUNCTION_BLOCK in ST, called from the same cyclic OB
- Fallback protocol triggers valve freeze / Layer 0 interlock when ρ ≤ 0
- This integration closes the loop: BAK-1 (plant model) → YBK-1 (controller + ODD monitor) → CKG-2 (ODD specification)

---

## Minor Issues

### m1. Community Adoption Plan

**Response**: Added §4.3 "Sustainability": maintained by CHS lab at Hebei University, GitHub Issues for bug reports, contribution guidelines (CONTRIBUTING.md), bi-annual releases, 3 core developers + student contributors.

### m2. Tutorial Availability

**Response**: Repository includes 4 tutorials: (1) single-pool PID, (2) single-pool MPC, (3) 3-pool DMPC, (4) code generation to S7-1500. Each as live Simulink + step-by-step README.
