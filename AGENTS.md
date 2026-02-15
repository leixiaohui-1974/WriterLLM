\# CHS论文体系 — 自动写作引擎



\## A. 项目总览



本项目是"水系统控制论 (Cybernetics of Hydro Systems, CHS)"论文群的自动化写作系统。共25篇论文（21篇英文 + 4篇已发表中文），分5条研究线、4个批次推进。目标：在最少人工干预下，通过迭代式"写作—评审—修改"循环，完成全部论文的高质量投稿稿件。



\*\*工作目录\*\*: 所有论文稿件存放在 `papers/` 目录中。已完成初稿的论文已在其中，新写论文也存入对应子目录。每次开始工作前先 `ls papers/` 查看当前文件结构。



\*\*核心规则\*\*: 一切可恢复的状态都写入文件，不依赖对话记忆。中断后读取 `progress.json` 和各论文 `status.json` 即可恢复。



---



\## B. 核心作者信息



\### 通讯作者

\- \*\*姓名\*\*: 雷晓辉 (Xiaohui Lei)

\- \*\*职务\*\*: 河北工程大学学术副校长

\- \*\*头衔\*\*: 国家万人计划入选者，二级教授，博士

\- \*\*研究方向\*\*: 水网自主控制系统、CHS理论、HydroOS水网操作系统、多智能体系统

\- \*\*核心成果\*\*: 200+论文(150+ SCI)，60+专利，10部专著，30+软件著作权

\- \*\*主要荣誉\*\*: 国家科技进步一等奖1项、省部级一等奖8项

\- \*\*累计科研经费\*\*: 超过2亿元

\- \*\*教育背景\*\*: 清华大学水利水电工程(1993-1998)，中国水科院硕士(导师王浩院士)，日本筑波大学博士(导师前川高明教授)

\- \*\*Email\*\*: lxh@iwhr.com



\### 主要合作者

\- \*\*王浩 (Wang Hao)\*\*: 中国工程院院士，中国水利水电科学研究院

\- \*\*姬辰 (Ji Chen)\*\*: 四川大学（论文中使用 Chen Ji 或 Ji Chen）

\- \*\*王超 (Wang Chao)\*\*: 中国水利水电科学研究院

\- \*\*龙岩 (Long Yan)\*\*: 合作者

\- \*\*刘晓维 (Liu Xiaowei)\*\*: 学科建设论文负责人



\### 博士生团队

\- \*\*陈凯歌 (Chen Kaige)\*\*: 实验线A，双水箱MBD/xIL平台

\- \*\*苏超 (Su Chao)\*\*: 实验线B，水槽DMPC实验验证

\- \*\*黄志锋 (Huang Zhifeng)\*\*: 算法线，GPU并行计算

\- \*\*吴辉明 (Wu Huiming)\*\*: 工程线，密云水库MAS/MBD

\- \*\*白亚开 (Bai Yakai)\*\*: 水槽团队，OpenModelica组件化建模

\- \*\*尹兵宽 (Yin Bingkuan)\*\*: 水槽团队，Simulink快速原型

\- \*\*叶尚君 (Ye Shangjun)\*\*: 工程线，沙坪水电站

\- \*\*张雷 (Zhang Lei)\*\*: 工程线，沙坪ODD扩展

\- \*\*杨明晗 (Yang Minghan)\*\*: 工程线，胶东调水

\- \*\*金鹏宇 (Jin Pengyu)\*\*: 工程线，胶东调水



\### 单位

\- \*\*第一单位\*\*: 河北工程大学水利水电学院, 邯郸 056038

\- \*\*合作单位\*\*: 四川大学, 成都 610065; 中国水利水电科学研究院, 北京 100038

\- \*\*注意\*\*: 所有论文中不使用"State Key Laboratory"



---



\## C. 三篇已完成核心论文（理论基座）



以下论文已有高质量初稿存放在 `papers/` 目录中，是整个体系的理论基座。所有后续论文必须与之保持概念、术语、数学符号的完全一致。\*\*写任何新论文前，必须先读取这三篇的内容。\*\*



\### C.1 Paper P1a — WRR v9（~15,000词，独著）



\*\*文件位置\*\*: `papers/` 目录中的 WRR 相关文件

\*\*标题\*\*: Cybernetics of Hydro Systems: A Unified Control-Theoretic Framework for Water Network Operations

\*\*期刊\*\*: Water Resources Research (AGU)

\*\*作者\*\*: Xiaohui Lei (sole author)



\*\*结构\*\*:

1\. Introduction

2\. Why Water Systems Demand a Dedicated Control Science

&nbsp;  - 2.1 Operational Singularity (Definition 1: 五个共现属性)

&nbsp;  - 2.2 Disciplinary Fragmentation (Table 1: 7概念×5子领域术语映射)

&nbsp;  - 2.3 IWRM–Operations Gap

3\. CHS Formalization

&nbsp;  - 3.1 Definition 2 (六元组)

&nbsp;  - 3.2 Proposition 1 (结构同构性)

&nbsp;  - 3.3 Six-Element Architecture (Table 2)

4\. Unified Model Hierarchy（数学核心）

&nbsp;  - 4.1 Diffusion Wave: Common Ancestor

&nbsp;  - 4.2 Theorem 2: Unified Transfer Function Family

&nbsp;    - Family α (积分型): G(s) = (1+τₘs)·e^(−τᵈs) / (Aₛ·s)

&nbsp;    - Family β (自调节型): H(s) = (1−KXs) / (1+K(1−X)s)

&nbsp;  - 4.3 Corollary 1: Muskingum–IDZ Duality

&nbsp;  - 4.4 Pipe Compliance Integrator

&nbsp;  - 4.5 Lemma 3: Unified Actuator Characteristic (ΔQ = αΔu + β\_up·ΔH\_up + β\_dn·ΔH\_dn)

&nbsp;  - 4.6 Five-Level Hierarchy (LSV→IDZ→ID→I→SS)

&nbsp;  - 4.7 IDZ Derivation

&nbsp;  - 4.8 Theorem 3: Model–Layer Correspondence

5\. Eight Governing Principles

&nbsp;  - Operational Tetrad: Feedback, Decoupling, Order Reduction, Emergence

