# Review Report — Paper P-DC (EMS v1)

**Iteration**: 1 of 20+
**Reviewer**: B (Engineering Practitioner) — US water systems CTO
**Date**: 2026-02-13

---

## Overall Assessment

This paper proposes Design for Operation (DfO) as a paradigm shift for water engineering, formalizes a seven-layer Model-Based Definition (MBD) framework, and presents a CHS graduate curriculum. The topic is timely and relevant to Environmental Modelling & Software: the gap between design-phase and operation-phase thinking in water engineering is real and well-articulated. The three contributions are clearly delineated.

However, the paper has significant weaknesses in its current form. The DfO concept is presented at a high level without sufficient technical depth or operational evidence. The MBD framework, while structurally sound, lacks the detail needed for reproducibility. The reference workflow is too brief to demonstrate practical feasibility. And the curriculum section, while interesting, may not be appropriate for EMS (which focuses on software and modeling, not education policy).

**Score: 6.5/10**
**Verdict: Major Revision**

---

## Dimension Scores

| Dimension | Score (1-10) | Comment |
|-----------|-------------|---------|
| Novelty/Innovation | 7 | DfO concept is genuinely novel for water sector; MBD adaptation useful |
| Mathematical Rigor | 5.5 | DfO principles stated but not formalized; no quantitative DfO metrics |
| Reproducibility | 5.5 | Reference workflow too sketchy; tool chain gaps acknowledged but not addressed |
| Case Validation | 5 | Three-pool canal example is illustrative only; no real system application |
| Literature Completeness | 6 | 18 references is thin for EMS; missing key MBD and systems engineering refs |
| Writing Quality | 7.5 | Clear and well-organized; professional style |
| System Differentiation | 7 | Good DfC vs DfO contrast; digital twin and BIM positioning helpful |

---

## Major Issues

### M1. DfO Principles Lack Quantitative Metrics

The five DfO principles (controllability, observability, ODD-awareness, verifiability, maintainability) are stated as design philosophy but lack quantitative metrics. How does an engineer evaluate whether a design satisfies "controllability by design"? In control theory, controllability has a precise definition (rank condition of the controllability matrix). DfO should connect to these formal definitions. For example: "A DfO-compliant design achieves full state controllability within the target ODD, as verified by the controllability Gramian of the Layer 6 model." Without quantitative metrics, DfO is a philosophy rather than an engineering methodology.

**Recommendation**: For each DfO principle, provide (a) a formal definition linked to control/systems theory, (b) a quantitative metric that can be computed from the MBD model stack, and (c) a threshold or decision criterion. This transforms DfO from a manifesto to a checkable specification.

### M2. Reference Workflow Insufficiently Detailed

The three-pool canal workflow (§6) occupies only ~500 words and reads as a list of steps rather than a demonstrated workflow. For EMS readers, the value proposition is the software tool chain—they need to see code snippets, model specifications, FMI coupling details, and quantitative verification results. Currently, the workflow says "an OpenModelica model is constructed" but does not show what the model looks like; "the MPC controller is designed in Simulink" but does not show the Simulink block diagram or controller parameterization details; "MiL verification: water level tracking RMSE is verified to be below 0.05 m" but does not present the verification results.

**Recommendation**: Expand §6 to ~1,500 words with: (a) key OpenModelica equations or component diagram; (b) Simulink MPC configuration table (prediction horizon, weights, sampling time, solver); (c) FMI coupling configuration; (d) quantitative MiL results (RMSE values, constraint satisfaction, computation time); (e) at least one figure showing the comparison between Layer 7 simulation and Layer 6 control model response.

### M3. Curriculum Section May Not Fit EMS Scope

Environmental Modelling & Software focuses on "the use of new software concepts and techniques, the design of new algorithms, and the development of novel computational methods." Curriculum design is outside its usual scope. The curriculum section (§5, ~600 words) could be perceived as tangential by EMS reviewers. Consider either: (a) substantially reducing §5 to a brief forward-looking paragraph in the Discussion; or (b) reframing the curriculum content as "educational software requirements"—what simulation and laboratory software is needed to teach CHS, how existing tools fall short, and what new educational software packages are needed.

