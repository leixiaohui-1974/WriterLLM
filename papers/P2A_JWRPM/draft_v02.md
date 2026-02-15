*Manuscript submitted to Journal of Water Resources Planning and Management*

__From SCADA to Autonomy: A Multi\-Agent System Architecture__

__and Water Systems Autonomy Level Classification__

__with Applications to Cascade Hydropower and Inter\-Basin Transfer__

__Xiaohui Lei__1,2\*, Chao Su1, Yun Long1, Hao Wang2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research \(IWHR\), Beijing 100038, China

\*Corresponding author: Xiaohui Lei \(lxh@iwhr\.com\)

__Abstract__

Water conveyance infrastructure worldwide operates predominantly at manual\-supervisory levels, creating a widening gap between the operational intelligence of water systems and that of comparable infrastructure domains such as automotive and aerospace\. While the theoretical foundations of water system control have been articulated \(Lei, 2025a\), a critical missing element is an implementable system architecture that bridges theory and engineering practice—one that specifies how control algorithms, safety certification, and intelligent decision\-making should be organized within operational water networks\. This paper addresses that gap by presenting two interlocking contributions\. First, we formalize a Multi\-Agent System \(MAS\) architecture for autonomous water networks, defined as MAS = HDC \+ ODD \+ CI, where Hierarchical Distributed Control \(HDC\) serves as the physics\-based control engine operating across four temporal layers \(safety, regulation, coordination, planning\), the Operational Design Domain \(ODD\) defines certified operating envelopes within which autonomous control is permitted, and Cognitive Intelligence \(CI\) provides scenario recognition and adaptive goal assembly\. The architecture is instantiated through a three\-tier agent hierarchy \(Edge–Area–Cloud\) with formally defined communication protocols and island\-autonomy degradation modes\. Second, we propose Water Systems Autonomy Levels \(WSAL\), a five\-level classification \(WSAL\-1 through WSAL\-5\) with quantitative admission criteria for each level, adapted from SAE J3016 but incorporating three water\-specific design principles: the bucket principle, the non\-negotiable safety floor, and ODD\-bounded autonomy\. The framework is validated through two operational case studies representing distinct water infrastructure typologies\. Case Study 1—the Shaoping cascade hydropower station—demonstrates WSAL\-2 \(Assisted Control\) achievement through real\-time MPC\-based optimization of a multi\-reservoir cascade, showing \[XX\]% improvement in power generation efficiency and \[XX\]% reduction in water level deviations compared to rule\-based SCADA operation\. Case Study 2—the Jiaodong inter\-basin water transfer project—demonstrates WSAL\-2 achievement through multi\-timescale integration spanning annual allocation through real\-time gate control, with \[XX\]% reduction in operational water losses\. For both cases, we analyze the specific technological and institutional barriers to the WSAL\-2→3 transition and propose an X\-in\-the\-Loop \(xIL\) verification roadmap for ODD certification\. The results establish MAS\-WSAL as a practical framework for planning, benchmarking, and advancing the automation maturity of water conveyance systems worldwide\.

__Keywords: __autonomous water networks; multi\-agent systems; hierarchical distributed control; operational design domain; water systems autonomy levels; cascade hydropower; inter\-basin transfer

__1  Introduction__

The global stock of water conveyance infrastructure—canals, pipelines, reservoirs, pump stations, and associated control structures—represents a cumulative investment measured in trillions of dollars \(UNESCO, 2024\)\. These systems serve functions essential to human welfare: irrigation water delivery, urban water supply, hydroelectric power generation, flood management, and environmental flow maintenance\. Yet a persistent asymmetry characterizes the sector: while the science of designing and building water infrastructure is mature, the science of operating it in real time remains at an early stage\. Cross\-sector benchmarking reveals that operational autonomy of water conveyance systems worldwide remains at levels equivalent to manual driving with minimal driver assistance—decades behind the automation maturity achieved in automotive \(SAE Level 2–3\), commercial aviation \(Level 4–5 in cruise\), and power systems \(fully automated frequency regulation\) \(Lei, 2025a; Savic, 2022\)\.

Two recent developments have brought this gap into sharp focus\. First, advances in sensing, communication, and computing have made real\-time automated control technically feasible for water networks—yet adoption remains limited to isolated pilot projects rather than system\-wide deployment\. Second, the Cybernetics of Hydro Systems \(CHS\) framework \(Lei, 2025a; Lei et al\., 2025a\) has provided a unified theoretical foundation showing that all water conveyance and distribution systems share a structurally isomorphic six\-element control architecture and can be governed by a common set of eight principles organized into dual tetrads\. CHS establishes what water system control should achieve; what remains unaddressed is how—through what specific system architecture, safety certification framework, and intelligence hierarchy—water networks should transition from their current SCADA\-based supervisory mode to progressively higher levels of autonomous operation\.

This architectural gap has practical consequences\. Without a shared framework for describing and measuring automation maturity, water utilities, government agencies, and technology providers lack a common language for procurement, regulation, and investment planning\. Without a formal safety certification concept, operators face a binary choice between full manual control and opaque ‘smart water’ systems whose failure modes are poorly understood\. Without a layered intelligence architecture, the integration of physics\-based control and artificial intelligence remains ad hoc, with no principled allocation of responsibilities between algorithmic and human decision\-making\.

This paper addresses the architectural gap through two interlocking contributions\. The first contribution is the Multi\-Agent System \(MAS\) architecture for autonomous water networks, which organizes control intelligence into three components: Hierarchical Distributed Control \(HDC\) as the physics\-based engine, the Operational Design Domain \(ODD\) as the safety certification framework, and Cognitive Intelligence \(CI\) as the scenario\-aware decision layer\. The second contribution is Water Systems Autonomy Levels \(WSAL\), a five\-level classification with quantitative admission criteria that provides the shared vocabulary for planning, measuring, and advancing water network automation\.

Critically, both contributions are validated through operational engineering case studies rather than purely theoretical constructs\. The Shaoping cascade hydropower station \(Sichuan, China\) and the Jiaodong inter\-basin water transfer project \(Shandong, China\) represent two fundamentally different water infrastructure typologies—point\-based multi\-reservoir cascade control and linear long\-distance conveyance control, respectively—yet both are shown to achieve WSAL\-2 \(Assisted Control\) through implementations that share the common MAS architectural principles\. This dual\-case validation demonstrates the generalizability of the framework across infrastructure types\.

The remainder of the paper is structured as follows\. Section 2 reviews the state of the art in water system automation and identifies the specific gaps addressed\. Section 3 formalizes the MAS architecture\. Section 4 presents the WSAL classification with quantitative criteria\. Section 5 and Section 6 present the Shaoping and Jiaodong case studies, respectively\. Section 7 analyzes the WSAL\-2→3 transition pathway including X\-in\-the\-Loop verification requirements\. Section 8 discusses implications and limitations\. Section 9 concludes\.

__2  State of the Art and Research Gaps__

__2\.1  Water System Automation: Current Practice__