&nbsp;  - Resilience Tetrad: Robustness, Coordination, Adaptation, Hierarchy

&nbsp;  - Inter-Principle Tradeoffs

6\. Illustrative Applications (Single Pool LQR → Multi-Pool DMPC → Cross-Sector Transfer)

7\. Autonomous Operation Framework (HDC → ODD → MAS → WSAL L0-L5)

8\. Positioning CHS

9\. Research Agenda \& Testable Predictions

10\. Conclusion



\### C.2 Paper P1b — Nature Water Perspective（~4,300词）



\*\*文件位置\*\*: `papers/` 目录中的 Nature Water 相关文件

\*\*标题\*\*: Towards Autonomous Water Networks

\*\*期刊\*\*: Nature Water (Perspective)

\*\*作者\*\*: Xiaohui Lei, Chen Ji, Chao Wang, Hao Wang



\*\*结构\*\*: Infrastructure–Intelligence Gap → Paradigm Shift → Structural Invariants → CHS Framework → WSAL Classification → Early Implementations → Responsible Deployment → Outlook



\*\*与P1a的分工\*\*: P1b面向广泛读者，无数学公式，强调问题意识和社会影响。P1a是完整技术论文。两篇无内容重复。



\### C.3 Paper P1c — 中国科学 v2（~17,000字）



\*\*文件位置\*\*: `papers/` 目录中的中国科学相关文件

\*\*标题\*\*: 从水资源配置到水网自主运行：水系统控制论的学科基础与工程范式

\*\*期刊\*\*: 中国科学：技术科学

\*\*作者\*\*: 雷晓辉, 姬辰, 王超, 王浩



\*\*结构\*\*:

1\. 引言 → 2. 学科演进(三阶段) → 3. 理论体系(六元架构+传递函数族+八原理+执行器) → 4. 关键技术(HydroOS+HDMPC+xIL+MAS) → 5. 工程实践(沙坪+胶东) → 6. 发展路线(WSAL) → 7. 总结



\*\*独有内容\*\*: 王浩WRSA学术传承、MAS=HDC+ODD+认知智能公式、HydroOS四层架构、多时间尺度(年/月/旬/日)HDMPC



\*\*重要术语约定\*\*:

\- 正文用"水系统控制论"而非CHS缩写

\- 用"分层分布式控制"(HDC)而非"分布式控制"

\- 用"自主运行"而非"智能运控"

\- 南水北调中线不作为成功案例（仍处L2），仅作背景

\- 沙坪和胶东定位为"前期探索"



\### P1三篇差异化红线



| 维度 | P1a (WRR) | P1b (Nature Water) | P1c (中国科学) |

|------|-----------|---------------------|----------------|

| 定位 | 完整技术论文 | 远景展望短文 | 学科传承综述 |

| 数学 | 完整推导含证明 | 无公式 | 关键公式+物理意义 |

| 案例 | 抽象通用算例 | 无具体案例 | 沙坪+胶东 |

| 独有 | Muskingum-IDZ对偶证明 | 范式转移+社会影响 | 王浩传承+HydroOS+xIL |

| 作者 | Lei独著 | Lei/Ji/Wang C/Wang H | Lei/Ji/Wang C/Wang H |



\*\*三篇文字重复率必须 <10%。\*\*



---



\## D. 25篇论文完整规格



\### D.1 理论奠基线（5篇）



| 编号 | 标题 | 期刊 | 领衔 | 状态 | 批次 |

|------|------|------|------|------|------|

| P1a | CHS Unified Theory | WRR | 雷(独著) | v9完成 | B1 |

| P1b | Towards Autonomous Water Networks | Nature Water | 雷/姬/王超/王浩 | 初稿完成 | B1 |

| P1c | 水系统控制论学科基础与工程范式 | 中国科学 | 雷/姬/王超/王浩 | v2完成 | B1 |

| P2A | MAS Architecture + WSAL | JWRPM (ASCE) | 雷/张/叶/姬/刘/王/王 | v2完成 | B1 |

| P-DC | Discipline Construction | Env. Model. \& Software | 雷/王浩/龙/刘(刘领衔) | 待写 | B2 |



\### D.2 实验线A — 陈凯歌（3篇）



| 编号 | 核心内容 | 期刊 | 批次 |

|------|----------|------|------|

| CKG-1 | MBD七层框架，双水箱FMI→Simulink→xIL | J. Hydroinformatics | B2 |

| CKG-2 | ODD形式化定义 + SiL闭环验证 | Control Eng. Practice | B3 |

| CKG-3 | HiL验证 + 自适应MAS + 工程级对比 | JWRPM (ASCE) | B4 |



渐进逻辑: CKG-1(方法) → CKG-2(软件验证) → CKG-3(硬件验证+迁移)



\### D.3 实验线B — 水槽团队（4篇）



| 编号 | 领衔 | 核心内容 | 期刊 | 批次 |

|------|------|----------|------|------|

| BAK-1 | 白亚开 | OpenModelica组件化水系统建模，开源组件库 | Env. Model. \& Software | B2 |

| YBK-1 | 尹兵宽 | Simulink快速原型+自动代码生成→PLC | SoftwareX | B3 |

| SC-1 | 苏超 | 水槽验证Theorem 2和Corollary 1，多渠池DMPC | J. Irrig. Drain. Eng. | B2 |

| SC-2 | 苏超 | OpenModelica+Simulink+DMPC集成，xIL全流程 | J. Hydrology / WRR | B4 |



工具链三角: BAK-1(建模) + YBK-1(控制器) → SC-2(集成), SC-1(算法) → SC-2(基准)



\### D.4 算法线 — 黄志锋（3篇）



| 编号 | 核心内容 | 期刊 | 批次 |

|------|----------|------|------|

| HZF-1 | GPU并行Saint-Venant求解器(CUDA) | Advances in Water Resources | B2 |

| HZF-2 | 分布式MPC并行QP求解 | JWRPM / WRR | B3 |

| HZF-3 | 图拓扑→GPU求解→数字孪生引擎，开源框架 | Env. Model. \& Software | B4 |



\### D.5 工程线（6篇）



| 编号 | 领衔 | 核心内容 | 期刊 | 批次 |

|------|------|----------|------|------|

