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

Water infrastructure design has historically prioritized structural safety and hydraulic capacity—a construction\-centric paradigm we term Design for Construction \(DfC\)—while the operational phase spanning decades of real\-time control receives comparatively little systematic attention during design\. This paper proposes Design for Operation \(DfO\) as a complementary paradigm that integrates operational intelligence into every stage of the water infrastructure lifecycle\. We formalize DfO through five quantitative principles \(controllability, observability, ODD\-awareness, verifiability, maintainability\) and a seven\-layer Model\-Based Definition \(MBD\) framework that structures the progression from physical\-law models through control models, system architecture, safety certification, software, hardware, to deployment verification\. Each MBD layer is mapped to existing open\-source and commercial software tools, identifying three critical toolchain gaps \(physical model componentization, architecture description language, ODD specification format\) and an FMI\-mediated integration pathway\. A competency framework organized by MBD layers and Bloom's taxonomy levels provides a concrete educational foundation for Cybernetics of Hydro Systems \(CHS\) as an interdisciplinary graduate program\. The framework is validated through a reference workflow—a three\-pool canal control system traced from Saint\-Venant physical model through IDZ control model derivation, MPC design, and FMI co\-simulation—achieving water level RMSE of 0\.018 m \(mean\) with zero constraint violations across 12 ODD scenarios\. The open\-source reference implementation \(OpenModelica \+ Python/do\-mpc \+ FMI\) demonstrates that the DfO\-MBD pipeline is implementable without commercial dependencies for Layers 7–6\.

__Keywords: __Design for Operation; model\-based definition; water systems control; cybernetics of hydro systems; software engineering; curriculum design; X\-in\-the\-Loop

__Software Availability__

__Name of software__: CHS\-MBD Toolchain: Open\-Source Water Systems Component Library and MPC Reference Implementation

__Developer__: China Institute of Water Resources and Hydropower Research \(IWHR\) and Hebei University of Engineering

__Contact__: lxh@iwhr\.com

__Year first available__: 2025

__Hardware required__: Standard workstation \(8 GB RAM, multi\-core CPU\); CODESYS\-compatible PLC for Layers 2–1 \(optional\)

__Software required__: OpenModelica \(≥1\.21\), Python 3\.10\+ with numpy, scipy, python\-control, and do\-mpc packages

__Program language__: Modelica \(component library\), Python \(MPC controllers and FMI coupling scripts\)

__Program size__: ~15 MB \(excluding OpenModelica installation\)

__Availability__: The software consists of three components: \(1\) an OpenModelica component library \(CHS\.WaterComponents\) containing CanalPool, ControlGate, Reservoir, PumpStation, and Sensor models with FMI 2\.0 export capability; \(2\) Python\-based MPC controller templates using do\-mpc for single\-pool and multi\-pool DMPC control; \(3\) FMI co\-simulation coupling scripts connecting OpenModelica plant models with Python controllers\. The three\-pool canal reference workflow \(§6\) is included as a fully executable example\. Source code, documentation, and tutorial notebooks are available at https://github\.com/IWHR\-CHS/chs\-mbd\-toolchain \(to be made public upon acceptance; reviewer access available upon request\)\.

__1  Introduction__

The lifecycle of water conveyance infrastructure—canals, pipelines, reservoirs, pump stations, and associated control structures—spans three phases: design, construction, and operation\. The design phase receives the most concentrated intellectual investment: teams of engineers spend years optimizing structural dimensions, hydraulic capacity, and material specifications\. The construction phase translates these designs into physical reality over a period of years to decades\. The operational phase, however, extends for decades to centuries and is where the infrastructure's societal value is actually delivered—yet it receives the least systematic attention during the design process\.

This asymmetry reflects what we term the Design for Construction \(DfC\) paradigm: the dominant engineering philosophy treats the design challenge as complete once the infrastructure is built to specification\. Operational intelligence—how the system should be controlled in real time, how it should respond to disturbances, how it should degrade gracefully under failure—is addressed ad hoc during the operational phase, typically through experience\-based rules and manual SCADA \(Supervisory Control and Data Acquisition\) operation \(Savic, 2022\)\. The DfC paradigm has deep historical roots: when water infrastructure was simpler and hydrological conditions more stationary, experience\-based operation was adequate\. Two developments have undermined this adequacy\. First, climate non\-stationarity has shifted hydrological regimes beyond historical envelopes, rendering experience\-based rules increasingly unreliable \(Milly et al\., 2008\)\. Second, the complexity and interconnection of modern water networks—multi\-source systems, inter\-basin transfers, coupled urban\-rural supply chains—have exceeded the cognitive capacity of manual operation\. These challenges are not merely technical: UN Sustainable Development Goal 6 \(Clean Water and Sanitation\), particularly Target 6\.4 on water\-use efficiency, and the IPCC AR6 emphasis on climate\-adaptive infrastructure \(IPCC, 2022\) demand a systematic approach to operational intelligence that the DfC paradigm cannot provide\.

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

DfO is governed by five principles, each with a formal metric computable from the MBD model stack\.

__*Principle P1 \(Controllability by Design\)\. *__Actuator placement and sizing are co\-optimized with the control algorithm\. Metric: the controllability Gramian $W_c$ of the Layer 6 state\-space model is computed at each vertex of the discretized ODD \(corners of the Cartesian product $\mathcal{V}(ODD)$\), and the worst\-case minimum singular value must satisfy $\sigma_{min}(W_c) = \min_{p \in \mathcal{V}(ODD)} \sigma_{min}(W_c(p)) \geq \gamma_c$\. The threshold $\gamma_c$ is defined relative to the control objective: $\gamma_c = Q_{max}^2 / (N \cdot \Delta t)$ where $Q_{max}$ is the maximum required flow change and $N \cdot \Delta t$ is the MPC prediction horizon, representing the minimum energy needed to achieve the design control authority\. A design that places gates only at construction\-convenient locations may yield $\sigma_{min}(W_c) \approx 0$ for certain ODD vertices, indicating that some states are practically uncontrollable\.

