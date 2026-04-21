# Geotechnical Consolidation FEM (FEniCSx)

A Python-based finite element framework for modelling consolidation settlement in soils.

- 1D Terzaghi consolidation
- 1D multilayer consolidation
- 2D layered strip loading using FEM
- Verification against analytical solutions and engineering comparison data
- Streamlit interface for running and visualising the models
- Verification and demo notebooks for interpretation of results

---

## For Geotechnical Engineers & Students (No Programming Experience Required)

This section is for you if you have never used programming tools before, but want to run the consolidation models. No understanding in programming is needed. Following the steps below will allow you to run the models.

### What you will need to install first

Before you can run anything, you need to install two pieces of software on your computer. Think of them like apps that this project depends on.

**1. Git**

Git is a free software tool used to download and manage code projects from the internet. It works through a terminal (explained below). You use it once to grab a copy of this project onto your computer.

Download it here: https://git-scm.com/downloads — choose the version for your operating system (Windows, Mac, etc.) and install it like any normal program.

**2. Docker**

Docker is a free program that packages up everything this project needs to run (Python, libraries, solvers) into a self contained box called a "container". This means you do not need to install Python or anything else manually, Docker handles it all. Without Docker, the project will not run.

Download Docker Desktop here: https://www.docker.com/products/docker-desktop. Once installed, open Docker Desktop and leave it running in the background before you proceed.

### What is the terminal?

The terminal (also called "Command Prompt" on Windows or "Terminal" on Mac/Linux) is a text based way of talking to your computer. Instead of clicking buttons, you type short commands and press Enter. Only a handful of commands are needed here. 

- On **Windows**: press the Windows key, type `cmd` or `PowerShell`, and press Enter.
- On **Mac**: press Cmd + Space, type `Terminal`, and press Enter.

### Step-by-step: getting the project running

Once Git and Docker are both installed and Docker Desktop is open:

**Step 1 — Download the project**

Open your terminal and type the following, then press Enter:

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
```

This will download all the project files into a folder on your computer. You only need to do this once.

**Step 2 — Navigate into the project folder**

In the same terminal, type:

```bash
cd Geotechnical-Consolidation-FEM
```

`cd` means "change directory" — it moves you into the folder that was just downloaded.

**Step 3 — Build and run the project**

Type the following and press Enter:

```bash
docker compose up --build
```

Docker will now download and set up everything it needs (this may take a few minutes the first time). Once it finishes, you will see a message in the terminal with a local address, usually `http://localhost:8501`.

**Step 4 — Open the app**

Open any web browser (Chrome, Firefox, Edge) and go to:

```
http://localhost:8501
```

You will see a web interface where you can input soil parameters and run the consolidation models.

**Step 5 — Stopping the project**

When you are done, go back to the terminal and press `Ctrl + C` to stop the application.

---

## For Technical Users

A Python based finite element framework for 1D and 2D consolidation settlement modelling, built on FEniCSx (DOLFINx). The project is fully containerised via Docker and implements a Streamlit interface alongside Jupyter notebooks for verification and demonstration. The Theory section below is deliberately concise, it indicates the formulation and methods used, not a full derivation. The dissertation accompanying this repository contains a more in depth theoretical development and analysis.

### Quick Start

Clone the repository:

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
cd Geotechnical-Consolidation-FEM
```

Run the project with:

```bash
docker compose up --build
```

**Development environment:** The `.devcontainer` configuration has been removed from this repository. The Docker setup is intentionally kept as a runtime environment rather than a development container. If you want to develop or extend the codebase interactively in VS Code, you will need to create your own `devcontainer.json` pointing at the Docker image defined in the `Dockerfile`.

### Features

- 1D single-layer consolidation modelling (FEM + Fourier series analytical solver for verification)
- 1D multilayer consolidation with layer-wise `Cv` and `Mv`, with flux continuity at layer interfaces handled as a natural condition in the weak formulation 
- 2D FEM consolidation under uniform strip loading with layered material input; the initial pore pressure field is taken from Boussinesq elasticity theory for a strip load (see e.g. Craig, 2004)
- Settlement computed via trapezoidal/rectangle quadrature of the pore pressure dissipation integral
- Separation of FEM solvers (`src/geotech_consolidation/models/`) from plotting utilities (`src/plotting/`) to allow programmatic use without the Streamlit layer
- Verification notebooks (`notebooks/`) covering Fourier series convergence, FEM vs analytical comparison, and multilayer behaviour
- Demo notebooks (`demo/`) with Settle3 comparison datasets and signed percentage difference plots
- Unit tests in `tests/unit/`
- The FEM solvers are structured as an importable Python package (`src/geotech_consolidation/`) with a clean separation between solver, post-processing, and visualisation layers. This allows the pore pressure field output to be consumed directly by external scripts or extended post-processing pipelines. Note the package requires either the Docker environment or a manual FEniCSx installation.

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
|-- ui/                       # Shared Streamlit UI components and layout helpers
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

The 1D governing equation is the Terzaghi consolidation equation:

```text
∂u/∂t = Cv ∂²u/∂z²
```

with `u` the excess pore pressure, `Cv` the coefficient of consolidation, `z` depth, and `t` time.

This implementation follows Terzaghi's uncoupled formulation, non coupled pore pressure and displacement. Settlement is post-processed from the pore pressure field rather than solved as part of a coupled system, distinguishing it from the full Biot framework (Biot, 1941).

Settlement is obtained from the pore pressure dissipation via:

```text
s(t) = ∫ Mv(z) [u0(z) - u(z,t)] dz
```

evaluated by trapezoidal quadrature over depth (unless stated otherwise).

For the 2D case, the initial pore pressure distribution `u0(z)` is taken from Boussinesq elasticity theory for a uniform strip load. The profile is forced to zero at the drained boundary to avoid the singular behaviour at `z = 0`.

### Weak form

Find `u ∈ V` such that for all `v ∈ V`:

```text
∫_Ω (∂u/∂t) v dz  +  ∫_Ω Cv (∂u/∂z)(∂v/∂z) dz  =  0
```

on `Ω = [0, H]`, with `u = 0` at the drained boundary and zero flux at the undrained boundary. For the multilayer case, `Cv` is piecewise constant and flux continuity at layer interfaces is recovered naturally from the variational form (not forced).

### Element and time discretisation

Linear Lagrange (CG1 / P1) elements are used throughout for 1D, and triangles on an unstructured mesh in 2D. Time stepping is backward Euler with uniform `Δt`:

```text
(u^{n+1} - u^n) / Δt  +  A u^{n+1}  =  0
```

## Verification & Validation

Verification in this project is carried in [notebooks](notebooks). This should not be confused with the demo and comparison to settle3 dataset.

### Convergence

Spatial and temporal convergence studies for the 1D single-layer model are reported in the verification notebooks. Observed rates under uniform refinement:

| Refinement | Observed order |
|------------|---------------|
| Spatial (h-refinement, fixed Δt) | ~2.0 |
| Temporal (Δt-refinement, fixed h) | ~1.1 |

### Validation

Validation work is lighter at this stage, but includes comparison datasets in [demo/settle3_data](demo/settle3_data)

Demo notebooks are kept separately in [demo](demo):

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
- Craig, R. F. (2004). *Craig's Soil Mechanics* (7th ed.). Spon Press.
- Larsson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
- Rocscience. *Settle3*. [https://www.rocscience.com/software/settle3](https://www.rocscience.com/software/settle3)
- FEniCSx Project Documentation: [https://docs.fenicsproject.org/](https://docs.fenicsproject.org/)
