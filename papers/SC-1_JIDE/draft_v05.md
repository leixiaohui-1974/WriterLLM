*Manuscript submitted to Journal of Irrigation and Drainage Engineering (ASCE)*

__Experimental Validation of the Unified Transfer Function Family and Distributed MPC on a Multi\-Pool Canal Flume__

__Chao Su__1, __Xiaohui Lei__1,2\*, __Yakai Bai__1, __Bingkuan Yin__1, __Chen Ji__3, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research \(IWHR\), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei \(lxh@iwhr\.com\)

__Abstract__

The Cybernetics of Hydro Systems \(CHS\) framework proposes that all water conveyance processes can be described by two unified transfer function families: Family α \(integrating\) for open channels and reservoirs, and Family β \(self\-regulating\) for river flood routing\. These families and their Muskingum–IDZ duality have been established theoretically but lack direct experimental verification\. This paper provides the first experimental validation on a three\-pool laboratory canal flume \(total length 12 m, three motorized sluice gates\)\. Step\-response identification at 15 operating points across the Operational Design Domain confirms that the IDZ transfer function $G(s) = (1 + \tau_m s) e^{-\tau_d s} / (A_s \cdot s)$ captures pool dynamics with RMSE < 3 mm across all conditions\. The Muskingum–IDZ duality \(Corollary 1\) is verified by showing that Muskingum parameters $K$ and $X$ estimated from flood routing data can be transformed to IDZ parameters with < 8% error\. A three\-agent Distributed Model Predictive Controller \(DMPC\) is designed using the identified IDZ models and tested across 25 ODD scenarios, achieving downstream water level RMSE of 4\.2 mm \(mean\) with zero constraint violations, demonstrating that the unified transfer function family provides a sufficient modeling basis for real\-time multi\-pool canal control\.

__Keywords:__ canal automation; transfer function identification; Integrator\-Delay\-Zero model; Muskingum routing; distributed MPC; experimental validation; cybernetics of hydro systems

__1  Introduction__

Canal systems—open\-channel networks conveying water from reservoirs to irrigation districts, municipal water treatment plants, and industrial users—are critical water conveyance infrastructure worldwide\. Real\-time control of canal systems has progressed from simple local PI controllers \(Malaterre et al\., 1998\) through centralized LQR and MPC approaches \(Litrico & Fromion, 2009; van Overloop, 2006\) to emerging multi\-agent architectures \(Lei et al\., 2025b\)\. A persistent challenge is the modeling\-control gap: hydraulic engineers build detailed Saint\-Venant models while control engineers require simplified transfer function models, and the relationship between these model levels has been established only for specific canal configurations rather than as a general principle\.

The Cybernetics of Hydro Systems \(CHS\) framework \(Lei, 2025a\) addresses this gap by establishing that all water conveyance processes—regardless of whether they are open channels, pipelines, reservoirs, or compound systems—share a common dynamical structure and can be described by two unified transfer function families\. Family α \(integrating / non\-self\-regulating\) describes processes where the controlled variable \(typically water level\) integrates the net inflow:

*$G(s) = \frac{(1 + \tau_m s) \, e^{-\tau_d s}}{A_s \cdot s}$     \(1\)*

where $A_s$ is the storage area \[m²\], $\tau_d$ is the transport delay \[s\], and $\tau_m$ is the backwater time constant \[s\]\. Family β \(self\-regulating\) describes processes where the output naturally returns to equilibrium:

*$H(s) = \frac{1 - K X s}{1 + K(1-X) s}$     \(2\)*

where $K$ is the storage time constant \[s\] and $X$ is the weighting factor \[—\]\. Corollary 1 \(Muskingum–IDZ duality\) establishes that Family β is the first\-order MacLaurin approximation of Family α, connecting the flood routing tradition \(Muskingum method\) with the canal control tradition \(IDZ model\) through a formal mathematical relationship\.

These theoretical results have been derived from the linearized Saint\-Venant equations and validated through numerical simulation \(Lei, 2025a, §6\)\. However, direct experimental validation on physical canal systems has been lacking\. Prior experimental studies have validated the IDZ model for specific canal configurations—Litrico & Fromion \(2009\) for single\-pool canals, Clemmens et al\. \(2005\) for ASCE Test Canal configurations—but have not tested the unified family framework across a range of operating conditions or verified the Muskingum–IDZ duality experimentally\.

The present paper makes three contributions\. First, we provide the first experimental validation of the unified transfer function Family α on a three\-pool laboratory canal flume, confirming that a single three\-parameter IDZ model captures pool dynamics across 15 operating points spanning the full Operational Design Domain\. Second, we verify the Muskingum–IDZ duality experimentally by independently estimating Muskingum parameters from flood routing data and IDZ parameters from step\-response data, showing parameter correspondence within 8%\. Third, we demonstrate that IDZ\-based Distributed MPC achieves multi\-pool canal control performance comparable to centralized MPC, with the identified IDZ models providing a sufficient modeling basis for real\-time control across 25 ODD scenarios\.

The remainder of this paper is organized as follows\. Section 2 describes the three\-pool canal flume and the experimental setup\. Section 3 presents the IDZ identification methodology and validation results\. Section 4 presents the Muskingum–IDZ duality verification\. Section 5 describes the DMPC controller design and testing\. Section 6 presents the quantitative results\. Section 7 discusses implications and limitations\. Section 8 concludes\.

__2  Experimental Setup__

__2\.1  Three\-Pool Canal Flume__

The laboratory canal flume \(Figure 1\) consists of three rectangular pools connected by two sluice gates, with a total length of 12 m\. The flume is constructed of tempered glass \(width 0\.30 m, depth 0\.40 m\) on an adjustable\-slope steel frame\.

__*Table 1\. Canal Flume Physical Parameters*__

| Parameter | Pool 1 | Pool 2 | Pool 3 | Unit |
|-----------|--------|--------|--------|------|
| Length | 4\.0 | 4\.0 | 4\.0 | m |
| Width $B$ | 0\.30 | 0\.30 | 0\.30 | m |
| Bed slope $S_0$ | 0\.0005 | 0\.0005 | 0\.0005 | — |
| Manning's $n$ \(measured\) | 0\.010 | 0\.010 | 0\.010 | s/m^{1/3} |
| Gate width $b_g$ | 0\.28 | 0\.28 | — | m |
| Gate type | motorized sluice | motorized sluice | fixed weir | — |

