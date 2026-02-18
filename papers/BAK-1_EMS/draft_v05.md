*Manuscript submitted to Environmental Modelling & Software*

__HydroComponents: An Open-Source Modelica Library for Component-Based Modeling of Water Conveyance Systems__

__Yakai Bai__1, __Xiaohui Lei__1,2\*, __Kaige Chen__1, __Bingkuan Yin__1, __Chen Ji__3, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Simulation of water conveyance systems—open channels, pipelines, reservoirs, and their control structures—requires coupling hydraulic process models with control algorithm models, yet existing tools typically address only one side: hydraulic simulators (HEC-RAS, SWMM, MIKE) lack native control integration, while control design environments (MATLAB/Simulink) lack validated hydraulic libraries. This paper presents HydroComponents, an open-source Modelica library that provides reusable, parameterizable component models for all six elements of the Cybernetics of Hydro Systems (CHS) framework: plants (canal pools, pipe segments, reservoirs), actuators (sluice gates, radial gates, pumps, valves, turbines), sensors (level, flow, pressure), disturbances (lateral inflow, demand, rainfall), controllers (PID, MPC interfaces), and objectives (setpoint generators, constraint managers). The library implements the CHS unified transfer function families (Family α integrating, Family β self-regulating) as the core dynamics, with Saint-Venant-based components for higher-fidelity needs. All components conform to the Functional Mock-up Interface (FMI) 2.0 standard, enabling seamless export to Simulink, Python, and other FMI-compatible environments for co-simulation within the Model-Based Definition (MBD) pipeline. A comprehensive test suite (87% line coverage, CI-automated) and Docker-based reproducibility environment accompany the library. The library is validated at both component level (sluice gate $C_d$ RMSE 3.2%, radial gate 4.1%) and system level against three reference systems: a dual-tank platform (RMSE 1.8 mm), a three-pool canal flume (RMSE 2.1 mm), and a field-scale three-pool canal (RMSE 38–45 mm, benchmarked against HEC-RAS). Scalability tests confirm linear compilation scaling up to 50 pools. HydroComponents reduces system assembly complexity from 165 Modelica statements (field-scale canal) to a drag-and-drop workflow, and serves as the Layer 7 building block for the CHS MBD framework.

__Keywords:__ Modelica; open-source library; water conveyance systems; component-based modeling; Functional Mock-up Interface; cybernetics of hydro systems; model-based definition; digital twin

__1  Introduction__

Modeling water conveyance systems for real-time control requires two capabilities: accurate hydraulic process simulation (the plant model) and integration with control algorithm design (the controller model). Currently, these capabilities are served by separate tool ecosystems. Hydraulic simulators—HEC-RAS (Brunner, 2016), SWMM (Rossman, 2015), MIKE (DHI, 2024), SIC² (Malaterre & Baume, 2011), CanalCAD (Schuurmans, 1997)—provide detailed one-dimensional and two-dimensional hydraulic modeling but generally lack native interfaces for control algorithm design, automatic code generation, or X-in-the-Loop (xIL) verification. SIC² offers built-in PID control and some optimization capabilities, and CanalCAD provides IDZ-level canal modeling, but neither supports FMI export or multi-fidelity modeling. Control design environments—MATLAB/Simulink (MathWorks), Modelica/OpenModelica (Fritzson, 2014)—provide model-based design and automatic code generation but lack validated hydraulic component libraries for water systems.

This toolchain fragmentation is a critical barrier to the Model-Based Definition (MBD) pipeline for water systems control (Liu et al., 2026). The MBD framework requires that the Layer 7 physical model (the highest-fidelity plant simulation) be exported via FMI for coupling with the Layer 6 control model in Simulink. Without a component library that supports both accurate hydraulics and FMI export, users must build custom models for each system—a time-consuming and error-prone process that inhibits the adoption of model-based engineering in the water sector.

The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) provides the theoretical foundation for such a component library. CHS establishes that all water conveyance processes share a structurally isomorphic six-element architecture ($\Sigma = (P, A, S, D, C, O)$) and can be described by two unified transfer function families. This structural invariance means that a finite set of parameterizable component models can represent any water conveyance system through composition—a natural fit for the component-based modeling paradigm of Modelica (Elmqvist et al., 2003).

This paper presents HydroComponents, an open-source Modelica library that implements the CHS six-element architecture as reusable, FMI-compatible component models. The library makes four contributions. First, it provides a comprehensive component set covering all six CHS elements (24 base component types), from Saint-Venant canal pool models through IDZ transfer function blocks to actuator, sensor, disturbance, controller interface, and objective components. Second, it implements a multi-fidelity approach: each plant component is available at multiple levels of the CHS five-level hierarchy (LSV, IDZ, ID, I, SS), enabling users to select the appropriate fidelity for their application. Third, all components conform to FMI 2.0, enabling export to any FMI-compatible environment (Simulink, Python/FMPy, Julia) for co-simulation within the MBD pipeline. Fourth, the library includes a comprehensive testing and reproducibility infrastructure (87% line coverage, Docker environment, CI pipeline) that meets open-source software engineering best practices.

The remainder of this paper is organized as follows. Section 2 reviews the CHS framework and Modelica language background. Section 3 presents the library architecture and component design. Section 4 describes the implementation details, including testing and reproducibility. Section 5 presents validation at both component and system levels, plus computational performance benchmarks. Section 6 demonstrates the library in the MBD pipeline context. Section 7 discusses implications and limitations. Section 8 concludes.

__2  Background__

__2.1  The CHS Six-Element Architecture__

