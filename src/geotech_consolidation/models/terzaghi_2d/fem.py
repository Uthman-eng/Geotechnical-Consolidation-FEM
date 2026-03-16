from mpi4py import MPI

import numpy as np
from petsc4py import PETSc

import ufl
from dolfinx import fem, mesh
from dolfinx.fem import petsc
from dolfinx.fem.petsc import (
    assemble_vector,
    assemble_matrix,
    apply_lifting,
    set_bc)


def boussinesq_condition_2d(x, load, base):
    B = base / 2
    eps = 1e-12
    X = x[0]
    Z = np.maximum(-x[1], eps)              # depth is positive downward; mesh y <= 0

    term1 = np.arctan((X + B) / Z) - np.arctan((X - B) / Z)
    term2 = Z * ((X + B) / ((X + B)**2 + Z**2) - (X - B) / ((X - B)**2 + Z**2))

    u = (load / np.pi) * (term1 + term2)
    u[np.isclose(x[1], 0.0)] = 0.0         # enforce drained BC at surface
    return u


def Get_terzaghi2D_FEA(
    H: float,
    W: float,
    nx: int,
    load: float,
    final_time: float,
    time_steps: int,
    Cv: float,
    Mv: float,
    base: float,
):
    """
    2D Terzaghi consolidation FEM solver (Boussinesq initial condition).

    Domain: rectangle [-W, W] x [-H, 0], where y = 0 is the drained top surface.

    Parameters
    ----------
    H : float
        Depth of the soil layer (m).
    W : float
        Half-width of the domain (m); full domain width = 2W.
    nx : int
        Number of elements in each direction (nx x nx triangular mesh).
    load : float
        Applied surface load (kPa).
    final_time : float
        Total simulation time (s).
    time_steps : int
        Number of time steps (including t = 0).
    Cv : float
        Coefficient of consolidation (m^2/s).
    Mv : float
        Coefficient of volume compressibility (1/kPa).
    base : float
        Full width of the loaded area for Boussinesq distribution (m).

    Returns
    -------
    settlement_surface : np.ndarray, shape (time_steps, nX)
        Consolidation settlement at each surface x-position for every time step.
        Analogous to settlement_history in the 1D model, extended over the surface width.
    u_hist : np.ndarray, shape (time_steps, n_nodes)
        Excess pore pressure at every mesh node for every time step.
    unique_X : np.ndarray, shape (nX,)
        x-coordinates corresponding to the columns of settlement_surface.
        Use as the horizontal axis when plotting surface settlement.
    node_X : np.ndarray, shape (n_nodes,)
        x-coordinates of every mesh node (msh.geometry.x[:, 0]).
        Pass directly to the plotting functions alongside node_Y.
    node_Y : np.ndarray, shape (n_nodes,)
        y-coordinates of every mesh node (msh.geometry.x[:, 1]).
        Pass directly to the plotting functions alongside node_X.
    """

    dt = final_time / (time_steps - 1)

    msh = mesh.create_rectangle(
        MPI.COMM_WORLD,
        [np.array([-W, -H]), np.array([W, 0.0])],
        [nx, nx],
        mesh.CellType.triangle,
    )

    initial_condition = lambda x: boussinesq_condition_2d(x, load, base)

    V = fem.functionspace(msh, ("Lagrange", 1))

    # Solution functions
    u_n = fem.Function(V)
    u_n.name = "u_n"
    u_n.interpolate(initial_condition)

    # Drained boundary condition: u = 0 at top surface (y = 0)
    fdim = msh.topology.dim - 1
    boundary_facets = mesh.locate_entities_boundary(
        msh, fdim,
        marker=lambda x: np.isclose(x[1], 0.0),
    )
    dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
    bc = fem.dirichletbc(PETSc.ScalarType(0), dofs, V)

    uh = fem.Function(V)
    uh.name = "uh"
    uh.interpolate(initial_condition)

    # Variational form (implicit Euler)
    u, v = ufl.TrialFunction(V), ufl.TestFunction(V)
    c = fem.Constant(msh, Cv)
    a = (u * v) * ufl.dx + dt * c * ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
    L = u_n * v * ufl.dx
    bilinear_form = fem.form(a)
    linear_form = fem.form(L)

    A = assemble_matrix(bilinear_form, bcs=[bc])
    A.assemble()
    b = petsc.create_vector(fem.extract_function_spaces(linear_form))

    solver = PETSc.KSP().create(msh.comm)
    solver.setOperators(A)
    solver.setType(PETSc.KSP.Type.PREONLY)
    solver.getPC().setType(PETSc.PC.Type.LU)

    u_hist = np.zeros((time_steps, uh.x.array.size), dtype=float)
    u_hist[0, :] = uh.x.array.copy()       # initial state at t = 0

    for i in range(time_steps - 1):
        with b.localForm() as loc_b:
            loc_b.set(0.0)
        assemble_vector(b, linear_form)

        apply_lifting(b, [bilinear_form], [[bc]])
        b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES,
                      mode=PETSc.ScatterMode.REVERSE)
        set_bc(b, [bc])

        solver.solve(b, uh.x.petsc_vec)

        u_n.x.array[:] = uh.x.array
        u_n.x.scatter_forward()

        u_hist[i + 1, :] = uh.x.array.copy()

    A.destroy()
    b.destroy()
    solver.destroy()

    # --- Settlement post-processing ---
    node_X = msh.geometry.x[:, 0].copy()
    node_Y = msh.geometry.x[:, 1].copy()

    u0 = u_hist[0, :]
    settlement_slices = Mv * (u0[None, :] - u_hist) * (H / (nx + 1))

    # Bin nodes by x-coordinate to get surface settlement per x-column
    tol = 1e-8
    x_rounded = np.round(node_X / tol) * tol
    unique_X, inv = np.unique(x_rounded, return_inverse=True)
    nX = unique_X.size
    nt = settlement_slices.shape[0]

    settlement_by_x = np.empty((nX, nt), dtype=float)
    for t in range(nt):
        settlement_by_x[:, t] = np.bincount(inv, weights=settlement_slices[t], minlength=nX)

    # (time_steps, nX) — analogous to settlement_history in 1D, extended over the surface
    settlement_surface = settlement_by_x.T

    return settlement_surface, u_hist, unique_X, node_X, node_Y
