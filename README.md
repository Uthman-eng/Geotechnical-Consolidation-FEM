# Finite Element Methods for Geotechnical Consolidation

This repository explores 1D and 2D consolidation modelling for saturated soils using via FEniCSx. The focus is on Terzaghi consolidation theory, comparing analytical and FEM pore-pressure dissipation and settlement. The project is still under development.

## Current Status

- Single-layer 1D modelling and verification
- Multilayer 1D solving is implemented, and multilayer verification is still under development
- 2D work is present as an early draft

## Theory

The governing equation solved here is a diffusion type excess pore pressure equation

```text
du/dt = Cv d²u/dz²
```

where:

- `u` is excess pore pressure
- `t` is time
- `z` is depth
- `Cv` is the coefficient of consolidation

Where the top boundary is treated as drained, and is enforced to zero.

Settlement is calculated from the the pore pressure dissipation history using the compressibility parameter `Mv`. 
Settlement = ∫ Mv​(z) * Δσ′(z) * dz (integral over the domain)



Modelling notes for interpretation and verification:

1. The Boussinesq initial pore pressure profile is zeroed near the drained boundary to avoid singular behaviour at `z = 0`, where the equaion collapse to a singularity.
2. Settlement is currently evaluated using a discrete depth summation over the mesh spacing. This is a numerical quadrature choice. Comparison to alternatives quadrature choices, such as trapezoidal integration, so not to be confused with post processing error.
## Repository Structure

```text
Geotechnical-Consolidation-FEM-1/
|-- app.py
|-- pages/
|   |-- 1_1d_terazaghi.py
|   `-- 2_1d_multilayer_terazaghi.py
|-- demo/
|   |-- 1_terzaghi_1d.singlelayer.ipynb
|   |-- 2_terzaghi_1d_multilayer.ipynb
|   `-- 7_terzaghi_2d.ipynb
|-- notebooks/
|   |-- 1_terzaghi_1d_singlelayer.ipynb
|   |-- 2_Analytical_Fourier_Series.ipynb
|   |-- 3_terzaghi_1d_multilayer.ipynb
|   |-- 4_terzaghi_2d.ipynb
|-- src/
|   |-- geotech_consolidation/
|   |   `-- models/
|   |       |-- terzaghi_1d/
|   |       |-- terzaghi_1d_multi/
|   |       `-- terzaghi_2d/
|   `-- plotting/
|       |-- terzaghi_1d/
|       `-- terzaghi_2d/
|-- tests/
|   `-- unit/
|-- assets/
|   `-- images/
|-- Dockerfile
|-- requirements.txt
`-- LICENSE
```

## Environment Setup

The FEM solvers depend on the DOLFINx / PETSc / MPI stack. The recommended workflow is to run this project inside Docker.

### Docker

Build the image:

```bash
docker build -t geotech-consolidation .
```

Run the container:

```bash
docker run -it -p 8501:8501 geotech-consolidation
```

Then start Streamlit inside the container:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Open the app at [http://localhost:8501](http://localhost:8501).

## Running Checks

Automated checks in [tests/unit](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/tests/unit).

Typical command:

```bash
python -m pytest -q
```

## Verification and Demo Notebooks

The Jupyter notebooks are the main place for verification, comparison, and demonstration of the FEM models.

- Verification notebooks focus on analytical comparison, convergence studies, interface checks, and interpretation of consolidation behaviour.
- Demo notebooks are lighter notebooks intended mainly for visualising pore pressure and settlement outputs.

## Demo Figures

### 1D Consolidation

Example 1D excess pore-pressure result:

<img src="assets/images/u_data_1D.png" width="450" alt="1D pore pressure response" />

Example 1D settlement result:

<img src="assets/images/Settlement_1D.png" width="450" alt="1D settlement response" />

### 2D Consolidation

Example 2D excess pore-pressure result:

<img src="assets/images/u0_2D.png" width="450" alt="2D pore pressure response" />

Example 2D settlement result:

<img src="assets/images/Settlement_2D.png" width="450" alt="2D settlement response" />

## References

- Terzaghi, K. (1943). *Theoretical Soil Mechanics*. Wiley.
- Biot, M. A. (1941). General theory of three-dimensional consolidation. *Journal of Applied Physics*, 12(2), 155-164.
- FEniCSx Project Documentation: [https://docs.fenicsproject.org/](https://docs.fenicsproject.org/)
- Larson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
