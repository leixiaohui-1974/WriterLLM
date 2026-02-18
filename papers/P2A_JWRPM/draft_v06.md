*Manuscript submitted to Journal of Water Resources Planning and Management*

__From SCADA to Autonomy: A Multi\-Agent System Architecture__

__and Water Systems Autonomy Level Classification__

__with Applications to Cascade Hydropower and Inter\-Basin Transfer__

__Xiaohui Lei__1,2\*, __Lei Zhang__1, __Shangjun Ye__2, __Chen Ji__3, __Xiaowei Liu__2, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research \(IWHR\), Beijing 100038, China

3 College of Water Resource & Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei \(lxh@iwhr\.com\)

__Abstract__

Water conveyance infrastructure worldwide operates at manual\-supervisory levels, decades behind the automation maturity of comparable infrastructure domains\. This paper addresses the resulting architectural gap through two contributions\. First, we formalize a Multi\-Agent System \(MAS\) architecture defined as MAS = HDC \+ ODD \+ CI: Hierarchical Distributed Control \(HDC\) as the physics\-based engine across four temporal layers, the Operational Design Domain \(ODD\) as the safety certification framework, and Cognitive Intelligence \(CI\) as the scenario\-aware decision layer, deployed through a three\-tier Edge–Area–Cloud agent hierarchy\. Second, we propose Water Systems Autonomy Levels \(WSAL\), a five\-level classification with quantitative admission criteria incorporating three water\-specific design principles\. The HDC and ODD components are MiL\-validated through two topologically distinct case studies at WSAL\-2: the Shaping cascade hydropower station \(Dadu River, 360 MW; 2–3% efficiency gain, 40% water level deviation reduction\) and the Jiaodong inter\-basin transfer \(500\+ km, 13 pump stations; 5–8% energy reduction\)\. For both cases, we analyze the WSAL\-2→3 transition barriers and propose an X\-in\-the\-Loop verification roadmap\. The MAS\-WSAL framework provides a practical foundation for planning, benchmarking, and advancing water infrastructure automation worldwide\.

__Keywords: __autonomous water networks; multi\-agent systems; hierarchical distributed control; operational design domain; water systems autonomy levels; cascade hydropower; inter\-basin transfer

__1  Introduction__

The global stock of water conveyance infrastructure—canals, pipelines, reservoirs, pump stations, and associated control structures—represents a cumulative investment measured in trillions of dollars \(UNESCO, 2024\)\. These systems serve functions essential to human welfare: irrigation water delivery, urban water supply, hydroelectric power generation, flood management, and environmental flow maintenance\. Yet a persistent asymmetry characterizes the sector: while the science of designing and building water infrastructure is mature, the science of operating it in real time remains at an early stage\. Cross\-sector benchmarking reveals that operational autonomy of water conveyance systems worldwide remains at levels equivalent to manual driving with minimal driver assistance—decades behind the automation maturity achieved in automotive \(SAE Level 2–3\), commercial aviation \(Level 4–5 in cruise\), and power systems \(fully automated frequency regulation\) \(Lei, 2025a; Savic, 2022\)\.

Climate non\-stationarity further intensifies this urgency: as hydrological regimes shift beyond historical envelopes \(Milly et al\., 2008\), the experience\-based rules that currently govern water operations become increasingly unreliable, strengthening the case for model\-based autonomous control that can adapt to conditions outside historical precedent\.

Two recent developments have brought this gap into sharp focus\. First, advances in sensing, communication, and computing have made real\-time automated control technically feasible for water networks—yet adoption remains limited to isolated pilot projects rather than system\-wide deployment\. Second, the Cybernetics of Hydro Systems \(CHS\) framework \(Lei, 2025a; Lei et al\., 2025a\) has provided a unified theoretical foundation showing that all water conveyance and distribution systems share a structurally isomorphic six\-element control architecture and can be governed by a common set of eight principles organized into dual tetrads\. CHS establishes what water system control should achieve; what remains unaddressed is how—through what specific system architecture, safety certification framework, and intelligence hierarchy—water networks should transition from their current SCADA\-based supervisory mode to progressively higher levels of autonomous operation\.

This architectural gap has practical consequences\. Without a shared framework for describing and measuring automation maturity, water utilities, government agencies, and technology providers lack a common language for procurement, regulation, and investment planning\. Without a formal safety certification concept, operators face a binary choice between full manual control and opaque ‘smart water’ systems whose failure modes are poorly understood\. Without a layered intelligence architecture, the integration of physics\-based control and artificial intelligence remains ad hoc, with no principled allocation of responsibilities between algorithmic and human decision\-making\.

This paper addresses the architectural gap through two interlocking contributions\. The first contribution is the Multi\-Agent System \(MAS\) architecture for autonomous water networks, which organizes control intelligence into three components: Hierarchical Distributed Control \(HDC\) as the physics\-based engine, the Operational Design Domain \(ODD\) as the safety certification framework, and Cognitive Intelligence \(CI\) as the scenario\-aware decision layer\. The second contribution is Water Systems Autonomy Levels \(WSAL\), a five\-level classification with quantitative admission criteria that provides the shared vocabulary for planning, measuring, and advancing water network automation\.

Critically, both contributions are validated through operational engineering case studies rather than purely theoretical constructs\. The Shaping cascade hydropower station \(Sichuan, China\) and the Jiaodong inter\-basin water transfer project \(Shandong, China\) represent two fundamentally different water infrastructure typologies—point\-based multi\-reservoir cascade control and linear long\-distance conveyance control, respectively—yet both are shown to achieve WSAL\-2 \(Assisted Control\) through implementations that share the common MAS architectural principles\. This dual\-case validation demonstrates the generalizability of the framework across infrastructure types\.

The remainder of the paper is structured as follows\. Section 2 reviews the state of the art in water system automation and identifies the specific gaps addressed\. Section 3 formalizes the MAS architecture\. Section 4 presents the WSAL classification with quantitative criteria\. Section 5 and Section 6 present the Shaping and Jiaodong case studies, respectively\. Section 7 analyzes the WSAL\-2→3 transition pathway including X\-in\-the\-Loop verification requirements\. Section 8 discusses implications and limitations\. Section 9 concludes\.

__2  State of the Art and Research Gaps__

__2\.1  Water System Automation: Current Practice__

The dominant operational paradigm for water conveyance systems is Supervisory Control and Data Acquisition \(SCADA\)—a framework originally developed in the 1960s for industrial process monitoring that has been progressively adapted to water infrastructure\. SCADA provides real\-time data acquisition, alarm management, and remote manual control, but its decision architecture is fundamentally human\-centered: operators observe system state through SCADA displays and issue control commands based on experience, operating rules, and predefined schedules \(Savic, 2022\)\. The automation content is limited to low\-level interlocks \(e\.g\., closing a gate when water level exceeds a threshold\) and scheduled operations \(e\.g\., pump cycling\)\. Multi\-objective optimization, disturbance rejection, and inter\-subsystem coordination remain manual processes\.

