import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.graph_objects as go


def Get_Settlement_Plot(settlement_hist, time):
    fig, ax = plt.subplots(figsize = (7,4))
    ax.plot(time, -settlement_hist, label="FEM Settlement")
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Settlement (m)")
    ax.set_title("Settlement vs Time")
    ax.grid(True)
    ax.legend()
    return fig, ax


def Get_Settlement_Plot_Plotly(settlement_hist, time):
    fig = px.line(x = time, y = -settlement_hist,
                  title = "Settlement vs Time",
                  labels = {
                      'x' : "Time (days)",
                      'y' : "Settlement (m)"
                  })
    fig.update_layout(height=650)
    return fig
 
def consolidation_heatmap_plotly(data, x, y):
    fig = go.Figure(data=go.Heatmap(
                z = data,
                x = x, 
                y = y,
                colorscale="Viridis"
                ))
    fig.update_layout(
        title="Pore Pressure Dissipation Over Time",
        xaxis=dict(title="Time (days)", nticks=10),
        yaxis=dict(title="Depth (m)", nticks=10),
        height=650
        )
    return fig 