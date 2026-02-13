__Towards autonomous water networks__

__Xiaohui Lei__1\*, __Chen Ji__2, __Chao Wang__3 & __Hao Wang__3

1 Hebei University of Engineering, Handan 056038, China

2 Sichuan University, Chengdu 610065, China

3 China Institute of Water Resources and Hydropower Research, Beijing 100038, China

*\* Corresponding author\. E\-mail: lxh@iwhr\.com*

__Abstract__

Water infrastructure worldwide faces a widening gap between physical capacity and operational intelligence\. While nations have invested trillions of dollars in dams, canals, and pipelines, real\-time operation of these systems remains overwhelmingly manual, resulting in chronic inefficiencies — compounded by climate non\-stationarity that undermines planning\-based approaches — including irrigation delivery losses of 40–60%, urban pipe leakage exceeding 20%, and multi\-day response times for supply disruptions\. Here we argue that a fundamental paradigm shift is needed—from static water allocation to autonomous, closed\-loop water network control\. Drawing on control theory, artificial intelligence, and lessons from the autonomous vehicle industry, we propose Cybernetics of Hydro Systems as a unifying theoretical framework and introduce a five\-level Water Systems Autonomy Level classification to guide incremental deployment\. Early implementations on hydropower stations and long\-distance water transfer projects demonstrate feasibility\. We outline a roadmap for achieving progressively autonomous water networks while ensuring safety, equity, and responsible deployment\.

__The infrastructure–intelligence gap__

Global investment in water infrastructure has reached an unprecedented scale\. China alone has committed over one trillion yuan to the South\-to\-North Water Diversion Project and related national water network construction\[1,2\]\. India's Jal Shakti Abhiyan, the United States' Infrastructure Investment and Jobs Act, and the European Union's water framework investments collectively represent hundreds of billions of dollars in water system modernization\[3\]\. Yet a striking paradox persists: the 'hardware' of water infrastructure has reached world\-class levels, while the 'software'—the operational intelligence that governs how these systems actually deliver water—remains rudimentary\.

Consider the South\-to\-North Middle Route, a 1,432\-km canal with dozens of check gates and nearly one hundred diversion outlets\. Despite its engineering sophistication, daily operation relies primarily on human experience, with dispatch response times measured in hours to days\[2\]\. This is not an isolated case\. The World Bank estimates that non\-revenue water losses in developing countries average 35–40%\[4\]\. Globally, irrigation systems deliver only 40–60% of diverted water to crops\[5\]\. When extreme events strike—droughts, floods, infrastructure failures—the gap between what these systems could do and what they actually do becomes acute\.

The root cause is not a shortage of sensors, actuators, or communication networks—these are increasingly available and affordable\. Rather, it is the absence of a systematic theoretical framework for water network operation control\. Water resources systems analysis \(WRSA\), the field's foundational methodology, was developed for planning and design: determining how much water to allocate where, at monthly\-to\-annual timescales\[6,7\]\. It was never designed to answer the operational question: how to deliver water efficiently, safely, and adaptively through complex networks in real time\.

This gap parallels what the automotive industry faced before the autonomous vehicle revolution\. Cars were engineered for performance and safety, but their real\-time operation was left entirely to human drivers\. The convergence of control theory, sensor fusion, and artificial intelligence is now transforming transportation\[8,9\]\. We argue that water infrastructure is poised for an analogous transformation—and that the theoretical foundations for this transformation are now within reach\.

__From allocation to control: a necessary paradigm shift__

WRSA has evolved through three phases \(Fig\. 1\)\. The first \(1950s–1980s\), exemplified by the Harvard Water Program and Rippl's reservoir analysis, established water balance and infrastructure planning methods—answering the question 'what to build'\[10,11\]\. The second \(1990s–2010s\), driven by multi\-objective optimization and integrated water resources management\[7,12\], developed allocation frameworks—answering 'how much water to distribute'\. Wang et al\.'s dualistic water cycle theory\[1\], which integrated human activity impacts into hydrological analysis, exemplifies this phase's advances\. Both phases operate at monthly\-to\-annual timescales using algebraic models \(mass balance equations\) and have achieved remarkable success in water resources planning\[6,13\]\.

The urgency of this transition is compounded by a foundational crisis in the planning paradigm\. Classical WRSA assumed hydrological stationarity—that historical statistics reliably predict future conditions\. Climate change has invalidated this assumption: as Milly et al\. \(2008\) argued, 'stationarity is dead'\[57\]\. Non\-stationarity means that even optimal static allocations become progressively mismatched to actual conditions\. The hydrological community has recognized this paradigm shift through the IAHS 'Panta Rhei' decade on change in hydrology and society\[67\]\. Real\-time adaptive control is therefore not merely an efficiency gain—it is becoming a necessity as the planning\-based paradigm's foundational assumption erodes\.