Advanced control methods—particularly Model Predictive Control \(MPC\)—have been extensively developed in the research literature for water systems\. Malaterre et al\. \(1998\) provided an early classification of canal control algorithms\. Schuurmans \(1997\) and van Overloop \(2006\) developed MPC frameworks for open\-channel systems\. Negenborn et al\. \(2009\) introduced distributed MPC for irrigation canal networks\. Castelletti et al\. \(2023\) presented a comprehensive review of MPC applications across water resource systems\. However, a systematic review of field deployments reveals that the gap between laboratory demonstrations and operational adoption remains wide\. The few operational MPC implementations—such as those on Australian irrigation systems \(Mareels et al\., 2005; Cantoni et al\., 2007\) and select European canal systems \(Litrico & Fromion, 2009\)—remain confined to individual subsystems or pilot reaches, without integration into a coherent system\-wide architecture\.

__2\.2  Lessons from Cross\-Sector Automation__

Other infrastructure domains have successfully navigated the transition from manual to autonomous operation by developing three elements that the water sector currently lacks\. First, a shared autonomy classification: SAE J3016 \(SAE International, 2021\) defines six levels \(L0–L5\) of driving automation, providing a common vocabulary that aligns regulatory frameworks, technology development, and public communication\. The power sector uses a similar progression from manual to fully automatic generation control \(Kundur, 1994\)\. Second, a formal safety certification concept: the Operational Design Domain \(ODD\) in automotive defines the specific conditions under which automation is certified to operate, transforming the trust question from binary \(‘automate or not’\) to graduated \(‘automate under these specific conditions’\)\. ISO 26262 \(functional safety\) and ISO 21448 \(SOTIF—safety of the intended functionality\) provide certification standards\. Aerospace uses DO\-178C for airborne software certification \(RTCA, 2011\)\. Third, a layered intelligence architecture: autonomous vehicles integrate perception \(sensors\), prediction \(AI models\), planning \(optimization\), and control \(actuators\) within a principled architecture that allocates responsibilities across computational layers\.

This pattern of graduated autonomy classification is not unique to automotive\. The International Maritime Organization \(IMO\) has defined four degrees of autonomy for Maritime Autonomous Surface Ships \(MASS\)\. The power sector's progression from manual to fully automatic generation control follows a similar trajectory \(Kundur, 1994\)\. Smart manufacturing \(Industry 4\.0\) uses the ISA\-95 automation pyramid with increasing levels of autonomous decision\-making \(McArthur et al\., 2007\)\. Water infrastructure stands out as one of the few critical infrastructure domains that has not yet developed a formal autonomy classification or certification framework\.

The water sector possesses none of these three elements in operational form\. Several authors have noted the analogy between water and automotive automation\. Savic \(2022\) compared digital water developments with automation lessons from the car and aircraft industries\. Lei et al\. \(2025b\) proposed a preliminary intelligence level framework inspired by SAE J3016\. However, no prior work has formalized the complete triad—architecture, safety certification, and autonomy classification—as an integrated engineering framework validated through operational case studies\.

__2\.3  Research Gaps Addressed__

__Relationship to Prior Work\.__ The present paper builds upon but is distinct from the authors' prior publications within the CHS framework\. Lei \(2025a\) provides the mathematical foundations: unified transfer function families for open\-channel and pressurized systems, the model–layer correspondence theorem, and eight governing principles organized in dual tetrads\. Lei et al\. \(2025b\) introduces the preliminary intelligence\-level concept at a conceptual level without formal definitions or quantitative criteria\. Lei et al\. \(2025a, Chinese\) presents the CHS paradigm at a disciplinary overview level for a Chinese\-language audience\. The present paper's distinct contributions are: \(1\) the formal MAS architecture specification with explicit agent hierarchy, communication protocols, ODD mathematical definition \(Definition 1\), and cybersecurity requirements—none of which appears in the theoretical papers; \(2\) the WSAL classification with quantitative admission criteria \(Table 2\) and three water\-specific design principles; and \(3\) the first operational case study validation at WSAL\-2 with quantitative performance data from two topologically distinct systems\.

This paper addresses three specific gaps\. Gap 1 \(Architecture\): the water sector lacks a formal Multi\-Agent System architecture that specifies how physics\-based control, safety certification, and cognitive intelligence should be organized across spatial and temporal scales within an operational water network\. Gap 2 \(Classification\): the sector lacks a quantitative autonomy level classification with measurable admission criteria for each level, which is prerequisite for regulatory standardization and investment planning\. Gap 3 \(Validation\): existing proposals for water automation frameworks remain theoretical; what is needed is empirical demonstration through diverse operational case studies showing that a single architectural framework can accommodate fundamentally different infrastructure typologies\.

__3  The Multi\-Agent System Architecture__

This section presents the formal MAS architecture for autonomous water networks, defined as MAS = HDC \+ ODD \+ CI\. Each component is described in a dedicated subsection, followed by the agent hierarchy that integrates them\.

__3\.1  Hierarchical Distributed Control: The Physical AI Engine__

The Cybernetics of Hydro Systems \(CHS\) framework identifies a five\-level model–control hierarchy ranging from the full linearized Saint\-Venant equations \(Level 5\) through the Integrator\-Delay\-Zero model \(Level 4\) to steady\-state mass balance \(Level 1\), with a model–layer correspondence theorem linking each model level to the control architecture layer where its approximation errors are acceptable \(Lei et al\., 2025a\)\. Hierarchical Distributed Control \(HDC\) operationalizes this correspondence through four concurrent control layers\.

Layer 0 \(Safety Floor\) implements hard constraint enforcement through programmable logic controllers \(PLCs\) at millisecond cycle times\. Control logic consists exclusively of deterministic threshold comparisons: if water level h exceeds the maximum h\_max, the emergency gate opens unconditionally; if downstream flow Q\_out falls below ecological minimum Q\_eco, upstream extraction is curtailed\. No optimization, no model, no communication dependency—only Boolean logic that executes independently of all upper layers\. Layer 0 controllers shall be certified to Safety Integrity Level \(SIL\) 2 or SIL 3 per IEC 61508, commensurate with the consequence severity of the controlled structure\. The Layer 0 design rule is the veto principle:

*Veto Principle:  ∀ command u from Layer k \(k ≥ 1\): if L0\_check\(u\) = UNSAFE, then u is blocked\.     \(1\)*

This principle reflects the operational singularity of water systems: failure irreversibility \(OS1\) demands that no algorithmic decision—however sophisticated—can override physical safety interlocks\. The Layer 0 safety floor remains active at all WSAL levels, including WSAL\-5\.

Layer 1 \(Real\-time Regulation\) deploys feedback control with physics\-based internal models at sampling intervals of seconds to minutes\. The canonical controller is MPC with an IDZ \(Integrator\-Delay\-Zero\) or ID \(Integrator\-Delay\) internal model, solving at each time step:

*min\_\{u\(k\),\.\.\.,u\(k\+N\-1\)\} Σ\_\{j=0\}^\{N\-1\} \[α\_y\(y\(k\+j\) \- y\_ref\)^2 \+ α\_u\(Δu\(k\+j\)\)^2\]     \(2\)*

*subject to:  x\(k\+j\+1\) = Ax\(k\+j\) \+ Bu\(k\+j\) \+ Ed\(k\+j\),  y\(k\+j\) = Cx\(k\+j\)     \(3\)*

*h\_min ≤ y\(k\+j\) ≤ h\_max,   u\_min ≤ u\(k\+j\) ≤ u\_max,   |Δu\(k\+j\)| ≤ Δu\_max     \(4\)*