The dominant operational paradigm for water conveyance systems is Supervisory Control and Data Acquisition \(SCADA\)—a framework originally developed in the 1960s for industrial process monitoring that has been progressively adapted to water infrastructure\. SCADA provides real\-time data acquisition, alarm management, and remote manual control, but its decision architecture is fundamentally human\-centered: operators observe system state through SCADA displays and issue control commands based on experience, operating rules, and predefined schedules \(Savic, 2022\)\. The automation content is limited to low\-level interlocks \(e\.g\., closing a gate when water level exceeds a threshold\) and scheduled operations \(e\.g\., pump cycling\)\. Multi\-objective optimization, disturbance rejection, and inter\-subsystem coordination remain manual processes\.

Advanced control methods—particularly Model Predictive Control \(MPC\)—have been extensively developed in the research literature for water systems\. Malaterre et al\. \(1998\) provided an early classification of canal control algorithms\. Schuurmans \(1997\) and van Overloop \(2006\) developed MPC frameworks for open\-channel systems\. Negenborn et al\. \(2009\) introduced distributed MPC for irrigation canal networks\. Castelletti et al\. \(2023\) presented a comprehensive review of MPC applications across water resource systems\. However, a systematic review of field deployments reveals that the gap between laboratory demonstrations and operational adoption remains wide\. The few operational MPC implementations—such as those on Australian irrigation systems \(Mareels et al\., 2005; Cantoni et al\., 2007\) and select European canal systems \(Litrico & Fromion, 2009\)—remain confined to individual subsystems or pilot reaches, without integration into a coherent system\-wide architecture\.

__2\.2  Lessons from Cross\-Sector Automation__

Other infrastructure domains have successfully navigated the transition from manual to autonomous operation by developing three elements that the water sector currently lacks\. First, a shared autonomy classification: SAE J3016 \(SAE International, 2021\) defines six levels \(L0–L5\) of driving automation, providing a common vocabulary that aligns regulatory frameworks, technology development, and public communication\. The power sector uses a similar progression from manual to fully automatic generation control \(Kundur, 1994\)\. Second, a formal safety certification concept: the Operational Design Domain \(ODD\) in automotive defines the specific conditions under which automation is certified to operate, transforming the trust question from binary \(‘automate or not’\) to graduated \(‘automate under these specific conditions’\)\. ISO 26262 \(functional safety\) and ISO 21448 \(SOTIF—safety of the intended functionality\) provide certification standards\. Aerospace uses DO\-178C for airborne software certification \(RTCA, 2011\)\. Third, a layered intelligence architecture: autonomous vehicles integrate perception \(sensors\), prediction \(AI models\), planning \(optimization\), and control \(actuators\) within a principled architecture that allocates responsibilities across computational layers\.

The water sector possesses none of these three elements in operational form\. Several authors have noted the analogy between water and automotive automation\. Savic \(2022\) compared digital water developments with automation lessons from the car and aircraft industries\. Lei et al\. \(2025b\) proposed a preliminary intelligence level framework inspired by SAE J3016\. However, no prior work has formalized the complete triad—architecture, safety certification, and autonomy classification—as an integrated engineering framework validated through operational case studies\.

__2\.3  Research Gaps Addressed__

This paper addresses three specific gaps\. Gap 1 \(Architecture\): the water sector lacks a formal Multi\-Agent System architecture that specifies how physics\-based control, safety certification, and cognitive intelligence should be organized across spatial and temporal scales within an operational water network\. Gap 2 \(Classification\): the sector lacks a quantitative autonomy level classification with measurable admission criteria for each level, which is prerequisite for regulatory standardization and investment planning\. Gap 3 \(Validation\): existing proposals for water automation frameworks remain theoretical; what is needed is empirical demonstration through diverse operational case studies showing that a single architectural framework can accommodate fundamentally different infrastructure typologies\.

__3  The Multi\-Agent System Architecture__

This section presents the formal MAS architecture for autonomous water networks, defined as MAS = HDC \+ ODD \+ CI\. Each component is described in a dedicated subsection, followed by the agent hierarchy that integrates them\.

__3\.1  Hierarchical Distributed Control: The Physical AI Engine__

The Cybernetics of Hydro Systems \(CHS\) framework identifies a five\-level model–control hierarchy ranging from the full linearized Saint\-Venant equations \(Level 5\) through the Integrator\-Delay\-Zero model \(Level 4\) to steady\-state mass balance \(Level 1\), with a model–layer correspondence theorem linking each model level to the control architecture layer where its approximation errors are acceptable \(Lei et al\., 2025a\)\. Hierarchical Distributed Control \(HDC\) operationalizes this correspondence through four concurrent control layers\.

Layer 0 \(Safety Floor\) implements hard constraint enforcement through programmable logic controllers \(PLCs\) at millisecond cycle times\. Control logic consists exclusively of deterministic threshold comparisons: if water level h exceeds the maximum h\_max, the emergency gate opens unconditionally; if downstream flow Q\_out falls below ecological minimum Q\_eco, upstream extraction is curtailed\. No optimization, no model, no communication dependency—only Boolean logic that executes independently of all upper layers\. The Layer 0 design rule is the veto principle:

*Veto Principle:  ∀ command u from Layer k \(k ≥ 1\): if L0\_check\(u\) = UNSAFE, then u is blocked\.     \(1\)*

This principle reflects the operational singularity of water systems: failure irreversibility \(OS1\) demands that no algorithmic decision—however sophisticated—can override physical safety interlocks\. The Layer 0 safety floor remains active at all WSAL levels, including WSAL\-5\.

Layer 1 \(Real\-time Regulation\) deploys feedback control with physics\-based internal models at sampling intervals of seconds to minutes\. The canonical controller is MPC with an IDZ \(Integrator\-Delay\-Zero\) or ID \(Integrator\-Delay\) internal model, solving at each time step:

*min\_\{u\(k\),\.\.\.,u\(k\+N\-1\)\} Σ\_\{j=0\}^\{N\-1\} \[α\_y\(y\(k\+j\) \- y\_ref\)^2 \+ α\_u\(Δu\(k\+j\)\)^2\]     \(2\)*

*subject to:  x\(k\+j\+1\) = Ax\(k\+j\) \+ Bu\(k\+j\) \+ Ed\(k\+j\),  y\(k\+j\) = Cx\(k\+j\)     \(3\)*

*h\_min ≤ y\(k\+j\) ≤ h\_max,   u\_min ≤ u\(k\+j\) ≤ u\_max,   |Δu\(k\+j\)| ≤ Δu\_max     \(4\)*

where y is water level \(or pressure head\), u is actuator position \(gate opening, pump speed, valve setting\), d is the disturbance estimate \(inflow forecast, demand prediction\), N is the prediction horizon, and α\_y, α\_u are weighting parameters\. The state\-space matrices \(A, B, C, E\) are derived from the IDZ transfer function G\(s\) = \(1 \+ τ\_m·s\)·e^\(−τ\_d·s\) / \(A\_s·s\) through Padé approximation and zero\-order hold discretization \(Litrico & Fromion, 2004; Schuurmans et al\., 1995\)\. Layer 1 controllers operate independently for each control node \(gate, pump, valve\), using only local state and nearest\-neighbor boundary conditions\.