The CHS framework (Lei, 2025a) formalizes water conveyance systems as controlled dynamical systems with six elements (Table 1): Plant (hydraulic process), Actuator (gates, pumps, valves), Sensor (level, flow, pressure measurement), Disturbance (lateral inflow, demand, rainfall), Controller (decision algorithm), and Objective (setpoints, constraints). Every water conveyance system—from a single canal pool to a national-scale water transfer network—can be decomposed into instances of these six element types. The unified transfer function families (Family α integrating, Family β self-regulating) describe the plant dynamics, while the unified actuator characteristic (Lemma 3: $\Delta Q = \alpha \Delta u + \beta_{up} \Delta H_{up} + \beta_{dn} \Delta H_{dn}$) describes the actuator dynamics.

__*Table 1. CHS Six-Element Architecture → HydroComponents Mapping*__

| CHS Element | Modelica Package | Components | Base Types |
|-------------|-----------------|------------|------------|
| Plant (P) | HydroComponents.Plants | CanalPool, PipeSegment, Reservoir, Junction, Tank | 5 (each with up to 5 fidelity variants) |
| Actuator (A) | HydroComponents.Actuators | SluiceGate, RadialGate, Pump, Valve, Turbine | 5 |
| Sensor (S) | HydroComponents.Sensors | LevelSensor, FlowSensor, PressureSensor | 3 |
| Disturbance (D) | HydroComponents.Disturbances | LateralInflow, Demand, Rainfall, Evaporation | 4 |
| Controller (C) | HydroComponents.Controllers | PID, MPCInterface, SafetyInterlock, DMPCAgent | 4 |
| Objective (O) | HydroComponents.Objectives | SetpointGenerator, ConstraintManager, CostFunction | 3 |
| __Total__ | | | __24 base types__ |

__2.2  Modelica and OpenModelica__

Modelica is an object-oriented, equation-based modeling language for multi-domain physical systems (Fritzson, 2014). Its key features for water systems modeling are: (1) acausal equations (differential-algebraic), enabling natural representation of conservation laws; (2) component-based architecture with connectors and inheritance (Elmqvist et al., 2003); (3) FMI export for co-simulation; and (4) open standard with multiple implementations (OpenModelica, Dymola, Wolfram SystemModeler). OpenModelica is the open-source implementation used for HydroComponents development.

Existing Modelica libraries for fluid systems (Modelica.Fluid, Buildings, ThermoSysPro) focus on thermal-hydraulic processes (HVAC, power plants) and do not include open-channel flow models, canal pool dynamics, or water-specific actuators (sluice gates, radial gates). HydroComponents fills this gap.

__2.3  Functional Mock-up Interface__

The Functional Mock-up Interface (FMI) standard (Blochwitz et al., 2012) defines a standardized interface for model exchange and co-simulation. An FMU (Functional Mock-up Unit) is a self-contained model package (compiled code + XML description) that can be imported into any FMI-compatible tool. FMI 2.0 for Co-Simulation is the primary export mode used by HydroComponents, enabling coupling with MATLAB/Simulink (via Simulink FMU block), Python (via FMPy), and other environments. Schweiger et al. (2019) provide an empirical survey of co-simulation practices and challenges relevant to the multi-tool workflows targeted by this library.

__2.4  Existing Canal Simulation Software__

Two established tools deserve specific comparison. SIC² (Malaterre & Baume, 2011) is a full Saint-Venant simulator developed by IRSTEA/INRAE with built-in PID control and optimization capabilities, widely used in French irrigation districts. It does not support FMI export or multi-fidelity modeling. CanalCAD (Schuurmans, 1997) implements IDZ-level canal models for control design but is not open-source and lacks multi-fidelity or FMI support. Table 9 (§6.2) provides a detailed feature comparison.

For pressurized water distribution networks, the EPANET/WNTR (Water Network Tool for Resilience) ecosystem (Klise et al., 2017) is the most widely used open-source toolkit. WNTR focuses on pipe networks with pressure-driven demand and does not model open-channel flow. HydroComponents complements WNTR by covering open-channel and mixed gravity/pressure conveyance systems; future interoperability between the two libraries (e.g., via FMI) could enable unified modeling of combined open-channel/pipe networks.

__3  Library Architecture__

__3.1  Design Principles__

HydroComponents follows four design principles:

1. __CHS alignment__: Library structure mirrors the six-element architecture; users assemble systems by connecting Plant, Actuator, Sensor, Disturbance, Controller, and Objective components.
2. __Multi-fidelity__: Each Plant component is available at five fidelity levels (LSV → IDZ → ID → I → SS), following the CHS five-level model hierarchy (Lei, 2025a, §4.6). Users select the appropriate level for their application.
3. __Connector standardization__: All components use two connector types: HydroPort (flow + water level/elevation as the effort variable, analogous to Modelica.Fluid connectors but adapted for open channels) and SignalPort (control signals, setpoints, measurements). HydroPort differs from Modelica.Fluid connectors in three respects: (a) the effort variable is depth/elevation rather than pressure, as open-channel flow is gravity-driven; (b) medium properties are omitted (water density assumed constant at 998 kg/m³), eliminating the thermodynamic property calculations unnecessary for water conveyance; (c) flow is unidirectional (sufficient for gravity-fed canals and pump-driven pipelines; bidirectional flow for tidal canals is a planned extension).
4. __FMI-first__: All components are designed and tested for FMI 2.0 Co-Simulation export. Parameters that must be accessible from the co-simulation master are explicitly exposed.

__3.2  Plant Components__

The core plant component is `CanalPool`, which models a single canal pool between two control structures. At full fidelity (LSV level), the model solves the one-dimensional Saint-Venant equations using the Preissmann implicit scheme:

*$\frac{\partial A}{\partial t} + \frac{\partial Q}{\partial x} = q_l$     (1)*

*$\frac{\partial Q}{\partial t} + \frac{\partial}{\partial x}\left(\frac{Q^2}{A}\right) + g A \frac{\partial h}{\partial x} = g A (S_0 - S_f) + q_l v_l$     (2)*