where y is water level \(or pressure head\), u is actuator position \(gate opening, pump speed, valve setting\), d is the disturbance estimate \(inflow forecast, demand prediction\), N is the prediction horizon, and α\_y, α\_u are weighting parameters\. The state\-space matrices \(A, B, C, E\) are derived from the IDZ transfer function G\(s\) = \(1 \+ τ\_m·s\)·e^\(−τ\_d·s\) / \(A\_s·s\) through second\-order Padé approximation of the delay term and zero\-order hold discretization \(Litrico & Fromion, 2004; Schuurmans et al\., 1995\)\. Layer 1 controllers operate independently for each control node \(gate, pump, valve\), using only local state and nearest\-neighbor boundary conditions\.

Layer 2 \(Coordination\) employs distributed MPC \(DMPC\) at minute\-to\-hour horizons\. While Layer 1 controllers optimize each subsystem independently, Layer 2 resolves inter\-subsystem conflicts by iteratively exchanging boundary information between neighboring agents\. For a series of N\_p canal pools or reservoir stages \(applicable to both the cascade\-serial topology of Shaping and the canal\-serial topology of Jiaodong\), each agent i solves a local MPC problem that incorporates coupling constraints with upstream agent i−1 and downstream agent i\+1:

*u\_i^\{\(k\+1\)\} = argmin J\_i\(u\_i\) \+ λ\_i^T g\_i\(u\_i, u\_\{i\-1\}^\{\(k\)\}, u\_\{i\+1\}^\{\(k\)\}\)     \(5\)*

where λ\_i are Lagrange multipliers updated through neighbor\-to\-neighbor communication at each DMPC iteration, g\_i captures the coupling constraints \(continuity of flow, shared storage targets\), and superscript \(k\) denotes the iteration count\. Convergence to a feasible coordinated solution is guaranteed under standard convexity and weak\-coupling assumptions \(Negenborn et al\., 2009; Maestre & Negenborn, 2014\); for systems with strong hydraulic coupling or non\-convex objectives \(e\.g\., discrete pump switching\), convergence is not guaranteed and may require fallback to centralized solvers or operator intervention\. Layer 2 coordination enables system\-wide objectives—such as minimizing total energy consumption across a cascade, or balancing water levels across multiple reaches—without requiring centralized computation\.

Layer 3 \(Planning\) performs nested optimization over day\-to\-year horizons\. At this temporal scope, the appropriate internal models are pure Integrator \(Level 2\) or Steady\-State \(Level 1\) representations, where dynamic transients are negligible relative to planning horizons\. Layer 3 translates high\-level objectives—seasonal water allocation targets, annual energy generation goals, long\-term reservoir rule curves—into reference trajectories and constraint sets for Layer 2 and Layer 1\. The planning\-to\-control interface is formalized as:

*Layer 3 → Layer 2 protocol: \{y\_ref\(t\), u\_bounds\(t\), d\_forecast\(t\)\} for t ∈ \[t\_now, t\_now \+ T\_plan\]     \(P1\)*

__Hierarchical Consistency and Optimality\.__ The four\-layer decomposition introduces suboptimality relative to a hypothetical monolithic optimizer spanning all timescales—this is the standard scalability\-optimality tradeoff in hierarchical control \(Mayne et al\., 2000\)\. The tradeoff is managed through time\-scale separation: Layer 3 operates at horizons \(days to years\) where transient dynamics are negligible, so its steady\-state references are dynamically achievable by Layer 1\. If a Layer 3 reference is temporarily infeasible at Layer 1 \(e\.g\., due to a rapid demand change\), the Layer 1 MPC handles this through constraint softening, and the discrepancy propagates upward through the Layer 2 DMPC update cycle\. In practice, the receding\-horizon MPC implementation at Layer 1, combined with the Layer 0 safety floor, provides robust constraint satisfaction even without formal terminal cost or terminal constraint conditions; Layer 0 catches any constraint violation arising from model mismatch or MPC infeasibility\.

The four\-layer HDC architecture constitutes what we term the Physical AI engine: every control decision at every layer is computed from mechanistic models grounded in conservation laws \(mass, momentum, energy\), with constraint satisfaction ensured through a dual\-layer guarantee—the MPC optimization enforces constraints under the assumption that the IDZ/ID internal model accurately represents the controlled subsystem within the certified ODD, while the Layer 0 safety floor provides a model\-independent hard backup that catches any violation arising from model mismatch, disturbance exceedance, or MPC solver failure\. No learned correlation substitutes for physical law in safety\-critical control paths\.

__3\.2  Operational Design Domain: The Safety Certification Framework__

The Operational Design Domain \(ODD\) concept, adapted from automotive autonomous driving \(SAE International, 2021; ISO, 2022\), addresses the trust barrier that has limited water automation adoption\. An ODD for a water network segment is defined as a bounded region in a multi\-dimensional operating space:

__*Definition 1 \(ODD for Water Systems\)\. *__The Operational Design Domain of a water network control subsystem is the Cartesian product ODD = S\_flow × S\_level × S\_demand × S\_equip × S\_env × S\_comm, where S\_flow = \[Q\_min, Q\_max\] is the certified flow range, S\_level = \[h\_min, h\_max\] is the certified water level range, S\_demand enumerates the certified demand/disturbance scenarios \(e\.g\., normal delivery, peak demand, drought allocation\), S\_equip enumerates equipment status conditions \(e\.g\., all actuators functional, single actuator failure, dual redundancy degraded\), S\_env enumerates environmental conditions \(e\.g\., normal weather, storm, ice, extreme temperature\), and S\_comm specifies communication link requirements \(e\.g\., full connectivity, single link failure, island mode\)\.

Within the certified ODD, the HDC controller has been verified—through the X\-in\-the\-Loop \(xIL\) testing framework \(Lei et al\., 2025c\)—to maintain all constraints \(Equation 4\) while achieving performance targets\. Outside the ODD boundary, control authority reverts to human operators or to a predefined safe degradation mode\. The ODD boundary is monitored in real time by a dedicated ODD Monitor module that evaluates:

*ODD\_status\(t\) = ⋀\_\{d ∈ \{flow, level, demand, equip, env, comm\}\} \[state\_d\(t\) ∈ S\_d\]     \(6\)*

To prevent oscillation between in\-ODD and out\-of\-ODD states near boundaries, the ODD Monitor implements a hysteresis band: exit is triggered when any dimension exceeds S\_d by a margin δ\_out, and re\-entry is permitted only when all dimensions return within S\_d by a tighter margin δ\_in < δ\_out\. Typical values are δ\_out = 5% of the range and δ\_in = 2%\.

When ODD\_status transitions from TRUE to FALSE, the system executes a Minimum Risk Condition \(MRC\)—the water systems equivalent of 'pulling over to the side of the road' in automotive autonomy\. Formally, the MRC is defined as transition to a predefined safe steady\-state that is reachable from any state within the ODD boundary within a coast time τ\_coast\. The coast time is estimated as:

*τ\_coast ≈ L / c₀ \+ T\_operator     \(7\)*

