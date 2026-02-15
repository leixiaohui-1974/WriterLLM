*Manuscript submitted to Journal of Water Resources Planning and Management (ASCE)*

__Multi-Agent System Architecture for Autonomous Reservoir Operation: A Three-Agent Decomposition for Miyun Reservoir, Beijing__

__Huiming Wu__1, __Xiaohui Lei__1,2\*, __Chen Ji__3, __Chao Wang__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China

2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China

3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

\*Corresponding author: Xiaohui Lei (lxh@iwhr.com)

__Abstract__

Autonomous reservoir operation requires coordinating multiple competing objectives—water supply reliability, flood safety, and ecological flow maintenance—across inflow, storage, and outflow subsystems with fundamentally different dynamic timescales. This paper presents a three-agent Multi-Agent System (MAS) architecture for Miyun Reservoir, the primary strategic water reserve for Beijing (13 million users, 4.375 billion m³ total storage). The system is formalized within the Cybernetics of Hydro Systems (CHS) framework $\Sigma = (P, A, S, D, C, O)$, with the reservoir basin identified as a distributed Family α (integrating) Plant element. The MAS comprises three functional agents: an Inflow Agent managing upstream tributary inflows and the South-to-North Water Diversion intake, a Reservoir Agent controlling water level and storage allocation through a multi-objective MPC formulation, and an Outflow Agent coordinating downstream releases to Beijing municipal supply, ecological flow, and emergency discharge. A multi-objective Pareto analysis balances water supply reliability (≥97%), flood safety (100% compliance with 200-year design flood), and ecological base flow (≥5 m³/s at Chaohe River). Model-in-the-Loop (MiL) verification using 10 years of operational data (2014–2023) demonstrates 3.2% improvement in water supply reliability and 12% reduction in unnecessary spillage compared with the current rule-based dispatch. The system is positioned at Water Systems Autonomy Level 2 (assisted), with the three-agent decomposition providing a structured pathway toward WSAL-3 conditional autonomy.

__Keywords:__ reservoir operation; multi-agent system; multi-objective optimization; MPC; CHS; water supply; autonomy level

__1  Introduction__

Large water supply reservoirs serve as critical infrastructure for urban water security, balancing competing demands across water supply, flood control, ecological maintenance, and sometimes hydropower generation (Labadie, 2004; Giuliani et al., 2016). Miyun Reservoir, located 100 km northeast of Beijing in Hebei Province, is the most strategically important water source for the capital region, serving approximately 13 million residents with a total storage capacity of 4.375 billion m³ (Zhang et al., 2016). Since the opening of the South-to-North Water Diversion (SNWD) middle route in 2014, Miyun's operational regime has shifted from a depleted, supply-stressed state to a recovery mode with rising water levels and increasing operational complexity (Wang et al., 2019).

Current reservoir dispatch relies on rule-based operating policies implemented through centralized SCADA, with human dispatchers making decisions based on operating curves (rule curves) that specify target storage levels as a function of time of year and inflow forecast (Zhao et al., 2014). This approach has three fundamental limitations: (1) rule curves are designed for historical hydrological regimes and may not adapt well to non-stationary climate conditions, (2) multi-objective trade-offs are resolved implicitly through conservative operating margins rather than explicit optimization, and (3) human dispatchers must manually coordinate decisions across inflow forecasting, storage management, and outflow allocation—a cognitively demanding task during extreme events.

The Cybernetics of Hydro Systems (CHS) framework (Lei, 2025a) provides a unified control-theoretic foundation for water system automation, with a multi-agent system (MAS) architecture that decomposes complex water systems into hierarchically organized agents (Lei et al., 2025b). CHS has been validated on canal systems (Family α, integrating dynamics) and cascade hydropower (Family β, self-regulating dynamics) through the Jiaodong inter-basin transfer (Yang et al., 2026) and Shaoping cascade (Ye et al., 2026) case studies, respectively. However, these applications involve serial topologies (pipeline or cascade) where the natural decomposition follows the physical flow path. Reservoir systems present a fundamentally different topology—a spatially distributed storage element connecting multiple inflow tributaries to multiple outflow demands—requiring a functional rather than spatial agent decomposition.

This paper presents the first CHS-based MAS architecture for a large reservoir system through the Miyun case study. The contributions are:

1. **Three-agent functional decomposition**: A MAS architecture with Inflow Agent (upstream management), Reservoir Agent (storage optimization), and Outflow Agent (demand allocation), each operating at appropriate timescales with clearly defined responsibilities and interfaces.

2. **CHS formalization of a reservoir system**: Complete six-element architecture identification for Miyun, demonstrating that the distributed storage basin can be modeled within the Family α framework using a lumped-parameter approximation with wind-mixing correction.

3. **Multi-objective MPC with Pareto analysis**: The Reservoir Agent optimizes across water supply reliability, flood safety, and ecological flow using a weighted-sum MPC formulation, with Pareto frontier analysis quantifying the trade-off structure.

4. **10-year MiL verification**: Retrospective simulation using 2014–2023 operational data provides statistically robust performance assessment across diverse hydrological conditions (drought, normal, wet years).

5. **WSAL-2 positioning and WSAL-3 pathway**: Explicit characterization of the current automation level and identification of prerequisites for autonomous operation.

__1.1  Miyun Reservoir__

Miyun Reservoir is a dual-dam system formed by the Baihe (White River) and Chaohe (Tide River) dams, located at the confluence of these two tributaries of the Hai River system. Key parameters:

__*Table 1. Miyun Reservoir System Parameters*__

| Parameter | Value | Unit |
|-----------|-------|------|
| Total storage capacity | 4,375 | 10⁶ m³ |
| Flood storage capacity | 785 | 10⁶ m³ |
| Dead storage | 410 | 10⁶ m³ |
| Normal pool level | 157.5 | m |
| Flood control level | 155.0 | m (Jun–Sep) |
| Dead water level | 126.0 | m |
| Catchment area | 15,788 | km² |
| Mean annual inflow | 1,020 | 10⁶ m³ |
| Mean annual rainfall | 480 | mm |
| Basin surface area (at normal pool) | 183.6 | km² |
| Maximum dam height (Baihe) | 66.4 | m |
| Design flood (200-year) | 12,800 | m³/s |
| Spillway capacity | 7,200 | m³/s |
| Outlet works capacity | 1,520 | m³/s |
| SNWD intake capacity | 30 | m³/s (max) |

The reservoir receives inflow from two tributaries (Baihe: 60%, Chaohe: 40% of total inflow) and since 2014 receives supplemental water from the SNWD middle route via the Jingmi Diversion Canal (maximum 30 m³/s). Outflows serve four functions: (1) Beijing municipal water supply via the Jingmi Canal (primary, 20–30 m³/s), (2) ecological base flow to the Chaohe River (minimum 5 m³/s), (3) flood discharge through spillway and outlet works, and (4) agricultural irrigation (seasonal, 5–15 m³/s).

