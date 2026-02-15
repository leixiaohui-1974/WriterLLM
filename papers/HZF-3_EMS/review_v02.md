# Reviewer Report (Iteration 1)

- **Paper ID**: HZF-3  
- **Reviewer**: B (工程实践型)  
- **Score**: 6.8 / 10  
- **Verdict**: Major Revision

## Major Issues

1. The manuscript reports multiple quantitative performance results in v01 without reproducibility details (hardware spec, dataset identifiers, run scripts, and statistical protocol).
2. Software Availability section includes a public repository URL that is not verified in this project workspace.
3. References list is explicitly marked placeholder and includes bibliographic items that are not yet fully verifiable.
4. Engineering deployment section lacks concrete failure-mode handling details (communication jitter, packet loss mitigation, fallback mode).
5. EMS software paper expectations require stronger reproducibility structure (artifacts, environment, deterministic replay procedure).

## Minor Issues

1. Abstract is too assertive for an initialization draft and should distinguish planned vs. validated findings.
2. Notation is mostly consistent with P1a but unit declarations should be made explicit at first appearance in method sections.
3. API section should include minimal interface contract and error handling behavior.
4. Benchmark section should define repeat count and confidence interval reporting.
5. Add an explicit limitations subsection for unsupported topologies and current scope.

## Recommendation

- Keep the paper in active revision.
- In next version, convert unsupported claims to planned evaluation language or provide full evidence package.
