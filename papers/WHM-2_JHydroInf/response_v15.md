# Response to Reviewer C (Round 14, WHM-2 v15)

We thank Reviewer C for the final transfer-governance recommendations. We addressed all requested points by adding Section 22 in `draft_v15.md`.

## Major Comment 1
Transferability statements may be read as performance-forward rather than boundary-forward.

### Response
Addressed in Section 22.1 by introducing Eq. (24), requiring boundary, blocker, and fallback disclosure as a prerequisite for reusable claim packages.

## Major Comment 2
Need one predicate enforcing package completeness for reusable claims.

### Response
Addressed via Eq. (24), the claim-package completeness predicate $\Pi_{\text{pkg}}$.

## Major Comment 3
Critical unresolved blockers should hard-lock transfer claims.

### Response
Addressed in Section 22.2 via Eq. (25), where transfer claims are admissible only when $\Pi_{\text{pkg}}=1$ and $N_{\text{blocker,critical}}=0$.

## Major Comment 4
Public summaries need an uncertainty floor.

### Response
Addressed in Section 22.3 by requiring ODD coverage, authority-state occupancy distribution, severity-stratified unresolved blockers, and rollback-SLO non-attainment incidence in all external summaries.

## Major Comment 5
Need explicit publication-lock semantics under unresolved critical blockers.

### Response
Added publication-lock wording in Section 22.2: unresolved critical blockers force cross-site transfer claims into “reference-only” status until re-audit.

## Minor Comments 1–5
Terminology consistency, occupancy representation, predicate linkage, blocker severity granularity, and concise journal style.

### Response
All addressed in Section 22: existing authority labels are preserved, occupancy is reported as a distribution, transfer admissibility is linked to $\Pi_{\text{ops}}$ via Eq. (24), blocker counts are severity-aware, and language remains concise.

These revisions complete the requested minor changes and further strengthen trust-preserving transfer governance for WHM-2.
