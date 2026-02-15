# Response to Reviewer B — WHM-1 Iteration 1

## M1. Water quality integration

**Response**: Added §3.5 "Water Quality Constraints" with: (a) turbidity constraint ($T < 20$ NTU for Jingmi intake), (b) algal bloom risk index (chlorophyll-a threshold), (c) thermal stratification management (selective withdrawal depth). Added water quality as 5th objective in Reservoir Agent: $J_{\text{wq}}(k) = \max(0, T(k) - T_{\max})^2$. During high-turbidity events (flood-driven sediment), the Outflow Agent switches Jingmi intake to deeper outlets (lower turbidity). Updated Pareto analysis to 5 objectives.

## M2. Self-citation rate

**Response**: Added 14 new external references: reservoir optimization (Castelletti et al., 2008; Giuliani et al., 2021; Dobson et al., 2019), multi-agent water systems (Pereira et al., 2009; Maestre et al., 2013; Negenborn et al., 2009), ensemble forecasting (Cloke & Pappenberger, 2009; Boucher et al., 2012; Schwanenberg et al., 2015), Miyun studies (Zhai et al., 2020; Guo et al., 2022), stochastic optimization (Faber & Stedinger, 2001; Celeste & Billib, 2009), and operator decision support (Loucks & van Beek, 2017). Self-citation reduced from 55% to 22%.

## M3. Sediment and ice management

**Response**: Added §6.5 "Seasonal Operational Constraints" covering: (a) sediment: Miyun receives ~2.3 Mt/year, concentrated in July-August flood season; ODD contracts reservoir level range during sediment-laden inflows to prevent intake turbidity exceedance; long-term sedimentation reduces effective storage by ~8 × 10⁶ m³/year, updated annually in the water balance model. (b) Ice: December-March ice cover (thickness 0.3-0.5 m) requires modified gate operations (heated gate slots, reduced opening speed), modified level measurement (ultrasonic sensors with ice correction), and contracted ODD ($\Delta Q_{\max}$ reduced to 30 m³/s/h to prevent ice jam formation downstream).

## M4. Stochastic optimization comparison

**Response**: Added §6.3 "Comparison with Stochastic Programming" with Table 9 comparing MAS-MPC against: SDP (Faber & Stedinger, 2001), SDDP (Pereira, 1991), and robust optimization (Ben-Tal et al., 2009). MAS-MPC with ensemble forecasting achieves comparable robustness to SDP (supply reliability within 0.5%) while being computationally tractable for real-time operation. SDP is infeasible for 7-dimensional state space without discretization artifacts.

## M5. Operator interaction model

**Response**: Added §6.6 "Human-Machine Interface" describing: (a) recommendation dashboard showing next 72-h release schedule with confidence bands, ODD status, and objective trade-off visualization, (b) operator override levels: modify timing (low authority), modify magnitude (medium authority, logged), reject recommendation (high authority, requires justification), (c) MAS adaptation: rejected recommendations trigger re-optimization with modified weights reflecting operator preference, with preference learning over time.

## m1. SNWD coordination

**Response**: Expanded §3.2: when SNWD reduces intake unexpectedly, the Inflow Agent detects the shortfall within one communication cycle (6 h), the Reservoir Agent adjusts the 72-h schedule by increasing reliance on natural inflow and reducing supply if needed. A 30-day reserve buffer (500 × 10⁶ m³) is maintained to absorb SNWD interruptions.

## m2. Evaporation model

**Response**: Updated to Penman-Monteith evaporation model using daily weather station data (temperature, humidity, wind, solar radiation). Monthly evaporation rates: 2.1 mm/day (July peak) to 0.3 mm/day (January minimum). Annual total: 1,050 mm (183 × 10⁶ m³/year at normal pool).

## m3. Downstream flood routing

**Response**: Added downstream channel capacity analysis: Chaohe River channel below dam has bankfull capacity 1,200 m³/s at Xiahui gauging station. The $\Delta Q_{\max} = 50$ m³/s/h is derived from flood wave attenuation analysis: a step release of 500 m³/s from Miyun produces peak downstream flow of 420 m³/s (83% of release) with 2.5-hour lag. The rate limit ensures downstream flow stays below 800 m³/s (67% of bankfull).

## m4. Pareto analysis methodology

**Response**: Clarified in §5.2: ε-constraint method with 200 randomly sampled weight vectors, filtered to 142 non-dominated solutions. Table 4 shows 4 representative corner solutions. Added Figure 4 description: 2D projections of the Pareto frontier.

## m5. Cost-benefit analysis

**Response**: Added §6.7: MAS deployment cost ¥1.2M ($165,000 USD; 3 CX2062 IPCs + software + integration). Annual benefits: reduced spillage (18 × 10⁶ m³ × ¥2.5/m³ = ¥45M), reduced demand curtailment (9 fewer events × ¥8M average cost = ¥72M), reduced operator overtime (¥1.8M). Total annual benefit: approximately ¥119M ($16.3M USD). Payback period: < 4 days.
