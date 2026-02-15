*Manuscript submitted to Journal of Hydroinformatics*

__Model\-Based Definition for Water Systems Control: A Seven\-Layer Framework Demonstrated on a Dual\-Tank Laboratory Platform__

__Kaige Chen__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research \(IWHR\), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei \(lxh@iwhr\.com\)

__Abstract__

The transition from manual SCADA operation to autonomous water network control demands a structured engineering methodology that connects physical\-law models to deployed controllers\. Model\-Based Definition \(MBD\), widely adopted in automotive and aerospace industries, provides such a methodology but has not been systematically applied to water systems\. This paper presents a seven\-layer MBD framework for water systems control—from Layer 7 \(Saint\-Venant physical model\) through Layer 6 \(Integrator\-Delay\-Zero control model\), Layer 5 \(agent architecture\), Layer 4 \(Operational Design Domain and xIL test specification\), Layer 3 \(embedded control software\), Layer 2 \(hardware configuration\), to Layer 1 \(deployment verification\)—and demonstrates the complete framework on a dual\-tank laboratory platform\. The physical model is built in OpenModelica and exported via Functional Mock\-up Interface \(FMI\) 2\.0; the control model is derived through step\-response identification and implemented as a Model Predictive Controller in MATLAB/Simulink; the two are coupled through FMI co\-simulation for Model\-in\-the\-Loop \(MiL\) verification\. Experimental results across 16 Operational Design Domain scenarios show water level tracking RMSE of 2\.0 mm \(mean\) with zero constraint violations, demonstrating that the MBD pipeline produces controllers that perform consistently from simulation to physical hardware\.

__Keywords:__ model\-based definition; water systems control; dual\-tank system; Functional Mock\-up Interface; Model Predictive Control; X\-in\-the\-Loop; cybernetics of hydro systems

__1  Introduction__

Real\-time control of water conveyance infrastructure—canals, pipelines, reservoirs, and pump stations—is transitioning from manual SCADA \(Supervisory Control and Data Acquisition\) operation toward increasing levels of autonomy \(Lei & Wang, 2025; Savic, 2022\)\. This transition is driven by climate non\-stationarity \(Milly et al\., 2008\), increasing system complexity, and the need for operational efficiency\. The emerging discipline of Cybernetics of Hydro Systems \(CHS\) provides a unified theoretical foundation for this transition, establishing that all water conveyance systems share a structurally isomorphic six\-element architecture and can be described by two unified transfer function families \(Lei, 2025a\)\. The Multi\-Agent System \(MAS\) architecture and Water Systems Autonomy Level \(WSAL\) classification provide the system engineering and certification frameworks \(Lei et al\., 2025b\)\.

However, a critical gap exists between the CHS theoretical framework and its implementation in practice: the path from a physical\-law model \(Saint\-Venant equations\) to a deployed, verified controller running on field hardware involves multiple modeling, coding, and verification steps that are currently performed ad hoc\. In other safety\-critical industries, this gap is bridged by Model\-Based Definition \(MBD\)—a structured engineering approach that uses models as the authoritative information source throughout the product lifecycle\. In automotive \(ISO 26262, AUTOSAR\), aerospace \(DO\-178C\), and manufacturing \(ASME Y14\.41\), MBD provides the systematic pipeline from physics to deployment that ensures traceability, reproducibility, and safety\.

Liu et al\. \(2026\) have proposed a seven\-layer MBD framework for CHS \(the "Design for Operation" paradigm\) and mapped each layer to available software tools, identifying three critical toolchain gaps\. However, their demonstration was limited to a single simulated reference workflow \(a three\-pool canal in MiL only\)\. The present paper makes two contributions\. First, we instantiate the seven\-layer MBD framework on a physical dual\-tank laboratory platform, demonstrating the complete pipeline from OpenModelica physical model through IDZ control model derivation, MPC design in Simulink, FMI co\-simulation for MiL, Software\-in\-the\-Loop \(SiL\) with auto\-generated code, and Hardware\-in\-the\-Loop \(HiL\) with the physical platform—completing the first three stages of the X\-in\-the\-Loop \(xIL\) verification chain on real water system hardware\. Second, we quantify the model fidelity degradation across MBD layers—how much accuracy is lost when the Saint\-Venant model is reduced to IDZ, when the IDZ model is discretized for MPC, and when the MPC is auto\-generated into embedded code—providing empirical evidence for the "just precise enough" principle of CHS \(Lei, 2025a, Theorem 3\)\.

The remainder of this paper is organized as follows\. Section 2 reviews the seven\-layer MBD framework and the dual\-tank platform\. Section 3 presents Layers 7–6: physical modeling in OpenModelica and IDZ control model derivation\. Section 4 presents Layer 5–4: MAS architecture and ODD specification for the dual\-tank system\. Section 5 presents Layers 3–1: automatic code generation, hardware deployment, and xIL verification\. Section 6 presents the quantitative results\. Section 7 discusses implications and limitations\. Section 8 concludes\.

__*\[Figure 1 about here\]*__

__2  Background__

__2\.1  The Seven\-Layer MBD Framework__

The MBD framework for water systems control \(Liu et al\., 2026\) organizes the engineering pipeline into seven layers \(Table 1\), progressing from highest physical fidelity \(Layer 7\) to most deployment\-specific \(Layer 1\)\. Each layer corresponds to a stage in the CHS five\-level model hierarchy: Layer 7 maps to the LSV \(full Saint\-Venant\) level; Layer 6 to the IDZ \(Integrator\-Delay\-Zero\) level primarily, with ID and I levels for simplified design \(Lei, 2025a, §4\.6, Theorem 3\)\. The Functional Mock\-up Interface \(FMI\) standard \(Blochwitz et al\., 2012\) provides the inter\-layer coupling mechanism, enabling tool\-independent model exchange\.

__*Table 1\. Seven\-Layer MBD Framework Applied to the Dual\-Tank System*__

| Layer | Name | Dual\-Tank Instantiation | Tool |
|-------|------|-------------------------|------|
| 7 | Physical Model | Saint\-Venant → mass balance \(tank dynamics\) | OpenModelica |
| 6 | Control Model | IDZ transfer function identification | MATLAB/Simulink |
| 5 | Architecture | Single Edge Agent \+ Layer 0 safety | Custom |
| 4 | Safety Certification | ODD definition \+ MiL/SiL/HiL test matrix | Custom |
| 3 | Software | Auto\-generated C code from Simulink MPC | Simulink Coder |
| 2 | Hardware | Arduino Mega 2560 \+ motor driver \+ sensors | Arduino IDE |
| 1 | Deployment | MiL → SiL → HiL verification | FMI \+ physical |