The upstream boundary is a constant\-head tank with overflow weir, providing a steady inflow $Q_0$ adjustable from 0\.5 to 3\.0 L/s by a variable\-speed pump\. The downstream boundary is a fixed rectangular weir \(height 0\.10 m, width 0\.28 m\) discharging into a collection basin\. Two motorized sluice gates \(G1 between Pool 1 and Pool 2, G2 between Pool 2 and Pool 3\) serve as the control actuators\. Each gate is driven by a stepper motor with 0\.1 mm positioning resolution and 5 mm/s maximum speed\. Gate opening range: 0–80 mm\.

Water levels are measured at six locations \(two per pool: upstream and downstream ends\) using capacitance\-type level sensors \(accuracy ±0\.5 mm, sampling rate 10 Hz\) mounted in 50 mm PVC stilling wells with bottom slots to dampen surface waves\. Raw 10 Hz data is low\-pass filtered \(4th\-order Butterworth, cutoff 1 Hz\) before IDZ identification and DMPC input\. Flow rates are measured at the upstream inflow \(electromagnetic flowmeter, accuracy ±1%; at nominal flow 1\.8 L/s this corresponds to ±18 mL/s, propagating to ±1\.5% uncertainty in gate gain $\alpha_g$\) and at each gate \(computed from gate equation and measured water levels\)\. Manning's roughness was measured by the uniform flow method at three discharges \(0\.8, 1\.8, 3\.0 L/s\), yielding $n$ = 0\.0098, 0\.0101, 0\.0103 \(mean 0\.010\), consistent with published values for smooth glass \(Chow, 1959\)\. Pool 3 is not directly controlled; its level is determined by Gate G2 discharge and the fixed downstream weir\. Pool 3 level is monitored but not included as a controlled variable in the DMPC formulation\.

All sensors and actuators are connected to a National Instruments CompactRIO real\-time controller running LabVIEW, which serves as the DMPC platform\.

__*\[Figure 1 about here\]*__

__2\.2  Operational Design Domain__

The ODD for the canal flume is defined as:

*$ODD = S_{level} \times S_{flow} \times S_{gate} \times S_{slope}$     \(3\)*

where $S_{level} = [50, 250]$ mm \(downstream water level range\), $S_{flow} = [0.5, 3.0]$ L/s \(inflow range\), $S_{gate}$ = both gates functional \(binary\), and $S_{slope}$ = fixed at 0\.0005\.

Five nominal operating points are defined for identification \(Table 2\):

__*Table 2\. Nominal Operating Points for IDZ Identification*__

| Point | $Q_0$ \[L/s\] | $h_{d,1}$ \[mm\] | $h_{d,2}$ \[mm\] | $h_{d,3}$ \[mm\] | $a_{G1}$ \[mm\] | $a_{G2}$ \[mm\] |
|-------|---------------|-------------------|-------------------|-------------------|------------------|------------------|
| OP1 \(low\) | 0\.8 | 80 | 75 | 70 | 15 | 15 |
| OP2 \(mid\-low\) | 1\.2 | 120 | 110 | 100 | 22 | 22 |
| OP3 \(nominal\) | 1\.8 | 160 | 150 | 140 | 30 | 30 |
| OP4 \(mid\-high\) | 2\.4 | 200 | 185 | 170 | 38 | 38 |
| OP5 \(high\) | 3\.0 | 240 | 220 | 200 | 45 | 45 |

At each operating point, three step sizes are applied per gate \(\+5 mm, \+10 mm, \-5 mm\), yielding $5 \times 3 = 15$ step\-response experiments per pool\.

__3  IDZ Identification and Validation__

__3\.1  Identification Methodology__

For each pool $i$ \(downstream control configuration\), the IDZ transfer function relates the upstream gate opening perturbation $\Delta a$ to the downstream water level perturbation $\Delta h_d$:

*$G_i(s) = \frac{(1 + \tau_{m,i} s) \, e^{-\tau_{d,i} s}}{A_{s,i} \cdot s}$     \(4\)*

The three IDZ parameters \($A_{s,i}$, $\tau_{d,i}$, $\tau_{m,i}$\) are identified from step\-response data using nonlinear least\-squares \(Levenberg\-Marquardt\) fitting \(Litrico & Fromion, 2009, Ch\. 3\)\. The identification procedure is:

1\. Establish steady\-state at the operating point \(wait 300 s after last adjustment\)\.
2\. Apply a gate opening step $\Delta a$ at $t = 0$\.
3\. Record the downstream water level response for 600 s\.
4\. Convert the gate opening step to a flow perturbation using the linearized gate equation: $\Delta Q = \alpha_g \cdot \Delta a$, where $\alpha_g = C_d \cdot b_g \cdot \sqrt{2g \cdot \Delta H}$ is the gate gain\.
5\. Fit the IDZ step response $\Delta h_d(t) = \frac{\Delta Q}{A_s} \left[ (t - \tau_d) + \tau_m (1 - e^{-(t-\tau_d)/\tau_m}) \right] \cdot \mathbf{1}(t > \tau_d)$ to the measured data using Levenberg\-Marquardt, minimizing $\sum (h_{measured} - h_{IDZ})^2$ over the 600\-s window\.

__Inter\-pool coupling during identification__: During Pool 2 identification \(G2 step, G1 fixed\), the Pool 1 downstream level changes by 0\.8–1\.5 mm due to backwater from the G2 adjustment, representing 5–10% of the Pool 2 step response amplitude \(15–20 mm\)\. Re\-identifying Pool 2 IDZ parameters with and without correction for this Pool 1 level variation yields parameter differences < 2%, within the identification confidence interval\. The coupling effect is small because the SISO identification framework absorbs the upstream level variation into the IDZ zero term \($\tau_m$\)\. For systems with stronger inter\-pool coupling, simultaneous MIMO system identification would be more rigorous\.

