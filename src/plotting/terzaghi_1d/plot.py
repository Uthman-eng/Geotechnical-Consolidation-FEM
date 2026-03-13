import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Get_Settlement_Plot(settlement_hist, time):
    fig, ax = plt.subplots()
    ax.plot(time, -settlement_hist, label="FEM Settlement")
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Settlement (m)")
    ax.set_title("Settlement vs Time")
    ax.grid(True)
    ax.legend()
    return fig, ax