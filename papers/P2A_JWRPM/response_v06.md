# Response to Review — Paper P2A Iteration 4

**Reviewer**: B (Engineering Practitioner, 2nd review)
**Review Score**: 8.5/10 — Minor Revision

---

## Minor Issues

### m1. Shadow-Mode Deployment
**Response**: Accepted. Shadow-mode operation is indeed the natural intermediate step between MiL and field commissioning, and is standard practice in power systems (economic dispatch shadow mode) and autonomous vehicles (safety driver override mode). We will add 2–3 sentences in §7.1 describing shadow-mode as a pre-SiL operational validation step: the MAS runs alongside human operators, producing control recommendations that are logged and scored against actual human decisions, providing both algorithmic validation and operator familiarization without operational risk.

### m2. Interoperability and Open Standards
**Response**: Accepted. For WSAL to serve as a genuine industry framework, open standardization of agent interfaces is essential. We will add a brief note in §8.3 acknowledging the need for open WSAL specifications — including standardized ODD description format, agent communication protocol (analogous to IEC 61850 for power substations), and Layer 0 safety interface — developed under international auspices (IAHR/IWA/ISO).
