import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import plotly.graph_objects as go



def Get_Settlement_Animation(settlement_surface, unique_X, time, interval=30):
    fig, ax = plt.subplots()
    ax.grid(True)
    line, = ax.plot(unique_X, -settlement_surface[0], label="Surface settlement", marker="o")
    ax.set_xlim(unique_X.min(), unique_X.max())
    ax.set_ylim(-settlement_surface.max() * 1.1, -settlement_surface.min() * 1.1)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Settlement (m)")
    ax.legend()

    def update(frame):
        line.set_ydata(-settlement_surface[frame])
        ax.set_title(f"Settlement - t = {time[frame]:.1f} days")
        return (line,)

    anim = animation.FuncAnimation( fig=fig, func=update, frames=len(time), interval=interval, blit=True)
    return fig, anim


def Get_Settlement_Plot(settlement_surface, unique_X, time_idx, time):
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.plot(unique_X, -settlement_surface[time_idx], label="Surface settlement", marker="o")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Settlement (m)")
    ax.set_title(f"Settlement at t = {time[time_idx]:.1f} days")
    ax.legend()
    return fig, ax


def Get_Mesh_Plot_Plotly(node_X, node_Y):

    fig = go.Figure()
    fig.add_scatter( x=node_X, y=node_Y, mode="markers")

    fig.update_layout( title="2D FEM mesh", xaxis_title="x (m)", yaxis_title="y (m)",height=650)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def Get_Settlement_Plot_Plotly(settlement_surface, unique_X, time_idx, time):
    fig = go.Figure()
    fig.add_trace( go.Scatter( x=unique_X, y=-settlement_surface[time_idx], mode="lines+markers", name="Surface settlement")
    )
    fig.update_layout(
        title=f"Settlement at t = {time[time_idx]:.1f} days",
        xaxis_title="x (m)",
        yaxis_title="Settlement (m)",
        height=650,
    )
    return fig

def Get_Centre_Line_Settlement_Plot_Plotly(settlement_surface, unique_X, time):
    centre_idx = int(np.argmin(np.abs(unique_X)))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time,
            y=-settlement_surface[:, centre_idx],
            mode="lines",
            name=f"x = {unique_X[centre_idx]:.2f} m",
        )
    )
    fig.update_layout(
        title="Centre-line settlement",
        xaxis_title="Time (days)",
        yaxis_title="Settlement (m)",
        height=650,
    )
    return fig


def Get_Pore_Pressure_Plot_Plotly(node_X, node_Y, u_hist, time_idx, time, load):
    x_tol = 1e-8
    y_tol = 1e-8
    x_rounded = np.round(node_X / x_tol) * x_tol
    y_rounded = np.round(node_Y / y_tol) * y_tol

    unique_x = np.unique(x_rounded)
    unique_y = np.unique(y_rounded)
    z_grid = np.full((unique_y.size, unique_x.size), np.nan, dtype=float)

    x_index = {value: idx for idx, value in enumerate(unique_x)}
    y_index = {value: idx for idx, value in enumerate(unique_y)}

    for node_id, value in enumerate(u_hist[time_idx, :]):
        ix = x_index[x_rounded[node_id]]
        iy = y_index[y_rounded[node_id]]
        z_grid[iy, ix] = value

    fig = go.Figure(
        data=go.Heatmap(
            x=unique_x,
            y=unique_y,
            z=z_grid,
            colorscale="Viridis",
            zmin=0.0,
            zmax=load,
            colorbar=dict(title="u (kPa)"),
        )
    )
    fig.update_layout(
        title=f"Pore pressure at t = {time[time_idx]:.1f} days",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        height=650,
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=2)
    return fig

