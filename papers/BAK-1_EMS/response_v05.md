# Point-by-Point Response — BAK-1 Iteration 4

**Reviewer**: B (Engineering Practitioner)
**Draft**: v04 → v05

---

## Minor Issues

### m1. Docker Image Size and Availability

**Response**: Clarified in §4.5: Docker image size is 2.1 GB (OpenModelica base: 1.8 GB, HydroComponents + MSL: 0.3 GB). The image is hosted on Docker Hub (public, free pull). A lightweight alternative is provided: direct installation of OpenModelica + library clone (total ~50 MB excluding OpenModelica).

### m2. License Compatibility

**Response**: Clarified in Software Availability: "The MIT license applies to the HydroComponents Modelica source code. Runtime compilation and simulation require a Modelica-compliant compiler; OpenModelica (GPL-3.0, free) is recommended. The Modelica Standard Library 4.0.0 dependency is BSD-3-Clause licensed."