The emerging third phase addresses a fundamentally different question: how to deliver water through complex networks in real time\. This requires a qualitative shift in mathematical structure—from algebraic optimization to dynamic control—across four dimensions\. In timescale: from months to seconds\. In models: from algebraic mass balance to partial differential equations \(Saint\-Venant or water hammer equations\)\. In decision variables: from scalar water volumes to time\-varying actuator signals \(gate openings, pump speeds, valve positions\)\. In uncertainty treatment: from offline scenario analysis to online feedback control\[14–16\]\.

__\[Figure 1\]__ Three\-phase evolution of water resources systems analysis\. Phase I \(1950s–1980s\): water balance and infrastructure planning\. Phase II \(1990s–2010s\): optimal allocation and integrated management\. Phase III \(2020s–\): dynamic control and autonomous operation\. The transition from Phase II to Phase III requires a qualitative shift from algebraic optimization to dynamic control theory\. A central driver of this transition is the breakdown of the hydrological stationarity assumption that underpinned Phases I and II\.

This four\-dimensional mismatch is not merely a matter of resolution—it represents a fundamentally different class of problem\. Bridging this gap requires a dedicated theoretical framework that can inherit WRSA's systems perspective while incorporating control science's feedback principles\.

__Structural invariants: why water systems need dedicated theory__

A natural question arises: why not simply apply existing industrial process control methods? The answer lies in five structural properties that, while individually present in other engineered systems, combine uniquely in water networks\[14\]\. First, irreversible failure modes: dam overtopping, canal breaching, and pipe bursting cause damage that no control action can reverse—unlike temperature excursions in chemical processes\. Second, extreme spatial distribution: a single controlled system can span hundreds to thousands of kilometres, with hydraulic wave propagation times measured in hours to days\. Third, slow distributed actuators: gates require 10–30 minutes for full travel and pump stations need staged start\-up sequences—orders of magnitude slower than industrial valves\. Fourth, open\-boundary environmental coupling: rainfall, evaporation, and seepage continuously perturb the system through spatially distributed, uncontrolled inputs\. Fifth, no trial\-and\-error: safety\-critical operation precludes fault injection experiments on live infrastructure—a constraint shared with aviation but absent from most industrial settings\[17,18\]\.

We term this combination 'operational singularity'—using 'singularity' in its original sense of uniqueness, distinct from the mathematical or AI\-discourse meanings—: the co\-occurrence of these five properties makes water systems fundamentally different from other controlled processes and necessitates a dedicated theoretical framework\[14\]\.

Yet beneath the surface diversity of water systems—irrigation canals, urban pipe networks, hydropower reservoirs, inter\-basin transfer schemes—lies a remarkable structural isomorphism\. From a control\-theoretic perspective, all one\-dimensional water systems are governed by hyperbolic conservation laws, controlled through constrained boundary inputs, exhibit state\-dependent propagation delays, face uncertain environmental disturbances, and must satisfy inviolable safety constraints\[14,19\]\. The canal automation community—from Schuurmans \(1997\)\[59\] through Litrico and Fromion \(2004, 2009\)\[20,60\] and van Overloop \(2006\)\[61\] to Horváth et al\. \(2024\)\[62\]—established the control\-theoretic tools for individual canal pools\. CHS extends this work to a cross\-sector unification and system\-level architecture\. We have formalized this observation by proving that the low\-order control models of all one\-dimensional water systems—open channels, pressurized pipes, and natural rivers—are special instances of two parametric transfer function families\[14\]\. The non\-self\-regulating family \(integrator\-delay\-zero models\[20\]\) applies to gate\-controlled canal pools and valve\-controlled pipe segments\. The self\-regulating family \(first\-order\-delay models\[21\]\) applies to overflow weirs and natural river reaches\. This unification connects previously disconnected models from irrigation engineering\[20,22\], hydrology\[21\], and pipeline hydraulics\[23,24\], establishing for the first time a mathematical bridge across water sub\-disciplines\.

__Cybernetics of Hydro Systems: a unifying framework__

Building on these foundations, we propose Cybernetics of Hydro Systems \(CHS\) as a theoretical framework for water network operation control\[14\]\. We adopt 'cybernetics' deliberately, connecting to Wiener's \(1948\) original definition of feedback control in complex systems—a framework that, after decades of fragmented development, is experiencing renewed relevance as water systems integrate sensing, computation, and actuation at network scale\. CHS formalizes any water system as a six\-element controlled system: Plant \(the hydraulic process governed by conservation laws\), Actuators \(gates, pumps, valves\), Sensors \(level gauges, flow meters\), Disturbances \(rainfall, demand fluctuations\), Controller \(decision algorithms\), and Objectives \(level tracking, flow matching, safety constraints\)\. This formalization applies universally—from a single hydropower station to a thousand\-kilometre inter\-basin transfer system\.

