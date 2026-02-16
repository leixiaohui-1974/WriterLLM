# Response to Reviewer A (Round 27, WHM-2 v28)

We thank Reviewer A for the final audit-replay governance recommendations. We addressed all requested points by adding Section 35 in `draft_v28.md`.

## Major Comment 1
Add a completed-state predicate for locked replay policy and replay pass status.

### Response
Addressed in Section 35.1 via Eq. (50), requiring replay-policy lock and replay-pass verification under completed state before compliance assertions.

## Major Comment 2
Replay failure should deterministically trigger reopen.

### Response
Addressed in Section 35.2 via Eq. (51), forcing `Completed:=0`, opening a reopen ticket, and invalidating audit-replay state.

## Major Comment 3
Define minimum frozen replay-audit manifest fields.

### Response
Addressed in Section 35.3 with explicit policy digest/timestamp, replay input bundle hash, replay result hash with verifier signature digest, and reopen linkage fields.

## Major Comment 4
Ensure replay-verifier linkage is machine-checkable.

### Response
Handled by mandatory replay verifier-signature digest and deterministic replay-result hash in Section 35.3.

## Major Comment 5
Keep closure concise and avoid runtime control expansion.

### Response
Section 35 is concise, archival-audit scoped, and does not modify accepted technical/control claims.

## Minor Comments 1–5
Terminology reuse, compact notation, concise style, no new technical claims, and CHS consistency.

### Response
All handled in Section 35: frozen/audited/reopen vocabulary is reused, notation remains compact and aligned with prior sections, style remains concise, no new technical claims are introduced, and CHS consistency is preserved.

These revisions finalize post-completion audit-replay governance for deterministic and reproducible compliance validation.
