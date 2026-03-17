import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np


def Get_Mesh_Plot(node_X, node_Y):
    tri = mtri.Triangulation(node_X, node_Y)
    fig, ax = plt.subplots()
    ax.triplot(tri, color="0.35", linewidth=0.5)
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Depth (m)")
    ax.set_title("2D FEM mesh")
    return fig, ax



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
