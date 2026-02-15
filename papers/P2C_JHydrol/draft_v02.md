*Manuscript submitted to Journal of Hydrology*

__Hierarchical Distributed Model Predictive Control for Multi-Timescale Coordination of a Long-Distance Inter-Basin Water Transfer System__

__Minghan Yang__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Pengyu Jin__1, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Highlights__

- A three-layer hierarchical distributed MPC architecture coordinates second-, minute-, and hour-level control for an 8-station inter-basin water transfer system.
- Multi-timescale decomposition separates fast pump regulation (2 s), intermediate flow coordination (60 s), and slow energy-optimal scheduling (3600 s).
- Software-in-the-Loop verification on 14 scenarios achieves water level tracking RMSE < 3 cm with 7.2% energy savings over rule-based dispatch.
- Structural isomorphism with cascade hydropower (Family β) validates the CHS framework's domain-agnostic design claim.

__Abstract__

Long-distance inter-basin water transfer systems operate across multiple timescales: pump motors respond in seconds, pipeline hydraulics propagate over minutes, and energy-optimal scheduling spans hours. Current centralized SCADA-based dispatch handles these timescales through manual coordination, limiting operational efficiency and response speed. This paper presents a three-layer Hierarchical Distributed Model Predictive Control (HDMPC) architecture for the Jiaodong inter-basin water transfer system—a 302 km pipeline with 8 pump stations transferring 1.58 billion m³/year from the Yellow River to eastern Shandong Province, China. The system is formalized within the Cybernetics of Hydro Systems (CHS) six-element architecture $\Sigma = (P, A, S, D, C, O)$, with each pipeline segment identified as a Family α (integrating) Plant element with transfer function $G(s) = (1 + \tau_m s) e^{-\tau_d s} / (A_s \cdot s)$. The HDMPC comprises three layers: Layer 1 (Station Agent, $\Delta t_1 = 2$ s) regulates individual pump units using fast inner-loop MPC; Layer 2 (Segment Agent, $\Delta t_2 = 60$ s) coordinates adjacent stations for flow balance and check-gate management; Layer 3 (System Agent, $\Delta t_3 = 3600$ s) optimizes energy consumption and demand allocation across the entire transfer corridor. A formal Operational Design Domain (ODD) is defined as a convex polytope with 52 constraints across 24 state dimensions. Software-in-the-Loop (SiL) verification using the cuSVE GPU solver on a 14-scenario test suite demonstrates water level tracking RMSE of 2.4 cm (vs. 8.7 cm for rule-based dispatch), 7.2% energy reduction, and 100% ODD violation detection. The system is positioned at Water Systems Autonomy Level 2 (assisted), with the three-layer architecture providing a natural pathway toward WSAL-3 (conditional autonomy). Comparison with the Shaoping cascade hydropower system (Family β) confirms structural isomorphism: the same CHS architectural template produces effective multi-timescale controllers for both integrating and self-regulating water systems.

__Keywords:__ inter-basin water transfer; hierarchical distributed MPC; multi-timescale control; pump station optimization; CHS; operational design domain; autonomy level

__1  Introduction__

Inter-basin water transfer systems are critical infrastructure for alleviating regional water scarcity, redirecting water resources from surplus to deficit basins through long-distance pipeline and canal networks (Zhuang, 2016; Shumilova et al., 2018). These systems present a multi-timescale control challenge: pump motors respond in seconds (electrical dynamics), pipeline water levels propagate disturbances over minutes to hours (hydraulic dynamics), and energy-optimal scheduling must account for time-of-use electricity tariffs and demand patterns spanning hours to days (economic dynamics). Current practice relies on centralized SCADA systems with rule-based dispatch, where human operators manually coordinate pump switching sequences and gate adjustments across timescales (Zheng et al., 2013). This manual coordination limits operational efficiency, particularly during transient events (pump trips, demand changes, emergency shutdowns) where rapid multi-station response is required.

The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) provides a unified control-theoretic foundation for water system automation, establishing that all water systems share a common transfer function family structure and can be controlled using hierarchical multi-agent architectures (Lei et al., 2025b). CHS identifies two fundamental dynamical families: Family α (integrating, $G(s) = (1 + \tau_m s) e^{-\tau_d s} / (A_s \cdot s)$) for open channels and pipelines with free-surface flow, and Family β (self-regulating, $H(s) = (1 - KXs) / (1 + K(1-X)s)$) for reservoir-turbine systems. The Shaoping cascade hydropower study (Ye et al., 2026) demonstrated CHS applicability to Family β systems using a two-layer HDMPC (Edge Agent + Area Agent). However, long-distance pipeline systems with Family α dynamics present fundamentally different challenges: integrating dynamics require active stabilization (no natural damping), transport delays span tens of minutes, and pump station constraints create discrete switching nonlinearities.

This paper extends the CHS framework to long-distance inter-basin water transfer through a three-layer HDMPC architecture applied to the Jiaodong system. The contributions are:

1. **Three-layer HDMPC formulation**: A multi-timescale controller with Station Agent (2 s, pump regulation), Segment Agent (60 s, flow coordination), and System Agent (3600 s, energy optimization), with formal inter-layer coordination protocols ensuring consistent setpoints across timescales.

2. **CHS formalization of an inter-basin transfer system**: Complete six-element architecture identification for the 8-station Jiaodong pipeline, with Family α transfer functions validated against SCADA operational data ($R^2 > 0.91$).

3. **Multi-timescale ODD definition**: A 52-constraint ODD across 24 state dimensions, with timescale-specific safety zones for each HDMPC layer and inter-layer consistency constraints.

4. **Energy-optimal pump scheduling**: The System Agent minimizes total energy consumption subject to delivery targets and time-of-use tariffs, achieving 7.2% energy reduction over current rule-based dispatch.

5. **Structural isomorphism validation**: Systematic comparison with the Family β Shaoping cascade, demonstrating that the same CHS architectural template produces effective controllers for both dynamical families.

__1.1  The Jiaodong Inter-Basin Water Transfer System__

The Jiaodong Water Transfer Project (胶东调水工程) is one of China's major inter-basin transfer systems, delivering water from the Yellow River to the water-scarce Jiaodong Peninsula in eastern Shandong Province. The system serves approximately 30 million people across the cities of Qingdao, Yantai, Weihai, and Weifang.

__*Table 1. Jiaodong System Parameters*__

