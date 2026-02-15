# Response to Reviewer B — P2C Iteration 4

## m1. Commissioning and startup guidance

**Response**: Added §6.9 "Commissioning Pathway" describing a three-phase deployment: Phase 1 (months 1–3): Layer 1 Station Agents deployed at S1 and S4 (highest-impact stations) in shadow mode (computing recommendations without executing), validated against operator decisions. Phase 2 (months 4–6): Layer 1 active at all 8 stations + Layer 2 Segment Agents in shadow mode. Phase 3 (months 7–9): Full three-layer HDMPC active at WSAL-2. Acceptance criteria for each phase: (a) RMSE within 120% of SiL prediction, (b) zero ODD violations, (c) operator approval rate > 90%.

## m2. Cybersecurity considerations

**Response**: Added to §3.5: OPC UA communication uses TLS 1.3 encryption with certificate-based mutual authentication (IEC 62443 Security Level 2). Profinet communication is isolated on a dedicated VLAN with firewall-protected gateway. Intrusion detection: anomaly-based monitoring on System Agent commands (rate-of-change limits on setpoints, consistency checks against physical models). A compromised System Agent sending physically impossible setpoints (e.g., negative flow) would be rejected by the Segment Agent's local constraint checks (Eq. 6a-6b). The ODD framework provides an inherent safety layer: any command driving the system outside the ODD triggers the fallback protocol regardless of source.