Current smart water and digital twin initiatives have advanced monitoring, data analytics, and decision support capabilities significantly\[53,54,66\]\. CHS complements these advances by providing three elements that existing approaches typically lack: a unified mathematical framework connecting models across water sub\-disciplines \(the transfer function family unification\), a formal autonomy classification \(WSAL\) with testable entry criteria and defined operational design domains, and a safety architecture \(the propose\-validate loop\) ensuring that AI\-augmented decisions respect physical constraints before reaching actuators\.

A key contribution is the model hierarchy established through progressive simplification: from full Saint\-Venant partial differential equations, through linearized transfer functions, to steady\-state mass balance\. Each simplification level discards one timescale, creating a natural correspondence between model complexity and control layer\[14\]: safety protection \(milliseconds, hardware interlocks\), real\-time regulation \(seconds to minutes, local model predictive control\[25,26\]\), coordination \(minutes to hours, distributed MPC\[27,28\]\), and planning \(hours to years, nested optimization\[29,30\]\)\. This 'just precise enough' principle ensures that each layer uses the minimum model complexity needed for its control task, maintaining both computational tractability and physical fidelity\.

Eight design principles, organized as four dual pairs—feedback versus decoupling, model reduction versus emergence, robustness versus coordination, hierarchy versus autonomy—capture the fundamental tensions in water network control design\[14\]\. These principles are not independent rules but a tension network: maximizing any single principle degrades its dual\. For example, the hierarchy–autonomy duality reflects the trade\-off between global optimality \(requiring centralized information\) and local resilience \(requiring autonomous fallback\)\. System design thus becomes an exercise in navigating a multi\-dimensional trade\-off space, where the optimal balance depends on network topology, operational requirements, and management constraints\.

__The autonomous water network architecture__

The CHS framework provides theoretical foundations, but achieving autonomous operation requires an integrated technical architecture\. We propose that autonomous water networks rest on three pillars, expressed as a core equation\[15\]: MAS = HDC \+ ODD \+ Cognitive Intelligence \(Fig\. 2\)\.

__\[Figure 2\]__ The autonomous water network architecture\. MAS \(Multi\-Agent System\) integrates three pillars: HDC \(Hierarchical Distributed Control\) providing the Physical AI engine based on mechanistic models and optimization; ODD \(Operational Design Domain\) defining safety boundaries for each autonomy level; and Cognitive Intelligence providing the Cognitive AI engine for scenario understanding and adaptive decision\-making\. Within each intelligent agent, Physical AI and Cognitive AI interact through a propose\-validate loop: Cognitive AI proposes actions based on situational understanding; Physical AI validates proposals against hydraulic constraints and returns either confirmation or constraint violations requiring revision\.

Hierarchical Distributed Control \(HDC\) constitutes the Physical AI engine\. Based on mechanistic models \(Saint\-Venant equations and their simplifications\) and numerical optimization \(model predictive control\), HDC decomposes the network spatially into distributed sub\-controllers and temporally into layered control problems\. HDC solves the 'compute accurately' problem: given a defined scenario, it determines optimal actuator trajectories satisfying all hydraulic constraints\[15,27\]\. However, HDC possesses distributed 'execution capability' but lacks distributed 'judgement capability'—all strategies are designed for predefined scenarios, and the critical decisions of scenario identification and strategy switching remain with human operators\.

This limitation motivates the second pillar: Cognitive Intelligence, the Cognitive AI engine\. Built on scenario recognition models, knowledge graphs, and hybrid AI methods\[32,63,64\], Cognitive Intelligence provides scenario recognition, goal assembly, emergency reasoning, and explainable decision generation\. It solves the 'think clearly' problem\. Within each intelligent agent, a Physical AI–Cognitive AI interaction loop operates: Cognitive AI proposes actions based on situational understanding; Physical AI validates proposals against hydraulic constraints; Cognitive AI revises if necessary\[15\]\. To illustrate: during an unexpected drought, Cognitive Intelligence might recognize the scenario from historical precedents and knowledge graphs, and propose revised delivery targets—reducing allocations to lower\-priority demand nodes while maintaining minimum supply to hospitals and critical facilities\. Physical AI would then simulate the proposed operating plan against the network's hydraulic model, verifying that the reduced allocations are physically feasible without violating minimum pressure constraints, pipe velocity limits, or reservoir safety levels\. Only after this physics\-based validation would the validated schedule be presented to the operator for confirmation \(WSAL\-2\) or executed directly \(WSAL\-3 and above\)\. The reliability concerns inherent in probabilistic AI systems—including hallucination, distributional shift, and lack of formal verification\[33\]—are addressed architecturally: Cognitive Intelligence may only propose actions that Physical AI has validated against hydraulic constraints\. No AI\-generated decision reaches an actuator without passing through the physics\-based safety filter\. This dual\-engine architecture ensures that AI\-generated decisions always respect physical laws—addressing a core concern about AI reliability in safety\-critical infrastructure\[33,34\]\.