Layer 2 \(Coordination\) employs distributed MPC \(DMPC\) at minute\-to\-hour horizons\. While Layer 1 controllers optimize each subsystem independently, Layer 2 resolves inter\-subsystem conflicts by iteratively exchanging boundary information between neighboring agents\. For a series of N\_p canal pools or reservoir stages, each agent i solves a local MPC problem that incorporates coupling constraints with upstream agent i−1 and downstream agent i\+1:

*u\_i^\{\(k\+1\)\} = argmin J\_i\(u\_i\) \+ λ\_i^T g\_i\(u\_i, u\_\{i\-1\}^\{\(k\)\}, u\_\{i\+1\}^\{\(k\)\}\)     \(5\)*

where λ\_i are Lagrange multipliers updated through neighbor\-to\-neighbor communication at each DMPC iteration, g\_i captures the coupling constraints \(continuity of flow, shared storage targets\), and superscript \(k\) denotes the iteration count\. Convergence to a feasible coordinated solution is guaranteed under standard convexity assumptions \(Negenborn et al\., 2009; Maestre & Negenborn, 2014\)\. Layer 2 coordination enables system\-wide objectives—such as minimizing total energy consumption across a cascade, or balancing water levels across multiple reaches—without requiring centralized computation\.

Layer 3 \(Planning\) performs nested optimization over day\-to\-year horizons\. At this temporal scope, the appropriate internal models are pure Integrator \(Level 2\) or Steady\-State \(Level 1\) representations, where dynamic transients are negligible relative to planning horizons\. Layer 3 translates high\-level objectives—seasonal water allocation targets, annual energy generation goals, long\-term reservoir rule curves—into reference trajectories and constraint sets for Layer 2 and Layer 1\. The planning\-to\-control interface is formalized as:

*Layer 3 output: \{y\_ref\(t\), u\_bounds\(t\), d\_forecast\(t\)\} for t ∈ \[t\_now, t\_now \+ T\_plan\]     \(6\)*

The four\-layer HDC architecture constitutes what we term the Physical AI engine: every control decision at every layer is computed from mechanistic models grounded in conservation laws \(mass, momentum, energy\), with mathematically provable constraint satisfaction\. No learned correlation substitutes for physical law in safety\-critical control paths\.

__3\.2  Operational Design Domain: The Safety Certification Framework__

The Operational Design Domain \(ODD\) concept, adapted from automotive autonomous driving \(SAE International, 2021; ISO, 2022\), addresses the trust barrier that has limited water automation adoption\. An ODD for a water network segment is defined as a bounded region in a multi\-dimensional operating space:

__*Definition 1 \(ODD for Water Systems\)\. *__The Operational Design Domain of a water network control subsystem is the Cartesian product ODD = S\_flow × S\_level × S\_demand × S\_equip × S\_env × S\_comm, where S\_flow = \[Q\_min, Q\_max\] is the certified flow range, S\_level = \[h\_min, h\_max\] is the certified water level range, S\_demand enumerates the certified demand/disturbance scenarios \(e\.g\., normal delivery, peak demand, drought allocation\), S\_equip enumerates equipment status conditions \(e\.g\., all actuators functional, single actuator failure, dual redundancy degraded\), S\_env enumerates environmental conditions \(e\.g\., normal weather, storm, ice, extreme temperature\), and S\_comm specifies communication link requirements \(e\.g\., full connectivity, single link failure, island mode\)\.

Within the certified ODD, the HDC controller has been verified—through the X\-in\-the\-Loop \(xIL\) testing framework \(Lei et al\., 2025c\)—to maintain all constraints \(Equation 4\) while achieving performance targets\. Outside the ODD boundary, control authority reverts to human operators or to a predefined safe degradation mode\. The ODD boundary is monitored in real time by a dedicated ODD Monitor module that evaluates:

*ODD\_status\(t\) = ⋀\_\{d ∈ \{flow, level, demand, equip, env, comm\}\} \[state\_d\(t\) ∈ S\_d\]     \(7\)*

When ODD\_status transitions from TRUE to FALSE, the system executes a Minimum Risk Condition \(MRC\)—the water systems equivalent of ‘pulling over to the side of the road’ in automotive autonomy\. For water systems, MRC typically means: maintain current actuator positions \(freeze gates\), activate Layer 0 safety floor, alert human operators, and log all state variables for post\-event analysis\. The MRC design must account for the operational singularity: unlike a car that can safely stop, a water system’s mass in transit continues moving, so the MRC must ensure that the frozen state remains within safety constraints for a duration sufficient for human intervention \(the ‘coast time’ τ\_coast, typically minutes to hours depending on system inertia\)\.

__3\.3  Cognitive Intelligence: The Scenario\-Aware Decision Layer__

HDC computes accurately within a given scenario; ODD defines which scenarios are certified\. Cognitive Intelligence \(CI\) addresses what happens between scenarios: recognizing the current operational situation, selecting the appropriate objective function and constraint set, and reasoning about whether conditions are approaching ODD boundaries\. CI serves as the Cognitive AI engine of the architecture—complementary to the Physical AI engine of HDC\.

The CI module performs four functions\. First, scenario recognition: classifying the current operating state into one of the predefined scenario categories \(normal operation, drought, flood risk, equipment degradation, emergency\) using a combination of rule\-based logic, statistical classifiers, and—where appropriate—large language model reasoning for unstructured information integration \(weather advisories, operator notes, regulatory communications\)\. Second, goal assembly: translating the recognized scenario into a specific objective function and constraint set for HDC, including reference trajectories, weighting parameters, and constraint bounds\. Third, ODD boundary prediction: estimating the time\-to\-boundary for each ODD dimension, providing early warning when operating conditions are trending toward ODD limits\. Fourth, explainability: generating human\-readable explanations of automated decisions for operator oversight and regulatory compliance\.

The critical architectural rule governing CI is the propose\-validate interaction loop:

*CI proposes: \{θ\_new, y\_ref\_new, C\_new\} → HDC validates: feasibility\(A, B, θ\_new, C\_new\)     \(8\)*

*if feasible: execute;   if infeasible: CI revises or escalates to human operator     \(9\)*

where θ\_new is a proposed parameter set, y\_ref\_new is a proposed reference trajectory, and C\_new is a proposed constraint set\. This loop ensures that no CI reasoning error—however sophisticated the underlying AI model—can bypass the physics\-based feasibility checking of HDC\. The propose\-validate architecture represents a design choice grounded in the operational singularity \(OS1\): because water system failures are irreversible, the Cognitive AI engine must never have unilateral authority over actuators\.

__3\.4  The Agent Hierarchy: Edge–Area–Cloud__

