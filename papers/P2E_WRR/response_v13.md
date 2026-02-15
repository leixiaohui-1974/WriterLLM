# Response to Reviewer A — Iteration 12 (v12 → v13)

Thank you for the precise rigor-focused review. All requested formal clarifications were incorporated.

## Point-by-point response

1. **Freshness semantics added**  
   Added Section 15.1 and Eq. (4), defining gate-validity freshness indicator $F_i$ using build-ID consistency and bounded time window.

2. **Predicate coupling completed**  
   Added Section 15.2 and Eq. (5), introducing effective gates $\tilde g_i$ and freshness-aware promotion predicate $\tilde\Pi$.

3. **Invalidation triggers specified**  
   Added Section 15.3 listing controller/model/safety-threshold/sensor-map drift triggers that force requalification.

4. **Invariant consistency preserved**  
   Section 15.2 explicitly states decision outcomes remain governed by I1–I3 when $\tilde\Pi \ne 1$.

5. **Requalification clarified**  
   Section 15.3 enforces monotonic invalidation and mandatory rerun of affected gates after drift.

## Revision summary

- Draft advanced from **v12** to **v13**.
- Verdict remains **Minor Revision** with stronger formal auditability.
- Core CHS model assumptions and prior equations remain unchanged.