The third pillar, the Operational Design Domain \(ODD\), borrowed from autonomous vehicle standards \(SAE J3016\)\[8\], defines the boundary conditions under which autonomous operation is safe\. Each autonomy level corresponds to a specific ODD—the set of validated operating conditions \(flow ranges, equipment states, weather parameters\) within which the system may operate without human intervention\. When conditions approach ODD boundaries, the system automatically degrades to human\-supervised mode\. Progress toward higher autonomy is fundamentally an ODD expansion process, achieved through systematic in\-the\-loop verification: model\-in\-the\-loop, software\-in\-the\-loop, hardware\-in\-the\-loop, and plant\-in\-the\-loop testing\[16\]—following the V\-model verification paradigm proven in aviation \(DO\-178C\) and automotive \(ISO 26262\) safety\-critical systems\[17,35\]\.

The resulting Multi\-Agent System \(MAS\) deploys intelligent agents at multiple hierarchical levels: edge agents at individual control stations handle local sensing and real\-time control; area agents coordinate neighbouring sub\-systems through distributed optimization; cloud agents manage network\-wide resource allocation and situational awareness\. Layer 0 \(safety protection via SCADA/PLC hardware interlocks\) serves as an inviolable safety floor—no upper\-layer decision may override L0 safety logic\[15\]\.

__From theory to practice: early implementations__

CHS and its technical architecture emerged from over a decade of engineering practice in China, progressing from single\-facility \('point'\) to long\-distance \('line'\) implementations\.

At the Shaping Hydropower Station \(360 MW, Dadu River\), we developed model predictive control for real\-time optimization of turbine dispatch and spillway gate coordination\. Using 10\-minute prediction intervals over 6\-hour horizons, the system demonstrated 2–3% improvement in generation efficiency while reducing water level constraint violations by approximately 40% in model\-in\-the\-loop testing with historical inflow data—simulation\-based validation, not operational deployment results\[36\]\. The key theoretical insight was that the reservoir–turbine system is structurally isomorphic to a canal pool–gate system: both are non\-self\-regulating integrator processes with constrained boundary inputs\. This discovery directly supported the unified transfer function thesis\.

The Jiaodong Water Transfer Project \(500\+ km, Shandong Province\) extended predictive control from a single facility to a long\-distance, mixed\-mode transfer system combining gravity flow, pump stations, tunnels, and regulating reservoirs\[37\]\. The project implemented a SCADA\+HDC architecture with four core modules: \(i\) a multi\-timescale planning optimization system with annual–monthly–ten\-day–daily nested water allocation models, where each temporal level constrains the next through iterative coordination; \(ii\) full\-line hydraulic simulation solving the Saint\-Venant equations; \(iii\) cascade pump station optimization minimizing energy consumption under hydraulic constraints\[38,39\]; and \(iv\) gate coordination for gravity\-flow canal sections\. These results represent validated simulation performance; operational deployment with full closed\-loop control is underway\.

These Chinese implementations complement international efforts: the ASCE canal control test cases \(Clemmens et al\., 2005\)\[59\] established performance benchmarks; Dutch research demonstrated operational MPC on real canals \(van Overloop et al\., 2010; Horváth et al\., 2024\)\[65,62\]; and Australian irrigation modernization programs have deployed automation at scale\. The Dutch Maeslant Barrier—an automated storm surge barrier operational since 1997—provides a precedent for fully autonomous water infrastructure control at the individual\-facility level\[65\]\. References 14–16 and 19 are Chinese\-language publications; the CHS framework is being developed for English\-language publication in Water Resources Research \(companion paper in preparation\)\.

The Jiaodong implementation achieved a preliminary unification of long\-term water allocation with short\-term operational control through the nested multi\-timescale optimization framework—directly validating the CHS principle that hierarchical distributed control applies to temporal decomposition as well as spatial decomposition\. However, both implementations also exposed a fundamental limitation: all control strategies were designed for predefined 'normal' scenarios\. When atypical conditions arose—multi\-year droughts requiring source switching, infrastructure failures requiring emergency rerouting—the system could only provide advisory information while human operators made all critical decisions\. These atypical scenarios account for less than 10% of operating time but consume over 50% of operator attention—a Pareto pattern that directly motivates the upgrade from HDC to cognitive\-intelligence\-augmented MAS\.

__Autonomy levels for water networks__

Borrowing from the autonomous vehicle industry's proven classification approach\[8,9\], we propose Water Systems Autonomy Levels \(WSAL\), a five\-level framework for classifying water network automation maturity and guiding incremental deployment \(Fig\. 3\)\. L1 \(Remote Monitoring\): SCADA provides data acquisition; all decisions are human\-made\. L2 \(Assisted Control\): HDC algorithms execute control actions for predefined scenarios; humans confirm commands and handle all scenario transitions\. L3 \(Conditional Autonomy\): the system operates autonomously within a verified ODD; humans intervene only when conditions approach ODD boundaries\. L4 \(High Autonomy\): MAS with cognitive intelligence handles most scenarios, including many novel situations; human oversight is maintained but intervention is rare\. L5 \(Full Autonomy\): the system autonomously manages all conditions with self\-expanding ODD\.