__*Principle P2 \(Observability by Design\)\. *__Sensor locations are selected to maximize observability of state variables critical for control\. Metric: the condition number $\kappa(W_o)$ of the observability Gramian of the Layer 6 balanced realization, evaluated at worst\-case ODD vertex, must satisfy $\kappa(W_o) = \max_{p \in \mathcal{V}(ODD)} \kappa(W_o(p)) \leq \kappa_{max}$\. The balanced realization ensures scale\-independent conditioning\. Large condition numbers indicate that some states are poorly observable, leading to degraded controller performance\. Sensor placement optimization \(e\.g\., using greedy algorithms on the observability Gramian\) should be a standard design deliverable\.

__*Principle P3 \(ODD\-Aware Design\)\. *__The physical design defines and constrains the achievable ODD; DfO ensures that the target ODD is achievable given the physical design, or modifies the design to expand the ODD\. Metric: ODD coverage ratio $R_{ODD} = N_{pass} / N_{grid}$, where $N_{grid}$ is the number of test points in the discretized ODD and $N_{pass}$ is the number passing all acceptance criteria\. This discrete formulation avoids dimensional inconsistency across ODD dimensions with different units\. A DfO\-compliant design achieves $R_{ODD} \geq 0.95$\.

__*Principle P4 \(Verifiability by Design\)\. *__The design includes provisions for xIL verification—test points, simulation interfaces, redundant sensors—that enable progressive validation from MiL through PiL\. Metric: xIL test coverage $C_{xIL} = N_{verified} / N_{total}$ where $N_{total}$ is the number of ODD scenarios in the test matrix and $N_{verified}$ is the number passing all acceptance criteria\. WSAL\-3 certification requires $C_{xIL} \geq 0.95$\.

__*Principle P5 \(Maintainability by Design\)\. *__The system architecture supports online reconfiguration, software updates, and actuator replacement without full system shutdown\. Metric: mean time to software update $T_{update} \leq 4$ hours and system availability during update $A_{update} \geq 0.99$ \(achieved through redundant controllers and graceful degradation to island\-autonomy mode\)\.

__2\.3  Cross\-Sector Precedents__

The DfO concept is not new in other engineering domains\. In aerospace, "Design for Manufacturability" \(DfM\) and "Design for Testability" \(DfT\) are established practices that integrate downstream lifecycle concerns into the design process \(Boothroyd et al\., 2011\)\. The automotive industry's adoption of model\-based design \(MBD\) through ISO 26262 requires that safety\-critical control software be developed from verified models, with the design\-to\-deployment pipeline structured through progressive verification stages \(ISO, 2018\)\. The power systems sector has long integrated operational optimization into the design of generation dispatch and transmission systems \(Kundur, 1994\)\. The semiconductor industry uses "Design for Test" \(DfT\) to ensure that manufactured chips can be verified against their specifications\.

The water sector stands out as one of the few critical infrastructure domains where the design\-operation integration remains ad hoc\. The reasons are partly historical \(water infrastructure predates modern control theory\), partly institutional \(design and operation are managed by different organizations\), and partly technical \(the distributed, gravity\-driven nature of water systems makes them harder to instrument and control than electrical or mechanical systems\)\. DfO aims to close this gap\.

__3  The Seven\-Layer Model\-Based Definition Framework__

__3\.1  Overview__

Model\-Based Definition \(MBD\) is a structured approach to engineering that uses models as the authoritative source of information throughout the product lifecycle\. In manufacturing, MBD replaces 2D drawings with annotated 3D models \(ASME Y14\.41\); in automotive, MBD encompasses model\-based design, model\-based testing, and model\-based calibration\. We adapt MBD to water systems control through a seven\-layer framework that structures the progression from physical\-law models to operational deployment\.

The seven layers are organized in descending order of physical fidelity and ascending order of implementation specificity\. Layers 7 and 6 correspond directly to the CHS five\-level model hierarchy established in Lei \(2025a, §4\.6, Theorem 3: Model–Layer Correspondence\):

__*Table 0\. Correspondence between CHS Model Levels and MBD Layers 7–6*__

| CHS Model Level | MBD Layer | Content | Use Case |
|-----------------|-----------|---------|----------|
| LSV \(Saint\-Venant\) | Layer 7 | Full PDE; reference\-fidelity simulation | xIL plant model, digital twin core |
| IDZ \(Integrator\-Delay\-Zero\) | Layer 6 \(primary\) | Three\-parameter transfer function | MPC internal model for real\-time control |
| ID \(Integrator\-Delay\) | Layer 6 \(simplified\) | Two\-parameter model \(no non\-min\-phase zero\) | Preliminary design, analytical tuning |
| I \(Integrator\) | Layer 6 \(minimal\) | Single\-parameter model | Order\-of\-magnitude estimation |
| SS \(Steady\-State\) | Layer 6 \(static\) | Algebraic balance | Capacity planning; not for dynamic control |

The Layer 7→6 transition is the LSV→IDZ reduction pathway described in Lei \(2025a, §4\.7\): linearization around an operating point, spatial discretization, and transfer function identification\. The IDZ level is the primary control model for MPC design; the ID and I levels serve for preliminary design and analytical insight\.


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

The control model layer derives simplified representations suitable for real\-time controller design\. CHS theory provides the theoretical basis for this simplification through the Unified Transfer Function Family \(Lei, 2025a, Theorem 2; structurally grounded in the Six\-Element Architecture and Structural Isomorphism of Proposition 1\): all water conveyance systems belong to either Family α \(integrating/non\-self\-regulating: $G(s) = (1+\tau_m s) e^{-\tau_d s} / (A_s \cdot s)$\) or Family β \(self\-regulating: $H(s) = (1-KXs) / (1+K(1-X)s)$\), and the five\-level model hierarchy \(LSV→IDZ→ID→I→SS\) provides a principled reduction pathway from full PDE to steady\-state\.

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

