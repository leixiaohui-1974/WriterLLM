# Review Report — SC-2 v01 → v02

**Reviewer**: B (Engineering Practitioner)
**Iteration**: 1

## Overall Assessment

The paper demonstrates a genuinely useful toolchain integration that fills an important gap in the CHS ecosystem. The five-pool xIL demonstration is convincing, and the engineering productivity analysis (Table 12) provides quantifiable value. However, several practical gaps need addressing.

**Score**: 6.5 / 10
**Verdict**: **Major Revision**

## Major Issues

**M1. No field-scale extrapolation.** The five-pool flume (12 m, 2 L/s) is far from a field canal (20 km, 10 m³/s). Add a table extrapolating the toolchain performance metrics (FMU compile time, DMPC solve time, ST code size, PLC memory) to 10, 50, and 100-pool field-scale systems.

**M2. Manual baseline HiL not shown.** Table 11 compares with LabVIEW baseline but not with the "manual ST coding" baseline from Table 12. Show that the auto-generated ST code achieves equivalent or better performance than hand-coded ST on the same five-pool system.

**M3. FMI step-size sensitivity not analyzed.** The communication step size is set to 1.0 s based on the $\tau_d/5$ rule, but no sensitivity analysis is provided. Test 0.5 s, 1.0 s, 2.0 s, and 5.0 s step sizes to verify the rule and quantify degradation.

**M4. PLC resource profiling missing.** Report PLC memory usage (work memory, load memory), CPU utilization, and communication bandwidth for the five-pool DMPC deployment.

**M5. Installation and deployment reproducibility.** The paper claims open-source toolchain but does not specify version requirements (OpenModelica version, MATLAB version, TIA Portal version), Docker availability, or step-by-step installation guide.

## Minor Issues

**m1.** Table 2: Add Manning's roughness $n$ for each pool (or state if uniform).
**m2.** Section 3.1: "Assembly time: approximately 5 minutes" — is this for an expert user? Clarify.
**m3.** Eq. (2) traceability chain is conceptually useful but should include error bounds at each step.
**m4.** Figure 5 should include the LabVIEW baseline response for direct visual comparison.

## Reference Audit

- Self-citation rate ~11/24 = 46% — significantly ABOVE the 25% limit. Must be reduced.
- Missing: Lemos et al. (2009) for adaptive canal MPC
- Missing: Wahlin & Clemmens (2006) for branching canal control
- Missing: Horváth et al. (2015) for gate opening vs. discharge control

## Recommendation

Major revision. Core contribution is strong but needs field-scale projection, manual baseline comparison, FMI sensitivity, and self-citation reduction.