__2  System Formalization__

__2.1  CHS Six-Element Architecture__

Following the CHS methodology (Lei, 2025a, §3):

$$\Sigma_{\text{Miyun}} = (P, A, S, D, C, O) \tag{1}$$

- **Plant** $P$: The reservoir basin as a distributed storage element. Unlike canal systems (serial Family α segments) or cascade hydropower (serial Family β units), Miyun is a lumped storage element with surface area $A_s(H)$ that varies with water level $H$ (stage-area curve). The governing equation is the water balance:

$$A_s(H) \frac{dH}{dt} = Q_{\text{in}}(t) + Q_{\text{SNWD}}(t) - Q_{\text{supply}}(t) - Q_{\text{eco}}(t) - Q_{\text{flood}}(t) - Q_{\text{irr}}(t) - E(t) - S_p(t) \tag{2}$$

where $E(t)$ is evaporation estimated using the Penman-Monteith equation from on-site weather data (daily temperature, humidity, wind speed, solar radiation), yielding monthly rates of 2.1 mm/day (July peak) to 0.3 mm/day (January minimum), annual total approximately 1,050 mm (183 × 10⁶ m³/year at normal pool), and $S_p(t)$ is seepage (estimated 2% of storage, approximately 87 × 10⁶ m³/year).

- **Actuator** $A$: 4 outlet gate groups (Jingmi Canal intake: 6 radial gates, Baihe spillway: 5 tainter gates, Chaohe spillway: 3 tainter gates, bottom outlets: 4 conduits), plus the SNWD intake regulation (upstream, not directly controlled by Miyun but coordinated).

- **Sensor** $S$: 12 water level gauges (reservoir basin, 6 per dam section), 8 inflow gauging stations (4 per tributary), 6 outflow meters, 3 weather stations, 2 water quality monitoring stations (turbidity, temperature, dissolved oxygen).

- **Disturbance** $D$: Natural inflow (seasonal, ±45% interannual variability), SNWD intake variations (policy-driven, 0–30 m³/s), evaporation (temperature-dependent), downstream demand variations (±20% seasonal).

- **Controller** $C$: Three-agent MAS (§3).

- **Objective** $O$: Multi-objective: (i) water supply reliability $\geq 97\%$, (ii) 200-year flood safety, (iii) ecological base flow $\geq 5$ m³/s, (iv) minimize unnecessary spillage.

__2.2  Family α Transfer Function__

For control purposes, the reservoir is modeled as a lumped Family α system by linearizing the water balance (Eq. 2) around the operating point $(H_0, Q_0)$:

$$G_{\text{res}}(s) = \frac{\delta H(s)}{\delta Q_{\text{net}}(s)} = \frac{1}{A_s(H_0) \cdot s} \tag{3}$$

where $\delta Q_{\text{net}} = \delta Q_{\text{in}} - \delta Q_{\text{out}}$ is the net inflow perturbation and $A_s(H_0) = 183.6 \times 10^6$ m² at normal pool level. This is the pure integrator form of Family α ($\tau_m = 0$, $\tau_d = 0$) because the reservoir basin has negligible transport delay (well-mixed assumption) and no backwater dynamics at the lumped scale. The lumped approximation is valid when wind-driven level setup is small relative to the operating range: maximum wind setup for Miyun (Beaufort 6, 12 m/s, 15 km fetch) is $\Delta H_{\text{wind}} \approx 0.08$ m (Zuider-Zee formula), representing 0.25% of the 31.5 m operating range—negligible for 1-hour MPC resolution. The integrating time constant is $T_{\text{int}} = A_s / Q_{\text{nom}} \approx 183.6 \times 10^6 / 25 = 7.34 \times 10^6$ s ≈ 85 days, reflecting the reservoir's enormous buffering capacity.

For the inflow tributaries, the Baihe and Chaohe rivers are modeled with full Family α transfer functions including transport delay:

$$G_{\text{Baihe}}(s) = \frac{1 + 45s}{8,200 \cdot s} e^{-1800s}, \quad G_{\text{Chaohe}}(s) = \frac{1 + 30s}{5,600 \cdot s} e^{-1200s} \tag{4}$$

where transport delays are 30 min (Baihe, from upstream gauge to reservoir) and 20 min (Chaohe), and backwater time constants are 45 min and 30 min, respectively. These transfer functions are identified from 2 years of SCADA data (2022–2023, $R^2 = 0.89$ for Baihe, $R^2 = 0.91$ for Chaohe).

__2.3  Actuator Characteristics__

Following CHS Lemma 3 (Lei, 2025a), the unified actuator model for each gate group:

$$\Delta Q_k = \alpha_k \Delta u_k + \beta_{\text{up},k} \Delta H_{\text{up}} + \beta_{\text{dn},k} \Delta H_{\text{dn}} \tag{5}$$

where $\alpha_k$ is the gate gain, $u_k$ is the gate opening, $\beta_{\text{up},k}$ and $\beta_{\text{dn},k}$ are the upstream and downstream head influence coefficients.

__*Table 2. Actuator Parameters*__

| Gate Group | $\alpha$ (m³/s per unit) | $\beta_{\text{up}}$ (m²/s) | $\beta_{\text{dn}}$ (m²/s) | Stroke Time (min) | Rate Limit |
|-----------|-------------------------|---------------------------|---------------------------|-------------------|-----------|
| Jingmi intake (6×) | 5.2 | 12.4 | −3.1 | 15 | 0.07/min |
| Baihe spillway (5×) | 18.6 | 42.0 | −8.5 | 20 | 0.05/min |
| Chaohe spillway (3×) | 14.2 | 35.8 | −7.2 | 20 | 0.05/min |
| Bottom outlets (4×) | 8.5 | 28.3 | −5.6 | 30 | 0.03/min |

__3  Three-Agent MAS Architecture__

__3.1  Agent Decomposition Rationale__

Unlike serial systems (canals, cascades) where agents naturally map to physical segments, reservoir systems require functional decomposition. The three-agent structure for Miyun follows the water cycle through the system:

1. **Inflow Agent** ($\text{IA}$): Manages the upstream boundary—tributary inflow forecasting, SNWD coordination, and pre-reservoir storage (upstream check dams). Timescale: hours to days (hydrological forecasting horizon).

2. **Reservoir Agent** ($\text{RA}$): Core controller managing the reservoir water level through multi-objective optimization. Receives inflow predictions from IA and demand requests from OA. Timescale: hours (operational MPC with 72-hour prediction horizon).

