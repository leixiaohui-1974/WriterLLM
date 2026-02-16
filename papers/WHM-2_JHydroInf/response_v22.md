# Response to Reviewer A (Round 21, WHM-2 v22)

We thank Reviewer A for the post-completion archival integrity recommendations. We addressed all requested points by adding Section 29 in `draft_v22.md`.

## Major Comment 1
Need explicit freeze predicate after `Completed=1`.

### Response
Addressed in Section 29.1 via Eq. (38), introducing post-completion immutability semantics.

## Major Comment 2
Post-completion edits should auto-reopen workflow.

### Response
Addressed in Section 29.2 via Eq. (39), forcing `Completed:=0`, opening a reopen ticket, and revoking `\Pi_{\text{activate}}` on edits.

## Major Comment 3
Need standardized archival checksum manifest.

### Response
Addressed in Section 29.3 by defining minimum checksum fields for manuscript, evidence package, release-token manifest, and reopen linkage.

## Major Comment 4
Reopen path should be deterministic and machine-checkable.

### Response
Handled by Eq. (39) deterministic state transition and ticket requirement.

## Major Comment 5
Closure should be concise and preserve accepted technical claims.

### Response
Section 29 is concise, archival-only in scope, and does not alter accepted technical content.

## Minor Comments 1–5
Symbol reuse, implementation style, scope control, concise journal style, and terminology consistency.

### Response
All handled in Section 29: existing symbols are reused, scope is archival integrity only, language remains concise, and CHS terminology is preserved.

These revisions complete post-completion hardening while maintaining acceptance-state technical consistency.