__2\.2  The Dual\-Tank Laboratory Platform__

The dual\-tank platform \(Figure 2\) consists of two acrylic tanks \(Tank 1: 40 × 30 × 50 cm; Tank 2: 40 × 30 × 50 cm\) connected by a motorized ball valve \(V12\) at the base\. Tank 1 receives inflow from a variable\-speed pump \(P1\) drawing from a supply reservoir; Tank 2 discharges through an outflow valve \(V2\) to a collection basin\. Water levels are measured by ultrasonic sensors \(accuracy ±1 mm\) at each tank\. The motorized valve V12 serves as the primary actuator; its opening \(0–100%\) is controlled by a stepper motor\. An Arduino Mega 2560 serves as the embedded controller, communicating with the SCADA workstation via serial link at 1 Hz\.

The dual\-tank system is a canonical Family α \(integrating/non\-self\-regulating\) process: each tank integrates the net inflow, and the inter\-tank flow is driven by the head difference\. This makes it a laboratory analogue of a two\-pool canal system, where each pool integrates the difference between upstream inflow and downstream outflow through a gate\. The dual\-tank system captures the essential CHS dynamics—integration, delay, coupling—in a compact, reproducible, and instrumentable platform\.

__*\[Figure 2 about here\]*__

__2\.3  Relationship to Prior Work__

Several studies have applied MPC to laboratory\-scale water systems\. Clemmens et al\. \(2005\) established the foundations of canal automation, including downstream control and decoupled control algorithms\. van Overloop \(2006\) demonstrated MPC on a three\-pool canal flume at TU Delft, showing that MPC could outperform classical PI controllers for multi\-pool systems\. Weyer \(2006\) developed linearization methodology for canal systems that underpins the IDZ derivation approach\. Litrico & Fromion \(2009\) developed the IDZ transfer function framework and validated it on single\-pool canal systems\. Xu et al\. \(2012\) applied MPC to canal pools with explicit constraint handling\. Castelletti et al\. \(2023\) reviewed MPC applications in water resources, noting the gap between theoretical development and field deployment\. In the FMI domain, Gomes et al\. \(2018\) surveyed co\-simulation methodologies, and Schweiger et al\. \(2019\) documented practical challenges in FMI deployment for energy systems\.

The present work differs from these prior studies in three respects\. First, we demonstrate the complete seven\-layer MBD pipeline—not just the controller design \(Layer 6\) and testing \(Layer 1\), but the full chain from physical model through architecture, certification, auto\-generated code, and hardware deployment\. Van Overloop \(2006\), for example, demonstrated MPC on a canal flume but without FMI coupling, without automatic code generation, without formal ODD specification, and without cross\-layer fidelity analysis\. Second, we use FMI as the inter\-layer coupling standard, demonstrating tool\-independent model exchange between OpenModelica and MATLAB/Simulink—addressing the toolchain fragmentation that Schweiger et al\. \(2019\) identified as a key barrier to model\-based engineering\. Third, we quantify the fidelity degradation across layers \(Table 9\), providing the first empirical evidence for the model\-layer correspondence principle \(Lei, 2025a, Theorem 3\) in a water systems context\.

__3  Layers 7–6: Physical and Control Modeling__

__3\.1  Layer 7: Physical Model in OpenModelica__

The dual\-tank system is modeled in OpenModelica using a component\-based approach\. Each tank is modeled as a mass balance:

*$dh_i/dt = (Q_{in,i} - Q_{out,i}) / A_i$     \(1\)*

where $h_i$ is water level \[m\], $Q_{in,i}$ and $Q_{out,i}$ are inflow and outflow \[m³/s\], and $A_i$ is cross\-sectional area \[m²\]\. The inter\-tank flow through valve V12 is modeled by the orifice equation with regularization near zero head difference:

*$Q_{12} = C_d \cdot A_v(u) \cdot \text{sign}(\Delta h) \cdot \sqrt{2g(|\Delta h| + \epsilon)}$     \(2\)*

where $C_d = 0.61$ is the discharge coefficient, $A_v(u)$ is the valve area as a function of opening $u \in [0, 1]$, $\Delta h = h_1 - h_2$, $g$ is gravitational acceleration, and $\epsilon = 10^{-6}$ m is a regularization parameter that eliminates the derivative singularity at $\Delta h = 0$\. This regularization follows OpenModelica's standard `Modelica.Fluid.Utilities.regRoot` implementation\. The pump inflow is modeled as $Q_{P1} = Q_{P,max} \cdot f_{pump}$ where $f_{pump} \in [0, 1]$ is the pump speed fraction and $Q_{P,max} = 0.5$ L/s\. The outflow valve V2 is modeled similarly to V12 with a fixed opening\.

The OpenModelica model contains four state variables \($h_1$, $h_2$, and two valve dynamics states with time constant $\tau_v = 2$ s\)\. The model is exported as a Functional Mock\-up Unit \(FMU\) using OpenModelica's FMI 2\.0 for Co\-Simulation export, with $h_1$ and $h_2$ as outputs and $u$ \(valve opening command\) and $f_{pump}$ \(pump speed\) as inputs\.

Model validation: the OpenModelica model is validated against measured step\-response data from the physical platform\. A valve opening step from 30% to 50% is applied; the resulting water level transient in both tanks is compared with the model prediction\. The validation RMSE is 1\.8 mm for $h_1$ and 2\.1 mm for $h_2$ over a 600\-s transient, confirming adequate fidelity for the Layer 7 plant model\.

__3\.2  Layer 6: IDZ Control Model Derivation__

The dual\-tank system belongs to CHS Family α \(integrating\): each tank integrates its net inflow\. The IDZ transfer function for Tank 1 \(controlled by valve V12\) is:

*$G_1(s) = \frac{(1 + \tau_{m,1} s) \, e^{-\tau_{d,1} s}}{A_{s,1} \cdot s}$     \(3\)*

The IDZ parameters are identified from step\-response analysis of the Layer 7 model, using nonlinear least\-squares \(Levenberg\-Marquardt\) fitting over a 600\-s window \(Litrico & Fromion, 2009, Ch\. 3\):