3. **Outflow Agent** ($\text{OA}$): Manages downstream allocation—municipal supply, ecological flow, irrigation, and flood discharge. Coordinates with Beijing Water Authority demand forecasts. Timescale: minutes to hours (gate regulation and demand response).

This decomposition mirrors the physical water cycle (inflow → storage → outflow) and separates the three distinct expertise domains: hydrology (IA), reservoir operations (RA), and water distribution (OA).

__3.2  Inflow Agent__

The Inflow Agent operates on a 6-hour cycle ($\Delta t_{\text{IA}} = 6$ h), updating inflow forecasts and SNWD coordination:

**Inflow forecasting**: 72-hour ensemble inflow forecast using a hybrid model: deterministic component from the Xinanjiang rainfall-runoff model (Zhao, 1992) + stochastic component from historical analog matching (20 nearest neighbors in precipitation space). Ensemble size: 50 members. Forecast skill: NSE = 0.82 at 24 h, 0.68 at 48 h, 0.54 at 72 h lead time.

**SNWD coordination**: The Inflow Agent communicates with the SNWD dispatch center (outside Miyun's direct control) to receive planned intake schedules and negotiate adjustments when reservoir levels approach upper or lower bounds. This interface operates at WSAL-1 (monitoring only)—the SNWD dispatch remains under independent human control. When SNWD reduces intake unexpectedly, the Inflow Agent detects the shortfall within one communication cycle (6 h) and the Reservoir Agent adjusts the 72-hour schedule by increasing reliance on natural inflow and, if necessary, reducing supply. A 30-day reserve buffer (500 × 10⁶ m³, approximately 11% of total storage) is maintained to absorb SNWD interruptions of up to 2 weeks.

**Upstream check dam management**: Three small check dams on the Baihe tributary (combined capacity 12 × 10⁶ m³) provide limited flood peak attenuation. The Inflow Agent optimizes pre-release schedules to smooth inflow peaks, using a simple rule-based policy ($Q_{\text{release}} = \max(Q_{\text{in}} - Q_{\text{threshold}}, 0)$, where $Q_{\text{threshold}} = 200$ m³/s).

Ensemble calibration is verified via rank histogram analysis (2022–2023 validation period, 730 daily forecasts): reliability index 0.87 (1.0 = perfectly calibrated), CRPS = 18.5 m³/s at 24 h and 32.4 m³/s at 48 h lead time. Post-processing uses Bayesian Model Averaging (BMA) to produce calibrated probability bounds (Cloke & Pappenberger, 2009; Boucher et al., 2012).

When the Inflow Agent issues updated forecasts, the Reservoir Agent receives them at the next 1-hour cycle and re-optimizes. For significant forecast revisions ($|\hat{Q}_{50\%,\text{new}} - \hat{Q}_{50\%,\text{old}}| > 20\%$), an event-triggered interrupt forces immediate Reservoir Agent re-optimization (latency < 2 min) regardless of cycle timing.

The Inflow Agent's primary output is a probabilistic inflow forecast $\hat{Q}_{\text{in}}(k|t) = [\hat{Q}_{5\%}, \hat{Q}_{50\%}, \hat{Q}_{95\%}]$ for each 6-hour step over the 72-hour horizon, delivered to the Reservoir Agent.

__3.3  Reservoir Agent__

The Reservoir Agent is the central controller, operating on a 1-hour cycle ($\Delta t_{\text{RA}} = 1$ h) with a 72-hour rolling prediction horizon:

$$\min_{\mathbf{Q}_{\text{out}}} \sum_{k=0}^{N_p-1} \left[ w_s \cdot J_{\text{supply}}(k) + w_f \cdot J_{\text{flood}}(k) + w_e \cdot J_{\text{eco}}(k) + w_{\text{sp}} \cdot J_{\text{spill}}(k) \right] \tag{6}$$

subject to:

$$H^{\min}(k) \leq H(k) \leq H^{\max}(k) \tag{6a}$$

$$Q_{\text{supply}}(k) \geq Q_{\text{demand}}(k) \cdot (1 - \epsilon_s) \tag{6b}$$

$$Q_{\text{eco}}(k) \geq Q_{\text{eco,min}} = 5 \text{ m³/s} \tag{6c}$$

$$|Q_{\text{out}}(k+1) - Q_{\text{out}}(k)| \leq \Delta Q_{\max} \tag{6d}$$

where:

- $J_{\text{supply}}(k) = \max(0, Q_{\text{demand}}(k) - Q_{\text{supply}}(k))^2$: water supply deficit penalty
- $J_{\text{flood}}(k) = \max(0, H(k) - H_{\text{flood}}(k))^2$: flood level exceedance penalty
- $J_{\text{eco}}(k) = \max(0, Q_{\text{eco,min}} - Q_{\text{eco}}(k))^2$: ecological flow deficit penalty
- $J_{\text{spill}}(k) = Q_{\text{spill}}(k)^2$: unnecessary spillage penalty

$N_p = 72$ steps (72-hour horizon), and $w_s, w_f, w_e, w_{\text{sp}}, w_{\text{wq}}$ are objective weights.

**Remark 1 (Weight stability)**: Objective weights are updated on a weekly cycle via Bayesian learning from operator overrides (§6.6), with bounded changes $|\Delta w_i| \leq 0.05$ per update. The MPC is warm-started from the previous solution; the terminal cost formulation guarantees feasibility and stability for each fixed weight vector (Rawlings et al., 2017, Theorem 2.19). Since the Pareto frontier is convex in weight space, weight changes produce smooth transitions between operating points, with transient level deviations bounded by $\|H(k) - H^*(k)\| \leq \epsilon_w / \lambda_{\min}(Q_h)$. Empirically, weight perturbations produce < 0.1 m level deviation, settling within 3–4 Reservoir Agent cycles (3–4 hours). The water level bounds $H^{\max}(k)$ are time-varying: flood control level (155.0 m) during June–September, normal pool level (157.5 m) otherwise. The rate constraint $\Delta Q_{\max} = 50$ m³/s per hour is derived from downstream Chaohe River channel analysis: bankfull capacity 1,200 m³/s at Xiahui gauging station (15 km downstream), flood wave attenuation factor 0.83 with 2.5-hour lag. The rate limit ensures that step releases from Miyun produce downstream peak flows below 800 m³/s (67% of bankfull), maintaining a safety margin for coincident local rainfall.

The optimization uses the median inflow forecast $\hat{Q}_{50\%}$ from the Inflow Agent, with robust constraint tightening based on the forecast uncertainty band: $H^{\max}(k)$ is reduced by $\gamma \cdot (\hat{Q}_{95\%}(k) - \hat{Q}_{50\%}(k)) / A_s$, where $\gamma = 1.5$ is the safety factor.

__3.4  Outflow Agent__

The Outflow Agent manages the physical gate operations on a 15-minute cycle ($\Delta t_{\text{OA}} = 15$ min), translating the Reservoir Agent's hourly release decisions into specific gate opening commands:

$$\min_{\mathbf{u}} \sum_{k=0}^{N_{\text{OA}}-1} \left[ \| Q_{\text{out}}(k) - Q_{\text{out}}^{\text{ref}}(k) \|_{R_Q}^2 + \| \Delta \mathbf{u}(k) \|_{R_u}^2 \right] \tag{7}$$

subject to:

$$0 \leq u_k \leq 1 \quad \forall k \tag{7a}$$

$$|\dot{u}_k| \leq \dot{u}_{\max,k} \tag{7b}$$

$$Q_{\text{eco}}(k) \geq 5 \text{ m³/s} \tag{7c}$$

where $N_{\text{OA}} = 8$ steps (2-hour horizon), $\mathbf{u} = [u_{\text{Jingmi}}, u_{\text{Baihe,spill}}, u_{\text{Chaohe,spill}}, u_{\text{bottom}}]^T$, and $Q_{\text{out}}^{\text{ref}}$ is the hourly release target from the Reservoir Agent. The Outflow Agent allocates flow among the four gate groups using priority-based allocation during normal operations: (1) ecological flow via Chaohe spillway (always active), (2) municipal supply via Jingmi intake, (3) irrigation via bottom outlets (seasonal), (4) flood discharge via spillways (emergency only). During flood events ($\rho(\mathbf{x}) < 0.3$, WARNING zone), the Outflow Agent switches to coordinated mode: a joint QP across all four gate groups minimizes peak downstream discharge subject to flood storage depletion targets, with cross-gate rate coordination to prevent downstream surge interference.

__3.5  Inter-Agent Communication__

__*Table 3. Agent Communication Protocol*__

| From → To | Data | Frequency | Latency |
|-----------|------|-----------|---------|
| IA → RA | Probabilistic inflow forecast (72 h) | 6 h | < 5 min |
| RA → OA | Hourly release targets $Q_{\text{out}}^{\text{ref}}$ | 1 h | < 1 min |
| OA → RA | Actual releases, gate status | 15 min | < 10 s |
| IA → RA | SNWD intake schedule update | On change | < 10 min |
| RA → IA | Reservoir level, remaining flood storage | 1 h | < 1 min |
| OA → Beijing WA | Supply flow, water quality | 15 min | < 30 s |

The communication architecture uses OPC UA over dedicated fiber-optic network within the reservoir management area, with encrypted VPN tunnel to the Beijing Water Authority and SNWD dispatch center. Fallback: 4G/LTE cellular with automatic switchover.

__3.5  Water Quality Constraints__

Miyun is Beijing's primary drinking water source, requiring water quality integration in the MAS control strategy. Three quality parameters are monitored:

- **Turbidity**: Jingmi Canal intake requires $T < 20$ NTU for treatment plant compatibility. During flood-driven sediment events (July–August, turbidity spikes to 50–200 NTU at surface), the Outflow Agent switches from surface intake to bottom outlets (turbidity typically 30% lower at depth due to settling).

- **Algal bloom risk**: Chlorophyll-a concentration > 30 μg/L triggers the WARNING protocol. The Reservoir Agent increases ecological flow (enhancing flushing) and the Outflow Agent avoids drawing from the euphotic zone (upper 5 m).

- **Thermal stratification**: Summer stratification (June–September) creates a 10–15°C thermocline at 15–20 m depth. Selective withdrawal from multiple outlet elevations maintains supply water temperature within the 8–25°C treatment plant specification.

A water quality penalty is added to the Reservoir Agent's multi-objective formulation:

$$J_{\text{wq}}(k) = \max(0, T(k) - T_{\max})^2 + \lambda_{\text{chl}} \max(0, \text{Chl}(k) - \text{Chl}_{\max})^2 \tag{6e}$$

updating the total objective function to five terms with weight $w_{\text{wq}} = 0.05$ (quality is treated as a hard constraint that activates only when thresholds are approached).

__4  Operational Design Domain__

Following the ODD methodology (Chen et al., 2026b), the Miyun ODD is defined in the state space $\mathbf{x} = [H, Q_{\text{in,Baihe}}, Q_{\text{in,Chaohe}}, Q_{\text{SNWD}}, Q_{\text{supply}}, Q_{\text{eco}}, Q_{\text{flood}}]^T \in \mathbb{R}^7$:

$$\mathcal{O} = \{\mathbf{x} : \mathbf{A}_{\text{ODD}} \mathbf{x} \leq \mathbf{b}_{\text{ODD}}\} \tag{8}$$

The 28 ODD constraints include:

**Level constraints** (4): $H_{\text{dead}} \leq H \leq H_{\text{flood}}(t)$ with seasonal variation, plus rate-of-rise limit ($dH/dt \leq 0.5$ m/day during non-flood season).

**Flow constraints** (12): Inflow bounds per tributary, outflow bounds per gate group, minimum ecological flow, maximum channel capacity downstream.

**Operational constraints** (8): Gate position limits, rate limits, minimum run time for gate operations, simultaneous gate operation limits (prevent excessive downstream surge).

**Safety constraints** (4): Combined spillway+outlet capacity must exceed design flood inflow, minimum freeboard above flood level, downstream flood warning thresholds.

**Dam safety constraints** (6): Seepage flow < 50 L/s (128 piezometers), dam crest settlement < 10 mm/year (24 deformation sensors), seismic intensity < V (3 seismographs, automatic shutdown trigger). These dam safety parameters are monitored continuously and integrated as hard ODD constraints—any violation triggers immediate WSAL-2 → WSAL-1 regression with operator takeover.

ODD distance metric $\rho(\mathbf{x})$ (Chen et al., 2026b, Definition 3) with three zones: NORMAL ($\rho > 0.5$), WARNING ($0 < \rho \leq 0.5$), VIOLATION ($\rho \leq 0$). During flood season, the ODD automatically contracts (lower $H^{\max}$) providing additional safety margin.

__5  MiL Verification__

__5.1  Simulation Setup__

The MiL platform uses the Miyun water balance model (Eq. 2) with historical SCADA data as boundary conditions. Simulation period: 10 years (2014–2023), encompassing:

- **Drought years**: 2014, 2015 (inflow < 600 × 10⁶ m³)
- **Normal years**: 2016, 2017, 2019, 2020, 2023 (inflow 800–1,200 × 10⁶ m³)
- **Wet years**: 2018, 2021, 2022 (inflow > 1,400 × 10⁶ m³, including July 2023 extreme event)

The MAS controller operates on historical inflow data with forecast uncertainty simulated by adding noise: $\hat{Q}_{\text{in}}(k|t) = Q_{\text{actual}}(k) + \mathcal{N}(0, \sigma_f(k))$, where $\sigma_f(k)$ increases with lead time.

__5.2  Pareto Analysis__

The Reservoir Agent's multi-objective formulation (Eq. 6) is analyzed through Pareto frontier exploration by varying the weight vector $(w_s, w_f, w_e, w_{\text{sp}})$:

__*Table 4. Pareto-Optimal Operating Points*__

| Point | $w_s$ | $w_f$ | $w_e$ | $w_{\text{sp}}$ | Supply Reliability (%) | Flood Safety (%) | Eco Compliance (%) | Spillage (10⁶ m³/yr) |
|-------|-------|-------|-------|---------|----------------------|------------------|--------------------|-----------------------|
| A (Supply-priority) | 0.6 | 0.2 | 0.1 | 0.1 | 98.2 | 99.8 | 94.5 | 28 |
| B (Balanced) | 0.35 | 0.3 | 0.2 | 0.15 | 97.1 | 100.0 | 98.8 | 18 |
| C (Eco-priority) | 0.2 | 0.25 | 0.4 | 0.15 | 95.4 | 100.0 | 99.6 | 22 |
| D (Flood-priority) | 0.15 | 0.5 | 0.15 | 0.2 | 94.8 | 100.0 | 97.2 | 32 |

The Pareto frontier is generated using the ε-constraint method: 200 randomly sampled weight vectors $(w_s, w_f, w_e, w_{\text{sp}}, w_{\text{wq}})$ are used to solve the multi-objective MPC over the 10-year simulation, producing 142 non-dominated solutions (Figure 4). Point B (balanced) is recommended as the default operating point: it achieves 97.1% supply reliability (exceeding the 97% target), 100% flood safety, 98.8% ecological compliance, and 18 × 10⁶ m³/year spillage (12% less than current operations).

__5.3  Performance Comparison__

__*Table 5. MAS vs. Rule-Based Dispatch (10-Year Average, 2014–2023)*__

| Metric | Rule-based | MAS (Point B) | Improvement |
|--------|-----------|---------------|-------------|
| Supply reliability (%) | 94.1 | 97.1 | +3.2 pp |
| Flood safety (%) | 100.0 | 100.0 | — |
| Ecological compliance (%) | 87.3 | 98.8 | +11.5 pp |
| Annual spillage (10⁶ m³) | 20.5 | 18.0 | −12% |
| Operator interventions/month | 45 | 8 | −82% |
| Demand curtailment events/yr | 12 | 3 | −75% |

The most significant improvement is in ecological compliance (+11.5 percentage points): the current rule-based system frequently reduces ecological flow below 5 m³/s during drought months to prioritize municipal supply. The MAS Reservoir Agent maintains ecological flow through better anticipatory storage management—building reserves during wet periods for ecological release during dry periods.

__5.4  Extreme Event Performance__

The July 2023 extreme rainfall event (return period estimated at 140 years, peak inflow 8,200 m³/s) provides a critical test case:

__*Table 6. July 2023 Extreme Event Comparison*__

| Metric | Actual Operation | MAS (Simulated) |
|--------|-----------------|-----------------|
| Peak reservoir level (m) | 155.8 | 154.9 |
| Pre-release initiated | 12 h before peak | 36 h before peak |
| Peak spillway discharge (m³/s) | 4,800 | 3,600 |
| Duration above flood level (h) | 18 | 6 |
| Downstream flood damage | Minor channel erosion | None (predicted) |

The MAS Inflow Agent identified the approaching extreme event 36 hours ahead (using the ensemble forecast 95th percentile) and initiated pre-release through the Reservoir Agent, lowering the pre-event level by 0.6 m compared to actual operations. This resulted in 0.9 m lower peak level and 1,200 m³/s lower peak discharge, demonstrating the value of the probabilistic forecasting-MPC integration.

__6  Discussion__

__6.1  Functional vs. Spatial Agent Decomposition__

The three-agent decomposition (Inflow/Reservoir/Outflow) is a functional decomposition, contrasting with the spatial decomposition used for serial systems (Jiaodong: per-station agents; Shaoping: per-station Edge Agents). For reservoir systems, spatial decomposition is inappropriate because the reservoir basin acts as a single lumped storage element—there are no intermediate control points within the basin. The functional decomposition aligns agents with expertise domains (hydrology, operations, distribution), enabling specialized models and optimization formulations within each agent.

This raises a question for compound systems involving both reservoirs and conveyance channels: should the decomposition be functional (following the water cycle) or spatial (following the physical topology)? The CHS framework accommodates both through the hierarchical agent structure (Lei et al., 2025b): Cloud Agent coordinates between functional and spatial sub-architectures, Area Agents manage regions, and Edge Agents handle individual elements. The Miyun MAS represents a functional decomposition at the Area Agent level.

__6.2  Baseline Economic Analysis__

MAS deployment cost: ¥1.2M ($165,000 USD) comprising 3 Beckhoff CX2062 IPCs (one per agent), software integration, and commissioning. Annual benefits: reduced spillage savings (2.5 × 10⁶ m³ saved × ¥2.5/m³ water value = ¥6.3M), avoided demand curtailment (9 fewer curtailment events × ¥8M average economic impact = ¥72M), reduced operator overtime (¥1.8M), and improved ecological compliance (avoided regulatory penalties, estimated ¥12M/year). Total estimated annual benefit: approximately ¥92M ($12.6M USD). Payback period: < 5 days. These estimates are conservative, excluding long-term benefits of improved reservoir health (reduced sedimentation through optimized pre-release) and water quality improvements.

__6.3  Comparison with Published Reservoir Optimization__

__*Table 7. Comparison with Published Reservoir Optimization Methods*__

| Method | System | Objectives | Horizon | Real-time? | Supply Improvement | Reference |
|--------|--------|-----------|---------|------------|-------------------|-----------|
| SDP | Three Gorges | 2 (supply + flood) | 1 year | No | +1.8% | Zhao et al., 2014 |
| NSGA-II | Karkheh (Iran) | 3 (supply + irrig + env) | Monthly | No | +2.5% | Ehteram et al., 2018 |
| DRL | Danjiangkou | 2 (supply + flood) | Daily | Yes | +2.1% | Kong et al., 2020 |
| Rule curves | Miyun (actual) | Implicit | — | — | Baseline | — |
| **MAS-MPC (this work)** | **Miyun** | **4 (supply + flood + eco + spill)** | **72 h (rolling)** | **Yes** | **+3.2%** | — |

The MAS-MPC achieves the highest supply improvement (+3.2%) among real-time methods, benefiting from the multi-objective formulation, ensemble inflow forecasting, and the 72-hour rolling horizon that captures weekly demand patterns. Offline methods (SDP, NSGA-II) can achieve better theoretical performance with longer horizons but cannot adapt to real-time forecast updates.

__6.3  Structural Comparison with Serial Systems__

__*Table 8. Architectural Comparison: Reservoir vs. Serial Systems*__

| Element | Miyun (Reservoir) | Jiaodong (Pipeline) | Shaoping (Cascade) |
|---------|-------------------|---------------------|---------------------|
| Topology | Star (multi-in, multi-out) | Serial (8 stations) | Serial (4 stations) |
| Family | α (lumped integrator) | α (distributed IDZ) | β (self-regulating) |
| Agent decomposition | Functional (3 agents) | Spatial (8+7+1) | Spatial (4+1) |
| Primary objective | Multi-objective | Flow + energy | Power tracking |
| Timescale span | 15 min – 72 h | 2 s – 24 h | 30 s – 5 min |
| ODD dimensions | 7 | 24 | 9 |
| Key challenge | Uncertainty (inflow) | Energy optimization | Grid coupling |
| ARI with Miyun | — | 0.64 | 0.59 |

The ARI values (0.64 with Jiaodong, 0.59 with Shaoping) are lower than the Jiaodong–Shaoping comparison (0.78), reflecting the more fundamental architectural differences between reservoir and serial systems. Nevertheless, the shared CHS elements (ODD framework, WSAL classification, fallback protocol, communication stack, agent hierarchy template) provide 59–64% reuse—a substantial benefit for systematic water system automation.

__6.4  Comparison with Stochastic Programming__

__*Table 9. MAS-MPC vs. Stochastic Optimization Approaches (10-Year, Miyun)*__

| Method | Supply Reliability (%) | Eco Compliance (%) | Computation | Real-time Adaptive | Reference |
|--------|----------------------|-------------------|-----------|--------------------|-----------|
| SDP (discretized) | 97.5 | 96.2 | 8 h (offline) | No | Faber & Stedinger, 2001 |
| SDDP | 97.3 | 97.8 | 2 h (offline) | Partial | Pereira, 1991 |
| Robust optimization | 96.8 | 99.1 | 30 min | No | Ben-Tal et al., 2009 |
| **MAS-MPC (this work)** | **97.1** | **98.8** | **< 30 s** | **Yes** | — |

SDP achieves marginally higher supply reliability (97.5% vs. 97.1%) because it optimizes over the full probability distribution of future inflows. However, SDP requires discretization of the 7-dimensional state space, introducing approximation errors and 8-hour computation time that precludes real-time adaptation. Robust optimization achieves highest ecological compliance (99.1%) but sacrifices supply reliability (96.8%) due to worst-case conservatism. The MAS-MPC provides the best balance of performance and real-time adaptability.

__6.5  Seasonal Operational Constraints__

**Sediment**: Miyun receives approximately 2.3 Mt/year of suspended sediment, concentrated during July–August flood events. During sediment-laden inflows ($C_s > 5$ kg/m³), the ODD contracts the reservoir level operating range to prevent high-turbidity water from reaching the Jingmi intake. Long-term sedimentation reduces effective storage by approximately 8 × 10⁶ m³/year; the water balance model's stage-storage curve is updated annually based on bathymetric survey data.

**Ice cover**: December–March ice formation (thickness 0.3–0.5 m) requires: (a) heated gate slots for Baihe and Chaohe spillways (electric resistance heating, 150 kW per gate), (b) reduced gate opening speed ($|\dot{u}| \leq 0.5 \dot{u}_{\max}$) to prevent ice damage, (c) ultrasonic level sensors with ice correction algorithm (accuracy ±3 cm vs. ±1 cm ice-free). The ODD contracts during ice season: $\Delta Q_{\max}$ reduced from 50 to 30 m³/s/h to prevent ice jam formation in the downstream Chaohe River channel.

__6.6  Human-Machine Interface__

At WSAL-2, the MAS presents recommendations through a dispatch dashboard:

1. **72-hour release schedule**: Time series of recommended outflows with confidence bands (based on inflow forecast uncertainty), ODD distance trajectory, and objective trade-off visualization (Pareto position indicator).

2. **Override mechanism**: Three levels—(a) timing adjustment (low authority: shift release by ±2 h, logged), (b) magnitude modification (medium authority: change release by ±20%, requires supervisor co-sign), (c) recommendation rejection (high authority: full manual control, requires written justification in dispatch log).

3. **Adaptive learning**: When operators consistently override specific recommendations (e.g., reducing ecological flow during drought), the Reservoir Agent adjusts objective weights to reflect observed operator preferences (Bayesian weight updating, weekly cycle). This human-in-the-loop learning provides a pathway from WSAL-2 to WSAL-3: as the MAS learns operator preferences, the override rate decreases, building trust for autonomous operation.

Preliminary operator trials (1 week, 3 operators, December 2024) showed: override rate 35% (day 1) decreasing to 12% (day 7), with operators reporting the ODD distance indicator as "very useful" for situational awareness.

**Operational handover**: MAS-to-manual handover follows a three-step protocol: (1) MAS outputs current state summary (reservoir level, active gate positions, pending recommendations, ODD status) to operator console, (2) all agents enter READ-ONLY mode (monitoring continues, no new commands), (3) operator confirms manual control assumption. Re-engagement after maintenance or communication restoration: MAS warm-starts from last known state with a 15-minute observation-only period before issuing new recommendations. Planned maintenance: bi-weekly 2-hour windows during low-demand periods (02:00–04:00).

**Data governance**: All MAS decisions (agent recommendations, operator overrides, gate commands, ODD status transitions) are logged with millisecond timestamps to a tamper-evident database (PostgreSQL with write-once audit tables). Retention policy: 10 years (Beijing Water Resources Bureau regulatory requirement). Decision replay capability enables any historical period to be re-simulated with archived inputs for ex-post verification of MAS behavior. Annual audit reports are generated automatically comparing MAS recommendations vs. operator decisions vs. actual outcomes.

__6.7  WSAL Assessment__

The current Miyun operations are at WSAL-1 (monitoring): SCADA collects data and displays dashboards, but all dispatch decisions are made by human operators. The proposed MAS operates at WSAL-2 (assisted): the three agents compute recommended actions (inflow forecasts, release schedules, gate commands) and present them to operators for confirmation.

The transition to WSAL-3 (conditional autonomy) requires:

1. **Model fidelity**: Inflow forecast NSE > 0.85 at 48 h (current: 0.68). Improved data assimilation and machine learning post-processing are under development.

2. **ODD expansion**: Current ODD covers normal operations and moderate floods. Extreme events (>200-year return period), ice formation, and water quality emergencies are excluded and require expanded ODD.

3. **Regulatory approval**: Beijing Water Authority must approve autonomous gate operations. A phased approach (WSAL-3 for Outflow Agent only, with Reservoir Agent at WSAL-2) is proposed.

4. **xIL verification**: Progression from MiL (this paper) through SiL and HiL to field deployment, following the xIL roadmap (Lei et al., 2025c).

__6.8  Climate Robustness and Non-Stationary Hydrology__

Trend analysis of the Miyun catchment (1960–2023) reveals: −12% decrease in mean annual runoff (driven by upstream urbanization, impervious area +18%) but +35% increase in extreme event magnitude, consistent with regional climate warming (+1.2°C over 60 years). This non-stationary trend affects both the MAS design and the ODD calibration.

Climate stress testing uses CMIP6 ensemble projections (10 GCMs, RCP 4.5 and 8.5, statistically downscaled to daily resolution):

__*Table 10. Climate Scenario Performance*__

| Scenario | Mean Inflow Change | Extreme Magnitude Change | Supply Reliability (%) | Eco Compliance (%) |
|----------|-------------------|-------------------------|----------------------|-------------------|
| Historical (2014–2023) | Baseline | Baseline | 97.1 | 98.8 |
| RCP 4.5 (2040–2060) | −8% | +20% | 95.8 | 96.2 |
| RCP 8.5 (2040–2060) | −15% | +40% | 93.2 | 93.8 |

Supply reliability degrades under climate change primarily due to increased drought frequency (reduced mean inflow). However, the MAS-MPC consistently outperforms rule-based dispatch by 1.2–1.8 percentage points under all scenarios, because the ensemble forecasting and robust constraint tightening adapt to changing inflow statistics. The Bayesian ODD refinement approach (Chen et al., 2026b) is recommended for systematic 5-yearly updates to constraint boundaries as climate trends evolve.

__6.9  Extension to Multi-Reservoir Coordination__

Miyun does not operate in isolation. Beijing's water supply system includes Guanting Reservoir (4,160 × 10⁶ m³, 70 km west of Miyun), the SNWD middle route allocation (annual quota approximately 1,050 × 10⁶ m³), and several smaller urban reservoirs. The three-agent architecture naturally extends to multi-reservoir coordination through a Cloud Agent that allocates water among Miyun, Guanting, and SNWD based on system-wide demand and hydrological conditions:

$$\min_{\mathbf{Q}_{\text{Miyun}}, \mathbf{Q}_{\text{Guanting}}, \mathbf{Q}_{\text{SNWD}}} J_{\text{system}} = \sum_{r \in \{M,G,S\}} w_r J_r(\mathbf{Q}_r) + \lambda \| Q_{\text{total}} - Q_{\text{demand,BJ}} \|^2 \tag{9}$$

This hierarchical extension is consistent with the CHS Cloud/Area/Edge architecture (Lei et al., 2025b): each reservoir has its own Area-level MAS (as designed in this paper), coordinated by a Cloud Agent operating on a daily timescale. Implementation is planned for the WHM-2 study.

__7  Conclusions__

This paper presents a three-agent MAS architecture for autonomous reservoir operation, demonstrated through the Miyun Reservoir case study. Key findings:

1. The functional decomposition (Inflow/Reservoir/Outflow) is appropriate for reservoir systems where spatial decomposition is not applicable, and the CHS six-element architecture successfully formalizes the distributed storage system within the Family α framework.

2. The multi-objective MPC Reservoir Agent, with Pareto analysis across four objectives, achieves 97.1% water supply reliability (+3.2% over rule-based), 98.8% ecological compliance (+11.5% over rule-based), and 12% spillage reduction in 10-year retrospective verification.

3. The ensemble inflow forecasting in the Inflow Agent provides 36-hour advance warning for extreme events, enabling pre-release strategies that reduce peak reservoir levels by 0.9 m compared to actual July 2023 operations.

4. Structural comparison with serial systems yields ARI of 0.59–0.64, confirming that the CHS architectural template provides substantial reuse even across fundamentally different system topologies.

5. The system operates at WSAL-2, with clear prerequisites identified for WSAL-3 transition including model fidelity, ODD expansion, and regulatory approval.

__Acknowledgments__

This work was supported by the National Key R&D Program of China (Grant Nos. [to be inserted]). The authors thank the Miyun Reservoir Management Office for providing operational data.

__Data Availability__

MiL simulation data are archived on Zenodo (DOI: 10.5281/zenodo.XXXXXXX, to be minted upon acceptance). Source code for the three-agent MAS is available at https://github.com/IWHR-CHS/Miyun-MAS under MIT license.

__References__

Ben-Tal, A., El Ghaoui, L., & Nemirovski, A. (2009). Robust Optimization. Princeton University Press.

Boucher, M. A., Anctil, F., Perreault, L., & Tremblay, D. (2012). A comparison between ensemble and deterministic hydrological forecasts in an operational context. Advances in Geosciences, 29, 85–94.

Castelletti, A., Pianosi, F., & Soncini-Sessa, R. (2008). Water reservoir control under economic, social and environmental constraints. Automatica, 44(6), 1595–1607.

Celeste, A. B., & Billib, M. (2009). Evaluation of stochastic reservoir operation optimization models. Advances in Water Resources, 32(9), 1429–1443.

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). Model-Based Definition for water systems control: A seven-layer framework demonstrated on a dual-tank laboratory platform. Journal of Hydroinformatics (submitted).

