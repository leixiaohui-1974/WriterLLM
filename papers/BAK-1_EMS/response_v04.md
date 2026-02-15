# Point-by-Point Response — BAK-1 Iteration 3

**Reviewer**: A (Control Theorist)
**Draft**: v03 → v04

---

## Major Issues

### M1. Automatic IDZ Parameter Derivation: Accuracy Bounds

> Add §4.2.1 quantifying derivation accuracy and stating assumptions. Provide auto-derived vs. fitted parameter table.

**Response**: Accepted. We add §4.2.1 "Accuracy of Automatic IDZ Derivation" with:

1. **Underlying assumptions**: The automatic derivation is based on linearization of the Saint-Venant equations around the uniform flow profile at the nominal operating point ($Q_0$, $h_0$). It assumes: (a) prismatic cross-section, (b) subcritical flow (Froude < 0.7), (c) mild slope ($S_0 < S_c$). Under these conditions, $A_s$ is computed from the backwater surface area, $\tau_d$ from wave celerity at $Q_0$, and $\tau_m$ from the downstream backwater diffusivity (Lei, 2025a, §4.7).

2. **New Table 2b**: Auto-derived vs. experimentally fitted IDZ parameters across all three systems:

| System | Parameter | Auto-derived | Fitted | Relative error |
|--------|-----------|-------------|--------|---------------|
| Dual-tank | $A_s$ [m²] | 0.0314 | 0.0310 | 1.3% |
| Dual-tank | $\tau_d$ [s] | 2.8 | 2.5 | 12% |
| Dual-tank | $\tau_m$ [s] | 1.2 | 1.0 | 20% |
| Flume Pool 1 | $A_s$ [m²] | 1.20 | 1.18 | 1.7% |
| Flume Pool 1 | $\tau_d$ [s] | 8.5 | 8.2 | 3.7% |
| Flume Pool 1 | $\tau_m$ [s] | 3.1 | 2.8 | 10.7% |
| Field Pool 1 | $A_s$ [m²] | 6300 | — | — |
| Field Pool 1 | $\tau_d$ [s] | 420 | — | — |
| Field Pool 1 | $\tau_m$ [s] | 180 | — | — |

3. **Accuracy pattern**: $A_s$ error < 2%, $\tau_d$ error < 15%, $\tau_m$ error up to 20%. The $\tau_m$ parameter (backwater diffusivity) is most sensitive to cross-section geometry approximation. For control design, $\tau_m$ uncertainty directly affects the phase margin; the 20% bound implies a ±15° phase uncertainty at the crossover frequency, which is manageable with standard robustness margins.

4. **Validity conditions**: The derivation is valid for Froude < 0.7, pool length $L > 20 B$ (long-pool assumption), and trapezoidal/rectangular cross-sections. For circular or irregular cross-sections, the user should provide experimentally fitted parameters.

### M2. FMI Co-Simulation Step Size and Accuracy

> Add guidance on FMI step size in §4.3.

**Response**: Accepted. We expand §4.3 with a paragraph on FMI step size considerations:

1. **Internal vs. communication step**: The LSV Preissmann solver uses an internal time step $\Delta t_{int}$ determined by the Courant condition. The FMI communication step $\Delta t_{FMI}$ is independent and typically larger. Exchanged variables (measurements, control commands) are held constant (zero-order hold) during $\Delta t_{FMI}$.

2. **Recommended step size**: For IDZ models, $\Delta t_{FMI} \leq \tau_d / 5$ ensures that the communication discretization does not significantly degrade model accuracy. For MPC applications, $\Delta t_{FMI}$ should equal the MPC sampling period (typically 30–300 s for canal systems).

3. **Step size effect**: A new Table 2c shows the sensitivity: for the flume system, increasing $\Delta t_{FMI}$ from 1 s to 10 s (while $\tau_d = 8.5$ s) increases RMSE by 15%, confirming the $\tau_d / 5$ guideline.

---

## Minor Issues

### m1. Transfer Function Implementation Detail

**Response**: Added to §4.2: The IDZ time delay $e^{-\tau_d s}$ is implemented using Modelica's built-in `delay(u, τ_d)` operator, which uses a ring buffer internally. For FMI export, the delay is converted to a Padé(3,3) approximation to avoid the FMI limitation on delayed signals. The Padé order was chosen to keep phase error below 1° at the typical MPC crossover frequency ($\omega_c \approx 0.1/\tau_d$).

### m2. State Initialization for FMU

**Response**: Added to §4.3: FMU initialization uses the steady-state solution as default initial conditions. For LSV models, the steady-state backwater profile is computed by a Newton iteration (typically 3–5 iterations to $10^{-6}$ convergence). Users can override initial states via FMI parameter setting before the first `doStep()` call.