__3\.8  Cross\-Domain MBD Comparison__

Table 1b compares the CHS\-MBD framework with established MBD frameworks in other safety\-critical domains\.

__*Table 1b\. Cross\-Domain MBD Framework Comparison*__

| Aspect | Automotive \(AUTOSAR\) | Aerospace \(DO\-178C\) | CHS\-MBD |
|--------|----------------------|----------------------|----------|
| Governing standard | ISO 26262 | DO\-178C/DO\-331 | Proposed \(WSAL\) |
| Model layers | 3 \(App/RTE/BSW\) | 5 \(Requirements→Object code\) | 7 \(Physics→Deployment\) |
| Safety concept | ASIL \(A–D\) | DAL \(A–E\) | WSAL \(1–5\) \+ ODD |
| Verification method | HiL mandatory | DO\-178C testing | xIL \(MiL→SiL→HiL→PiL\) |
| Code generation | AUTOSAR\-compliant | DO\-178C\-qualified | IEC 61131\-3 |
| Physical model role | Vehicle dynamics sim | Flight dynamics sim | Saint\-Venant / pipe transient |
| Domain maturity | Mature \(20\+ years\) | Mature \(30\+ years\) | Emerging |
| Open\-source tools | Limited | Limited | Growing \(OpenModelica, FMI\) |

The key structural difference is the prominence of Layer 7 \(physical model\): in automotive and aerospace, the physical plant model is well\-characterized and standardized, whereas in water systems, each installation has unique geometry, and the physical model must be site\-calibrated—making the Layer 7→6 validation step more challenging and more important\.

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

The CHS\-MBD toolchain reference implementation provides basic FMI coupling between OpenModelica water component models and Python/do\-mpc controllers, demonstrating the feasibility of this approach for a single\-pool canal control scenario\. Scaling to multi\-agent systems with realistic complexity is an active area of development\.

Importantly, the FMI pathway enables a fully open\-source MBD pipeline for Layers 7–6: OpenModelica \(L7, OSMC Public License\), Python with do\-mpc and python\-control \(L6, open\-source\), and FMI 2\.0 \(open standard\) provide a complete physics\-to\-controller workflow without commercial dependencies\. For Layers 3–2, commercial tools currently dominate \(Simulink PLC Coder, CODESYS\), but an emerging open\-source pathway exists: OpenModelica's code generation to C, combined with open PLC platforms \(e\.g\., OpenPLC\) and open SCADA systems \(e\.g\., ScadaBR\), could extend the open\-source pipeline to deployment\. This open\-source philosophy aligns with the growing recognition that computational hydrology must be reproducible \(Hutton et al\., 2016\) and that open\-source tools democratize access to advanced methods for institutions with limited resources\.

__5  Educational Software Infrastructure for CHS__

__5\.1  The Software\-Driven Interdisciplinary Challenge__

CHS sits at the intersection of three established disciplines: water engineering, control engineering, and software engineering\. Training the next generation of water systems engineers requires not only a conceptual curriculum but also a software infrastructure that enables hands\-on, MBD\-layer\-by\-layer learning\. The absence of integrated educational software packages is a major barrier to CHS adoption: students cannot learn model\-based water control if the tools for building physical models, designing controllers, generating embedded code, and running xIL tests exist in disconnected, expensive, or inaccessible silos\.

__5\.2  Educational Software Stack by MBD Layer__

Table 3 maps the required educational software infrastructure to MBD layers, identifying existing tools, gaps, and open\-source alternatives\.

__*Table 3\. Educational Software Infrastructure for CHS Training*__

| MBD Layer | Learning Objective | Software Tool | Status | Gap / Need |
|-----------|-------------------|---------------|--------|------------|
| L7 | Build physical model | OpenModelica \+ water library | Partial | Water component library needed |
| L6 | Derive control model | python\-control, Simulink | Available | Open\-source MPC toolbox needed |
| L6→L7 | Validate model reduction | FMI co\-simulation | Prototype | Turnkey FMI coupling script |
| L5 | Design agent architecture | Custom notebooks | Gap | Architecture design GUI needed |
| L4 | Define ODD, write xIL plan | Spreadsheets | Gap | ODD specification editor needed |
| L3 | Generate PLC code | CODESYS, Simulink PLC Coder | Available | Free academic licenses needed |
| L2 | Configure PLC hardware | PLC IDE | Available | Standardized lab PLC kit needed |
| L1 | Run xIL verification | Custom scripts | Gap | Integrated xIL orchestration tool |

__5\.3  Virtual Laboratory and Remote Access__

A key opportunity for democratizing CHS education is the development of cloud\-based virtual laboratories that provide remote access to simulation \(Layers 7–6\) and emulated hardware \(Layers 3–2\) environments\. Students at institutions without physical flume facilities could access virtual xIL environments hosted by partner institutions, running OpenModelica plant models coupled with student\-designed controllers via web\-based interfaces\. This approach is analogous to remote laboratory platforms in electrical engineering education \(Zubia & Alves, 2011\) and would address the capital investment barrier that limits CHS education to well\-resourced institutions\.

__5\.4  Physical Test Facility Standards__

The most capital\-intensive educational component is a laboratory\-scale hydraulic test bench—a multi\-pool canal flume with motorized gates and real\-time water level sensors—providing the physical plant for HiL and PiL verification\. Multi\-pool canal flumes exist at several research institutions \(Delft, INRAE, Melbourne, IWHR\), but their designs are not standardized\. Developing an open\-source flume specification with standardized gate actuators, sensor interfaces, and PLC connectivity would enable reproducible CHS education across institutions\. The standardized flume would serve as both an educational platform and a community benchmark for comparing control algorithms—analogous to the OpenAI Gym benchmarks in reinforcement learning research \(Brockman et al\., 2016\)\.