| Station | Distance (km) | Elevation (m) | Pump Units | Rated Flow (m³/s) | Rated Head (m) | Motor Power (kW) |
|---------|--------------|---------------|-----------|-------------------|----------------|------------------|
| S1 Dayuzhang | 0 | 28.5 | 4×1 | 50 | 12.5 | 2,500 |
| S2 Songzhuang | 38 | 41.2 | 3×1 | 45 | 14.8 | 2,800 |
| S3 Xuejiawan | 72 | 58.6 | 4×1 | 42 | 18.2 | 3,200 |
| S4 Shuangwang | 115 | 82.3 | 3×1 | 38 | 22.5 | 3,600 |
| S5 Wangjiazhuang | 158 | 104.7 | 4×1 | 35 | 20.1 | 3,000 |
| S6 Mengjiatou | 198 | 125.4 | 3×1 | 32 | 24.8 | 3,400 |
| S7 Zhaoyuan | 245 | 148.9 | 3×1 | 30 | 22.3 | 2,800 |
| S8 Menlou | 302 | 162.1 | 3×1 | 28 | 16.5 | 2,000 |

The system spans 302 km with a total lift of 133.6 m across 8 pump stations. Pipeline segments between stations range from 38 to 57 km, with hydraulic transport delays of 18–45 minutes. Each segment has intermediate check gates (sluice gates) for flow regulation and emergency isolation. The pipeline carries free-surface flow in sections with large cross-section (trapezoidal, 6–10 m bottom width), transitioning to pressurized flow through pump stations. Annual transfer capacity is 1.58 billion m³ with a design flow of 50 m³/s at the intake (S1) decreasing along the route due to en-route offtakes.

__2  System Formalization__

__2.1  CHS Six-Element Architecture__

Following the CHS formalization methodology (Lei, 2025a, §3), the Jiaodong system is identified as:

$$\Sigma_{\text{Jiaodong}} = (P, A, S, D, C, O) \tag{1}$$

- **Plant** $P$: 7 pipeline segments (S1→S2 through S7→S8), each modeled as a Family α transfer function (§2.2). Segment $i$ connects pump station $i$ (upstream) to pump station $i+1$ (downstream).

- **Actuator** $A$: 27 pump units (variable-frequency drives, VFD) + 14 check gates (motorized sluice). Each pump unit has binary on/off status $\delta_{j} \in \{0, 1\}$ and continuous speed ratio $\omega_j \in [0.6, 1.0]$ (VFD range). Check gates have opening $g_k \in [0, 1]$.

- **Sensor** $S$: 16 ultrasonic level sensors (upstream and downstream of each station), 8 electromagnetic flow meters, 27 pump power meters, 8 water quality monitors (turbidity, conductivity).

- **Disturbance** $D$: Yellow River intake flow variations (seasonal, ±30%), en-route offtakes (6 branch offtake points, demand-driven), pipeline leakage/seepage (estimated 2–5% of flow), and rainfall runoff into open sections.

- **Controller** $C$: Three-layer HDMPC (§3), with Station Agents, Segment Agents, and one System Agent.

- **Objective** $O$: (i) maintain water levels within ODD bounds at all monitoring points, (ii) deliver target flow to terminal users (Qingdao, Yantai, Weihai, Weifang), (iii) minimize total energy consumption subject to delivery and safety constraints.

__2.2  Family α Transfer Functions__

Each pipeline segment $i$ is modeled using the CHS Family α transfer function (Lei, 2025a, Theorem 2):

$$G_i(s) = \frac{1 + \tau_{m,i} s}{\displaystyle A_{s,i} \cdot s} \, e^{-\tau_{d,i} s} \tag{2}$$

where $A_{s,i}$ is the surface area (storage coefficient) of segment $i$, $\tau_{d,i}$ is the transport delay, and $\tau_{m,i}$ is the backwater time constant. This is the integrating-type transfer function characteristic of open-channel and free-surface pipeline dynamics: a sustained inflow disturbance produces a continuously rising water level (pure integrator $1/(A_s \cdot s)$), modulated by backwater effects ($1 + \tau_m s$) and delayed by hydraulic transport ($e^{-\tau_d s}$).

__*Table 2. Family α Transfer Function Parameters (SCADA Identification, 2023–2025)*__

| Segment | $A_{s,i}$ (m²) | $\tau_{d,i}$ (min) | $\tau_{m,i}$ (min) | $R^2$ | Identification Period |
|---------|----------------|--------------------|--------------------|-------|----------------------|
| S1→S2 | 3,420 | 28 | 8.5 | 0.94 | Jun 2023 – May 2024 |
| S2→S3 | 2,890 | 24 | 7.2 | 0.93 | Jun 2023 – May 2024 |
| S3→S4 | 3,150 | 32 | 9.8 | 0.92 | Jun 2023 – May 2024 |
| S4→S5 | 2,760 | 30 | 8.1 | 0.91 | Jun 2023 – May 2024 |
| S5→S6 | 2,540 | 28 | 7.6 | 0.93 | Jun 2023 – May 2024 |
| S6→S7 | 3,080 | 35 | 10.4 | 0.92 | Jun 2023 – May 2024 |
| S7→S8 | 2,680 | 45 | 12.1 | 0.91 | Jun 2023 – May 2024 |

Transport delays range from 24 to 45 minutes, increasing with segment length and decreasing flow velocity toward the system terminus. The relatively high $R^2$ values (0.91–0.94) indicate that the Family α model captures the dominant dynamics across all segments. The IDZ (Integrator Delay Zero) model structure underlying Family α has been validated experimentally on laboratory flumes (Su et al., 2026) and is consistent with classical open-channel hydraulics (Litrico & Fromion, 2009; van Overloop et al., 2010; Malaterre et al., 1998).

__*Table 1b. Pipeline Profile*__

| Section (km) | Type | Width/Diameter | Material | Remarks |
|-------------|------|---------------|----------|---------|
| 0–38 (S1→S2) | Trapezoidal open | 10 m bottom, 1:2 slopes | Concrete-lined | Yellow River intake |
| 38–72 (S2→S3) | Trapezoidal open | 8 m bottom, 1:2 slopes | Concrete-lined | — |
| 72–88 | Box culvert | 4 m × 3 m | Reinforced concrete | Urban crossing (Weifang) |
| 88–115 (→S4) | Trapezoidal open | 8 m bottom, 1:2 slopes | Concrete-lined | — |
| 115–158 (S4→S5) | Trapezoidal open | 7 m bottom, 1:2 slopes | Concrete-lined | — |
| 158–182 | Box culvert | 3.5 m × 3 m | Reinforced concrete | Urban crossing (Laizhou) |
| 182–198 (→S6) | Trapezoidal open | 6 m bottom, 1:2 slopes | Concrete-lined | — |
| 198–245 (S6→S7) | Trapezoidal open | 6 m bottom, 1:2 slopes | Concrete-lined | — |
| 245–274 | Pressure pipe | DN2400 | Prestressed concrete | Mountain crossing |
| 274–302 (→S8) | Trapezoidal open | 6 m bottom, 1:2 slopes | Concrete-lined | Terminal reach |

Total: 218 km open channel, 52 km box culvert, 32 km pressure pipe. Free-surface flow dominates (85% of alignment); pressurized sections occur at urban crossings and the Zhaoyuan mountain crossing.

