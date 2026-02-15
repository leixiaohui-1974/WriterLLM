# Response to Reviewer B (Iteration 1)

We thank Reviewer B for the practical engineering review. We addressed all major and minor comments in `draft_v02.md` as follows.

## Major Comments

1. **Unverified quantitative claims**  
   - **Action**: Reframed abstract and results language from definitive claims to protocol-based targets and preliminary observations.  
   - **Location**: Abstract, Sections 4–5.

2. **Unverified repository URL**  
   - **Action**: Replaced with release policy statement: public repository URL will be finalized after internal release approval and artifact packaging.  
   - **Location**: Software Availability section.

3. **Placeholder references**  
   - **Action**: Marked references as *internal manuscript records* pending external bibliographic verification; removed implication of finalized bibliography.  
   - **Location**: `references.bib`, draft references note.

4. **Failure-mode handling**  
   - **Action**: Added engineering fallback subsection covering packet loss, clock drift, and degraded-mode control routing to safe layers.  
   - **Location**: Section 3.4.

5. **Reproducibility structure**  
   - **Action**: Added explicit reproducibility protocol items (environment pinning, deterministic seeds, artifact manifest, replay checksums).  
   - **Location**: Section 4.2.

## Minor Comments

1. **Over-assertive abstract** → softened and separated planned vs. validated claims.
2. **Units at first appearance** → added unit notes for key symbols in formulation section.
3. **API contract** → added request/response/error contract summary.
4. **Benchmark statistics** → specified repeat count and confidence interval reporting protocol.
5. **Limitations** → added dedicated limitations subsection.

## Outcome

All reviewer comments were incorporated in v02. We request re-evaluation.
