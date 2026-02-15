# Reviewer Report (Iteration 3)

- **Paper ID**: HZF-3  
- **Reviewer**: A (理论严谨型)  
- **Score**: 8.2 / 10  
- **Verdict**: Minor Revision

## 7-Dimension Scoring

1. Innovation: 8.1  
2. Mathematical rigor: 8.0  
3. Reproducibility: 8.1  
4. Case validation design: 8.0  
5. Literature completeness: 7.8  
6. Writing quality: 8.3  
7. System differentiation: 8.4

## Major Issues

1. The paper should explicitly state that HZF-3 does not alter Theorem-2 model family definitions and only provides software realization.
2. The mapping from model abstraction level (LSV/IDZ/ID/I/SS) to runtime usage should be made explicit to avoid ambiguity in control-layer deployment.
3. Add a formal consistency check list ensuring all runtime symbols preserve P1a definitions ($A_s, \tau_d, \tau_m, \alpha, \beta_{\text{up}}, \beta_{\text{dn}}$).
4. Clarify boundary-condition update order to avoid interpretation differences between synchronous and asynchronous runtime modes.
5. Add an explicit “scope of claims” paragraph in Discussion to prevent over-extension beyond current validation stage.

## Minor Issues

1. Add equation references (Eq. (1)-(3)) when first used in architecture discussion.
2. Include one compact table mapping CHS elements (P/A/S/D/C/O) to software modules.
3. Standardize wording around “deterministic” vs “replay-consistent”.
4. Add one sentence clarifying that looped topology support remains experimental.
5. Slightly shorten abstract closing sentence for EMS readability.

## Reference Audit

- Mandatory anchor references are acceptable for this iteration.
- Recommend adding at least 2 external verified digital-twin software references in next cycle.

## Recommendation

- Accept after minor revision focused on formal consistency and scope boundaries.
