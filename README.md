# Finite Element Methods for Geotechnical Consolidation

This repository implements FEniCSx to model excess pore pressure dissipation in soils over time, due to consolidation. The project focuses on finite element solvers, verification, and streamlit integration of models.

The repository currently includes:
- **Terzaghi 1D Consolidation (Single Layer)**: Analytical reference solution + verified FEM implementation + Streamlit integration

- **Terzaghi 1D Consolidation (Multi-Layer)**: FEM model with layered, piecewise material properties *(working; verification in progress)* + Streamlit integration

- **Terzaghi 2D Consolidation (Single or Multi-Layer)**: Extension to 2D mesh-based FEM modelling *(under active development)*

- **Biot Consolidation (Planned)**: Future implementation of fully coupled displacement pore pressure consolidation theory

## Repository Structure
- `app.py` + `pages/` – Streamlit user interface

- `docs/` – Notebooks and supporting derivations
 
- `.devcontainer/` + `Dockerfile` – Reproducible development environment  

### Scripts
- `scripts/terzaghi_1d/` – Analytical + FEM solver (single-layer)
  
- `scripts/terzaghi_1d_multilayer/` – FEM solver (multi-layer)
   
- `scripts/terzaghi_2d/` – 2D FEM consolidation *(under development)*  

## Demos

### 1D Model 

- 1D Consolidation Demo: Time-dependent excess pore pressure dissipation and resulting settlement evolution (single- and multi-layer).
  
<p align="center">
  <img src="https://github.com/user-attachments/assets/c74f45fa-6e01-498d-a151-fb6d1a064e5d" width="550" alt="Initial excess pore pressure (1D)" />
  <br/>
  <em>Initial excess pore pressure distribution, u₀ (1D consolidation).</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/1f7e9e53-1b02-43db-91ee-da23046f97ac" width="550" alt="Settlement evolution (1D)" />
  <br/>
  <em>Surface settlement evolution over time (1D model).</em>
</p>


### 2D Model 

- 2D Consolidation Demo: Mesh-based pore pressure dissipation and surface settlement response under strip loading (single- or multi-layer, in progress).
  
<p align="center">
  <img src="https://github.com/user-attachments/assets/f8935e74-ae54-43f8-8cdc-f648de6ac0d8" width="550" alt="Initial excess pore pressure (2D)" />
  <br/>
  <em>Initial excess pore pressure field, u₀ (2D strip loading).</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/67eedd5e-5ed5-4bdf-916d-90ecec1fb988" width="550" alt="Settlement evolution (2D)" />
  <br/>
  <em>Surface settlement response at end time (2D model).</em>
</p>

## References

- Terzaghi, K. (1943). Theoretical Soil Mechanics. Wiley.  

- Biot, M. A. (1941). General theory of three-dimensional consolidation. Journal of Applied Physics, 12(2), 155–164.  

- FEniCSx Project Documentation: https://docs.fenicsproject.org/

- Larson, M. G., & Bengzon, F. (2013). The Finite Element Method: Theory, Implementation, and Applications. Springer.  









