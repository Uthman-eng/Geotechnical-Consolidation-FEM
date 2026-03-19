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
    u[np.isclose(x[1], 0.0)] = 0.0 
    return u

def _normalise_depth_interfaces(depths, H):
    depths = np.asarray(depths, dtype=np.float64)

    if np.isclose(depths[0], 0.0):
        interfaces = depths.copy()
    else:
        interfaces = np.concatenate(([0.0], depths))

    if not np.isclose(interfaces[-1], H):
        interfaces = np.concatenate((interfaces, [H]))

    return interfaces

def _as_layer_values(values):
    return np.atleast_1d(np.asarray(values, dtype=np.float64))


def _build_layer_field_2d(msh, interfaces, layer_values):
    tdim = msh.topology.dim
    msh.topology.create_connectivity(tdim, 0)
    conn = msh.topology.connectivity(tdim, 0)

    num_cells_local = msh.topology.index_map(tdim).size_local
    cell_vertices = conn.array.reshape(num_cells_local, 3)

    coords = msh.geometry.x
    cell_mid_depths = -np.mean(coords[cell_vertices, 1], axis=1)

    DG0 = fem.functionspace(msh, ("DG", 0))
    layer_field = fem.Function(DG0)
    layer_field.x.array[:] = 0.0

    dofmap = DG0.dofmap
    layer_ids = np.digitize(cell_mid_depths, interfaces[1:], right=True)
    layer_ids = np.clip(layer_ids, 0, len(layer_values) - 1)

    for cell in range(num_cells_local):
        dof = dofmap.cell_dofs(cell)[0]
        layer_field.x.array[dof] = layer_values[layer_ids[cell]]

    layer_field.x.scatter_forward()
    return layer_field


def _settlement_by_surface_column(strain_hist, node_X, node_depths):
    tol = 1e-8
    x_rounded = np.round(node_X / tol) * tol
    unique_X, inv = np.unique(x_rounded, return_inverse=True)
    settlement_surface = np.zeros((strain_hist.shape[0], unique_X.size), dtype=float)

    for x_id in range(unique_X.size):
        column_nodes = np.where(inv == x_id)[0]
        column_order = np.argsort(node_depths[column_nodes])
        ordered_nodes = column_nodes[column_order]
        ordered_depths = node_depths[ordered_nodes]
        settlement_surface[:, x_id] = np.trapezoid(
            strain_hist[:, ordered_nodes],
            x=ordered_depths,
            axis=1,
        )

    return settlement_surface, unique_X


def Get_terzaghi2D_FEA(H: float, W: float, nx: int, load: float, final_time: float, time_steps: int, Cv, Mv, base: float, depths=None):

    dt = final_time / (time_steps - 1)
    Cv_values = _as_layer_values(Cv)
    Mv_values = _as_layer_values(Mv)

    if depths is None:
        interfaces = np.asarray([0.0, H], dtype=np.float64)
    else:
        interfaces = _normalise_depth_interfaces(depths, H)

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
    if Cv_values.size == 1:
        kappa = fem.Constant(msh, Cv_values[0])
    else:
        kappa = _build_layer_field_2d(msh, interfaces, Cv_values)

    a = (u * v) * ufl.dx + dt * kappa * ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
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

    node_X = msh.geometry.x[:, 0].copy()
    node_Y = msh.geometry.x[:, 1].copy()
    node_depths = -node_Y

    u0 = u_hist[0, :]
    node_layer_ids = np.digitize(node_depths, interfaces[1:], right=True)
    node_layer_ids = np.clip(node_layer_ids, 0, len(Mv_values) - 1)
    Mv_profile = Mv_values[node_layer_ids]
    strain_hist = Mv_profile[None, :] * (u0[None, :] - u_hist)
    settlement_surface, unique_X = _settlement_by_surface_column(
        strain_hist,
        node_X,
        node_depths,
    )

    total_strain = Mv_profile * u0
    total_settlement_surface, _ = _settlement_by_surface_column(
        total_strain[None, :],
        node_X,
        node_depths,
    )
    total_settlement = np.max(total_settlement_surface[0, :])

    return settlement_surface, total_settlement, u_hist, unique_X, node_X, node_Y