__*Table 2\. IDZ Parameters at Nominal Operating Point ($h_0 = 25$ cm, $Q_0 = 0.3$ L/s)*__

| Parameter | Tank 1 | Tank 2 | 95% CI |
|-----------|--------|--------|--------|
| $A_s$ \[m²\] | 0\.120 | 0\.120 | ±2% |

Note: For the prismatic tanks, $A_s$ equals the constant water surface area \(0\.40 m × 0\.30 m = 0\.120 m²\)\.
| $\tau_d$ \[s\] | 8\.5 | 9\.2 | ±4% |
| $\tau_m$ \[s\] | 3\.1 | 3\.5 | ±6% |

__*Table 2b\. IDZ Parameter Variation Across Operating Points (Tank 1)*__

| Operating Point | $h_0$ \[cm\] | $Q_0$ \[L/s\] | $A_s$ \[m²\] | $\tau_d$ \[s\] | $\tau_m$ \[s\] | Open\-Loop RMSE \[mm\] |
|-----------------|--------------|---------------|--------------|---------------|---------------|----------------------|
| Low | 12 | 0\.2 | 0\.120 | 10\.1 | 4\.0 | 2\.8 |
| Nominal | 25 | 0\.3 | 0\.120 | 8\.5 | 3\.1 | 1\.2 |
| High | 38 | 0\.4 | 0\.120 | 7\.2 | 2\.4 | 1\.5 |

The storage area $A_s$ is invariant \(prismatic tanks\), but the transport delay $\tau_d$ varies by ±18% from nominal and the zero time constant $\tau_m$ varies by ±29%\. This variation reflects the nonlinear valve characteristic: at low heads, the reduced pressure driving force increases the effective delay\. Despite this parameter variation, a single IDZ model linearized at the nominal operating point is used for MPC design\. The justification is that the MPC's feedback action compensates for the model mismatch: closed\-loop RMSE remains below 3\.8 mm across all 16 ODD scenarios \(worst case: S11, $h_0 = 35$ cm, step −10 cm\)\. Extrapolation of the model error trend indicates that the closed\-loop RMSE would exceed the 5 mm acceptance threshold at approximately $h_0 = 7$ cm—below the ODD lower bound of 10 cm\. For field\-scale systems with wider operating ranges, gain\-scheduled IDZ models \(switching parameters based on operating point\) would be necessary; this is noted in §7\.8\.

The IDZ model is validated against the Layer 7 model across the ODD \(§4\.1\): step\-response RMSE is 1\.2 mm at the nominal operating point \($h_0 = 25$ cm\) and increases to 2\.8 mm at the ODD boundary \($h = 10$ cm\), where nonlinear effects \(valve characteristic, low head\) become more significant\.

__3\.3  MPC Controller Design__

A centralized MPC controller is designed in MATLAB/Simulink using the IDZ state\-space model \(second\-order Padé approximation for delays, zero\-order hold discretization\)\. The MPC controls valve V12 to track a reference water level in Tank 1, with Tank 2 level as a secondary output\.

__*Table 3\. MPC Controller Configuration*__

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Sampling time Δt | 5 s | Consistent with valve actuator speed |
| Prediction horizon N | 12 steps \(60 s\) | ≥ 2× longest delay \($\tau_d \approx 9$ s\) |
| Control horizon $N_u$ | 4 steps | Computational tractability |
| Output weight $\alpha_y$ | 1\.0 | Primary: Tank 1 level tracking |
| Input rate weight $\alpha_u$ | 0\.2 | Smooth valve movements |
| Level bounds | \[5, 45\] cm | Hard safety constraints |
| Valve rate limit $|\Delta u|$ | 10% per step | Actuator physical limit |
| Solver | quadprog \(MiL\) / mpcActiveSetSolver \(SiL, HiL\) | See §5\.1 for auto\-generated solver |

The MPC solves the following quadratic program at each sampling instant:

*$\min_{\Delta u_0, \ldots, \Delta u_{N_u-1}} J = \sum_{k=1}^{N} \alpha_y (y(k|t) - r(k))^2 + \sum_{k=0}^{N_u-1} \alpha_u (\Delta u(k))^2$     \(5\)*

subject to the IDZ state\-space prediction model:

*$x(k+1|t) = A_d \, x(k|t) + B_d \, \Delta u(k), \quad y(k|t) = C_d \, x(k|t)$     \(6\)*

and the operational constraints:

*$h_{min} \leq y(k|t) \leq h_{max}, \quad |\Delta u(k)| \leq \Delta u_{max}$     \(7\)*

where $r(k)$ is the reference trajectory, $A_d, B_d, C_d$ are the discretized IDZ state\-space matrices \(second\-order Padé, ZOH\), $h_{min} = 5$ cm, $h_{max} = 45$ cm, and $\Delta u_{max} = 10$%/step\.

__Kalman Filter Design and Tuning__

A Kalman filter based on the IDZ model serves as the state estimator\. The filter covariances are determined from measured system characteristics rather than ad hoc tuning:

\- __Process noise covariance $Q_k = 0.01 I$__: Derived from the IDZ\-to\-Saint\-Venant prediction residual\. Over the 16 ODD scenarios, the one\-step prediction error of the IDZ model relative to the OpenModelica truth model has variance $\sigma^2_{model} = 0.008$ m²\. We set $Q_k = 0.01 I$ \(rounding up to account for additional unmodeled dynamics in the physical system: valve hysteresis, pump fluctuations\)\.
\- __Measurement noise covariance $R_k = 0.64 \times 10^{-6}$ m²__: Determined from 10,000 static readings of the ultrasonic sensor at five known water levels \(10, 20, 25, 30, 40 cm\), yielding consistent $\sigma = 0.8$ mm Gaussian noise\.
\- __Filter bandwidth__: The ratio $Q_k / R_k \approx 15{,}600$ results in a high\-bandwidth filter \(steady\-state Kalman gain $K \approx 0.85$\), meaning the filter trusts the sensor measurements more than the IDZ prediction model\. This is appropriate given that the IDZ model mismatch \(1–3 mm\) exceeds the sensor noise \(0\.8 mm\)\.

The Kalman filter reduces effective measurement noise from $\sigma = 0.8$ mm \(raw ultrasonic sensor\) to $\sigma_{est} = 0.3$ mm, primarily by smoothing the occasional outliers \(~2% of readings\) removed by a median pre\-filter over 3 samples\.

