*Manuscript submitted to Environmental Modelling & Software*

__Design for Operation: A Model\-Based Framework for Establishing__

__Cybernetics of Hydro Systems as an Interdisciplinary Discipline__

__Xiaowei Liu__1, __Xiaohui Lei__1,2\*, __Yan Long__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research \(IWHR\), Beijing 100038, China

\*Corresponding author: Xiaohui Lei \(lxh@iwhr\.com\)

__Highlights__

\- Introduces Design for Operation \(DfO\) as a paradigm shift from construction\-centric to operation\-centric water engineering

\- Proposes a seven\-layer Model\-Based Definition \(MBD\) framework spanning physical models to deployment verification

\- Presents a curriculum structure for Cybernetics of Hydro Systems bridging water engineering, control theory, and software engineering

\- Maps existing open\-source and commercial software tools to MBD layers, identifying critical gaps

__Abstract__

Water infrastructure design has historically prioritized structural safety and hydraulic capacity—a construction\-centric paradigm we term Design for Construction \(DfC\)\. Yet the operational phase, spanning decades of real\-time control, maintenance, and adaptation, receives comparatively little systematic attention during the design process\. The emerging discipline of Cybernetics of Hydro Systems \(CHS\) provides a unified theoretical framework for water network operations, but its translation into engineering practice, software tools, and educational programs requires a structured disciplinary foundation\. This paper proposes Design for Operation \(DfO\) as a complementary paradigm that integrates operational intelligence into every stage of the water infrastructure lifecycle—from conceptual design through modeling, verification, deployment, and continuous improvement\. We formalize DfO through a seven\-layer Model\-Based Definition \(MBD\) framework that structures the progression from physical\-law models \(Layer 7: Saint\-Venant equations\) through progressively simplified control models \(Layer 6: Integrator\-Delay\-Zero\), to system architecture \(Layer 5: agent hierarchy\), safety certification \(Layer 4: Operational Design Domain\), software implementation \(Layer 3: embedded control code\), hardware integration \(Layer 2: PLC/SCADA interfaces\), and operational deployment \(Layer 1: X\-in\-the\-Loop verification\)\. Each MBD layer is mapped to existing software tools—OpenModelica, MATLAB/Simulink, EPANET, Python control libraries, PLC programming environments, and SCADA platforms—identifying both available capabilities and critical toolchain gaps\. We then present a curriculum structure for CHS as an interdisciplinary graduate program, organized around the MBD layers with laboratory courses anchored to the tool chain\. The framework is illustrated through a reference workflow for the design\-to\-deployment pipeline of an autonomous canal control system, demonstrating how DfO and MBD connect the theoretical foundations of CHS to implementable engineering practice\. The paper concludes with a software availability assessment and a research agenda for the missing toolchain components\.

__Keywords: __Design for Operation; model\-based definition; water systems control; cybernetics of hydro systems; software engineering; curriculum design; X\-in\-the\-Loop

__Software Availability__

__Name of software__: CHS\-MBD Toolchain Reference Implementation

__Developer__: China Institute of Water Resources and Hydropower Research \(IWHR\) and Hebei University of Engineering

__Contact__: lxh@iwhr\.com

__Year first available__: 2025

__Hardware required__: Standard workstation; PLC hardware for Layers 2–1

__Software required__: OpenModelica \(≥1\.21\), MATLAB/Simulink \(R2023b\+\), Python 3\.10\+, CODESYS \(PLC\)

__Program language__: Modelica, MATLAB, Python, Structured Text \(IEC 61131\-3\)

__Program size__: ~50 MB \(excluding third\-party dependencies\)

__Availability__: Component libraries and reference workflows available at \[repository URL to be provided upon acceptance\]

__1  Introduction__

The lifecycle of water conveyance infrastructure—canals, pipelines, reservoirs, pump stations, and associated control structures—spans three phases: design, construction, and operation\. The design phase receives the most concentrated intellectual investment: teams of engineers spend years optimizing structural dimensions, hydraulic capacity, and material specifications\. The construction phase translates these designs into physical reality over a period of years to decades\. The operational phase, however, extends for decades to centuries and is where the infrastructure's societal value is actually delivered—yet it receives the least systematic attention during the design process\.

This asymmetry reflects what we term the Design for Construction \(DfC\) paradigm: the dominant engineering philosophy treats the design challenge as complete once the infrastructure is built to specification\. Operational intelligence—how the system should be controlled in real time, how it should respond to disturbances, how it should degrade gracefully under failure—is addressed ad hoc during the operational phase, typically through experience\-based rules and manual SCADA \(Supervisory Control and Data Acquisition\) operation \(Savic, 2022\)\. The DfC paradigm has deep historical roots: when water infrastructure was simpler and hydrological conditions more stationary, experience\-based operation was adequate\. Two developments have undermined this adequacy\. First, climate non\-stationarity has shifted hydrological regimes beyond historical envelopes, rendering experience\-based rules increasingly unreliable \(Milly et al\., 2008\)\. Second, the complexity and interconnection of modern water networks—multi\-source systems, inter\-basin transfers, coupled urban\-rural supply chains—have exceeded the cognitive capacity of manual operation\.

