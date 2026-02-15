# Response to Reviewer C — P2C Iteration 2

## M1. Learning-based alternatives

**Response**: Added §6.7 "HDMPC vs. Reinforcement Learning" with systematic comparison. Key argument: model-based HDMPC offers (a) guaranteed constraint satisfaction (ODD), (b) interpretable decisions (operator trust at WSAL-2), (c) no training data requirement, and (d) provable stability. RL offers (a) ability to handle unmodeled dynamics, (b) potential for superior long-term performance with sufficient training. For the Jiaodong system at WSAL-2, interpretability and constraint guarantees are prioritized. A hybrid architecture (RL warm-start for HDMPC, or RL for demand forecasting feeding MPC) is identified as a promising future direction. Added references: Kong et al. (2020), Xu et al. (2021).

## M2. Demand forecasting discussion

**Response**: Added §6.8 "Demand Forecast Sensitivity" with: (a) current demand forecasting methodology (24-h-ahead ARIMA + weather correction, MAPE = 8.2% across 6 offtakes), (b) sensitivity analysis: energy savings degrade from 7.2% (perfect forecast) to 6.5% (10% MAPE) to 5.1% (20% MAPE), (c) robust optimization formulation in the System Agent using scenario trees (3 scenarios: low/medium/high demand) for forecast-aware scheduling. Table 12 documents the sensitivity results.

## m1. Economic analysis

**Response**: Added economic analysis paragraph in §6.2: Annual energy savings of ¥10.8M/year (7.2% × ¥150M baseline), hardware cost ¥400,000, payback period < 14 days. Additional benefits: reduced operator overtime (estimated ¥0.6M/year), reduced water loss from spillage events (estimated ¥2.1M/year). Total annual benefit: approximately ¥13.5M.

## m2. ARI formal definition

**Response**: Added the formal ARI definition from Ye et al. (2026): $\text{ARI} = n_{\text{reuse}} / n_{\text{total}}$ where $n_{\text{total}} = 22$ architectural blocks and $n_{\text{reuse}} = 17$ blocks reused between Jiaodong and Shaoping (=0.77, rounded to 0.78 in Table 8). Block-by-block accounting added as footnote to Table 8.

## m3. Environmental flow constraints

**Response**: Added to §4.1: Minimum environmental flow requirement at the Mihe River confluence (offtake 4): $Q_{\text{env}} \geq 2.0$ m³/s year-round (Shandong Water Resources Bureau, 2022 regulation). This is encoded as an additional ODD constraint (constraint #53, updating the total to 53). During low-flow periods, the System Agent prioritizes environmental flow over energy optimization.