__5\.5  Competency Framework and Assessment__

A discipline\-construction paper must specify not only what to teach but what graduates should be able to do\. Table 3b presents a competency matrix mapping MBD layers to Bloom's taxonomy levels, with specific learning outcomes and assessment methods\.

__*Table 3b\. CHS Competency Matrix: MBD Layer × Bloom's Taxonomy*__

| MBD Layer | Bloom's Level | Learning Outcome | Assessment Method |
|-----------|--------------|------------------|-------------------|
| L7 Physical | Understand / Apply | Derive Saint\-Venant equations for a given geometry; build and validate an OpenModelica canal model | Written exam \+ lab report |
| L6 Control | Apply / Analyze | Identify IDZ parameters from step\-response data; design an MPC controller meeting tracking specs | Lab report \+ MATLAB/Python assignment |
| L6→L7 Validation | Analyze | Validate control model against physical model across ODD; quantify model mismatch | FMI co\-simulation lab report |
| L5 Architecture | Analyze / Evaluate | Design a MAS agent hierarchy for a multi\-pool system; specify communication protocols and failover | Design project report |
| L4 Certification | Evaluate | Define a formal ODD; write an xIL test matrix; specify WSAL admission criteria | Design project \+ peer review |
| L3 Software | Apply / Create | Generate IEC 61131\-3 Structured Text from a verified model; integrate with SCADA via OPC\-UA | Code review \+ lab demonstration |
| L2–L1 Deployment | Create / Evaluate | Execute a complete xIL campaign \(MiL→SiL→HiL\) on the laboratory flume; diagnose and resolve failures | Capstone project with oral defense |

The competency progression is designed to be vertically integrated: each layer builds on the competencies developed at higher layers\. This vertical integration is the unique differentiator of CHS education compared with existing curricula\. Traditional water engineering programs cover Layer 7 \(hydraulic modeling\) but not Layers 6–1\. Control engineering programs cover Layers 6–3 but without domain\-specific physical models \(Layer 7\) or water\-specific safety certification \(Layer 4\)\. Software engineering programs cover Layer 3 but without the physical\-model and control\-theoretic foundations\. CHS education integrates all seven layers into a coherent progression, producing graduates who can trace a design decision from the Saint\-Venant equations through to PLC code and xIL verification\.

Assessment rigor increases with Bloom's level: Layers 7–6 are assessed through individual exams and assignments \(factual and procedural knowledge\); Layers 5–4 through team design projects \(analytical and evaluative thinking\); Layers 3–1 through capstone projects with physical hardware \(synthesis and real\-world problem\-solving\)\. The capstone project—designing, implementing, and verifying a complete control system on the laboratory flume—serves as the integrative assessment that demonstrates competency across all MBD layers\.

__*\[Figure 4 about here\]*__

__6  Reference Workflow: Canal Control Design\-to\-Deployment__

__6\.1  Problem Setup__

To illustrate the MBD framework, we trace a reference workflow for designing, verifying, and deploying an autonomous control system for a three\-pool irrigation canal\. The canal has the following parameters: pool lengths L₁ = L₂ = L₃ = 2,000 m; trapezoidal cross\-section with bottom width b = 3 m, side slope m = 1\.5; design flow Q₀ = 5 m³/s; downstream control gates at each pool boundary; water level sensors at downstream ends\.

__6\.2  Layer 7: Physical Model \(OpenModelica\)__

The physical model is constructed in OpenModelica using a component\-based approach\. Each canal pool is modeled as a CanalPool component solving the one\-dimensional Saint\-Venant equations:

*∂A/∂t \+ ∂Q/∂x = q\_lat     \(1\)*

*∂Q/∂t \+ ∂\(Q²/A\)/∂x \+ gA\(∂h/∂x\) = gA\(S₀ − S\_f\) \+ q\_lat · v\_lat     \(2\)*

where A is cross\-sectional area, Q is flow, q\_lat is lateral inflow, g is gravitational acceleration, S₀ is bed slope, and S\_f is friction slope computed from Manning's equation\. Each pool is discretized with a Preissmann implicit scheme using θ = 0\.6 and Δx = 100 m \(20 nodes per pool\)\. The choice θ = 0\.6 follows standard practice for canal applications \(Litrico & Fromion, 2009\), providing adequate numerical diffusion control without excessive dissipation\. Gate components implement the standard orifice equation: $Q_{gate} = C_d \cdot w \cdot a \cdot \sqrt{2g \cdot \Delta h}$ where w is gate width, a is opening, and Δh is head difference\.

The three\-pool model contains 63 state variables \(water level and flow at each node\)\. Validation against the analytical backwater curve for uniform flow yields RMSE < 0\.002 m; validation against a measured gate step\-response dataset from the IWHR flume facility yields RMSE = 0\.008 m over a 2\-hour transient\.

__6\.3  Layer 6: Control Model \(IDZ Derivation and MPC Design\)__

The IDZ transfer function for each pool is identified from the Layer 7 model through step\-response analysis, following the methodology of Litrico & Fromion \(2009, Ch\. 3\)\. A downstream gate opening step of Δa = 0\.05 m is applied; the resulting water level response over a 3\-hour simulation window is fitted to the IDZ model $G(s) = (1 + \tau_m s) e^{-\tau_d s} / (A_s \cdot s)$ using nonlinear least\-squares \(Levenberg\-Marquardt\), minimizing $J = \sum_{k=1}^{N} (h_{SV}(k\Delta t) - h_{IDZ}(k\Delta t))^2$\. The 95% confidence intervals on identified parameters are ±3% for $A_s$, ±5% for $\tau_d$, and ±8% for $\tau_m$ \(wider for $\tau_m$ because the non\-minimum\-phase zero is harder to identify from step data\)\. The identified parameters for the reference operating point \(Q₀ = 5 m³/s, h₀ = 1\.2 m\) are:

__*Table 4\. IDZ Parameters for Three\-Pool Canal*__