The emerging discipline of Cybernetics of Hydro Systems \(CHS\) provides a unified theoretical foundation for water network operations \(Lei, 2025a\)\. CHS establishes that all water conveyance and distribution systems share a structurally isomorphic six\-element control architecture, can be described by two unified transfer function families, and are governed by eight principles organized in dual tetrads\. Companion papers have developed the Multi\-Agent System \(MAS\) architecture and Water Systems Autonomy Levels \(WSAL\) classification \(Lei et al\., 2025b\), the disciplinary heritage perspective \(Lei et al\., 2025c\), and the X\-in\-the\-Loop \(xIL\) verification framework \(Lei et al\., 2025d\)\. However, a critical gap remains between these theoretical and architectural contributions and their translation into engineering practice\. Specifically, the CHS literature does not address: \(1\) how operational intelligence should be integrated into the design process from the earliest stages; \(2\) what software tool chain supports the progression from physical models to deployed controllers; and \(3\) how the next generation of water engineers should be trained in this interdisciplinary synthesis\.

This paper addresses these three gaps through three contributions\. First, we introduce Design for Operation \(DfO\) as a paradigm that complements DfC by integrating operational intelligence into the water infrastructure lifecycle\. DfO is not a replacement for structural design but a systematic extension: every design decision is evaluated not only for construction feasibility but also for operational controllability, certifiability, and maintainability\. Second, we formalize a seven\-layer Model\-Based Definition \(MBD\) framework that structures the progression from physics to deployment, mapping each layer to available software tools and identifying critical gaps\. Third, we propose a curriculum structure for CHS as an interdisciplinary graduate program, organized around the MBD layers\.

The remainder of the paper is structured as follows\. Section 2 contrasts DfC and DfO through historical analysis and cross\-sector comparison\. Section 3 presents the seven\-layer MBD framework\. Section 4 maps the software tool chain to MBD layers\. Section 5 describes the curriculum structure\. Section 6 presents a reference workflow illustration\. Section 7 discusses implications and limitations\. Section 8 concludes\.

__*\[Figure 1 about here\]*__

__2  From Design for Construction to Design for Operation__

__2\.1  The DfC Paradigm: Historical Roots__

The construction\-centric paradigm in water engineering emerged from the grand infrastructure era of the 20th century, when the primary challenge was building the physical infrastructure itself\. Dams, canals, and aqueducts were designed for structural safety \(static and dynamic loads, seismic resistance, material durability\) and hydraulic capacity \(maximum flow, flood routing, storage volume\)\. The operational phase was implicitly assumed to be straightforward: open the gates to deliver water, close them to stop\. The engineering challenge was in the concrete and steel, not in the control logic\.

This paradigm produced remarkable infrastructure—the Hoover Dam, the California Aqueduct, the South\-to\-North Water Transfer in China—but it also produced infrastructure that is difficult to operate optimally\. Three systemic consequences of DfC are evident\. First, actuator placement is optimized for construction convenience rather than observability and controllability: gates are placed where structures are needed, not where control authority is maximized\. Second, sensor instrumentation is added after construction as a monitoring afterthought rather than integrated into the design as a control system requirement\. Third, the control design space—the range of feasible operating strategies—is constrained by physical dimensions that were fixed during design without considering their control implications\.

__2\.2  The DfO Paradigm: Principles__

Design for Operation \(DfO\) extends the design objective function to include operational performance alongside structural safety and hydraulic capacity\. Formally, we define:

__*Definition 1 \(Design for Operation\)\. *__DfO is a design paradigm in which every physical design decision \(structure dimensions, actuator placement, sensor locations, communication infrastructure\) is evaluated against an operational performance criterion: the achievable closed\-loop control performance \(stability, disturbance rejection, constraint satisfaction\) of the resulting system under the target Operational Design Domain \(ODD\)\.

DfO is governed by five principles\. \(P1\) Controllability by Design: actuator placement and sizing are co\-optimized with the control algorithm, not determined independently\. \(P2\) Observability by Design: sensor locations are selected to maximize the observability of state variables critical for control, not merely for monitoring\. \(P3\) ODD\-Aware Design: the physical design defines and constrains the achievable ODD; DfO ensures that the target ODD is achievable given the physical design, or modifies the design to expand the ODD\. \(P4\) Verifiability by Design: the design includes provisions for xIL verification—test points, simulation interfaces, redundant sensors—that enable progressive validation from MiL through PiL\. \(P5\) Maintainability by Design: the system architecture supports online reconfiguration, software updates, and actuator replacement without full system shutdown\.

__2\.3  Cross\-Sector Precedents__

The DfO concept is not new in other engineering domains\. In aerospace, "Design for Manufacturability" \(DfM\) and "Design for Testability" \(DfT\) are established practices that integrate downstream lifecycle concerns into the design process \(Boothroyd et al\., 2011\)\. The automotive industry's adoption of model\-based design \(MBD\) through ISO 26262 requires that safety\-critical control software be developed from verified models, with the design\-to\-deployment pipeline structured through progressive verification stages \(ISO, 2018\)\. The power systems sector has long integrated operational optimization into the design of generation dispatch and transmission systems \(Kundur, 1994\)\. The semiconductor industry uses "Design for Test" \(DfT\) to ensure that manufactured chips can be verified against their specifications\.

