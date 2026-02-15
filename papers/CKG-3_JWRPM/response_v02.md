# Revision Response — CKG-3 v01 → v02

**Responding to**: Reviewer B, Iteration 1

## Response to Major Issues

**M1. Five-pool canal flume description.**
Added Table 2b with complete five-pool specifications: gate geometry (undershot vertical sluice, 0–15 cm opening), pump head-flow curve (linear approximation 0–5 L/s at 1.2 m head), downstream boundary (free overfall), Manning's n = 0.012 (acrylic), and IDZ parameters for all five pools at the nominal operating point. Added Section 2.3.1 with full instrumentation details.

**M2. Individual scenario results.**
Added Figure 6 showing a representative five-pool HiL scenario (B3: upstream flow step +30%): water levels in all five pools, gate positions, RLS-estimated $\tau_d$ for each pool, and Area Agent ODD status. Added Figure 7 showing the 10-pool cascading disturbance scenario (C15) with the full MAS coordination response.

**M3. RLS convergence and stability analysis.**
Added Section 4.2.1 with: (a) persistent excitation condition (minimum input SNR > 3 dB required, derived from Ljung 1999 Ch. 9); (b) steady-state behavior — covariance matrix $\mathbf{P}$ growth is bounded by the forgetting factor reset mechanism (reset to $\mathbf{P}_0$ when trace exceeds $10 \times$ trace($\mathbf{P}_0$)); (c) Table 3b with $\lambda$ sensitivity analysis (0.95, 0.97, 0.98, 0.99) showing RMSE and parameter estimation variance across 16 boundary scenarios. Optimal range is $\lambda \in [0.97, 0.99]$; $\lambda = 0.98$ is confirmed as a good compromise.

**M4. Cost-benefit analysis.**
Added Table 10 comparing Arduino vs. S7-1200 vs. S7-1500 across cost, performance, scalability, and compliance dimensions. Key finding: PLC cost ($700 + TIA Portal $3,000) is < 0.1% of typical canal automation project cost ($1–5M), making it negligible for field deployment but significant for teaching labs where Arduino remains a valid choice for WSAL-1/2 demonstration.

**M5. Cybersecurity discussion.**
Added Section 7.4.1 with IEC 62443 security level mapping table. Current implementation achieves SL-1 (basic protection): OPC-UA with TLS 1.2, username/password authentication, read-only SCADA access by default. Gaps identified for SL-2: network segmentation (PROFINET isolation), access logging, and firmware signing. The S7-1200 supports these features natively but they were not activated for this laboratory study.

## Response to Minor Issues

**m1.** Cost row added to Table 1.
**m2.** Added online delay estimation: $d$ is now estimated by testing $d \in \{1, 2, 3, 4\}$ and selecting the value minimizing the ARX prediction error, re-evaluated every 100 samples (500 s). Section 4.2 updated.
**m3.** Bumpless transfer detailed: exponential blending applied to the control output $u(k) = w(k) \cdot u_{\text{new}}(k) + (1-w(k)) \cdot u_{\text{old}}(k)$ where $w(k) = 1 - e^{-k/\tau_b}$, $\tau_b = 2$ samples. Section 4.3 updated.
**m4.** Steady-state assumption stated explicitly after Eq. (4).
**m5.** Added discussion in Section 6.5: for field-scale canals (e.g., 10-pool benchmark with $h \in [1.0, 3.0]$ m), the 12% expansion translates to 24 cm on each side — meaningful for operational flexibility. The dual-tank 3-cm expansion is a proof of protocol.

## References Added

- Åström, K. J., & Wittenmark, B. (2008). Adaptive Control (2nd ed.). Dover.
- Wahlin, B. T., & Clemmens, A. J. (2006). Automatic downstream water-level feedback control of branching canal networks. Journal of Irrigation and Drainage Engineering, 132(6), 598–609.
- Lemos, J. M., Machado, F., Nogueira, N., Rato, L., & Rijo, M. (2009). Adaptive and non-adaptive model predictive control of an irrigation channel. Networks and Heterogeneous Media, 4(2), 303–324.
- Ye et al. (2026) clarified as P2B (Shaoping SiL+ODD+MAS), cross-referenced with paper ID.
