# Review Report — Paper YBK-1 (SoftwareX v01)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The paper presents a useful toolbox that addresses a genuine pain point in water systems control: the design-to-deployment gap. The one-click workflow from Simulink to PLC is appealing. However, SoftwareX papers require rigorous software quality evidence that is currently lacking.

**Score: 6.5/10**
**Verdict: Major Revision**

---

## Major Issues

### M1. No Software Quality Metrics

SoftwareX expects evidence of software quality: test coverage, static analysis results, coding standards compliance. The paper mentions "built-in unit tests via Simulink Test" (§2.1) but provides no data. How many tests? What coverage? What is the test pass rate? The MISRA-C:2012 compliance claim (§2.3) needs evidence: which rules are checked, which are waived, and why?

### M2. Comparison with Existing Tools Missing

No comparison with existing Simulink-to-PLC workflows. MathWorks already offers Simulink PLC Coder as a commercial product. How does HydroRTP differ? What does it add beyond the standard MathWorks toolchain? Without this comparison, the novelty claim is unclear. Also, other academic tools exist (e.g., OPENMODELICA's code generation, Ptolemy II) that should be discussed.

### M3. Reproducibility Concerns

The paper claims open-source (MIT license, GitHub) but the repository is "to be made public upon acceptance." SoftwareX requires functional code at review time. At minimum, the metadata table should include: (a) DOI (Zenodo), (b) specific MATLAB version tested, (c) Simulink Embedded Coder license requirement (commercial, not free), and (d) instructions for users without Embedded Coder.

### M4. No Scalability Evidence Beyond 3 Pools

The 3-pool flume is a small system. How does HydroRTP scale? What is the code generation time for 10, 50, 100 pools? What is the PLC memory usage? Does the QP solver remain real-time feasible for 50-pool DMPC? These questions are critical for practitioners considering deployment on real canal systems.

### M5. Limited Self-Citation Context

The paper cites 5 Lei-group papers out of 12 total = 42%. This exceeds the 25% guideline. Add external references to bring the rate down to 20-25%.

---

## Minor Issues

### m1. No Installation Instructions in Paper

SoftwareX papers typically include a brief installation section or point to comprehensive documentation.

### m2. Floating-Point Precision Discussion

Table 1 shows max 1.0 mm difference due to single vs. double precision. For safety-critical applications, this discrepancy needs quantification: under what conditions does single precision cause constraint violations that double precision avoids?

### m3. DMPC Communication Protocol

§2.2 mentions "shared memory (SiL) or Profinet/EtherNet/IP (HiL/PiL)" but does not specify the communication overhead or latency for the PLC-to-PLC case.

---

## Summary

The toolbox addresses a real need but requires: (1) software quality evidence, (2) comparison with Simulink PLC Coder, (3) reproducibility improvements, (4) scalability data, and (5) self-citation adjustment.