| P2B | 叶尚君 | 沙坪SiL+ODD+自适应MAS | J. Hydrology | B3 |

| P2E | 张雷 | 沙坪ODD扩展+WSAL-2→3跨越 | WRR / Control Eng. | B4 |

| P2C | 姬辰 | 胶东三层HDMPC(秒→分钟→小时) | J. Hydrology | B3 |

| P2D | 刘晓维 | 胶东能效优化+数字孪生xIL | J. Hydroinformatics | B4 |

| WHM-1 | 吴辉明 | 密云水库MAS(入库/库区/出库Agent) | JWRPM / J. Hydrol. | B3 |

| WHM-2 | 吴辉明 | 密云MBD七层+数字孪生 | J. Hydroinformatics | B4 |



\### D.6 中文支撑线（4篇已发表）



| 编号 | 标题 | 期刊 | 与英文论文的关系 |

|------|------|------|-----------------|

| Lei 2025a | 水系统控制论：基本原理与理论框架 | 南水北调与水利科技 | P1a中文核心 |

| Lei 2025b | 自主水网：概念、架构与关键技术 | 南水北调与水利科技 | P2A中文核心 |

| Lei 2025c | 水系统在回路测试体系 | 南水北调与水利科技 | xIL方法论基础 |

| Lei 2025d | 从静态水量平衡到动态运行控制 | 南水北调与水利科技 | 学科演进背景 |



---



\## E. 代表作引用清单（自引控制15-25%）



\### 必引（Lei 2025a-d，所有英文论文的Literature Review中自然引用）

1\. 雷晓辉等 (2025a). 水系统控制论：基本原理与理论框架. 南水北调与水利科技(中英文).

2\. 雷晓辉等 (2025b). 自主水网：概念、架构与关键技术. 南水北调与水利科技(中英文).

3\. 雷晓辉等 (2025c). 水系统在回路测试体系：从MiL到PiL. 南水北调与水利科技(中英文).

4\. 雷晓辉等 (2025d). 从静态水量平衡到动态运行控制. 南水北调与水利科技(中英文).



\### 按相关性选引

5\. Lei X.H., Wang H., et al. Cascaded hydropower scheduling optimization. Journal of Hydroinformatics.

6\. Lei X.H., et al. Multi-objective reservoir optimization (NSGA-II). Water Resources Management.

7\. Lei X.H., et al. MPC for canal automation. J. Irrigation and Drainage Engineering.

8\. Lei X.H., et al. Real-time flood forecasting. Journal of Hydrology.

9\. Lei X.H., Wang H., et al. South-to-North Water Diversion dispatching. Water Resources Research.

10\. Lei X.H., et al. SCADA intelligent control. Water Science \& Technology.

11\. Lei X.H., et al. Digital twin for water networks. JWRPM.

12\. Lei X.H., et al. RL for reservoir operation. Env. Modelling \& Software.



\*\*规则\*\*: 每篇论文引4-8篇Lei代表作，不超过总引用25%。调整时优先削减5-12项，保留1-4项。



---



\## F. 引用网络



(a) \*\*理论基座\*\*: 所有论文 → P1a + P2A

(b) \*\*工程→实验\*\*: P2B→CKG-2(ODD), P2E→CKG-3(HiL)

(c) \*\*工程→算法\*\*: P2D→HZF-1(GPU)

(d) \*\*工具链三角\*\*: BAK-1+YBK-1→SC-2, SC-1→SC-2

(e) \*\*建模↔计算\*\*: BAK-1↔HZF-3

(f) \*\*工具复用\*\*: YBK-1→P2B/P2D (Simulink)

(g) \*\*实验→工程\*\*: WHM-2→CKG-1 (MBD迁移)

(h) \*\*中文支撑\*\*: Lei 2025a-d → 所有英文论文

(i) \*\*学科建设\*\*: P-DC→P1a+P1c, P1c/P2D→P-DC



---



\## G. 四批次节奏



| 批次 | 时间 | 论文 | 数量 |

|------|------|------|------|

| B1 | 2026 Q1-Q2 | P1a+P1b+P1c+P2A | 4 |

| B2 | 2026 Q2 | P-DC+CKG-1+SC-1+BAK-1+HZF-1 | 5 |

| B3 | 2026 Q3 | CKG-2+YBK-1+P2B+P2C+WHM-1+HZF-2 | 6 |

| B4 | 2026 Q4-Q1 | CKG-3+SC-2+P2D+P2E+HZF-3+WHM-2 | 6 |



---



\## H. 统一术语表



| English | 中文 | 缩写 | 来源 |

|---------|------|------|------|

| Cybernetics of Hydro Systems | 水系统控制论 | CHS | P1a Def.2 |

| Operational Singularity | 运行奇异性 | OS | P1a Def.1 |

| Structural Isomorphism | 结构同构性 | SI | P1a Prop.1 |

| Water Systems Autonomy Level | 水系统自治等级 | WSAL | P2A |

| Multi-Agent System | 多智能体系统 | MAS | P1c §4.4 |

| Hierarchical Distributed Control | 分层分布式控制 | HDC | P1a §7.1 |

| Operational Design Domain | 运行设计域 | ODD | P1a §7.2 |

| Cognitive Intelligence | 认知智能 | CI | P1c §4.4 |

| Model-Based Definition | 基于模型的定义 | MBD | CKG-1 |

| Design for Operation | 面向运行的设计 | DfO | P-DC |

| X-in-the-Loop | X在环测试 | xIL | Lei 2025c |

| Distributed MPC | 分布式模型预测控制 | DMPC | P1a §6.2 |

| Hierarchical DMPC | 分层分布式MPC | HDMPC | P2C |

| Unified Transfer Function Family | 统一传递函数族 | — | P1a Thm.2 |

| Family α | 积分型: G(s)=(1+τₘs)e^(-τᵈs)/(Aₛ·s) | — | P1a Thm.2 |

| Family β | 自调节型: H(s)=(1-KXs)/(1+K(1-X)s) | — | P1a Thm.2 |

| Muskingum–IDZ Duality | M-IDZ对偶性 | — | P1a Cor.1 |

| Five-Level Hierarchy | LSV→IDZ→ID→I→SS | — | P1a §4.6 |

| HydroOS | 水网操作系统 | — | P1c §4.1 |