The three MAS components \(HDC, ODD, CI\) are deployed through a three\-tier spatial hierarchy of intelligent agents, aligned with the physical topology of water networks\.

Edge Agents reside at individual control nodes \(a gate, a pump station, a valve, a turbine\)\. Each Edge Agent runs a complete Layer 0 safety PLC and a Layer 1 MPC controller with local IDZ/ID internal model\. The Edge Agent is self\-contained: if communication with upper\-tier agents is severed, it continues autonomous operation within its local ODD using the most recently received reference trajectory and the locally measured state\. This island\-autonomy capability reflects the slow\-actuator reality of water systems \(OS3\): communication interruptions of minutes to hours cannot be allowed to freeze actuators mid\-stroke\.

Area Agents coordinate groups of Edge Agents within a hydraulically coupled subsystem—a canal reach between major structures, a reservoir cascade, or a district metered area\. Area Agents execute Layer 2 DMPC, manage the intra\-area ODD, and run the CI scenario recognition module for their jurisdiction\. Communication between Area Agent and its Edge Agents uses a heartbeat protocol at intervals of 10–300 seconds\. Area Agents also mediate between Edge Agents and the Cloud Agent, translating system\-wide objectives into local reference trajectories\.

Cloud Agents provide system\-wide intelligence at Layer 3\. Cloud Agents run long\-horizon planning optimization, system\-wide CI for inter\-area conflict resolution, and global ODD monitoring\. The Cloud Agent communicates with Area Agents at intervals of minutes to hours\. Cloud Agents are the primary locus for integration with external information sources: weather forecasts, demand predictions, energy market signals, and regulatory requirements\.

Table 1 summarizes the agent hierarchy with its HDC layers, ODD scope, CI functions, and communication characteristics\.

__Table 1\. Agent hierarchy with HDC layer allocation, ODD scope, and communication__

__Agent Tier__

__HDC Layers__

__ODD Scope__

__CI Functions__

__Comm\. Interval__

__Island Mode__

__Edge__

L0 \(safety\)  
L1 \(regulation\)

Local node:  
single gate/pump  
/valve

None  
\(deterministic  
control only\)

Heartbeat:  
10–300 s

Full: continues  
L0\+L1 with last  
reference

__Area__

L2 \(coordination\)

Subsystem:  
canal reach,  
reservoir cascade

Scenario recog\.,  
goal assembly,  
ODD monitoring

DMPC update:  
1–30 min

Partial: L2  
reverts to  
independent L1s

__Cloud__

L3 \(planning\)

System\-wide:  
entire network

Inter\-area  
conflict, long\-  
horizon planning,  
explainability

Planning cycle:  
min–hours

Areas operate  
independently  
with last plan

__*\[Figure 1 about here\]*__

__4  Water Systems Autonomy Levels__

This section presents the WSAL classification with formal definitions and quantitative admission criteria for each level\.

__4\.1  Design Principles__

WSAL adapts the SAE J3016 autonomous driving taxonomy to water infrastructure while incorporating three water\-specific principles that reflect the operational singularity identified in CHS theory \(Lei et al\., 2025a\)\.

__*Principle W1 \(Bucket Principle\)\. *__The overall WSAL rating of a water network equals the minimum WSAL rating among its constituent subsystems: WSAL\_system = min\_i\(WSAL\_i\)\. A single manually operated gate in an otherwise automated network defines the system\-wide bottleneck, because water is a connected medium and a local control failure propagates hydraulically\.

__*Principle W2 \(Non\-negotiable Safety Floor\)\. *__Regardless of WSAL level, Layer 0 PLC interlocks remain permanently active\. No command from any HDC layer, CI module, or external system may override Layer 0\. This principle has no automotive equivalent—an autonomous car can be manually overridden at any time, but a water system’s safety interlocks must never be disabled because the consequences of constraint violation are physically irreversible \(OS1\)\.

__*Principle W3 \(ODD\-Bounded Autonomy\)\. *__Autonomous operation at WSAL\-3 and above is defined only within a certified ODD\. There is no concept of ‘unconditional’ autonomy; every automation capability is bounded by specific, verified operating conditions\. This principle reflects OS5 \(impossibility of controlled failure testing\): unlike crash tests for vehicles, water systems cannot be intentionally failed for certification, so the ODD must be verified through simulation\-based methods \(xIL\)\.

__4\.2  Level Definitions and Admission Criteria__

Table 2 defines the five WSAL levels with their human role, system capability, required technology, and quantitative admission criteria\.

__Table 2\. WSAL level definitions with quantitative admission criteria__

__Level__

__Name__

__Human Role__

__System Capability__

__Technology__  
__Required__

__Admission__  
__Criteria__

__ODD__  
__Coverage__

WSAL\-1

Remote  
Monitoring

All decisions  
manual; full\-time  
presence

Data acquisition,  
display, alarm

SCADA

SCADA uptime  
≥99\.5%;  
alarm response  
≤30 min

N/A

WSAL\-2

Assisted  
Control

Confirms all  
commands; handles  
all transitions

HDC provides  
recommendations;  
operator approves

SCADA \+  
HDC  
\(L0–L1\)

MiL verified;  
RMS deviation  
≤30% vs\. manual;  
zero L0 violations

Typical  
scenarios  
only

WSAL\-3

Conditional  
Autonomy

Monitors ODD  
boundaries;  
intervenes at  
approach

Autonomous within  
certified ODD;  
automatic fallback

SCADA \+  
HDC \+  
xIL cert\.

SiL\+HiL verified;  
operator interv\.  
<5% of cycles  
within ODD;  
MRC tested

Certified  
typical \+  
single\-  
failure

WSAL\-4

High  
Autonomy

Strategic  
oversight;  
rare interv\.

MAS handles most  
scenarios via CI  
reasoning

SCADA \+  
MAS  
\(HDC\+CI\)

PiL verified;  
CI correct  
scenario recog\.  
>95%; ODD  
coverage >80%

Broad:  
most  
foreseeable  
conditions

WSAL\-5

Full  
Autonomy

Strategic  
governance  
only

Self\-expanding  
ODD via continuous  
learning

SCADA \+  
MAS  
\(full\)

Continuous  
learning verified;  
ODD self\-  
expansion rate  
>0; regulatory  
approval

All  
foreseeable  
conditions

__4\.3  The Critical WSAL\-2 to WSAL\-3 Transition__

The transition from WSAL\-2 to WSAL\-3 is identified as the most critical near\-term milestone for the global water sector\. At WSAL\-2, the system provides control recommendations but every action requires human confirmation—the operator remains ‘in the loop’ for every control cycle\. At WSAL\-3, the system operates autonomously within its certified ODD and the operator shifts to ‘on the loop’—monitoring boundary conditions and intervening only when the system approaches ODD limits\. This is the ‘letting go’ moment, analogous to the SAE Level 2→Level 3 transition in autonomous driving that has proven to be the most challenging regulatory and engineering barrier\.