**Recommendation**: Reframe §5 as "Educational Software Infrastructure for CHS" and focus on the software tools and platforms needed for training, including open-source simulation environments, laboratory automation software, and remote-access virtual laboratory platforms. This brings the curriculum content within EMS scope.

### M4. Software Availability Section Needs Substance

EMS requires a Software Availability section for papers presenting software contributions. The current section describes a "CHS-MBD Toolchain Reference Implementation" at "prototype stage" with a repository URL "to be provided upon acceptance." This is insufficient. EMS expects: (a) a functional, downloadable software artifact; (b) documentation and examples; (c) a clear description of what the software does and how it differs from existing tools. If the software is not yet available, the paper should state this honestly and position the contribution as a framework/methodology paper rather than a software paper.

**Recommendation**: Either (a) provide a genuine software artifact (e.g., an OpenModelica water component library + Simulink MPC templates + FMI coupling scripts) with a public repository, or (b) remove the Software Availability section and reframe the paper as a methodology/review paper. Option (a) would significantly strengthen the paper for EMS.

### M5. Literature Too Thin

18 references is insufficient for an EMS paper presenting a new framework. Key missing references include: (a) model-based systems engineering literature (Estefan, 2007; Friedenthal et al., 2014); (b) FMI/co-simulation literature beyond Blochwitz (Gomes et al., 2018); (c) water systems software reviews (Vojinovic & Tutulic, 2009; Creaco et al., 2019); (d) open-source water modeling initiatives (Hutton et al., 2016); (e) engineering education literature for interdisciplinary programs (Borrego & Newswander, 2010). Adding 10-15 references would bring the paper to a respectable level for EMS.

---

## Minor Issues

### m1. Definition 1 Scope
Definition 1 (DfO) uses "operational performance criterion" without specifying what this criterion is. List specific criteria: closed-loop stability margin, disturbance rejection bandwidth, WSAL-level achievability, ODD coverage.

### m2. Table 1 "Water-Specific" Column
Table 2 includes a "Water-Specific" column but Table 1 does not. Adding a column to Table 1 indicating which MBD layers have water-specific content vs. generic systems engineering content would help readers identify the paper's domain contribution.

### m3. MBD Layer Numbering Direction
The layers are numbered 7 (top, most abstract) to 1 (bottom, most concrete). This is counterintuitive for most readers who expect Layer 1 to be the most fundamental. Consider reversing the numbering (Layer 1 = Physical, Layer 7 = Deployment) or adding a clear rationale for the chosen direction.

### m4. V-Model Discussion
The V-model correspondence (§7.2) is mentioned briefly but not shown in a figure. Given that this is a key organizing concept, consider adding it to Figure 2 or creating a separate figure.

### m5. DfO vs BIM Integration
§7.4 mentions that DfO extends BIM but does not specify how. What BIM data formats (IFC, COBie) would carry DfO information? How would ODD specifications be embedded in a BIM model? This connection is potentially valuable for the infrastructure engineering audience.

### m6. No Comparison with Other MBD Frameworks
The paper does not compare its seven-layer MBD with existing MBD frameworks in other domains (AUTOSAR in automotive, DO-178C in aerospace). A brief comparison table showing how each domain structures its model-to-deployment pipeline would strengthen the cross-sector argument.

---

## Summary

The paper addresses a genuine gap—the absence of a design-to-deployment methodology for water systems control—and the DfO and MBD concepts are potentially valuable contributions. However, the current version lacks the quantitative depth, software substance, and reference workflow detail that EMS expects. The major revisions needed are: quantify DfO principles, expand the reference workflow substantially, reframe the curriculum as educational software, provide or honestly position the software availability, and strengthen the literature. These are substantive but addressable issues.