| Shaping Control | 塑性调控 | — | P2E |



---



\## I. 数学符号（以P1a为准，所有论文统一）



| 符号 | 含义 | 单位 |

|------|------|------|

| Q, q | 流量(绝对/偏差) | m³/s |

| H, h, y | 水位/水头(绝对/偏差) | m |

| Aₛ | 水面面积/储能系数 | m² |

| τᵈ | 传输延迟 | s |

| τₘ | 回水时间 | s |

| K, X | Muskingum参数 | s, — |

| Cₕ | 管道弹性容量 | m·s² |

| α | 执行器增益 | m²/s per unit |

| β\_up, β\_dn | 上下游水头影响系数 | m²/s per m |

| u | 执行器开度/转速 | — |

| G(s), H(s) | 积分型/自调节型传递函数 | — |



---



\## J. 期刊格式速查



| 期刊 | 字数 | 摘要 | 参考格式 | 特殊要求 |

|------|------|------|----------|----------|

| WRR (AGU) | ~8k+附录 | 150词 | AGU | Key Points(3), Plain Language Summary, Open Research |

| Nature Water | Persp:3-4k | 150词 | Nature编号 | Summary paragraph |

| 中国科学 | ~15k字 | 300字中+200词英 | GB/T 7714 | 中英文摘要, 基金声明 |

| J. Hydrology | ~8k词 | 300词 | Elsevier编号 | Highlights(3-5), Graphical Abstract |

| Adv. Water Res. | ~7k词 | 250词 | Elsevier编号 | — |

| Env. Model. \& Soft. | ~8k词 | 300词 | Elsevier APA | Software Availability |

| J. Hydroinformatics | ~7k词 | 250词 | IWA | — |

| JWRPM (ASCE) | ~8k词 | 200词 | ASCE | — |

| SoftwareX | ~3k词 | 100词 | Elsevier编号 | Metadata表, 代码仓库 |

| Control Eng. Prac. | ~7k词 | 200词 | Elsevier编号 | Notation表 |

| J. Irrig. Drain. | ~7k词 | 200词 | ASCE | — |



---



\## K. 质量红线



1\. \*\*虚构参考文献\*\*: 零容忍，用web搜索验证

2\. \*\*跨论文矛盾\*\*: 回溯修改已完成论文

3\. \*\*自引率>30%\*\*: 削减自引、补充第三方

4\. \*\*自引率<10%\*\*: 补充Lei代表作

5\. \*\*>300词跨论文重复\*\*: 改写其中一篇

6\. \*\*符号不一致\*\*: 以P1a为准

7\. \*\*P1三篇重复率>10%\*\*: 差异化改写

8\. \*\*南水北调中线\*\*: 不可作为成功案例(仍L2)，仅作背景



---



\## L. 迭代写作流程



每篇论文至少经历20轮"写作→评审→修改"循环：



\### 写作 (Author Mode)

角色: 雷晓辉教授。按目标期刊格式撰写，理论+技术+案例三者兼顾，合理自引(15-25%)，每轮聚焦改进1-3个方面。



\### 评审 (Reviewer Mode)

三位评审人轮流(每轮 iteration % 3 选择):



\*\*Reviewer A — 理论严谨型\*\*: 欧洲控制论教授，逐行查公式，质疑假设，检查与P1a定理的一致性。

\*\*Reviewer B — 工程实践型\*\*: 美国水利CTO，关心SCADA可行性，验证案例数据真实性。

\*\*Reviewer C — 学科交叉型\*\*: 亚洲AI+水利带头人，Nature编委，评价创新性与影响力。



评审7个维度: 创新性、数学严谨性、可重复性、案例验证、文献完备性、写作质量、体系区分度。

输出: 评分(1-10) + 判定(Accept/Minor/Major/Reject) + 主要问题≥5条 + 次要问题≥5条 + 参考文献审查。



\### 修改 (Revision Mode)

逐条回应评审意见。Critical级完全解决，Major级实质性回应，Minor级全部修正。参考文献问题用web搜索验证。



\### 退出条件

连续3轮获得Accept或Minor Revision，且总迭代≥20轮 → 标记完成。



\### 主循环伪代码

```python

for batch in \[B1, B2, B3, B4]:

&nbsp;   for paper in batch.papers:

&nbsp;       # 如有已有初稿，从papers/目录读取

&nbsp;       if paper.has\_existing\_draft:

&nbsp;           read\_existing\_draft\_from\_papers\_dir(paper)

&nbsp;       else:

&nbsp;           create\_initial\_draft(paper)

&nbsp;           save\_to\_papers\_dir(paper)

&nbsp;       

&nbsp;       verify\_references(paper)  # web搜索验证

&nbsp;       

&nbsp;       iteration = 0

&nbsp;       consecutive\_accepts = 0

&nbsp;       while iteration < 20 or consecutive\_accepts < 3:

&nbsp;           iteration += 1

&nbsp;           reviewer = \["A","B","C"]\[iteration % 3]

&nbsp;           review = conduct\_review(paper, reviewer)

&nbsp;           revise\_paper(paper, review)

&nbsp;           

&nbsp;           if review.verdict in \["Accept","Minor Revision"]:

&nbsp;               consecutive\_accepts += 1

&nbsp;           else:

&nbsp;               consecutive\_accepts = 0

&nbsp;           

&nbsp;           if iteration % 5 == 0:

&nbsp;               verify\_references(paper)

&nbsp;           

&nbsp;           update\_status(paper)

&nbsp;           save\_to\_papers\_dir(paper)

&nbsp;           

&nbsp;           if consecutive\_accepts >= 3 and iteration >= 20:

&nbsp;               mark\_complete(paper)

&nbsp;               break

&nbsp;       

&nbsp;       finalize\_paper(paper)

&nbsp;   

&nbsp;   cross\_paper\_consistency\_check(batch)

```



---



\## M. 文件管理



每篇论文在 `papers/` 目录下管理，文件命名规则:

\- `papers/P1a\_WRR/draft\_vXX.md` — 稿件版本

\- `papers/P1a\_WRR/review\_vXX.md` — 评审报告

\- `papers/P1a\_WRR/response\_vXX.md` — 修改说明

\- `papers/P1a\_WRR/references.bib` — 参考文献

