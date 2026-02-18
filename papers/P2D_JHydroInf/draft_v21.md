*Manuscript prepared for Journal of Hydroinformatics*

__Energy-Aware Hierarchical Distributed MPC with Digital-Twin xIL for the Jiaodong Water Transfer System: A CHS-Governed Deployment Framework__

__Liu Xiaowei__1, __Xiaohui Lei__1,2*, __Ji Chen__3, __Chao Wang__2, __Yang Minghan__2, __Jin Pengyu__2, __Hao Wang__2

1 School of Water Resources, Hebei University of Engineering, Handan 056038, China
2 China Institute of Water Resources and Hydropower Research (IWHR), Beijing 100038, China
3 College of Water Resource and Hydropower, Sichuan University, Chengdu 610065, China

*Corresponding author: Xiaohui Lei (lxh@iwhr.com)*

__Abstract__

Long-distance inter-basin water transfer systems must simultaneously satisfy hydraulic safety, delivery reliability, and energy efficiency under multi-timescale disturbances. This paper presents an energy-aware hierarchical distributed model predictive control (HDMPC) framework integrated with a digital-twin x-in-the-loop (xIL) verification chain for the Jiaodong water transfer system. The controlled system is formulated using the Cybernetics of Hydro Systems (CHS) six-element representation $\Sigma=(P,A,S,D,C,O)$ with a unified actuator boundary relation. A staged verification chain covering model-in-the-loop, software-in-the-loop, and hardware-in-the-loop testing ensures systematic validation prior to field deployment. The framework is validated on the Jiaodong system through simulation benchmarks, hardware-in-the-loop tests, and field pilot campaigns, demonstrating reductions in unit transfer energy consumption while maintaining hydraulic constraint compliance and rollback capability.

__Keywords__: digital twin; xIL; HDMPC; energy optimization; water transfer; CHS

## 1. Introduction

A significant engineering gap persists between algorithmic optimization research and auditable field deployment in long-distance regulated water transfer systems. The Jiaodong water transfer system, one of China's major inter-basin conveyance projects, requires simultaneous satisfaction of hydraulic safety, delivery reliability, and energy efficiency under multi-timescale disturbances including demand variation, inflow uncertainty, and equipment degradation.

While model predictive control (MPC) and its distributed variants have demonstrated promise in simulation studies, their transition to operational deployment in critical water infrastructure demands systematic verification and validated authority-transfer protocols. This paper addresses that transition by combining three elements:

- a unified hydraulic model hierarchy and actuator characteristic based on the Cybernetics of Hydro Systems (CHS) formulation,
- an energy-aware hierarchical distributed MPC (HDMPC) architecture tailored to the Jiaodong system topology,
- a digital-twin x-in-the-loop (xIL) verification chain that provides staged validation from simulation through hardware testing to field pilot deployment.

*[TODO: Expand with literature review on MPC for water transfer systems, digital twin deployment methodologies, and energy optimization in pumped conveyance. Articulate specific contributions relative to prior work.]*

## 2. System formulation

The controlled water transfer system is represented using the CHS six-element formulation:

$$
\Sigma = (P, A, S, D, C, O) \tag{1}
$$

Actuator boundary behavior follows the unified local relation:

$$
\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{2}
$$

Symbols and units are defined as follows: $Q$ [m$^3$/s] is the flow rate, $H$ [m] is the hydraulic head, $A_s$ [m$^2$] is the storage cross-sectional area, $\alpha$ [m$^2$/s per unit] is the actuator gain coefficient, and $u$ [-] is the normalized actuator command.

## 3. Problem definition

### 3.1 Multi-objective operational requirement

The operational control problem addresses three coupled objectives under safety constraints:

1. **Hydraulic safety**: maintain water level/pressure within hard bounds;
2. **Delivery service**: satisfy planned transfer targets and schedule adherence;
3. **Energy efficiency**: minimize pumping energy and peak-demand penalties.

### 3.2 Baseline optimization structure

For control region $i$, the stage cost is initialized as:

$$
J_i = \sum_{k=0}^{N_p-1} \left( \|y_i(k)-r_i(k)\|_{Q_i}^2 + \|\Delta u_i(k)\|_{R_i}^2 + \lambda_E \, E_i(k) \right) \tag{3}
$$

