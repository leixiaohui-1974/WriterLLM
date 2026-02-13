*Manuscript submitted to Environmental Modelling & Software*

__HydroComponents: An Open\-Source Modelica Library for Component\-Based Modeling of Water Conveyance Systems__

__Yakai Bai__1, __Xiaohui Lei__1,2\*, __Kaige Chen__1, __Bingkuan Yin__1, __Chen Ji__3, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research \(IWHR\), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei \(lxh@iwhr\.com\)

__Abstract__

Simulation of water conveyance systems—open channels, pipelines, reservoirs, and their control structures—requires coupling hydraulic process models with control algorithm models, yet existing tools typically address only one side: hydraulic simulators \(HEC\-RAS, SWMM, MIKE\) lack native control integration, while control design environments \(MATLAB/Simulink\) lack validated hydraulic libraries\. This paper presents HydroComponents, an open\-source Modelica library that provides reusable, parameterizable component models for all six elements of the Cybernetics of Hydro Systems \(CHS\) framework: plants \(canal pools, pipe segments, reservoirs\), actuators \(sluice gates, radial gates, pumps, valves, turbines\), sensors \(level, flow, pressure\), disturbances \(lateral inflow, demand, rainfall\), controllers \(PID, MPC interfaces\), and objectives \(setpoint generators, constraint managers\)\. The library implements the CHS unified transfer function families \(Family α integrating, Family β self\-regulating\) as the core dynamics, with Saint\-Venant\-based components for higher\-fidelity needs\. All components conform to the Functional Mock\-up Interface \(FMI\) 2\.0 standard, enabling seamless export to Simulink, Python, and other FMI\-compatible environments for co\-simulation within the Model\-Based Definition \(MBD\) pipeline\. The library is validated against three reference systems: a dual\-tank platform \(RMSE 1\.8 mm\), a three\-pool canal flume \(RMSE 2\.1 mm\), and a field\-scale three\-pool canal \(RMSE 45 mm\)\. HydroComponents reduces system assembly time from days to hours by providing drag\-and\-drop component composition, and serves as the Layer 7 building block for the CHS MBD framework\.

__Keywords:__ Modelica; open\-source library; water conveyance systems; component\-based modeling; Functional Mock\-up Interface; cybernetics of hydro systems; model\-based definition

__1  Introduction__

Modeling water conveyance systems for real\-time control requires two capabilities: accurate hydraulic process simulation \(the plant model\) and integration with control algorithm design \(the controller model\)\. Currently, these capabilities are served by separate tool ecosystems\. Hydraulic simulators—HEC\-RAS \(Brunner, 2016\), SWMM \(Rossman, 2015\), MIKE \(DHI, 2024\)—provide detailed one\-dimensional and two\-dimensional hydraulic modeling but lack native interfaces for control algorithm design, automatic code generation, or X\-in\-the\-Loop \(xIL\) verification\. Control design environments—MATLAB/Simulink \(MathWorks\), Modelica/OpenModelica \(Fritzson, 2014\)—provide model\-based design and automatic code generation but lack validated hydraulic component libraries for water systems\.

This toolchain fragmentation is a critical barrier to the Model\-Based Definition \(MBD\) pipeline for water systems control \(Liu et al\., 2026\)\. The MBD framework requires that the Layer 7 physical model \(the highest\-fidelity plant simulation\) be exported via FMI for coupling with the Layer 6 control model in Simulink\. Without a component library that supports both accurate hydraulics and FMI export, users must build custom models for each system—a time\-consuming and error\-prone process that inhibits the adoption of model\-based engineering in the water sector\.

The Cybernetics of Hydro Systems \(CHS\) framework \(Lei, 2025a\) provides the theoretical foundation for such a component library\. CHS establishes that all water conveyance processes share a structurally isomorphic six\-element architecture \($\Sigma = (P, A, S, D, C, O)$\) and can be described by two unified transfer function families\. This structural invariance means that a finite set of parameterizable component models can represent any water conveyance system through composition—a natural fit for the component\-based modeling paradigm of Modelica\.