The automotive analogy that motivates WSAL is instructive but imperfect, and three differences shape the water sector's path\. First, standardization: SAE J3016 emerged from broad industry collaboration; WSAL requires similar international consensus\-building through organizations such as IAHR and ISO TC 224, not adoption of any single research group's classification\. Second, market incentives: automotive autonomy is driven by massive private investment; water infrastructure is predominantly public, and the economic case must emphasize avoided losses \(non\-revenue water, energy waste, flood damage\) rather than new revenue streams\. Third, consequence scale: an autonomous vehicle failure affects individual passengers; a water system failure can affect an entire city or region\. This asymmetry of consequences demands even more rigorous verification than automotive standards require\.

__\[Figure 3\]__ Water Systems Autonomy Levels \(WSAL\) five\-level classification\. Each level is defined by the scope of its Operational Design Domain, the role of human operators, and the required technical architecture\. The critical near\-term transition is from L2 to L3, requiring systematic in\-the\-loop verification to certify ODD boundaries\. For instance, an L2→L3 transition requires demonstrating, through systematic model\-in\-the\-loop and software\-in\-the\-loop testing, that the control system maintains safe operation across all scenarios within the defined ODD without human intervention\. Current state\-of\-the\-art implementations \(Shaping, Jiaodong\) have achieved L2 for typical scenarios\.

Most water systems globally operate at L1\. Our implementations achieved L2 for typical scenarios\. The critical near\-term challenge is the L2→L3 transition, which requires systematic in\-the\-loop verification to formally certify that HDC algorithms perform safely across a defined ODD\[16\]—establishing the evidence base needed for operators and regulators to 'let go' of manual control within certified boundaries\.

We propose a staged deployment strategy: 'point' implementations \(individual facilities, L2→L3\) provide the simplest test bed for verification methodology; 'line' implementations \(transfer systems, L2→L3→L4\) validate distributed coordination; 'area' implementations \(urban water systems, L1→L3\) test structural isomorphism across system types—for example, Fuzhou's smart water platform \(Lei et al\., 2022\)\[40\], which integrated real\-time hydraulic monitoring with dispatch optimization across an urban water supply network; and 'network' implementations \(national/basin\-scale interconnected systems, L3→L5\) address the ultimate system\-of\-systems challenge\.

__Challenges and responsible deployment__

Realizing autonomous water networks requires progress on multiple fronts beyond control algorithms\. On theory: the multi\-timescale hierarchical framework demonstrated at Jiaodong lacks formal guarantees of optimality propagation between layers and convergence of inter\-layer iterations\. The unified transfer function framework must extend from one\-dimensional systems to two\-dimensional river networks and three\-dimensional reservoirs\. And the interaction between Physical AI \(deterministic, constraint\-respecting\) and Cognitive AI \(probabilistic, creative\) requires formal safety verification—ensuring that system behaviour remains safe even when the two engines produce conflicting recommendations\[33,41,42\]\.

On standards: WSAL levels need operationalization into testable engineering criteria with defined entry and exit conditions\. ODD specifications require standardized scenario description languages covering hydrological conditions, equipment states, demand patterns, and extreme events\. In\-the\-loop testing needs certification standards analogous to DO\-178C in aviation\[35\]\. And interoperability across heterogeneous sub\-systems demands a unified semantic model—analogous to the Common Information Model \(IEC 61970\) that transformed power grid interoperability\[43,44\]\.

On governance: liability frameworks must clarify responsibility when autonomous decisions lead to adverse outcomes\. We propose that within certified ODD boundaries, responsibility is shared between system developers and operators; beyond ODD, automatic degradation to human control returns responsibility to operators\[15\]\.

On equity: autonomous water network technology must not widen existing digital divides\[34,45\]\. Three specific mechanisms can ensure equitable access\. First, open\-source control algorithms: the MPC and DMPC implementations underlying HDC should be released under permissive licenses, following the precedent of OpenFOAM in computational fluid dynamics\. Second, open verification standards: WSAL certification criteria and xIL testing protocols should be developed as ISO or IAHR open standards, freely available to all water utilities regardless of size or location\. Third, capacity\-building partnerships: technology transfer programs pairing advanced research institutions with developing\-country water utilities—modelled on the Global Water Partnership's approach—should be integral to WSAL deployment, not an afterthought\. Alignment with UN Sustainable Development Goal 6 \(clean water and sanitation\) should ensure that autonomy standards and verification methodologies are globally accessible rather than restricted to wealthy nations\[46–48\]\.