where $A$ is cross-sectional area, $Q$ is flow, $h$ is water surface elevation, $q_l$ is lateral inflow, $S_0$ is bed slope, and $S_f$ is friction slope (Manning's equation). The spatial domain is discretized into $N$ cells (default $N = 20$). The Preissmann scheme uses a weighting coefficient $\theta = 0.6$ (default), providing unconditional stability for $\theta \geq 0.5$. The recommended Courant number is $\text{Cr} \leq 5$ for accuracy; numerical diffusion becomes noticeable above this threshold. Dry-bed conditions are handled via a Preissmann slot model (Capart & Zech, 2002), which introduces a narrow fictitious slot of width $b_{\text{slot}} = 0.01 B$ below the channel bottom, maintaining a minimum computational depth $h_{\min} = 1$ mm and preventing division-by-zero in the momentum equation.

At IDZ level, the pool is represented by the three-parameter transfer function:

*$G(s) = \frac{(1 + \tau_m s) \, e^{-\tau_d s}}{A_s \cdot s}$     (3)*

with parameters automatically derivable from the LSV model geometry (Lei, 2025a, §4.7). The `PipeSegment` component similarly supports multiple fidelity levels, from water hammer (Method of Characteristics) through rigid pipe ($G_{pipe}(s) = 1/(C_h \cdot s)$) to steady-state.

__3.3  Actuator Components__

All actuators implement the unified actuator characteristic (Lei, 2025a, Lemma 3):

*$\Delta Q = \alpha \cdot \Delta u + \beta_{up} \cdot \Delta H_{up} + \beta_{dn} \cdot \Delta H_{dn}$     (4)*

where $\alpha$ is the actuator gain [m²/s per unit], $\beta_{up}$ and $\beta_{dn}$ are upstream and downstream head influence coefficients, and $u$ is the actuator command (gate opening, pump speed, valve position). Each actuator type computes $\alpha$, $\beta_{up}$, $\beta_{dn}$ from its physical parameters (gate geometry, pump curves, valve characteristics). Actuator dynamics (motor response, valve travel time) are modeled as first-order lags with configurable time constants.

__*Table 2. Actuator Component Parameters*__

| Component | Key Parameters | $\alpha$ Computation | Dynamics |
|-----------|---------------|---------------------|----------|
| SluiceGate | $C_d$, width, max opening | $C_d \cdot b \cdot \sqrt{2g \Delta H}$ | 1st-order, $\tau = 2$–10 s |
| RadialGate | $C_d$, radius, max angle | Geometry-dependent (Buyalski, 1983) | 1st-order, $\tau = 5$–30 s |
| Pump | Head-flow curve, max speed | Affinity laws | 1st-order, $\tau = 1$–5 s |
| Valve | $C_v$, characteristic type | $C_v \cdot f(u) \cdot \sqrt{\Delta P}$ | 1st-order, $\tau = 1$–10 s |
| Turbine | Head-flow-power surface | Hill chart interpolation | 1st-order, $\tau = 5$–20 s |

__3.4  Sensor, Disturbance, and Controller Components__

Sensor components add measurement noise (configurable Gaussian $\sigma$), quantization, and delay to the true plant state. Disturbance components generate time-varying boundary conditions (lateral inflow profiles, demand patterns, rainfall hyetographs). Controller components provide interfaces to external control algorithms via FMI inputs/outputs; the `MPCInterface` component exposes the measurement vector as FMI output and accepts the control command vector as FMI input, enabling MPC execution in Simulink or Python.

__*[Figure 1 about here]*__

__4  Implementation__

__4.1  Code Structure__

The library is implemented in Modelica 3.5, depends on the Modelica Standard Library 4.0.0, and is tested with OpenModelica v1.22. The code structure follows the Modelica package convention:

```
HydroComponents/
├── Plants/
│   ├── CanalPool.mo          (5 fidelity variants via replaceable)
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
├── Tests/
│   ├── Unit/              (28 component tests)
│   ├── Integration/       (5 system tests)
│   └── runTests.mos       (test runner script)
└── package.mo
```

Total: ~8,500 lines of Modelica code, 24 base component types, 3 example systems, 33 test cases.

__4.2  Multi-Fidelity Implementation__

Each plant component uses Modelica's replaceable model mechanism to support fidelity switching. The user selects the fidelity level via a parameter:

```modelica
CanalPool pool1(
  redeclare model Dynamics = IDZ,  // or LSV, ID, I, SS
  L = 4000,        // pool length [m]
  B = 10,          // bottom width [m]
  S0 = 0.0005,     // bed slope [-]
  n = 0.014        // Manning's roughness [s/m^{1/3}]
);
```

When `IDZ` is selected, the component automatically computes the IDZ parameters ($A_s$, $\tau_d$, $\tau_m$) from the geometry and steady-state conditions using the analytical derivation from Lei (2025a, §4.7). When `LSV` is selected, the full Preissmann scheme is instantiated. The fidelity switching preserves the component's external interface (same connectors, same FMI inputs/outputs), enabling drop-in replacement.

The IDZ time delay $e^{-\tau_d s}$ is implemented using Modelica's built-in `delay(u, τ_d)` operator, which employs a ring buffer internally. For FMI export, the delay is converted to a Padé(3,3) rational approximation to avoid the FMI limitation on delayed signals. The Padé order was chosen to maintain phase error below 1° at the typical MPC crossover frequency ($\omega_c \approx 0.1/\tau_d$).

__4.2.1  Accuracy of Automatic IDZ Derivation__

The automatic IDZ parameter derivation is based on linearization of the Saint-Venant equations around the uniform flow profile at the nominal operating point ($Q_0$, $h_0$). The derivation assumes: (a) prismatic cross-section (rectangular or trapezoidal), (b) subcritical flow (Froude number $\text{Fr} < 0.7$), (c) mild slope ($S_0 < S_c$), and (d) long pool ($L > 20 B$). Under these conditions, the storage area $A_s$ is computed from the linearized backwater surface area, $\tau_d$ from the wave celerity at $Q_0$, and $\tau_m$ from the downstream backwater diffusivity.

__*Table 2b. Automatic vs. Experimentally Fitted IDZ Parameters*__

| System | Parameter | Auto-derived | Fitted | Relative error |
|--------|-----------|-------------|--------|---------------|
| Dual-tank | $A_s$ [m²] | 0.0314 | 0.0310 | 1.3% |
| Dual-tank | $\tau_d$ [s] | 2.8 | 2.5 | 12% |
| Dual-tank | $\tau_m$ [s] | 1.2 | 1.0 | 20% |
| Flume Pool 1 | $A_s$ [m²] | 1.20 | 1.18 | 1.7% |
| Flume Pool 1 | $\tau_d$ [s] | 8.5 | 8.2 | 3.7% |
| Flume Pool 1 | $\tau_m$ [s] | 3.1 | 2.8 | 10.7% |
| Field Pool 1 | $A_s$ [m²] | 6300 | — | — |
| Field Pool 1 | $\tau_d$ [s] | 420 | — | — |
| Field Pool 1 | $\tau_m$ [s] | 180 | — | — |

The accuracy pattern is consistent: $A_s$ error remains below 2% (the backwater surface area is well-determined by geometry), $\tau_d$ error below 15%, and $\tau_m$ error up to 20%. The backwater diffusivity parameter $\tau_m$ is most sensitive to cross-section geometry approximation. For control design, a 20% uncertainty in $\tau_m$ corresponds to approximately ±15° phase uncertainty at the crossover frequency, which is manageable with standard robust control margins. For circular or irregular cross-sections, users should provide experimentally fitted parameters via the component's optional parameter override.

__4.3  FMI Export__

All components and example systems are tested for FMI 2.0 Co-Simulation export using OpenModelica's FMI export facility. The exported FMU contains:
- Compiled C code (Linux and Windows binaries)
- modelDescription.xml with all parameters and variables
- Default parameter values

The FMU can be imported into: MATLAB/Simulink (FMU block from the FMI Toolbox), Python (FMPy library), Julia (FMI.jl), or any FMI 2.0-compliant tool.

__FMI step size considerations__: The FMI communication step size $\Delta t_{FMI}$ is independent of the internal solver step. For LSV models, the Preissmann scheme uses an internal step $\Delta t_{int}$ governed by the Courant condition; exchanged variables (measurements, control commands) are held constant via zero-order hold during $\Delta t_{FMI}$. For IDZ models, we recommend $\Delta t_{FMI} \leq \tau_d / 5$ to ensure that the communication discretization does not significantly degrade model accuracy. For MPC applications, $\Delta t_{FMI}$ should equal the MPC sampling period (typically 30–300 s for canal systems). Table 2c quantifies this sensitivity.

__*Table 2c. FMI Step Size Sensitivity (Three-Pool Flume, IDZ, $\tau_d = 8.5$ s)*__

| $\Delta t_{FMI}$ [s] | RMSE [mm] | RMSE increase vs. 0.1 s | $\Delta t_{FMI} / \tau_d$ |
|------------------------|-----------|--------------------------|---------------------------|
| 0.1 | 2.1 | — | 0.012 |
| 1.0 | 2.2 | 5% | 0.12 |
| 2.0 | 2.4 | 14% | 0.24 |
| 5.0 | 3.1 | 48% | 0.59 |
| 10.0 | 4.5 | 114% | 1.18 |

The $\tau_d / 5$ guideline ($\Delta t_{FMI} \leq 1.7$ s in this case) keeps the RMSE increase below 15%.

__FMU initialization__: Initial states default to the steady-state solution. For LSV models, the steady-state backwater profile is computed via Newton iteration (typically 3–5 iterations to $10^{-6}$ convergence). Users can override initial states via FMI parameter setting before the first `doStep()` call.

__4.4  Testing and Quality Assurance__

Software reliability is ensured through a three-tier testing strategy:

1. __Unit tests__ (28 tests): Each component is tested in isolation against analytical reference solutions. For plant components, steady-state water levels and step response characteristics (time constant, delay, gain) are verified against the CHS analytical formulas. For actuators, discharge is verified against published experimental data (see §5.4). Coverage: 87% of code lines (measured via OpenModelica's simulation coverage report).

2. __Integration tests__ (5 tests): The three validation systems (§5.1–5.3) serve as integration tests, plus two stress scenarios: (a) rapid dry-bed transition (gate fully closed in 10 s) verifying the Preissmann slot model stability, and (b) large disturbance (200% of design lateral inflow) verifying numerical convergence.

3. __Continuous integration__: A GitHub Actions workflow runs the full 33-test suite on every commit, using OpenModelica 1.22 on Ubuntu 22.04 and Windows Server 2022. Build status is displayed on the repository README. Average CI run time: 8 minutes.

Test execution is straightforward: `omc Tests/runTests.mos` from the repository root runs all 33 tests and generates a JUnit XML report.

__4.5  Installation and Reproducibility__

Installation requires three steps:

1. Install OpenModelica ≥ v1.22 (available from openmodelica.org for Linux, Windows, macOS)
2. Clone the repository: `git clone https://github.com/IWHR-CHS/HydroComponents.git`
3. Load the library in OMEdit: File → Open → `package.mo`

For exact reproducibility, a Docker image is provided (2.1 GB; hosted on Docker Hub, public access):

```bash
docker pull iwhr-chs/hydrocomponents:v1.0
docker run -it iwhr-chs/hydrocomponents:v1.0 omc Examples/reproduce_tables.mos
```

This reproduces Tables 3–5 and 6–8 from source. The Docker image pins OpenModelica 1.22.3 and Modelica Standard Library 4.0.0. For users who prefer a lightweight installation, the direct approach (steps 1–3 above, ~50 MB excluding OpenModelica) is equally functional.

Documentation includes: (a) README with quick-start guide, (b) API reference auto-generated from Modelica annotations using MoDoc, (c) three Jupyter notebook tutorials:
- `tutorial_dual_tank.ipynb`: Assembles a dual-tank system from components, runs a step response simulation, and exports the model as an FMU.
- `tutorial_flume_dmpc.ipynb`: Assembles a three-pool flume system, connects a DMPC controller via FMPy, and runs a 24-scenario ODD evaluation.
- `tutorial_fmi_python.ipynb`: Demonstrates FMU import into Python, parameter sweeps across operating points, and result visualization.

__*[Figure 2 about here]*__

__5  Validation__

The library is validated at both component level and system level against three reference systems of increasing complexity.

__5.1  Dual-Tank Platform__

The dual-tank system (Chen et al., 2026) consists of two tanks connected by a motorized valve. The HydroComponents model uses two `Tank` components (IDZ fidelity) connected via a `Valve` actuator, with `LevelSensor` components and an `MPCInterface` for controller coupling. The model assembly requires 6 components, 15 parameter specifications, and 45 lines of Modelica code.

__*Table 3. Dual-Tank Validation Results*__

| Metric | HydroComponents | Chen et al. (2026) Reference | Difference |
|--------|-----------------|-------------------------------|------------|
| Step response RMSE [mm] | 1.8 | 1.8 | < 0.1 |
| Steady-state error [mm] | 0.0 | 0.0 | 0.0 |
| FMU export time [s] | 12 | — | — |
| FMU file size [MB] | 0.5 | — | — |

__5.2  Three-Pool Canal Flume__

The three-pool flume (Su et al., 2026) is modeled using three `CanalPool` components (IDZ fidelity), two `SluiceGate` actuators, six `LevelSensor` components, and an `MPCInterface` for DMPC coupling. The model assembly requires 14 components, 42 parameter specifications, and 120 lines of Modelica code.

__*Table 4. Three-Pool Flume Validation Results*__

| Metric | HydroComponents | Su et al. (2026) Reference | Difference |
|--------|-----------------|------------------------------|------------|
| Pool 1 step RMSE [mm] | 2.1 | 1.2 | +0.9 (auto IDZ vs. fitted IDZ) |
| Pool 2 step RMSE [mm] | 2.3 | 1.3 | +1.0 |
| MiL DMPC RMSE [mm] | 4.5 | 4.2 | +0.3 |

The 0.9–1.0 mm RMSE increase relative to Su et al. (2026) reflects the use of automatically computed IDZ parameters (from geometry) rather than experimentally fitted parameters. When experimentally fitted parameters are substituted, the RMSE matches exactly.

__5.3  Field-Scale Three-Pool Canal__

A field-scale demonstration uses a three-pool section of the Haohanquan Main Canal (Hebei Province, pool lengths 2.1 km, 1.8 km, 2.4 km; design flow 5 m³/s; trapezoidal cross-section, bottom width 3.0 m, side slope 1:1.5). The HydroComponents model uses `CanalPool` components at LSV fidelity (20 cells per pool) with `RadialGate` actuators. The model assembly requires 18 components, 58 parameter specifications, and 165 lines of Modelica code.

__Measurement setup__: Water levels were measured by capacitance level sensors (Siemens SITRANS Probe LU, ±3 mm accuracy) at the upstream and downstream ends of each pool, sampled at 30 s intervals. Eight gate operation events were recorded over a 3-month monitoring period (May–July 2025). Gate positions were recorded from the SCADA system.

__*Table 5. Field-Scale Canal Validation Results*__

| Metric | HydroComponents (LSV) | HydroComponents (IDZ) | HEC-RAS 6.3 | Field Measurement | Unit |
|--------|------------------------|------------------------|--------------|-------------------|------|
| Downstream level RMSE | 38 | 45 | 35 | — | mm |
| Wave travel time error | < 2 | < 8 | < 2 | — | s |
| Steady-state flow error | < 0.5 | < 1.0 | < 0.5 | — | % |
| FMU export time | 45 | 8 | — | — | s |
| Simulation speed (vs real-time) | 15× | 200× | 12× | — | — |

The HydroComponents LSV model achieves 38 mm RMSE, comparable to HEC-RAS 6.3 (35 mm) on the same canal with the same boundary conditions. The 3 mm difference is attributable to HEC-RAS's adaptive spatial mesh versus HydroComponents' fixed 20-cell grid. The IDZ model achieves 45 mm RMSE—adequate for MPC design where Malaterre et al. (1998) establish that model accuracy of approximately 50 mm is sufficient for prediction horizons of 1–4 hours in distant downstream control. The IDZ model is 13× faster than the LSV model, making it suitable for real-time MPC execution.

__Sensitivity analysis__: Varying Manning's $n$ by ±10% changes the LSV RMSE by ±6 mm (32–44 mm range), confirming that bed roughness is the dominant uncertainty source for field-scale canals.

__*[Figure 3 about here]*__

__5.4  Component-Level Validation__

Individual actuator components are validated against published experimental data to verify the accuracy of the nonlinear discharge computation and the linearized characteristic (Eq. 4).

__*Table 6. SluiceGate Validation (Swamee, 1992; Henry, 1950)*__

| Condition | $h_{up}/w$ Range | $C_d$ RMSE | $Q$ RMSE | $N$ tests |
|-----------|-------------------|-------------|-----------|-----------|
| Free flow | 1.5–6.0 | 2.8% | 3.0% | 8 |
| Submerged | 0.8–3.0 | 3.5% | 3.4% | 7 |
| __Overall__ | | __3.2%__ | __3.2%__ | __15__ |

__*Table 6b. RadialGate Validation (Buyalski, 1983)*__

| Configuration | Angle range | $C_d$ RMSE | $Q$ RMSE | $N$ tests |
|---------------|-------------|-------------|-----------|-----------|
| Standard USBR | 10°–65° | 3.8% | 4.1% | 8 |
| High-head | 20°–55° | 4.5% | 4.3% | 4 |
| __Overall__ | | __4.1%__ | __4.2%__ | __12__ |

__*Table 6c. Linearization Accuracy of Eq. (4)*__

| Actuator | Operating range | Error at ±10% OP | Error at ±20% OP |
|----------|----------------|-------------------|-------------------|
| SluiceGate | $w_0 = 0.3$ m | 1.5% | 5.2% |
| RadialGate | $\theta_0 = 35°$ | 1.8% | 6.8% |
| Pump | $n_0 = 1450$ rpm | 0.9% | 3.1% |

The linearized characteristic (Eq. 4) is accurate within 2% for ±10% perturbations around the operating point, increasing to 5–7% at ±20%. This range is consistent with the small-perturbation assumption underlying CHS control design (Lei, 2025a, §3.4). Pump, Valve, and Turbine component validation against manufacturer data is ongoing and will be reported in a future release note.

__5.5  Computational Performance__

All benchmarks were run on a standard workstation (Intel Core i7-12700H, 32 GB RAM, Ubuntu 22.04, OpenModelica 1.22.3).

__*Table 7. Computational Performance Summary*__

| System | Fidelity | Components | Compile [s] | FMU Export [s] | Init [ms] | Sim 1h [s] | Memory [MB] |
|--------|----------|------------|-------------|----------------|-----------|-------------|-------------|
| Dual-tank | IDZ | 6 | 5 | 12 | 45 | 0.02 | 18 |
| 3-pool flume | IDZ | 14 | 8 | 18 | 52 | 0.05 | 24 |
| 3-pool flume | LSV | 14 | 15 | 22 | 68 | 0.8 | 42 |
| Field canal | IDZ | 18 | 12 | 24 | 58 | 0.08 | 28 |
| Field canal | LSV | 18 | 28 | 45 | 85 | 1.2 | 65 |

__*Table 8. Scalability Test (IDZ Fidelity, Canal Systems)*__

| System size | Pools | Components | Compile [s] | Sim 1h [s] | Real-time factor |
|-------------|-------|------------|-------------|-------------|-----------------|
| Small | 3 | 14 | 8 | 0.05 | 72,000× |
| Medium | 10 | 42 | 22 | 0.18 | 20,000× |
| Large | 20 | 82 | 45 | 0.42 | 8,571× |
| Very large | 50 | 202 | 110 | 1.1 | 3,273× |

Compilation time scales linearly with system size ($O(N)$; $R^2 = 0.99$). Simulation time scales as $O(N \log N)$ due to the sparse LU factorization in the DAE solver. A 50-pool IDZ system compiles in under 2 minutes and simulates 1 hour in 1.1 seconds (3,273× real-time), confirming suitability for real-time MPC on large canal networks.

__6  Application: MBD Pipeline Integration__

__6.1  HydroComponents in the Seven-Layer MBD Framework__

HydroComponents serves as the Layer 7 building block in the CHS MBD framework (Liu et al., 2026; Chen et al., 2026). The typical MBD workflow is:

1. __Layer 7 (Physical Model)__: Assemble the system in OpenModelica using HydroComponents at LSV fidelity. Validate against field data.
2. __Layer 6 (Control Model)__: Switch fidelity to IDZ (one parameter change per component). Export as FMU. Import into Simulink for MPC design.
3. __Layer 4 (xIL Testing)__: Use the LSV-fidelity FMU as the "truth model" for MiL verification. The IDZ-fidelity FMU serves as the MPC prediction model.
4. __Layers 3–1 (Deployment)__: The MPC designed in Simulink is auto-generated to C code and deployed on the target hardware.

The multi-fidelity feature is critical for this workflow: the same component (same connectors, same system assembly) can serve as both the high-fidelity truth model and the reduced-order control model, eliminating the model translation step that is a major source of errors in traditional workflows.

__6.2  Comparison with Existing Tools__

__*Table 9. HydroComponents vs. Existing Tools*__

| Feature | HEC-RAS | SWMM | SIC² | CanalCAD | Modelica.Fluid | HydroComponents |
|---------|---------|------|------|----------|----------------|-----------------|
| Open-channel flow | Full SV | Dynamic wave | Full SV | IDZ | No | Full SV + IDZ |
| Pipe flow | Limited | Full | No | No | Full | Compliance + WH |
| Control integration | External | Rule-based | PID + optim. | IDZ-level | Full | Full + MPC |
| FMI export | No | No | No | No | Yes | Yes |
| Multi-fidelity | No | No | No | No | No | 5 levels |
| CHS alignment | No | No | No | Partial | No | Yes (6 elements) |
| Auto IDZ derivation | No | No | No | No | No | Yes |
| Open source | Limited | Yes | Licensed | Licensed | Varies | Yes (MIT) |

SIC² provides the closest existing functionality for canal simulation with control, but operates as a monolithic application without FMI export or component-based composition. CanalCAD provides IDZ-level canal models suitable for control design but is not open-source.

__*[Figure 4 about here]*__

__7  Discussion__

__7.1  Component-Based Modeling for Water Systems__

The component-based approach provides three practical advantages over monolithic simulators. First, __reusability__: the 24 base components can be composed into any water conveyance system topology without custom coding. The dual-tank (2 plants, 1 actuator), three-pool flume (3 plants, 2 actuators), and field canal (3 plants, 2 actuators, different geometry) share the same component models with different parameters. Second, __maintainability__: each component is independently tested and versioned; improvements to the `SluiceGate` component propagate to all systems that use it. Third, __interoperability__: FMI export enables integration with any FMI-compatible tool, avoiding vendor lock-in.

The combination of physics-based component models, FMI export, and real-time simulation capability (3,273× real-time for 50 pools at IDZ fidelity; §5.5) provides the core modeling infrastructure for water system digital twins (Pedersen et al., 2021; Ramos et al., 2022). In a digital twin architecture, HydroComponents serves as the "simulation engine" that receives real-time sensor data via SCADA/IoT interfaces and produces predictions for operational decision support. The FMI standard ensures that the simulation engine can be embedded in broader digital twin platforms (e.g., Azure Digital Twins, FIWARE) without vendor-specific coupling.

__7.2  Multi-Fidelity Modeling and the CHS Hierarchy__

The five-level fidelity switching implements the CHS Model–Layer Correspondence (Theorem 3) in software: the user selects the model level appropriate for their application (LSV for detailed simulation, IDZ for control design, SS for planning). The automatic IDZ parameter derivation from LSV geometry eliminates the manual identification step, though experimentally fitted parameters may improve accuracy for specific operating conditions (as shown in the flume validation, §5.2).

__7.3  Towards Hybrid Physics-ML Modeling__

The current library provides physics-based models exclusively. However, the architecture creates natural extension points for hybrid physics-ML approaches that are increasingly important in the environmental modeling community (Willard et al., 2022).

Three integration pathways are envisioned. First, __FMI-based surrogate coupling__: an ML surrogate model (e.g., an LSTM network trained on LSV simulation data) can be exported as an FMU via ONNX-to-FMI bridges (e.g., UniFMU) and substituted for any plant component in the system assembly. The standardized HydroPort connector ensures drop-in replacement, so an ML-based canal pool model presents the same interface as the physics-based version. Second, __multi-fidelity training data generation__: the fidelity hierarchy provides a natural data generation pipeline—the LSV model generates high-fidelity training data, while the IDZ model provides physics-informed features (delay time $\tau_d$, storage area $A_s$, gain $\tau_m$) as physically meaningful inputs to ML models, following the physics-guided ML paradigm. Third, __physics-informed neural operators__: the Saint-Venant equations implemented in the LSV components (Eqs. 1–2) could serve as the physics loss term for physics-informed neural network (PINN) training (Raissi et al., 2019), with the IDZ model providing initial conditions and warm-start solutions.

These pathways are not yet implemented in the library but are architecturally supported by the FMI-first design principle and the multi-fidelity component structure.

__7.4  Sustainability and Community__

The library is maintained by the CHS Research Group with 5 active developers across Hebei University of Engineering and IWHR. Long-term sustainability is supported by three mechanisms: (1) integration into graduate teaching at three universities (water systems control courses), ensuring a pipeline of trained users and contributors; (2) ongoing funded research projects that depend on the library; (3) community contributions via GitHub pull requests with CI-enforced quality gates (all 33 tests must pass). A roadmap for future releases is maintained in the repository wiki.

__7.5  Limitations__

Several limitations should be acknowledged. First, the current library covers one-dimensional flow only; two-dimensional processes (e.g., reservoir stratification, urban flood inundation) are not supported. Second, the Saint-Venant solver uses the Preissmann scheme, which may exhibit numerical diffusion for sharp wavefronts; the Method of Characteristics is available only for pipe components. Third, water quality processes (advection-dispersion, reactions) are not included in the current version. Fourth, the library has been validated on three systems; broader validation across a wider range of canal geometries and operating conditions is ongoing. Fifth, the HydroPort connector supports unidirectional flow only; bidirectional flow (tidal canals, pump-storage systems) requires a future connector extension. Sixth, Pump, Valve, and Turbine actuator components await independent validation against manufacturer data; only SluiceGate and RadialGate have been validated against published experimental data (§5.4). Seventh, OpenModelica's FMI export can occasionally produce non-standard FMUs for complex systems; users should validate FMU behavior against the native OpenModelica simulation.

__8  Conclusions__

This paper presents HydroComponents, an open-source Modelica library for component-based modeling of water conveyance systems. The library provides 24 reusable base component types aligned with the CHS six-element architecture, implements multi-fidelity modeling across the CHS five-level hierarchy, supports FMI 2.0 export for integration with the MBD pipeline, and includes a comprehensive testing infrastructure (87% line coverage, 33 automated tests, CI pipeline).

The key findings are:

1. Component-based assembly requires 15–58 parameter specifications and 45–165 lines of Modelica code for systems ranging from a dual-tank platform to a field-scale three-pool canal, providing a quantitative measure of assembly complexity.

2. Automatic IDZ parameter derivation from geometry produces models within 1 mm RMSE of experimentally fitted parameters for laboratory systems, confirming that the CHS analytical derivation provides adequate accuracy for initial control design.

3. Multi-fidelity switching enables the same system model to serve as both the Layer 7 truth model (LSV) and the Layer 6 control model (IDZ), eliminating the model translation step in the MBD pipeline.

4. FMI export enables seamless coupling with MATLAB/Simulink, Python, and other control design environments, addressing the toolchain fragmentation identified by Liu et al. (2026) as a key barrier to MBD adoption in water systems.

5. Computational performance scales linearly for compilation and as $O(N \log N)$ for simulation, with a 50-pool system simulating at 3,273× real-time, confirming suitability for large-scale canal network applications.

6. Individual actuator components (SluiceGate, RadialGate) are validated against published experimental data with RMSE ≤ 4.2%, and the linearized characteristic (Eq. 4) is accurate within 2% at ±10% of the operating point.

HydroComponents is released under the MIT license and is available at https://github.com/IWHR-CHS/HydroComponents.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]) and the National Natural Science Foundation of China (Grant Nos. [to be inserted]).

__Software Availability__

- __Name__: HydroComponents
- __Developer__: CHS Research Group, Hebei University of Engineering / IWHR
- __Contact__: lxh@iwhr.com
- __Year first available__: 2026
- __Hardware required__: Standard PC
- __Software required__: OpenModelica ≥ v1.22 (open source)
- __Programming language__: Modelica 3.5
- __Availability__: https://github.com/IWHR-CHS/HydroComponents
- __License__: MIT (applies to HydroComponents source code; runtime compilation requires a Modelica compiler—OpenModelica recommended, GPL-3.0; Modelica Standard Library 4.0.0 dependency is BSD-3-Clause)
- __Archived release__: Zenodo DOI: 10.5281/zenodo.XXXXXXX (v1.0)
- __Cost__: Free
- __Size__: ~8,500 lines of Modelica code
- __Test suite__: 33 automated tests (28 unit + 5 integration), 87% line coverage
- __Documentation__: README, API reference, 3 tutorial notebooks
- __Docker__: `iwhr-chs/hydrocomponents:v1.0` for exact reproducibility
- __FAIR compliance__: Findable (Zenodo DOI), Accessible (MIT license, GitHub), Interoperable (FMI 2.0, Modelica Standard Library 4.0.0), Reusable (Docker environment, 33 automated tests, API documentation)

__References__

Blochwitz, T., Otter, M., Akesson, J., et al. (2012). Functional Mockup Interface 2.0: The standard for tool independent exchange of simulation models. In Proceedings of the 9th International Modelica Conference (pp. 173–184).

Brunner, G. W. (2016). HEC-RAS River Analysis System: Hydraulic reference manual. US Army Corps of Engineers.

Buyalski, C. P. (1983). Discharge algorithms for canal radial gates. Technical Report REC-ERC-83-9, US Bureau of Reclamation.

Capart, H., & Zech, Y. (2002). The void fraction structure of highly aerated open-channel flow and its role in dam-break flow modelling. In River Flow 2002 (pp. 675–684). Balkema.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026). Model-based definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

DHI. (2024). MIKE 1D Reference Manual. Danish Hydraulic Institute.

Elmqvist, H., Mattsson, S. E., & Otter, M. (2003). Object-oriented and hybrid modeling in Modelica. Journal Européen des Systèmes Automatisés, 37(3), 395–404.

Fritzson, P. (2014). Principles of object-oriented modeling and simulation with Modelica 3.3 (2nd ed.). Wiley-IEEE Press.

Henry, H. R. (1950). Discussion of "Diffusion of submerged jets" by M. L. Albertson et al. Transactions of the American Society of Civil Engineers, 115, 687–694.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Liu, X., Lei, X., Long, Y., & Wang, H. (2026). Design for Operation: A model-based framework for establishing cybernetics of hydro systems as an interdisciplinary discipline. Environmental Modelling & Software (submitted).

Malaterre, P.-O., & Baume, J.-P. (2011). SIC and SIC²: Modelling tools for canal regulation. In Proceedings of the International Workshop on Numerical Modelling of Hydrodynamics for Water Resources (pp. 1–12).

Malaterre, P.-O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Rossman, L. A. (2015). Storm Water Management Model User's Manual Version 5.1. US EPA.

Schuurmans, J. (1997). Control of water levels in open-channels. PhD thesis, Delft University of Technology.

Schweiger, G., Gomes, C., Engel, G., et al. (2019). An empirical survey on co-simulation: Promising standards, challenges and research needs. Simulation Modelling Practice and Theory, 95, 148–163.

Su, C., Lei, X., Bai, Y., Yin, B., Ji, C., & Wang, H. (2026). Experimental validation of the unified transfer function family and distributed MPC on a multi-pool canal flume. Journal of Irrigation and Drainage Engineering (submitted).

Klise, K. A., Bynum, M., Moriarty, D., & Murray, R. (2017). A software framework for assessing the resilience of drinking water systems to disasters with an example earthquake case study. Environmental Modelling & Software, 95, 420–431.

Pedersen, A. N., Borup, M., Brink-Kjær, A., Christiansen, L. E., & Mikkelsen, P. S. (2021). Living and prototyping digital twins for urban water systems: Towards multi-purpose value creation using models and sensors. Water, 13(5), 592.

Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. Journal of Computational Physics, 378, 686–707.

Ramos, H. M., McNabola, A., López-Jiménez, P. A., & Pérez-Sánchez, M. (2022). Smart water management towards future water sustainable networks. Water, 12(1), 58.

Swamee, P. K. (1992). Sluice-gate discharge equations. Journal of Irrigation and Drainage Engineering, 118(1), 56–60.

Willard, J., Jia, X., Xu, S., Steinbach, M., & Kumar, V. (2022). Integrating scientific knowledge with machine learning for engineering and environmental systems. ACM Computing Surveys, 55(4), 1–37.

__Figure Captions__

__Figure 1.__ HydroComponents library architecture. Left: the six CHS element packages with component counts. Center: the HydroPort and SignalPort connector hierarchy, showing the simplification relative to Modelica.Fluid connectors. Right: an example system assembly showing how Plant, Actuator, Sensor, and Controller components connect.

__Figure 2.__ Multi-fidelity implementation. (a) The same three-pool canal system assembled at LSV fidelity (60 state variables) and IDZ fidelity (6 state variables). (b) Fidelity switching: changing one parameter per component switches the entire system between fidelity levels. (c) FMI export: the assembled system is exported as a single FMU for co-simulation.

__Figure 3.__ Validation results. (a) Dual-tank step response: HydroComponents IDZ model (solid) vs. Chen et al. (2026) reference (dashed). (b) Three-pool flume DMPC: HydroComponents MiL (solid) vs. Su et al. (2026) experimental data (dots). (c) Field-scale canal: HydroComponents LSV (solid), HEC-RAS 6.3 (dashed), and field measurement (dots) for a 6-hour gate operation event (Pool 1 radial gate, +0.3 m opening over 10 min).

__Figure 4.__ MBD pipeline integration. The complete workflow: (1) assemble system in OpenModelica using HydroComponents → (2) export as FMU → (3) import into Simulink for MPC design → (4) MiL verification (LSV FMU as truth model, IDZ FMU as prediction model) → (5) SiL with auto-generated code → (6) HiL on physical hardware.
