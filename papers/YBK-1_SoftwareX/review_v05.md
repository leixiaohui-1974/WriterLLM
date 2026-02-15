# Review Report — Paper YBK-1 (SoftwareX v04)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner)
**Date**: 2026-02-13

---

## Overall Assessment

The paper is now comprehensive. The QP convergence handling, EKF option, code determinism note, and ODD monitor integration address all remaining concerns. Two minor practical items.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Minor Issues

### m1. License Compatibility Clarification

HydroRTP is MIT but requires MATLAB (commercial) and Embedded Coder (commercial add-on). The paper should explicitly state the cost implications for different user scenarios (academic vs. commercial vs. simulation-only).

### m2. Version Numbering Strategy

The paper mentions v1.0.0 and v1.1 (with ODD monitor). What is the semantic versioning policy? Minor for new blocks, major for breaking API changes?

---

## Summary

These are truly minor. The paper is ready for acceptance after addressing these two items.