Looking ahead, recent advances in AI offer both opportunities and caution\. Foundation models show promise for zero\-shot transfer across water system types\[31,49,50\], potentially accelerating ODD expansion\. Physics\-informed neural networks may bridge the gap between data\-driven flexibility and mechanistic fidelity\[51,52\], while differentiable modelling approaches offer new pathways for unifying machine learning with physical models in geosciences\[64\]\. Digital twin platforms are maturing to support full\-lifecycle in\-the\-loop testing\[53,54\]\. Advances in data\-driven hydrology\[63\] demonstrate that machine learning can match or exceed traditional models when trained on large datasets, but deploying such approaches in safety\-critical control requires careful attention to distributional shift and interpretability\. Yet the deployment of AI in safety\-critical water infrastructure demands a level of rigour that the AI community has only begun to address\[33,34,55\]\. The lesson from aviation is clear: autonomous systems earn trust not through algorithmic sophistication alone, but through exhaustive, transparent, and independently auditable verification\[17,35\]\. Recent surveys have drawn direct parallels between water network digitalization and the automation trajectories of the automotive and aviation industries\[66\], suggesting that systematic approaches to verification and incremental deployment are essential\.

The technical foundations are advancing rapidly, but significant challenges remain in theory, standards, governance, and equity\. Meeting these challenges requires the collective commitment of the research community, industry, and policymakers\.




__References__

1\. Wang, H\., Wang, J\., Qin, D\. et al\. Theory and methodology of water resources assessment based on dualistic water cycle model\. J\. Hydraul\. Eng\. 37, 1496–1502 \(2006\)\.

2\. Lei, X\., Liao, W\., Wang, H\. et al\. Key Technologies for Dispatch and Operation of the South\-to\-North Water Diversion Middle Route \(Science Press, 2023\)\.

3\. UNESCO\. The United Nations World Water Development Report 2024: Water for Prosperity and Peace \(UNESCO, 2024\)\.

4\. Kingdom, B\., Liemberger, R\. & Marin, P\. The Challenge of Reducing Non\-Revenue Water \(NRW\) in Developing Countries\. Water Supply and Sanitation Board Discussion Paper No\. 8 \(World Bank, 2006\)\.

5\. Plusquellec, H\. Modern Water Control in Irrigation: Concepts, Issues, and Applications\. World Bank Technical Paper No\. 246 \(World Bank, 2002\)\.

6\. Loucks, D\. P\. & van Beek, E\. Water Resources Systems Planning and Management: An Introduction to Methods, Models and Applications \(Springer, 2017\)\.

7\. Biswas, A\. K\. Integrated water resources management: a reassessment\. Water Int\. 29, 248–256 \(2004\)\.

8\. SAE International\. Taxonomy and Definitions for Terms Related to Driving Automation Systems for On\-Road Motor Vehicles\. SAE Standard J3016 \(SAE International, 2021\)\.

9\. Yurtsever, E\., Lambert, J\., Carballo, A\. & Takeda, K\. A survey of autonomous driving: common practices and emerging technologies\. IEEE Access 8, 58443–58469 \(2020\)\.

10\. Maass, A\., Hufschmidt, M\. M\., Dorfman, R\. et al\. Design of Water\-Resource Systems \(Harvard Univ\. Press, 1962\)\.

11\. Rippl, W\. The capacity of storage reservoirs for water supply\. Minutes Proc\. Inst\. Civ\. Eng\. 71, 270–278 \(1883\)\.

12\. Labadie, J\. W\. Optimal operation of multireservoir systems: state\-of\-the\-art review\. J\. Water Resour\. Plan\. Manag\. 130, 93–111 \(2004\)\.

13\. Loucks, D\. P\. & Beek, E\. v\. Water resources planning and analysis: the state of play\. Water Resour\. Res\. 59, e2022WR033811 \(2023\)\.

14\. Lei, X\., Long, Y\., Xu, H\. et al\. Cybernetics of Hydro Systems: background, framework, and research paradigm\. South\-to\-North Water Transfers Water Sci\. Technol\. 23, 761–769 \(2025\)\.

15\. Lei, X\., Su, C\., Long, Y\. et al\. Architecture and key technologies for next\-generation autonomous intelligent water networks based on autonomous driving concepts\. South\-to\-North Water Transfers Water Sci\. Technol\. 23, 778–786 \(2025\)\.

16\. Lei, X\., Zhang, Z\., Su, C\. et al\. In\-the\-loop testing system for autonomous intelligent water networks\. South\-to\-North Water Transfers Water Sci\. Technol\. 23, 787–793 \(2025\)\.

17\. RTCA\. Software Considerations in Airborne Systems and Equipment Certification\. DO\-178C \(RTCA, 2011\)\.

18\. Aven, T\. Risk assessment and risk management: review of recent advances on their foundation\. Eur\. J\. Oper\. Res\. 253, 1–13 \(2016\)\.