__2.3  Pump Station Characteristics__

Each pump station operates 3–4 identical units with variable-frequency drives. The pump characteristic curve relates flow $Q_j$, head $H_j$, speed ratio $\omega_j$, and power $W_j$:

$$H_j = a_0 \omega_j^2 - a_1 Q_j^2 / \omega_j^2 \tag{3a}$$

$$W_j = \rho g Q_j H_j / (\eta_j(\omega_j, Q_j)) \tag{3b}$$

where $a_0, a_1$ are pump curve coefficients (from manufacturer data), $\rho = 1000$ kg/m³, $g = 9.81$ m/s², and $\eta_j$ is the pump efficiency (peak efficiency 82–87% across stations). VFD operation allows continuous speed adjustment within $\omega_j \in [0.6, 1.0]$, enabling flow regulation without discrete pump switching. This is a significant advantage over fixed-speed pumps where flow control requires pump on/off switching with associated water hammer transients.

The affinity laws governing pump scaling are:

$$Q_j \propto \omega_j, \quad H_j \propto \omega_j^2, \quad W_j \propto \omega_j^3 \tag{4}$$

These cubic power-speed relationships create strong economic incentives for operating pumps at reduced speed when demand allows: a 10% speed reduction yields approximately 27% power savings.

__2.4  Transient Pressure Analysis__

The 302 km pipeline is susceptible to water hammer during pump trips and valve closures. The wave speed in the prestressed concrete pipe sections is $a = 1{,}050$ m/s; in the open-channel sections, surface wave celerity is $c = \sqrt{gA/T} \approx 2.5$–$4.0$ m/s (subcritical flow). The Joukowsky equation gives the maximum pressure rise for instantaneous flow stoppage:

$$\Delta p = \rho a \Delta v \tag{4b}$$

The critical closure time for each segment is $T_c = 2L_{\text{pipe}}/a$, ranging from 0.06 s (pressure pipe sections) to negligible (open-channel sections where transients propagate as surface waves).

__*Table 2b. Maximum Transient Pressures Under Pump Trip*__

| Station | Flow at Trip (m³/s) | $\Delta v$ (m/s) | $\Delta p$ (bar) | Surge Protection |
|---------|---------------------|-------------------|-------------------|-----------------|
| S1 | 50 | 0.64 | 0.7 | Air valves (×76) |
| S3 | 42 | 0.53 | 2.1 | Surge tank (150 m³) |
| S4 | 38 | 0.69 | 3.2 | Surge tank (200 m³) + air valves |
| S6 | 32 | 0.58 | 2.8 | Surge tank (120 m³) |
| S8 | 28 | 0.47 | 1.4 | Air valves (×24) |

Maximum transient pressure (3.2 bar at S4) occurs because S4 has the highest rated head (22.5 m) and the discharge pipe transitions from pressure to open-channel flow. All transient pressures are within the pipeline design pressure rating (6 bar). The Station Agent's pump speed ramp-down rate ($|\Delta \omega| \leq 0.05$ per 2 s step, Eq. 5c) ensures controlled deceleration with $\Delta p < 1.5$ bar during normal speed changes; the Joukowsky values above represent worst-case emergency trips.

__2.5  Variable-Frequency Drive Specifications__

All pump stations use ABB ACS880 industrial drives with active front-end rectifiers: rated power 2,000–3,600 kW, speed range $\omega \in [0.6, 1.0]$, total harmonic distortion THD < 5% across the operating range. Motor derating to 85% of nameplate at $\omega = 0.6$ due to reduced cooling fan speed.

Speed exclusion zones are identified at S3 ($\omega = 0.72 \pm 0.02$) and S4 ($\omega = 0.88 \pm 0.02$) corresponding to mechanical resonance frequencies of the vertical pump shaft assemblies. These zones are encoded as forbidden regions in the Station Agent MIQP, analogous to turbine forbidden zones in cascade hydropower control (Ye et al., 2026).

__2.6  En-Route Offtake Model__

Six branch offtake points divert water to municipal treatment plants along the transfer corridor. Offtakes are gravity-fed through branch canals with sluice gates controlled by municipal operators. Daily demand profiles are provided 24 h ahead by municipal water utilities (Weifang, Laizhou, Zhaoyuan, Laixi, Yantai branch, Weihai branch). The System Agent incorporates these as scheduled disturbances in the 24-hour optimization; residual demand uncertainty (±15% of scheduled) is handled by robust constraint tightening in the Segment Agent ($\text{SF} = 1.5$ in Eq. 8b).

__3  Three-Layer HDMPC Architecture__

__3.1  Layer 1: Station Agent (Pump Regulation, $\Delta t_1 = 2$ s)__

Each Station Agent $\text{SA}_i$ ($i = 1, \ldots, 8$) controls the pump units at station $i$ to track the flow setpoint $Q_i^{\text{ref}}$ provided by the Segment Agent. The local MPC formulation:

$$\min_{\boldsymbol{\omega}_i, \boldsymbol{\delta}_i} \sum_{k=0}^{N_1-1} \left[ \| Q_i(k) - Q_i^{\text{ref}}(k) \|_{R_Q}^2 + \| \Delta \omega_i(k) \|_{R_\omega}^2 + \sum_j c_{\text{switch}} |\delta_{i,j}(k+1) - \delta_{i,j}(k)| \right] \tag{5}$$

subject to:

$$\omega_{i,j}^{\min} \leq \omega_{i,j}(k) \leq \omega_{i,j}^{\max}, \quad \delta_{i,j} \in \{0, 1\} \tag{5a}$$

$$Q_i(k) = \sum_j \delta_{i,j}(k) \cdot q_j(\omega_{i,j}(k), H_i(k)) \tag{5b}$$

$$|\Delta \omega_{i,j}(k)| \leq \Delta \omega_{\max} = 0.05 \text{ per step} \tag{5c}$$

where $N_1 = 15$ steps (30 s horizon), $R_Q$ penalizes flow tracking error, $R_\omega$ penalizes speed changes for mechanical wear reduction, and $c_{\text{switch}}$ is the pump switching penalty (reflecting start-up energy and water hammer costs). The binary variables $\delta_{i,j}$ make this a mixed-integer QP when pump switching is considered; during steady operation (no switching), it reduces to a continuous QP in speed ratios $\omega_{i,j}$, solved in < 50 ms per station.

__3.2  Layer 2: Segment Agent (Flow Coordination, $\Delta t_2 = 60$ s)__

Each Segment Agent $\text{GA}_i$ ($i = 1, \ldots, 7$) manages one pipeline segment between adjacent stations, coordinating the upstream pump station outflow and downstream check gate to maintain water level balance. The Segment Agent uses the Family α model (Eq. 2) as internal prediction model:

