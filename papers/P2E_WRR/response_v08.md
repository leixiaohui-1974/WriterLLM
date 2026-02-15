# Response to Reviewer B (Iteration 7)

Thank you for the implementation-focused review. We implemented a minor revision emphasizing shift-level operability.

## Major Comments

1. **Shift-level protocol added**  
   - **Action**: Added Section 10.1 with a five-step activation protocol and explicit cancellation rule.

2. **Communication stress envelope added**  
   - **Action**: Added Section 10.2 with latency/packet-loss/blackout conditions and rejection rule for unresolved alarm ambiguity.

3. **Campaign closure criteria added**  
   - **Action**: Added Section 10.3 defining operationally acceptable vs open campaign states.

4. **Implementation-oriented wording strengthened**  
   - **Action**: Kept rollback/safety monitor checks tied to active shift procedures.

5. **Bounded claims preserved**  
   - **Action**: Scope remains pilot-stage WSAL-2→3 transition governance.

## Minor Comments

1. Assisted-mode fallback wording kept consistent.
2. Immutable-key terminology retained.
3. No new physical symbols introduced.
4. Structure remains concise and auditable.
5. ODD boundary semantics preserved.

## Outcome

Minor-revision comments addressed; manuscript advanced from v07 to v08.