\- `papers/P1a\_WRR/status.json` — 进度追踪



全局文件:

\- `progress.json` — 全局进度

\- `papers/shared/glossary.md` — 术语表

\- `papers/shared/symbols.md` — 符号表

\- `papers/shared/cross\_check.json` — 一致性记录



\### status.json 模板

```json

{

&nbsp; "paper\_id": "P1a",

&nbsp; "journal": "Water Resources Research",

&nbsp; "current\_version": 9,

&nbsp; "total\_iterations": 0,

&nbsp; "status": "existing\_draft",

&nbsp; "consecutive\_accepts": 0,

&nbsp; "completed": false,

&nbsp; "self\_cite\_rate": null,

&nbsp; "history": \[]

}

```



\### progress.json 模板

```json

{

&nbsp; "project": "CHS Paper System",

&nbsp; "total\_papers": 25,

&nbsp; "completed": 0,

&nbsp; "in\_progress": 4,

&nbsp; "not\_started": 17,

&nbsp; "published": 4,

&nbsp; "current\_batch": 1,

&nbsp; "current\_paper": "P1a",

&nbsp; "papers": {

&nbsp;   "P1a": {"status":"existing\_draft\_v9"},

&nbsp;   "P1b": {"status":"existing\_draft\_v1"},

&nbsp;   "P1c": {"status":"existing\_draft\_v2"},

&nbsp;   "P2A": {"status":"existing\_draft\_v2"},

&nbsp;   "P-DC": {"status":"not\_started"},

&nbsp;   "CKG-1": {"status":"not\_started"},

&nbsp;   "CKG-2": {"status":"not\_started"},

&nbsp;   "CKG-3": {"status":"not\_started"},

&nbsp;   "BAK-1": {"status":"not\_started"},

&nbsp;   "YBK-1": {"status":"not\_started"},

&nbsp;   "SC-1": {"status":"not\_started"},

&nbsp;   "SC-2": {"status":"not\_started"},

&nbsp;   "HZF-1": {"status":"not\_started"},

&nbsp;   "HZF-2": {"status":"not\_started"},

&nbsp;   "HZF-3": {"status":"not\_started"},

&nbsp;   "P2B": {"status":"not\_started"},

&nbsp;   "P2E": {"status":"not\_started"},

&nbsp;   "P2C": {"status":"not\_started"},

&nbsp;   "P2D": {"status":"not\_started"},

&nbsp;   "WHM-1": {"status":"not\_started"},

&nbsp;   "WHM-2": {"status":"not\_started"},

&nbsp;   "Lei2025a": {"status":"published"},

&nbsp;   "Lei2025b": {"status":"published"},

&nbsp;   "Lei2025c": {"status":"published"},

&nbsp;   "Lei2025d": {"status":"published"}

&nbsp; }

}

```



---



\## N. 断点续传



如果对话中断，发送：

```

读取 CLAUDE.md 和 progress.json，查看 papers/ 目录结构，找到上次中断位置，继续工作。

```



---



\## O. 公式渲染规范



论文草稿使用 Markdown 格式，公式采用 LaTeX 语法。



\### O.1 公式书写规则



\*\*行内公式\*\*: 用单 `$` 包裹，如 `$G(s) = \\frac{(1+\\tau\_m s) e^{-\\tau\_d s}}{A\_s \\cdot s}$`



\*\*独立公式\*\*: 用双 `$$` 包裹并单独成段，附编号：

```latex

$$

G(s) = \\frac{(1+\\tau\_m s) \\, e^{-\\tau\_d s}}{A\_s \\cdot s} \\tag{1}

$$

```



\*\*编号规则\*\*: 每篇论文从 (1) 独立编号。引用 `Eq. (1)` 或 `式(1)`（中文）。



\### O.2 核心公式速查表（以P1a为准，所有论文直接复用）



```latex

% --- Theorem 2: Unified Transfer Function Family ---

% Family α (integrating / non-self-regulating)

G(s) = \\frac{(1 + \\tau\_m s) \\, e^{-\\tau\_d s}}{A\_s \\cdot s}



% Family β (self-regulating)

H(s) = \\frac{1 - K X s}{1 + K(1-X) s}



% --- Corollary 1: Muskingum–IDZ Duality ---

H\_{\\text{Musk}}(s) = \\frac{1 - K X s}{1 + K(1-X) s}

\\approx G\_{\\text{IDZ}}(s) \\big|\_{\\text{1st order MacLaurin}}



% --- Lemma 2: Nash Cascade Limit ---

\\lim\_{n \\to \\infty,\\, nK \\to \\tau\_d} \\left(\\frac{1}{1+Ks}\\right)^n = e^{-\\tau\_d s}



% --- Lemma 3: Unified Actuator Characteristic ---

\\Delta Q = \\alpha \\, \\Delta u + \\beta\_{\\text{up}} \\, \\Delta H\_{\\text{up}} + \\beta\_{\\text{dn}} \\, \\Delta H\_{\\text{dn}}



% --- Saint-Venant Equations (linearized) ---

\\frac{\\partial A}{\\partial t} + \\frac{\\partial Q}{\\partial x} = q\_l



% --- Diffusion Wave Approximation ---

\\frac{\\partial Q}{\\partial t} + c \\frac{\\partial Q}{\\partial x} = D \\frac{\\partial^2 Q}{\\partial x^2}



% --- Pipe Compliance Integrator ---

G\_{\\text{pipe}}(s) = \\frac{1}{C\_h \\cdot s} \\quad \\text{where } C\_h = \\frac{\\rho g A L}{a^2}



% --- Six-Element System ---

\\Sigma = (P, A, S, D, C, O)



% --- MAS Formula ---

\\text{MAS} = \\text{HDC} + \\text{ODD} + \\text{Cognitive Intelligence}



% --- DMPC Cost Function ---

J\_i = \\sum\_{k=0}^{N\_p-1} \\left\[ \\| y\_i(k) - r\_i(k) \\|^2\_{Q\_i} + \\| \\Delta u\_i(k) \\|^2\_{R\_i} \\right]



% --- Five-Level Model Hierarchy ---

\\text{LSV} \\xrightarrow{\\text{spatial lumping}} \\text{IDZ}

\\xrightarrow{\\text{drop zero}} \\text{ID}

\\xrightarrow{\\text{drop delay}} \\text{I}

\\xrightarrow{\\text{steady state}} \\text{SS}

```



