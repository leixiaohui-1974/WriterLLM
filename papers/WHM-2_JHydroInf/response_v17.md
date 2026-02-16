# Response to Reviewer B (Round 16, WHM-2 v17)

We thank Reviewer B for the practical surge-operability recommendations. We addressed all requested points by adding Section 24 in `draft_v17.md`.

## Major Comment 1
Need a dedicated surge-window admissibility predicate.

### Response
Addressed in Section 24.1 via Eq. (28), introducing $\Pi_{\text{surge}}$ with alarm-window and command-rate constraints.

## Major Comment 2
AUTO persistence during surges is not explicitly throttled.

### Response
Addressed in Section 24.2 via Eq. (29), binding surge failure to `HOLD`/`DOWNGRADE` and command-frequency throttling.

## Major Comment 3
Load-shedding trigger criteria are not machine-checkable.

### Response
Addressed by formal threshold conditions in Eq. (28) and deterministic state transition in Eq. (29).

## Major Comment 4
Post-surge recovery path needs deterministic checklist and lineage-linked evidence.

### Response
Addressed in Section 24.3 by adding closure record requirements, lineage-linked replay packaging, and blocker-clearance checks before reasserting $\Pi_{\text{surge}}=1$.

## Major Comment 5
Need compact rule tying surge failure to HOLD/DOWNGRADE.

### Response
Provided directly in Eq. (29), which enforces authority-state throttling under surge inadmissibility.

## Minor Comments 1–5
Notation compactness, interval notation, handover linkage, authority label discipline, and concise journal style.

### Response
All handled in Section 24: A/B severity notation is retained, interval window $\Delta t$ is explicit, Eq. (23) linkage is referenced, no new authority labels are introduced, and text remains concise.

These revisions complete the requested minor changes and improve disturbance-surge robustness for WHM-2 control-room deployment governance.