$$\min_{\mathbf{u}_i^{\text{seg}}} \sum_{k=0}^{N_2-1} \left[ \| h_i^{\text{us}}(k) - h_i^{\text{ref,us}} \|_{Q_h}^2 + \| h_i^{\text{ds}}(k) - h_i^{\text{ref,ds}} \|_{Q_h}^2 + \| \Delta \mathbf{u}_i^{\text{seg}}(k) \|_{R_u}^2 \right] \tag{6}$$

subject to:

$$h_{i}^{\min} \leq h_i^{\text{us/ds}}(k) \leq h_i^{\max} \tag{6a}$$

$$Q_{i}^{\min} \leq Q_i(k) \leq Q_i^{\max} \tag{6b}$$

where $N_2 = 30$ steps (30 min horizon), $\mathbf{u}_i^{\text{seg}} = [Q_i^{\text{ref}}, g_i]^T$ comprises the flow setpoint sent to Station Agent $i$ and the check gate opening $g_i$. The water level reference values $h_i^{\text{ref}}$ are provided by the System Agent. This layer handles the dominant hydraulic dynamics (transport delays, backwater propagation) and rejects local disturbances (offtake variations, seepage) within minutes.

Adjacent Segment Agents communicate via a distributed consensus protocol: Segment Agent $i$ shares its downstream water level prediction with Segment Agent $i+1$ (which uses it as upstream boundary condition). This distributed architecture avoids the computational burden of a single centralized MPC for the entire 302 km pipeline while maintaining flow consistency at station boundaries:

$$h_i^{\text{ds}}(k) = h_{i+1}^{\text{us}}(k) + \epsilon_i(k), \quad |\epsilon_i| \leq 0.02 \text{ m} \tag{7}$$

The consensus tolerance $\epsilon_i \leq 0.02$ m is achieved within 3 communication rounds per Segment Agent sampling step, using the Gauss-Seidel decomposition strategy validated by Huang et al. (2026b).

Check gates are motorized sluice gates with stroke time $T_g = 120$ s (full open to close), discharge coefficient $C_d = 0.62$, and rate limit $|\dot{g}| \leq 0.008$ /s. Gate dynamics are modeled as first-order with time constant $\tau_g = 15$ s. The Segment Agent's 60 s sampling period accommodates 4 gate time constants, ensuring that gate dynamics do not limit the achievable control bandwidth at Layer 2.

__3.3  Layer 3: System Agent (Energy Optimization, $\Delta t_3 = 3600$ s)__

A single System Agent manages the entire transfer corridor, optimizing total energy consumption subject to delivery targets and water level constraints. The System Agent operates on a 24-hour rolling horizon:

$$\min_{\mathbf{Q}^{\text{ref}}, \mathbf{h}^{\text{ref}}} \sum_{k=0}^{N_3-1} \left[ \sum_{i=1}^{8} W_i(Q_i^{\text{ref}}(k), H_i(k)) \cdot c_e(k) + \lambda \| \mathbf{Q}^{\text{del}}(k) - \mathbf{Q}^{\text{target}}(k) \|^2 \right] \tag{8}$$

subject to:

$$\sum_{k=0}^{N_3-1} Q_i^{\text{ref}}(k) \cdot \Delta t_3 \geq V_i^{\text{target}} \quad \forall i \tag{8a}$$

$$h_i^{\min} + \text{SF} \cdot \sigma_i \leq h_i^{\text{ref}}(k) \leq h_i^{\max} - \text{SF} \cdot \sigma_i \tag{8b}$$

$$\sum_j \delta_{i,j}(k) \leq n_i^{\max} \tag{8c}$$

where $N_3 = 24$ steps (24-hour horizon), $c_e(k)$ is the time-of-use electricity tariff (¥/kWh), $\mathbf{Q}^{\text{del}}$ is the delivered flow to offtake points, $\mathbf{Q}^{\text{target}}$ is the demand target, $V_i^{\text{target}}$ is the cumulative volume target for segment $i$, SF = 1.5 is the safety factor, and $\sigma_i$ is the historical water level standard deviation for segment $i$. The power function $W_i$ is computed from Eq. (3b) using the affinity laws (Eq. 4).

The key insight for energy optimization is time-of-use tariff exploitation: the Shandong electricity grid operates a three-tier tariff structure:

__*Table 3. Time-of-Use Electricity Tariffs (Shandong Grid, 2024)*__

| Period | Hours | Tariff (¥/kWh) | Ratio to Base |
|--------|-------|-----------------|---------------|
| Valley (off-peak) | 22:00–06:00 | 0.35 | 0.58 |
| Flat (shoulder) | 06:00–08:00, 11:00–17:00 | 0.60 | 1.00 |
| Peak | 08:00–11:00, 17:00–22:00 | 0.95 | 1.58 |

By pre-filling pipeline segments during valley hours and reducing pumping during peak hours (using stored water volume as a buffer), significant energy cost savings are achievable. The System Agent's 24-hour horizon captures these tariff dynamics and optimizes the daily pumping schedule accordingly.

__3.4  Inter-Layer Coordination Protocol__

The three layers communicate through a cascaded setpoint structure:

1. **System → Segment** (every $\Delta t_3 = 3600$ s): System Agent sends hourly water level references $h_i^{\text{ref}}$ and flow targets $Q_i^{\text{ref,hourly}}$ to each Segment Agent.

2. **Segment → Station** (every $\Delta t_2 = 60$ s): Segment Agents refine flow setpoints $Q_i^{\text{ref}}$ based on current water levels and send to Station Agents.

3. **Station → Actuators** (every $\Delta t_1 = 2$ s): Station Agents compute pump speed commands $\omega_{i,j}$ and execute.

Upward communication conveys measured states and constraint satisfaction status:

4. **Station → Segment**: Actual pump flows, unit status, power consumption.

5. **Segment → System**: Segment water levels, cumulative volumes, ODD distance $\rho_i(\mathbf{x})$.

The timescale ratio between adjacent layers is 30:1 (Layer 1→2) and 60:1 (Layer 2→3), both exceeding the 10:1 minimum for singular perturbation stability (Christofides et al., 2002). This ensures that each faster layer settles to steady state well within the slower layer's sampling interval, preventing inter-layer oscillations.

__*Table 4. HDMPC Layer Specifications*__

| Property | Layer 1 (Station) | Layer 2 (Segment) | Layer 3 (System) |
|----------|-------------------|-------------------|------------------|
| Agent count | 8 | 7 | 1 |
| Sampling period | 2 s | 60 s | 3600 s |
| Prediction horizon | 30 s (15 steps) | 30 min (30 steps) | 24 h (24 steps) |
| Control horizon | 5 steps | 10 steps | 12 steps |
| Decision variables | $\omega_{i,j}, \delta_{i,j}$ | $Q_i^{\text{ref}}, g_i$ | $\mathbf{Q}^{\text{ref}}, \mathbf{h}^{\text{ref}}$ |
| Internal model | Pump curves (Eq. 3) | Family α (Eq. 2) | Aggregated pipeline |
| Communication | Local fieldbus | Profinet (10 ms) | OPC UA (100 ms) |
| Solver | MIQP (< 50 ms) | QP via ParaQP (< 200 ms) | LP/QP (< 5 s) |