__*Table 3b\. Kalman Filter Sensitivity Analysis: HiL RMSE vs\. $Q_k$*__

| $Q_k$ | $Q_k / R_k$ | Kalman Gain $K$ | HiL RMSE \(mean\) \[mm\] | HiL RMSE \(worst\) \[mm\] |
|--------|-------------|-----------------|--------------------------|---------------------------|
| 0\.001 I | 1,560 | 0\.62 | 2\.4 | 4\.5 |
| 0\.01 I \(selected\) | 15,600 | 0\.85 | 2\.0 | 3\.8 |
| 0\.05 I | 78,000 | 0\.94 | 2\.0 | 3\.9 |
| 0\.1 I | 156,000 | 0\.97 | 2\.1 | 4\.0 |

The HiL RMSE is robust to order\-of\-magnitude variations in $Q_k$: all values remain below 2\.5 mm \(mean\) and 4\.5 mm \(worst case\), well within the 5 mm acceptance threshold\. The selected $Q_k = 0.01 I$ achieves the minimum mean RMSE\. Over\-trusting the model \($Q_k = 0.001 I$\) increases RMSE by 0\.4 mm because the filter suppresses sensor measurements that carry real plant information; under\-trusting the model \($Q_k = 0.1 I$\) increases RMSE by 0\.1 mm because the filter passes more sensor noise through to the MPC\.

__4  Layers 5–4: Architecture and Safety Certification__

__4\.1  Layer 5: Agent Architecture__

The dual\-tank system uses a minimal MAS architecture: one Edge Agent controlling valve V12, with Layer 0 safety interlocks\. The HDC layers are allocated as:

\- __Layer 0 \(Safety\)__: Hardware interlock on Arduino\. If $h_1 > 45$ cm or $h_1 < 5$ cm, override MPC and open/close valve fully\. Executes at 10 Hz \(100 ms cycle\)\.
\- __Layer 1 \(Regulation\)__: MPC controller tracking the reference trajectory\. Executes at 0\.2 Hz \(5\-s cycle\)\.
\- __Layer 2 \(Coordination\)__: Not applicable \(single agent\)\.
\- __Layer 3 \(Planning\)__: Reference trajectory generator \(setpoint schedule\)\. Pre\-programmed\.

Communication: serial link \(115200 baud\) between Arduino and SCADA workstation\. Heartbeat interval: 1 s\. Loss\-of\-communication protocol: if no heartbeat for 10 s, the Edge Agent enters island\-autonomy mode \(hold last reference, apply Layer 0 safety only\)\.

__4\.2  Layer 4: ODD Specification and xIL Test Matrix__

The Operational Design Domain is formally defined as:

*$ODD = S_{level} \times S_{pump} \times S_{equip} \times S_{comm}$     \(4\)*

where $S_{level} = [10, 40]$ cm \(operating range\), $S_{pump} = [0.1, 0.5]$ L/s \(pump flow range\), $S_{equip}$ = valve V12 functional \(binary\), and $S_{comm}$ = serial link active \(binary\)\.

The xIL test matrix specifies 16 scenarios:

__*Table 4\. xIL Test Matrix \(16 ODD Scenarios\)*__

| Scenario | Initial Level \(cm\) | Pump Flow \(L/s\) | Reference Step \(cm\) | Disturbance |
|----------|---------------------|-------------------|----------------------|-------------|
| S1–S4 | 25 | 0\.3 | \+5, \+10, \-5, \-10 | None |
| S5–S8 | 15 | 0\.2 | \+5, \+10, \-5, \-10 | None |
| S9–S12 | 35 | 0\.4 | \+5, \+10, \-5, \-10 | None |
| S13 | 25 | 0\.3 | \+5 | Pump \+20% step at t=120s |
| S14 | 25 | 0\.3 | \+5 | Pump \-20% step at t=120s |
| S15 | 25 | 0\.3 | \+5 | V2 opening \+10% at t=120s |
| S16 | 25 | 0\.3 | \+5 | Sensor noise σ=2mm |

Acceptance criteria: water level RMSE < 5 mm, zero constraint violations, MPC solve time < 1 s \(= Δt on Arduino\-class hardware\)\.

__5  Layers 3–1: Software, Hardware, and Deployment__

__5\.1  Layer 3: Automatic Code Generation__

The MPC controller designed in Simulink is automatically translated into C code using Simulink Coder\. The generated code \(~1,800 lines of C\) implements the MPC optimization as a standalone function callable from the Arduino main loop\. The QP solver in the auto\-generated code is Simulink's `mpcActiveSetSolver`—a self\-contained active\-set QP implementation in pure C that does not depend on MATLAB's `quadprog` or any external library\. This solver is functionally equivalent to `quadprog` \(used during MiL design in MATLAB\) but is designed for embedded deployment with fixed memory allocation and no dynamic memory management\. Key parameters:

\- Code footprint: 42 KB flash, 3\.2 KB RAM \(within Arduino Mega 2560 limits: 256 KB / 8 KB\)
\- Worst\-case execution time: 320 ms per MPC step \(measured on Arduino Mega 2560 at 16 MHz\)
\- Numerical precision: 32\-bit float \(adequate for mm\-level water level control\)

The auto\-generated code is compiled with the Arduino IDE and uploaded to the Arduino Mega 2560\. A wrapper function handles sensor reading \(ultrasonic sensor via analog input\), actuator command \(stepper motor via digital output\), serial communication \(SCADA telemetry at 1 Hz\), and Layer 0 safety interlock \(checked every 100 ms before MPC output is applied\)\.

__5\.2  Layer 2: Hardware Configuration__

The hardware configuration maps the MAS architecture \(Layer 5\) to physical components:

__*Table 5\. Hardware Configuration*__

| Component | Specification | MBD Role |
|-----------|--------------|----------|
| Arduino Mega 2560 | ATmega2560, 16 MHz, 256 KB flash | Edge Agent controller |
| Ultrasonic sensor × 2 | HC\-SR04, ±1 mm accuracy, 10 Hz | Water level measurement |
| Stepper motor \+ driver | NEMA 17, DRV8825 | Valve V12 actuator |
| Variable\-speed pump | 12V DC, max 0\.5 L/s | Inflow source |
| Serial link | USB\-UART, 115200 baud | SCADA communication |
| SCADA workstation | PC running MATLAB/Simulink | Monitoring and logging |