| Pool | A\_s \(m²\) | τ\_d \(s\) | τ\_m \(s\) |
|------|-----------|-----------|-----------|
| 1 | 6,800 | 420 | 180 |
| 2 | 7,100 | 440 | 190 |
| 3 | 6,500 | 400 | 170 |

The IDZ model is validated against the Saint\-Venant model \(Layer 7\) across the ODD: step response RMSE is below 0\.01 m for Q ∈ \[3, 7\] m³/s, increasing to 0\.025 m at the ODD boundary \(Q = 2 m³/s and Q = 8 m³/s\) where nonlinear effects become more significant\. Sensitivity analysis confirms robustness: a ±10% perturbation in the most influential parameter \($A_s$\) increases the worst\-case closed\-loop RMSE from 0\.042 m to 0\.048 m—still below the 0\.05 m acceptance threshold\.

An MPC controller is designed in MATLAB/Simulink using the IDZ state\-space model \(second\-order Padé for delay, ZOH discretization\)\. Key design parameters:

__*Table 5\. MPC Controller Configuration*__

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Sampling time Δt | 60 s | Consistent with gate actuator speed |
| Prediction horizon N | 20 steps \(20 min\) | Delay\-compensation condition: N·Δt ≥ 2τ\_d \(Litrico & Fromion, 2009, Ch\. 5\) |
| Control horizon N\_u | 5 steps | Computational tractability |
| Output weight α\_y | 1\.0 | Primary objective: level tracking |
| Input rate weight α\_u | 0\.1 | Smooth gate movements |
| Water level bounds | \[0\.8, 1\.5\] m | Hard constraints \(safety\) |
| Gate rate limit |Δu| | 0\.02 m/step | Actuator physical limit |
| Solver | quadprog \(active set\) | Feasible for 60\-s cycle on PLC |

__6\.4  Layers 5–4: Architecture and Certification__

The MAS architecture assigns one Edge Agent per gate \(3 agents\), one Area Agent for the canal reach, and one Cloud Agent for planning\. The DMPC coordination protocol is specified: sequential upstream\-to\-downstream iteration with 3 DMPC iterations per control step\. The ODD is formally defined: $ODD = S_{flow} \times S_{level} \times S_{equip} \times S_{comm}$ where S\_flow = \[2, 8\] m³/s, S\_level = \[0\.7, 1\.6\] m, S\_equip = all 3 gates functional, S\_comm = heartbeat interval ≤ 60 s\. The MiL test matrix specifies 12 scenarios: 4 flow conditions \(2, 4, 6, 8 m³/s\) × 3 disturbance types \(upstream step ±20%, downstream offtake ±0\.5 m³/s, sensor noise σ = 0\.01 m\)\. DfO metric evaluation: $\sigma_{min}(W_c) = 0.12$ \(above threshold γ\_c = 0\.01\); $\kappa(W_o) = 45$ \(below κ\_max = 100\); $R_{ODD} = 0.97$ \(above 0\.95\)\.

__6\.5  Layers 3–1: Software, Hardware, Deployment__

The MPC controller is automatically translated from Simulink to IEC 61131\-3 Structured Text using Simulink PLC Coder\. The generated code \(~2,400 lines of Structured Text\) is loaded onto three CODESYS\-compatible PLCs \(one per gate\)\. Communication uses Modbus TCP/IP at 1\-s polling for gate\-to\-Edge Agent and OPC\-UA at 60\-s updates for Edge\-to\-Area Agent\. Layer 0 safety interlocks are programmed in ladder logic on a separate safety PLC: if h > 1\.5 m, open gate fully; if h < 0\.7 m, close gate fully\.

__6\.6  Quantitative MiL Results__

The FMI co\-simulation couples the Simulink MPC controller \(Layer 6\) with the OpenModelica plant model \(Layer 7\) using FMI 2\.0 for Co\-Simulation\. The communication step size is 10 s \(6 exchanges per MPC step\)\. All 12 ODD scenarios are executed; Table 6 summarizes the results\.

__*Table 6\. MiL Verification Results \(12 ODD Scenarios\)*__

| Metric | Mean | Worst Case | Threshold | Pass? |
|--------|------|------------|-----------|-------|
| Water level RMSE \(m\) | 0\.018 | 0\.042 | 0\.050 | Yes |
| Max level violation | 0 | 0 | 0 | Yes |
| Gate rate violation | 0 | 0 | 0 | Yes |
| MPC solve time \(ms\) | 12 | 28 | 1,000 \(= Δt\) | Yes |
| DMPC iterations to converge | 2\.1 | 3 | 5 | Yes |

The worst\-case RMSE \(0\.042 m\) occurs at the ODD boundary \(Q = 8 m³/s\) where the IDZ model mismatch is largest\. Even in this case, all hard constraints are satisfied and the RMSE is well below the 0\.05 m threshold\. MPC computation time \(mean 12 ms, max 28 ms\) is two orders of magnitude below the 60\-s sampling interval, confirming real\-time feasibility on standard PLC hardware\.

__*\[Figure 3 about here\]*__

__7  Discussion__

__7\.1  DfO as a Design Paradigm Shift__

DfO represents a shift in how water engineers think about infrastructure value\. Under DfC, value is created during construction—a well\-designed dam is a good dam\. Under DfO, value is created during operation—a well\-controlled dam is a good dam\. This shift has implications for procurement \(operational performance criteria in design contracts\), regulation \(operational certifiability as a design requirement\), and insurance \(automated control as a risk mitigation factor\)\. The DfO paradigm also reframes the economics of water infrastructure\. A parametric estimate based on the reference workflow suggests that adding DfO provisions \(sensor placement optimization, actuator co\-sizing, ODD specification, xIL test plan\) adds 5–8% to the design engineering budget—approximately ¥500K–800K for a ¥10M canal control project\. Post\-construction sensor and actuator additions typically cost 3–5× the equivalent design\-phase provisions due to civil works, system shutdown, and re\-commissioning\. Autonomous control \(WSAL\-2\+\) reduces operational labor by 40–60% and improves water delivery efficiency by 5–15% compared to manual SCADA operation, based on early results from pilot projects \(Lei et al\., 2025c\)\. Over a 30\-year operational lifecycle, the design\-phase DfO investment represents <0\.5% of cumulative operational costs, while the operational savings are estimated at 10–20× the DfO investment\. These are order\-of\-magnitude estimates; project\-specific cost\-benefit analysis is an identified research need\.

