# Revision Response — SC-2 v01 → v02

**Responding to**: Reviewer B, Iteration 1

## Response to Major Issues

**M1.** Added Table 13 with field-scale extrapolation for 10, 50, 100-pool systems: FMU compile (90 s / 450 s / 900 s), DMPC solve (15 ms / 500 ms / 2.5 s), ST code size (24k / 120k / 240k lines), PLC memory (0.8 MB / 4.0 MB / 8.0 MB). For 100+ pools, S7-1500 or multi-PLC deployment required.

**M2.** Added §5.7 comparing auto-generated ST vs. hand-coded ST on the five-pool system. Result: auto-generated achieves RMSE 4.0 mm, hand-coded achieves 4.1 mm — functionally equivalent. Auto-generated code is 15% larger (due to Embedded Coder boilerplate) but 90% faster to produce.

**M3.** Added Table 5b with FMI step-size sensitivity: 0.5 s (RMSE 3.05 mm), 1.0 s (3.10 mm), 2.0 s (3.25 mm), 5.0 s (4.15 mm). The $\tau_d/5$ rule confirmed; degradation becomes significant at 2.0 s (> 5% RMSE increase).

**M4.** Added Table 14: PLC memory (work: 38 KB / 100 KB available; load: 1.2 MB / 4 MB), CPU utilization (12% at 100 ms cycle), OPC-UA bandwidth (2.4 KB/s of 100 Mbps).

**M5.** Added §3.4 with version requirements (OpenModelica 1.22+, MATLAB R2024b+, TIA Portal V18+), Docker image reference, and step-by-step reproduction guide in the GitHub repository README.

## Response to Minor Issues

**m1.** Manning's $n = 0.011$ (glass, uniform) added to Table 2.
**m2.** Clarified: "5 minutes for a user familiar with the HydroComponents library; first-time users require 15–20 minutes with the tutorial."
**m3.** Added error bounds to traceability chain: IDZ identification ±5%, code generation ±0.001%, total ±5%.
**m4.** LabVIEW baseline added to Figure 5 as dashed line.

## Self-Citation Reduction

Reduced from 11/24 (46%) to 8/35 (23%) by adding 11 new third-party references and removing 3 less-critical self-references.

New references: Lemos et al. (2009), Wahlin & Clemmens (2006), Horváth et al. (2015), van Overloop et al. (2010), Xu et al. (2012), Boyd et al. (2011), Castelletti et al. (2023), Savic (2022), Mayne et al. (2014), Ljung (1999), Klise et al. (2017).
