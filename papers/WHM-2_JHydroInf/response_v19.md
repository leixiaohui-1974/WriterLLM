# Response to Reviewer A (Round 18, WHM-2 v19)

We thank Reviewer A for the final completion-language formalization suggestions. We addressed all requested points by adding Section 26 in `draft_v19.md`.

## Major Comment 1
Need a dedicated pre-completion predicate combining threshold and portfolio consistency.

### Response
Addressed in Section 26.1 via Eq. (32), defining $\Pi_{\text{precomp}}$ from iteration threshold, sustained accept/minor outcomes, and portfolio-consistency satisfaction.

## Major Comment 2
"Ready/final" wording remains ambiguous before threshold fulfillment.

### Response
Addressed in Section 26.2 via Eq. (33), which forbids completion-style labels when $\Pi_{\text{precomp}}=0$.

## Major Comment 3
Need compact evidence card for late-stage completion-precheck audits.

### Response
Addressed in Section 26.3 by adding a minimum pre-completion evidence card schema (counters, predicate frontier, blockers, explicit completion-false statement).

## Major Comment 4
Completion-false state should be explicit when threshold is unmet.

### Response
Addressed by the mandatory explicit statement in Section 26.3 and the language lock in Eq. (33).

## Major Comment 5
Need concise formal closure linking language policy to predicate truth.

### Response
Section 26 provides this linkage directly through Eqs. (32)–(33) and concise implementation bullets.

## Minor Comments 1–5
Notation compactness, terminology reuse, non-overlap with `\Pi_complete`, concise style, and machine-checkable phrasing.

### Response
All handled in Section 26: notation is compact, Section 20 terminology is reused, `\Pi_{\text{precomp}}` is explicitly scoped as pre-completion (not completion), and text remains concise and machine-checkable.

These revisions complete the requested minor changes and close residual ambiguity in late-stage completion communication.