The water sector stands out as one of the few critical infrastructure domains where the design\-operation integration remains ad hoc\. The reasons are partly historical \(water infrastructure predates modern control theory\), partly institutional \(design and operation are managed by different organizations\), and partly technical \(the distributed, gravity\-driven nature of water systems makes them harder to instrument and control than electrical or mechanical systems\)\. DfO aims to close this gap\.

__3  The Seven\-Layer Model\-Based Definition Framework__

__3\.1  Overview__

Model\-Based Definition \(MBD\) is a structured approach to engineering that uses models as the authoritative source of information throughout the product lifecycle\. In manufacturing, MBD replaces 2D drawings with annotated 3D models \(ASME Y14\.41\); in automotive, MBD encompasses model\-based design, model\-based testing, and model\-based calibration\. We adapt MBD to water systems control through a seven\-layer framework that structures the progression from physical\-law models to operational deployment\.

The seven layers are organized in descending order of physical fidelity and ascending order of implementation specificity:

__*Table 1\. The Seven\-Layer MBD Framework for Water Systems Control*__

| Layer | Name | Content | Model Type | Tool Examples |
|-------|------|---------|------------|---------------|
| 7 | Physical Model | Full Saint\-Venant / pipe transient equations | PDE | OpenModelica, HEC\-RAS, MIKE 11 |
| 6 | Control Model | IDZ/ID transfer functions, MPC internal models | ODE/TF | MATLAB/Simulink, Python Control |
| 5 | Architecture | MAS agent hierarchy, HDC layer allocation, communication protocols | System spec | UML/SysML, custom tools |
| 4 | Safety Certification | ODD definition, xIL test specifications, WSAL criteria | Verification spec | Test management, simulation |
| 3 | Software | Embedded control code, SCADA integration, HMI | Source code | CODESYS, C/C\+\+, IEC 61131\-3 |
| 2 | Hardware | PLC configuration, I/O mapping, network topology | Hardware spec | PLC IDEs, network tools |
| 1 | Deployment | xIL verification execution, shadow mode, commissioning | Operational | Field instruments, SCADA |

__*\[Figure 2 about here\]*__

__3\.2  Layer 7: Physical Model__

The physical model layer captures the governing equations of the water system with full fidelity\. For open\-channel systems, this is the one\-dimensional Saint\-Venant equations—conservation of mass and momentum—discretized spatially and solved numerically\. For pressurized pipe systems, this is the water hammer equations \(elastic wave propagation\)\. For reservoir systems, this is the mass balance equation with storage\-discharge relationships\.

The physical model serves two purposes in MBD\. First, it provides the reference\-fidelity simulation against which all simplified models \(Layer 6\) are validated\. Second, it serves as the "plant model" in xIL verification: when the controller \(Layers 3–2\) is tested in Model\-in\-the\-Loop or Software\-in\-the\-Loop, the physical model represents the real system\.

Key requirements: the physical model must be parameterizable from survey and design data \(channel geometry, pipe properties, boundary conditions\) and must execute faster than real time for xIL testing\. Software tools at this layer include OpenModelica for component\-based modeling \(Fritzson, 2014\), HEC\-RAS for one\-dimensional unsteady flow simulation \(US Army Corps, 2023\), and commercial platforms such as MIKE 11 \(DHI\) and InfoWorks \(Innovyze\)\.

__3\.3  Layer 6: Control Model__

The control model layer derives simplified representations suitable for real\-time controller design\. CHS theory provides the theoretical basis for this simplification through the Unified Transfer Function Family \(Lei, 2025a, Theorem 2\): all water conveyance systems belong to either Family α \(integrating/non\-self\-regulating: $G(s) = (1+\tau_m s) e^{-\tau_d s} / (A_s \cdot s)$\) or Family β \(self\-regulating: $H(s) = (1-KXs) / (1+K(1-X)s)$\), and the five\-level model hierarchy \(LSV→IDZ→ID→I→SS\) provides a principled reduction pathway from full PDE to steady\-state\.

The Layer 7→6 transition involves three steps: \(1\) linearization around an operating point; \(2\) spatial discretization to obtain the IDZ or ID transfer function for each pool or pipe segment; \(3\) state\-space realization through Padé approximation and discretization\. The resulting models are used directly as internal models for MPC controllers at HDC Layers 1 and 2\.

Key requirements: the control model must be validated against the physical model \(Layer 7\) across the entire target ODD\. The validation criterion is that the closed\-loop performance \(water level tracking error, constraint satisfaction\) using the control model as the MPC internal model, with the physical model as the simulated plant, meets the WSAL\-2 admission criteria\. Software tools include MATLAB/Simulink for model\-based control design, the Python Control Systems Library \(python\-control\), and Modelica\-based linearization tools\.

__3\.4  Layer 5: Architecture__