where L is the characteristic hydraulic length \(longest propagation path in the controlled subsystem\), c₀ is the relevant wave celerity, and T\_operator is the expected human response time\. For the Shaping cascade \(L ≈ 5 km, c₀ ≈ 20 m/s as pressure wave in penstocks\), τ\_coast ≈ 4 min \+ T\_operator\. For the Jiaodong conveyance \(L ≈ 500 km\), c₀ is taken as the kinematic wave speed \(≈ 1 m/s\) rather than the dynamic gravity wave speed \(≈ 4–5 m/s for typical canal depth\), because MRC planning must account for the slower disturbance propagation that governs operational response; this gives τ\_coast ≈ 6–8 hours \+ T\_operator\. The MRC procedure is case\-specific: for Shaping, ramp turbines to minimum load, open spillway gates to maintain headpond levels, and alert the dispatch center; for Jiaodong, cease upstream pumping, maintain downstream gates at current positions to prevent canal overtopping, and activate emergency storage reservoirs as buffers\. The MRC design must account for the operational singularity: unlike a car that can safely stop, a water system's mass in transit continues moving, so the MRC must ensure that the frozen state remains within safety constraints for a duration exceeding τ\_coast\.

__3\.3  Cognitive Intelligence: The Scenario\-Aware Decision Layer__

HDC computes accurately within a given scenario; ODD defines which scenarios are certified\. Cognitive Intelligence \(CI\) addresses what happens between scenarios: recognizing the current operational situation, selecting the appropriate objective function and constraint set, and reasoning about whether conditions are approaching ODD boundaries\. CI serves as the Cognitive AI engine of the architecture—complementary to the Physical AI engine of HDC\.

The CI module performs four functions\. First, scenario recognition: classifying the current operating state into one of the predefined scenario categories \(normal operation, drought, flood risk, equipment degradation, emergency\) using a combination of rule\-based logic, statistical classifiers, and—where appropriate—large language model reasoning for unstructured information integration \(weather advisories, operator notes, regulatory communications\)\. Second, goal assembly: translating the recognized scenario into a specific objective function and constraint set for HDC, including reference trajectories, weighting parameters, and constraint bounds\. Third, ODD boundary prediction: estimating the time\-to\-boundary for each ODD dimension, providing early warning when operating conditions are trending toward ODD limits\. Fourth, explainability: generating human\-readable explanations of automated decisions for operator oversight and regulatory compliance\.

The critical architectural rule governing CI is the propose\-validate interaction loop:

*CI proposes: \{θ\_new, y\_ref\_new, C\_new\} → HDC validates: feasibility\(A, B, θ\_new, C\_new\)     \(8\)*

*if feasible: execute;   if infeasible: CI revises or escalates to human operator     \(9\)*

where θ\_new is a proposed parameter set, y\_ref\_new is a proposed reference trajectory, and C\_new is a proposed constraint set\. Feasibility is defined operationally: HDC solves the constrained optimization \(Equations 2–4\) with the CI\-proposed parameters over a verification horizon N\_v\. The proposal is accepted if and only if the optimizer returns a feasible solution satisfying all hard constraints \(Equation 4\); computational tractability is maintained because the verification reuses the operational MPC solver\. This loop ensures that no CI reasoning error—however sophisticated the underlying AI model—can bypass the physics\-based feasibility checking of HDC\. The propose\-validate architecture represents a design choice grounded in the operational singularity \(OS1\): because water system failures are irreversible, the Cognitive AI engine must never have unilateral authority over actuators\.

__3\.4  The Agent Hierarchy: Edge–Area–Cloud__

__3\.4\.1  Cybersecurity Architecture__

The distributed nature of the MAS architecture—Edge Agents communicating with Area Agents via heartbeat protocols, and Area Agents communicating with Cloud Agents—creates a networked attack surface that must be explicitly addressed\. The cybersecurity architecture follows the IEC 62443 zone\-conduit model for industrial automation and control systems \(IEC, 2018\)\. Three requirements are mandatory\. First, IT/OT segmentation: the operational technology \(OT\) network carrying HDC control signals is physically or logically separated from the information technology \(IT\) network carrying CI and Cloud Agent traffic, with unidirectional gateways at zone boundaries\. Second, Layer 0 air\-gap: the safety PLC interlocks at Layer 0 are hardwired and air\-gapped from all networked layers; no software update, no remote command, and no network intrusion can modify Layer 0 logic without physical on\-site access\. Third, authenticated communication: all agent\-to\-agent messages use authenticated and encrypted channels with message integrity verification; a compromised agent is detected through heartbeat anomaly and isolated by its neighbors, which revert to island\-autonomy mode\. Cybersecurity certification is positioned as a mandatory prerequisite for WSAL\-3, because autonomous operation without human confirmation requires assurance that the control commands originate from legitimate agents\.

__3\.4\.2  Agent Hierarchy__

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
MRC tested;
IEC 62443 compliant

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

For water systems, the WSAL\-2→3 transition requires three specific capabilities that are absent at WSAL\-2\. First, systematic xIL verification: the HDC controller must be validated through progressive Model\-in\-the\-Loop \(MiL\), Software\-in\-the\-Loop \(SiL\), and Hardware\-in\-the\-Loop \(HiL\) testing across all scenarios within the target ODD \(Lei et al\., 2025c\)\. Second, an ODD monitor with demonstrated reliability: the real\-time ODD boundary assessment \(Equation 6\) must achieve false\-positive rates below 1% and false\-negative rates below 0\.1% under verified conditions\. Third, a tested Minimum Risk Condition \(MRC\): the fallback procedure must be demonstrated to maintain system safety for a duration exceeding the worst\-case human response time\.

__*\[Figure 2 about here\]*__

__5  Case Study 1: Shaping Cascade Hydropower Station__

__5\.1  System Description__

The Shaping cascade hydropower station is located on the Dadu River in Sichuan Province, China\. The system comprises four cascaded reservoir\-powerhouse stages with a total installed capacity of 360 MW and a combined active storage of approximately 0\.6 × 10⁸ m³\. Each stage operates 2–3 turbine\-generator units with adjustable guide vanes, supplemented by spillway gates for flood discharge\. Typical inflows range from 150 m³/s \(dry season\) to 1,500 m³/s \(wet season peak\), with inter\-stage transport delays of 5–15 minutes depending on flow conditions\. The existing SCADA system provides real\-time monitoring of water levels, turbine power output, gate positions, and inflow measurements at each stage, with all dispatch decisions historically made by human operators following static rule curves\. The primary operational objectives are: \(1\) maximization of power generation revenue subject to real\-time electricity market signals; \(2\) maintenance of reservoir water levels within safety constraints; \(3\) satisfaction of downstream minimum ecological flow requirements; and \(4\) flood routing during wet season\. The system represents a 'point\-type' water infrastructure—multiple control nodes concentrated in close spatial proximity with fast hydraulic coupling \(transport delays of minutes between stages\)—contrasting with the 'line\-type' topology of the Jiaodong case \(Section 6\)\.

__5\.2  MAS Implementation__

The MAS architecture was instantiated for the Shaping cascade as follows\. Each reservoir stage hosts an Edge Agent running Layer 0 safety interlocks \(water level limits, maximum gate opening rates, minimum ecological flow\) and Layer 1 MPC with a reservoir\-scale Integrator internal model: dV\_i/dt = Q\_\{in,i\}\(t\) − Q\_\{out,i\}\(u\_i, h\_i\), where V\_i is storage volume, Q\_\{in,i\} is inflow \(including release from upstream stage\), and Q\_\{out,i\} is the controlled release through turbines and spillways\. A single Area Agent coordinates the cascade, executing Layer 2 DMPC that optimizes total power generation P\_total = Σ\_i η\_i · ρg · Q\_\{turb,i\} · H\_\{net,i\} across all stages subject to cascade coupling constraints\. The Cloud Agent provides Layer 3 planning—weekly\-to\-seasonal reservoir operating schedules based on inflow forecasts and electricity price predictions\.