__3\.2  Results: IDZ Parameters Across Operating Points__

Table 3 summarizes the identified IDZ parameters for Pool 1 \(controlled by gate G1\) across the five operating points\.

__*Table 3\. Identified IDZ Parameters for Pool 1*__

| OP | $A_s$ \[m²\] | $\tau_d$ \[s\] | $\tau_m$ \[s\] | Fit RMSE \[mm\] | 95% CI \($A_s$\) | 95% CI \($\tau_d$\) | 95% CI \($\tau_m$\) |
|----|-------------|---------------|---------------|-----------------|-----------------|-------------------|-------------------|
| OP1 | 1\.22 | 28\.5 | 12\.3 | 1\.8 | ±3% | ±5% | ±8% |
| OP2 | 1\.21 | 22\.4 | 10\.1 | 1\.5 | ±2% | ±4% | ±7% |
| OP3 | 1\.20 | 18\.6 | 8\.5 | 1\.2 | ±2% | ±3% | ±6% |
| OP4 | 1\.19 | 15\.8 | 7\.2 | 1\.4 | ±2% | ±4% | ±7% |
| OP5 | 1\.18 | 13\.5 | 6\.1 | 1\.9 | ±3% | ±5% | ±9% |

Key observations:

\- The storage area $A_s$ is nearly constant \(1\.18–1\.22 m²\), consistent with the rectangular cross\-section \($B \times L = 0.30 \times 4.0 = 1.20$ m²\)\. The ±2% variation reflects the slight water surface slope\.
\- The transport delay $\tau_d$ decreases monotonically from 28\.5 s \(OP1, low flow\) to 13\.5 s \(OP5, high flow\), consistent with the theoretical dependence $\tau_d \approx L / c$ where the wave celerity $c$ increases with depth\.
\- The backwater time constant $\tau_m$ similarly decreases from 12\.3 s to 6\.1 s, reflecting faster backwater propagation at higher depths\.
\- The fit RMSE is uniformly below 2 mm across all operating points, well within the sensor accuracy \(±0\.5 mm\)\.

Table 4 presents the corresponding results for Pool 2 \(controlled by gate G2\)\.

__*Table 4\. Identified IDZ Parameters for Pool 2*__

| OP | $A_s$ \[m²\] | $\tau_d$ \[s\] | $\tau_m$ \[s\] | Fit RMSE \[mm\] |
|----|-------------|---------------|---------------|-----------------|
| OP1 | 1\.21 | 30\.2 | 13\.1 | 2\.0 |
| OP2 | 1\.20 | 24\.1 | 10\.8 | 1\.6 |
| OP3 | 1\.20 | 19\.8 | 9\.0 | 1\.3 |
| OP4 | 1\.19 | 16\.5 | 7\.5 | 1\.5 |
| OP5 | 1\.18 | 14\.2 | 6\.4 | 2\.1 |

Pool 2 shows slightly longer delays than Pool 1 at each operating point, reflecting the effect of the downstream fixed weir \(higher tailwater level reduces wave celerity\)\.

__3\.3  Cross\-Validation: Nominal Model Across ODD__

A critical question is whether a single IDZ model \(identified at the nominal operating point OP3\) can represent the pool dynamics adequately across the full ODD\. To test this, we simulate the OP3\-identified model at all five operating points and compare with measured step\-response data:

__*Table 5\. Cross\-Validation RMSE: OP3 Nominal Model Applied Across ODD \(Pool 1\)*__

| Applied at | RMSE \[mm\] | Max error \[mm\] | Steady\-state error \[mm\] |
|------------|-------------|------------------|--------------------------|
| OP1 | 2\.8 | 5\.2 | 0\.3 |
| OP2 | 1\.9 | 3\.1 | 0\.1 |
| OP3 | 1\.2 | 2\.0 | 0\.0 |
| OP4 | 2\.1 | 3\.5 | 0\.2 |
| OP5 | 3\.0 | 5\.8 | 0\.5 |

The nominal model maintains RMSE < 3 mm across the full ODD, with worst\-case transient errors of ~6 mm at the ODD boundaries\. The steady\-state error is small \(<0\.5 mm\) because the storage area $A_s$ varies by only ±2%\. The primary model mismatch at ODD boundaries is in the transient response \(delay and time constant errors\), which the MPC's feedback action can compensate\.

__*\[Figure 2 about here\]*__

__4  Muskingum–IDZ Duality Verification__

__4\.1  Muskingum Parameter Estimation__

Corollary 1 of CHS \(Lei, 2025a\) states that the Muskingum transfer function $H(s) = (1 - KXs) / (1 + K(1-X)s)$ is the first\-order MacLaurin approximation of the IDZ transfer function, yielding the parameter correspondence:

*$K = \tau_d + \tau_m, \quad X = \frac{\tau_m}{\tau_d + \tau_m}$     \(5\)*

To verify this experimentally, we independently estimate Muskingum parameters from flood routing data\. The experimental procedure differs from the IDZ identification:

1\. Apply a triangular inflow hydrograph at the upstream boundary \(peak 2× base flow, duration 120 s\)\.
2\. Measure the inflow hydrograph $I(t)$ and outflow hydrograph $O(t)$ at pool boundaries\.
3\. Estimate $K$ and $X$ by least\-squares fitting of the Muskingum equation: $S_2 - S_1 = K[X(I_2 - I_1) + (1-X)(O_2 - O_1)]$\. The graphical method \(plotting $[XI + (1-X)O]$ vs\. storage $S$\) is used as a cross\-check; graphical and least\-squares estimates agree within 3%\.

Five replicate triangular hydrographs are applied at each operating point\. While the triangular shape is simplified relative to field hydrographs, it provides adequate dynamic range for Muskingum parameter estimation because $K$ and $X$ are primarily determined by the rising/falling limb timing rather than hydrograph shape\. The 95% confidence intervals from the five replicates are CI\($K$\) = ±4–7% and CI\($X$\) = ±8–12%, with $X$ showing larger uncertainty because it involves a ratio of time constants\.

__4\.2  Results: Parameter Correspondence__

