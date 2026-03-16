import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri


def Get_Pore_Pressure_Contour(u_hist, node_X, node_Y, time_idx, time):
    """
    Filled contour plot of excess pore pressure on the 2D mesh at a single time step.

    Parameters
    ----------
    u_hist : np.ndarray, shape (time_steps, n_nodes)
        Pore pressure history from Get_terzaghi2D_FEA.
    node_X : np.ndarray, shape (n_nodes,)
        x-coordinates of mesh nodes (msh.geometry.x[:, 0]).
    node_Y : np.ndarray, shape (n_nodes,)
        y-coordinates of mesh nodes (msh.geometry.x[:, 1]).
    time_idx : int
        Time step index to plot.
    time : np.ndarray, shape (time_steps,)
        Time axis in days (used for the plot title).

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    tri = mtri.Triangulation(node_X, node_Y)
    u_min = np.min(u_hist)
    u_max = np.max(u_hist)

    fig, ax = plt.subplots()
    cs = ax.tricontourf(tri, u_hist[time_idx], levels=20, vmin=u_min, vmax=u_max, cmap="YlOrRd")
    fig.colorbar(cs, ax=ax, label="Excess pore pressure (kPa)")
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Depth (m)")
    ax.set_title(f"Pore Pressure — t = {time[time_idx]:.1f} days")

    return fig, ax


def Get_Settlement_Surface_Plot(settlement_surface, unique_X, time_idx, time):
    """
    Settlement profile across the surface at a single time step.

    Parameters
    ----------
    settlement_surface : np.ndarray, shape (time_steps, nX)
        Surface settlement history from Get_terzaghi2D_FEA.
    unique_X : np.ndarray, shape (nX,)
        x-coordinates of the surface settlement profile.
    time_idx : int
        Time step index to plot.
    time : np.ndarray, shape (time_steps,)
        Time axis in days (used for the plot title).

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    fig, ax = plt.subplots()
    ax.plot(unique_X, -settlement_surface[time_idx], label=f"t = {time[time_idx]:.1f} days")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Settlement (m)")
    ax.set_title("Surface Settlement Profile")
    ax.grid(True)
    ax.legend()

    return fig, ax


def Get_Settlement_Surface_History_Plot(settlement_surface, unique_X, time, n_curves=8):
    """
    Surface settlement profiles at multiple time steps on a single axes —
    useful for showing how the settlement trough evolves over time.

    Parameters
    ----------
    settlement_surface : np.ndarray, shape (time_steps, nX)
        Surface settlement history from Get_terzaghi2D_FEA.
    unique_X : np.ndarray, shape (nX,)
        x-coordinates of the surface settlement profile.
    time : np.ndarray, shape (time_steps,)
        Time axis in days.
    n_curves : int
        Number of evenly spaced time curves to overlay (default 8).

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    indices = np.linspace(0, len(time) - 1, n_curves, dtype=int)

    fig, ax = plt.subplots()
    for idx in indices:
        ax.plot(unique_X, -settlement_surface[idx], label=f"{time[idx]:.0f} days")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("Settlement (m)")
    ax.set_title("Surface Settlement Profile Over Time")
    ax.grid(True)
    ax.legend(title="Time", fontsize=8)

    return fig, ax