This paper presents HydroComponents, an open\-source Modelica library that implements the CHS six\-element architecture as reusable, FMI\-compatible component models\. The library makes three contributions\. First, it provides a comprehensive component set covering all six CHS elements \(28 components in total\), from Saint\-Venant canal pool models through IDZ transfer function blocks to actuator, sensor, disturbance, controller interface, and objective components\. Second, it implements a multi\-fidelity approach: each plant component is available at multiple levels of the CHS five\-level hierarchy \(LSV, IDZ, ID, I, SS\), enabling users to select the appropriate fidelity for their application\. Third, all components conform to FMI 2\.0, enabling export to any FMI\-compatible environment \(Simulink, Python/FMPy, Julia\) for co\-simulation within the MBD pipeline\.

The remainder of this paper is organized as follows\. Section 2 reviews the CHS framework and Modelica language background\. Section 3 presents the library architecture and component design\. Section 4 describes the implementation details\. Section 5 presents validation against three reference systems\. Section 6 demonstrates the library in the MBD pipeline context\. Section 7 discusses implications and limitations\. Section 8 concludes\.

__2  Background__

__2\.1  The CHS Six\-Element Architecture__

The CHS framework \(Lei, 2025a\) formalizes water conveyance systems as controlled dynamical systems with six elements \(Table 1\): Plant \(hydraulic process\), Actuator \(gates, pumps, valves\), Sensor \(level, flow, pressure measurement\), Disturbance \(lateral inflow, demand, rainfall\), Controller \(decision algorithm\), and Objective \(setpoints, constraints\)\. Every water conveyance system—from a single canal pool to a national\-scale water transfer network—can be decomposed into instances of these six element types\. The unified transfer function families \(Family α integrating, Family β self\-regulating\) describe the plant dynamics, while the unified actuator characteristic \(Lemma 3: $\Delta Q = \alpha \Delta u + \beta_{up} \Delta H_{up} + \beta_{dn} \Delta H_{dn}$\) describes the actuator dynamics\.

__*Table 1\. CHS Six\-Element Architecture → HydroComponents Mapping*__

| CHS Element | Modelica Package | Components | Count |
|-------------|-----------------|------------|-------|
| Plant \(P\) | HydroComponents\.Plants | CanalPool, PipeSegment, Reservoir, Junction, Tank | 5 × 5 fidelity levels |
| Actuator \(A\) | HydroComponents\.Actuators | SluiceGate, RadialGate, Pump, Valve, Turbine | 5 |
| Sensor \(S\) | HydroComponents\.Sensors | LevelSensor, FlowSensor, PressureSensor | 3 |
| Disturbance \(D\) | HydroComponents\.Disturbances | LateralInflow, Demand, Rainfall, Evaporation | 4 |
| Controller \(C\) | HydroComponents\.Controllers | PID, MPCInterface, SafetyInterlock, DMPCAgent | 4 |
| Objective \(O\) | HydroComponents\.Objectives | SetpointGenerator, ConstraintManager, CostFunction | 3 |
| __Total__ | | | __28__ \(including 5 fidelity variants for Plant\) |

__2\.2  Modelica and OpenModelica__

Modelica is an object\-oriented, equation\-based modeling language for multi\-domain physical systems \(Fritzson, 2014\)\. Its key features for water systems modeling are: \(1\) acausal equations \(differential\-algebraic\), enabling natural representation of conservation laws; \(2\) component\-based architecture with connectors and inheritance; \(3\) FMI export for co\-simulation; and \(4\) open standard with multiple implementations \(OpenModelica, Dymola, Wolfram SystemModeler\)\. OpenModelica is the open\-source implementation used for HydroComponents development\.

Existing Modelica libraries for fluid systems \(Modelica\.Fluid, Buildings, ThermoSysPro\) focus on thermal\-hydraulic processes \(HVAC, power plants\) and do not include open\-channel flow models, canal pool dynamics, or water\-specific actuators \(sluice gates, radial gates\)\. HydroComponents fills this gap\.

__2\.3  Functional Mock\-up Interface__

The Functional Mock\-up Interface \(FMI\) standard \(Blochwitz et al\., 2012\) defines a standardized interface for model exchange and co\-simulation\. An FMU \(Functional Mock\-up Unit\) is a self\-contained model package \(compiled code \+ XML description\) that can be imported into any FMI\-compatible tool\. FMI 2\.0 for Co\-Simulation is the primary export mode used by HydroComponents, enabling coupling with MATLAB/Simulink \(via Simulink FMU block\), Python \(via FMPy\), and other environments\.