Industry adoption of DfO can follow a graduated pathway\. In Stage 1 \(immediate\), a "DfO Design Review Checklist" can be introduced as a supplementary requirement in existing procurement processes—5–10 additional design review questions covering controllability \(P1\), observability \(P2\), and ODD achievability \(P3\)\. In Stage 2 \(2–5 years\), pilot DfO requirements can be applied to project types with high automation potential: inter\-basin water transfers, automated irrigation districts, and urban pump station networks\. In Stage 3 \(5–10 years\), DfO can be formalized as a design standard, with WSAL\-level requirements embedded in regulatory frameworks\. This graduated pathway mirrors the industry adoption trajectory of model\-based design in automotive, where ISO 26262 took approximately 15 years from initial concept to mandatory standard\.

__7\.2  MBD and the V\-Model__

The seven\-layer MBD framework maps naturally onto the V\-model of systems engineering, where the left side of the V \(Layers 7→1 in design\) mirrors the right side \(Layers 1→7 in verification\)\. Layer 7 physical models are validated against field data \(top right\); Layer 6 control models are validated against Layer 7 simulations; Layer 3 software is verified against Layer 6 models \(SiL\); Layers 2–1 hardware and deployment are verified against Layer 7 through HiL and PiL\. This V\-model correspondence provides a natural quality assurance framework for CHS engineering projects\.

__7\.3  Curriculum Integration Challenges__

The proposed CHS curriculum faces practical challenges\. First, faculty expertise: few academics simultaneously possess deep knowledge of hydraulics, control theory, and embedded systems\. The curriculum may require team\-teaching across departments, which is institutionally difficult\. Second, laboratory cost: the physical test facility \(flume with automated gates\) requires significant capital investment\. Third, industry alignment: graduates of this program would need employment in a water automation sector that is still nascent\. The curriculum design must balance depth in CHS\-specific skills with breadth in transferable competencies \(MPC, embedded systems, SCADA\) that are valued across infrastructure sectors\.

__7\.4  DfO, MBD, and Digital Twins__

The digital twin paradigm has become the dominant framework for operational intelligence in water systems \(Rashidi et al\., 2020\) and smart infrastructure broadly\. A digital twin is a dynamic virtual representation of a physical asset that mirrors its real\-time state through sensor data, enabling monitoring, simulation, and predictive analytics\. The relationship between DfO\-MBD and digital twins is hierarchical and clarifying\.

First, the MBD Layer 7 physical model is the digital twin's simulation core\. When calibrated and connected to real\-time sensor feeds, the Layer 7 model becomes a descriptive digital twin—one that mirrors the current state of the infrastructure\. Second, Layers 6–3 of MBD provide what we call the controller twin: the simplified control models, agent architecture, and embedded software that enable the digital twin to be prescriptive rather than merely descriptive\. A descriptive digital twin answers "what is happening?"; a prescriptive digital twin answers "what should we do?" and executes the answer autonomously\. The MBD framework structures the development of both twins in an integrated pipeline\.

Third, and most importantly, DfO extends the digital twin concept temporally\. Most digital twin implementations are retrofitted to existing infrastructure: the physical asset is built, and the digital twin is constructed afterwards to mirror it\. DfO inverts this sequence by embedding operational intelligence—the digital twin and controller twin—into the design process from the earliest stages\. Infrastructure designed under DfO is "born digital twin\-ready": the physical model \(Layer 7\), control model \(Layer 6\), and ODD specification \(Layer 4\) are design deliverables, not post\-construction additions\. This distinction has practical implications: a DfO\-designed canal includes sensor placement optimized for state observability \(Principle P2\), actuator sizing co\-optimized with the control algorithm \(Principle P1\), and a pre\-verified ODD \(Principle P3\)—none of which a retrofitted digital twin can guarantee\.

Building Information Modeling \(BIM\) captures the physical design in a structured digital format; DfO extends BIM by embedding operational intelligence as first\-class design deliverables\. Specifically, the Industry Foundation Classes \(IFC\) data model could be extended with CHS\-specific property sets carrying ODD specifications \(as bounded parameter ranges\), control model parameters \(IDZ coefficients per pool\), and xIL test results \(as linked verification records\)\. This DfO\-enriched BIM would enable a seamless handoff from design to operation: the infrastructure's "operational DNA" is embedded in the same digital model used for its structural design\. Systems engineering \(SE\) provides a general framework for complex system development \(Estefan, 2007; Friedenthal et al\., 2014\); CHS\-MBD specializes SE to the water domain with domain\-specific model hierarchies \(the five\-level family\) and verification concepts \(xIL, WSAL\)\.

__7\.5  Data\-Driven and Machine Learning Approaches within the MBD Framework__

The MBD framework as presented is classical: physics\-based models \(Layer 7\), linearized transfer functions \(Layer 6\), and model\-based control \(MPC\)\. However, data\-driven and machine learning \(ML\) approaches are increasingly important in water systems modeling and control \(Razavi et al\., 2021\), and the MBD framework should explicitly accommodate them\.

