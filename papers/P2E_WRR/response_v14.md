# Response to Reviewer B — Iteration 13 (v13 → v14)

Thank you for the deployment-focused recommendations. We addressed all requested operational gaps.

## Point-by-point response

1. **Minimum live-observation period**  
   Added Section 16.1 introducing mandatory live-observation window $T_{\text{obs}}$ before any `PROMOTE` activation.

2. **Measurable rollback target**  
   Added Section 16.2 and Eq. (6): $t_{\text{rollback}} \le T_{\text{fb,max}}$.

3. **Shift-handover governance closure**  
   Added Section 16.3 requiring continuity package across handovers in multi-shift campaigns.

4. **Continuity evidence requirement**  
   Section 16.3 mandates state snapshot, alarm ownership, readiness timestamps, and dual-sign acknowledgement.

5. **Rollback-SLO to gate logic coupling**  
   Section 16.2 explicitly sets $g_{\text{fb}}=0$ when Eq. (6) is violated and requires requalification.

## Revision summary

- Draft advanced from **v13** to **v14**.
- Verdict remains **Minor Revision** with improved field executability.
- Prior CHS equations and invariants remain preserved.