For water systems, the WSAL\-2→3 transition requires three specific capabilities that are absent at WSAL\-2\. First, systematic xIL verification: the HDC controller must be validated through progressive Model\-in\-the\-Loop \(MiL\), Software\-in\-the\-Loop \(SiL\), and Hardware\-in\-the\-Loop \(HiL\) testing across all scenarios within the target ODD \(Lei et al\., 2025c\)\. Second, an ODD monitor with demonstrated reliability: the real\-time ODD boundary assessment \(Equation 7\) must achieve false\-positive rates below 1% and false\-negative rates below 0\.1% under verified conditions\. Third, a tested Minimum Risk Condition \(MRC\): the fallback procedure must be demonstrated to maintain system safety for a duration exceeding the worst\-case human response time\.

__*\[Figure 2 about here\]*__

__5  Case Study 1: Shaoping Cascade Hydropower Station__

__5\.1  System Description__

The Shaoping cascade hydropower station is located on the \[River name\] in Sichuan Province, China\. The system comprises \[N\] cascaded reservoirs with a total installed capacity of \[XX\] MW and a combined active storage of \[XX\] million m³\. The primary operational objectives are: \(1\) maximization of power generation revenue subject to real\-time electricity market signals; \(2\) maintenance of reservoir water levels within safety constraints; \(3\) satisfaction of downstream minimum ecological flow requirements; and \(4\) flood routing during wet season\. The system represents a ‘point\-type’ water infrastructure—multiple control nodes concentrated in close spatial proximity with fast hydraulic coupling \(transport delays of minutes between stages\)—contrasting with the ‘line\-type’ topology of the Jiaodong case \(Section 6\)\.

\[Author note: Specific system parameters to be inserted based on project data—number of stages, installed capacity per stage, reservoir storage volumes, typical inflow ranges, gate specifications, existing SCADA configuration\.\]

__5\.2  MAS Implementation__

The MAS architecture was instantiated for the Shaoping cascade as follows\. Each reservoir stage hosts an Edge Agent running Layer 0 safety interlocks \(water level limits, maximum gate opening rates, minimum ecological flow\) and Layer 1 MPC with a reservoir\-scale Integrator internal model: dV\_i/dt = Q\_\{in,i\}\(t\) − Q\_\{out,i\}\(u\_i, h\_i\), where V\_i is storage volume, Q\_\{in,i\} is inflow \(including release from upstream stage\), and Q\_\{out,i\} is the controlled release through turbines and spillways\. A single Area Agent coordinates the cascade, executing Layer 2 DMPC that optimizes total power generation P\_total = Σ\_i η\_i · ρg · Q\_\{turb,i\} · H\_\{net,i\} across all stages subject to cascade coupling constraints\. The Cloud Agent provides Layer 3 planning—weekly\-to\-seasonal reservoir operating schedules based on inflow forecasts and electricity price predictions\.

The ODD for the Shaoping WSAL\-2 implementation was defined as: S\_flow = \[normal season inflow range\], S\_level = \[normal operating pool levels excluding flood reserve\], S\_equip = \[all turbines and gates functional\], S\_env = \[non\-flood season\]\. Operation during flood season, single\-turbine failure scenarios, and extreme low\-inflow conditions were excluded from the initial ODD and managed through manual SCADA control\.

__5\.3  Results and WSAL\-2 Assessment__

\[Author note: Insert quantitative results from Shaoping project data\. Expected structure:\]

Performance comparison between MAS\-assisted \(WSAL\-2\) operation and historical rule\-based SCADA operation under identical hydrological conditions: \(a\) power generation efficiency improvement \(ΔP/%\); \(b\) water level deviation reduction \(RMS in meters\); \(c\) ecological flow compliance rate; \(d\) number of operator interventions per day; \(e\) constraint violation events \(expected: zero under Layer 0 protection\)\.

The operational data from \[time period\] demonstrate that the Shaoping system meets the WSAL\-2 admission criteria \(Table 2\): MiL verification completed for all normal\-season scenarios; RMS water level deviation reduced by \[XX\]% compared to manual operation; zero Layer 0 safety violations during the assessment period\. The operator confirmation requirement—the defining characteristic of WSAL\-2—remained in place throughout, with all MPC\-generated control recommendations reviewed and approved by the dispatch center before execution\.

__*\[Figure 3 about here\]*__

__6  Case Study 2: Jiaodong Inter\-Basin Water Transfer__

__6\.1  System Description__

The Jiaodong inter\-basin water transfer project is a large\-scale water conveyance system in Shandong Province, China, transferring water from the Yellow River and local sources to the eastern Shandong peninsula to serve municipal, industrial, and agricultural demands in cities including Yantai, Weihai, and Qingdao\. The system comprises \[XX\] km of main canals and pipelines, \[XX\] pump stations, \[XX\] regulating reservoirs, and \[XX\] control gates\. The primary operational objectives are: \(1\) reliable delivery of contracted water volumes to multiple demand nodes with heterogeneous priority levels; \(2\) minimization of conveyance losses \(evaporation, seepage, operational spillage\); \(3\) energy\-efficient pump scheduling; and \(4\) equitable allocation during shortage conditions\.

The Jiaodong system represents a ‘line\-type’ water infrastructure: control nodes distributed along a long linear conveyance route with transport delays of hours between major nodes, creating a spatially indexed control problem that is fundamentally different from the point\-type Shaoping cascade\. This topological contrast is deliberately chosen to test the generalizability of the MAS architecture across infrastructure typologies\.

\[Author note: Specific system parameters to be inserted—total length, number of pump stations with capacities, number of regulating reservoirs with storage volumes, canal cross\-section parameters, typical flow ranges, existing SCADA configuration\.\]

__6\.2  MAS Implementation: Multi\-Timescale Integration__

The distinctive feature of the Jiaodong MAS implementation is its multi\-timescale integration spanning four temporal horizons\. Layer 3 \(Cloud Agent\) performs annual water allocation planning using a linear programming model that distributes available water supply \(Yellow River quota \+ local sources\) across demand nodes subject to priority\-weighted shortage rules and minimum guarantee constraints\. This annual plan generates monthly and ten\-day delivery schedules that serve as reference trajectories for Layer 2\.

Layer 2 \(Area Agents, one per major conveyance segment\) translates ten\-day delivery targets into daily gate and pump schedules through a rolling\-horizon DMPC that accounts for conveyance delays, reservoir storage buffering, and energy tariff optimization\. The DMPC formulation minimizes the weighted sum of delivery shortfall, energy cost, and operational losses:

*min Σ\_t Σ\_j \[α\_j\(Q\_\{del,j\}\(t\) \- Q\_\{target,j\}\(t\)\)^2 \+ β · E\_cost\(t\) \+ γ · Q\_loss\(t\)\]     \(10\)*

Layer 1 \(Edge Agents at each gate and pump station\) implements real\-time feedback control at minute\-scale intervals, tracking the water level and flow references generated by Layer 2 while compensating for unmeasured disturbances \(local inflows, demand variations, canal seepage\)\.

