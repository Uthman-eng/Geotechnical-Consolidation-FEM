<<<<<<< HEAD
# Finite Element Methods for Geotechnical Consolidation (One Dimensional)

This repository implements FEniCSx to model excess pore pressure dissipation in soils over time, due to consolidation. The project focuses on finite element solvers, verification, and streamlit integration of models.

The repository currently includes:
- **Terzaghi 1D Consolidation (Single Layer)**: Analytical reference solution + verified FEM implementation + Streamlit integration

- **Terzaghi 1D Consolidation (Multi-Layer)**: FEM model with layered, piecewise material properties *(working; verification in progress)* + Streamlit integration

- **Terzaghi 2D Consolidation (Single or Multi-Layer)**: Extension to 2D mesh-based FEM modelling *(under active development)*

- **Biot Consolidation (Planned)**: Future implementation of fully coupled displacement pore pressure consolidation theory

## Repository Structure
```text
Geotechnical-Consolidation-FEM/
|-- app.py                        # Main Streamlit entry point
|-- pages/                        # Streamlit pages for each consolidation model
|-- scripts/                      # Numerical solvers and model code
|   |-- terazaghi_1d/             # Analytical + FEM solver (single-layer)
|   |-- terazaghi_1d_multilayer/  # FEM solver (multi-layer)
|   `-- terazaghi_2d/             # 2D FEM consolidation (under development)
|-- docs/                         # Notebooks and supporting derivations
|-- static/                       # Demo figures and result images
|-- .devcontainer/                # Dev Container configuration
`-- Dockerfile                    # Container setup for reproducible environment
```

## Demo

### 1D Consolidation
- Example 1D excess pore pressure response:

![1D pore pressure response](static/u_data_1D.png)

- Example 1D settlement response:

![1D settlement response](static/Settlement_1D.png)

### 2D Consolidation
- Example 2D excess pore pressure response:

![2D pore pressure response](static/u0_2D.png)

- Example 2D settlement response:

![2D settlement response](static/Settlement_2D.png)

## Environment Setup

This project was set up using the provided Dev Container configuration, since the FEM solvers depend on the FEniCSx / dolfinx stack.

### Option 1 - VS Code Dev Container *(recommended)*
- Open this repository in VS Code

- Make sure the **Dev Containers** extension is installed

- Reopen the project in the container using the `.devcontainer/devcontainer.json` configuration

- This will use the `dolfinx/dolfinx:stable` image and then run:
  `python -m pip install --no-cache-dir -r requirements.txt`

- Once the container has finished loading, run the Streamlit app:
  `streamlit run app.py`

- Then open the local Streamlit link shown in the terminal

### Option 2 - Manual Docker setup
- If not using the Dev Container, the repository also includes a `Dockerfile`

- Build the container:
  `docker build -t geotech-consolidation .`

- Start an interactive container:
  `docker run -it -p 8501:8501 geotech-consolidation`

- Once inside the container, run the Streamlit app:
  `streamlit run app.py --server.address 0.0.0.0`

- Then open Streamlit in your browser at:
  `http://localhost:8501`


## References

- Terzaghi, K. (1943). Theoretical Soil Mechanics. Wiley.  

- Biot, M. A. (1941). General theory of three-dimensional consolidation. Journal of Applied Physics, 12(2), 155–164.  

- FEniCSx Project Documentation: https://docs.fenicsproject.org/

- Larson, M. G., & Bengzon, F. (2013). The Finite Element Method: Theory, Implementation, and Applications. Springer.  






=======
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









>>>>>>> 0c087ca99867e08c3d68b96a8093564e862e875b
