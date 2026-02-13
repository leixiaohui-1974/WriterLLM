# Review Report — Paper HZF-1 (Adv. Water Resour. v04)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The convergence analysis and temporal order verification from the control theorist's review have been thoroughly addressed. The paper is now technically complete. Two minor items remain.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Major Issues

None.

## Minor Issues

### m1. CUDA Compute Capability Requirements

The Software Availability section states "Compute Capability ≥ 7.0 (Volta)" but doesn't mention whether the code uses any Volta-specific features (tensor cores, cooperative groups). Clarify whether CC 7.0 is a hard requirement or if earlier GPUs (Pascal, CC 6.0) can run the code with reduced performance.

### m2. JSON Input Format Documentation

The JSON input format (§4.4) is described in one sentence. For reproducibility, provide at least one example JSON snippet or reference the documentation.

---

## Summary

Minor revision with two small clarifications. The paper is close to acceptance.