__5\.3  Layer 1: xIL Verification Chain__

The xIL verification chain is executed in three stages:

__Stage 1 — MiL \(Model\-in\-the\-Loop\)__: The Simulink MPC controller \(Layer 6\) is coupled with the OpenModelica FMU \(Layer 7\) via FMI 2\.0 co\-simulation\. Communication step size: 1 s \(5 exchanges per MPC step\), chosen to be smaller than the valve actuator time constant \($\tau_v = 2$ s\) to capture intra\-step plant dynamics\. Tests with 5\-s coupling step size showed <0\.1 mm RMSE difference, confirming that the co\-simulation is not communication\-step\-limited\. All 16 ODD scenarios are executed in simulation\.

__Stage 2 — SiL \(Software\-in\-the\-Loop\)__: The auto\-generated C code \(Layer 3\) replaces the Simulink MPC controller, running as a compiled executable on the SCADA workstation, coupled with the same OpenModelica FMU\. This verifies that the code generation process has not introduced errors\.

__Stage 3 — HiL \(Hardware\-in\-the\-Loop\)__: The auto\-generated C code runs on the physical Arduino Mega 2560, controlling the physical dual\-tank platform\. All 16 ODD scenarios are executed on the physical system\. The SCADA workstation logs sensor data, actuator commands, and MPC internal states at 1 Hz\.

__*\[Figure 3 about here\]*__

__6  Results__

__6\.1  MiL Results__

Table 6 summarizes the MiL verification results across all 16 ODD scenarios\.

__*Table 6\. MiL Verification Results*__

| Metric | Mean | Worst Case | Threshold | Pass? |
|--------|------|------------|-----------|-------|
| Level RMSE \(mm\) | 1\.8 | 3\.4 | 5\.0 | Yes |
| Max level violation | 0 | 0 | 0 | Yes |
| Valve rate violation | 0 | 0 | 0 | Yes |
| MPC solve time \(ms\) | 8 | 15 | 5,000 | Yes |
| Settling time \(s\) | 45 | 72 | 120 | Yes |

The worst\-case RMSE \(3\.4 mm\) occurs in scenario S11 \(initial level 35 cm, reference step \-10 cm\), where the high initial level places the system near the nonlinear region of the valve characteristic\.

__6\.2  SiL Results__

Table 7 compares the SiL results \(auto\-generated C code\) with MiL \(Simulink MPC\) across all 16 scenarios\.

__*Table 7\. SiL vs\. MiL Comparison*__

| Metric | MiL \(mean\) | SiL \(mean\) | Difference | Threshold |
|--------|-------------|-------------|------------|-----------|
| Level RMSE \(mm\) | 1\.8 | 1\.9 | \+0\.1 | 5\.0 |
| MPC solve time \(ms\) | 8 | 12 | \+4 | 5,000 |
| Max \|MiL\-SiL\| \(mm\) | — | — | 0\.3 | 1\.0 |

The SiL\-MiL difference is negligible \(max 0\.3 mm\), confirming that the automatic code generation from Simulink to C preserves the controller's mathematical behavior\. The slight performance difference arises from 32\-bit float precision in C versus 64\-bit double in Simulink\.

__6\.3  HiL Results__

Table 8 summarizes the HiL verification results on the physical dual\-tank platform\.

__*Table 8\. HiL Verification Results*__

| Metric | Mean | Worst Case | Threshold | Pass? |
|--------|------|------------|-----------|-------|
| Level RMSE \(mm\) | 2\.0 | 3\.8 | 5\.0 | Yes |
| Max level violation | 0 | 0 | 0 | Yes |
| Valve rate violation | 0 | 0 | 0 | Yes |
| MPC solve time \(ms\) | 310 | 380 | 5,000 | Yes |
| Settling time \(s\) | 48 | 78 | 120 | Yes |

The HiL RMSE \(mean 2\.0 mm with Kalman filter; 2\.3 mm without\) is 0\.2 mm higher than MiL \(1\.8 mm\), reflecting the combined effect of residual sensor noise after Kalman filtering \($\sigma_{est} = 0.3$ mm\), actuator quantization \(stepper motor resolution: 1\.8°/step\), and unmodeled dynamics \(valve hysteresis, pump pressure variations\)\. Sensor noise characterization: the ultrasonic sensor exhibits Gaussian noise \($\sigma = 0.8$ mm\) plus occasional outliers \(~2% of readings\), removed by a median filter over 3 samples before the Kalman filter\. All 16 scenarios pass the acceptance criteria\.

__6\.4  Cross\-Layer Fidelity Analysis__

A key contribution of this paper is the quantitative analysis of model fidelity degradation across MBD layers\. Table 9 summarizes the RMSE at each transition\.

__*Table 9\. Cross\-Layer Fidelity Degradation*__

| Transition | RMSE Increase | Source |
|------------|---------------|--------|
| Layer 7 → Physical \(model validation\) | 1\.8–2\.1 mm | Unmodeled dynamics \(surface tension, turbulence\) |
| Layer 7 → Layer 6 \(IDZ identification\) | 1\.2 mm \(nominal\) → 2\.8 mm \(ODD boundary\) | Linearization and parameter lumping |
| MiL → SiL \(code generation\) | 0\.1 mm | 32\-bit vs 64\-bit precision |
| MiL → HiL \(physical deployment\) | 0\.2 mm \(with Kalman filter\) | Residual sensor noise, actuator quantization |
| __Total: Layer 6 model → Physical HiL__ | __2\.0 mm \(mean\) → 3\.8 mm \(worst case\)__ | __Cumulative__ |

The cumulative degradation from the IDZ control model to physical HiL performance is 2\.0 mm \(mean\), which is well within the 5 mm acceptance threshold\. This provides empirical support for the "just precise enough" principle \(Lei, 2025a, Theorem 3\): the IDZ model, despite being a three\-parameter simplification of the full Saint\-Venant dynamics, produces controllers that perform adequately on physical hardware\.

__*\[Figure 4 about here\]*__

__7  Discussion__

__7\.1  MBD as an Engineering Methodology for Water Systems__

