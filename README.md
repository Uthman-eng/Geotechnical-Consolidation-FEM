# Geotechnical Consolidation FEM (FEniCSx)

A Python-based finite element framework for modelling consolidation settlement in soils.

- 1D Terzaghi consolidation
- 1D multilayer consolidation
- 2D layered strip loading using FEM
- Verification against analytical solutions and engineering comparison data
- Streamlit interface for running and visualising the models
- Verification and demo notebooks for interpretation of results

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
cd Geotechnical-Consolidation-FEM
```

Run the project with:

```bash
docker compose up --build
```

## Features

- 1D single-layer consolidation modelling
- 1D multilayer consolidation with layer-wise `Cv` and `Mv`
- 2D FEM consolidation under strip loading with layered material input
- Settlement and excess pore pressure plots
- Jupyter notebooks for verification and demonstration
- Settle3 comparison notebooks with signed percentage difference plots

## Example Outputs / Results

The project currently produces:

- settlement against time
- excess pore pressure dissipation with depth
- 2D pore pressure heatmaps
- FEM against analytical comparison plots
- 2D surface settlement response across the loaded width
- FEM against Settle3 comparison plots in the demo notebooks

Example figures used in the project:

1D pore pressure:

![alt text](/assets/images/1d_pp.png)

1D settlement:

![alt text](/assets/images/1d_settlement.png)

2D pore pressure:

![alt text](/assets/images/2d_pp.png)

2D settlement:

![alt text](/assets/images/2d_settlement.png)

## Project Structure

```text
Geotechnical-Consolidation-FEM-1/
|-- app.py
|-- .devcontainer/            # Optional VS Code dev container setup
|-- ui/                       
|-- pages/                    # Streamlit pages
|-- .streamlit/               # Streamlit theme and local config
|-- src/
|   |-- geotech_consolidation/
|   |   `-- models/           # 1D, multilayer 1D, and 2D FEM solvers
|   `-- plotting/             # Plotting helpers used by notebooks and Streamlit
|-- notebooks/                # Main verification notebooks
|-- demo/                     # Demo notebooks and Settle3 comparison data
|-- tests/
|   `-- unit/
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

In the FEM post-processing, this depth integral is evaluated numerically using trapezoidal quadrature (or rectangle qaudrature).

For the Boussinesq-type initial condition, the profile has been forced to be zero near the drained boundary to avoid the singular behaviour at `z = 0`.

## Verification & Validation

Verification in this project is carried in [notebooks](notebooks). This should not be confused with the demo and comparison to settle3 dataset.

Validation work is lighter at this stage, but includes comparison datasets in [demo/settle3_data](demo/settle3_data)

Demo notebooks are kept separately in [demo](/Users/uthmanaziz/Desktop/Github/Consolidation-FEM/Geotechnical-Consolidation-FEM-1/demo):

- [demo/1_terzaghi_1d_singlelayer.ipynb](demo/1_terzaghi_1d_singlelayer.ipynb)
- [demo/2_terzaghi_1d_multilayer.ipynb](demo/2_terzaghi_1d_multilayer.ipynb)
- [demo/3_terzaghi_2d.ipynb](demo/3_terzaghi_2d.ipynb)

## Tech Stack

- Python
- NumPy
- matplotlib
- Plotly
- FEniCSx / DOLFINx
- Streamlit
- Jupyter Notebook
- Docker

## References

- Terzaghi, K. (1943). *Theoretical Soil Mechanics*. Wiley.
- Biot, M. A. (1941). General theory of three-dimensional consolidation. *Journal of Applied Physics*, 12(2), 155-164.
- Larson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
- Rocscience. *Settle3*. [https://www.rocscience.com/software/settle3](https://www.rocscience.com/software/settle3)
- FEniCSx Project Documentation: [https://docs.fenicsproject.org/](https://docs.fenicsproject.org/)