This four\-horizon integration—annual→monthly→ten\-day→daily→real\-time—represents a key technical achievement: the planning optimization that determines what water to deliver where is seamlessly connected to the real\-time control that determines how to deliver it, through the MAS agent hierarchy\. In prior practice, planning and operation were disconnected processes executed by different departments using different models and different data systems\.

__6\.3  Results and WSAL\-2 Assessment__

\[Author note: Insert quantitative results from Jiaodong project data\. Expected structure:\]

Performance comparison over \[time period\] between MAS\-assisted \(WSAL\-2\) operation and prior manual SCADA operation: \(a\) water delivery compliance rate \(actual vs\. contracted volumes\); \(b\) conveyance loss reduction \(% of total diverted volume\); \(c\) pump energy efficiency improvement \(kWh/m³ delivered\); \(d\) number of operational spillage events; \(e\) water level stability \(RMS deviation at key nodes\)\.

Multi\-timescale integration metrics: \(f\) consistency between annual plan and actual monthly deliveries; \(g\) response time to demand changes; \(h\) time from plan adjustment \(Layer 3\) to execution \(Layer 1\)\.

The Jiaodong system meets WSAL\-2 admission criteria through a different implementation pathway than Shaoping—emphasizing multi\-timescale planning\-control integration rather than real\-time optimization of a single cascade—yet sharing the identical MAS architectural framework\. This dual\-path convergence at WSAL\-2 provides empirical evidence that the MAS\-WSAL framework accommodates diverse infrastructure typologies\.

__*\[Figure 4 about here\]*__

__7  The WSAL\-2 to WSAL\-3 Transition: X\-in\-the\-Loop Verification Pathway__

Both the Shaoping and Jiaodong systems currently operate at WSAL\-2, where operators confirm every control action\. This section analyzes the specific technical and institutional requirements for advancing to WSAL\-3—conditional autonomy within a certified ODD\.

__7\.1  X\-in\-the\-Loop Verification Framework__

The X\-in\-the\-Loop \(xIL\) framework \(Lei et al\., 2025c\) defines four progressive verification stages, each adding a layer of physical realism to the testing environment\.

Stage 1: Model\-in\-the\-Loop \(MiL\)\. The HDC algorithms are tested against a high\-fidelity hydraulic simulation model \(typically a full Saint\-Venant solver\) with synthetic but realistic disturbance scenarios\. MiL validates algorithmic correctness: does the MPC produce feasible, stabilizing control actions for all scenarios within the target ODD? Both the Shaoping and Jiaodong projects have completed MiL verification for their respective normal\-operation ODDs\.

Stage 2: Software\-in\-the\-Loop \(SiL\)\. The production software code—not a research prototype but the actual embedded software that will execute on field controllers—is tested against the same simulation environment\. SiL catches implementation bugs \(numerical precision, timing issues, communication protocol errors\) that are invisible in MiL\. SiL is the minimum verification stage required for WSAL\-3 certification\.

Stage 3: Hardware\-in\-the\-Loop \(HiL\)\. The physical controller hardware \(PLC, industrial PC\) running production software is connected to real\-time simulation via analog/digital I/O interfaces\. HiL testing validates the hardware\-software\-communication stack under realistic timing constraints, including tests for communication failure, sensor malfunction, and actuator degradation\. For the WSAL\-2→3 transition, HiL must specifically verify: \(a\) that Layer 0 safety interlocks function correctly when upper\-layer communication fails; \(b\) that the MRC procedure executes within the specified coast time; and \(c\) that island\-autonomy mode maintains safety constraints\.

Stage 4: Plant\-in\-the\-Loop \(PiL\)\. A limited section of the real physical system operates under automated control \(WSAL\-3\) while the remainder continues at WSAL\-2 with human confirmation\. PiL is the final validation before full WSAL\-3 deployment, corresponding to the ‘controlled deployment’ phase in automotive autonomy certification\.

__7\.2  Case\-Specific Transition Analysis__

For Shaoping, the WSAL\-2→3 transition is technically closer than for Jiaodong, because the point\-type topology has shorter transport delays \(faster feedback\), simpler hydraulic coupling \(cascade connectivity\), and a well\-defined normal\-operation ODD\. The primary barriers are: \(a\) completion of SiL and HiL testing for the production control software; \(b\) formal specification and testing of the MRC procedure \(what happens if all communication to the cascade dispatch center fails?\); and \(c\) institutional acceptance—regulatory approval for automated reservoir operations without real\-time human confirmation\.

For Jiaodong, the transition is more complex because the line\-type topology introduces longer transport delays \(hours\), larger ODD dimensionality \(more demand nodes, more equipment failure combinations\), and tighter coupling between planning and control layers\. The specific additional requirements are: \(a\) SiL verification must cover not only normal delivery scenarios but also single\-pump\-failure and drought\-allocation scenarios; \(b\) HiL testing must validate the Area Agent coordination mechanism under communication degradation between pump stations; and \(c\) the multi\-timescale integration requires that Layer 3 plan adjustments propagate correctly to Layer 1 under all ODD conditions\.

Table 3 summarizes the xIL verification status and remaining requirements for both cases\.

__Table 3\. xIL verification status and WSAL\-2→3 gap analysis__

__xIL Stage__

__Shaoping Status__

__Jiaodong Status__

__WSAL\-3__  
__Requirement__

__Remaining Gap__

__MiL__

✓ Complete for  
normal\-season ODD

✓ Complete for  
normal\-delivery ODD

All ODD  
scenarios  
verified

Expand to  
single\-failure  
scenarios

__SiL__

Partial: L1 MPC  
code verified

Partial: L1\+L2  
code in testing

Production code  
fully verified  
in simulation

Complete SiL  
for L2 DMPC  
and MRC code

__HiL__

Not started

Not started

Hardware\+comm\.  
stack validated;  
MRC tested

Full HiL  
platform build  
and testing

__PiL__

N/A \(post\-HiL\)

N/A \(post\-HiL\)

Controlled field  
deployment on  
limited section

Full HiL  
must precede

__8  Discussion__

__8\.1  Generalizability of the MAS\-WSAL Framework__

The deliberate selection of two topologically distinct case studies—a point\-type cascade \(Shaoping\) and a line\-type conveyance system \(Jiaodong\)—provides preliminary evidence that the MAS architecture accommodates diverse infrastructure typologies through the same three\-component structure \(HDC \+ ODD \+ CI\), differentiated only by the parameterization of the HDC internal models, the dimensionality of the ODD, and the communication topology of the agent hierarchy\. This is consistent with the structural isomorphism proposition of CHS theory \(Lei et al\., 2025a\), which predicts that all water conveyance systems share the same six\-element control structure\. Extending the framework to additional typologies—urban distribution networks \(pressure management\), flood detention basins \(event\-driven control\), and coupled multi\-source systems \(conjunctive use\)—is a priority for future work\.

