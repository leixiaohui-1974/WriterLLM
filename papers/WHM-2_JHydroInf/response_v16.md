# Response to Reviewer A (Round 15, WHM-2 v16)

We thank Reviewer A for the final formal-consistency recommendations. We addressed all requested points by adding Section 23 in `draft_v16.md`.

## Major Comment 1
Predicate chain should be explicitly monotonic.

### Response
Addressed in Section 23.1 via Eq. (26), introducing explicit predicate-chain monotonicity from deployment to claim-package readiness.

## Major Comment 2
Need deterministic downstream invalidation when upstream fails.

### Response
Addressed in Section 23.2 via Eq. (27), defining automatic downstream invalidation for any upstream predicate failure.

## Major Comment 3
Token/evidence rebinding under lineage updates requires hard constraints.

### Response
Addressed in Section 23.3 by adding mandatory token rebinding, stale-token exclusion, and reassertion blocks until rebinding plus revalidation are complete.

## Major Comment 4
Partial-validity interpretation risk remains.

### Response
Resolved by coupling Eq. (26) and Eq. (27), which removes ambiguous partial-validity states from audit logic.

## Major Comment 5
Need concise final section linking monotonicity and rebinding.

### Response
Section 23 now provides this linkage with compact equations and a short implementation-oriented constraint list.

## Minor Comments 1–5
Symbol compactness, index ordering, linkage to existing constructs, terminology discipline, and concise style.

### Response
All handled in Section 23: symbols and ordering are explicit, rebinding references existing token/lineage constructs, no redundant predicate names were added, and prose remains concise.

These revisions complete the requested minor changes and close the remaining formal-consistency gap for WHM-2.