19\. Lei, X\., Xu, H\., He, Z\. et al\. Disciplinary prospects of water resources systems analysis: from static balance to dynamic control\. South\-to\-North Water Transfers Water Sci\. Technol\. 23, 770–777 \(2025\)\.

20\. Litrico, X\. & Fromion, V\. Simplified modeling of irrigation canals for controller design\. J\. Irrig\. Drain\. Eng\. 130, 373–383 \(2004\)\.

21\. Cunge, J\. A\. On the subject of a flood propagation computation method \(Muskingum method\)\. J\. Hydraul\. Res\. 7, 205–230 \(1969\)\.

22\. Malaterre, P\.\-O\., Rogers, D\. C\. & Schuurmans, J\. Classification of canal control algorithms\. J\. Irrig\. Drain\. Eng\. 124, 3–10 \(1998\)\.

23\. Ghidaoui, M\. S\., Zhao, M\., McInnis, D\. A\. & Axworthy, D\. H\. A review of water hammer theory and practice\. Appl\. Mech\. Rev\. 58, 49–76 \(2005\)\.

24\. Wylie, E\. B\. & Streeter, V\. L\. Fluid Transients in Systems \(Prentice Hall, 1993\)\.

25\. Camacho, E\. F\. & Bordons, C\. Model Predictive Control 2nd edn \(Springer, 2007\)\.

26\. Rawlings, J\. B\., Mayne, D\. Q\. & Diehl, M\. Model Predictive Control: Theory, Computation, and Design \(Nob Hill, 2017\)\.

27\. Negenborn, R\. R\., van Overloop, P\. J\., Keviczky, T\. & De Schutter, B\. Distributed model predictive control of irrigation canals\. Netw\. Heterog\. Media 4, 359–380 \(2009\)\.

28\. Christofides, P\. D\., Scattolini, R\., Muñoz de la Peña, D\. & Liu, J\. Distributed model predictive control: a tutorial review and future research directions\. Comput\. Chem\. Eng\. 51, 21–41 \(2013\)\.

29\. Castelletti, A\., Galelli, S\., Restelli, M\. & Soncini\-Sessa, R\. Tree\-based reinforcement learning for optimal water reservoir operation\. Water Resour\. Res\. 46, W09507 \(2010\)\.

30\. Giuliani, M\., Castelletti, A\., Pianosi, F\., Mason, E\. & Reed, P\. M\. Curses, tradeoffs, and scalable management: advancing evolutionary multiobjective direct policy search\. Water Resour\. Res\. 52, 421–440 \(2016\)\.

31\. Brown, T\. et al\. Language models are few\-shot learners\. Adv\. Neural Inf\. Process\. Syst\. 33, 1877–1901 \(2020\)\.

32\. Lewis, P\. et al\. Retrieval\-augmented generation for knowledge\-intensive NLP tasks\. Adv\. Neural Inf\. Process\. Syst\. 33, 9459–9474 \(2020\)\.

33\. Richards, L\. A\. et al\. Rewards, risks and responsible deployment of artificial intelligence in water systems\. Nat\. Water 1, 422–432 \(2023\)\.

34\. Stokel\-Walker, C\. & Van Noorden, R\. What ChatGPT and generative AI mean for science\. Nature 614, 214–216 \(2023\)\.

35\. ISO\. Road Vehicles – Functional Safety\. ISO 26262 \(International Organization for Standardization, 2018\)\.

36\. Ye, S\., Wang, C\., Wang, Y\. et al\. Real\-time model predictive control study of run\-of\-river hydropower plants with data\-driven and physics\-based coupled model\. J\. Hydrol\. 618, 129250 \(2023\)\.

37\. Shandong Jiaodong Water Transfer Project Administration\. Chronicles of the Jiaodong Water Transfer Project \(Yellow River Water Conservancy Press, 2020\)\.

38\. Zhang, Z\., Lei, X\. H\., Tian, Y\. et al\. Optimized scheduling of cascade pumping stations in open\-channel water transfer systems based on station skipping\. J\. Water Resour\. Plan\. Manag\. 145, 05019011 \(2019\)\.

39\. Yan, P\. R\., Zhang, Z\., Lei, X\. H\. et al\. A multi\-objective optimal control model of cascade pumping stations considering both cost and safety\. J\. Clean\. Prod\. 345, 131171 \(2022\)\.

40\. Lei, X\., He, Z\., Long, Y\. et al\. Smart water platform construction and application in Fuzhou\. China Water Resour\. 14, 55–58 \(2022\)\.

41\. Amodei, D\. et al\. Concrete problems in AI safety\. Preprint at https://arxiv\.org/abs/1606\.06565 \(2016\)\.

42\. Russell, S\., Dewey, D\. & Tegmark, M\. Research priorities for robust and beneficial artificial intelligence\. AI Mag\. 36, 105–114 \(2015\)\.

43\. IEC\. Energy Management System Application Program Interface\. IEC 61970 \(International Electrotechnical Commission, 2005\)\.