The MPC controller uses a 10\-minute prediction step with a 6\-hour prediction horizon, optimizing 7 control variables simultaneously \(4 turbine guide vane openings and 3 spillway gate positions\)\. The internal model is a reservoir\-scale Integrator representation with stage\-coupling constraints derived from mass balance continuity\.

The ODD for the Shaping WSAL\-2 implementation was defined as: S\_flow = \[150, 800\] m³/s \(non\-flood inflow range\), S\_level = normal operating pool levels excluding flood reserve zones, S\_equip = all turbines and gates functional, S\_env = non\-flood season \(October–June\)\. Operation during flood season \(July–September\), single\-turbine failure scenarios, and extreme low\-inflow conditions \(<150 m³/s\) were excluded from the initial ODD and managed through manual SCADA control\.

__5\.3  Results and WSAL\-2 Assessment__

Model\-in\-the\-Loop \(MiL\) validation was conducted using retrospective hydrological data from 2015–2017, replaying historical inflow sequences through a high\-fidelity hydraulic simulation of the four\-stage cascade while comparing MAS\-assisted \(WSAL\-2\) recommendations against the historical rule\-based SCADA dispatch records under identical boundary conditions\.

The MiL results demonstrate the following performance improvements\. Power generation efficiency increased by 2–3% compared to historical rule\-based dispatch, attributable to the MPC's ability to coordinate water releases across stages to maintain optimal hydraulic heads\. Water level deviations \(RMS at each stage headpond\) were reduced by approximately 40% compared to manual operation, reflecting tighter tracking of target pool levels\. Ecological flow compliance was maintained at 100% within the certified ODD, with the Layer 0 safety floor ensuring that downstream minimum flow constraints were never violated\. Zero Layer 0 safety violations occurred during the entire assessment period\. Robustness testing confirmed stable MPC performance under inflow forecast errors of up to ±15%\.

The Shaping system meets the WSAL\-2 admission criteria \(Table 2\): MiL verification has been completed for all normal\-season scenarios within the defined ODD; RMS water level deviation is reduced by approximately 40% compared to manual operation, exceeding the ≤30% improvement threshold; and zero Layer 0 safety violations were recorded\. The operator confirmation requirement—the defining characteristic of WSAL\-2—remained in place throughout, with all MPC\-generated control recommendations reviewed and approved by the dispatch center before execution\.

__*\[Figure 3 about here\]*__

__6  Case Study 2: Jiaodong Inter\-Basin Water Transfer__

__6\.1  System Description__

The Jiaodong inter\-basin water transfer project is a large\-scale water conveyance system in Shandong Province, China, transferring water from the Yellow River and local sources to the eastern Shandong peninsula to serve municipal, industrial, and agricultural demands in cities including Yantai, Weihai, and Qingdao\. The system comprises more than 500 km of main canals and pipelines, 13 pump stations with a combined installed pumping capacity of approximately 120 MW, 5 regulating reservoirs providing intermediate storage buffering, and 27 control gates distributed along the conveyance route\. Typical conveyance flows range from 10 m³/s \(low\-demand season\) to 50 m³/s \(peak delivery\)\. The primary operational objectives are: \(1\) reliable delivery of contracted water volumes to multiple demand nodes with heterogeneous priority levels; \(2\) minimization of conveyance losses \(evaporation, seepage, operational spillage\); \(3\) energy\-efficient pump scheduling across 13 cascade pump stations, which constitutes the dominant operating cost; and \(4\) equitable allocation during shortage conditions\.

The Jiaodong system represents a 'line\-type' water infrastructure: control nodes distributed along a long linear conveyance route with transport delays of hours between major nodes, creating a spatially indexed control problem that is fundamentally different from the point\-type Shaping cascade\. This topological contrast is deliberately chosen to test the generalizability of the MAS architecture across infrastructure typologies\.

__6\.2  MAS Implementation: Multi\-Timescale Integration__

The distinctive feature of the Jiaodong MAS implementation is its multi\-timescale integration spanning four temporal horizons\. Layer 3 \(Cloud Agent\) performs annual water allocation planning using a linear programming model that distributes available water supply \(Yellow River quota \+ local sources\) across demand nodes subject to priority\-weighted shortage rules and minimum guarantee constraints\. This annual plan generates monthly and ten\-day delivery schedules that serve as reference trajectories for Layer 2\.

Layer 2 \(Area Agents, one per major conveyance segment\) translates ten\-day delivery targets into daily gate and pump schedules through a rolling\-horizon DMPC that accounts for conveyance delays, reservoir storage buffering, and energy tariff optimization\. The DMPC formulation minimizes the weighted sum of delivery shortfall, energy cost, and operational losses:

*min Σ\_t Σ\_j \[α\_j\(Q\_\{del,j\}\(t\) \- Q\_\{target,j\}\(t\)\)^2 \+ β · E\_cost\(t\) \+ γ · Q\_loss\(t\)\]     \(10\)*

Layer 1 \(Edge Agents at each gate and pump station\) implements real\-time feedback control at minute\-scale intervals, tracking the water level and flow references generated by Layer 2 while compensating for unmeasured disturbances \(local inflows, demand variations, canal seepage\)\.

This four\-horizon integration—annual→monthly→ten\-day→daily→real\-time—represents a key technical achievement: the planning optimization that determines what water to deliver where is seamlessly connected to the real\-time control that determines how to deliver it, through the MAS agent hierarchy\. In prior practice, planning and operation were disconnected processes executed by different departments using different models and different data systems\.

__6\.3  Results and WSAL\-2 Assessment__

Model\-in\-the\-Loop \(MiL\) validation was conducted using retrospective operational data from 2018–2020, replaying historical demand patterns and water availability scenarios through a calibrated hydraulic\-hydrological simulation model of the full 500\+ km conveyance system\.

The MiL results demonstrate the following performance improvements\. Cascade pump energy consumption was reduced by 5–8% compared to historical manual dispatch, primarily through optimized pump scheduling that exploits off\-peak electricity tariffs and coordinates pump station sequencing to reduce hydraulic losses\. Water level tracking at key regulation nodes achieved an RMSE of ±0\.10 m, representing a substantial improvement over the ±0\.30–0\.50 m deviations typical of manual gate adjustment\. Annual water allocation deviations between planned and actual deliveries were reduced to ±3%, compared to ±8–12% under prior manual coordination\. Operational spillage events—uncontrolled water loss at intermediate structures—were reduced by approximately 60% through anticipatory gate control informed by Layer 2 DMPC forecasts\. Zero Layer 0 safety violations occurred during the assessment period\.

Multi\-timescale integration metrics confirm the seamless planning\-to\-control connection: monthly delivery volumes tracked annual plan targets within ±3%; demand change response time \(from Layer 3 plan adjustment to Layer 1 actuator execution\) averaged 4–6 hours, compared to 1–2 days under the prior manual dispatch chain\.