\### O.3 公式质检规则



1\. \*\*符号一致性\*\*: 所有论文同一物理量使用相同符号（参照 §I 符号表）

2\. \*\*下标规范\*\*: `\\text{}` 包裹英文下标（`\\tau\_{\\text{up}}` 而非 `\\tau\_{up}`）

3\. \*\*单位\*\*: 公式后首次出现时标注单位（如 "$A\_s$ \[m²]"）

4\. \*\*向量/矩阵\*\*: 向量 `\\mathbf{x}`，矩阵 `\\mathbf{A}`

5\. \*\*中文论文\*\*: 中国科学公式编号右对齐，用 `\\tag{}`



\### O.4 docx 输出公式处理



最终生成 `.docx` 时用 `pandoc` 转换：

```bash

pandoc draft.md -o manuscript.docx --mathjax

```

或用 Node.js docx 库时公式用 OMML 格式插入（参见P1a生成脚本 gen\_wrr\_v9.js 中的 Math 对象用法）。



---



\## P. 全部论文图片生成提示词



每篇论文每张图附中英文提示词。用AI工具生成初稿，再用 PowerPoint/Illustrator 精修。



\*\*统一配色方案\*\*:

\- 主色: #1565C0（深蓝，水/控制）

\- 辅色1: #4CAF50（绿，安全/ODD）

\- 辅色2: #7B1FA2（紫，认知智能）

\- 辅色3: #FF7043（橙红，扰动/警告）

\- 背景: 白色，辅助线 #E0E0E0



---



\### P.1 Paper P1a — WRR（5张图）



\#### WRR-Fig1: CHS六元受控系统架构



\*\*用途\*\*: §3，Σ = (P, A, S, D, C, O) 闭环控制架构



> Create a professional control systems block diagram: "CHS Six-Element Controlled System Architecture". Classic closed-loop feedback layout, horizontal flow. Six elements as colored rounded rectangles: \*\*P (Plant)\*\* \[blue, largest, center] with canal/pipe cross-section, labeled "Hydraulic process (Saint-Venant equations)"; \*\*A (Actuators)\*\* \[green, left] with gate/pump/valve icons; \*\*S (Sensors)\*\* \[orange, bottom] with level/flow gauges; \*\*D (Disturbances)\*\* \[red dashed, top arrow into P] labeled "Rainfall, evaporation, demand, failure"; \*\*C (Controller)\*\* \[dark blue, bottom-left] labeled "HDC/MAS"; \*\*O (Objectives)\*\* \[purple, input to C] labeled "Level tracking, flow matching, safety". Signal flow: O→C→A→P→S→C (feedback dashed), D→P (red dashed). Bottom-right formula: Σ = (P, A, S, D, C, O). Style: flat vector, white background, sans-serif, 180mm × 100mm, 300dpi.



\*\*图注\*\*: Figure 1. The CHS six-element controlled dynamical system architecture. All water systems share this feedback loop structure: Objective (O) provides reference signals; the Controller computes actions; the Actuator (A) implements them on the Plant (P); the Sensor (S) measures the response; Disturbance (D) enters externally; Constraint (C) imposes absolute operational boundaries reflecting operational singularity (Definition 1).



\#### WRR-Fig2: 统一模型层级（五级 + 双族传递函数）



\*\*用途\*\*: §4，Family α / Family β 双分支 + LSV→IDZ→ID→I→SS



> Create an academic figure: "Unified Model Hierarchy". Vertical layout, top-to-bottom fine→coarse. Top: Diffusion wave common ancestor (∂Q/∂t + c∂Q/∂x = D∂²Q/∂x²). Forks into two branches: \*\*Left: Family α (integrating)\*\* \[blue gradient] — LSV → IDZ: G(s)=(1+τₘs)e^(−τᵈs)/(Aₛ·s) → ID (drop zero) → I (drop delay) → SS. Labels: open channels, reservoirs, pipelines. \*\*Right: Family β (self-regulating)\*\* \[green gradient] — H(s)=(1−KXs)/(1+K(1−X)s) → Muskingum reservoir. Labels: river flood routing. At Level iv: bidirectional dashed arrow "Muskingum–IDZ Duality (Corollary 1)". Bottom: Actuator reduction (Lemma 3): ΔQ = αΔu + β\_up·ΔH\_up + β\_dn·ΔH\_dn, "algebraic BCs for all gates/pumps/valves/turbines". Arrows labeled with reduction operations. Academic vector, blue-green palette, white bg, 180mm × 160mm, 300dpi.



\*\*图注\*\*: Figure 2. The unified model hierarchy: five-level plant dynamics (Family α integrating and Family β self-regulating branches) with the actuator reduction (Lemma 3) providing algebraic boundary conditions. The Muskingum–IDZ duality (Corollary 1) bridges the two branches at Level 4.



\#### WRR-Fig3: 模型层级—控制层级对应



\*\*用途\*\*: §4.8 Theorem 3



> Create a dual-column academic figure: "Model–Layer Correspondence". \*\*Left: Model Hierarchy\*\* (top-down, fine→coarse) — five bands deep-blue to light-blue: Level i (LSV), ii (IDZ), iii (ID), iv (I), v (SS). Downward arrows: "Discard one timescale". \*\*Right: Control Hierarchy\*\* (bottom-up, fast→slow) — four bands: Layer 0 Safety (PLC, ms), Layer 1 Regulation (local MPC, s–min), Layer 2 Coordination (DMPC, min–h), Layer 3 Planning (nested opt, day–yr). Dashed arrows: i↔L0, ii↔L1, iii–iv↔L2, v↔L3. Right edge: timescale ruler ms→yr. Center: "Just Precise Enough". Symmetric, blue palette, white bg, 180mm × 120mm, 300dpi.



\*\*图注\*\*: Figure 3. Model–layer correspondence: each control layer uses the model level whose approximation errors are acceptable at that temporal scope (Theorem 3).



\#### WRR-Fig4: 八原理双四元组



\*\*用途\*\*: §5