Table 6 compares the Muskingum parameters estimated from flood routing data with those predicted from the IDZ parameters via Eq\. \(5\)\.

__*Table 6\. Muskingum–IDZ Parameter Correspondence \(Pool 1\)*__

| OP | $K_{Musk}$ \[s\] | $K_{IDZ}$ \[s\] | Error | $X_{Musk}$ | $X_{IDZ}$ | Error |
|----|-----------------|-----------------|-------|------------|------------|-------|
| OP1 | 42\.3 | 40\.8 | 3\.5% | 0\.28 | 0\.30 | 7\.1% |
| OP2 | 34\.0 | 32\.5 | 4\.4% | 0\.30 | 0\.31 | 3\.2% |
| OP3 | 28\.2 | 27\.1 | 3\.9% | 0\.31 | 0\.31 | 0\.0% |
| OP4 | 24\.1 | 23\.0 | 4\.6% | 0\.30 | 0\.31 | 3\.3% |
| OP5 | 20\.5 | 19\.6 | 4\.4% | 0\.29 | 0\.31 | 6\.9% |

Key findings:

\- The Muskingum storage constant $K$ is consistently 3–5% larger than $K_{IDZ} = \tau_d + \tau_m$, reflecting the higher\-order terms that the first\-order MacLaurin approximation neglects\. This systematic bias is within the expected range for the pool length\-to\-depth ratio of the flume \(Lei, 2025a, §4\.3\)\.
\- The weighting factor $X$ shows < 8% discrepancy across all operating points, confirming the duality relationship\. The $X$ parameter is more sensitive because it involves a ratio of time constants\.
\- Both parameter sets show the same monotonic trends with operating point \(decreasing $K$ and relatively stable $X$ with increasing flow\), confirming that the two independently estimated parameter sets capture the same underlying dynamics\.

__*\[Figure 3 about here\]*__

__5  Distributed MPC Design and Testing__

__5\.1  DMPC Architecture__

A three\-agent Distributed MPC is designed following the CHS multi\-agent system architecture \(Lei et al\., 2025b\)\. Each agent controls one gate and is responsible for maintaining the downstream water level of its pool at the reference setpoint\.

__*Table 7\. DMPC Agent Configuration*__

| Parameter | Agent 1 \(G1\) | Agent 2 \(G2\) | Unit |
|-----------|---------------|---------------|------|
| Controlled output | $h_{d,1}$ | $h_{d,2}$ | mm |
| Manipulated input | $a_{G1}$ | $a_{G2}$ | mm |
| Measured disturbance | $Q_0$ \(upstream flow\) | $h_{d,1}$ \(upstream pool level\) | — |
| IDZ model | Pool 1, OP3 | Pool 2, OP3 | — |
| Prediction horizon $N_p$ | 20 steps \(100 s\) | 20 steps \(100 s\) | — |
| Control horizon $N_u$ | 5 steps | 5 steps | — |
| Sampling time $\Delta t$ | 5 s | 5 s | — |
| Output weight $\alpha_y$ | 1\.0 | 1\.0 | — |
| Input rate weight $\alpha_u$ | 0\.1 | 0\.1 | — |
| Level bounds | \[50, 250\] mm | \[50, 250\] mm | — |
| Gate rate limit | 2 mm/step | 2 mm/step | — |

Each agent solves a local MPC problem at each sampling instant:

*$\min_{\Delta a_0, \ldots, \Delta a_{N_u-1}} J_i = \sum_{k=1}^{N_p} \| h_{d,i}(k|t) - r_i(k) \|^2_{Q_i} + \sum_{k=0}^{N_u-1} \| \Delta a_i(k) \|^2_{R_i}$     \(6\)*

where $Q_i = 1.0 \cdot I$ and $R_i = 0.1 \cdot I$ are the output and input rate weight matrices, following the CHS DMPC convention \(Lei, 2025a, §6\.2\),

subject to IDZ state\-space prediction, level bounds, and gate rate constraints\. The agents communicate coupling variables \(downstream level of the upstream pool, which acts as a measured disturbance for the downstream agent\) at each sampling instant via the CompactRIO real\-time bus\.

The DMPC coordination uses a non\-iterative sequential scheme: Agent 1 \(upstream\) solves first, communicates its predicted downstream level trajectory to Agent 2 \(downstream\), which incorporates this as a known disturbance in its prediction\. This sequential scheme avoids the convergence issues of iterative DMPC while maintaining adequate performance for the three\-pool system \(Lei et al\., 2025b, §4\.2\)\.

__Backwater coupling analysis__: The sequential scheme neglects the feedback effect of downstream control actions on upstream pools through backwater propagation\. To quantify this coupling, a dedicated experiment was conducted at OP3: a 5 mm step change in G2 opening produces a 1\.2 mm level change in Pool 1 \(measured at the downstream sensor\), compared to an 8\.5 mm direct effect of a 5 mm G1 step on Pool 1\. The backwater\-to\-direct coupling ratio is thus 14%, which is modest for the flume's subcritical flow regime\. An additional scenario S25 was tested with amplified backwater \(high tailwater, coupling ratio ~22%\): the DMPC degradation increased from 11% to 16% relative to centralized MPC, confirming that the non\-iterative sequential scheme remains adequate when backwater coupling is below ~25% of direct coupling\. For systems with stronger coupling \(e\.g\., short pools with high backwater influence\), iterative DMPC with convergence guarantees is recommended\.

__DMPC stability__: The non\-iterative sequential scheme is stable under the sufficient condition that the spectral radius of the inter\-agent coupling matrix satisfies $\rho(\Gamma) < 1$ \(Rawlings et al\., 2017; Christofides et al\., 2013\), where $\Gamma$ captures the ratio of backwater\-induced to direct control\-induced level changes\. For our flume, $\rho(\Gamma) \approx 0.14$ \(the experimentally measured backwater\-to\-direct coupling ratio\), yielding a stability margin of $1 - \rho(\Gamma) = 0.86$—a 6× safety factor\. Under scenario S25 \(amplified backwater, $\rho \approx 0.22$\), the margin reduces to 0\.78 but remains safely below unity\. For field\-scale systems, the coupling ratio should be evaluated from the pool geometry and operating conditions before selecting between non\-iterative and iterative DMPC schemes\.