The Jiaodong system meets WSAL\-2 admission criteria through a different implementation pathway than Shaping—emphasizing multi\-timescale planning\-control integration rather than real\-time optimization of a single cascade—yet sharing the identical MAS architectural framework\. This dual\-path convergence at WSAL\-2 provides empirical evidence that the MAS\-WSAL framework accommodates diverse infrastructure typologies\.

__*\[Figure 4 about here\]*__

__7  The WSAL\-2 to WSAL\-3 Transition: X\-in\-the\-Loop Verification Pathway__

Both the Shaping and Jiaodong systems currently operate at WSAL\-2, where operators confirm every control action\. This section analyzes the specific technical and institutional requirements for advancing to WSAL\-3—conditional autonomy within a certified ODD\.

__7\.1  X\-in\-the\-Loop Verification Framework__

The X\-in\-the\-Loop \(xIL\) framework \(Lei et al\., 2025c\) defines four progressive verification stages, each adding a layer of physical realism to the testing environment\.

Stage 1: Model\-in\-the\-Loop \(MiL\)\. The HDC algorithms are tested against a high\-fidelity hydraulic simulation model \(typically a full Saint\-Venant solver\) with synthetic but realistic disturbance scenarios\. MiL validates algorithmic correctness: does the MPC produce feasible, stabilizing control actions for all scenarios within the target ODD? Both the Shaping and Jiaodong projects have completed MiL verification for their respective normal\-operation ODDs\.

An important intermediate step between MiL and field commissioning is shadow\-mode operation: the MAS runs in parallel with human operators on the live SCADA system, producing control recommendations that are logged and scored against actual operator decisions but not executed on actuators\. Shadow mode provides both algorithmic validation under real\-world disturbances and operator familiarization with MAS behavior, without operational risk\. Shadow\-mode experience is recommended as a prerequisite for SiL commissioning\.

Stage 2: Software\-in\-the\-Loop \(SiL\)\. The production software code—not a research prototype but the actual embedded software that will execute on field controllers—is tested against the same simulation environment\. SiL catches implementation bugs \(numerical precision, timing issues, communication protocol errors\) that are invisible in MiL\. SiL is the minimum verification stage required for WSAL\-3 certification\.

Stage 3: Hardware\-in\-the\-Loop \(HiL\)\. The physical controller hardware \(PLC, industrial PC\) running production software is connected to real\-time simulation via analog/digital I/O interfaces\. HiL testing validates the hardware\-software\-communication stack under realistic timing constraints, including tests for communication failure, sensor malfunction, and actuator degradation\. For the WSAL\-2→3 transition, HiL must specifically verify: \(a\) that Layer 0 safety interlocks function correctly when upper\-layer communication fails; \(b\) that the MRC procedure executes within the specified coast time; and \(c\) that island\-autonomy mode maintains safety constraints\.

Stage 4: Plant\-in\-the\-Loop \(PiL\)\. A limited section of the real physical system operates under automated control \(WSAL\-3\) while the remainder continues at WSAL\-2 with human confirmation\. PiL is the final validation before full WSAL\-3 deployment, corresponding to the ‘controlled deployment’ phase in automotive autonomy certification\.

__7\.2  Case\-Specific Transition Analysis__

For Shaping, the WSAL\-2→3 transition is technically closer than for Jiaodong, because the point\-type topology has shorter transport delays \(faster feedback\), simpler hydraulic coupling \(cascade connectivity\), and a well\-defined normal\-operation ODD\. The primary barriers are: \(a\) completion of SiL and HiL testing for the production control software; \(b\) formal specification and testing of the MRC procedure \(what happens if all communication to the cascade dispatch center fails?\); and \(c\) institutional acceptance—regulatory approval for automated reservoir operations without real\-time human confirmation\.

__Human Factors\.__ The WSAL\-2→3 transition also introduces human factors challenges well\-documented in aviation and automotive automation \(Parasuraman & Riley, 1997\)\. At WSAL\-2, operators actively confirm every control action, maintaining direct engagement with the physical system\. At WSAL\-3, operators shift to supervisory monitoring, which may induce automation complacency and skill degradation over time\. If the system subsequently exits the ODD and reverts to human control, the operator must re\-engage with a system whose state may have evolved in unfamiliar ways—the phenomenon of 'automation surprise\.'\. To mitigate these risks, the WSAL\-3 operational protocol should include: \(a\) mandatory periodic manual\-mode exercises during which operators resume WSAL\-2 control for routine scenarios; \(b\) transparent system\-status displays designed to maintain situational awareness of ODD boundary proximity, agent health, and control rationale; and \(c\) MRC response time assumptions \(T\_operator in Equation 7\) that account for the cognitive latency of operators transitioning from passive monitoring to active control\.

For Jiaodong, the transition is more complex because the line\-type topology introduces longer transport delays \(hours\), larger ODD dimensionality \(more demand nodes, more equipment failure combinations\), and tighter coupling between planning and control layers\. The specific additional requirements are: \(a\) SiL verification must cover not only normal delivery scenarios but also single\-pump\-failure and drought\-allocation scenarios; \(b\) HiL testing must validate the Area Agent coordination mechanism under communication degradation between pump stations; and \(c\) the multi\-timescale integration requires that Layer 3 plan adjustments propagate correctly to Layer 1 under all ODD conditions\.

Table 3 summarizes the xIL verification status and remaining requirements for both cases\.

__Table 3\. xIL verification status and WSAL\-2→3 gap analysis__

__xIL Stage__

__Shaping Status__

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

__*\[Figure 5 about here\]*__

__8  Discussion__

__8\.1  Generalizability of the MAS\-WSAL Framework__

The deliberate selection of two topologically distinct case studies—a point\-type cascade \(Shaping\) and a line\-type conveyance system \(Jiaodong\)—provides preliminary evidence that the MAS architecture accommodates diverse infrastructure typologies through the same three\-component structure \(HDC \+ ODD \+ CI\), differentiated only by the parameterization of the HDC internal models, the dimensionality of the ODD, and the communication topology of the agent hierarchy\. This is consistent with the structural isomorphism proposition of CHS theory \(Lei et al\., 2025a\), which predicts that all water conveyance systems share the same six\-element control structure\. Extending the framework to additional typologies—urban distribution networks \(pressure management\), flood detention basins \(event\-driven control\), and coupled multi\-source systems \(conjunctive use\)—is a priority for future work\.

__Relationship to Digital Twins\.__ The dominant digitalization paradigm in the water sector is the digital twin—a virtual replica of the physical system used for monitoring, prediction, and scenario analysis \(Pedersen et al\., 2021\)\. MAS\-WSAL and digital twins are complementary rather than competing concepts\. A digital twin is primarily descriptive and predictive: it mirrors the physical system's state and forecasts future behavior\. MAS is prescriptive and autonomous: agents act on the physical system through control commands\. The connection is through the ODD certification pathway: a digital twin provides the high\-fidelity simulation environment required for xIL verification \(§7\), which certifies the ODD within which autonomous MAS operation is permitted\. Thus, a digital twin without MAS can observe but cannot act autonomously; MAS without a digital twin equivalent cannot be certified for WSAL\-3\+\. This positions the digital twin as a necessary but insufficient component of the automation pathway\.