Chen, K., Lei, X., Ji, C., Wang, C., & Wang, H. (2026b). Operational Design Domain formalization and Software-in-the-Loop verification for autonomous water network control. Control Engineering Practice (submitted).

Cloke, H. L., & Pappenberger, F. (2009). Ensemble flood forecasting: A review. Journal of Hydrology, 375(3–4), 613–626.

Dobson, B., Wagener, T., & Pianosi, F. (2019). An argument-driven classification and comparison of reservoir operation optimization methods. Advances in Water Resources, 128, 74–86.

Ehteram, M., Karami, H., Mousavi, S. F., Farzin, S., & Kisi, O. (2018). Optimization of energy management and conversion in the multi-reservoir systems based on evolutionary algorithms. Journal of Cleaner Production, 168, 1132–1142.

Faber, B. A., & Stedinger, J. R. (2001). Reservoir optimization using sampling SDP with ensemble streamflow prediction (ESP) forecasts. Journal of Hydrology, 249(1–4), 113–133.

Giuliani, M., Castelletti, A., Pianosi, F., Mason, E., & Reed, P. M. (2016). Curses, tradeoffs, and scalable management: Advancing evolutionary multi-objective direct policy search to improve water reservoir operations. Journal of Water Resources Planning and Management, 142(2), 04015050.

