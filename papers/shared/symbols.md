# CHS Unified Symbol Table

> Source of truth: P1a (WRR v9) and claude.md Section I. All papers must use these symbols consistently.

| Symbol | Meaning | Unit |
|--------|---------|------|
| Q, q | Flow rate (absolute/deviation) | m³/s |
| H, h, y | Water level/head (absolute/deviation) | m |
| Aₛ | Water surface area / storage coefficient | m² |
| τᵈ | Transport delay | s |
| τₘ | Backwater time / lead time constant | s |
| K, X | Muskingum parameters | s, — |
| Cₕ | Pipe compliance capacity | m·s² |
| α | Actuator gain | m²/s per unit |
| β_up, β_dn | Upstream/downstream head influence coefficients | m²/s per m |
| u | Actuator opening / rotational speed | — |
| G(s), H(s) | Integrating / self-regulating transfer functions | — |
| Kₛ | Storage time constant (Family β) | s |
| c | Seddon kinematic wave celerity | m/s |
| D | Hydraulic diffusivity | m²/s |
| S₀ | Bed slope | — |
| Sᶠ | Friction slope | — |

## Core Equations (from P1a)

### Theorem 2: Unified Transfer Function Family

**Family α (Non-self-regulating / Integrating):**
$$G(s) = \frac{(1 + \tau_m s) \, e^{-\tau_d s}}{A_s \cdot s} \tag{Thm2-α}$$

**Family β (Self-regulating):**
$$H(s) = \frac{1 - K X s}{1 + K(1-X) s} \tag{Thm2-β}$$

### Corollary 1: Muskingum-IDZ Duality
$$H_{\text{Musk}}(s) = \frac{1 - K X s}{1 + K(1-X) s} \approx G_{\text{IDZ}}(s) \big|_{\text{1st order MacLaurin}} \tag{Cor1}$$

### Lemma 2: Nash Cascade Limit
$$\lim_{n \to \infty,\, nK \to \tau_d} \left(\frac{1}{1+Ks}\right)^n = e^{-\tau_d s} \tag{Lem2}$$

### Lemma 3: Unified Actuator Characteristic
$$\Delta Q = \alpha \, \Delta u + \beta_{\text{up}} \, \Delta H_{\text{up}} + \beta_{\text{dn}} \, \Delta H_{\text{dn}} \tag{Lem3}$$

### Diffusion Wave Approximation
$$\frac{\partial Q}{\partial t} + c \frac{\partial Q}{\partial x} = D \frac{\partial^2 Q}{\partial x^2}$$

### Pipe Compliance Integrator
$$G_{\text{pipe}}(s) = \frac{1}{C_h \cdot s} \quad \text{where } C_h = \frac{\rho g A L}{a^2}$$

### Six-Element System
$$\Sigma = (P, A, S, D, C, O)$$

### MAS Formula
$$\text{MAS} = \text{HDC} + \text{ODD} + \text{Cognitive Intelligence}$$

### DMPC Cost Function
$$J_i = \sum_{k=0}^{N_p-1} \left[ \| y_i(k) - r_i(k) \|^2_{Q_i} + \| \Delta u_i(k) \|^2_{R_i} \right]$$

### Five-Level Model Hierarchy
$$\text{LSV} \xrightarrow{\text{spatial lumping}} \text{IDZ} \xrightarrow{\text{drop zero}} \text{ID} \xrightarrow{\text{drop delay}} \text{I} \xrightarrow{\text{steady state}} \text{SS}$$