__8\.2  Relationship Between Physical AI and Cognitive AI__

The MAS architecture makes an explicit and deliberate allocation of responsibilities between physics\-based computation \(HDC\) and AI\-enhanced reasoning \(CI\)\. At WSAL\-2, CI plays no role—all control is HDC\-based with human confirmation\. At WSAL\-3, CI begins to contribute through ODD monitoring and scenario recognition, but all actions remain within the HDC\-computed feasible set\. The Cognitive AI engine becomes architecturally essential only at WSAL\-4, where it must handle novel scenarios that were not pre\-certified in the ODD\. This graduated introduction mirrors the operational singularity: because water failures are irreversible, AI capabilities must be proven incrementally rather than deployed at once\.

The propose\-validate interaction loop \(Equations 8–9\) is the architectural mechanism that ensures this graduated integration\. It deserves emphasis that this is not merely a ‘check’ that CI outputs are reasonable—it is a hard mathematical feasibility verification\. The HDC engine solves the constrained optimization \(Equations 2–4\) with the CI\-proposed parameters and rejects any proposal that would violate physical constraints\. This architecture provides formal guarantees that no CI error, no matter how subtle, can produce an unsafe actuator command\.

__8\.3  Implications for Water Sector Governance__

WSAL provides a shared vocabulary that can serve multiple governance functions\. For regulators, WSAL levels provide a basis for certification requirements: what verification evidence must a utility provide before operating a section at WSAL\-3? For utilities, WSAL provides a maturity benchmark: where does each subsystem stand, and what investments are needed to advance? For technology providers, WSAL provides interoperability requirements: Edge Agents from different vendors must implement the same Layer 0 safety logic and the same heartbeat protocol to achieve WSAL\-3 certification\. For international standardization bodies \(IAHR, IWA, ISO\), WSAL provides a candidate framework for water automation standards, analogous to SAE J3016 for automotive\.

__8\.4  Limitations__

Several limitations should be acknowledged\. First, both case studies currently operate at WSAL\-2; the WSAL\-3 transition analysis \(Section 7\) is prospective rather than empirical\. Full validation of the WSAL\-3 criteria requires completion of the xIL verification program, which is ongoing\. Second, the quantitative admission criteria in Table 2 are proposed rather than standardized; community discussion and iterative refinement through diverse case studies will be needed before standardization\. Third, the CI component \(Section 3\.3\) is described architecturally but has not been implemented in either case study; the current WSAL\-2 deployments use HDC without CI, consistent with the graduated integration pathway\. Fourth, WSAL\-4 and WSAL\-5 remain aspirational; no empirical data support the proposed criteria for these levels\. Fifth, the economic analysis of WSAL advancement—the cost\-benefit tradeoff of investing in xIL verification infrastructure versus the operational benefits of higher autonomy levels—is not addressed in this paper and constitutes an important direction for future work\.

__9  Conclusions__

This paper has presented two interlocking contributions for advancing water infrastructure from manual SCADA\-based supervision toward autonomous operation\.

First, the Multi\-Agent System \(MAS\) architecture, formally defined as MAS = HDC \+ ODD \+ CI, provides an implementable framework for organizing control intelligence within operational water networks\. Hierarchical Distributed Control \(HDC\) deploys physics\-based MPC across four temporal layers \(safety, regulation, coordination, planning\), with a mathematically guaranteed Layer 0 safety floor that no upper\-layer decision may override\. The Operational Design Domain \(ODD\) transforms the trust question from binary to graduated: automation is certified for specific, verified operating conditions, with automatic fallback to safe modes at ODD boundaries\. Cognitive Intelligence \(CI\) adds scenario\-aware reasoning through a propose\-validate interaction loop that ensures physics\-based safety is never compromised\. The three\-tier agent hierarchy \(Edge–Area–Cloud\) maps these components onto the spatial topology of water networks, with island\-autonomy capabilities at every tier\.

Second, Water Systems Autonomy Levels \(WSAL\) provide a five\-level classification \(WSAL\-1 through WSAL\-5\) with quantitative admission criteria for each level\. Three water\-specific design principles—the bucket principle, the non\-negotiable safety floor, and ODD\-bounded autonomy—distinguish WSAL from SAE J3016 and reflect the operational singularity of water infrastructure\. The WSAL\-2 to WSAL\-3 transition is identified as the critical near\-term milestone, requiring systematic X\-in\-the\-Loop verification to certify ODD boundaries\.

The framework has been validated through two operational case studies spanning distinct infrastructure typologies: the Shaoping cascade hydropower station \(point\-type, real\-time power optimization\) and the Jiaodong inter\-basin water transfer \(line\-type, multi\-timescale planning\-control integration\)\. Both systems demonstrate WSAL\-2 achievement through the same MAS architectural principles, differentiated only by internal model parameterization and agent topology—providing empirical evidence that a single architectural framework can accommodate diverse water infrastructure types\. The xIL verification gap analysis \(Table 3\) provides a concrete roadmap for the WSAL\-2→3 transition at both sites\.

The MAS\-WSAL framework is offered as a foundation for community standardization\. Just as SAE J3016 transformed the automotive industry’s approach to autonomous driving by providing a shared vocabulary, WSAL aims to provide the water community with a common framework for planning, benchmarking, and advancing the operational intelligence of water infrastructure worldwide\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\. The authors thank the Shaoping hydropower station and the Jiaodong Water Transfer Authority for providing operational data and facilitating field implementation\. The authors also thank the members of the IAHR Working Group on Water System Operations for discussions that shaped the WSAL framework\.

__References__

Cantoni, M\., Weyer, E\., Li, Y\., Ooi, S\. K\., Mareels, I\., & Ryan, M\. \(2007\)\. Control of large\-scale irrigation networks\. Proceedings of the IEEE, 95\(1\), 75–91\. https://doi\.org/10\.1109/JPROC\.2006\.887289

Castelletti, A\., Ficchì, A\., Cominola, A\., Segovia, P\., Giuliani, M\., Wu, W\., Lucia, S\., Ocampo\-Martinez, C\., De Schutter, B\., & Maestre, J\. M\. \(2023\)\. Model Predictive Control of water resources systems: A review and research agenda\. Annual Reviews in Control, 55, 442–465\. https://doi\.org/10\.1016/j\.arcontrol\.2023\.03\.013

Creaco, E\., Campisano, A\., Fontana, N\., Marini, G\., Page, P\. R\., & Walski, T\. \(2019\)\. Real time control of water distribution networks: A state\-of\-the\-art review\. Water Research, 161, 517–530\. https://doi\.org/10\.1016/j\.watres\.2019\.06\.025

Giuliani, M\., Lamontagne, J\. R\., Reed, P\. M\., & Castelletti, A\. \(2021\)\. A state\-of\-the\-art review of optimal reservoir control for managing conflicting demands in a changing world\. Water Resources Research, 57\(12\), e2021WR029927\. https://doi\.org/10\.1029/2021WR029927