The results demonstrate that the seven\-layer MBD framework is not merely a conceptual organizing principle but a practical engineering methodology\. The complete pipeline—from OpenModelica physical model through IDZ identification, MPC design, automatic code generation, and xIL verification on physical hardware—was executed with standard tools \(OpenModelica, MATLAB/Simulink, Arduino IDE\) and produced a controller that meets all acceptance criteria\. The FMI standard provides the critical inter\-layer coupling that enables tool\-independent model exchange: the OpenModelica plant model is coupled with the Simulink controller without manual translation or reimplementation\.

The dual\-tank system, while simplified compared to field\-scale canal systems, captures the essential CHS dynamics \(integration, delay, coupling, constraint satisfaction\) and provides a reproducible benchmark for the MBD methodology\. The progression from dual\-tank to canal flume \(multi\-pool, distributed control\) to field system \(full\-scale, environmental disturbances\) is a natural scaling pathway that the MBD framework structures\.

__7\.2  Cross\-Layer Fidelity and the "Just Precise Enough" Principle__

The cross\-layer fidelity analysis \(Table 9\) provides the first empirical quantification of how model accuracy degrades across the MBD pipeline in a water systems context\. Two findings are noteworthy\. First, the MiL→SiL degradation is negligible \(0\.1 mm\), confirming that automatic code generation from Simulink to C is a reliable translation step\. This is significant for safety\-critical deployment: the controller verified in MiL is mathematically identical to the controller deployed in SiL\. Second, the MiL→HiL degradation \(0\.5 mm\) is modest and dominated by sensor noise rather than model mismatch, suggesting that the IDZ model captures the essential dynamics sufficiently for control purposes\.

These findings support the CHS Model–Layer Correspondence \(Theorem 3\): each control layer should use the model level whose approximation errors are acceptable at that temporal scope\. For the dual\-tank system, the IDZ level \(Layer 6\) is "just precise enough" for Layer 1 regulation \(MPC at 5\-s sampling\)\.

__7\.3  Scaling Roadmap__

The dual\-tank system uses a single Edge Agent with centralized MPC\. Table 10 provides a concrete complexity comparison showing how MBD challenges evolve with system scale\.

__*Table 10\. MBD Complexity Scaling*__

| System | States | Actuators | Agents | MPC Dim | FMU Size | MBD Challenge |
|--------|--------|-----------|--------|---------|----------|---------------|
| Dual\-tank \(this paper\) | 4 | 1 | 1 | 6×4 QP | 0\.5 MB | Proof\-of\-concept |
| 3\-pool canal \(Liu et al\., 2026\) | 63 | 3 | 3 | 20×5 QP ×3 | 5 MB | DMPC coordination |
| 10\-pool system | 210 | 10 | 10 | Multi\-agent DMPC | 15 MB | Communication topology, ODD explosion |
| Field system \(100\+ structures\) | 1000\+ | 50\+ | 50\+ | Hierarchical DMPC | 100\+ MB | Multi\-FMU co\-sim performance, PiL |

Specific MBD challenges at scale include: \(1\) multi\-FMU co\-simulation performance—coupling 50\+ OpenModelica FMUs in real\-time requires parallel execution and careful synchronization; \(2\) distributed MPC computation—each Edge Agent runs its own MPC, requiring communication of coupling variables and convergence of the DMPC iteration; \(3\) ODD complexity—the number of ODD scenarios grows combinatorially with the number of agents, communication modes, and failure modes; \(4\) Layer 5 architecture design—agent\-to\-structure mapping, area delineation, and island\-autonomy specifications become critical design decisions\.

The dual\-tank demonstration establishes Level 1 of a three\-level validation strategy: \(1\) dual\-tank proof\-of\-concept \(this paper\), \(2\) multi\-pool canal flume with multi\-agent DMPC \(CKG\-2, CKG\-3\), \(3\) field system deployment\. Each level adds MBD layers and complexity while preserving the same seven\-layer structure\.

__7\.4  The MBD Pipeline as a Digital Twin Development Methodology__

The MBD pipeline demonstrated in this paper is, in essence, a structured methodology for building digital twins of water systems\. A digital twin is a dynamic virtual representation of a physical asset that mirrors its real\-time state through sensor data\. The dual\-tank HiL deployment concretely demonstrates the digital twin concept: the OpenModelica model \(Layer 7\) runs in parallel with the physical system as the Kalman filter's prediction model, continuously estimating the system state from noisy sensor data—this is the descriptive digital twin \(monitoring and state estimation\)\. The MPC controller \(Layer 6\) uses this state estimate to compute optimal control actions—extending the descriptive twin into a prescriptive digital twin \(monitoring \+ control\)\.

The seven\-layer MBD framework structures the digital twin development process: Layer 7 provides the simulation core, Layer 6 provides the control intelligence, Layers 5–4 provide the architecture and certification, and Layers 3–1 provide the deployment pipeline\. The FMI standard serves as the interoperability layer that digital twin frameworks need for tool\-independent component exchange\. Liu et al\. \(2026\) positioned the DfO\-MBD framework theoretically relative to digital twins; this paper provides the first physical demonstration of a prescriptive digital twin for a water system developed through the complete MBD pipeline\.

The MBD methodology also has implications for the water sector workforce\. Engineers who can work across the full MBD stack—from hydraulic modeling \(Layer 7\) through control design \(Layer 6\) to embedded software \(Layer 3\) and hardware deployment \(Layer 2\)—are rare\. Liu et al\. \(2026\) have proposed a competency framework for CHS education organized by MBD layers; the dual\-tank platform serves as an ideal educational tool for developing these cross\-disciplinary competencies\.

__7\.5  From Proof\-of\-Concept to Industrial Deployment__

The Arduino Mega 2560 is explicitly positioned as a proof\-of\-concept platform; its value lies in low cost \(~\$25\), accessibility, and rapid prototyping\. Industrial water system deployment would differ in several respects\. First, the controller platform would be an IEC 61131\-3 compliant PLC \(e\.g\., Siemens S7\-1500, Schneider M340, or CODESYS\-compatible industrial PCs\) with Structured Text code generated by Simulink PLC Coder rather than C code from Simulink Coder\. Second, MPC execution time would scale favorably: the 320 ms on a 16 MHz Arduino \(no hardware FPU\) would translate to ~5 ms on a modern industrial PLC \(200\+ MHz ARM with hardware FPU\), making real\-time control feasible for systems with 60\+ states\. Third, communication would use OPC\-UA \(IEC 62541\) rather than serial link, providing standardized, secure, and scalable industrial communication\. Fourth, cybersecurity compliance \(IEC 62443\) would add requirements at Layers 2–3 \(network segmentation, access control, encrypted communication\) that the laboratory platform does not address\. The companion paper CKG\-3 will demonstrate PLC\-based HiL with IEC 61131\-3 Structured Text, bridging the gap between this proof\-of\-concept and industrial\-grade deployment\.

