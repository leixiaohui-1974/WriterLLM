# Review Report — Paper YBK-1 (SoftwareX v02)

**Iteration**: 2 of 20+
**Reviewer**: C (Cross-disciplinary Scholar)
**Date**: 2026-02-13

---

## Overall Assessment

The revised manuscript addresses the major practical concerns well. The comparison table, software quality metrics, and scalability data are convincing additions. Two cross-disciplinary aspects need attention.

**Score: 7.5/10**
**Verdict: Minor Revision**

---

## Major Issues

### M1. No AI/ML Integration Pathway

The toolbox generates classical MPC controllers. How will it accommodate neural network-based controllers or hybrid physics-ML approaches that are increasingly used in water systems? A brief discussion of future extensibility for RL/neural MPC blocks would broaden appeal.

### M2. No ODD Integration with CKG-2

The toolbox generates controllers but does not include ODD monitoring capabilities from CKG-2 (Chen et al., 2026b). Since HydroRTP is part of the same tool chain, the ODD monitor should be a deployable block. At minimum, discuss the integration pathway.

---

## Minor Issues

### m1. Community Adoption Plan

SoftwareX values community impact. How will the toolbox be maintained? Is there a plan for community contributions? A brief statement on governance and sustainability would help.

### m2. Tutorial/Example Availability

The paper describes one example (3-pool flume). Are additional tutorials available in the repository?

---

## Summary

Two focused additions (AI/ML extensibility and ODD integration) would complete the paper.
