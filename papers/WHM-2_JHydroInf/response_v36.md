# Response to Reviewer C (Round 35, WHM-2 v36)

We thank Reviewer C for the final citation-integrity governance recommendations. We addressed all requested points by adding Section 43 in `draft_v36.md`.

## Major Comment 1
Add a completed-state predicate for citation-registry completeness and reference-evidence linkage.

### Response
Addressed in Section 43.1 via Eq. (66), requiring citation-registry completeness and reference-evidence linkage under completed state before dissemination assertions are maintained.

## Major Comment 2
Citation gaps should deterministically trigger reopen.

### Response
Addressed in Section 43.2 via Eq. (67), forcing `Completed:=0`, opening a reopen ticket, and invalidating citation-integrity governance state.

## Major Comment 3
Define minimum frozen citation manifest fields.

### Response
Addressed in Section 43.3 with explicit citation-registry digest/timestamp, citation-to-reference linkage matrix hash, signed citation-integrity verdict digest, and reopen linkage fields.

## Major Comment 4
Ensure citation-integrity verdict linkage is machine-checkable.

### Response
Handled by mandatory signed citation-integrity verdict digest linked to package identifiers in Section 43.3.

## Major Comment 5
Keep closure concise and avoid technical-scope expansion.

### Response
Section 43 is concise, archival-governance scoped, and does not modify accepted technical/control claims.

## Minor Comments 1–5
Terminology reuse, compact notation, concise style, no new hydraulic performance claims, and CHS consistency.

### Response
All handled in Section 43: frozen/audited/reopen vocabulary is reused, notation remains compact and aligned with prior sections, style remains concise, no new hydraulic performance claims are introduced, and CHS consistency is preserved.

These revisions finalize post-completion citation-integrity governance for deterministic and auditable dissemination traceability.
