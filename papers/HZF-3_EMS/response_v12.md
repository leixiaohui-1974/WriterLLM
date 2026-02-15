# Response to Reviewer A (Iteration 11)

Thank you for the theory-rigor check. We implemented the requested machine-audit clarifications in `draft_v12.md` while preserving technical core content.

## Major Comments

1. **Schema-lock note for consistency artifact**  
   - **Action**: Added Section 7.3 defining stable top-level and check-level fields of `cross_paper_consistency_hzf3.json`.  
   - **Location**: Section 7.3.

2. **Cross-file state alignment rule**  
   - **Action**: Added explicit alignment rule between `submission_readiness_gate.json.state` and `cross_paper_consistency_hzf3.json.state`.  
   - **Location**: Section 7.3.

3. **Equations/theorem references unchanged**  
   - **Action**: No modification to Sections 2–5 mathematical content.

4. **Pre-submission blocker unchanged**  
   - **Action**: `external_reference_verification` remains the single blocked gate in gate artifact semantics.

5. **API/SLA/deployability unchanged**  
   - **Action**: No edits in API/SLA/runbook sections.

## Minor Comments

1. Abstract unchanged.
2. Conclusion bounded-claim wording unchanged.
3. Section 7.2 table kept concise.
4. Reference policy wording unchanged.
5. Deterministic restart bundle wording preserved.

## Outcome

All comments were addressed with schema-level clarifications only. We request continuation in the scheduled iteration loop.
