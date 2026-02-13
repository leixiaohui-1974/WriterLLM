# Response to Review — Paper P1c Iteration 2

**Reviewer**: C (Cross-disciplinary Scholar)
**Review Score**: 7.5/10 — Minor Revision

---

## Major Issues

### M1. Differentiation from "Smart Water" and "Digital Twin"
**Response**: Accepted. We will add a new paragraph at the end of §2.2 explicitly positioning CHS:
"需要指出, 水系统控制论与当前水利行业广泛讨论的'智慧水务'(smart water)和'数字孪生'(digital twin)并非替代关系, 而是提供了不同层次的理论支撑. '智慧水务'主要关注数据驱动的分析与异常检测, 是以数据为中心的信息化范式; '数字孪生'提供了虚拟仿真环境用于方案推演, 是以模型为中心的仿真范式; 水系统控制论则独特地提供了控制论理论基础——形式化的模型层级、稳定性保证和闭环自主运行架构, 是以控制为中心的自主化范式[56]. 三者并非互斥, 而是互补: 智慧水务提供数据基础, 数字孪生提供仿真平台, 水系统控制论提供闭环控制内核."

### M2. Climate Non-Stationarity Underexploited
**Response**: Accepted. This is a compelling argument that deserves more prominence. We will expand §2.1 Phase 3 to include:
- A more prominent citation of Milly et al. (2008) [42] and add Montanari et al. (2013) [59]
- An explicit statement: "传统WRSA的第一和第二阶段均建立在水文平稳性假设之上——来水频率分析和设计保证率计算都假定历史统计规律可外推至未来. Milly等[42]指出'平稳性已死'(stationarity is dead), 气候变化正在改变水文极端事件的频率、强度和时序, 使基于历史频率分析的静态配置方案变得不可靠. 这一根本性挑战构成了从静态配置向实时反馈控制转型的最强理论驱动力——只有具备实时感知和自适应反馈能力的控制系统, 才能应对一个统计性质不断变化的水文世界"

### M3. Cross-Domain Autonomous Systems Connection
**Response**: Accepted. We will add a brief paragraph in §1 or §6:
"水系统的自主运行转型并非孤立事件, 而是全球关键基础设施智能化浪潮的组成部分. 电力系统正在从集中调度向分布式自主管理转型(以应对大规模新能源并网), 交通系统从人工指挥向自动驾驶和自主空管演进, 制造业通过工业4.0实现柔性自主生产. 水系统的特殊挑战在于其运行奇异性(§3.1命题一)——故障不可逆、极端空间分布、开放边界环境耦合——使其自主化路径不能简单照搬上述领域的经验, 需要建立专门的理论体系. 水系统控制论正是水利工程领域对这一全球技术趋势的理论回应."

### M4. Narrative Balance — International Landscape
**Response**: Partially accepted. We will add a paragraph in §4.2 surveying international developments:
"在实时水系统控制领域, 国际上已形成若干活跃的研究群体: 荷兰Delft学派(van Overloop [27], Negenborn [16])在明渠MPC和分布式协调方面做出了开创性贡献; 澳大利亚学派(Mareels [53], Cantoni [54])在灌溉系统工程实践中积累了丰富经验; 法国学派(Litrico & Fromion [13], Malaterre [25])在渠道建模和控制算法分类方面建立了标准性成果; 以色列和西班牙学者在管网压力管理方面有重要突破. 这些工作主要聚焦于特定子系统(渠道、管网)的控制方法, 水系统控制论的贡献在于提供一个跨子系统的统一理论框架, 将这些分散的成果纳入一个系统化的学科体系."

However, we respectfully maintain the Wang Hao legacy framing as central to a 中国科学 paper specifically positioned as a 学科传承综述.

### M5. WSAL Calibration Caveat
**Response**: Accepted. Will add: "上述量化判据为基于工程经验的初步建议值, 具体阈值需通过工程实践和行业共识逐步校准, 并参考航空航天(DO-178C)和汽车(ISO 26262)领域安全关键系统认证标准的经验确定."

---

## Minor Issues

### m1. Wang Hao "创立" Phrasing
**Response**: Accepted. Will revise "创立" to "系统发展" — acknowledging WRSA's international roots while maintaining appropriate credit.

### m2. English Abstract Length
**Response**: Will review and condense if exceeding 200 words.

### m3. Figure Placeholders
**Response**: Noted. Figures will be prepared for submission; current review focuses on text content.

### m4. "运行奇异性" Clarification
**Response**: Will add parenthetical: "运行奇异性(此处'奇异性'指水系统独特性质组合的不可约性, 非AI领域的'技术奇点'概念)"

### m5. Data Quality Challenges
**Response**: Will add a sentence in §4.1 HydroOS section: "需要指出, 中国水利工程SCADA系统普遍存在传感器覆盖不完整、数据传输间断和量测精度不均匀等问题. HydroOS感知层的数据质量评估与融合处理功能, 正是针对这一现实挑战而设计."

### m6. "二八现象" Citation
**Response**: Will add: "据作者团队对胶东调水工程2018-2020年调度日志的统计分析" as the source.

### m7. Reference Format
**Response**: Will ensure all references conform to GB/T 7714 format.