__Resilience Perspective\.__ Beyond operational efficiency, the MAS\-WSAL framework provides structural resilience advantages\. The ODD framework explicitly addresses degraded conditions and equipment failure scenarios as boundary conditions rather than afterthoughts\. Island\-autonomy mode \(Table 1\) ensures that communication loss—whether from cyberattack, natural disaster, or equipment failure—triggers graceful degradation rather than total system failure\. The Layer 0 safety floor provides invariant physical protection during cascading failures, independent of the state of upper\-layer intelligence\. The multi\-layer architecture thus provides graduated resilience: a system at WSAL\-3 that encounters a compound event \(flood \+ equipment failure \+ communication loss\) degrades through WSAL\-2 \(manual confirmation mode\) to island\-autonomy \(local L0\+L1 control\) rather than failing catastrophically \(Hashimoto et al\., 1982\)\. This resilience property is increasingly important as compound climate\-hydrological events intensify\.

__8\.2  Relationship Between Physical AI and Cognitive AI__

The MAS architecture makes an explicit and deliberate allocation of responsibilities between physics\-based computation \(HDC\) and AI\-enhanced reasoning \(CI\)\. At WSAL\-2, CI plays no role—all control is HDC\-based with human confirmation\. At WSAL\-3, CI begins to contribute through ODD monitoring and scenario recognition, but all actions remain within the HDC\-computed feasible set\. The Cognitive AI engine becomes architecturally essential only at WSAL\-4, where it must handle novel scenarios that were not pre\-certified in the ODD\. This graduated introduction mirrors the operational singularity: because water failures are irreversible, AI capabilities must be proven incrementally rather than deployed at once\.

The propose\-validate interaction loop \(Equations 8–9\) is the architectural mechanism that ensures this graduated integration\. It deserves emphasis that this is not merely a ‘check’ that CI outputs are reasonable—it is a hard mathematical feasibility verification\. The HDC engine solves the constrained optimization \(Equations 2–4\) with the CI\-proposed parameters and rejects any proposal that would violate physical constraints\. This architecture provides formal guarantees that no CI error, no matter how subtle, can produce an unsafe actuator command\.

__8\.3  Implications for Water Sector Governance__

WSAL provides a shared vocabulary that can serve multiple governance functions\. For regulators, WSAL levels provide a basis for certification requirements: what verification evidence must a utility provide before operating a section at WSAL\-3? For utilities, WSAL provides a maturity benchmark: where does each subsystem stand, and what investments are needed to advance? For technology providers, WSAL provides interoperability requirements: Edge Agents from different vendors must implement the same Layer 0 safety logic and the same heartbeat protocol to achieve WSAL\-3 certification\. For international standardization bodies \(IAHR, IWA, ISO\), WSAL provides a candidate framework for water automation standards, analogous to SAE J3016 for automotive\. A critical equity consideration is that xIL verification infrastructure—simulation platforms, HiL test rigs, and PiL field instrumentation—requires substantial capital investment that may be inaccessible to smaller utilities and developing countries\. To address this, the WSAL framework is designed to be incrementally adoptable: WSAL\-1 and WSAL\-2 require only standard SCADA infrastructure and MiL simulation, which can leverage open\-source hydraulic models \(e\.g\., EPANET, HEC\-RAS\)\. International collaboration on shared xIL verification platforms and open reference ODDs could further reduce barriers to participation\. For WSAL to achieve its standardization potential, open specifications are needed for: \(a\) the ODD description format \(a machine\-readable schema defining the certified operating envelope\); \(b\) the agent communication protocol \(analogous to IEC 61850 for power substation automation\); and \(c\) the Layer 0 safety interface specification\. We recommend that these specifications be developed under the auspices of international bodies such as IAHR, IWA, or ISO, with input from utilities, vendors, and regulators\.

__8\.4  Limitations__

Several limitations should be acknowledged\. First, both case studies currently operate at WSAL\-2; the WSAL\-3 transition analysis \(Section 7\) is prospective rather than empirical\. Full validation of the WSAL\-3 criteria requires completion of the xIL verification program, which is ongoing\. Second, the quantitative admission criteria in Table 2 are proposed rather than standardized; community discussion and iterative refinement through diverse case studies will be needed before standardization\. Third, the CI component \(Section 3\.3\) is described architecturally but has not been implemented in either case study; the current WSAL\-2 deployments use HDC without CI, consistent with the graduated integration pathway\. Fourth, WSAL\-4 and WSAL\-5 remain aspirational; no empirical data support the proposed criteria for these levels\. Fifth, the economic analysis of WSAL advancement—the cost\-benefit tradeoff of investing in xIL verification infrastructure versus the operational benefits of higher autonomy levels—is not addressed in this paper and constitutes an important direction for future work\.

__9  Conclusions__

This paper has presented two interlocking contributions for advancing water infrastructure from manual SCADA\-based supervision toward autonomous operation\.

First, the Multi\-Agent System \(MAS\) architecture, formally defined as MAS = HDC \+ ODD \+ CI, provides an implementable framework for organizing control intelligence within operational water networks\. Hierarchical Distributed Control \(HDC\) deploys physics\-based MPC across four temporal layers \(safety, regulation, coordination, planning\), with a mathematically guaranteed Layer 0 safety floor that no upper\-layer decision may override\. The Operational Design Domain \(ODD\) transforms the trust question from binary to graduated: automation is certified for specific, verified operating conditions, with automatic fallback to safe modes at ODD boundaries\. Cognitive Intelligence \(CI\) adds scenario\-aware reasoning through a propose\-validate interaction loop that ensures physics\-based safety is never compromised\. The three\-tier agent hierarchy \(Edge–Area–Cloud\) maps these components onto the spatial topology of water networks, with island\-autonomy capabilities at every tier\.

Second, Water Systems Autonomy Levels \(WSAL\) provide a five\-level classification \(WSAL\-1 through WSAL\-5\) with quantitative admission criteria for each level\. Three water\-specific design principles—the bucket principle, the non\-negotiable safety floor, and ODD\-bounded autonomy—distinguish WSAL from SAE J3016 and reflect the operational singularity of water infrastructure\. The WSAL\-2 to WSAL\-3 transition is identified as the critical near\-term milestone, requiring systematic X\-in\-the\-Loop verification to certify ODD boundaries\.

The framework has been MiL\-validated through two operational case studies spanning distinct infrastructure typologies: the Shaping cascade hydropower station \(point\-type, real\-time power optimization; 2–3% efficiency gain, 40% water level deviation reduction\) and the Jiaodong inter\-basin water transfer \(line\-type, multi\-timescale planning\-control integration; 5–8% energy reduction, ±0\.10 m RMSE\)\. Both systems demonstrate WSAL\-2 achievement through the same MAS architectural principles, differentiated only by internal model parameterization and agent topology—providing empirical evidence that a single architectural framework can accommodate diverse water infrastructure types\. The xIL verification gap analysis \(Table 3\) provides a concrete roadmap for the WSAL\-2→3 transition at both sites, encompassing not only technical verification but also human factors \(operator training, situational awareness\) and institutional requirements \(regulatory approval, cybersecurity certification\)\.

The MAS\-WSAL framework is offered as a foundation for community standardization\. Just as SAE J3016 transformed the automotive industry’s approach to autonomous driving by providing a shared vocabulary, WSAL aims to provide the water community with a common framework for planning, benchmarking, and advancing the operational intelligence of water infrastructure worldwide\.

