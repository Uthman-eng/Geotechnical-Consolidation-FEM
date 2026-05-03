# Geotechnical Consolidation FEM (FEniCSx)

A Python-based finite element framework for modelling consolidation settlement in soils using FEniCSx (DOLFINx).

## Features

- Fourier series analytical solver (arbitrary initial conditions) used as a reference solution
- 1D multilayer FEM with piecewise `Cv` and `Mv`; flux continuity at layer interfaces is recovered as a natural condition
- 2D FEM under uniform strip loading with layered material input; initial pore pressure from Boussinesq elasticity (Craig, 2004)
- Settlement computed via trapezoidal quadrature of pore pressure dissipation
- FEM solvers in `src/geotech_consolidation/models/` are importable independently of the Streamlit layer
- Verification notebooks in `notebooks/` and Settle3 comparison in `demo/`
- Unit tests in `tests/unit/`

## Example Outputs

- Settlement against time
- Excess pore pressure dissipation with depth
- 2D pore pressure heatmaps
- FEM vs analytical comparison plots
- 2D surface settlement profile
- FEM vs Settle3 comparison plots (demo notebooks)

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

### Quick Start

```bash
git clone https://github.com/Uthman-eng/Geotechnical-Consolidation-FEM.git
cd Geotechnical-Consolidation-FEM
docker compose up --build
```

> The `.devcontainer` configuration has been removed. If you want to develop interactively in VS Code, create your own `devcontainer.json` pointing at the `Dockerfile`.

### Screenshots

**1D pore pressure**

![1D pore pressure](/assets/images/1d_pp.png)

**1D settlement**

![1D settlement](/assets/images/1d_settlement.png)

**2D pore pressure**

![2D pore pressure](/assets/images/2d_pp.png)

**2D settlement**

![2D settlement](/assets/images/2d_settlement.png)

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
|-- notebooks/                # Verification notebooks
|-- demo/                     # Settle3 comparison notebooks and data
|-- tests/
|   `-- unit/
|-- assets/
|   `-- images/
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

## Theory

This implementation uses Terzaghi's uncoupled formulation (pore pressure and displacement are not coupled). Settlement is post processed from the pore pressure field, rather than solved, as part of a coupled system, distinguishing it from full Biot (Biot, 1941).

The governing equation is:

```text
∂u/∂t = Cv ∂²u/∂z²
```

with `u` excess pore pressure, `Cv` coefficient of consolidation, `z` depth, and `t` time.

Settlement is computed from pore pressure dissipation:

```text
s(t) = ∫ Mv(z) [u0(z) - u(z,t)] dz
```

evaluated by trapezoidal quadrature over depth.

For the 2D case, `u0` is taken from Boussinesq linear elasticity for a uniform strip load. The profile is forced to zero at the drained boundary to avoid the singularity at `z = 0`.

## Verification & Validation

Verification is carried out in [notebooks/](notebooks/). The demo notebooks in [demo/](demo/) contain Settle3 comparisons and are kept separate.

## Tech Stack

- Python, NumPy, matplotlib, Plotly
- FEniCSx / DOLFINx
- Streamlit
- Jupyter Notebook
- Docker

## References

- Terzaghi, K. (1943). *Theoretical Soil Mechanics*. Wiley.
- Biot, M. A. (1941). General theory of three-dimensional consolidation. *Journal of Applied Physics*, 12(2), 155–164.
- Craig, R. F. (2004). *Craig's Soil Mechanics* (7th ed.). Spon Press.
- Larsson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
- Rocscience. *Settle3*. [https://www.rocscience.com/software/settle3](https://www.rocscience.com/software/settle3)
- FEniCSx Project Documentation: [https://docs.fenicsproject.org/](https://docs.fenicsproject.org/)
