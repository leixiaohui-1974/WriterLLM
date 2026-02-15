# Point-by-Point Response — YBK-1 Iteration 4

**Reviewer**: B (Engineering Practitioner)
**Draft**: v04 → v05

---

### m1. License Compatibility

**Response**: Added paragraph in §2.5: "HydroRTP source code is MIT-licensed. MATLAB R2023b+ with Simulink (academic: ~$500/yr; commercial: ~$5,000/yr) is required for model design. Embedded Coder (additional ~$4,000 commercial) is required for code generation. Users without Embedded Coder can use HydroRTP in simulation-only mode for controller design and SiL verification. The generated IEC 61131-3 Structured Text files are standalone and do not require MATLAB at runtime."

### m2. Version Numbering

**Response**: Added note in §4.3: "HydroRTP follows semantic versioning (semver.org): MAJOR for breaking API changes, MINOR for new blocks or features (e.g., v1.1 adds ODD monitor), PATCH for bug fixes."
