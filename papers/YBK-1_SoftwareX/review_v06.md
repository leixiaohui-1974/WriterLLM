# Review — YBK-1 Iteration 5

**Reviewer**: C (Cross-Disciplinary Scholar)
**Draft reviewed**: v05
**Score**: 9.0 / 10
**Verdict**: Accept

---

## Summary

This SoftwareX manuscript describes HydroRTP, an open-source Simulink toolbox for automatic code generation of water network controllers targeting industrial PLCs. The paper has undergone four substantial revision rounds and now presents a mature, well-documented software contribution. The toolbox fills a genuine gap in the water systems automation pipeline—bridging MATLAB/Simulink controller design and IEC 61131-3 PLC deployment—with domain-specific blocks, vendor-specific code generation, and built-in verification.

## Strengths

1. **Complete software lifecycle coverage**: The four-layer architecture (block library → assembly → code generation → deployment/verification) covers the full design-to-deployment workflow. The one-click pipeline is a genuine productivity improvement over manual ST recoding.

2. **Thorough validation**: The 3-pool flume validation with both SiL and PiL results (Table 1, Table 2) provides convincing evidence of code generation fidelity (0.3 mm RMSE). The scalability analysis (Table 5) up to 100 pools gives practitioners clear guidance on applicability limits.

3. **Software quality rigor**: 87 unit tests, 91% statement coverage, MISRA-C:2012 compliance, and Polyspace static analysis demonstrate industrial-grade quality assurance rarely seen in academic water systems software.

4. **Extensibility and integration**: The neural/hybrid controller extensibility (§4.1), ODD Monitor block integration (§4.2), and positioning within the CHS tool chain demonstrate forward-looking design. The connection to CKG-2's ODD formalization is particularly valuable for safety-critical deployments.

5. **License and cost transparency**: The added license compatibility paragraph (§2.5) clearly delineates the open-source (MIT) toolbox from the commercial MATLAB dependencies, including cost estimates and simulation-only fallback. This is essential information for adoption decisions.

6. **Semantic versioning**: The explicit versioning policy (§4.3) following semver.org conventions signals professional software management and aids downstream dependency tracking.

## Minor Comments (Non-Blocking)

1. The Docker image for non-licensed users is mentioned but the specific image tag or registry URL is not provided. Consider adding this to the README or Zenodo deposit (not required for acceptance).

2. A brief mention of CI/CD (e.g., GitHub Actions running the 87 tests on push) would strengthen the sustainability narrative, though the current description of bi-annual releases and contribution guidelines is adequate.

## Decision

**Accept**. The manuscript is ready for publication. HydroRTP addresses a real and well-defined problem (design-to-deployment gap for water network MPC controllers), provides a clean software architecture with strong quality assurance, and demonstrates its value through rigorous validation. The revisions across four iterations have systematically addressed all reviewer concerns. The paper meets SoftwareX standards for software description, reproducibility, and impact documentation.