Data\-driven models occupy three positions in the MBD hierarchy\. First, as Layer 7 surrogates: neural network emulators or reduced\-order models trained on Saint\-Venant simulation data can provide orders\-of\-magnitude speedup for real\-time applications, enabling digital twin deployments where full PDE solvers are too slow\. Second, as Layer 6 alternatives: when linearization is inadequate \(e\.g\., highly nonlinear systems or systems with unknown parameters\), data\-driven models—including physics\-informed neural networks \(PINNs\) and neural ODEs—can serve as MPC internal models that preserve physical structure while learning residual dynamics from operational data \(Tsai et al\., 2021\)\. Third, as Cognitive Intelligence \(CI\) components: reinforcement learning \(RL\) agents operating at HDC Layer 3 can learn high\-level operational policies \(e\.g\., seasonal reservoir dispatch\) that complement the MPC\-based real\-time control at HDC Layers 1–2\.

The integration of data\-driven approaches raises a fundamental challenge for safety certification \(Layer 4\)\. Black\-box ML models lack the formal guarantees \(constraint satisfaction, stability margins\) that model\-based controllers provide\. The ODD framework offers a structured approach to this challenge: data\-driven controllers can be admitted within well\-characterized ODD boundaries where their performance has been statistically validated through extensive xIL testing—providing probabilistic confidence rather than the formal guarantees \(feasibility ⇒ constraint satisfaction\) that model\-based MPC offers\. The model\-based MPC serves as a safety fallback outside the validated ODD\. This hybrid architecture—ML for performance within ODD, MPC for safety everywhere—is analogous to the runtime monitoring approach in autonomous vehicles\. The verification challenge for data\-driven water controllers—ensuring that learned policies respect physical constraints across the ODD—remains an open research problem that the MBD framework structures but does not solve\.

__7\.6  Limitations__

Several limitations should be acknowledged\. First, the MBD framework is presented conceptually with one reference workflow \(three\-pool canal\); validation across diverse infrastructure types \(reservoirs, pipe networks, pump stations\) is ongoing\. Second, the software tool chain assessment reflects 2025 capabilities; rapid evolution in open\-source tools may alter the gap analysis\. Third, the curriculum has been designed but not yet implemented as a full program; pilot courses at Hebei University of Engineering are planned for 2026–2027\. Fourth, the DfO paradigm requires buy\-in from the water infrastructure community—design consultants, regulatory agencies, and utilities—which is an institutional rather than technical challenge\. Fifth, the reference implementation \(CHS\-MBD toolchain\) is at prototype stage; production\-quality tools require sustained community development\.

__8  Conclusions__

This paper has presented three contributions for establishing Cybernetics of Hydro Systems as an interdisciplinary discipline\.

First, Design for Operation \(DfO\) provides a paradigm shift from construction\-centric to operation\-centric water engineering\. DfO's five principles—controllability, observability, ODD\-awareness, verifiability, and maintainability by design—extend the design objective function to include operational performance as a first\-class criterion\. This paradigm shift has implications for procurement, regulation, education, and the economics of water infrastructure\.

Second, the seven\-layer Model\-Based Definition \(MBD\) framework structures the progression from physical\-law models \(Layer 7\) through control models, architecture, safety certification, software, hardware, to operational deployment \(Layer 1\)\. Each layer is mapped to available software tools, identifying three critical gaps: physical model componentization \(FMI\-compatible water libraries\), architecture description language, and standardized ODD specification format\. The FMI integration pathway is demonstrated through a reference implementation coupling OpenModelica physical models with Python/do\-mpc controllers via a fully open\-source pipeline\.

Third, a two\-year graduate curriculum organized around the MBD layers, accompanied by a competency framework mapping MBD layers to Bloom's taxonomy levels, provides a concrete and assessable educational foundation for training the next generation of water systems engineers in the interdisciplinary synthesis that CHS demands\.

The reference workflow—a three\-pool canal control system traced from physical model through MPC design, automatic code generation, and xIL verification—demonstrates that the DfO\-MBD framework is not merely conceptual but implementable with existing tools, albeit with gaps that require community development\. The CHS\-MBD toolchain reference implementation is offered as a starting point for this community effort\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\. The authors thank the members of the CHS working group at Hebei University of Engineering and IWHR for discussions that shaped the MBD framework and curriculum design\.

__References__

Blochwitz, T\., Otter, M\., Akesson, J\., Arnold, M\., Clauss, C\., Elmqvist, H\., Friedrich, M\., Junghanns, A\., Mauss, J\., Neumerkel, D\., Olsson, H\., & Viel, A\. \(2012\)\. Functional Mockup Interface 2\.0: The standard for tool independent exchange of simulation models\. In Proceedings of the 9th International Modelica Conference \(pp\. 173–184\)\. https://doi\.org/10\.3384/ecp12076173

Borrego, M\., & Newswander, L\. K\. \(2010\)\. Definitions of interdisciplinary research: Toward graduate\-level interdisciplinary learning outcomes\. The Review of Higher Education, 34\(1\), 61–84\. https://doi\.org/10\.1353/rhe\.2010\.0006

Boothroyd, G\., Dewhurst, P\., & Knight, W\. A\. \(2011\)\. Product design for manufacture and assembly \(3rd ed\.\)\. CRC Press\.

Brockman, G\., Cheung, V\., Pettersson, L\., Schneider, J\., Schulman, J\., Tang, J\., & Zaremba, W\. \(2016\)\. OpenAI Gym\. arXiv preprint arXiv:1606\.01540\.

Castelletti, A\., Ficchì, A\., Cominola, A\., Segovia, P\., Giuliani, M\., Wu, W\., Lucia, S\., Ocampo\-Martinez, C\., De Schutter, B\., & Maestre, J\. M\. \(2023\)\. Model Predictive Control of water resources systems: A review and research agenda\. Annual Reviews in Control, 55, 442–465\. https://doi\.org/10\.1016/j\.arcontrol\.2023\.03\.013

Creaco, E\., Campisano, A\., Fontana, N\., Marini, G\., Page, P\. R\., & Walski, T\. \(2019\)\. Real time control of water distribution networks: A state\-of\-the\-art review\. Water Research, 161, 517–530\. https://doi\.org/10\.1016/j\.watres\.2019\.06\.025

