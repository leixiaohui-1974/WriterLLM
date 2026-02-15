# Review — P2C Iteration 4

**Reviewer**: B (Engineering Practitioner)
**Draft reviewed**: v04
**Score**: 8.5 / 10
**Verdict**: Minor Revision

---

## Summary

The paper has matured significantly. The stability analysis (§3.6) addresses the theoretical concerns, the RL positioning (§6.6) and demand sensitivity (§6.7) are excellent additions, and the economic case is clear. Two minor practical issues remain.

## Minor Issues

### m1. Commissioning and startup guidance
The paper describes the steady-state HDMPC architecture but provides no guidance on how to commission the system. How does an operator transition from the current rule-based dispatch to HDMPC? Is there a phased deployment plan (e.g., Layer 1 first, then Layer 2, then Layer 3)? What are the acceptance criteria for each phase?

### m2. Cybersecurity considerations
A 302 km pipeline with fiber-optic and cellular communication is a potential cybersecurity target. The paper mentions OPC UA and Profinet but does not discuss security measures (encryption, authentication, intrusion detection). For a WSAL-2 system where the controller recommends pump operations, a compromised System Agent could cause significant physical damage.

## Recommendation

Minor revision to address commissioning pathway and cybersecurity. The paper is otherwise ready for acceptance.