The architecture layer specifies the MAS system design: how many agents, where they are deployed, what HDC layers each agent runs, how they communicate, and what happens when communication fails\. This layer translates the abstract MAS = HDC \+ ODD \+ CI architecture \(Lei et al\., 2025b\) into a site\-specific engineering design\.

Key design decisions at Layer 5 include: \(a\) agent\-to\-structure mapping \(which physical structures are controlled by each Edge Agent\); \(b\) area delineation \(how structures are grouped into Area Agent jurisdictions\); \(c\) communication topology and protocol selection \(heartbeat intervals, redundancy, failover\); \(d\) island\-autonomy specifications \(what reference trajectories and constraint sets each agent stores locally for communication\-loss scenarios\)\. These decisions are informed by the control model \(Layer 6\)—for example, the DMPC coupling structure determines which agents must communicate—and constrain the software and hardware design \(Layers 3–2\)\.

Software tools for Layer 5 are currently the weakest link in the MBD chain\. System architecture specification typically relies on informal documents, UML/SysML diagrams, or custom spreadsheets\. A critical tool gap is the absence of a formal, machine\-readable architecture description language for water control systems—analogous to AADL \(Architecture Analysis and Description Language\) in aerospace or AUTOSAR in automotive\. Developing such a language is a priority for the CHS research agenda\.

__3\.5  Layer 4: Safety Certification__

The safety certification layer formalizes the ODD, specifies the xIL test plan, and defines the WSAL admission criteria for the specific system\. This layer bridges the architecture \(Layer 5\) and the software implementation \(Layer 3\) by establishing what must be verified before the system can operate at each WSAL level\.

Key deliverables at Layer 4 include: \(a\) the formal ODD specification as a Cartesian product of bounded operating dimensions \(Lei et al\., 2025b, Definition 1\); \(b\) the xIL test matrix mapping ODD scenarios to verification stages \(MiL, SiL, HiL, PiL\); \(c\) the acceptance criteria for each test \(constraint satisfaction, performance thresholds, failure\-mode responses\); \(d\) the Minimum Risk Condition \(MRC\) procedure specification\.

Software tools at this layer are borrowed from other safety\-critical domains: test management systems \(e\.g\., IBM DOORS for requirements tracing\), simulation orchestration tools for automated xIL test execution, and formal verification tools for Layer 0 safety logic \(e\.g\., model checking\)\. The water\-specific gap is the absence of standardized ODD description formats and xIL test protocols\.

__3\.6  Layer 3: Software Implementation__

The software layer translates the control model \(Layer 6\) and architecture \(Layer 5\) into executable code that runs on field controllers\. This is the critical transition from "model" to "code"—and the point where most water\-sector automation projects fail, because the ad hoc translation from research prototype to production software introduces bugs, timing errors, and integration failures\.

MBD addresses this through automatic code generation: the control model designed in MATLAB/Simulink or Modelica is automatically translated into C code or Structured Text \(IEC 61131\-3\) for execution on PLCs or industrial PCs\. Automatic code generation eliminates the manual translation step, ensuring that the deployed controller is mathematically identical to the verified model\. The Simulink Coder, Simulink PLC Coder, and OpenModelica code generation capabilities support this workflow\.

Key requirements at Layer 3 include: \(a\) compliance with IEC 61131\-3 for PLC software; \(b\) real\-time execution guarantees \(the control computation must complete within the sampling interval\); \(c\) SCADA integration through standard protocols \(OPC\-UA, Modbus TCP/IP\); \(d\) cybersecurity compliance per IEC 62443\.

__3\.7  Layers 2–1: Hardware and Deployment__

Layer 2 specifies the hardware platform: PLC models, industrial PC specifications, I/O card configurations, network switches, and communication link specifications\. Layer 1 encompasses the xIL verification execution \(MiL → SiL → HiL → PiL\), shadow\-mode operation, and operational commissioning\.

These layers are inherently site\-specific and involve physical engineering rather than software development\. The MBD contribution is to ensure traceability: every hardware decision \(Layer 2\) can be traced to a requirement from the architecture \(Layer 5\) and safety certification \(Layer 4\), and every deployment test \(Layer 1\) can be traced to a scenario in the xIL test matrix \(Layer 4\)\.

__4  Software Tool Chain Assessment__

__4\.1  Layer\-by\-Layer Mapping__

Table 2 presents a detailed assessment of available software tools for each MBD layer, including maturity level, licensing, and critical gaps\.

__*Table 2\. Software Tool Chain Assessment by MBD Layer*__

