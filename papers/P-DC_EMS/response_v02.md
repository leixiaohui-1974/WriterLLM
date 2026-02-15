# Response to Review — Paper P-DC Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Review Score**: 6.5/10 — Major Revision

---

## Major Issues

### M1. DfO Principles Lack Quantitative Metrics
**Response**: Accepted. Each DfO principle will be formalized with: (a) a mathematical definition linked to control theory; (b) a computable metric from the MBD model stack; (c) a threshold criterion. For example, P1 (Controllability by Design) → rank condition of controllability matrix within ODD; P2 (Observability by Design) → observability Gramian condition number ≤ threshold; P3 (ODD-Awareness) → achievable ODD coverage ratio; P4 (Verifiability) → xIL test coverage ≥ 95% of ODD scenarios; P5 (Maintainability) → mean time to software update ≤ threshold.

### M2. Reference Workflow Insufficiently Detailed
**Response**: Accepted. Will expand §6 to ~1,500 words with: OpenModelica component structure, MPC configuration table, FMI coupling details, quantitative MiL results (RMSE, constraint satisfaction, computation time), and a Layer 7 vs Layer 6 model comparison figure. This is the most critical revision.

### M3. Curriculum Section Scope
**Response**: Accepted. Will reframe §5 as "Educational Software Infrastructure for CHS" focusing on software tools, virtual laboratory platforms, open-source educational packages, and remote-access simulation. This brings curriculum content within EMS scope while retaining the educational contribution.

### M4. Software Availability
**Response**: Accepted. Will provide a genuine software artifact: an OpenModelica water component library (CanalPool, ControlGate, Reservoir, PumpStation) with FMI export capability, plus Simulink MPC templates and Python coupling scripts. Repository will be created with documentation. The paper is reframed as presenting both methodology and software.

### M5. Literature
**Response**: Accepted. Will add 12+ references covering model-based systems engineering, FMI/co-simulation, water systems software reviews, open-source water modeling, and engineering education.

---

## Minor Issues

### m1. Definition 1: Will add specific operational performance criteria
### m2. Table 1: Will add domain-specificity column
### m3. Layer numbering: Will add rationale (descending fidelity = standard in MBD literature)
### m4. V-model: Will integrate into Figure 2
### m5. DfO-BIM: Will add specific data format connection (IFC extensions)
### m6. Cross-domain MBD: Will add comparison table (AUTOSAR, DO-178C, CHS-MBD)