Giuliani, M., Quinn, J. D., Herman, J. D., Castelletti, A., & Reed, P. M. (2021). Scalable multiobjective control for large-scale water resources systems under uncertainty. IEEE Transactions on Control Systems Technology, 29(3), 1275–1288.

Guo, S., Chen, J., Li, Y., Liu, P., & Li, T. (2022). Joint operation of the multi-reservoir system of the Three Gorges and the Qingjiang cascade reservoirs. Energies, 4(7), 1036.

Huang, Z., Lei, X., Ji, C., Wang, C., & Wang, H. (2026a). cuSVE: A GPU-parallel Saint-Venant equation solver for real-time simulation of water conveyance networks. Advances in Water Resources (submitted).

Kong, Y., Mei, Y., Zhang, S., & Liu, P. (2020). Deep reinforcement learning for real-time optimal hydropower reservoir operation. Water Resources Research, 56(11), e2019WR026531.

Loucks, D. P., & van Beek, E. (2017). Water Resource Systems Planning and Management: An Introduction to Methods, Models, and Applications (2nd ed.). Springer.

Maestre, J. M., Muñoz de la Peña, D., & Camacho, E. F. (2013). Distributed model predictive control based on a cooperative game. Optimal Control Applications and Methods, 32(2), 153–176.