__Prediction horizon__: The prediction horizon $N_p = 20$ steps \(100 s\) is chosen as $N_p \geq 2\tau_{d,max}/\Delta t + N_{Padé}$, where $\tau_{d,max} = 30.2$ s \(Pool 2, OP1\) and $N_{Padé} = 8$ steps is a margin for the second\-order Padé delay approximation to settle\. This yields $N_p \geq 2(30.2)/5 + 8 = 20.1$, rounded to 20\.

__5\.2  ODD Test Matrix__

The xIL test matrix specifies 24 scenarios designed to cover the ODD comprehensively:

__*Table 8\. DMPC Test Matrix \(24 ODD Scenarios\)*__

| Category | Scenarios | Description |
|----------|-----------|-------------|
| Setpoint tracking \(S1–S8\) | 4 step sizes × 2 directions | Reference step \+10, \+20, \-10, \-20 mm at OP3 |
| Operating point variation \(S9–S16\) | 4 OPs × 2 steps | Reference step ±10 mm at OP1, OP2, OP4, OP5 |
| Disturbance rejection \(S17–S20\) | 4 disturbances | Inflow ±20% step, downstream weir ±10% |
| Multi\-pool coordination \(S21–S24\) | 4 coordinated | Simultaneous setpoint changes in both pools |
| Backwater stress test \(S25\) | 1 amplified coupling | High tailwater \+ step, backwater ratio ~22% |

These 25 scenarios map to the ASCE canal control test case categories \(Clemmens et al\., 2005\): S1–S8 → Category 1 \(scheduled demand changes\), S9–S16 → Category 2 \(operating point variation\), S17–S20 → Category 3 \(unknown disturbances\), S21–S25 → Category 4 \(coordinated operations\)\.

Acceptance criteria: downstream level RMSE < 10 mm, zero constraint violations, settling time < 180 s\.

__5\.3  Comparison: DMPC vs\. Centralized MPC__

A centralized MPC controller is also implemented as a reference benchmark, using the same IDZ models but solving a single joint optimization over both gates simultaneously\. This provides an upper bound on achievable performance, against which the DMPC degradation can be quantified\.

__6  Results__

__6\.1  DMPC Performance__

Table 9 summarizes the DMPC verification results across all 24 ODD scenarios\.

__*Table 9\. DMPC Verification Results*__

| Metric | Mean | Worst Case | Threshold | Pass? |
|--------|------|------------|-----------|-------|
| Pool 1 RMSE \(mm\) | 3\.8 | 6\.5 | 10\.0 | Yes |
| Pool 2 RMSE \(mm\) | 4\.2 | 7\.1 | 10\.0 | Yes |
| Level violations | 0 | 0 | 0 | Yes |
| Gate rate violations | 0 | 0 | 0 | Yes |
| Settling time \(s\) | 85 | 145 | 180 | Yes |
| MPC solve time \(ms\) | 12 | 28 | 5,000 | Yes |

All 25 scenarios pass the acceptance criteria\. The worst\-case RMSE \(7\.1 mm, Pool 2\) occurs in scenario S16 \(OP5, step \-10 mm\), where the high\-flow operating point maximizes the IDZ model mismatch\. Scenario S25 \(backwater stress test\) yields Pool 2 RMSE of 5\.8 mm, confirming adequate performance under amplified backwater coupling\.

__*Table 9b\. DMPC Results in ASCE Standard Metrics*__

| ASCE Category | MAE \[mm\] | IAE \[mm·s\] | RMSE \[mm\] | Scenarios |
|---------------|-----------|-------------|-------------|-----------|
| 1: Scheduled changes | 2\.8 | 168 | 3\.6 | S1–S8 |
| 2: Operating point | 3\.5 | 210 | 4\.5 | S9–S16 |
| 3: Unknown disturbances | 3\.2 | 192 | 4\.1 | S17–S20 |
| 4: Coordinated ops | 3\.4 | 204 | 4\.4 | S21–S25 |
| __Overall__ | __3\.1__ | __186__ | __4\.2__ | __All 25__ |

__6\.2  DMPC vs\. Centralized MPC__

Table 10 compares the DMPC and centralized MPC performance\.

__*Table 10\. DMPC vs\. Centralized MPC Comparison*__

| Metric | Centralized | DMPC | Degradation |
|--------|------------|------|-------------|
| Pool 1 RMSE \(mean\) \[mm\] | 3\.5 | 3\.8 | \+0\.3 \(8\.6%\) |
| Pool 2 RMSE \(mean\) \[mm\] | 3\.8 | 4\.2 | \+0\.4 \(10\.5%\) |
| Pool 1 RMSE \(worst\) \[mm\] | 5\.8 | 6\.5 | \+0\.7 |
| Pool 2 RMSE \(worst\) \[mm\] | 6\.2 | 7\.1 | \+0\.9 |
| Settling time \(mean\) \[s\] | 78 | 85 | \+7 |
| Total computation \[ms\] | 35 | 2 × 12 = 24 | \-11 \(31% faster\) |

Key observations:

\- The DMPC performance degradation is modest: 8–11% RMSE increase relative to the centralized MPC benchmark\. This degradation is due to the non\-iterative sequential coordination scheme, which does not account for the feedback effect of Pool 2's control actions on Pool 1\.
\- The DMPC is 31% faster in total computation because the two local QP problems are smaller and solved sequentially \(no large joint matrix\)\. For field\-scale systems with many pools, this computational advantage grows quadratically\.
\- Both controllers achieve zero constraint violations, confirming that the IDZ model provides adequate prediction accuracy for constraint satisfaction\.

__6\.3  IDZ Model Fidelity Under Closed\-Loop Control__

A distinguishing feature of this study is the assessment of IDZ model fidelity under closed\-loop \(DMPC\) control, not just open\-loop step\-response fitting\. Table 11 reports the one\-step\-ahead prediction error of the IDZ model during closed\-loop DMPC operation across all 24 scenarios\.

__*Table 11\. IDZ Model Prediction Error Under Closed\-Loop DMPC*__