Estefan, J\. A\. \(2007\)\. Survey of model\-based systems engineering \(MBSE\) methodologies \(Rev\. B\)\. INCOSE MBSE Initiative\.

Friedenthal, S\., Moore, A\., & Steiner, R\. \(2014\)\. A practical guide to SysML: The systems modeling language \(3rd ed\.\)\. Morgan Kaufmann\.

Fritzson, P\. \(2014\)\. Principles of object\-oriented modeling and simulation with Modelica 3\.3 \(2nd ed\.\)\. Wiley\-IEEE Press\.

Gomes, C\., Thule, C\., Broman, D\., Larsen, P\. G\., & Vangheluwe, H\. \(2018\)\. Co\-simulation: A systematic literature review\. ACM Computing Surveys, 51\(3\), 1–33\. https://doi\.org/10\.1145/3179993

Hutton, C\., Wagener, T\., Freer, J\., Han, D\., Duffy, C\., & Arheimer, B\. \(2016\)\. Most computational hydrology is not reproducible, so is it really science? Water Resources Research, 52\(10\), 7548–7555\. https://doi\.org/10\.1002/2016WR019285

IEC\. \(2018\)\. IEC 62443: Industrial communication networks—Network and system security\. International Electrotechnical Commission\.

IPCC\. \(2022\)\. Climate change 2022: Impacts, adaptation and vulnerability\. Contribution of Working Group II to the Sixth Assessment Report\. Cambridge University Press\. https://doi\.org/10\.1017/9781009325844

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

Rashidi, M\., Mohammadi, M\., Sadeghlou, S\. S\., Shafieezadeh, A\., & Bakhshi, A\. \(2020\)\. Digital twin for water distribution networks: A systematic review\. Journal of Water Resources Planning and Management, 146\(12\), 03120001\. https://doi\.org/10\.1061/\(ASCE\)WR\.1943\-5452\.0001290

Razavi, S\., Tolson, B\. A\., Matott, L\. S\., Thomson, N\. R\., MacLean, A\., & Seglenieks, F\. R\. \(2021\)\. The future of sensitivity analysis: An essential discipline for systems modeling and policy support\. Environmental Modelling & Software, 137, 104954\. https://doi\.org/10\.1016/j\.envsoft\.2020\.104954

Savic, D\. \(2022\)\. Digital water developments and lessons learned from automation in the car and aircraft industries\. Engineering, 9\(2\), 35–41\. https://doi\.org/10\.1016/j\.eng\.2021\.05\.013

Vojinovic, Z\., & Tutulic, D\. \(2009\)\. On the use of 1D and coupled 1D\-2D modelling approaches for assessment of flood damage in urban areas\. Urban Water Journal, 6\(3\), 183–199\. https://doi\.org/10\.1080/15730620802566877

Zubia, J\. G\., & Alves, G\. R\. \(Eds\.\)\. \(2011\)\. Using remote labs in education: Two little ducks in remote experimentation\. University of Deusto\.

Tsai, W\.\-P\., Feng, D\., Jia, X\., Shen, C\., Liu, J\., Chau, K\.\-W\., et al\. \(2021\)\. From calibration to parameter learning: Harnessing the scaling effects of big data in geoscientific modeling\. Nature Communications, 12, 5988\. https://doi\.org/10\.1038/s41467\-021\-26107\-z

US Army Corps of Engineers\. \(2023\)\. HEC\-RAS River Analysis System: Hydraulic reference manual \(Version 6\.4\)\. Hydrologic Engineering Center\.

van Overloop, P\. J\. \(2006\)\. Model predictive control on open water systems \(Doctoral dissertation\)\. Delft University of Technology\.

__Figure Captions__

__Figure 1\. __Design for Operation \(DfO\) paradigm contrasted with Design for Construction \(DfC\)\. Left: DfC pipeline where operational intelligence is added post\-construction as an afterthought\. Right: DfO pipeline where operational performance criteria \(controllability, observability, ODD, verifiability, maintainability\) are integrated from conceptual design through deployment\. The DfO pipeline produces an infrastructure that is not merely built to specification but designed to be operated autonomously\.

__Figure 2\. __The seven\-layer Model\-Based Definition \(MBD\) framework for water systems control, with V\-model correspondence\. Left: layers 7–1 in descending order of physical fidelity \(design arm of the V\)\. Center: V\-model showing the design\-to\-verification correspondence: Layer 7 models are validated against field data; Layer 6 models against Layer 7 simulations; Layer 3 software against Layer 6 models \(SiL\); Layers 2–1 hardware against Layer 7 \(HiL/PiL\)\. Right: software tools mapped to each layer, with critical gaps \(T1–T3\) highlighted\. The cross\-domain comparison \(Table 1b\) positions CHS\-MBD relative to AUTOSAR and DO\-178C\.

__Figure 3\. __Reference workflow: three\-pool canal control system traced through the seven MBD layers\. Top: physical model \(OpenModelica\) validated against analytical solution\. Middle: IDZ control model derivation and MPC design \(Simulink\)\. Bottom: automatic code generation \(Structured Text\), PLC deployment, and xIL verification sequence \(MiL → SiL → HiL → shadow mode\)\.

__Figure 4\. __CHS Competency Matrix: MBD Layer × Bloom's taxonomy level\. The matrix shows the expected progression from foundational knowledge \(Layer 7: understanding Saint\-Venant physics\) through application \(Layer 6: controller design\) and analysis \(Layer 5–4: architecture and certification\) to synthesis and evaluation \(Layers 3–1: implementation and deployment\)\. Assessment methods progress from individual exams \(Layers 7–6\) through team design projects \(Layers 5–4\) to capstone xIL campaigns on physical hardware \(Layers 2–1\)\. The vertical integration across all seven layers distinguishes CHS education from traditional water engineering or control engineering curricula\.
