# Geotechnical Consolidation FEM (FEniCSx)

A Python-based finite element framework for modelling consolidation settlement in soils.

- 1D Terzaghi consolidation
- 1D multilayer consolidation
- 2D strip loading using FEM
- Verification against analytical solutions and engineering comparison data
- Streamlit interface for running and visualising the models
- Verification and demo notebooks for interpretation of results

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
cd Geotechnical-Consolidation-FEM
```

Build the Docker image:

```bash
docker build -t geotech-consolidation .
```

Run the container and expose Streamlit:

```bash
docker run -it -p 8501:8501 geotech-consolidation
```

Start the app inside the container:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Open:

```text
http://localhost:8501
```

For tests inside the container:

```bash
python -m pytest -q
```

## Features

- 1D single-layer consolidation modelling
- 1D multilayer consolidation with layer-wise `Cv` and `Mv`
- 2D FEM consolidation under strip loading
- Analytical Fourier-series comparison for 1D verification
- Settlement and excess pore pressure plots
- Streamlit dashboard for interactive parameter input
- Jupyter notebooks for verification and demonstration

## Example Outputs / Results

The project currently produces:

- settlement against time
- excess pore pressure dissipation with depth
- 2D pore pressure distributions
- FEM against analytical comparison plots
- 2D surface settlement response across the loaded width

Example figures used in the project:

1D pore pressure:

![1D pore pressure](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/assets/images/u_data_1D.png)

1D settlement:

![1D settlement](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/assets/images/Settlement_1D.png)

2D pore pressure:

![2D pore pressure](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/assets/images/u0_2D.png)

2D settlement:

![2D settlement](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/assets/images/Settlement_2D.png)

## Project Structure

```text
Geotechnical-Consolidation-FEM-1/
|-- app.py
|-- pages/                    # Streamlit pages for 1D, multilayer 1D, and 2D
|-- src/
|   |-- geotech_consolidation/
|   |   `-- models/           # 1D, multilayer 1D, and 2D FEM solvers
|   `-- plotting/             # Plotting helpers used by notebooks and Streamlit
|-- notebooks/                # Main verification notebooks
|-- demo/                     # Lighter notebooks for visual output / comparison data
|-- tests/
|   |-- unit/
|   `-- integration/
|-- assets/
|   `-- images/
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

## Theory

The main 1D governing equation used here is the Terzaghi consolidation equation:

```text
∂u/∂t = Cv ∂²u/∂z²
```

where:

- `u` = excess pore pressure
- `Cv` = coefficient of consolidation
- `z` = depth
- `t` = time

Settlement is obtained from the pore pressure dissipation using `Mv`:

```text
s(t) = ∫ Mv(z) [u0(z) - u(z,t)] dz
```

In the FEM post-processing, this depth integral is evaluated numerically using trapezoidal quadrature.

For the Boussinesq-type initial condition, the profile is regularised near the drained boundary to avoid the singular behaviour at `z = 0`.

## Verification & Validation

Verification in this project is mainly carried out through the notebooks in [notebooks](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/notebooks).

Current verification notebooks:

- [notebooks/0_Analytical_Fourier_Quadrature.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/notebooks/0_Analytical_Fourier_Quadrature.ipynb)
- [notebooks/1_terzaghi_1d_singlelayer.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/notebooks/1_terzaghi_1d_singlelayer.ipynb)
- [notebooks/2_terzaghi_1d_multilayer.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/notebooks/2_terzaghi_1d_multilayer.ipynb)
- [notebooks/3_terzaghi_2d.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/notebooks/3_terzaghi_2d.ipynb)

Current checks include:

- 1D FEM against the analytical Terzaghi solution
- arbitrary `u0` Fourier reconstruction checks
- Boussinesq initial condition comparison
- mesh and time-step sensitivity checks
- multilayer logic checks in `pytest`

Validation work is lighter at this stage, but includes:

- comparison against engineering expectations
- comparison datasets in [demo/settle3_data](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/demo/settle3_data)

Demo notebooks are kept separately in [demo](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/demo):

- [demo/1_terzaghi_1d_singlelayer.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/demo/1_terzaghi_1d_singlelayer.ipynb)
- [demo/2_terzaghi_1d_multilayer.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/demo/2_terzaghi_1d_multilayer.ipynb)
- [demo/3_terzaghi_2d.ipynb](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/demo/3_terzaghi_2d.ipynb)

## Tech Stack

- Python
- NumPy
- matplotlib
- FEniCSx / DOLFINx
- PETSc
- MPI
- Streamlit
- Jupyter Notebook
- Docker

## Roadmap

- continue multilayer 1D verification
- improve 2D verification and interpretation
- extend layered material handling further in 2D
- investigate Biot-type coupled consolidation
- improve test coverage beyond smoke tests
- refine post-processing and engineering comparison workflows

## References

- Terzaghi, K. (1943). *Theoretical Soil Mechanics*. Wiley.
- Biot, M. A. (1941). General theory of three-dimensional consolidation. *Journal of Applied Physics*, 12(2), 155-164.
- Larson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
- FEniCSx Project Documentation: [https://docs.fenicsproject.org/](https://docs.fenicsproject.org/)