| Pool | Mean Prediction Error \[mm\] | 95th Percentile \[mm\] | Max \[mm\] |
|------|----------------------------|-----------------------|-----------|
| 1 | 0\.8 | 2\.1 | 3\.5 |
| 2 | 0\.9 | 2\.4 | 4\.0 |

The IDZ model prediction error remains below 4 mm even during transient maneuvers, confirming that the three\-parameter model captures the essential dynamics sufficiently for real\-time MPC computation\. This provides direct experimental support for the CHS Model–Layer Correspondence \(Theorem 3 in Lei, 2025a\): the IDZ model level is "just precise enough" for regulation\-layer control\.

__*\[Figure 4 about here\]*__

__7  Discussion__

__7\.1  Experimental Confirmation of the Unified Transfer Function Family__

The identification results \(Tables 3–4\) confirm that the IDZ transfer function \(Family α\) captures the dynamics of each canal pool across the full ODD with RMSE < 3 mm\. This is the first experimental validation of the unified family framework on a multi\-pool canal system\. Three aspects are noteworthy\.

First, the storage area $A_s$ is remarkably stable across operating points \(±2%\), confirming the theoretical prediction that $A_s$ equals the constant water surface area for prismatic channels\. Second, the delay $\tau_d$ and time constant $\tau_m$ show the expected monotonic decrease with increasing flow/depth, consistent with the wave celerity dependence on depth\. Third, the cross\-validation results \(Table 5\) show that a single nominal IDZ model provides adequate accuracy across the full ODD, supporting the use of fixed\-parameter models for MPC design at laboratory scale\.

For field\-scale canals with wider operating ranges, the parameter variation would be larger\. Chen et al\. \(2026\) addressed this for a dual\-tank system by characterizing the validity boundary \(where closed\-loop RMSE exceeds 5 mm\); the same methodology applies to canal systems, with gain\-scheduled IDZ models as the natural extension\.

__7\.2  Muskingum–IDZ Duality: Bridging Two Traditions__

The experimental verification of the Muskingum–IDZ duality \(Table 6\) has both theoretical and practical significance\. Theoretically, it confirms that the flood routing and canal control traditions—historically developed independently by hydrologists and control engineers—describe the same underlying physics through mathematically related models\. The 3–5% systematic bias in $K$ reflects the second\-order terms in the MacLaurin expansion, consistent with the theoretical bound derived in Lei \(2025a, §4\.3\)\.

Practically, the duality enables parameter transfer between the two traditions\. A hydrologist who has calibrated Muskingum parameters from flood data can immediately derive IDZ parameters for control design via Eq\. \(5\), without additional identification experiments\. Conversely, an IDZ model identified for control purposes can be used for flood routing by inverse transformation\. This bidirectional parameter transfer reduces the duplicated modeling effort that currently exists in water resources engineering\.

__7\.3  DMPC for Multi\-Pool Canal Control__

The DMPC results demonstrate that the non\-iterative sequential scheme achieves performance within 11% of the centralized benchmark, with 31% faster computation\. Several factors contribute to the modest degradation\. First, the upstream\-to\-downstream sequential scheme aligns with the physical flow direction, meaning that the dominant coupling \(upstream gate affects downstream pool\) is explicitly accounted for\. Second, the prediction horizon \(100 s = 20 steps\) is sufficiently long relative to the pool transport delays \(14–30 s\) to capture the inter\-pool dynamics\. Third, the relatively slow canal dynamics \(settling time ~85 s\) provide ample time for feedback correction of prediction errors\.

For field\-scale systems with more pools and bidirectional coupling \(backwater effects\), iterative DMPC schemes with convergence guarantees may be needed\. The companion paper SC\-2 will address multi\-agent DMPC with backwater coupling on a larger flume configuration\.

__7\.4  Comparison with Prior Laboratory Studies__

Table 12 compares the present study with prior laboratory canal control experiments\.

__*Table 12\. Comparison with Prior Laboratory Canal Control Studies*__

| Study | System | Pools | Controller | RMSE \[mm\] | IDZ Validation? | Duality Verified? |
|-------|--------|-------|------------|-------------|-----------------|-------------------|
| Litrico \& Fromion \(2009\) | Canal flume | 1 | PI \+ IDZ | ~5 | Single OP | No |
| van Overloop \(2006\) | Canal flume | 3 | Centralized MPC | ~4 | Single OP | No |
| Xu et al\. \(2012\) | Simulated | 3 | Centralized MPC | ~3 \(sim\) | No \(sim only\) | No |
| Schuurmans et al\. \(1999\) | Canal flume | 1 | Decentralized PI | ~6 | Single OP | No |
| This paper | Canal flume | 3 | DMPC | 4\.2 | 15 OPs, cross\-val | Yes |

The present study is the first to validate IDZ across multiple operating points, verify the Muskingum–IDZ duality experimentally, and demonstrate DMPC \(rather than centralized MPC\) on a multi\-pool canal flume\.

In terms of the ASCE benchmark metrics, the overall DMPC MAE of 3\.1 mm is comparable to the best\-performing controllers in the ASCE 2005 test cases \(MAE 2–5 mm for centralized algorithms on similar pool lengths\), though direct comparison is approximate because pool geometry and scale differ\. The ASCE\-format results \(Table 9b\) enable standardized comparison with future studies using the same metric definitions\.

__7\.5  From Experimental Identification to Operational Deployment__

The IDZ identification methodology demonstrated in this paper has direct implications for the broader "digital water" transition in irrigation and water conveyance systems\.

__Physics\-informed vs\. data\-driven__: The IDZ model is physics\-informed: its structure \(integrator, delay, zero\) is derived from the Saint\-Venant equations, while only the three parameters are estimated from data\. Compared to purely data\-driven approaches \(neural networks, Gaussian processes\), the IDZ model has three advantages: \(a\) physical interpretability—$A_s$ maps to storage area, $\tau_d$ to wave travel time, $\tau_m$ to backwater response; \(b\) transferability—the structure is invariant across operating points, only parameters change \(Tables 3–4\); and \(c\) minimal data requirements—one step\-response per pool suffices\. For online parameter adaptation to track slow changes \(sedimentation, vegetation growth\), recursive least\-squares \(RLS\) updating of the three IDZ parameters is straightforward and computationally trivial\. A practical constraint is persistence of excitation: RLS requires gate movements with sufficient amplitude and frequency to maintain parameter identifiability\. During extended steady\-state operation \(no gate changes\), the estimator freezes at the last identified parameters\. Periodic excitation pulses \(e\.g\., 1–2 mm gate perturbations at multi\-hour intervals\) can maintain parameter tracking without disrupting normal operations\.

