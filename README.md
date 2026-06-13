# Geotechnical Consolidation FEM (FEniCSx)

A Python-based finite element framework for modelling consolidation settlement in soils using FEniCSx.

## Features

- Fourier series analytical solver (arbitrary initial conditions) used as a reference solution
- 1D multilayer FEM with piecewise $C_v$ and $M_v$.
- 2D FEM under uniform strip loading with layered material input.
- Settlement computed via trapezoidal quadrature of pore pressure dissipation.
- FEM solvers in `src/geotech_consolidation/models/` are importable independently of the Streamlit layer.
- Verification notebooks in `notebooks/` and Settle3 comparison in `demo/`.

## Getting Started (No Coding Required)

> **TIP**
> Already comfortable with Git and Docker? Skip to [For Technical Users](#for-technical-users).

You don't need any programming experience to run the models, just install two free tools, then copy a few commands.

### 1. Install the two tools

- **[Git](https://git-scm.com/downloads)** - downloads the project onto your computer.
- **[Docker Desktop](https://www.docker.com/products/docker-desktop)** - runs the project in a self-contained box, so you don't have to install Python or anything else yourself. After installing,  **ensure Docker Desktop is open and leave it running**.

### 2. Open a terminal

- **Windows:** press the Windows key, type `cmd`, press Enter.
- **Mac:** press Cmd + Space, type `Terminal`, press Enter.

### 3. Run the project

Type these one at a time, pressing Enter after each:

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
cd Geotechnical-Consolidation-FEM
docker compose up --build
```

The first run takes a few minutes while Docker sets everything up. When it finishes, open a browser and go to **http://localhost:8501**. This is the interface for entering soil parameters and running the models.

To stop it, return to the terminal and press `Ctrl + C`.


## For Technical Users

### Quick Start

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
cd Geotechnical-Consolidation-FEM
docker compose up --build
```

>The .devcontainer configuration has been removed. If you want to develop interactively in VS Code, create your own devcontainer.json pointing at the Dockerfile.


### Screenshots

**1D pore pressure**

![1D pore pressure](assets/images/1d_pp.png)

**1D settlement**

![1D settlement](assets/images/1d_settlement.png)

**2D pore pressure**

![2D pore pressure](assets/images/2d_pp.png)

**2D settlement**

![2D settlement](assets/images/2d_settlement.png)

## Project Structure

```text
Geotechnical-Consolidation-FEM/
|-- app.py
|-- ui/                       # Shared Streamlit UI components
|-- pages/                    # Streamlit pages
|-- .streamlit/               # Streamlit theme and config
|-- src/
|   `-- geotech_consolidation/
|       |-- models/           # FEM solvers
|       `-- plotting/         # Plotting helpers
|-- notebooks/                # Verification notebooks
|-- demo/                     # Settle3 comparison
|-- assets/
|   `-- images/
|-- Dockerfile
|-- docker-compose.yml
|-- pyproject.toml
|-- requirements.txt
|-- README.md
|-- THEORY.md
`-- LICENSE
```

## Theory

This implementation uses Terzaghi's uncoupled formulation (pore pressure and displacement are not coupled). Settlement is post processed from the pore pressure field, rather than solved, as part of a coupled system, distinguishing it from full Biot *(Biot, 1941).*

The governing equation is:

$$\frac{\partial u}{\partial t} = C_v \nabla^2 u$$

with $u$ excess pore pressure, $C_v$ coefficient of consolidation, $z$ depth, and $t$ time.

Settlement is computed from pore pressure dissipation:

$$s(t) = \int_0^H m_v(z)\,[\,u_0(z) - u(z,t)\,]\, dz$$


For the 2D case, $u0$ is taken from the Boussinesq strip-load stress field, linear elasticity for a uniform strip load. The profile is forced to zero at the drained boundary to avoid the singularity at $z = 0$.

For further information on; weak form, discrete system, convergence bounds, settlement integral, and the Nyquist aliasing argument see [THEORY.md](THEORY.md).

## Verification & Validation

Verification is carried out in [notebooks/](notebooks/). The demo notebooks in [demo/](demo/) contain Settle3 comparisons and are kept separate. Convergence rates and validation results are summarised in [THEORY.md](THEORY.md).

## Tech Stack

- Python, NumPy, matplotlib, Plotly
- FEniCSx / DOLFINx
- Streamlit
- Jupyter Notebook
- Docker

## References

- Aziz, U. (2026). *Finite Element Modelling of Consolidation Settlement: Implementation, Verification and Open-Source Delivery* (dissertation).
- Terzaghi, K. (1943). *Theoretical Soil Mechanics*. Wiley.
- Biot, M. A. (1941). General theory of three-dimensional consolidation. *Journal of Applied Physics*, 12(2), 155–164.
- Craig, R. F. (2004). *Craig's Soil Mechanics* (7th ed.). Spon Press.
- Brenner, S. C., and Scott, L. R. (2008). *The Mathematical Theory of Finite Element Methods* (3rd ed.). Springer.
- Larsson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
- Rocscience. *Settle3*. [https://www.rocscience.com/software/settle3](https://www.rocscience.com/software/settle3)
- FEniCSx Project Documentation: [https://docs.fenicsproject.org/](https://docs.fenicsproject.org/)