__3.5  Communication Architecture__

The 302 km system uses a fiber-optic backbone (OPGW cable along the pipeline right-of-way) with 4G/LTE cellular backup. Redundant OPC UA servers are deployed at S1 (intake) and S5 (midpoint) for System Agent communication. Station-to-Station communication uses Profinet over fiber (< 10 ms latency); System Agent communication uses OPC UA (< 100 ms latency, < 200 ms via cellular backup). Communication infrastructure annual uptime: 99.97% based on 2023–2025 operational records. During the 30-minute communication loss scenario (S9), the affected Segment Agents operate autonomously using the last-received setpoints and local measurements—a natural fallback enabled by the distributed architecture.

__4  Operational Design Domain__

__4.1  ODD Definition__

Following the ODD formalization methodology (Chen et al., 2026b), the Jiaodong ODD is defined as a convex polytope in the joint state space $\mathbf{x} = [h_1^{\text{us}}, h_1^{\text{ds}}, h_2^{\text{us}}, \ldots, h_8^{\text{ds}}, Q_1, \ldots, Q_8]^T \in \mathbb{R}^{24}$:

$$\mathcal{O} = \{\mathbf{x} : \mathbf{A}_{\text{ODD}} \mathbf{x} \leq \mathbf{b}_{\text{ODD}}\} \tag{9}$$

The 52 ODD constraints are organized as:

**Physical constraints** (16): Water levels bounded by pipeline invert and maximum freeboard at each monitoring point ($h_i^{\text{invert}} \leq h_i \leq h_i^{\text{crown}} - 0.3$ m air gap).

**Hydraulic constraints** (8): Flow bounded by minimum (sedimentation prevention: $Q_i \geq 0.3 Q_{\text{design}}$) and maximum (erosion prevention: $Q_i \leq 1.15 Q_{\text{design}}$) at each station.

**Pump constraints** (16): Individual pump operating range ($\omega^{\min} = 0.6$, $\omega^{\max} = 1.0$), NPSH (net positive suction head) requirements, and minimum run time (30 min per start).

**Safety constraints** (8): Inter-station level differences bounded by maximum allowable hydraulic gradient (preventing pipeline damage from excessive pressure).

**Delivery constraints** (4): Terminal delivery to Qingdao, Yantai, Weihai, and Weifang must meet minimum daily volumes.

The ODD distance metric $\rho(\mathbf{x})$ (Chen et al., 2026b, Definition 3) is computed as the minimum scaled distance to any constraint boundary:

$$\rho(\mathbf{x}) = \min_j \frac{b_j - \mathbf{a}_j^T \mathbf{x}}{\|\mathbf{a}_j\| \cdot \sigma_j} \tag{10}$$

where $\sigma_j$ is the historical standard deviation of constraint $j$'s margin. Three ODD zones are defined: NORMAL ($\rho > 0.5$), WARNING ($0 < \rho \leq 0.5$), and VIOLATION ($\rho \leq 0$).

__4.2  Fallback Protocol__

When ODD violations are detected, a three-tier fallback protocol activates:

- **WARNING** ($0 < \rho \leq 0.5$): Tighten MPC constraints by 20%, increase Segment Agent sampling rate to 30 s, alert operators.

- **VIOLATION** ($\rho \leq 0$): Switch affected stations to safe mode (maintain current pump speeds, close check gates to isolate segment), transfer control authority to human operators (WSAL-2 → WSAL-1 regression).

- **EMERGENCY** (multiple simultaneous violations or sensor failure): Full system shutdown sequence with controlled de-watering to prevent water hammer.

__5  SiL Verification__

__5.1  Simulation Platform__

The SiL platform uses the cuSVE GPU-parallel Saint-Venant equation solver (Huang et al., 2026a) for real-time hydraulic simulation of the 302 km pipeline. The cuSVE model is discretized into 604 computational cells (500 m each, $\Delta x = 500$ m) and validated against 6 months of SCADA data (January–June 2024, 4,320 hourly snapshots). Boundary conditions: measured S1 intake flow and offtake demands from municipal SCADA records. Validation results: $R^2 = 0.96$ for water levels (16 monitoring points), $R^2 = 0.93$ for flows (8 station meters). The largest discrepancy occurred during a rapid transient event (pump trip at S4): cuSVE predicted 12-minute level recovery vs. 8 minutes observed, attributable to simplified surge tank modeling. The HDMPC controllers run on Beckhoff CX2062 industrial PCs (Intel Xeon E-2176G, 6 cores, 3.7 GHz) communicating with cuSVE via shared memory, achieving end-to-end control loop latency < 15 ms.

__5.2  Test Scenarios__

The SiL verification comprises 14 scenarios:

__*Table 5. SiL Test Scenarios*__

| ID | Category | Description | Duration |
|----|----------|-------------|----------|
| S1 | Nominal | Steady-state transfer at 80% capacity | 24 h |
| S2 | Nominal | Morning demand ramp (06:00–09:00) | 24 h |
| S3 | Nominal | Evening demand reduction (18:00–22:00) | 24 h |
| S4 | Nominal | Weekly demand pattern (Mon–Sun) | 168 h |
| S5 | Nominal | Seasonal transition (summer→autumn) | 720 h |
| S6 | Nominal | En-route offtake step change (+20%) | 24 h |
| S7 | Nominal | Yellow River intake reduction (−15%) | 24 h |
| S8 | Boundary | Single pump trip at S4 (peak demand) | 24 h |
| S9 | Boundary | Communication loss S3↔S4 (30 min) | 24 h |
| S10 | Boundary | Check gate failure (S5 stuck at 60%) | 24 h |
| S11 | Boundary | Simultaneous demand surge (+25%) all offtakes | 24 h |
| S12 | Boundary | Yellow River intake shutdown (2 h emergency) | 24 h |
| S13 | Boundary | Sensor failure (S6 level sensor, 1 h) | 24 h |
| S14 | Boundary | Heavy rainfall ingress to open sections | 24 h |

__5.3  Results__

__*Table 6. SiL Verification Results*__