| Layer | Tool | License | Maturity | Water\-Specific | Gap |
|-------|------|---------|----------|----------------|-----|
| 7 | OpenModelica | Open\-source \(OSMC\) | High | Low | Water component library needed |
| 7 | HEC\-RAS | Free \(USACE\) | High | High | Limited API for xIL coupling |
| 7 | EPANET | Open\-source \(EPA\) | High | High | Steady\-state only; no transient |
| 7 | MIKE 11 | Commercial \(DHI\) | High | High | Closed\-source; cost barrier |
| 6 | MATLAB/Simulink | Commercial \(MW\) | High | Medium | License cost; academic bias |
| 6 | python\-control | Open\-source | Medium | Low | No MPC built\-in |
| 6 | do\-mpc | Open\-source | Medium | Low | Promising; needs water examples |
| 5 | SysML/UML | Open standards | High | None | No water\-specific profiles |
| 4 | IBM DOORS | Commercial | High | None | Expensive; enterprise\-only |
| 4 | Custom scripts | — | Low | Varies | No standardization |
| 3 | CODESYS | Commercial \(free RT\) | High | None | Generic; water templates needed |
| 3 | Simulink Coder | Commercial \(MW\) | High | None | License cost |
| 2 | PLC IDEs | Vendor\-specific | High | None | Fragmented; interoperability |
| 1 | SCADA platforms | Commercial | High | High | Proprietary; limited open API |

__4\.2  Critical Toolchain Gaps__

Three critical gaps emerge from the assessment\. Gap T1 \(Physical Model Componentization\): open\-source hydraulic models \(HEC\-RAS, EPANET\) are monolithic applications designed for standalone simulation, not component libraries that can be coupled with control tools via standard interfaces \(e\.g\., Functional Mock\-up Interface, FMI\)\. Developing an open\-source water systems component library in Modelica that exports FMU \(Functional Mock\-up Units\) is a priority that would enable seamless Layer 7↔Layer 6 coupling\. Gap T2 \(Architecture Description Language\): no formal, machine\-readable specification language exists for water control system architectures\. This prevents automated consistency checking between the architecture \(Layer 5\) and the software implementation \(Layer 3\)\. Gap T3 \(ODD Specification Format\): the ODD definition \(Layer 4\) is currently expressed in natural language or ad hoc formats\. A standardized, machine\-readable ODD schema—analogous to OpenSCENARIO in automotive—would enable automated xIL test generation and cross\-system ODD comparison\.

__4\.3  The FMI Integration Pathway__

The Functional Mock\-up Interface \(FMI\) standard \(Blochwitz et al\., 2012\) provides a promising pathway for tool integration across MBD layers\. FMI defines a standard interface for exchanging simulation models between tools as Functional Mock\-up Units \(FMUs\)\. In the MBD context: the physical model \(Layer 7\) is exported as an FMU from OpenModelica; the control model \(Layer 6\) runs in Simulink and communicates with the physical model FMU via co\-simulation; the embedded code \(Layer 3\) is generated from Simulink and tested against the physical model FMU in SiL\. This FMI\-mediated workflow enables the tool\-agnostic MBD pipeline that DfO requires\.

The CHS\-MBD toolchain reference implementation provides basic FMI coupling between OpenModelica water component models and Simulink MPC controllers, demonstrating the feasibility of this approach for a single\-pool canal control scenario\. Scaling to multi\-agent systems with realistic complexity is an active area of development\.

__5  Curriculum Structure for CHS__

__5\.1  The Interdisciplinary Challenge__

CHS sits at the intersection of three established disciplines: water engineering \(hydraulics, hydrology, water resources planning\), control engineering \(feedback control, MPC, distributed systems\), and software engineering \(embedded systems, real\-time computing, cybersecurity\)\. No existing curriculum covers this intersection comprehensively\. Water engineering programs typically include one elective course in "computer applications" that covers hydrological modeling but not real\-time control\. Control engineering programs use water systems as textbook examples but lack domain knowledge of hydraulic phenomena and operational constraints\. Software engineering programs address embedded systems generically but have no exposure to the physical\-law constraints that govern water system behavior\.

__5\.2  Proposed Curriculum Structure__

We propose a two\-year graduate curriculum organized around the MBD layers, with each semester progressively ascending from physical fundamentals to operational deployment\.

__*Table 3\. Proposed CHS Graduate Curriculum*__

| Semester | Core Courses | MBD Focus | Lab Component |
|----------|-------------|-----------|---------------|
| 1 | Hydraulics of Open\-Channel and Pipe Systems; Applied Mathematics for Control | L7: Physical models | OpenModelica: Build canal model |
| 1 | Introduction to CHS: Theory and Principles | L7–L6: Model hierarchy | Replicate P1a five\-level derivation |
| 2 | Model\-Based Control of Water Systems | L6–L5: Control design + architecture | Simulink MPC for single pool |
| 2 | Safety Certification and ODD | L5–L4: Architecture + verification | Define ODD, write xIL test plan |
| 3 | Embedded Systems for Water Control | L3–L2: Software + hardware | PLC programming; CODESYS lab |
| 3 | Multi\-Agent Systems for Water Networks | L5–L3: DMPC + agents | Multi\-pool DMPC in Simulink |
| 4 | Capstone: Design\-to\-Deployment Project | L7–L1: Full MBD pipeline | Team project: canal xIL |
| 4 | CHS Research Seminar | Cross\-cutting | Literature review; paper writing |

__5\.3  Laboratory Infrastructure__

The curriculum requires four types of laboratory infrastructure, aligned with the MBD layers\.

\(a\) Simulation Laboratory \(Layers 7–6\): workstations running OpenModelica, MATLAB/Simulink, and Python, with access to calibrated hydraulic models of reference water systems \(a canal reach, a reservoir cascade, a pipe network\)\.