__3  Library Architecture__

__3\.1  Design Principles__

HydroComponents follows four design principles:

1\. __CHS alignment__: Library structure mirrors the six\-element architecture; users assemble systems by connecting Plant, Actuator, Sensor, Disturbance, Controller, and Objective components\.
2\. __Multi\-fidelity__: Each Plant component is available at five fidelity levels \(LSV → IDZ → ID → I → SS\), following the CHS five\-level model hierarchy \(Lei, 2025a, §4\.6\)\. Users select the appropriate level for their application\.
3\. __Connector standardization__: All components use two connector types: HydroPort \(flow \+ pressure/level, analogous to Modelica\.Fluid connectors but simplified for open channels\) and SignalPort \(control signals, setpoints, measurements\)\.
4\. __FMI\-first__: All components are designed and tested for FMI 2\.0 Co\-Simulation export\. Parameters that must be accessible from the co\-simulation master are explicitly exposed\.

__3\.2  Plant Components__

The core plant component is `CanalPool`, which models a single canal pool between two control structures\. At full fidelity \(LSV level\), the model solves the one\-dimensional Saint\-Venant equations using the Preissmann implicit scheme:

*$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = q_l$     \(1\)*

*$\frac{\partial Q}{\partial t} + \frac{\partial}{\partial x}\left(\frac{Q^2}{A}\right) + g A \frac{\partial h}{\partial x} = g A (S_0 - S_f) + q_l v_l$     \(2\)*