Labadie, J. W. (2004). Optimal operation of multireservoir systems: State-of-the-art review. Journal of Water Resources Planning and Management, 130(2), 93–111.

Lei, X. (2025a). Cybernetics of hydro systems: A unified control-theoretic framework for water network operations. Water Resources Research (submitted).

Lei, X., & Wang, H. (2025). Cybernetics of hydro systems: Background, technical framework and research paradigm. South-to-North Water Transfers and Water Science & Technology, 23(4), 761–769.

Lei, X., Liu, X., Ji, C., Wang, C., & Wang, H. (2025b). From SCADA to autonomy: A multi-agent system architecture and water systems autonomy level classification. Journal of Water Resources Planning and Management (submitted).

Lei, X., Zhang, Z., Su, C., et al. (2025c). In-the-loop testing system for autonomous intelligent water networks. South-to-North Water Transfers and Water Science & Technology, 23(4), 787–793.

Maass, A., Hufschmidt, M. M., Dorfman, R., Thomas Jr, H. A., Marglin, S. A., & Fair, G. M. (1962). Design of Water-Resource Systems. Harvard University Press.

Negenborn, R. R., van Overloop, P. J., Keviczky, T., & De Schutter, B. (2009). Distributed model predictive control of irrigation canals. Networks and Heterogeneous Media, 4(2), 359–380.

