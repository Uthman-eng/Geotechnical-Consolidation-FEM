import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.geotech_consolidation.models.terzaghi_2d.fem import Get_terzaghi2D_FEA
from src.plotting.terzaghi_2d.plot import (
    Get_Mesh_Plot,
    Get_Pore_Pressure_Plot,
    Get_Settlement_Plot,
)


def _parse_float_list(text):
    return [float(value.strip()) for value in text.split(",") if value.strip()]


st.set_page_config(layout="wide")
st.title("2D Terzaghi Consolidation")
st.write(
    "This dashboard solves the 2D Terzaghi consolidation model using the finite element method (FEM). "
    "The page shows the generated mesh, pore-pressure contours, and surface-settlement response."
)

col1, col2 = st.columns([3.5, 1.2])

with col2:
    H = st.number_input("depth (m)", min_value=0.5, value=5.0)
    W = st.number_input("half width (m)", min_value=0.5, value=5.0)
    nx = st.number_input("elements per direction", min_value=5, max_value=200, value=25)
    load = st.number_input("Load applied (kPa)", min_value=0.0, value=100.0)
    base = st.number_input("loaded width (m)", min_value=0.1, value=2.0)
    final_time_days = st.number_input("Final time (days)", min_value=1.0, value=365.0)
    time_steps = st.number_input("time steps", min_value=10, max_value=5000, value=300)
    use_layers = st.toggle("Use layered properties", value=True)

    if use_layers:
        depths_text = st.text_input("Depth interfaces (m)", "1.5, 3.0, 5.0")
        cv_text = st.text_input("Cv by layer", "2e-7, 1e-7, 3e-7")
        mv_text = st.text_input("Mv by layer", "5e-4, 8e-4, 4e-4")
    else:
        depths_text = ""
        cv_text = "2e-7"
        mv_text = "5e-4"

with col1:
    if st.button("Solve 2D model"):
        try:
            final_time = final_time_days * 60 * 60 * 24
            time = np.linspace(0.0, final_time_days, int(time_steps))

            if use_layers:
                depths = _parse_float_list(depths_text)
                Cv = _parse_float_list(cv_text)
                Mv = _parse_float_list(mv_text)
            else:
                depths = None
                Cv = float(cv_text)
                Mv = float(mv_text)

            settlement_surface, u_hist, unique_X, node_X, node_Y = Get_terzaghi2D_FEA(
                H=H,
                W=W,
                nx=int(nx),
                load=load,
                final_time=final_time,
                time_steps=int(time_steps),
                Cv=Cv,
                Mv=Mv,
                base=base,
                depths=depths,
            )
        except ValueError as exc:
            st.error(f"Invalid input: {exc}")
        else:
            st.subheader("Mesh")
            st.write("Triangular mesh used for the 2D FEM model.")
            fig_mesh, _ = Get_Mesh_Plot(node_X, node_Y)
            st.pyplot(fig_mesh)

            st.subheader("Pore Pressure")
            st.write("Pore-pressure contour at the selected time step.")
            time_idx = st.slider(
                "Pore-pressure time step",
                min_value=0,
                max_value=int(time_steps) - 1,
                value=min(10, int(time_steps) - 1),
            )
            fig_pressure, _ = Get_Pore_Pressure_Plot(u_hist, node_X, node_Y, time_idx, time)
            st.pyplot(fig_pressure)

            st.subheader("Settlement")
            st.write("Surface settlement profile at the selected time step.")
            settlement_idx = st.slider(
                "Settlement time step",
                min_value=0,
                max_value=int(time_steps) - 1,
                value=int(time_steps) - 1,
            )
            fig_settlement, _ = Get_Settlement_Plot(settlement_surface, unique_X, settlement_idx, time)
            st.pyplot(fig_settlement)

            centre_idx = int(np.argmin(np.abs(unique_X)))
            fig_hist, ax_hist = plt.subplots()
            ax_hist.plot(time, -settlement_surface[:, centre_idx], label=f"x = {unique_X[centre_idx]:.2f} m")
            ax_hist.set_xlabel("Time (days)")
            ax_hist.set_ylabel("Settlement (m)")
            ax_hist.set_title("Centre-line settlement through time")
            ax_hist.grid(True)
            ax_hist.legend()
            st.pyplot(fig_hist)

            st.write(f"Maximum pore pressure: {u_hist.max():.2f} kPa")
            st.write(f"Maximum surface settlement: {settlement_surface.max():.4f} m")
