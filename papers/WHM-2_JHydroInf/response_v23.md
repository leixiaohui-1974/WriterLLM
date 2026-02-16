# Response to Reviewer B (Round 22, WHM-2 v23)

We thank Reviewer B for the post-completion citation-provenance recommendations. We addressed all requested points by adding Section 30 in `draft_v23.md`.

## Major Comment 1
Need explicit frozen-reference provenance predicate.

### Response
Addressed in Section 30.1 via Eq. (40), introducing immutable reference-manifest and citation-provenance trace requirements.

## Major Comment 2
Citation mutation should deterministically trigger reopen.

### Response
Addressed in Section 30.2 via Eq. (41), forcing `Completed:=0`, opening a reopen ticket, and invalidating provenance predicate state.

## Major Comment 3
Need minimum archival reference manifest fields.

### Response
Addressed in Section 30.3 with explicit checksum, linkage-map, provenance-registry, and reopen-linkage fields.

## Major Comment 4
Citation-to-claim linkage must be machine-checkable.

### Response
Handled by the mandatory citation-to-claim linkage map hash in Section 30.3.

## Major Comment 5
Closure should stay concise and preserve accepted scope.

### Response
Section 30 is concise, archival-only, and does not alter accepted technical claims.

## Minor Comments 1–5
Reopen semantics reuse, compact notation, no runtime expansion, concise style, and CHS consistency.

### Response
All handled in Section 30: reopen logic reuses existing semantics, notation remains compact, runtime scope is unchanged, style is concise, and terminology remains CHS-consistent.

These revisions complete citation-provenance hardening for post-completion governance.
