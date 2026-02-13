# Review Report — Paper P1c (中国科学 v4)

**Iteration**: 3 of 20+
**Reviewer**: A (Control Theorist) — European control theory professor
**Date**: 2026-02-13

---

## Overall Assessment

This is my first review of this comprehensive Chinese-language paper. The paper attempts a broad synthesis: from WRSA disciplinary history through CHS theory to engineering practice and roadmap. Two rounds of prior revision have addressed practitioner and cross-disciplinary concerns (cybersecurity, LLM safety, terminology, international positioning).

From a control-theoretic perspective, the paper's core mathematical content — the unified transfer function families (§3.3), the five-level model hierarchy, the actuator reduction theorem (§3.5) — is sound and elegantly presented. The IDZ/Muskingum unification is a genuine contribution. The eight principles (§3.4) are now grounded in classical control theory (feedback-decoupling, H∞, Ramadge & Wonham), which significantly strengthens their theoretical standing.

However, I have concerns about mathematical precision in several areas. The "proof" claims in §3.3 need qualification — linearization around an operating point and mode truncation are approximations, not exact results. The DMPC convergence in the distributed setting (§4.2) is stated without caveats about convergence guarantees. The multi-timescale hierarchy (§4.2 and §5.2) claims a "unified framework" but lacks formal analysis of optimality transfer between layers. And the dual principles (§3.4), while now anchored in classical references, need explicit qualification of when the dual tensions can and cannot be formally resolved.

**Score: 8/10**
**Verdict: Minor Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 8 | Unified transfer function families and WSAL are genuine contributions |
| Mathematical Rigor | 7 | Transfer functions correct but "proof" overclaimed; DMPC convergence unstated |
| Reproducibility | 7 | MIL results provided; formulas well-specified |
| Case Validation | 7.5 | Both cases now have quantitative metrics; honestly positioned as preliminary |
| Literature Completeness | 8 | 59 references; international schools acknowledged; good cross-disciplinary coverage |
| Writing Quality | 8.5 | Excellent scholarly Chinese; well-structured |
| System Differentiation | 8 | Smart water/digital twin differentiation now clear and well-framed |

---

## Major Issues

### M1. "Proof" Qualification for Unified Transfer Function Families

§3.3 states that CHS "证明了天然河流、人工渠道和压力管道等各类一维水系统的低阶控制模型可统一为含参传递函数族的特殊实例." The word "证明" (prove) is too strong for what is actually shown. The transfer function families G(s) and H(s) are derived under:
- **Linearization** around a steady-state operating point (the Saint-Venant equations are nonlinear)
- **Mode truncation** (retaining only the dominant mode of the infinite-dimensional PDE system)
- **Quasi-steady-state assumption** for actuator dynamics (§3.5)

Each of these is a well-established approximation, but they are approximations nonetheless. The paper should state: "在线性化、主模态截断和执行器准稳态假设下, 证明了..." — qualifying the result's assumptions transparently. This is standard practice in control theory publications (cf. Litrico & Fromion [13] who explicitly state their linearization domain).

**Recommendation**: Replace "证明了" with "在线性化和主模态截断假设下, 本文证明了" in both the abstract and §3.3. Add a brief caveat: "非线性工况(如闸门大幅调节引起的水力跳跃)和高频动态(如水锤波)不在上述统一框架的适用范围内, 需要非线性控制理论或全阶数值模型处理."

### M2. DMPC Convergence and Optimality Caveats

§4.2 states that in distributed MPC, "各子控制器仅需与相邻子系统交换边界信息, 通过迭代协商达到全局近似最优." This claim requires caveats:
- DMPC convergence to global optimality is guaranteed only under specific conditions (convexity, coupling structure, communication topology). Christofides et al. [30] provide conditions but also document cases of non-convergence.
- The "近似最优" qualification is correct but should be quantified or at least characterized: how far from global optimal? Under what conditions does the gap increase?
- In the context of water systems with nonlinear actuator constraints and state-dependent delays, DMPC convergence is not trivially guaranteed.

**Recommendation**: Add a caveat: "需要指出, DMPC的全局近似最优性依赖于子问题耦合结构的特定条件(如凸性和弱耦合)[30]. 在强耦合工况(如多泵站同时启停)下, 迭代协商可能需要更多通信轮次或采用松弛策略, 其收敛性和最优性间隙有待进一步理论分析."

