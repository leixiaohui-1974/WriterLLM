# Review Report — Paper BAK-1 (Environ. Model. Softw. v04)

**Iteration**: 4 of 20+
**Reviewer**: B (Engineering Practitioner) — US water utility CTO
**Date**: 2026-02-13

---

## Overall Assessment

The manuscript has been transformed from my initial review. The testing infrastructure, reproducibility artifacts, component-level validation, performance benchmarks, IDZ accuracy bounds, and FMI step size guidance are all now present and well-documented. The digital twin and ML discussions add appropriate forward-looking content. Two minor items remain.

**Score: 8.5/10**
**Verdict: Minor Revision**

---

## Major Issues

None.

## Minor Issues

### m1. Docker Image Size and Availability

The Docker image `iwhr-chs/hydrocomponents:v1.0` is mentioned but: (a) what is the image size? OpenModelica images can be 2–5 GB, which may be prohibitive for some users. (b) Is the image hosted on Docker Hub or a private registry? State explicitly.

### m2. License Compatibility

The library is MIT-licensed, but it depends on OpenModelica (GPL) and the Modelica Standard Library (BSD). Clarify in the Software Availability section that the MIT license applies to HydroComponents source code only, and that runtime execution requires a Modelica compiler (OpenModelica recommended, GPL-licensed).

---

## Reference Verification

All references verified. Self-citation rate ~19%. Acceptable.

## Summary

Minor revision with two small clarifications needed. The paper is close to acceptance.