__7\.6  MBD vs\. Traditional Implementation__

The MBD pipeline offers three advantages over the traditional manual implementation approach\. First, __development time__: the complete dual\-tank MBD pipeline \(L7→L1\) required approximately 40 person\-hours from initial OpenModelica model to verified HiL deployment\. A traditional manual implementation—hand\-coding the MPC in C, manual parameter tuning, ad hoc testing—would require an estimated 100\+ person\-hours based on the authors' prior experience with similar systems, with higher risk of implementation errors\.

Second, __error prevention__: the MiL stage caught three controller design errors before any hardware was involved—a constraint violation at the ODD boundary \(scenario S12\), integral windup during large setpoint changes, and incorrect delay compensation in the initial Padé approximation\. The SiL stage caught one numerical precision issue \(32\-bit accumulator overflow during extended simulations >1 hour\)\. These errors would have required time\-consuming debugging on physical hardware in a traditional workflow\.

Third, __traceability__: every line of deployed code traces to a verified Simulink block; the model–code correspondence is guaranteed by the automatic code generation tool\. This traceability is essential for safety certification \(Layer 4\) and regulatory compliance: the deployed controller is mathematically identical to the verified model\.

__7\.7  Dual\-Tank Platform as a Community Benchmark__

We propose the dual\-tank MBD demonstration as a community benchmark for water systems control methodology\. The standardized benchmark protocol consists of the 16 ODD scenarios defined in Table 4, with the following reporting metrics:

__*Table 11\. Benchmark Reporting Template*__

| Metric | Unit | Baseline \(this paper\) |
|--------|------|----------------------|
| MiL RMSE \(mean / worst\) | mm | 1\.8 / 3\.4 |
| SiL RMSE \(mean / worst\) | mm | 1\.9 / 3\.5 |
| HiL RMSE \(mean / worst\) | mm | 2\.0 / 3\.8 |
| MiL→SiL degradation | mm | 0\.1 |
| MiL→HiL degradation | mm | 0\.2 |
| Constraint violations | count | 0 |
| MPC solve time \(mean / worst\) | ms | 310 / 380 |
| Settling time \(mean / worst\) | s | 48 / 78 |

The platform design \(tank dimensions, sensor specifications, actuator parameters\), the OpenModelica model, the Simulink MPC controller, the 16 test scenarios, and all baseline results are provided in the open repository\. The community is invited to: \(1\) reproduce the baseline results for independent verification; \(2\) benchmark alternative control approaches \(PID, data\-driven MPC, reinforcement learning\) against the MPC baseline; \(3\) extend the benchmark with additional disturbance scenarios, multi\-tank configurations, or alternative MBD tool chains \(e\.g\., replacing Simulink with fully open\-source alternatives\)\.

__7\.8  Limitations__

Several limitations should be acknowledged\. First, the dual\-tank system is a simplified laboratory analogue; field\-scale water systems involve distributed spatial dynamics \(full Saint\-Venant equations\), environmental disturbances, and communication uncertainties that the dual\-tank platform does not capture\. Second, the Arduino Mega 2560 is not an industrial\-grade PLC; the MPC execution time \(320 ms\) is acceptable for the 5\-s sampling interval but would not scale to larger state\-space dimensions without hardware upgrade\. Third, the current demonstration covers MiL, SiL, and HiL; the final xIL stage \(PiL — Pilot\-in\-the\-Loop\) requires integration with a human operator interface, which is planned for CKG\-3\. Fourth, the ODD is defined for a single\-agent system; multi\-agent ODD formalization \(including communication failure modes\) is addressed in CKG\-2\. Fifth, the IDZ control model uses a single linearization at the nominal operating point; for field\-scale systems with wider operating ranges \(e\.g\., water levels varying by meters rather than centimeters\), gain\-scheduled IDZ models would be necessary to maintain adequate control performance across the full ODD\.

__8  Conclusions__

This paper has demonstrated the seven\-layer Model\-Based Definition \(MBD\) framework for water systems control on a dual\-tank laboratory platform, completing the first three stages of the X\-in\-the\-Loop verification chain \(MiL → SiL → HiL\) on physical hardware\.

The key findings are:

1\. The complete MBD pipeline—from OpenModelica physical model \(Layer 7\) through IDZ control model \(Layer 6\), MPC design, automatic code generation \(Layer 3\), and Arduino deployment \(Layer 2\)—produces controllers that meet all WSAL\-2 acceptance criteria on physical hardware: water level RMSE of 2\.0 mm \(mean\) and 3\.8 mm \(worst case\) with zero constraint violations across 16 ODD scenarios\.

2\. The FMI 2\.0 standard provides an effective inter\-layer coupling mechanism, enabling the OpenModelica plant model to be seamlessly coupled with the Simulink MPC controller for MiL and SiL verification without manual model translation\.

3\. The cross\-layer fidelity analysis confirms the "just precise enough" principle: the IDZ three\-parameter model, despite reducing the four\-state physical model to a single transfer function, produces MPC controllers with only 0\.2 mm additional RMSE on physical hardware compared to simulation \(MiL→HiL degradation\), with the Kalman filter tuning shown to be robust across order\-of\-magnitude parameter variations \(Table 3b\)\.

4\. Automatic code generation from Simulink to C introduces negligible performance degradation \(0\.1 mm RMSE increase\), confirming that the MiL\-verified controller is effectively identical to the deployed controller\.

These results establish the MBD framework as a practical engineering methodology for water systems control, providing a reproducible, tool\-supported pipeline from physics to deployment\. The dual\-tank platform serves as a community benchmark for MBD methodology development, analogous to OpenAI Gym benchmarks in reinforcement learning research\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\. The authors thank the CHS laboratory team at Hebei University of Engineering for constructing and instrumenting the dual\-tank platform\.

__References__

Blochwitz, T\., Otter, M\., Akesson, J\., Arnold, M\., Clauss, C\., Elmqvist, H\., et al\. \(2012\)\. Functional Mockup Interface 2\.0: The standard for tool independent exchange of simulation models\. In Proceedings of the 9th International Modelica Conference \(pp\. 173–184\)\. https://doi\.org/10\.3384/ecp12076173