### M3. Multi-Timescale Hierarchy — Optimality Transfer

§4.2 and §5.2 describe a "年→月→旬→日→时→分" multi-timescale planning-control hierarchy. This is an ambitious and valuable framework, but the paper claims it achieves "水资源配置(长期)与实时运行控制(短期)在统一框架内实现衔接" without formal analysis of:
- **Optimality transfer**: When the upper layer passes down target values, does the lower layer's local optimum imply anything about the global multi-timescale optimum?
- **Consistency**: When actual operation deviates from the upper layer's plan (e.g., actual inflow < predicted), what guarantees that the lower layer's corrections don't violate the upper layer's constraints?
- **Convergence of the iterative refinement**: The "上级约束下级、下级反馈上级" mechanism is described but its convergence properties are not analyzed.

These are precisely the open questions acknowledged in §6.1 ("多时间尺度理论的形式化"). However, the main text in §4.2 and §5.2 should not claim "统一" without acknowledging these gaps.

**Recommendation**: In §4.2, add: "需要指出, 上述多时间尺度分层框架目前仍是工程启发式设计, 各层之间的最优性传递条件和层间迭代收敛性尚缺乏严格的理论保证, 这是水系统控制论待完善的重要理论问题(§6.1)." This transforms an unstated assumption into a transparent research agenda item.

### M4. Dual Principles — Resolution Conditions

§3.4 now includes connections to classical control theory (feedback-decoupling, H∞, Ramadge & Wonham), which is a significant improvement. However, the presentation implies these tensions are inherent and irresolvable ("不存在'万能解'"). While this is true in general, classical control theory provides specific conditions under which certain tensions can be formally resolved:
- The feedback-decoupling tension (P1-P2) can be partially resolved through structured decentralized control (Siljak, 1991) when the plant has a specific sparsity pattern.
- The robustness-coordination tension (P5-P6) has formal resolution conditions in the robust distributed MPC literature (convergence under bounded uncertainty).

Adding these resolution conditions, even briefly, would elevate the dual principles from philosophical observations to actionable design criteria.

**Recommendation**: Add a brief sentence after each tension pair indicating when formal resolution is possible. For example, after the P1-P2 discussion: "当水网拓扑满足特定稀疏结构条件时(如串联渠池系统), 解耦控制可在不损失反馈性能的前提下实现, 这一结论在IDZ控制框架[13,26]中已得到验证."

---

## Minor Issues

### m1. Family β Non-Minimum Phase — Physical Significance
§3.3 mentions the non-minimum phase characteristic (−τₘ′s term) of Family β and calls it "反向响应." This is physically important but could use one sentence of intuition: why does the water level initially move in the opposite direction? (Answer: downstream gate change first draws down the local pool before the upstream wave arrives.)

### m2. "IDZ" Abbreviation Expansion
The abbreviation "IDZ" (Integrator-Delay-Zero) is used frequently but only expanded once in §3.3 at its first mention in the model hierarchy discussion. Consider expanding it at its first appearance: "IDZ(积分—延迟—零点, Integrator-Delay-Zero)" for accessibility.

### m3. Layer 0 PLC Specification
§4.4 states L0 uses "PLC硬连锁" but does not specify the safety integrity level (SIL). For safety-critical water infrastructure, should L0 meet SIL 2 or SIL 3 per IEC 61508? A brief mention would strengthen the safety argument.

### m4. Equation Numbering
The transfer function formulas in §3.3 (Family α and Family β) should have equation numbers for cross-referencing. 中国科学 requires numbered equations.

### m5. Dual-Principle Section — Compression Opportunity
The four dual-principle tension discussions (§3.4) are individually well-written but collectively occupy substantial space. Consider whether the feedback-decoupling pair — being the most classical and widely understood — needs as much exposition as the less-standard pairings (e.g., hierarchy-autonomy).

---

## Summary

This paper presents a well-structured disciplinary review with genuine theoretical contributions. The unified transfer function families and the WSAL classification provide the field with concrete tools. The main areas for improvement are mathematical precision: qualifying the "proof" claims, acknowledging DMPC convergence caveats, and being transparent about the multi-timescale optimality gap. These are achievable within a minor revision and would bring the paper to the level of rigor expected for a 中国科学 theoretical review.
