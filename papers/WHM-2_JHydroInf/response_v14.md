# Response to Reviewer B (Round 13, WHM-2 v14)

We thank Reviewer B for the final operability-focused recommendations. We addressed all requested points by adding Section 21 in `draft_v14.md`.

## Major Comment 1
Pre-submission readiness lacks explicit duty-role coverage and escalation reachability.

### Response
Addressed in Section 21.1 via Eq. (22), introducing staffing-aware operability predicate $\Pi_{\text{ops}} = \Pi_{\text{audit}} \land \text{RoleCoverage} \land \text{EscalationReachable}$.

## Major Comment 2
Handover logic needs a machine-checkable consistency rule.

### Response
Addressed in Section 21.2 via Eq. (23), defining `HandoverPass` with explicit subset mapping from outgoing risk flags to incoming mitigations and tokenized acknowledgment.

## Major Comment 3
Need fatigue safeguard for prolonged high-load periods.

### Response
Addressed in Section 21.3 by adding fatigue-window downgrade constraints tied to `HOLD`, mandatory relief handover, and alarm/rollback rechecks.

## Major Comment 4
Audit status appears detached from staffing feasibility.

### Response
Resolved by making $\Pi_{\text{ops}}$ a strict extension of $\Pi_{\text{audit}}$, so audit pass alone is no longer sufficient without staffing and escalation feasibility.

## Major Comment 5
AUTO persistence across shifts should be non-bypassable.

### Response
Addressed in Eq. (23): AUTO continuation across shift boundaries requires `HandoverPass=1`; otherwise bounded autonomy continuity is blocked.

## Minor Comments 1–5
Role set clarity, signoff semantics, Eq. (16) linkage, terminology consistency, and invalidation under fatigue violations.

### Response
All handled in Section 21 text: required duty roles are named, `TokenAck` is defined as tokenized shift acknowledgment, Eq. (22) explicitly extends Eq. (16), terms remain `HOLD`/`DOWNGRADE`, and unresolved fatigue-window violations are defined to invalidate $\Pi_{\text{ops}}$.

These revisions complete the requested minor changes and further anchor manuscript readiness in realistic control-room operation constraints.