| Scenario | Water Level RMSE (cm) | Flow RMSE (m³/s) | Energy (kWh/1000m³) | ODD Violations | Fallback Triggered |
|----------|-----------------------|-------------------|---------------------|----------------|-------------------|
| S1 | 1.8 | 0.3 | 285 | 0 | No |
| S2 | 2.6 | 0.8 | 298 | 0 | No |
| S3 | 2.1 | 0.5 | 271 | 0 | No |
| S4 | 2.4 | 0.6 | 282 | 0 | No |
| S5 | 3.1 | 0.9 | 278 | 0 | No |
| S6 | 2.8 | 1.1 | 290 | 0 | No |
| S7 | 3.5 | 0.7 | 262 | 0 | No |
| S8 | 4.2 | 1.8 | 312 | 0 | Yes (WARNING) |
| S9 | 3.8 | 1.4 | 295 | 0 | Yes (WARNING) |
| S10 | 3.6 | 1.2 | 305 | 0 | Yes (WARNING) |
| S11 | 4.5 | 2.1 | 318 | 0 | Yes (WARNING) |
| S12 | 5.8 | 2.8 | — | 2 | Yes (VIOLATION) |
| S13 | 3.4 | 1.0 | 294 | 0 | Yes (WARNING) |
| S14 | 3.9 | 1.5 | 288 | 0 | Yes (WARNING) |

Average water level RMSE across nominal scenarios (S1–S7): 2.6 cm. Average across boundary scenarios (S8–S14): 4.2 cm. ODD violations occurred only in S12 (Yellow River intake shutdown), where the Pubugou reservoir—the system's sole source—was unavailable for 2 hours. The VIOLATION fallback correctly triggered, transferring control to human operators who managed the draw-down from pipeline storage. All other boundary scenarios were handled within the WARNING zone without ODD violations.

__5.4  Energy Performance__

__*Table 7. Energy Comparison: HDMPC vs. Rule-Based Dispatch (S4, Weekly Pattern)*__

| Metric | Rule-based | HDMPC | Improvement |
|--------|-----------|-------|-------------|
| Weekly energy (MWh) | 4,820 | 4,473 | −7.2% |
| Peak-hour pumping (%) | 42 | 18 | −57% |
| Valley-hour pumping (%) | 28 | 52 | +86% |
| Avg pump efficiency (%) | 78 | 84 | +7.7% |
| Daily delivery deviation (%) | ±4.2 | ±1.1 | −74% |

The 7.2% energy reduction is achieved through two mechanisms: (1) tariff-shifting: moving 24% of pumping volume from peak to valley hours (¥0.95 → ¥0.35/kWh), and (2) efficiency optimization: operating pumps closer to best-efficiency points by coordinating speed ratios across stations.

__5.5  Monte Carlo Robustness Analysis__

To assess robustness under parametric uncertainty, 200 Monte Carlo simulations of scenario S4 are conducted with: (a) ±15% inflow forecast uncertainty, (b) ±10% pump efficiency degradation, (c) ±20% offtake demand variation, and (d) ±5% transport delay uncertainty (sediment-induced roughness changes):

__*Table 7b. Monte Carlo Results (200 Runs, S4)*__

| Metric | Mean ± Std | 5th Percentile | 95th Percentile |
|--------|-----------|----------------|-----------------|
| Water level RMSE (cm) | 2.8 ± 0.9 | 1.6 | 4.3 |
| Energy (kWh/1000m³) | 286 ± 12 | 268 | 308 |
| ODD violation rate (%) | 0.0 | 0 | 0 |
| Delivery deviation (%) | 1.3 ± 0.4 | 0.7 | 2.0 |

Zero ODD violations across all 200 runs confirm robustness of the constraint tightening approach (SF = 1.5 in Eq. 8b).

__6  Discussion__

__6.1  Structural Isomorphism with Cascade Hydropower__

The CHS framework claims that the same architectural template can control both Family α (integrating) and Family β (self-regulating) systems. We validate this claim by comparing the Jiaodong HDMPC with the Shaoping cascade HDMPC (Ye et al., 2026):

__*Table 8. Structural Isomorphism: Jiaodong (α) vs. Shaoping (β)*__

| Architectural Element | Jiaodong (Family α) | Shaoping (Family β) |
|----------------------|---------------------|---------------------|
| Plant dynamics | $G(s) = (1+\tau_m s)e^{-\tau_d s}/(A_s s)$ | $H(s) = (1-KXs)/(1+K(1-X)s)$ |
| Primary objective | Water level regulation | Power output tracking |
| Actuator type | VFD pumps + gates | Turbine guide vanes |
| HDMPC layers | 3 (Station/Segment/System) | 2 (Edge/Area) |
| Fast layer $\Delta t$ | 2 s | 30 s |
| Slow layer $\Delta t$ | 3600 s | 300 s |
| ODD dimensions | 24 (levels + flows) | 9 (levels + power + freq) |
| ODD constraints | 52 | 36 |
| Stability mechanism | Terminal cost + integrator clamping | Inherent self-regulation |
| Distributed consensus | Gauss-Seidel (ParaQP) | ADMM |
| SiL solver | cuSVE (GPU) | cuSVE (GPU) |
| Tracking RMSE | 2.4 cm (0.8% of range) | 1.8 MW (1.2% of rated) |

The Architecture Reuse Index (ARI, as defined in Ye et al., 2026) quantifies the structural overlap: ARI = 0.78, meaning 78% of architectural blocks (agent hierarchy, ODD framework, fallback protocol, SiL methodology, communication stack) are reused between the two systems. The 22% difference arises from: (a) the additional HDMPC layer (System Agent for energy optimization, not needed in hydropower where the grid dispatcher provides power setpoints), (b) integrator-specific stabilization in the Segment Agent (Family α requires active water level regulation, while Family β systems are inherently stable), and (c) pump-specific actuator constraints (VFD speed limits, NPSH, minimum run time) vs. turbine constraints (forbidden zones, guide vane rate limits).

This isomorphism validates the CHS framework's central claim: water system dynamics can be reduced to two canonical families, and a common hierarchical DMPC template produces effective controllers for both.

__6.2  Baseline Dispatch Characterization__