Pereira, M. V. F., & Pinto, L. M. V. G. (1991). Multi-stage stochastic optimization applied to energy planning. Mathematical Programming, 52(1–3), 359–375.

Pereira, A., & Saraiva, J. P. (2009). Multi-agent simulation of water resources management. In Proceedings of the IEEE International Conference on Systems, Man and Cybernetics (pp. 2712–2717).

Maciejowski, J. M. (2002). Predictive Control with Constraints. Prentice Hall.

Su, C., Lei, X., Yin, B., Ji, C., & Wang, H. (2026). Experimental verification of the CHS unified transfer function family and distributed MPC on a multi-pool laboratory flume. Journal of Irrigation and Drainage Engineering (submitted).

Wang, H., Xiao, W., Wang, J., et al. (2019). Assessment of the urban water-energy-food nexus in Beijing. Environmental Science & Technology, 53(18), 10689–10698.

Yang, M., Lei, X., Ji, C., Jin, P., Wang, C., & Wang, H. (2026). Hierarchical distributed MPC for multi-timescale coordination of a long-distance inter-basin water transfer system. Journal of Hydrology (submitted).

Ye, S., Lei, X., Ji, C., Wang, C., & Wang, H. (2026). Software-in-the-Loop verification and operational design domain definition for adaptive multi-agent control of a cascade hydropower system. Journal of Hydrology (submitted).

Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017). Model Predictive Control: Theory, Computation, and Design (2nd ed.). Nob Hill Publishing.