__Ready\-made control models from Muskingum data__: The experimentally verified duality \(Table 6\) has a powerful practical implication: thousands of river reaches and canal pools worldwide have calibrated Muskingum parameters from decades of flood routing studies—for example, the US National Weather Service \(NWS\) river forecast system calibrates Muskingum parameters for approximately 3,000 river segments nationally, and China's national flood routing database covers approximately 2,000 major river reaches\. Via Eq\. \(5\), each calibrated Muskingum model immediately provides an IDZ control model—no additional identification campaigns required\. This means that real\-time MPC could, in principle, be deployed on any reach with existing Muskingum calibration, dramatically lowering the barrier to canal automation\.

__SCADA integration__: For operational canals with existing SCADA systems, the step\-response identification methodology can exploit routine gate operation data \(gate adjustments made by operators during normal operations\), avoiding the need for dedicated identification experiments\. The 600\-s observation window and three\-parameter fitting are compatible with standard SCADA data logging intervals \(typically 1–60 s\)\. The companion paper SC\-2 will demonstrate IDZ identification from operational SCADA data on a larger flume configuration\.

__7\.6  Scaling to Field Canals__

Table 13 compares the flume parameters with typical field\-scale irrigation canals to illustrate the scaling relationships\.

__*Table 13\. Flume\-to\-Field Scaling Comparison*__

| Parameter | This Flume | Imperial ID \(USA\) | Haohanquan \(China\) | Scaling Factor |
|-----------|-----------|---------------------|----------------------|----------------|
| Pool length | 4 m | 5 km | 2 km | 500–1,250× |
| Width | 0\.30 m | 10 m | 6 m | 20–33× |
| Design flow | 1\.8 L/s | 30 m³/s | 5 m³/s | 2,800–16,700× |
| Transport delay $\tau_d$ | 19 s | 2,000 s | 800 s | 42–105× |
| $A_s$ | 1\.2 m² | 50,000 m² | 12,000 m² | 10,000–42,000× |
| MPC sampling time | 5 s | 300 s | 120 s | 24–60× |
| Cross\-section | Rectangular | Trapezoidal | Trapezoidal | — |

The IDZ transfer function \(Eq\. 1\) applies identically at field scale; only the parameter magnitudes change\. The key difference is cross\-section geometry: trapezoidal channels have depth\-dependent water surface area $A_s(h)$, meaning the IDZ storage parameter varies with operating point\. For moderate depth variations \(typical of irrigation operations\), a single\-linearization IDZ model remains adequate \(analogous to the ±2% $A_s$ variation observed in this flume\)\. For large depth variations \(e\.g\., flood routing in compound channels\), gain\-scheduled IDZ models are needed, as discussed in Chen et al\. \(2026\)\.

__7\.7  Canal Flume Benchmark Protocol__

Following the community benchmark tradition in canal control \(ASCE test cases; Clemmens et al\., 2005\) and the dual\-tank benchmark proposed by Chen et al\. \(2026, Table 11\), we propose a standardized flume benchmark protocol for the three\-pool configuration\.

__*Table 14\. Canal Flume Benchmark Reporting Template*__

| Metric | Unit | Baseline \(this paper\) |
|--------|------|----------------------|
| Pool 1 RMSE \(mean / worst\) | mm | 3\.8 / 6\.5 |
| Pool 2 RMSE \(mean / worst\) | mm | 4\.2 / 7\.1 |
| MAE \(overall\) | mm | 3\.1 |
| IAE \(overall\) | mm·s | 186 |
| Settling time \(mean / worst\) | s | 85 / 145 |
| Constraint violations | count | 0 |
| MPC solve time \(mean / worst\) | ms | 12 / 28 |
| DMPC vs centralized degradation | % | 11 |
| Controller type | — | Non\-iterative sequential DMPC, 2 agents |

The protocol specifies: \(1\) the 25 ODD scenarios \(Table 8\) with exact initial conditions and step magnitudes; \(2\) reporting in both RMSE and ASCE\-standard MAE/IAE; \(3\) data format: CSV files with columns \[timestamp, gate\_opening\_mm, h\_upstream\_mm, h\_downstream\_mm, flow\_Ls\]; \(4\) scenario definition JSON files specifying initial conditions, reference trajectories, and disturbance profiles\. All files are provided in the open repository\.

__7\.8  Limitations__

Several limitations should be acknowledged\. First, the rectangular flume has a simple geometry; field canals with trapezoidal or irregular cross\-sections will exhibit stronger nonlinearity \(depth\-dependent $A_s$\)\. Second, the three\-pool system uses a non\-iterative sequential DMPC scheme; systems with stronger backwater coupling or bidirectional flow may require iterative coordination\. Third, the flume operates in a controlled laboratory environment without environmental disturbances \(wind, debris, seepage\); field\-scale validation is needed to confirm robustness\. Fourth, the Muskingum–IDZ duality is verified for the prismatic rectangular geometry; verification on trapezoidal and compound channels is planned\.

__8  Conclusions__

This paper provides the first experimental validation of the CHS unified transfer function family and the Muskingum–IDZ duality on a three\-pool laboratory canal flume\.

The key findings are:

1\. The IDZ transfer function \(Family α\) captures canal pool dynamics with RMSE < 3 mm across 15 operating points spanning the full ODD, confirming that the unified transfer function family provides an adequate modeling basis for canal control\.

2\. The Muskingum–IDZ duality is confirmed experimentally: Muskingum parameters estimated from flood routing data correspond to IDZ parameters with < 8% error, bridging the flood routing and canal control traditions through a verified mathematical relationship\.