44\. Uslar, M\. et al\. The Common Information Model CIM: IEC 61968/61970 and 62325 – A Practical Introduction to the CIM \(Springer, 2012\)\.

45\. Garrido\-Baserba, M\. et al\. Using water and wastewater decentralization to enhance the resilience and sustainability of cities\. Nat\. Water 2, 792–806 \(2024\)\.

46\. UN\-Water\. The United Nations World Water Development Report 2023: Partnerships and Cooperation for Water \(UNESCO, 2023\)\.

47\. Grafton, R\. Q\. et al\. The paradox of irrigation efficiency\. Science 361, 748–750 \(2018\)\.

48\. Sadoff, C\. W\. et al\. Rethinking water for SDG 6\. Nat\. Sustain\. 3, 346–347 \(2020\)\.

49\. Bommasani, R\. et al\. On the opportunities and risks of foundation models\. Preprint at https://arxiv\.org/abs/2108\.07258 \(2021\)\.

50\. Zhi, W\. et al\. Deep learning for water quality\. Nat\. Water 2, 228–241 \(2024\)\.

51\. Raissi, M\., Perdikaris, P\. & Karniadakis, G\. E\. Physics\-informed neural networks: a deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations\. J\. Comput\. Phys\. 378, 686–707 \(2019\)\.

52\. Karniadakis, G\. E\. et al\. Physics\-informed machine learning\. Nat\. Rev\. Phys\. 3, 422–440 \(2021\)\.

53\. Rasheed, A\., San, O\. & Kvamsdal, T\. Digital twin: values, challenges and enablers from a modeling perspective\. IEEE Access 8, 21980–22012 \(2020\)\.

54\. Bartos, M\. & Kerkez, B\. Pipedream: an interactive digital twin model for natural and urban drainage systems\. Environ\. Model\. Softw\. 144, 105120 \(2021\)\.

55\. Nearing, G\. S\. et al\. What role does hydrological science play in the age of machine learning? Water Resour\. Res\. 57, e2020WR028091 \(2021\)\.

56\. Dadson, S\. J\. et al\. A restatement of the natural science evidence concerning catchment\-based 'natural' flood management in the UK\. Proc\. R\. Soc\. A 473, 20160706 \(2017\)\.

57\. Milly, P\. C\. D\. et al\. Stationarity is dead: whither water management? Science 319, 573–574 \(2008\)\.

58\. Vörösmarty, C\. J\. et al\. Global threats to human water security and river biodiversity\. Nature 467, 555–561 \(2010\)\.

59\. Clemmens, A\. J\., Kacerek, T\. F\., Grawitz, B\. & Schuurmans, W\. Test cases for canal control algorithms\. J\. Irrig\. Drain\. Eng\. 131, 13–29 \(2005\)\.

60\. Litrico, X\. & Fromion, V\. Modeling and Control of Hydrosystems \(Springer, 2009\)\.

61\. van Overloop, P\. J\. Model Predictive Control on Open Water Systems\. PhD thesis \(TU Delft, 2006\)\.

62\. Horváth, K\. et al\. Automatic model structure and parameter selection for integrator\-delay\-zero canal gate models\. Water Resour\. Res\. 60, e2023WR036727 \(2024\)\.

63\. Kratzert, F\. et al\. Toward improved predictions in ungauged basins: exploiting the power of machine learning\. Water Resour\. Res\. 55, 11344–11354 \(2019\)\.

64\. Shen, C\. et al\. Differentiable modelling to unify machine learning and physical models for geosciences\. Nat\. Rev\. Earth Environ\. 4, 552–567 \(2023\)\.

65\. van Overloop, P\. J\. et al\. Real\-time implementation of model predictive control on Maeslant barrier\. J\. Water Resour\. Plan\. Manag\. 136, 766–768 \(2010\)\.

66\. Savic, D\. Digital water developments and lessons learned from automation in the car and aircraft industries\. Engineering 154, 102–117 \(2022\)\.

67\. Montanari, A\. et al\. 'Panta Rhei—Everything Flows': change in hydrology and society—the IAHS scientific decade 2013–2022\. Hydrol\. Sci\. J\. 58, 1256–1275 \(2013\)\.




__Acknowledgements__

This work was supported by the National Key Research and Development Program of China \(2022YFC3200500, 2023YFC3206400\) and the National Natural Science Foundation of China \(52130907\)\.

__Author contributions__

X\.L\. conceived the CHS framework, designed the study, and wrote the manuscript\. C\.J\. contributed to multi\-timescale optimization development\. C\.W\. contributed to engineering implementation\. H\.W\. provided the water resources systems analysis theoretical foundation and supervised the research\. All authors reviewed and approved the final manuscript\.

__Competing interests__

The authors declare no competing interests\.

__Data availability__

This Perspective does not report new experimental data\. All referenced data are available through the cited publications\.