\(b\) Control Design Laboratory \(Layers 6–5\): Simulink with MPC Toolbox; multi\-agent simulation environments; communication protocol emulators for agent\-to\-agent testing\.

\(c\) Embedded Systems Laboratory \(Layers 3–2\): PLC workbenches \(CODESYS\-compatible\); real\-time targets \(Simulink Real\-Time, dSPACE\); SCADA demonstration platform with OPC\-UA connectivity\.

\(d\) Physical Test Facility \(Layers 2–1\): a laboratory\-scale hydraulic test bench—a multi\-pool canal flume with motorized gates and real\-time water level sensors—providing the physical plant for Hardware\-in\-the\-Loop and Plant\-in\-the\-Loop verification\. This facility bridges the model\-based curriculum with physical reality, enabling students to experience the model\-plant gap firsthand\.

The physical test facility is the most capital\-intensive component and is not yet widely available\. However, multi\-pool canal flumes with automated gates exist at several research institutions \(Delft University of Technology, IRSTEA/INRAE France, University of Melbourne, IWHR China\), and the standardization of flume designs for CHS education is a priority for international collaboration\.

__6  Reference Workflow: Canal Control Design\-to\-Deployment__

__6\.1  Problem Setup__

To illustrate the MBD framework, we trace a reference workflow for designing, verifying, and deploying an autonomous control system for a three\-pool irrigation canal\. The canal has the following parameters: pool lengths L₁ = L₂ = L₃ = 2,000 m; trapezoidal cross\-section with bottom width b = 3 m, side slope m = 1\.5; design flow Q₀ = 5 m³/s; downstream control gates at each pool boundary; water level sensors at downstream ends\.

__6\.2  Layer 7: Physical Model__

An OpenModelica model is constructed using a component library: three CanalPool components connected by three ControlGate components, with upstream inflow as boundary condition\. Each pool is discretized using a staggered\-grid finite\-difference scheme solving the Saint\-Venant equations\. The model is validated against analytical solutions for uniform flow and measured data for unsteady gate operations\.

__6\.3  Layer 6: Control Model__

The IDZ transfer function parameters are identified from the physical model through step\-response analysis: for each pool, the storage area A\_s, delay τ\_d, and backwater time constant τ\_m are extracted\. The five\-level model hierarchy \(LSV→IDZ→ID→I→SS\) is computed, and the IDZ model is validated by comparing its step response against the Saint\-Venant model across the normal\-flow ODD \(Q ∈ \[2, 8\] m³/s\)\.

An MPC controller is designed in MATLAB/Simulink using the IDZ state\-space model as internal model: prediction horizon N = 20 steps at Δt = 60 s; control weights α\_y = 1, α\_u = 0\.1; water level constraints h\_min = 0\.8 m, h\_max = 1\.5 m; gate rate constraint |Δu| ≤ 0\.02 m/step\.

__6\.4  Layers 5–4: Architecture and Certification__

The MAS architecture assigns one Edge Agent per gate \(3 agents\), one Area Agent for the canal reach, and one Cloud Agent for planning\. The DMPC coordination protocol is specified: sequential upstream\-to\-downstream iteration with 3 DMPC iterations per control step\. The ODD is defined: S\_flow = \[2, 8\] m³/s, S\_level = \[0\.7, 1\.6\] m, S\_equip = all gates functional, S\_comm = heartbeat interval ≤ 60 s\. The MiL test matrix specifies 12 scenarios: 4 flow conditions × 3 disturbance types \(step change, ramp, offtake\)\.

__6\.5  Layers 3–1: Software, Hardware, Deployment__

The MPC controller is automatically translated from Simulink to IEC 61131\-3 Structured Text using Simulink PLC Coder\. The generated code is loaded onto CODESYS\-compatible PLCs\. Communication uses Modbus TCP/IP for gate\-to\-Edge Agent and OPC\-UA for Edge\-to\-Area Agent\. Layer 0 safety interlocks are programmed in ladder logic on a separate safety PLC\.

MiL verification: the Simulink controller is connected to the OpenModelica plant model via FMI; all 12 scenarios are executed; water level tracking RMSE is verified to be below 0\.05 m for all scenarios within the ODD\. SiL verification: the PLC code \(from Simulink Coder\) is executed against the same OpenModelica plant model; timing and communication are validated\. HiL verification: the physical PLC is connected to a real\-time OpenModelica simulation running on a dSPACE target; communication failure and sensor noise scenarios are tested\. Shadow\-mode operation: the controller runs in parallel with manual operation on the physical canal flume, comparing MPC recommendations against operator decisions for one month\.

__*\[Figure 3 about here\]*__

__7  Discussion__

__7\.1  DfO as a Design Paradigm Shift__

DfO represents a shift in how water engineers think about infrastructure value\. Under DfC, value is created during construction—a well\-designed dam is a good dam\. Under DfO, value is created during operation—a well\-controlled dam is a good dam\. This shift has implications for procurement \(operational performance criteria in design contracts\), regulation \(operational certifiability as a design requirement\), and insurance \(automated control as a risk mitigation factor\)\. The DfO paradigm also reframes the economics of water infrastructure: the capital cost of embedding control intelligence during design is small relative to the operational savings over the infrastructure lifecycle\.

