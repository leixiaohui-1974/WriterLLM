# Response to Review — Paper P1c Iteration 3

**Reviewer**: A (Control Theorist)
**Review Score**: 8/10 — Minor Revision

---

## Major Issues

### M1. "Proof" Qualification
**Response**: Fully accepted. The reviewer correctly identifies that the unification result requires explicit statement of assumptions. We will:
- Replace "证明了" with "在线性化和主模态截断假设下, 证明了" in both the abstract and §3.3
- Add caveat: "非线性工况(如闸门大幅调节引起的水力跳跃)和高频动态(如水锤波)不在上述统一框架的适用范围内, 需要非线性控制理论或全阶数值模型处理"
- This is consistent with Litrico & Fromion [13] who explicitly state their linearization domain

### M2. DMPC Convergence Caveats
**Response**: Accepted. We will add in §4.2:
"需要指出, DMPC的全局近似最优性依赖于子问题耦合结构的特定条件(如凸性和弱耦合)[30]. 在强耦合工况(如多泵站同时启停)下, 迭代协商可能需要更多通信轮次, 其收敛性和最优性间隙有待进一步理论分析."

### M3. Multi-Timescale Optimality Transfer
**Response**: Accepted. This is an intellectually honest observation — the paper should acknowledge this gap explicitly rather than claiming "unified" without qualification. We will add in §4.2:
"需要指出, 上述多时间尺度分层框架目前仍是工程启发式设计, 各层之间的最优性传递条件和层间迭代收敛性尚缺乏严格的理论保证——这正是水系统控制论待完善的重要理论问题(详见§6.1). 工程实践中, 该框架的有效性通过MIL回溯验证确认(§5.2), 但理论上严格的最优性和收敛性分析仍是开放课题."

### M4. Dual Principles Resolution Conditions
**Response**: Accepted. We will add specific resolution conditions:
- After P1-P2: "当水网拓扑满足特定稀疏结构条件时(如串联渠池系统), 基于IDZ模型的解耦前馈补偿可在不损失反馈性能的前提下实现解耦[13,26]"
- After P5-P6: "在子问题满足凸性和有界不确定性条件下, 鲁棒分布式MPC可在保证约束鲁棒性的同时实现近似最优协调[30]"
- After P7-P8: "当层间通信延迟有界且各层采样周期满足时间尺度分离条件时, 分层控制可同时保持全局最优性和局部自治响应速度"

---

## Minor Issues

### m1. Family β Physical Intuition
**Response**: Will add: "物理上, 这一'反向响应'源于: 下游闸门调节首先改变局部泄流, 引起水位初始下降(或上升), 随后上游传来的波动才使水位朝最终稳态方向运动"

### m2. IDZ Abbreviation
**Response**: Will expand first occurrence to "IDZ(积分—延迟—零点, Integrator-Delay-Zero)"

### m3. Layer 0 SIL Level
**Response**: Will add "L0层安全联锁应达到IEC 61508功能安全标准SIL 2或SIL 3等级"

### m4. Equation Numbering
**Response**: Will add equation numbers to Family α and Family β formulas per 中国科学 format

### m5. Dual-Principle Compression
**Response**: Will compress the feedback-decoupling exposition by approximately 30%, since this is the most classical pair and needs less pedagogical support.
