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


def initial_condition1(x, load):
    u = np.full(x.shape[1], load, dtype=np.float64)  
    u[np.isclose(x[0], 0.0)] = 0.0                    
    return u

def initial_condition2(x, load, base):
    z = np.maximum(x[0], 1e-12)                       
    u = (2.0 * load / np.pi) * (
        np.arctan(base / (2.0 * z)) +
        (base * z) / (2.0 * z**2 + 0.5 * base**2)
    )
    u[np.isclose(z, 0.0)] = 0.0                       
    return u


def _normalise_layer_depths(depths, H):
    depths = np.asarray(depths, dtype=np.float64)

    if np.isclose(depths[0], 0.0):
        layer_depths = depths.copy()
    else:
        layer_depths = np.concatenate(([0.0], depths))

    if not np.isclose(layer_depths[-1], H):
        layer_depths = np.concatenate((layer_depths, [H]))

    return layer_depths


def _layer_numbers_from_depths(depth_values, layer_depths):
    depth_values = np.asarray(depth_values, dtype=np.float64)
    layer_numbers = np.digitize(depth_values, layer_depths[1:], right=True)
    return np.clip(layer_numbers, 0, len(layer_depths) - 2)


def _layer_values_at_depths(depth_values, layer_depths, layer_values):
    layer_values = np.asarray(layer_values, dtype=np.float64)
    return layer_values[_layer_numbers_from_depths(depth_values, layer_depths)]


def Get_Kappa(msh, layer_depths, Cv):
    # defining dimensions and connectivity
    tdim = msh.topology.dim
    msh.topology.create_connectivity(tdim, 0)
    conn = msh.topology.connectivity(tdim, 0)

    num_cells_local = msh.topology.index_map(tdim).size_local
    cell_verts = conn.array.reshape(num_cells_local, 2)

    x = msh.geometry.x[:,0] # z geomtry only 
    midpoints = 0.5 * (x[cell_verts[:, 0]] + x[cell_verts[:, 1]]) # cell_verts the 0 or 1 talks about the left and right respectively

    DG0 = fem.functionspace(msh, ("DG", 0))
    kappa_values = _layer_values_at_depths(midpoints, layer_depths, Cv)

    kappa = fem.Function(DG0)
    dofmap = DG0.dofmap
    kappa.x.array[:] = 0.0

    for cell in range(num_cells_local):
        dof = dofmap.cell_dofs(cell)[0]
        kappa.x.array[dof] = kappa_values[cell]

    kappa.x.scatter_forward()
    return kappa





def Get_terzaghi1dMultilayer_FEA(depths, num:float, Load:float, T:float, time_steps:int, Cv: list[float], Mv: list[float], Base:float, U0=True):
    # defining further paramters 
    dt = T / (time_steps - 1)
    H = max(depths)
    z = np.linspace(0, H, num + 1, dtype= np.float64)
    layer_depths = _normalise_layer_depths(depths, H)

    # def mesh     
    msh = mesh.create_interval(
        comm=MPI.COMM_WORLD,
        nx=num,
        points=[0.0, H],
    )

    # Initial condition callback for fem.Function.interpolate
    if U0:
        initial_condition = lambda x : initial_condition1(x, Load)
    else:
        initial_condition = lambda x : initial_condition2(x, Load, Base)

    kappa = Get_Kappa(msh, layer_depths, Cv)

    V = fem.functionspace(msh, ("Lagrange", 1))

    # Solution functions
    u_n = fem.Function(V)

    # Initial condition
    u_n.interpolate(initial_condition)

    fdim = msh.topology.dim - 1
    boundary_facets = mesh.locate_entities_boundary(
        msh, fdim,
        marker=lambda x: np.isclose(x[0], 0.0)
    )

    dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
    bc = fem.dirichletbc(PETSc.ScalarType(0), dofs, V)
    uh = fem.Function(V)
    uh.name = "uh"
    uh.interpolate(initial_condition)
    # xdmf.write_function(uh,t)

    # varational form
    u, v = ufl.TrialFunction(V), ufl.TestFunction(V)
    # PETSc make sure the background stuff doesnt explode
    a = (u * v) * ufl.dx + dt * kappa  * ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
    L = (u_n) * v * ufl.dx
    bilinear_form = fem.form(a)
    linear_form = fem.form(L)

    A = assemble_matrix(bilinear_form, bcs = [bc])
    A.assemble()
    b = petsc.create_vector(fem.extract_function_spaces(linear_form))

    # creating linear solver 
    solver = PETSc.KSP().create(msh.comm)
    solver.setOperators(A)
    solver.setType(PETSc.KSP.Type.PREONLY)
    solver.getPC().setType(PETSc.PC.Type.LU)
    u_hist = np.zeros((time_steps, uh.x.array.size), dtype=float)
    u_hist[0, :] = uh.x.array.copy()   # initial state

    for i in range(time_steps - 1):
        with b.localForm() as loc_b:
            loc_b.set(0.0)
        assemble_vector(b, linear_form)

        apply_lifting(b ,[bilinear_form], [[bc]])
        b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES,
                    mode=PETSc.ScatterMode.REVERSE)
        set_bc(b, [bc])

        # Solve
        solver.solve(b, uh.x.petsc_vec)

        # Update time-step solution
        u_n.x.array[:] = uh.x.array
        u_n.x.scatter_forward()

        u_hist[i + 1, :] = uh.x.array.copy()

    # xdmf.close()
    A.destroy()
    b.destroy()
    solver.destroy()

    u0 = u_hist[0, :]                 # initial condition in space

    # getting settlement
    Mv_profile = _layer_values_at_depths(z, layer_depths, Mv)
    strain_hist = Mv_profile[None, :] * (u0[None, :] - u_hist)
    settlement_history = np.trapezoid(strain_hist, x=z, axis=1)
    settlement = u0 * Mv_profile * (H / num)

    return settlement_history, u_hist, settlement