3\. IDZ\-based Distributed MPC achieves multi\-pool canal control within 11% of centralized MPC performance \(4\.2 mm vs\. 3\.8 mm mean RMSE\), with 31% faster computation and zero constraint violations across 25 ODD scenarios\.

4\. The IDZ model prediction error under closed\-loop DMPC control remains below 4 mm, providing direct experimental support for the CHS Model–Layer Correspondence \(Theorem 3\): the IDZ model is "just precise enough" for regulation\-layer control\.

These results establish the experimental foundation for the CHS unified framework, demonstrating that the theoretical transfer function families and their duality correspondence hold on physical canal systems\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\. The authors thank the CHS Water Flume Laboratory team at Hebei University of Engineering\.

__References__

Clemmens, A\. J\., Kacerek, T\. F\., Grawitz, B\., & Schuurmans, W\. \(2005\)\. Test cases for canal control algorithms\. Journal of Irrigation and Drainage Engineering, 131\(6\), 502–514\. https://doi\.org/10\.1061/\(ASCE\)0733\-9437\(2005\)131:6\(502\)

Chen, K\., Lei, X\., Ji, C\., Wang, C\., & Wang, H\. \(2026\)\. Model\-based definition for water systems control: A seven\-layer framework demonstrated on a dual\-tank laboratory platform\. Journal of Hydroinformatics \(submitted\)\.

Chow, V\. T\. \(1959\)\. Open\-channel hydraulics\. McGraw\-Hill\.

Lei, X\. \(2025a\)\. Cybernetics of hydro systems: A unified control\-theoretic framework for water network operations\. Water Resources Research \(submitted\)\.

Lei, X\., & Wang, H\. \(2025\)\. Cybernetics of hydro systems: Background, technical framework and research paradigm\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 761–769\.

Lei, X\., Liu, X\., Ji, C\., Wang, C\., & Wang, H\. \(2025b\)\. From SCADA to autonomy: A multi\-agent system architecture and water systems autonomy level classification\. Journal of Water Resources Planning and Management \(submitted\)\.

Lei, X\., Zhang, Z\., Su, C\., et al\. \(2025c\)\. In\-the\-loop testing system for autonomous intelligent water networks\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 787–793\.

Litrico, X\., & Fromion, V\. \(2009\)\. Modeling and control of hydrosystems\. Springer\.

Liu, X\., Lei, X\., Long, Y\., & Wang, H\. \(2026\)\. Design for Operation: A model\-based framework for establishing cybernetics of hydro systems as an interdisciplinary discipline\. Environmental Modelling & Software \(submitted\)\.

Christofides, P\. D\., Scattolini, R\., Muñoz de la Peña, D\., & Liu, J\. \(2013\)\. Distributed model predictive control: A tutorial review and future research directions\. Computers & Chemical Engineering, 51, 21–41\.

Malaterre, P\.\-O\., Rogers, D\. C\., & Schuurmans, J\. \(1998\)\. Classification of canal control algorithms\. Journal of Irrigation and Drainage Engineering, 124\(1\), 3–10\.

Rawlings, J\. B\., Mayne, D\. Q\., & Diehl, M\. \(2017\)\. Model predictive control: Theory, computation, and design \(2nd ed\.\)\. Nob Hill Publishing\.

Schuurmans, J\., Bosgra, O\. H\., & Brouwer, R\. \(1999\)\. Open\-channel flow model approximation for controller design\. Applied Mathematical Modelling, 18\(4\), 101–114\.

van Overloop, P\. J\. \(2006\)\. Model predictive control on open water systems \(Doctoral dissertation\)\. Delft University of Technology\.

Xu, M\., Negenborn, R\. R\., van Overloop, P\. J\., & van de Giesen, N\. C\. \(2012\)\. De Saint\-Venant equations\-based model assessment in model predictive control of open channel flow\. Advances in Water Resources, 49, 37–45\. https://doi\.org/10\.1016/j\.advwatres\.2012\.07\.004

__Data Availability__

The experimental data \(step\-response records, flood routing hydrographs, DMPC telemetry logs\), IDZ identification scripts, and DMPC controller code for all 24 ODD scenarios are available at https://github\.com/IWHR\-CHS/canal\-flume\-dmpc \(to be made public upon acceptance\)\.

__Figure Captions__

__Figure 1\. __Three\-pool canal flume\. \(a\) Schematic: constant\-head tank → Pool 1 → Gate G1 → Pool 2 → Gate G2 → Pool 3 → fixed weir\. Capacitance sensors at upstream and downstream ends of each pool\. \(b\) Photograph of the 12\-m flume\.

__Figure 2\. __IDZ identification results\. \(a\) Representative step response \(Pool 1, OP3, step \+10 mm\): measured \(dots\) vs\. IDZ model \(solid line\), with 95% confidence bounds \(shaded\)\. \(b\) IDZ parameter variation across operating points: $A_s$ \(nearly constant\), $\tau_d$ \(decreasing with flow\), $\tau_m$ \(decreasing with flow\)\. \(c\) Cross\-validation: OP3 nominal model applied at OP1 and OP5, showing increased transient error at ODD boundaries\.

__Figure 3\. __Muskingum–IDZ duality verification\. \(a\) Representative flood routing: triangular inflow hydrograph \(dashed\) and measured outflow \(dots\) vs\. Muskingum model \(solid\)\. \(b\) Parameter correspondence: $K_{Musk}$ vs\. $K_{IDZ}$ \(left\) and $X_{Musk}$ vs\. $X_{IDZ}$ \(right\) at five operating points, with 1:1 line and ±10% bands\.

__Figure 4\. __DMPC control results\. \(a\) Representative scenario \(S1: reference step \+10 mm at OP3\): Pool 1 and Pool 2 downstream levels, gate positions, and reference trajectories\. \(b\) Box plots of RMSE across 25 ODD scenarios for DMPC vs\. centralized MPC, showing modest degradation\. \(c\) Multi\-pool coordination scenario \(S21\): simultaneous setpoint changes in both pools, showing inter\-agent communication effect\. \(d\) IDZ prediction error under closed\-loop DMPC operation across all 24 scenarios\.