> Create an academic figure: "Eight CHS Principles — Dual Tetrads with Tradeoffs". \*\*Left (blue): Operational Tetrad\*\* — P1 Feedback, P2 Decoupling, P3 Order Reduction, P4 Emergence. \*\*Right (orange): Resilience Tetrad\*\* — P5 Robustness, P6 Coordination, P7 Adaptation, P8 Hierarchy. \*\*Center: four tradeoff dashed arrows\*\* — P2↔P6 (local independence vs global consistency), P3↔P5 (simplification vs fidelity), P4↔P8 (bottom-up vs top-down), P1↔P7 (fixed model vs online learning). Symmetric, blue-orange palette, white bg, 180mm × 110mm, 300dpi.



\*\*图注\*\*: Figure 4. The eight CHS principles organized into dual tetrads with inter-principle tradeoffs. Dashed lines indicate the four fundamental tradeoffs (Section 5.3).



\#### WRR-Fig5: WSAL五级阶梯图



\*\*用途\*\*: §7.4



> Create an academic staircase figure: "Water Systems Autonomy Levels (WSAL)". Ascending steps L1→L5, gray-to-navy gradient. \*\*L1 Remote Monitoring\*\* \[gray]: manual, SCADA. \*\*L2 Assisted\*\* \[light blue]: human confirms, HDC recommends, ★"Current state-of-art". \*\*L3 Conditional Autonomy\*\* \[medium blue]: autonomous within verified ODD. \*\*L4 High Autonomy\*\* \[deep blue]: MAS handles most scenarios. \*\*L5 Full Autonomy\*\* \[navy]: self-expanding ODD. L2→L3: "CRITICAL TRANSITION — requires xIL verification". L3→L4: "HDC→MAS: adding Cognitive Intelligence". Bottom: ODD coverage expanding. Right: trust increasing. Grays-blues, white bg, 180mm × 100mm, 300dpi.



\*\*图注\*\*: Figure 5. Water Systems Autonomy Levels (WSAL): a five-level classification adapted from SAE J3016. The WSAL-2→3 transition is the critical near-term milestone requiring systematic xIL verification.



---



\### P.2 Paper P1b — Nature Water（3张图）



\#### NW-Fig1: 三阶段演进时间线



> Create a visually striking figure for Nature Water: "Three-phase evolution of water resources systems analysis". Horizontal timeline 1950s→present. \*\*Phase I (1950s–1980s)\*\* \[sand/beige]: "Water Balance \& Planning", question "WHAT to build?", dam icon, ΔS=Qin−Qout, Rippl 1883 / Harvard 1962, badge "Annual". \*\*Phase II (1990s–2010s)\*\* \[teal]: "Optimal Allocation \& IWRM", "HOW MUCH?", network graph, min f(x) s.t. Ax≤b, badge "Monthly–Annual". \*\*Phase III (2020s–)\*\* \[deep blue, larger]: "Dynamic Control \& Autonomy", "HOW to deliver in real time?", closed-loop circle, ∂A/∂t+∂Q/∂x=q, badge "Seconds–Years". Between II→III: "Paradigm Shift" callout with gear-shift icon. Modern Nature/Science aesthetic, white bg, 3-color, Helvetica, 180mm × 70mm, 300dpi.



\#### NW-Fig2: MAS三支柱架构



> Create a sophisticated architecture diagram for Nature Water: "MAS = HDC + ODD + Cognitive Intelligence". \*\*Top: Three Pillars\*\*: HDC—Physical AI \[blue] "Compute accurately" (Saint-Venant, MPC, L0-L3); ODD \[green] "Stay within safe boundaries" (boundary envelope, xIL, expanding dashed boundary); Cognitive Intelligence \[purple] "Think clearly" (brain icon, knowledge graph, LLM). \*\*Bottom: Dual-engine loop\*\* within agent: Cognitive proposes → Physical validates → conflict: revise → pass: execute. Core equation: MAS = HDC + ODD + Cognitive Intelligence. \*\*Right\*\*: Cloud/Area/Edge Agent hierarchy + L0 Safety Floor. Nature-quality, white bg, consistent colors, 180mm × 130mm, 300dpi.



\#### NW-Fig3: WSAL五级分类



> Same content as WRR-Fig5 but Nature-style: more visual, less text per level, one icon + one sentence per level. Key transitions (L2→L3, L3→L4) emphasized with large callouts. Modern gradients, 180mm × 90mm, 300dpi.



---



\### P.3 Paper P1c — 中国科学（3张图，中文标注）



\#### 中科-图1: WRSA三阶段演进



> 横向三栏布局，展示"水资源系统分析三阶段演进"。淡蓝渐变背景。Phase I（浅蓝）"水量平衡与规划设计（1950s—1980s）"，核心问题"建什么"，水坝截面+蓄水量曲线，关键词：线性规划/Rippl分析/哈佛项目，时间尺度：年，数学：ΔS = Qin − Qout。Phase II（中蓝）"优化配置与综合管理（1990s—2010s）"，"配多少"，网络拓扑+帕累托前沿，多目标优化/IWRM/二元水循环，月—年，min f(x) s.t. Ax≤b。Phase III（深蓝）"动态控制与自主运行（2020s—）"，"怎么调"，闭环控制框图+实时波形，水系统控制论/MPC/MAS/自主运行，秒—年，∂A/∂t + ∂Q/∂x = q。三栏间大箭头标注"范式转变"。扁平矢量，中文标注，180mm × 80mm，300dpi。



\#### 中科-图2: CHS六元受控系统（中文版）



> 与WRR-Fig1相同内容，全部标注改中文：P→"被控对象（水力过程）"，A→"执行器（闸/泵/阀）"，S→"传感器（水位/流量/水质）"，D→"扰动（降雨、蒸发、需水波动、设备故障）"，C→"控制器（HDC/MAS决策算法）"，O→"目标（水位跟踪、流量匹配、安全约束）"。公式保留：Σ = (P, A, S, D, C, O)。中文宋体/黑体，180mm × 100mm，300dpi。



\#### 中科-图3: 模型—控制层级对应（中文版）