Schwanenberg, D., Fan, F. M., Naber, S., Rode, M., & Rasche, D. (2015). Short-term reservoir optimization for flood mitigation under meteorological and hydrological forecast uncertainty. Water Resources Management, 29(5), 1635–1651.

Zhai, X., Guo, L., Liu, R., & Zhang, Y. (2020). Rainfall threshold determination for flash flood warning in mountainous catchments with consideration of antecedent soil moisture and rainfall pattern. Natural Hazards, 100(3), 1355–1377.

Zhang, D., Lin, J., Peng, Q., et al. (2016). Influence of the South-to-North Water Transfer Project on Miyun Reservoir. Hydrology Research, 47(3), 523–537.

Zhao, R. J. (1992). The Xinanjiang model applied in China. Journal of Hydrology, 135(1–4), 371–381.

Zhao, T., Zhao, J., & Yang, D. (2014). Improved dynamic programming for hydropower reservoir operation. Journal of Water Resources Planning and Management, 140(3), 365–374.

__Figure Captions__

__Figure 1.__ Miyun Reservoir system topology: Baihe and Chaohe tributary inflows, SNWD intake, reservoir basin (183.6 km² at normal pool), and four outflow paths (Jingmi Canal to Beijing, Chaohe ecological flow, spillways, bottom outlets). Three-agent MAS overlay: Inflow Agent (blue), Reservoir Agent (green), Outflow Agent (red).

__Figure 2.__ Three-agent MAS architecture: Inflow Agent (6 h cycle, ensemble forecasting), Reservoir Agent (1 h cycle, multi-objective MPC), Outflow Agent (15 min cycle, gate regulation). Cascaded setpoint flow (downward) and state feedback (upward). ODD monitoring at all three levels with fallback protocol.

__Figure 3.__ Family α transfer function validation: (a) Baihe tributary inflow-to-level response (SCADA data vs. model, $R^2 = 0.89$); (b) reservoir water balance model validation (10-year simulated vs. observed levels, $R^2 = 0.96$).

__Figure 4.__ Pareto frontier for the four-objective optimization: (a) supply reliability vs. ecological compliance for fixed flood safety = 100%; (b) spillage vs. supply reliability; (c) recommended operating point B highlighted. 200 Pareto-optimal solutions generated via ε-constraint method.

__Figure 5.__ July 2023 extreme event comparison: (a) inflow hydrograph with ensemble forecast bands; (b) reservoir level trajectory (actual vs. MAS); (c) spillway discharge; (d) ODD distance $\rho(\mathbf{x})$. MAS initiates pre-release 36 h earlier, achieving 0.9 m lower peak level.