where $A$ is cross\-sectional area, $Q$ is flow, $h$ is water surface elevation, $q_l$ is lateral inflow, $S_0$ is bed slope, and $S_f$ is friction slope \(Manning's equation\)\. The spatial domain is discretized into $N$ cells \(default $N = 20$\)\. At IDZ level, the pool is represented by the three\-parameter transfer function:

*$G(s) = \frac{(1 + \tau_m s) \, e^{-\tau_d s}}{A_s \cdot s}$     \(3\)*

with parameters automatically derivable from the LSV model geometry \(Lei, 2025a, §4\.7\)\. The `PipeSegment` component similarly supports multiple fidelity levels, from water hammer \(Method of Characteristics\) through rigid pipe \($G_{pipe}(s) = 1/(C_h \cdot s)$\) to steady\-state\.

__3\.3  Actuator Components__

All actuators implement the unified actuator characteristic \(Lei, 2025a, Lemma 3\):

*$\Delta Q = \alpha \cdot \Delta u + \beta_{up} \cdot \Delta H_{up} + \beta_{dn} \cdot \Delta H_{dn}$     \(4\)*

where $\alpha$ is the actuator gain \[m²/s per unit\], $\beta_{up}$ and $\beta_{dn}$ are upstream and downstream head influence coefficients, and $u$ is the actuator command \(gate opening, pump speed, valve position\)\. Each actuator type computes $\alpha$, $\beta_{up}$, $\beta_{dn}$ from its physical parameters \(gate geometry, pump curves, valve characteristics\)\. Actuator dynamics \(motor response, valve travel time\) are modeled as first\-order lags with configurable time constants\.

__*Table 2\. Actuator Component Parameters*__

| Component | Key Parameters | $\alpha$ Computation | Dynamics |
|-----------|---------------|---------------------|----------|
| SluiceGate | $C_d$, width, max opening | $C_d \cdot b \cdot \sqrt{2g \Delta H}$ | 1st\-order, $\tau = 2$–10 s |
| RadialGate | $C_d$, radius, max angle | Geometry\-dependent | 1st\-order, $\tau = 5$–30 s |
| Pump | Head\-flow curve, max speed | Affinity laws | 1st\-order, $\tau = 1$–5 s |
| Valve | $C_v$, characteristic type | $C_v \cdot f(u) \cdot \sqrt{\Delta P}$ | 1st\-order, $\tau = 1$–10 s |
| Turbine | Head\-flow\-power surface | Hill chart interpolation | 1st\-order, $\tau = 5$–20 s |

__3\.4  Sensor, Disturbance, and Controller Components__

Sensor components add measurement noise \(configurable Gaussian $\sigma$\), quantization, and delay to the true plant state\. Disturbance components generate time\-varying boundary conditions \(lateral inflow profiles, demand patterns, rainfall hyetographs\)\. Controller components provide interfaces to external control algorithms via FMI inputs/outputs; the `MPCInterface` component exposes the measurement vector as FMI output and accepts the control command vector as FMI input, enabling MPC execution in Simulink or Python\.

__*\[Figure 1 about here\]*__

__4  Implementation__

__4\.1  Code Structure__

The library is implemented in Modelica 3\.5 and tested with OpenModelica v1\.22\. The code structure follows the Modelica package convention:

```
HydroComponents/
├── Plants/
│   ├── CanalPool.mo          (5 fidelity variants)
│   ├── PipeSegment.mo         (4 fidelity variants)
│   ├── Reservoir.mo           (3 fidelity variants)
│   ├── Junction.mo
│   └── Tank.mo
├── Actuators/
│   ├── SluiceGate.mo
│   ├── RadialGate.mo
│   ├── Pump.mo
│   ├── Valve.mo
│   └── Turbine.mo
├── Sensors/
│   ├── LevelSensor.mo
│   ├── FlowSensor.mo
│   └── PressureSensor.mo
├── Disturbances/
│   ├── LateralInflow.mo
│   ├── Demand.mo
│   ├── Rainfall.mo
│   └── Evaporation.mo
├── Controllers/
│   ├── PID.mo
│   ├── MPCInterface.mo
│   ├── SafetyInterlock.mo
│   └── DMPCAgent.mo
├── Objectives/
│   ├── SetpointGenerator.mo
│   ├── ConstraintManager.mo
│   └── CostFunction.mo
├── Connectors/
│   ├── HydroPort.mo
│   └── SignalPort.mo
├── Examples/
│   ├── DualTank.mo
│   ├── ThreePoolFlume.mo
│   └── ThreePoolCanal.mo
└── package.mo
```

Total: ~8,500 lines of Modelica code, 28 components, 3 example systems\.

__4\.2  Multi\-Fidelity Implementation__

Each plant component uses Modelica's replaceable model mechanism to support fidelity switching\. The user selects the fidelity level via a parameter:

```modelica
CanalPool pool1(
  redeclare model Dynamics = IDZ,  // or LSV, ID, I, SS
  L = 4000,        // pool length [m]
  B = 10,          // bottom width [m]
  S0 = 0.0005,     // bed slope [-]
  n = 0.014        // Manning's roughness [s/m^{1/3}]
);
```

When `IDZ` is selected, the component automatically computes the IDZ parameters \($A_s$, $\tau_d$, $\tau_m$\) from the geometry and steady\-state conditions using the analytical derivation from Lei \(2025a, §4\.7\)\. When `LSV` is selected, the full Preissmann scheme is instantiated\. The fidelity switching preserves the component's external interface \(same connectors, same FMI inputs/outputs\), enabling drop\-in replacement\.

__4\.3  FMI Export__

All components and example systems are tested for FMI 2\.0 Co\-Simulation export using OpenModelica's FMI export facility\. The exported FMU contains:
\- Compiled C code \(Linux and Windows binaries\)
\- modelDescription\.xml with all parameters and variables
\- Default parameter values

The FMU can be imported into: MATLAB/Simulink \(FMU block from the FMI Toolbox\), Python \(FMPy library\), Julia \(FMI\.jl\), or any FMI 2\.0\-compliant tool\.

__*\[Figure 2 about here\]*__

__5  Validation__

The library is validated against three reference systems of increasing complexity\.

__5\.1  Dual\-Tank Platform__

The dual\-tank system \(Chen et al\., 2026\) consists of two tanks connected by a motorized valve\. The HydroComponents model uses two `Tank` components \(IDZ fidelity\) connected via a `Valve` actuator, with `LevelSensor` components and an `MPCInterface` for controller coupling\. The model assembly requires 6 components and ~15 parameter specifications\.

__*Table 3\. Dual\-Tank Validation Results*__

| Metric | HydroComponents | Chen et al\. \(2026\) Reference | Difference |
|--------|-----------------|-------------------------------|------------|
| Step response RMSE \[mm\] | 1\.8 | 1\.8 | < 0\.1 |
| Steady\-state error \[mm\] | 0\.0 | 0\.0 | 0\.0 |
| FMU export time \[s\] | 12 | — | — |
| FMU file size \[MB\] | 0\.5 | — | — |

__5\.2  Three\-Pool Canal Flume__

The three\-pool flume \(Su et al\., 2026\) is modeled using three `CanalPool` components \(IDZ fidelity\), two `SluiceGate` actuators, six `LevelSensor` components, and an `MPCInterface` for DMPC coupling\. The model assembly requires 14 components\.

__*Table 4\. Three\-Pool Flume Validation Results*__

| Metric | HydroComponents | Su et al\. \(2026\) Reference | Difference |
|--------|-----------------|------------------------------|------------|
| Pool 1 step RMSE \[mm\] | 2\.1 | 1\.2 | \+0\.9 \(IDZ vs\. fitted IDZ\) |
| Pool 2 step RMSE \[mm\] | 2\.3 | 1\.3 | \+1\.0 |
| MiL DMPC RMSE \[mm\] | 4\.5 | 4\.2 | \+0\.3 |
| Model assembly time | 2 hours | 2 days \(custom\) | 12× faster |

The 0\.9–1\.0 mm RMSE increase relative to Su et al\. \(2026\) reflects the use of automatically computed IDZ parameters \(from geometry\) rather than experimentally fitted parameters\. When experimentally fitted parameters are substituted, the RMSE matches exactly\.

__5\.3  Field\-Scale Three\-Pool Canal__

A field\-scale demonstration uses a three\-pool section of the Haohanquan Main Canal \(Hebei Province, pool lengths 2\.1 km, 1\.8 km, 2\.4 km; design flow 5 m³/s; trapezoidal cross\-section\)\. The HydroComponents model uses `CanalPool` components at LSV fidelity \(20 cells per pool\) with `RadialGate` actuators\.

__*Table 5\. Field\-Scale Canal Validation Results*__

| Metric | HydroComponents \(LSV\) | HydroComponents \(IDZ\) | Field Measurement | Unit |
|--------|------------------------|------------------------|-------------------|------|
| Downstream level RMSE | 38 | 45 | — | mm |
| Wave travel time error | < 2 | < 8 | — | s |
| Steady\-state flow error | < 0\.5 | < 1\.0 | — | % |
| FMU export time | 45 | 8 | — | s |
| Simulation speed \(vs real\-time\) | 15× | 200× | — | — |

The LSV model achieves 38 mm RMSE \(compared to field measurement\), while the IDZ model achieves 45 mm RMSE—adequate for MPC design where 50 mm accuracy is typically sufficient for field\-scale canals\. The IDZ model is 13× faster than the LSV model, making it suitable for real\-time MPC execution\.

__*\[Figure 3 about here\]*__

__6  Application: MBD Pipeline Integration__

__6\.1  HydroComponents in the Seven\-Layer MBD Framework__

HydroComponents serves as the Layer 7 building block in the CHS MBD framework \(Liu et al\., 2026; Chen et al\., 2026\)\. The typical MBD workflow is:

1\. __Layer 7 \(Physical Model\)__: Assemble the system in OpenModelica using HydroComponents at LSV fidelity\. Validate against field data\.
2\. __Layer 6 \(Control Model\)__: Switch fidelity to IDZ \(one parameter change per component\)\. Export as FMU\. Import into Simulink for MPC design\.
3\. __Layer 4 \(xIL Testing\)__: Use the LSV\-fidelity FMU as the "truth model" for MiL verification\. The IDZ\-fidelity FMU serves as the MPC prediction model\.
4\. __Layers 3–1 \(Deployment\)__: The MPC designed in Simulink is auto\-generated to C code and deployed on the target hardware\.

The multi\-fidelity feature is critical for this workflow: the same component \(same connectors, same system assembly\) can serve as both the high\-fidelity truth model and the reduced\-order control model, eliminating the model translation step that is a major source of errors in traditional workflows\.

__6\.2  Comparison with Existing Tools__

__*Table 6\. HydroComponents vs\. Existing Tools*__

| Feature | HEC\-RAS | SWMM | Modelica\.Fluid | HydroComponents |
|---------|---------|------|----------------|-----------------|
| Open\-channel flow | Full SV | Dynamic wave | No | Full SV \+ IDZ |
| Pipe flow | Limited | Full | Full | Compliance \+ WH |
| Control integration | External | Rule\-based | Full | Full \+ MPC |
| FMI export | No | No | Yes | Yes |
| Multi\-fidelity | No | No | No | 5 levels |
| CHS alignment | No | No | No | Yes \(6 elements\) |
| Auto IDZ derivation | No | No | No | Yes |
| Open source | Limited | Yes | Varies | Yes \(MIT\) |

__*\[Figure 4 about here\]*__

__7  Discussion__

__7\.1  Component\-Based Modeling for Water Systems__

The component\-based approach provides three practical advantages over monolithic simulators\. First, __reusability__: the 28 components can be composed into any water conveyance system topology without custom coding\. The dual\-tank \(2 plants, 1 actuator\), three\-pool flume \(3 plants, 2 actuators\), and field canal \(3 plants, 2 actuators, different geometry\) share the same component models with different parameters\. Second, __maintainability__: each component is independently tested and versioned; improvements to the `SluiceGate` component propagate to all systems that use it\. Third, __interoperability__: FMI export enables integration with any FMI\-compatible tool, avoiding vendor lock\-in\.

__7\.2  Multi\-Fidelity Modeling and the CHS Hierarchy__

The five\-level fidelity switching implements the CHS Model–Layer Correspondence \(Theorem 3\) in software: the user selects the model level appropriate for their application \(LSV for detailed simulation, IDZ for control design, SS for planning\)\. The automatic IDZ parameter derivation from LSV geometry eliminates the manual identification step, though experimentally fitted parameters may improve accuracy for specific operating conditions \(as shown in the flume validation, §5\.2\)\.

__7\.3  Limitations__

Several limitations should be acknowledged\. First, the current library covers one\-dimensional flow only; two\-dimensional processes \(e\.g\., reservoir stratification, urban flood inundation\) are not supported\. Second, the Saint\-Venant solver uses the Preissmann scheme, which may exhibit numerical diffusion for sharp wavefronts; the Method of Characteristics is available only for pipe components\. Third, water quality processes \(advection\-dispersion, reactions\) are not included in the current version\. Fourth, the library has been validated on three systems; broader validation across a wider range of canal geometries and operating conditions is ongoing\. Fifth, OpenModelica's FMI export can occasionally produce non\-standard FMUs for complex systems; users should validate FMU behavior against the native OpenModelica simulation\.

__8  Conclusions__

This paper presents HydroComponents, an open\-source Modelica library for component\-based modeling of water conveyance systems\. The library provides 28 reusable components aligned with the CHS six\-element architecture, implements multi\-fidelity modeling across the CHS five\-level hierarchy, and supports FMI 2\.0 export for integration with the MBD pipeline\.

The key findings are:

1\. Component\-based assembly reduces model development time by 10–12× compared to custom modeling \(2 hours vs\. 2 days for the three\-pool flume system\), while achieving comparable accuracy\.

2\. Automatic IDZ parameter derivation from geometry produces models within 1 mm RMSE of experimentally fitted parameters for laboratory systems, confirming that the CHS analytical derivation provides adequate accuracy for initial control design\.

3\. Multi\-fidelity switching enables the same system model to serve as both the Layer 7 truth model \(LSV\) and the Layer 6 control model \(IDZ\), eliminating the model translation step in the MBD pipeline\.

4\. FMI export enables seamless coupling with MATLAB/Simulink, Python, and other control design environments, addressing the toolchain fragmentation identified by Liu et al\. \(2026\) as a key barrier to MBD adoption in water systems\.

HydroComponents is released under the MIT license and is available at https://github\.com/IWHR\-CHS/HydroComponents\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\.

__Software Availability__

\- __Name__: HydroComponents
\- __Developer__: CHS Research Group, Hebei University of Engineering / IWHR
\- __Contact__: lxh@iwhr\.com
\- __Year first available__: 2026
\- __Hardware required__: Standard PC
\- __Software required__: OpenModelica ≥ v1\.22 \(open source\)
\- __Programming language__: Modelica 3\.5
\- __Availability__: https://github\.com/IWHR\-CHS/HydroComponents \(MIT license\)
\- __Cost__: Free

__References__

Blochwitz, T\., Otter, M\., Akesson, J\., et al\. \(2012\)\. Functional Mockup Interface 2\.0: The standard for tool independent exchange of simulation models\. In Proceedings of the 9th International Modelica Conference \(pp\. 173–184\)\.

Brunner, G\. W\. \(2016\)\. HEC\-RAS River Analysis System: Hydraulic reference manual\. US Army Corps of Engineers\.

Chen, K\., Lei, X\., Ji, C\., Wang, C\., & Wang, H\. \(2026\)\. Model\-based definition for water systems control: A seven\-layer framework demonstrated on a dual\-tank laboratory platform\. Journal of Hydroinformatics \(submitted\)\.

DHI\. \(2024\)\. MIKE 1D Reference Manual\. Danish Hydraulic Institute\.

Fritzson, P\. \(2014\)\. Principles of object\-oriented modeling and simulation with Modelica 3\.3 \(2nd ed\.\)\. Wiley\-IEEE Press\.

Lei, X\. \(2025a\)\. Cybernetics of hydro systems: A unified control\-theoretic framework for water network operations\. Water Resources Research \(submitted\)\.

Lei, X\., & Wang, H\. \(2025\)\. Cybernetics of hydro systems: Background, technical framework and research paradigm\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 761–769\.

Lei, X\., Liu, X\., Ji, C\., Wang, C\., & Wang, H\. \(2025b\)\. From SCADA to autonomy: A multi\-agent system architecture and water systems autonomy level classification\. Journal of Water Resources Planning and Management \(submitted\)\.

Lei, X\., Zhang, Z\., Su, C\., et al\. \(2025c\)\. In\-the\-loop testing system for autonomous intelligent water networks\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 787–793\.

Liu, X\., Lei, X\., Long, Y\., & Wang, H\. \(2026\)\. Design for Operation: A model\-based framework for establishing cybernetics of hydro systems as an interdisciplinary discipline\. Environmental Modelling & Software \(submitted\)\.

Rossman, L\. A\. \(2015\)\. Storm Water Management Model User's Manual Version 5\.1\. US EPA\.

Schweiger, G\., Gomes, C\., Engel, G\., et al\. \(2019\)\. An empirical survey on co\-simulation: Promising standards, challenges and research needs\. Simulation Modelling Practice and Theory, 95, 148–163\.

Su, C\., Lei, X\., Bai, Y\., Yin, B\., Ji, C\., & Wang, H\. \(2026\)\. Experimental validation of the unified transfer function family and distributed MPC on a multi\-pool canal flume\. Journal of Irrigation and Drainage Engineering \(submitted\)\.

__Figure Captions__

__Figure 1\. __HydroComponents library architecture\. Left: the six CHS element packages with component counts\. Center: the HydroPort and SignalPort connector hierarchy\. Right: an example system assembly showing how Plant, Actuator, Sensor, and Controller components connect\.

__Figure 2\. __Multi\-fidelity implementation\. \(a\) The same three\-pool canal system assembled at LSV fidelity \(60 state variables\) and IDZ fidelity \(6 state variables\)\. \(b\) Fidelity switching: changing one parameter per component switches the entire system between fidelity levels\. \(c\) FMI export: the assembled system is exported as a single FMU for co\-simulation\.

__Figure 3\. __Validation results\. \(a\) Dual\-tank step response: HydroComponents IDZ model \(solid\) vs\. Chen et al\. \(2026\) reference \(dashed\)\. \(b\) Three\-pool flume DMPC: HydroComponents MiL \(solid\) vs\. Su et al\. \(2026\) experimental data \(dots\)\. \(c\) Field\-scale canal: HydroComponents LSV \(solid\) vs\. field measurement \(dots\) for a gate operation event\.

__Figure 4\. __MBD pipeline integration\. The complete workflow: \(1\) assemble system in OpenModelica using HydroComponents → \(2\) export as FMU → \(3\) import into Simulink for MPC design → \(4\) MiL verification \(LSV FMU as truth model, IDZ FMU as prediction model\) → \(5\) SiL with auto\-generated code → \(6\) HiL on physical hardware\.