> 与WRR-Fig3相同内容，全部标注改中文。左栏：线性化Saint-Venant方程 / IDZ传递函数 / 积分延迟模型 / 纯积分 / 稳态平衡。右栏：安全保护层（PLC，毫秒）/ 实时调节层（单回路MPC，秒—分钟）/ 协调优化层（DMPC，分钟—小时）/ 计划调度层（嵌套优化，日—年）。中间："刚好足够精细"。中文标注，180mm × 120mm，300dpi。



---



\### P.4 Paper P2A — JWRPM（5张图）



\#### P2A-Fig1: MAS三层Agent架构



> Hierarchical diagram: "MAS Three-Layer Agent Architecture". \*\*Cloud Agent\*\* \[dark blue, top]: network-wide, days–months, global state estimator + nested optimization. \*\*Area Agent\*\* \[medium blue, middle]: regional DMPC, min–hours, neighbor negotiation. \*\*Edge Agent\*\* \[light blue, bottom]: local MPC/PID, s–min, sensor fusion + actuator command. \*\*L0 Safety Floor\*\* \[gray, base]: PLC hardwired interlocks, ms, always-on veto. Communication arrows with cycle times. "Island autonomy" annotation: graceful degradation when comms fail. 180mm × 140mm, 300dpi.



\#### P2A-Fig2: ODD边界与xIL验证扩展



> Concentric boundary diagram: "ODD Expansion through xIL". \*\*Center (solid green)\*\*: Verified ODD — normal operation, routine disturbance. \*\*Middle (dashed yellow)\*\*: Candidate ODD — extreme inflow, equipment degradation. \*\*Outer (dotted red)\*\*: Unverified — unprecedented flood, cascading failure. \*\*Right\*\*: xIL pipeline MiL→SiL→HiL→PiL with checkmark gates, arrow expanding green boundary. "Each xIL campaign expands the verified boundary". 180mm × 100mm, 300dpi.



\#### P2A-Fig3: WSAL路线图（工程时间线版）



> 与WRR-Fig5相同阶梯布局，每级增加"所需技术条件"和"典型工程案例"。L2标注沙坪/胶东，L3标注目标2027-2030，L4标注2030+。底部时间线2020→2035+。180mm × 110mm，300dpi。



\#### P2A-Fig4: 沙坪 vs 胶东双案例对比



> Side-by-side: \*\*Shaping\*\* \[blue] cascade hydropower (3 reservoirs + turbines, seconds response, power tracking) vs \*\*Jiaodong\*\* \[green] pipeline (8 pump stations, 300km, min–hours, flow delivery + energy). Center comparison table: Family α vs β, timescale, disturbance, agent count, HDC layers. Both use same DMPC architecture → structural isomorphism. 180mm × 100mm, 300dpi.



\#### P2A-Fig5: 认知智能双引擎交互闭环



> Circular workflow: "Dual-Engine Interaction Loop". 1) Cognitive AI proposes \[purple]: scenario recognition → goal assembly → candidate plan. 2) Physical AI validates \[blue]: MPC constraint check → hydraulic feasibility. 3) Decision gate \[diamond]: conflict → revise; pass → 4) Execute \[green]: actuator command. Center: "Propose–Validate–Execute". "Physical AI has veto authority". 140mm × 140mm, 300dpi.



---



\### P.5 后续论文图片规格



| 论文 | 预计图数 | 必含图类型 |

|------|----------|-----------|

| CKG-1 | 4-5 | MBD七层流程图、双水箱平台示意、FMI耦合架构、xIL验证曲线 |

| CKG-2 | 4-5 | ODD形式化定义图、SiL架构、安全边界检测流程、闭环对比曲线 |

| CKG-3 | 4-5 | HiL测试台架示意、PLC通信架构、MAS自适应时序图、性能对比 |

| BAK-1 | 4-6 | OpenModelica组件库结构、单元组件图、组装示例、验证曲线 |

| YBK-1 | 3-4 | Simulink→C代码→PLC全流程、控制器快速原型架构、部署验证 |

| SC-1 | 4-5 | 水槽装置示意、Theorem 2验证曲线、DMPC响应、IDZ辨识 |

| SC-2 | 5-6 | FMI异构耦合架构、三工具集成框图、xIL全流程、性能对比 |

| HZF-1 | 4-5 | GPU并行架构、CUDA核心映射、并行方案图、加速比曲线 |

| HZF-2 | 4-5 | 分布式QP分解图、通信拓扑、实时性验证、收敛分析 |

| HZF-3 | 5-6 | 图拓扑生成流程、GPU引擎架构、数字孪生集成、框架结构 |

| P2B | 4-5 | 沙坪拓扑、SiL平台、ODD边界定义、MAS闭环曲线 |

| P2E | 4-5 | ODD扩展路径、WSAL-2→3方案、性能进化对比、安全验证 |

| P2C | 5-6 | 胶东拓扑、三层HDMPC架构、多时间尺度协调时序、泵站曲线 |

| P2D | 5-6 | 数字孪生架构、GPU+SCADA同化、能效结果、MiL+SiL对比 |

| WHM-1 | 4-5 | 密云系统图、三Agent架构、多目标帕累托前沿 |

| WHM-2 | 4-5 | MBD七层密云应用、数字孪生平台、实验→工程迁移对比 |

| P-DC | 3-4 | DfO设计哲学对比、MBD七层全景、课程体系结构 |



\*\*通用规则\*\*：

1\. 架构图使用统一配色方案

2\. 物理量符号与§I符号表完全一致

3\. 英文论文英文标注，中国科学中文标注

4\. 数据曲线用matplotlib/plotly生成（不用AI图像工具）

5\. 概念图用AI工具初稿 + 矢量编辑器精修

6\. 图片内容必须与论文中的caption完全对应



\### P.6 Claude Code图片生成工作流



```python

for fig in paper.figures:

&nbsp;   if fig.type in \["architecture", "concept", "schematic"]:

&nbsp;       # 概念图：生成AI图像提示词

&nbsp;       save(f"papers/{paper\_id}/fig\_prompts/fig{fig.num}\_prompt.md", prompt)

&nbsp;   elif fig.type == "data\_curve":

&nbsp;       # 数据曲线：生成matplotlib代码

&nbsp;       save(f"papers/{paper\_id}/fig\_code/fig{fig.num}\_plot.py", code)

&nbsp;   # 在draft中用占位符 \[Figure X about here]

```
