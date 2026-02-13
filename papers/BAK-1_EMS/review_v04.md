# Review Report — Paper BAK-1 (Environ. Model. Softw. v03)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European professor
**Date**: 2026-02-13

---

## Overall Assessment

The manuscript has improved significantly across two revisions. The software engineering aspects (testing, reproducibility, FAIR) are now exemplary for an EMS paper. The digital twin and hybrid ML discussions add appropriate breadth. However, as a control theorist, I find two technical concerns that require attention before acceptance.

**Score: 8.0/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. Automatic IDZ Parameter Derivation: Accuracy Bounds Not Provided

The paper claims that IDZ parameters ($A_s$, $\tau_d$, $\tau_m$) are "automatically derivable from the LSV model geometry" (§3.2, §4.2) and cites Lei (2025a, §4.7). However, no accuracy bounds are provided for this automatic derivation. The flume validation (§5.2) shows a 0.9–1.0 mm RMSE penalty for automatic vs. fitted parameters, but this is a single data point. For the library to be trustworthy for control design, users need to know:

- Under what conditions does the automatic derivation produce accurate parameters? (What range of pool lengths, slopes, flows?)
- What is the theoretical basis for the derivation? (Is it based on uniform flow assumption? Backwater profile linearization?)
- What is the expected accuracy degradation for non-standard cross-sections (circular, trapezoidal with varying side slopes)?

This is essential because a control designer using the auto-derived IDZ model for MPC needs to know the model uncertainty bounds to set appropriate robustness margins.

**Recommendation**: Add a §4.2.1 "Accuracy of Automatic IDZ Derivation" quantifying the derivation accuracy across the three validation systems and stating the underlying assumptions. Provide a table showing auto-derived vs. fitted IDZ parameters ($A_s$, $\tau_d$, $\tau_m$) for each system.

### M2. FMI Co-Simulation Step Size and Accuracy Coupling

The FMI co-simulation framework introduces a communication step size between the HydroComponents FMU and the external controller (e.g., Simulink MPC). The paper does not discuss how this step size affects:
- Plant simulation accuracy (does the LSV Preissmann scheme internal step size differ from the FMI communication step?)
- Control performance (what is the maximum FMI step size that preserves MPC stability?)
- Numerical stability at the FMI interface (zero-order hold vs. linear extrapolation of exchanged variables)

For a library that positions FMI export as a primary feature, this is a non-trivial omission. Users may experience degraded performance or even instability if the FMI step size is chosen incorrectly.

**Recommendation**: Add a paragraph in §4.3 discussing the FMI step size consideration. Provide guidance on recommended step size relative to the fastest system dynamics (e.g., $\Delta t_{FMI} \leq \tau_d / 5$ for IDZ models).

---

## Minor Issues

### m1. Transfer Function Implementation Detail

The IDZ transfer function (Eq. 3) contains a pure time delay $e^{-\tau_d s}$. How is this implemented in Modelica? Modelica's `delay()` operator, Padé approximation, or a buffer? The implementation choice affects simulation accuracy and FMI compatibility.

### m2. State Initialization for FMU

When an FMU is loaded by an external tool, how are the initial states set? For the LSV model, the initial water surface profile must be consistent with the boundary conditions. Is Newton iteration used for initialization? This is a practical issue users will face.

---

## Reference Verification

All 26 references verified. Self-citation rate: 5 Lei-group / 26 total = 19%. Acceptable.

## Summary

Minor revision. The two technical issues—IDZ derivation accuracy bounds and FMI step size guidance—are important for users relying on the library for control design. Once addressed, the paper will be ready for acceptance.
