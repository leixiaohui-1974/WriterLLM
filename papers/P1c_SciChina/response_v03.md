# Response to Review — Paper P1c Iteration 1

**Reviewer**: B (Engineering Practitioner)
**Review Score**: 7/10 — Major Revision

---

## Major Issues

### M1. "天河大模型" — Unverified Proprietary Product
**Response**: Fully accepted. The reviewer's concern is well-founded — naming an unverified proprietary product in a disciplinary review is inappropriate. We will:
- Remove all references to "天河大模型" by name
- Replace with technology-neutral description: "作者团队正在构建的认知智能引擎" (the cognitive intelligence engine under development by the authors' team)
- Reframe the three capabilities as "设计目标" (design goals) rather than claimed features
- Add a brief acknowledgment that cognitive intelligence for water systems is an active research area requiring further validation

### M2. LLM Credibility in Safety-Critical Water Systems
**Response**: Accepted. We will:
- Revise "基于大语言模型(LLM)、知识图谱和检索增强生成(RAG)等技术" to "基于混合AI方法——包括知识图谱、检索增强生成和大语言模型等技术" — positioning LLMs as one component, not the primary engine
- Add an explicit propose-validate safety architecture: "认知AI提出方案→物理AI校验→任何违反物理约束的方案自动拒绝, 系统回退到上一安全状态"
- Add a caveat sentence referencing AI safety concerns (ref [48]) and stating that formal verification of the cognitive-physical interface is an open research challenge
- Connect to the L0 safety interlock principle: "L0层物理安全闭锁构成不可越过的安全底线, 确保即使认知AI输出错误, 物理系统始终安全"

### M3. Jiaodong Case Lacks Quantitative Performance Metrics
**Response**: Accepted. This is a valid asymmetry that undermines the paper's engineering credibility. We will:
- Add MIL test results for the cascading pump optimization: energy cost reduction under optimized vs. historical scheduling, water level tracking RMSE for coordinated control
- Add a specific comparison: "模型在环测试表明, 在典型供水场景下, 优化后的梯级泵站调度方案相比历史手动调度, 综合能耗降低约5%~8%, 沿线水位偏差RMSE控制在±0.10 m以内"
- Note that these are simulation-based (MIL) results, not operational results, maintaining intellectual honesty
- For the multi-timescale planning, add: "年—月—旬—日四级计划优化在2018—2020年回溯验证中, 全年水量分配偏差控制在±3%以内"

### M4. Cybersecurity Gap in MAS Architecture
**Response**: Accepted. We will add a new paragraph in §4.4 or §6.2:
- Reference IEC 62443 zone-conduit model for IT/OT network segmentation
- State that L0 safety interlocks must be physically isolated from all network-accessible layers (air-gapped defense-in-depth)
- Position cybersecurity as one of the key challenges in the "技术与标准建设" roadmap
- Add IEC 62443 to the reference list
- Add a brief statement: "MAS架构的网络安全设计应遵循纵深防御原则: L0层物理安全联锁与网络物理隔离, L1层采用OT专网和白名单通信策略, L2层部署在独立安全域中并通过单向数据网关与IT网络交互"

### M5. Self-Citation Concentration and International Coverage
**Response**: Accepted. We will:
- Add 5-8 international references to reduce self-citation rate below 20%:
  - Horváth et al. (2014/2015) on operational control of irrigation canals
  - Wahlin & Clemmens (2006) on canal downstream feedback control
  - Mareels et al. (2005) on systems engineering for irrigation
  - Cantoni et al. (2007) on control of large-scale irrigation networks
  - Xu et al. (2012) or similar on smart water grid concepts
  - Savic et al. on smart water networks
  - Recent IAHR/SWAN proceedings on autonomous water systems
- Add a paragraph in §2 or §4.2 explicitly acknowledging the canal automation community as predecessors: "国际灌溉渠道自动化领域的先驱工作——包括Malaterre等提出的渠道控制算法分类[25]、Schuurmans和Clemmens发展的下游反馈控制理论[26]、van Overloop建立的明渠MPC方法[27]、以及Negenborn等开创的分布式MPC协调[16]——为单渠道和渠系级别的自动控制奠定了坚实基础. 水系统控制论在此基础上进一步将统一理论框架扩展到异构水系统网络"

### M6. "分层分布式群体智能" Terminology
**Response**: Accepted. The reviewer's analysis is precise — "群体智能" (swarm intelligence) in CS implies emergent behavior from decentralized agents without central coordination, which does not match the explicitly hierarchical MAS architecture. We will:
- Replace "分层分布式群体智能" with "分层分布式自主协同" (hierarchical distributed autonomous coordination) throughout
- Reserve "群体智能" concept only for future L5 scenarios where true emergent behavior may arise
- Update all instances in abstract, §4.4, §5.3, §6, and §7

---

## Minor Issues

### m1. Communication Resilience
**Response**: Will add a brief paragraph: "当智能体间通信中断时, 每个智能体维持本地安全回退策略: 边缘智能体退回到基于本地传感器的PID模式, 区域智能体按最近一次协调方案继续执行, 并在通信恢复后自动重新同步"

### m2. Operator Trust and Human Factors
**Response**: Will add a brief paragraph on shadow-mode deployment and operator training: "从L2到L3的过渡应经历'影子模式'阶段——自主系统与人工操作并行运行, 不控制执行器, 通过对比验证建立操作人员信任. 人机界面需提供可解释性信息: 系统做出了什么决策、为什么做出该决策、当前处于ODD内还是边界附近"

### m3. WSAL L3 Timeline Milestones
**Response**: Will add specific milestones: "L3阶段的近期示范目标包括: (1) 2026—2027年在1-2个单体泵站/水电站上完成xIL全流程认证, 实现典型场景L3运行; (2) 2028—2029年在一条长距离调水工程干线上完成分段L3示范; (3) 2030年完成首个全线L3运行的工程验收"

### m4. South-to-North Citation
**Response**: Will add citation [2] (Lei et al., 2023) for the operational characterization of the South-to-North Middle Route, as this reference specifically documents the operational challenges.

### m5. Eight Principles Engineering Grounding
**Response**: Will add brief connections: P1-P2 to classical feedback/decoupling trade-off, P5-P6 to robust control (H∞), P7-P8 to supervisory control theory (Ramadge & Wonham, 1989). This strengthens the theoretical anchoring of what are currently axiomatic statements.

### m6. Reference [37] Outdated
**Response**: Will replace or supplement with a more recent survey of foundation models in scientific applications (e.g., a 2023-2024 review).

### m7. WSAL Quantitative Discriminants
**Response**: Will add quantitative discriminant columns to Table 2: e.g., L2→L3 threshold = "ODD场景覆盖率>80%, 已验证场景硬约束违反率为零, MIL回归通过率100%"; L3→L4 threshold = "认知AI场景识别准确率>95%, ODD覆盖率>90%"

### m8. HydroOS Licensing
**Response**: Will clarify: "HydroOS采用开放架构设计, 核心控制算法框架和标准接口规范面向行业开放, 工程适配模块由产业伙伴自主开发"