__7\.2  MBD and the V\-Model__

The seven\-layer MBD framework maps naturally onto the V\-model of systems engineering, where the left side of the V \(Layers 7→1 in design\) mirrors the right side \(Layers 1→7 in verification\)\. Layer 7 physical models are validated against field data \(top right\); Layer 6 control models are validated against Layer 7 simulations; Layer 3 software is verified against Layer 6 models \(SiL\); Layers 2–1 hardware and deployment are verified against Layer 7 through HiL and PiL\. This V\-model correspondence provides a natural quality assurance framework for CHS engineering projects\.

__7\.3  Curriculum Integration Challenges__

The proposed CHS curriculum faces practical challenges\. First, faculty expertise: few academics simultaneously possess deep knowledge of hydraulics, control theory, and embedded systems\. The curriculum may require team\-teaching across departments, which is institutionally difficult\. Second, laboratory cost: the physical test facility \(flume with automated gates\) requires significant capital investment\. Third, industry alignment: graduates of this program would need employment in a water automation sector that is still nascent\. The curriculum design must balance depth in CHS\-specific skills with breadth in transferable competencies \(MPC, embedded systems, SCADA\) that are valued across infrastructure sectors\.

__7\.4  Relationship to Existing Frameworks__

DfO and MBD are related to but distinct from several existing concepts\. Digital twins provide a real\-time simulation mirror of the physical system; MBD provides the structured modeling pipeline that creates both the digital twin \(Layer 7\) and the controller \(Layers 6–3\)\. Building Information Modeling \(BIM\) captures the physical design in a structured digital format; DfO extends BIM to include operational intelligence—control algorithms, ODD specifications, and xIL test results—as first\-class design deliverables\. Systems engineering \(SE\) provides a general framework for complex system development; CHS\-MBD specializes SE to the water domain with domain\-specific model hierarchies \(the five\-level family\) and verification concepts \(xIL, WSAL\)\.

__7\.5  Limitations__

Several limitations should be acknowledged\. First, the MBD framework is presented conceptually with one reference workflow \(three\-pool canal\); validation across diverse infrastructure types \(reservoirs, pipe networks, pump stations\) is ongoing\. Second, the software tool chain assessment reflects 2025 capabilities; rapid evolution in open\-source tools may alter the gap analysis\. Third, the curriculum has been designed but not yet implemented as a full program; pilot courses at Hebei University of Engineering are planned for 2026–2027\. Fourth, the DfO paradigm requires buy\-in from the water infrastructure community—design consultants, regulatory agencies, and utilities—which is an institutional rather than technical challenge\. Fifth, the reference implementation \(CHS\-MBD toolchain\) is at prototype stage; production\-quality tools require sustained community development\.

__8  Conclusions__

This paper has presented three contributions for establishing Cybernetics of Hydro Systems as an interdisciplinary discipline\.

First, Design for Operation \(DfO\) provides a paradigm shift from construction\-centric to operation\-centric water engineering\. DfO's five principles—controllability, observability, ODD\-awareness, verifiability, and maintainability by design—extend the design objective function to include operational performance as a first\-class criterion\. This paradigm shift has implications for procurement, regulation, education, and the economics of water infrastructure\.

Second, the seven\-layer Model\-Based Definition \(MBD\) framework structures the progression from physical\-law models \(Layer 7\) through control models, architecture, safety certification, software, hardware, to operational deployment \(Layer 1\)\. Each layer is mapped to available software tools, identifying three critical gaps: physical model componentization \(FMI\-compatible water libraries\), architecture description language, and standardized ODD specification format\. The FMI integration pathway is demonstrated through a reference implementation coupling OpenModelica physical models with Simulink MPC controllers\.

Third, a two\-year graduate curriculum organized around the MBD layers provides a concrete educational framework for training the next generation of water systems engineers in the interdisciplinary synthesis that CHS demands\. The curriculum spans hydraulics, control theory, embedded systems, and safety certification, with laboratory courses anchored to the software tool chain\.

The reference workflow—a three\-pool canal control system traced from physical model through MPC design, automatic code generation, and xIL verification—demonstrates that the DfO\-MBD framework is not merely conceptual but implementable with existing tools, albeit with gaps that require community development\. The CHS\-MBD toolchain reference implementation is offered as a starting point for this community effort\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\. The authors thank the members of the CHS working group at Hebei University of Engineering and IWHR for discussions that shaped the MBD framework and curriculum design\.

__References__

Blochwitz, T\., Otter, M\., Akesson, J\., Arnold, M\., Clauss, C\., Elmqvist, H\., Friedrich, M\., Junghanns, A\., Mauss, J\., Neumerkel, D\., Olsson, H\., & Viel, A\. \(2012\)\. Functional Mockup Interface 2\.0: The standard for tool independent exchange of simulation models\. In Proceedings of the 9th International Modelica Conference \(pp\. 173–184\)\. https://doi\.org/10\.3384/ecp12076173