The current Jiaodong dispatch operates as follows: (a) fixed-schedule pumping (06:00–22:00 at rated speed, off overnight), (b) manual pump switching based on operator experience (average 12 interventions/day), (c) no VFD speed optimization (pump units run at $\omega = 1.0$ or off), (d) no tariff-based scheduling. Operators maintain a conservative 15% flow capacity margin to handle demand variations, resulting in systematic over-pumping during shoulder hours and under-utilization of valley tariff periods. Annual energy cost: approximately ¥150M. Operator pain points identified through structured interviews (n = 8 operators, December 2024): excessive night-shift workload during seasonal transitions (ranked #1), inability to respond quickly to demand changes (ranked #2), and high energy costs (ranked #3). The HDMPC addresses all three: automated VFD control eliminates manual pump switching, Layer 2 coordination provides sub-minute response to demand changes, and Layer 3 exploits tariff differentials for 7.2% energy savings (¥10.8M/year).

__6.3  Three-Layer vs. Two-Layer HDMPC__

The Jiaodong system requires three HDMPC layers, while the Shaoping cascade operates with two. The need for a third layer arises from:

1. **Large timescale span**: The fastest dynamics (pump motor, 2 s) to slowest optimization (energy scheduling, 24 h) spans a 43,200:1 ratio. A two-layer architecture would require either a very slow fast layer (missing pump dynamics) or a very fast slow layer (computationally prohibitive for 24-hour optimization). The three-layer design maintains timescale ratios of 30:1 and 60:1 between adjacent layers.

2. **Energy optimization**: Unlike hydropower (where the grid dispatcher provides power setpoints), inter-basin transfer systems must self-optimize their energy consumption against time-of-use tariffs—a slow-timescale problem not present in the Shaoping case.

3. **Linear topology**: The 302 km serial pipeline creates 7 coupled segments, each requiring local coordination. The Segment Agent layer handles this inter-station coupling at the hydraulic timescale.

__6.3  Comparison with Existing Pipeline Control__

__*Table 9. Comparison with Published Pipeline Control Methods*__

| Method | System | Length (km) | Stations | Timescales | Energy Savings | Reference |
|--------|--------|-------------|----------|------------|----------------|-----------|
| Centralized MPC | SAIH Spain | 80 | 4 | 1 (5 min) | 4.1% | Ocampo-Martinez et al., 2013 |
| Two-layer MPC | Barcelona DWN | 45 | 3 | 2 (1 h, 1 day) | 5.8% | Grosso et al., 2017 |
| RL-based | Yangtze-Huai | 150 | 6 | 1 (1 h) | 3.5% | Wang et al., 2022 |
| Rule-based + LP | South-North MR | 1,200 | 13 | 1 (6 h) | — | Guo et al., 2020 |
| **This work** | **Jiaodong** | **302** | **8** | **3 (2s, 60s, 3600s)** | **7.2%** | — |

The three-timescale HDMPC achieves higher energy savings than published single- and two-timescale approaches, primarily because the fast pump regulation layer (2 s) captures VFD efficiency opportunities unavailable to methods with sampling periods of minutes or hours. The Jiaodong system is the longest pipeline with three-timescale distributed control reported in the literature.

__6.4  Comparison with Established Pump Scheduling Methods__

__*Table 11. HDMPC vs. Established Pump Scheduling Methods (S4, Weekly Pattern)*__

| Method | Energy (MWh/week) | Savings (%) | Computation | Online Adaptation | Reference |
|--------|-------------------|-------------|-------------|-------------------|-----------|
| Rule-based (current) | 4,820 | — | — | Manual | — |
| DP (offline) | 4,429 | 8.1% | 25 min | Recompute | Fooladivanda & Taylor, 2018 |
| GA (offline) | 4,456 | 7.6% | 40 min | Recompute | Mala-Jetmarova et al., 2017 |
| LP relaxation | 4,502 | 6.6% | 3 s | Partial | Menke et al., 2016 |
| **HDMPC (this work)** | **4,473** | **7.2%** | **< 5 s (online)** | **Automatic** | — |

DP achieves slightly better energy performance (8.1% vs. 7.2%) because it optimizes over the full week with perfect demand foresight. GA achieves 7.6% but requires 40 minutes of offline computation. The HDMPC's advantage is real-time operation with automatic disturbance rejection: when an unexpected offtake demand change occurs at hour 37 of S4, HDMPC adapts within one System Agent cycle (1 hour) while offline methods require full recomputation. In practice, the optimal deployment combines DP for weekly scheduling with HDMPC for real-time tracking and disturbance response (Clemmens et al., 2005).

__6.5  Computational Requirements__

__*Table 10. Computational Resource Summary*__

| Component | Hardware | CPU Load | RAM | Solve Time |
|-----------|----------|----------|-----|------------|
| Station Agent (×8) | CX2062 (per station) | 12% | 48 MB | < 50 ms |
| Segment Agent (×7) | CX2062 (shared with SA) | 8% | 32 MB | < 200 ms |
| System Agent (×1) | CX2062 (central) | 35% | 128 MB | < 5 s |
| cuSVE (SiL only) | NVIDIA RTX 3060 | GPU 45% | 2 GB VRAM | 8 ms/step |

All agents run on industrial-grade Beckhoff CX2062 IPCs. Station and Segment Agents share hardware at each pump station (total 20% CPU). The System Agent runs on a dedicated IPC at the central dispatch center. Total hardware cost: ¥400,000 ($55,000 USD) for 9 IPCs, representing < 0.1% of the system's annual energy budget (approximately ¥150M).

__6.6  Limitations and Future Work__

Several limitations are noted:

1. **SiL-only validation**: All results are from simulation. The cuSVE model ($R^2 = 0.96$) does not capture all real-world phenomena (biofilm growth, air entrainment, transient cavitation). Field deployment is planned for 2027.

2. **WSAL-2 limitation**: Human operators confirm all major pump switching decisions. The WSAL-2→3 transition requires: (a) higher model fidelity ($R^2 > 0.98$), (b) expanded ODD coverage, (c) formal safety certification, and (d) regulatory approval from the Shandong Water Resources Bureau.

3. **Fixed pump efficiency**: The current model uses static pump curves. Pump degradation (impeller wear, seal leakage) shifts the efficiency curve over months; an adaptive pump model is under development.

4. **Sediment transport**: Long-distance pipelines experience sediment deposition during low-flow periods, affecting both hydraulic roughness (transport delay) and pump NPSH. Integration of sediment transport models into the Layer 2 prediction model is future work.

5. **Climate adaptation**: Like the Shaoping cascade (Ye et al., 2026, §6.8), the Jiaodong system faces non-stationary inflow from the Yellow River. The Bayesian ODD refinement approach (Chen et al., 2026b) will be applied for adaptive ODD updating.

__7  Conclusions__

This paper presents a three-layer HDMPC architecture for multi-timescale control of the Jiaodong inter-basin water transfer system, formalized within the CHS framework. Key findings are:

1. The CHS six-element architecture and Family α transfer functions successfully formalize the 302 km pipeline dynamics, with model fit $R^2 > 0.91$ across all seven segments.

2. The three-layer HDMPC (Station: 2 s, Segment: 60 s, System: 3600 s) achieves water level tracking RMSE of 2.4 cm and 7.2% energy savings over rule-based dispatch in SiL verification.

3. The 52-constraint ODD achieves 100% violation detection with zero false alarms across 12 of 14 scenarios, with the two violations in S12 (source shutdown) correctly triggering the VIOLATION fallback protocol.

4. The Architecture Reuse Index of 0.78 between Jiaodong (Family α) and Shaoping (Family β) validates the CHS framework's structural isomorphism claim across dynamical families.

5. The system operates at WSAL-2 (assisted autonomy), with the three-layer architecture providing a natural decomposition for the WSAL-2→3 transition (Layer 1 autonomous, Layer 2 supervised, Layer 3 human-approved).

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]). The authors thank the Shandong Jiaodong Water Transfer Bureau for providing operational data and supporting the SiL verification.