where $E_i(k)$ is an energy proxy coupled with the pump operating point and hydraulic head, and $\lambda_E$ is the energy weighting coefficient calibrated to balance energy cost against tracking performance.

## 4. Digital-twin xIL verification chain

The framework employs a staged verification chain to bridge the gap from controller design to operational deployment:

1. **Model-in-the-loop (MiL)**: hydraulic model consistency verification and scenario generation across nominal and disturbed operating conditions;
2. **Software-in-the-loop (SiL)**: controller software verification with deterministic replay to confirm algorithmic correctness;
3. **Hardware-in-the-loop (HiL/xIL)**: SCADA/PLC interface testing to verify communication timing, alarm routing, and fallback execution under realistic conditions;
4. **Pilot deployment**: bounded live-shift trials under defined operational design domain (ODD) constraints with operator supervision.

Each stage produces traceable verification artifacts before progression to the next stage is permitted.

*[TODO: Expand with detailed description of each xIL stage, artifact specifications, and stage-gate criteria. Include schematic figure of the verification chain.]*

## 5. Deployment verification gates

Authority transfer from operator-assisted to bounded autonomous operation is governed by four verification criteria:

- **Observability**: all required sensor signals and timestamps are available and within quality thresholds;
- **Determinism**: deterministic replay of recorded scenarios reproduces controller decision traces within specified tolerances;
- **Safety**: no unresolved hard-constraint violations are observed across the full xIL scenario set;
- **Fallback**: rollback to operator-assisted operation is verified to complete within a bounded time window.

Progression to bounded autonomous execution requires satisfaction of all four criteria.

*[TODO: Formalize gate criteria with quantitative thresholds. Add table of specific pass/fail metrics for each gate applied to the Jiaodong system.]*

## 6. Study area and system description

*[TODO: Describe the Jiaodong water transfer system: geographic scope, canal reaches, pump stations, reservoirs, control infrastructure, and SCADA architecture. Include system schematic figure and key hydraulic parameters table.]*

## 7. Validation protocol and energy KPIs

The validation protocol comprises three tiers aligned with the xIL deployment chain:

1. **Simulation benchmark**: MiL/SiL scenarios covering nominal and disturbed operating conditions, with HDMPC performance measured against rule-based and single-level MPC baselines;
2. **Hardware-in-the-loop verification**: HiL/xIL testing with SCADA/PLC interfaces to confirm timing, alarm routing, and fallback execution under realistic communication conditions;
3. **Field pilot campaign**: bounded live-shift trials on the Jiaodong system under ODD constraints with operator-supervised authority transfer.

Energy performance is assessed through three mandatory KPIs per campaign window:

- **Unit transfer energy** $E_{\text{unit}}$ [kWh/m$^3$]: total pumping energy normalized by delivered volume;
- **Peak power ratio** $R_{\text{peak}}$: peak demand relative to scheduled baseline;
- **Off-peak utilization ratio** $R_{\text{offpeak}}$: fraction of pump dispatch scheduled during off-peak tariff periods.

Energy improvements are reported only when accompanied by full hydraulic safety compliance and verified fallback capability across all verification gates.

## 8. Results and Validation

*[TODO: Present quantitative results from the Jiaodong deployment. Include:]*

- *MiL/SiL scenario test outcomes and pass rates*
- *Energy KPI comparisons: unit transfer energy $E_{\text{unit}}$ [kWh/m$^3$], peak power ratio, off-peak utilization*
- *HDMPC tracking performance against baseline operational schedules*
- *xIL evidence chain completeness and deployment gate outcomes*
- *Field campaign statistics from pilot shift windows*

## 9. Discussion

*[TODO: Interpret results in the context of:]*

- *Energy savings versus hydraulic safety trade-offs observed in field trials*
- *Practical challenges of xIL deployment chain execution at Jiaodong scale*
- *Comparison with existing MPC and digital-twin deployment studies in water transfer*
- *Limitations of the current study and conditions for cross-site transferability*

## 10. Conclusions

*[TODO: Summarize key findings and contributions:]*

- *Energy-aware HDMPC integration results for the Jiaodong water transfer system*
- *Digital-twin xIL deployment chain effectiveness for authority transfer*
- *Governance gate framework utility for auditable field deployment*
- *Recommendations for future work and broader applicability*

## Acknowledgments

*[TODO: Add funding sources, project grants, and acknowledgments.]*

## References

*[TODO: Add references.]*
