# Response to Reviewer B — Iteration 1 (v01 → v02)

Thank you for the operability-focused review. We implemented all major requests to make WHM-2 shift-executable while preserving governance-only scope.

## Point-by-point response

1. **ODD envelope and violation policy added**  
   Added Section 9.1 defining reservoir-state, telemetry, and authority envelopes with deterministic `DOWNGRADE` and requalification rules.

2. **Immutable artifact package added**  
   Added Section 9.2 with minimal shift package IDs (`model_bundle_id`, `controller_build_id`, `scenario_hash`, `replay_hash`, `alarm_trace_id`, `rollback_test_id`).

3. **SCADA shift checklist added**  
   Added Section 9.3 with signed control-room checklist and role-bound handover requirements.

4. **Non-compensability clarified**  
   Explicitly stated that missing safety/evidence artifacts invalidate release readiness regardless of optimization gains.

5. **Requalification conditions clarified**  
   Added policy that re-entry after violations requires refreshed xIL evidence under controlled build/version identifiers.

## Revision summary

- Draft advanced from **v01** to **v02**.
- Iteration verdict is **Major Revision**.
- Next iteration can proceed to Reviewer C for positioning and transferability refinement.