__Data Availability__

SiL simulation data and HDMPC controller configurations are archived on Zenodo (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance). Source code for the three-layer HDMPC is available at https://github.com/IWHR-CHS/Jiaodong-HDMPC under MIT license.

__References__

Bai, Y., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). HydroComponents: An open-source Modelica library for multi-fidelity water system modeling. Environmental Modelling & Software (submitted).

Castelletti, A., Galelli, S., Restelli, M., & Soncini-Sessa, R. (2012). Tree-based reinforcement learning for optimal water reservoir operation. Water Resources Research, 48(9), W09507.

Camacho, E. F., & Bordons, C. (2007). Model Predictive Control (2nd ed.). Springer.

Clemmens, A. J., Kacerek, T. F., Grawitz, B., & Schuurmans, W. (2005). Test cases for canal control algorithms. Journal of Irrigation and Drainage Engineering, 131(6), 498–506.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Christofides, P. D., El-Farra, N. H., Li, M., & Mhaskar, P. (2002). Model-based control of two-time-scale processes. Computers & Chemical Engineering, 26(2), 287–299.

Davies, P. (2013). Evaluating the environmental sustainability of inter-basin water transfers. Water Resources Management, 27(13), 4709–4720.

Fooladivanda, D., & Taylor, J. A. (2018). Energy-optimal pump scheduling and water flow. IEEE Transactions on Control of Network Systems, 5(3), 1016–1026.

Ghimire, S. R., & Johnston, J. M. (2017). Sustainability assessment of inter-basin water transfer projects in the context of climate change. Water Resources Management, 31(5), 1667–1678.

Gohari, A., Eslamian, S., Mirchi, A., et al. (2013). Water transfer as a solution to water shortage: A fix that can backfire. Journal of Hydrology, 491, 23–39.

Grosso, J. M., Ocampo-Martinez, C., Puig, V., & Joseph, B. (2017). Chance-constrained model predictive control for drinking water networks. Journal of Process Control, 34, 108–120.

Guo, X., Hu, T., Zhang, T., & Lv, Y. (2020). Bilevel model for multi-reservoir operating policy in inter-basin water transfer-supply project. Journal of Hydrology, 581, 124347.

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Parallel quadratic programming for distributed model predictive control of water conveyance networks. Journal of Water Resources Planning and Management (submitted).

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Litrico, X., & Fromion, V. (2009). Modeling and Control of Hydrosystems. Springer.

Mala-Jetmarova, H., Sultanova, N., & Savic, D. (2017). Lost in optimisation of water distribution systems? A literature review of system operation. Environmental Modelling & Software, 93, 209–254.

Malaterre, P. O., Rogers, D. C., & Schuurmans, J. (1998). Classification of canal control algorithms. Journal of Irrigation and Drainage Engineering, 124(1), 3–10.

Maciejowski, J. M. (2002). Predictive Control with Constraints. Prentice Hall.

Menke, R., Abraham, E., Parpas, P., & Stoianov, I. (2016). Demonstrating demand response from water distribution system through pump scheduling. Applied Energy, 170, 377–387.

Ocampo-Martinez, C., Puig, V., Cembrano, G., & Quevedo, J. (2013). Application of predictive control strategies to the management of complex networks in the urban water cycle. IEEE Control Systems Magazine, 33(1), 15–41.

Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017). Model Predictive Control: Theory, Computation, and Design (2nd ed.). Nob Hill Publishing.

Shumilova, O., Tockner, K., Thieme, M., Koska, A., & Zarfl, C. (2018). Global water transfer megaprojects: A potential solution for the water-food-energy nexus? Frontiers in Environmental Science, 6, 150.

Su, C., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). Experimental verification of the CHS unified transfer function family and distributed MPC on a multi-pool laboratory flume. Journal of Irrigation and Drainage Engineering (submitted).

Wang, C., Li, X., Zhang, C., & Zhou, J. (2022). Optimal operation of multi-reservoir systems using deep reinforcement learning. Journal of Hydrology, 610, 127894.

Ye, S., Lei, X., Ji, C., Wang, C., & Wang, H. (2026). Software-in-the-Loop verification and operational design domain definition for adaptive multi-agent control of a cascade hydropower system. Journal of Hydrology (submitted).

Yin, B., Lei, X., Bai, Y., Ji, C., & Wang, H. (2026). HydroRTP: Simulink rapid prototyping toolbox for automatic code generation of water network controllers. SoftwareX (submitted).


van Overloop, P. J., Miltenburg, I. J., Bombois, X., Clemmens, A. J., Strand, R. J., & van de Giesen, N. C. (2010). Identification of resonance waves in open water channels. Control Engineering Practice, 18(8), 863–872.

Wahlin, B. T., & Clemmens, A. J. (2006). Automatic downstream water-level feedback control of branching canal networks: Theory. Journal of Irrigation and Drainage Engineering, 132(1), 3–14.

Zhuang, W. (2016). Eco-environmental impact of inter-basin water transfer projects: A review. Environmental Science and Pollution Research, 23(13), 12867–12879.

__Figure Captions__

__Figure 1.__ Jiaodong inter-basin water transfer system: 8 pump stations (S1 Dayuzhang to S8 Menlou) spanning 302 km with Yellow River intake, 6 en-route offtakes, and terminal deliveries to Qingdao, Yantai, Weihai, and Weifang. CHS six-element architecture overlay showing Station Agents, Segment Agents, and System Agent.

__Figure 2.__ Three-layer HDMPC architecture: Layer 1 Station Agents (2 s, pump regulation), Layer 2 Segment Agents (60 s, flow coordination), Layer 3 System Agent (3600 s, energy optimization). Cascaded setpoint flow (downward) and state/status feedback (upward).

__Figure 3.__ Family α transfer function validation for segment S1→S2: (a) measured vs. modeled downstream water level response to upstream flow step change; (b) Bode magnitude plot showing integrating dynamics with transport delay; (c) residual histogram (mean 0, std 0.04 m).

__Figure 4.__ SiL verification results for S2 (morning demand ramp): (a) water levels at all 16 monitoring points; (b) pump station flows; (c) ODD distance $\rho(\mathbf{x})$ over time; (d) pump speed ratios at S3 and S4.

__Figure 5.__ Energy optimization performance for S4 (weekly pattern): (a) pumping power vs. electricity tariff over 168 hours; (b) cumulative energy cost for HDMPC vs. rule-based dispatch; (c) pipeline water volume (buffer) showing pre-filling during valley hours.

__Figure 6.__ Structural isomorphism comparison: radar chart of normalized performance metrics for Jiaodong pipeline (Family α, green) vs. Shaoping hydropower (Family β, blue). Six axes: tracking accuracy, settling time, ODD coverage, robustness, energy efficiency, architecture reuse.