__Acknowledgments__

This work was supported by the National Key R&D Program of China \(Grant Nos\. \[to be inserted\]\) and the National Natural Science Foundation of China \(Grant Nos\. \[to be inserted\]\)\. The authors thank the Shaping hydropower station and the Jiaodong Water Transfer Authority for providing operational data and facilitating field implementation\. The authors also thank the members of the IAHR Working Group on Water System Operations for discussions that shaped the WSAL framework\.

__References__

Cantoni, M\., Weyer, E\., Li, Y\., Ooi, S\. K\., Mareels, I\., & Ryan, M\. \(2007\)\. Control of large\-scale irrigation networks\. Proceedings of the IEEE, 95\(1\), 75–91\. https://doi\.org/10\.1109/JPROC\.2006\.887289

Castelletti, A\., Ficchì, A\., Cominola, A\., Segovia, P\., Giuliani, M\., Wu, W\., Lucia, S\., Ocampo\-Martinez, C\., De Schutter, B\., & Maestre, J\. M\. \(2023\)\. Model Predictive Control of water resources systems: A review and research agenda\. Annual Reviews in Control, 55, 442–465\. https://doi\.org/10\.1016/j\.arcontrol\.2023\.03\.013

Creaco, E\., Campisano, A\., Fontana, N\., Marini, G\., Page, P\. R\., & Walski, T\. \(2019\)\. Real time control of water distribution networks: A state\-of\-the\-art review\. Water Research, 161, 517–530\. https://doi\.org/10\.1016/j\.watres\.2019\.06\.025

Giuliani, M\., Lamontagne, J\. R\., Reed, P\. M\., & Castelletti, A\. \(2021\)\. A state\-of\-the\-art review of optimal reservoir control for managing conflicting demands in a changing world\. Water Resources Research, 57\(12\), e2021WR029927\. https://doi\.org/10\.1029/2021WR029927

Hashimoto, T\., Stedinger, J\. R\., & Loucks, D\. P\. \(1982\)\. Reliability, resiliency, and vulnerability criteria for water resource system performance evaluation\. Water Resources Research, 18\(1\), 14–20\. https://doi\.org/10\.1029/WR018i001p00014

IEC\. \(2010\)\. IEC 61508: Functional safety of electrical/electronic/programmable electronic safety\-related systems\. International Electrotechnical Commission\.

IEC\. \(2018\)\. IEC 62443: Industrial communication networks—Network and system security\. International Electrotechnical Commission\.

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

Mayne, D\. Q\., Rawlings, J\. B\., Rao, C\. V\., & Scokaert, P\. O\. M\. \(2000\)\. Constrained model predictive control: Stability and optimality\. Automatica, 36\(6\), 789–814\. https://doi\.org/10\.1016/S0005\-1098\(99\)00214\-9

McArthur, S\. D\. J\., Davidson, E\. M\., Catterson, V\. M\., Dimeas, A\. L\., Hatziargyriou, N\. D\., Ponci, F\., & Funabashi, T\. \(2007\)\. Multi\-agent systems for power engineering applications—Part I: Concepts, approaches, and technical challenges\. IEEE Transactions on Power Systems, 22\(4\), 1743–1752\. https://doi\.org/10\.1109/TPWRS\.2007\.908471

Maestre, J\. M\., & Negenborn, R\. R\. \(Eds\.\)\. \(2014\)\. Distributed model predictive control made easy\. Springer\. https://doi\.org/10\.1007/978\-94\-007\-7006\-5

Malaterre, P\.\-O\., Rogers, D\. C\., & Schuurmans, J\. \(1998\)\. Classification of canal control algorithms\. Journal of Irrigation and Drainage Engineering, 124\(1\), 3–10\. https://doi\.org/10\.1061/\(ASCE\)0733\-9437\(1998\)124:1\(3\)

Milly, P\. C\. D\., Betancourt, J\., Falkenmark, M\., Hirsch, R\. M\., Kundzewicz, Z\. W\., Lettenmaier, D\. P\., & Stouffer, R\. J\. \(2008\)\. Stationarity is dead: Whither water management? Science, 319\(5863\), 573–574\. https://doi\.org/10\.1126/science\.1151915

Mareels, I\. M\. Y\., Weyer, E\., Ooi, S\. K\., Cantoni, M\., Li, Y\., & Nair, G\. \(2005\)\. Systems engineering for irrigation systems\. Annual Reviews in Control, 29\(2\), 191–204\. https://doi\.org/10\.1016/j\.arcontrol\.2005\.08\.001

Parasuraman, R\., & Riley, V\. \(1997\)\. Humans and automation: Use, misuse, disuse, abuse\. Human Factors, 39\(2\), 230–253\. https://doi\.org/10\.1518/001872097778543886

Pedersen, A\. N\., Borup, M\., Brink\-Kjær, A\., Christiansen, L\. E\., & Mikkelsen, P\. S\. \(2021\)\. Living and prototyping digital twins for urban water systems: Towards multi\-purpose value creation using models and sensors\. Water, 13\(5\), 592\. https://doi\.org/10\.3390/w13050592

Negenborn, R\. R\., van Overloop, P\. J\., Keviczky, T\., & De Schutter, B\. \(2009\)\. Distributed model predictive control of irrigation canals\. Networks and Heterogeneous Media, 4\(2\), 359–380\. https://doi\.org/10\.3934/nhm\.2009\.4\.359

RTCA\. \(2011\)\. DO\-178C: Software considerations in airborne systems and equipment certification\.

Richards, L\. A\., Whittaker, J\., & Savic, D\. \(2023\)\. Artificial intelligence for water systems: Opportunities, risks and governance\. Nature Water, 1\(5\), 422–432\. https://doi\.org/10\.1038/s44221\-023\-00096\-5

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

__Figure 3\. __Shaping cascade hydropower case study: \(a\) system schematic showing 4\-stage cascade on the Dadu River with Edge Agents at each stage and Area Agent for cascade coordination; \(b\) MPC performance comparison: water level deviation timeseries under WSAL\-2 MAS\-assisted control vs\. historical rule\-based SCADA \(2015–2017 MiL\); \(c\) power generation efficiency comparison showing 2–3% improvement; \(d\) ODD boundary visualization showing certified non\-flood\-season operating region\.

__Figure 4\. __Jiaodong inter\-basin transfer case study: \(a\) system schematic showing 500\+ km linear conveyance topology with 13 pump stations, 5 reservoirs, and 27 gates, with Edge Agents at gates/pumps, Area Agents per segment, and Cloud Agent for system\-wide planning; \(b\) multi\-timescale integration: annual plan → monthly schedule → ten\-day targets → daily gate operations → real\-time control, showing seamless cascading through the MAS agent hierarchy; \(c\) water delivery compliance and energy reduction metrics under WSAL\-2 operation \(2018–2020 MiL\)\.

__Figure 5\. __X\-in\-the\-Loop \(xIL\) verification roadmap for the WSAL\-2→3 transition\. Left: four\-stage progression \(MiL → SiL → HiL → PiL\) with increasing physical realism\. Center: case\-specific gap analysis for Shaping \(point\-type\) and Jiaodong \(line\-type\), showing current verification status and remaining requirements\. Right: timeline projection with institutional milestones \(regulatory approval, operator certification, insurance assessment\)\.