ISO\. \(2018\)\. ISO 26262: Road vehicles—Functional safety\. International Organization for Standardization\.

ISO\. \(2022\)\. ISO 21448:2022 Road vehicles—Safety of the intended functionality \(SOTIF\)\.

Kundur, P\. \(1994\)\. Power system stability and control\. McGraw\-Hill\.

Lei, X\. \(2025a\)\. Cybernetics of hydro systems: A unified control\-theoretic framework for water network operations\. Manuscript submitted to Water Resources Research\.

Lei, X\., Long, Y\., Xu, H\., et al\. \(2025a\)\. Cybernetics of hydro systems: Background, technical framework and research paradigm \[水系统控制论：提出背景、技术框架与研究范式\]\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 761–769\. https://doi\.org/10\.13476/j\.cnki\.nsbdqk\.2025\.0077

Lei, X\., Su, C\., Long, Y\., et al\. \(2025b\)\. Architecture and key technologies of next\-generation autonomous intelligent water networks \[基于无人驾驶理念的下一代自主运行智慧水网架构与关键技术\]\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 778–786\. https://doi\.org/10\.13476/j\.cnki\.nsbdqk\.2025\.0079

Lei, X\., Zhang, Z\., Su, C\., et al\. \(2025c\)\. In\-the\-loop testing system for autonomous intelligent water networks \[自主运行智能水网的在环测试体系\]\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 787–793\. https://doi\.org/10\.13476/j\.cnki\.nsbdqk\.2025\.0080

Lei, X\., Xu, H\., He, Z\., et al\. \(2025d\)\. Disciplinary perspectives on water resources systems analysis: From static water balance to dynamic control \[水资源系统分析学科展望：从静态平衡到动态控制\]\. South\-to\-North Water Transfers and Water Science & Technology, 23\(4\), 770–777\. https://doi\.org/10\.13476/j\.cnki\.nsbdqk\.2025\.0078

Litrico, X\., & Fromion, V\. \(2004\)\. Simplified modeling of irrigation canals for controller design\. Journal of Irrigation and Drainage Engineering, 130\(5\), 373–383\. https://doi\.org/10\.1061/\(ASCE\)0733\-9437\(2004\)130:5\(373\)

Litrico, X\., & Fromion, V\. \(2009\)\. Modeling and control of hydrosystems\. Springer\. https://doi\.org/10\.1007/978\-1\-84882\-624\-3

Maestre, J\. M\., & Negenborn, R\. R\. \(Eds\.\)\. \(2014\)\. Distributed model predictive control made easy\. Springer\. https://doi\.org/10\.1007/978\-94\-007\-7006\-5

Malaterre, P\.\-O\., Rogers, D\. C\., & Schuurmans, J\. \(1998\)\. Classification of canal control algorithms\. Journal of Irrigation and Drainage Engineering, 124\(1\), 3–10\. https://doi\.org/10\.1061/\(ASCE\)0733\-9437\(1998\)124:1\(3\)

Mareels, I\. M\. Y\., Weyer, E\., Ooi, S\. K\., Cantoni, M\., Li, Y\., & Nair, G\. \(2005\)\. Systems engineering for irrigation systems\. Annual Reviews in Control, 29\(2\), 191–204\. https://doi\.org/10\.1016/j\.arcontrol\.2005\.08\.001

Negenborn, R\. R\., van Overloop, P\. J\., Keviczky, T\., & De Schutter, B\. \(2009\)\. Distributed model predictive control of irrigation canals\. Networks and Heterogeneous Media, 4\(2\), 359–380\. https://doi\.org/10\.3934/nhm\.2009\.4\.359

RTCA\. \(2011\)\. DO\-178C: Software considerations in airborne systems and equipment certification\.

SAE International\. \(2021\)\. J3016: Taxonomy and definitions for terms related to driving automation systems\.

Savic, D\. \(2022\)\. Digital water developments and lessons learned from automation in the car and aircraft industries\. Engineering, 9\(2\), 35–41\. https://doi\.org/10\.1016/j\.eng\.2021\.05\.013

Schuurmans, J\. \(1997\)\. Control of water levels in open channels \(Doctoral dissertation\)\. Delft University of Technology\.

Schuurmans, J\., Bosgra, O\. H\., & Brouwer, R\. \(1995\)\. Open\-channel flow model approximation for controller design\. Applied Mathematical Modelling, 19\(9\), 525–530\. https://doi\.org/10\.1016/0307\-904X\(95\)00053\-M

UNESCO\. \(2024\)\. The United Nations World Water Development Report 2024\. UNESCO\.

van Overloop, P\. J\. \(2006\)\. Model predictive control on open water systems \(Doctoral dissertation\)\. Delft University of Technology\.

Wang, F\.\-Y\. \(2010\)\. The emergence of intelligent enterprises: From CPS to CPSS\. IEEE Intelligent Systems, 25\(4\), 85–88\. https://doi\.org/10\.1109/MIS\.2010\.104

Ye, L\., Wei, J\., Lei, X\., et al\. \(2023\)\. Model predictive control for real\-time optimal operation of cascade hydropower stations\. Journal of Water Resources Planning and Management, 149\(6\), 04023020\. https://doi\.org/10\.1061/JWRMD5\.WRENG\-5869

__Figure Captions__

__Figure 1\. __The MAS architecture for autonomous water networks: MAS = HDC \+ ODD \+ CI\. Left: three\-component architecture showing HDC \(Physical AI engine, four layers\), ODD \(safety certification framework with certified and uncertified regions\), and CI \(Cognitive AI engine with propose\-validate loop\)\. Right: three\-tier agent hierarchy \(Edge–Area–Cloud\) with communication topology and island\-autonomy capabilities\.

__Figure 2\. __Water Systems Autonomy Levels \(WSAL\-1 through WSAL\-5\) with quantitative admission criteria and the critical WSAL\-2→3 transition\. The staircase visualization shows increasing autonomy from left to right, with the xIL verification requirements \(MiL, SiL, HiL, PiL\) mapped to each transition\. The Layer 0 safety floor is shown as a constant base spanning all levels\.

__Figure 3\. __Shaoping cascade hydropower case study: \(a\) system schematic showing \[N\]\-stage cascade with Edge Agents at each stage and Area Agent for cascade coordination; \(b\) MPC performance comparison: water level deviation timeseries under WSAL\-2 MAS\-assisted control vs\. historical rule\-based SCADA; \(c\) power generation efficiency comparison; \(d\) ODD boundary visualization showing certified operating region\.

__Figure 4\. __Jiaodong inter\-basin transfer case study: \(a\) system schematic showing linear conveyance topology with Edge Agents at gates/pumps, Area Agents per segment, and Cloud Agent for system\-wide planning; \(b\) multi\-timescale integration: annual plan → monthly schedule → ten\-day targets → daily gate operations → real\-time control, showing seamless cascading through the MAS agent hierarchy; \(c\) water delivery compliance and loss reduction metrics under WSAL\-2 operation\.

