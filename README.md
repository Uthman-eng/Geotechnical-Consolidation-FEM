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

This section is for you if you have never used programming tools before but want to run the consolidation models. You do not need to understand code, you just need to follow the steps below.

### What you will need to install first

Before you can run anything, you need to install two pieces of software on your computer. Think of them like apps that this project depends on.

**1. Git**

Git is a free software tool used to download and manage code projects from the internet. It works through a terminal (explained below). You use it once to grab a copy of this project onto your computer.

Download it here: https://git-scm.com/downloads — choose the version for your operating system (Windows, Mac, etc.) and install it like any normal program.

**2. Docker**

Docker is a free program that packages up everything this project needs to run (Python, libraries, solvers) into a self contained box called a "container". This means you do not need to install Python or anything else manually, Docker handles it all. Without Docker, the project will not run.

Download Docker Desktop here: https://www.docker.com/products/docker-desktop. Once installed, open Docker Desktop and leave it running in the background before you proceed.

### What is the terminal?

The terminal (also called "Command Prompt" on Windows or "Terminal" on Mac/Linux) is a text-based way of talking to your computer. Instead of clicking buttons, you type short commands and press Enter. Only a handful of commands are needed here. 

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

Docker will now download and set up everything it needs (this may take a few minutes the first time). Once it finishes, you will see a message in the terminal with a local address — usually something like `http://localhost:8501`.

**Step 4 — Open the app**

Open any web browser (Chrome, Firefox, Edge) and go to:

```
http://localhost:8501
```

You will see a web interface where you can input soil parameters and run the consolidation models, no coding required.

**Step 5 — Stopping the project**

When you are done, go back to the terminal and press `Ctrl + C` to stop the application.

### What can you do in the app?

Once the app is open in your browser, you can:

- Run a **1D single-layer** Terzaghi consolidation analysis by entering your layer's `Cv`, `Mv`, drainage conditions, and load
- Run a **1D multilayer** analysis for a soil profile with multiple layers, each with their own `Cv` and `Mv` values
- Run a **2D strip load** analysis to see how pore pressures spread laterally beneath a foundation
- View plots of settlement against time, excess pore pressure dissipation with depth, and 2D pore pressure heatmaps

---

## For Technical Users

A Python-based finite element framework for 1D and 2D consolidation settlement modelling, built on FEniCSx (DOLFINx). The project is fully containerised via Docker and exposes a Streamlit interface alongside Jupyter notebooks for verification and demonstration.

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

### Features

- 1D single-layer consolidation modelling (FEM + Fourier series analytical solver for verification)
- 1D multilayer consolidation with layer-wise `Cv` and `Mv`, including interface continuity enforcement
- 2D FEM consolidation under strip loading with layered material input (Boussinesq-type initial pore pressure condition)
- Settlement computed via trapezoidal/rectangle quadrature of the pore pressure dissipation integral
- Separation of FEM solvers (`src/geotech_consolidation/models/`) from plotting utilities (`src/plotting/`) to allow programmatic use without the Streamlit layer
- Verification notebooks (`notebooks/`) covering Fourier series convergence, FEM vs analytical comparison, and multilayer behaviour
- Demo notebooks (`demo/`) with Settle3 comparison datasets and signed percentage difference plots
- Unit tests in `tests/unit/`

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

The main 1D governing equation used here is the Terzaghi consolidation equation:

```text
∂u/∂t = Cv ∂²u/∂z²
```

where:

- `u` = excess pore pressure
- `Cv` = coefficient of consolidation
- `z` = depth
- `t` = time

Note that this implementation follows Terzaghi's uncoupled formulation — pore pressure and displacement are not coupled; settlement is post-processed from the pore pressure field rather than solved as part of a coupled system. This distinguishes it from the full Biot consolidation framework (Biot, 1941).

Settlement is obtained from the pore pressure dissipation using `Mv`:

```text
s(t) = ∫ Mv(z) [u0(z) - u(z,t)] dz
```

In the FEM post-processing, this depth integral is evaluated numerically using trapezoidal quadrature (unless stated otherwise).

For the Boussinesq-type initial condition, the profile has been forced to be zero near the drained boundary to avoid the singular behaviour at `z = 0`.

### Weak form

Multiplying the strong form by a test function `v` and integrating by parts over the domain `Ω = [0, H]` gives the weak form: find `u ∈ V` such that for all `v ∈ V`:

```text
∫_Ω (∂u/∂t) v dz  +  ∫_Ω Cv (∂u/∂z)(∂v/∂z) dz  =  0
```

Boundary terms vanish because the drained boundary enforces `u = 0` (Dirichlet) and the undrained boundary enforces zero flux (homogeneous Neumann). For the multilayer case, `Cv` is piecewise constant and the flux continuity condition at layer interfaces is satisfied naturally by the variational formulation.

### Piecewise discontinuity and Darcy flux at layer interfaces

In a multilayer profile, `Cv` is piecewise constant with jump discontinuities at each layer interface `z = z_i`. The physical requirement at an interface is continuity of Darcy flux:

```text
[q]_{z=z_i}  =  0      where  q = -(k / γw) ∂u/∂z = -Cv (Mv / mv) ∂u/∂z
```

or, written directly in terms of the consolidation coefficient:

```text
Cv^+ (∂u/∂z)^+  =  Cv^- (∂u/∂z)^-      at  z = z_i
```

Because `Cv` jumps at the interface, `∂u/∂z` must also jump in the opposite sense so that their product — the flux — remains continuous. This is a **natural interface condition** in the Galerkin sense: it is not imposed explicitly. Instead, the global weak form integrates over each subdomain separately and the interface flux terms cancel when the test space is globally continuous (CG1). Pore pressure `u` itself is continuous across the interface (enforced by the CG1 continuity of the trial space), while its gradient `∂u/∂z` is allowed to be discontinuous, exactly as the physics requires.

This means the Galerkin discretisation automatically respects both conditions at every interface:
- `u` continuous (CG1 trial space)
- `Cv ∂u/∂z` continuous (natural condition, satisfied in the weak sense)

No additional penalty, Lagrange multiplier, or mortar treatment is needed.

### Element choice

Linear Lagrange elements (CG1 / P1) are used for the pore pressure field in all models. The resulting system matrix is sparse and symmetric positive definite, which allows efficient direct or iterative solves. For the 2D model, triangular CG1 elements are used on an unstructured mesh generated by DOLFINx's built-in mesh utilities.

### Time discretisation

A backward Euler (implicit, first-order) scheme is used throughout:

```text
(u^{n+1} - u^n) / Δt  +  A u^{n+1}  =  0
```

where `A` is the assembled stiffness operator. Backward Euler is unconditionally stable, which avoids the CFL-type restriction on `Δt` that would apply with an explicit scheme. The time step `Δt` is uniform and user-specified.

## Verification & Validation

Verification in this project is carried in [notebooks](notebooks). This should not be confused with the demo and comparison to settle3 dataset.

### Convergence

Spatial and temporal convergence studies are reported in the verification notebooks for the 1D single-layer model. Results under uniform mesh and time-step refinement:

| Refinement | Observed order |
|------------|---------------|
| Spatial (h-refinement, fixed Δt) | ~2.0 |
| Temporal (Δt-refinement, fixed h) | ~1.1 |

The spatial rate of ~2.0 is consistent with CG1 elements on a smooth problem (optimal L2 convergence for linear elements). The temporal rate of ~1.1 is consistent with backward Euler at O(Δt), with the slight elevation above 1.0 with minor deviation from unity likely reflecting the finite convergence range studied.

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