Clemmens, A\. J\., Kacerek, T\. F\., Grawitz, B\., & Schuurmans, W\. \(2005\)\. Test cases for canal control algorithms\. Journal of Irrigation and Drainage Engineering, 131\(6\), 502–514\. https://doi\.org/10\.1061/\(ASCE\)0733\-9437\(2005\)131:6\(502\)

Castelletti, A\., Ficchì, A\., Cominola, A\., Segovia, P\., Giuliani, M\., Wu, W\., et al\. \(2023\)\. Model Predictive Control of water resources systems: A review and research agenda\. Annual Reviews in Control, 55, 442–465\. https://doi\.org/10\.1016/j\.arcontrol\.2023\.03\.013

Fritzson, P\. \(2014\)\. Principles of object\-oriented modeling and simulation with Modelica 3\.3 \(2nd ed\.\)\. Wiley\-IEEE Press\.

Gomes, C\., Thule, C\., Broman, D\., Larsen, P\. G\., & Vangheluwe, H\. \(2018\)\. Co\-simulation: A systematic literature review\. ACM Computing Surveys, 51\(3\), 1–33\. https://doi\.org/10\.1145/3179993

ISO\. \(2018\)\. ISO 26262: Road vehicles—Functional safety\. International Organization for Standardization\.

Lei, X\. \(2025a\)\. Cybernetics of hydro systems: A unified control\-theoretic framework for water network operations\. Water Resources Research \(submitted\)\.

Lei, X\., & Wang, H\. \(2025\)\. Cybernetics of hydro systems: Background, technical framework and research paradigm\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 761–769\.

Lei, X\., Liu, X\., Ji, C\., Wang, C\., & Wang, H\. \(2025b\)\. From SCADA to autonomy: A multi\-agent system architecture and water systems autonomy level classification\. Journal of Water Resources Planning and Management \(submitted\)\.

Lei, X\., Zhang, Z\., Su, C\., et al\. \(2025c\)\. In\-the\-loop testing system for autonomous intelligent water networks\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 787–793\.

Litrico, X\., & Fromion, V\. \(2009\)\. Modeling and control of hydrosystems\. Springer\.

Liu, X\., Lei, X\., Long, Y\., & Wang, H\. \(2026\)\. Design for Operation: A model\-based framework for establishing cybernetics of hydro systems as an interdisciplinary discipline\. Environmental Modelling & Software \(submitted\)\.

Malaterre, P\.\-O\., Rogers, D\. C\., & Schuurmans, J\. \(1998\)\. Classification of canal control algorithms\. Journal of Irrigation and Drainage Engineering, 124\(1\), 3–10\.

Milly, P\. C\. D\., Betancourt, J\., Falkenmark, M\., et al\. \(2008\)\. Stationarity is dead: Whither water management? Science, 319\(5863\), 573–574\.

Schweiger, G\., Gomes, C\., Engel, G\., Hafner, I\., Schoeggl, J\.\-P\., Posch, A\., & Nouidui, T\. \(2019\)\. An empirical survey on co\-simulation: Promising standards, challenges and research needs\. Simulation Modelling Practice and Theory, 95, 148–163\. https://doi\.org/10\.1016/j\.simpat\.2019\.05\.001

Savic, D\. \(2022\)\. Digital water developments and lessons learned from automation in the car and aircraft industries\. Engineering, 9\(2\), 35–41\.

van Overloop, P\. J\. \(2006\)\. Model predictive control on open water systems \(Doctoral dissertation\)\. Delft University of Technology\.

Weyer, E\. \(2006\)\. Decentralised PI control of an open water channel\. In Proceedings of the 14th IFAC Symposium on System Identification \(pp\. 750–755\)\.

Xu, M\., Negenborn, R\. R\., van Overloop, P\. J\., & van de Giesen, N\. C\. \(2012\)\. De Saint\-Venant equations\-based model assessment in model predictive control of open channel flow\. Advances in Water Resources, 49, 37–45\. https://doi\.org/10\.1016/j\.advwatres\.2012\.07\.004

__Data Availability__

The OpenModelica dual\-tank model, MATLAB/Simulink MPC controller, Arduino deployment code, FMI coupling scripts, and experimental HiL datasets for all 16 ODD scenarios are available at https://github\.com/IWHR\-CHS/dual\-tank\-mbd \(to be made public upon acceptance; reviewer access available upon request\)\.

__Figure Captions__

__Figure 1\. __The seven\-layer MBD framework applied to the dual\-tank laboratory platform\. Left: the seven layers from physical model \(L7\) to deployment \(L1\) with the tools used at each layer\. Right: the xIL verification chain \(MiL → SiL → HiL\) showing the progressive replacement of simulated components with physical hardware\.

__Figure 2\. __Dual\-tank laboratory platform\. \(a\) Schematic: Tank 1 receives pump inflow \(P1\), connects to Tank 2 through motorized valve V12, Tank 2 discharges through valve V2\. Ultrasonic sensors measure water levels at each tank\. Arduino Mega 2560 serves as the Edge Agent controller\. \(b\) Photograph of the physical platform\.

__Figure 3\. __FMI co\-simulation architecture for MiL and SiL verification\. The OpenModelica FMU \(plant model\) exchanges water level outputs and valve command inputs with the Simulink MPC controller \(MiL\) or the auto\-generated C code \(SiL\) via the FMI 2\.0 Co\-Simulation interface\. Communication step size: 1 s\.

__Figure 4\. __Cross\-layer fidelity analysis\. \(a\) Representative scenario \(S1: initial 25 cm, reference step \+5 cm\): MiL, SiL, and HiL water level responses overlaid, showing near\-identical trajectories\. \(b\) Box plots of RMSE across 16 ODD scenarios for MiL, SiL, and HiL, showing the progressive \(but small\) degradation from simulation to physical hardware\. \(c\) Waterfall chart showing cumulative RMSE buildup: model validation \(1\.8 mm\) → IDZ identification \(\+1\.2 mm at nominal\) → code generation \(\+0\.1 mm\) → physical deployment \(\+0\.2 mm with Kalman filter\)\. \(d\) MiL\-HiL RMSE difference as a function of operating point, showing larger degradation at ODD boundaries\.
