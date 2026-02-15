# Review Report — Paper HZF-1 (Adv. Water Resour. v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar) — Asian AI+water researcher
**Date**: 2026-02-13

---

## Overall Assessment

The revised manuscript is substantially strengthened. Field data validation, weak scaling, branching topology support, and energy efficiency analysis address the previous reviewer's concerns comprehensively. The paper is now competitive for AWR. Two discussion-level issues remain.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. No Connection to ML-Based Surrogate Acceleration

GPU computing for SVE is one approach to real-time simulation; ML-based surrogates (learned emulators, neural operators) are another. The paper should discuss how cuSVE relates to the ML surrogate approach—is it complementary (cuSVE generates training data for surrogates)? Competitive (physics-based GPU solver vs. learned emulator)? This context is important for the AWR audience.

**Recommendation**: Add a paragraph in §6 comparing cuSVE's physics-based GPU acceleration with ML surrogate approaches (e.g., DeepONet, Fourier Neural Operator) and discussing complementarity.

### M2. No Mention of Multi-GPU or Cloud Deployment

For very large networks (>500 pools), a single GPU may be insufficient. The paper should discuss the pathway to multi-GPU scaling (e.g., NCCL for inter-GPU communication) and cloud deployment (e.g., AWS/Azure GPU instances). This is increasingly important for operational digital twin deployments.

**Recommendation**: Add a brief discussion in §6.3 or a new §6.4 about multi-GPU scaling and cloud deployment pathways.

---

## Minor Issues

### m1. Roofline Analysis

A roofline model analysis would help readers understand whether cuSVE is compute-bound or memory-bound, and how much headroom remains for optimization.

### m2. Reproducibility of Speedup Numbers

Speedup depends heavily on the CPU baseline. HEC-RAS runs single-threaded; a fair comparison might include OpenMP-parallel CPU as the baseline.

---

## Summary

Minor revision. The two discussion items (ML surrogates and multi-GPU) would complete the paper's positioning within the modern computational water resources landscape.