Boothroyd, G\., Dewhurst, P\., & Knight, W\. A\. \(2011\)\. Product design for manufacture and assembly \(3rd ed\.\)\. CRC Press\.

Castelletti, A\., Ficchì, A\., Cominola, A\., Segovia, P\., Giuliani, M\., Wu, W\., Lucia, S\., Ocampo\-Martinez, C\., De Schutter, B\., & Maestre, J\. M\. \(2023\)\. Model Predictive Control of water resources systems: A review and research agenda\. Annual Reviews in Control, 55, 442–465\. https://doi\.org/10\.1016/j\.arcontrol\.2023\.03\.013

Fritzson, P\. \(2014\)\. Principles of object\-oriented modeling and simulation with Modelica 3\.3 \(2nd ed\.\)\. Wiley\-IEEE Press\.

IEC\. \(2018\)\. IEC 62443: Industrial communication networks—Network and system security\. International Electrotechnical Commission\.

ISO\. \(2018\)\. ISO 26262: Road vehicles—Functional safety\. International Organization for Standardization\.

Kundur, P\. \(1994\)\. Power system stability and control\. McGraw\-Hill\.

Lei, X\. \(2025a\)\. Cybernetics of hydro systems: A unified control\-theoretic framework for water network operations\. Water Resources Research \(submitted\)\.

Lei, X\., Liu, X\., Ji, C\., Wang, C\., & Wang, H\. \(2025b\)\. From SCADA to autonomy: A multi\-agent system architecture and water systems autonomy level classification\. Journal of Water Resources Planning and Management \(submitted\)\.

Lei, X\., Ji, C\., Wang, C\., & Wang, H\. \(2025c\)\. Cybernetics of hydro systems: Disciplinary foundations and engineering paradigms \[水系统控制论：学科基础与工程范式\]\. Science China: Technological Sciences \(submitted\)\.

Lei, X\., Zhang, Z\., Su, C\., et al\. \(2025d\)\. In\-the\-loop testing system for autonomous intelligent water networks\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 787–793\. https://doi\.org/10\.13476/j\.cnki\.nsbdqk\.2025\.0080

Lei, X\., Long, Y\., Xu, H\., et al\. \(2025e\)\. Cybernetics of hydro systems: Background, technical framework and research paradigm\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 761–769\. https://doi\.org/10\.13476/j\.cnki\.nsbdqk\.2025\.0077

Litrico, X\., & Fromion, V\. \(2009\)\. Modeling and control of hydrosystems\. Springer\. https://doi\.org/10\.1007/978\-1\-84882\-624\-3

Malaterre, P\.\-O\., Rogers, D\. C\., & Schuurmans, J\. \(1998\)\. Classification of canal control algorithms\. Journal of Irrigation and Drainage Engineering, 124\(1\), 3–10\. https://doi\.org/10\.1061/\(ASCE\)0733\-9437\(1998\)124:1\(3\)

Milly, P\. C\. D\., Betancourt, J\., Falkenmark, M\., Hirsch, R\. M\., Kundzewicz, Z\. W\., Lettenmaier, D\. P\., & Stouffer, R\. J\. \(2008\)\. Stationarity is dead: Whither water management? Science, 319\(5863\), 573–574\. https://doi\.org/10\.1126/science\.1151915

Savic, D\. \(2022\)\. Digital water developments and lessons learned from automation in the car and aircraft industries\. Engineering, 9\(2\), 35–41\. https://doi\.org/10\.1016/j\.eng\.2021\.05\.013

US Army Corps of Engineers\. \(2023\)\. HEC\-RAS River Analysis System: Hydraulic reference manual \(Version 6\.4\)\. Hydrologic Engineering Center\.

van Overloop, P\. J\. \(2006\)\. Model predictive control on open water systems \(Doctoral dissertation\)\. Delft University of Technology\.

__Figure Captions__

__Figure 1\. __Design for Operation \(DfO\) paradigm contrasted with Design for Construction \(DfC\)\. Left: DfC pipeline where operational intelligence is added post\-construction as an afterthought\. Right: DfO pipeline where operational performance criteria \(controllability, observability, ODD, verifiability, maintainability\) are integrated from conceptual design through deployment\. The DfO pipeline produces an infrastructure that is not merely built to specification but designed to be operated autonomously\.

__Figure 2\. __The seven\-layer Model\-Based Definition \(MBD\) framework for water systems control\. Layers 7–1 are shown in descending order of physical fidelity and ascending order of implementation specificity\. Left column: layer name and content\. Center: V\-model correspondence showing design \(left arm\) and verification \(right arm\)\. Right column: software tools mapped to each layer, with critical gaps highlighted in red\.

__Figure 3\. __Reference workflow: three\-pool canal control system traced through the seven MBD layers\. Top: physical model \(OpenModelica\) validated against analytical solution\. Middle: IDZ control model derivation and MPC design \(Simulink\)\. Bottom: automatic code generation \(Structured Text\), PLC deployment, and xIL verification sequence \(MiL → SiL → HiL → shadow mode\)\.
