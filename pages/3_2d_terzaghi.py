import streamlit as st
import numpy as np

from ui.inputs import parse_float_list
from ui.style import page_style
from src.geotech_consolidation.models.terzaghi_2d.fem import Get_terzaghi2D_FEA
from src.plotting.terzaghi_2d.plot import (
    Get_Centre_Line_Settlement_Plot_Plotly,
    Get_Mesh_Plot_Plotly,
    Get_Pore_Pressure_Plot_Plotly,
    Get_Settlement_Plot_Plotly,
)


page_style("2D Terzaghi Consolidation")

seconds_to_days = 60 * 60 * 24
gamma_w = 9.81

st.title("2D Terzaghi Consolidation")
st.caption("2D FEM dashboard for strip loading with optional layered properties.")

controls, results = st.columns([1.05, 2.4], gap="large")
result_key = "twoD_result"

with controls:
    with st.form("twoD_form"):
        W = st.number_input("Half width (m)", min_value=0.5, value=5.0)
        nx = int(st.number_input("Elements per direction", min_value=5, max_value=200, value=25))
        load = st.number_input("Load applied (kPa)", min_value=0.0, value=100.0)
        base = st.number_input("Loaded width (m)", min_value=0.1, value=2.0)
        final_time_days = st.number_input("Final time (days)", min_value=1.0, value=365.0)
        time_steps = int(st.number_input("Time steps", min_value=10, max_value=5000, value=300))
        depths = parse_float_list(st.text_input("Depth interfaces (m)", "1.5, 3.0, 5.0"))
        H = max(depths)
        Cv = parse_float_list(st.text_input("Cv by layer", "2e-7, 1e-7, 3e-7"))
        Mv = parse_float_list(st.text_input("Mv by layer", "5e-4, 8e-4, 4e-4"))
        k_list = parse_float_list(st.text_input("Permeability k by layer", "9.81e-10, 19.62e-10, 9.81e-10, 9.81e-10"))
        Cv = [k_i / (Mv_i * gamma_w) for k_i, Mv_i in zip(k_list, Mv)]
        st.caption("Cv: " + ", ".join(f"{value:.2e}" for value in Cv))
        
        solve = st.form_submit_button("Solve 2D model", use_container_width=True)

with results:
    if solve:
        final_time = final_time_days * seconds_to_days
        time = np.linspace(0.0, final_time_days, int(time_steps))

        settlement_surface, total_settlement, u_hist, unique_X, node_X, node_Y = Get_terzaghi2D_FEA( H, W, nx, load, final_time, time_steps, Cv, Mv, base, depths=depths)
        st.session_state[result_key] = {
            "settlement_surface": settlement_surface,
            "total_settlement": total_settlement,
            "u_hist": u_hist,
            "unique_X": unique_X,
            "node_X": node_X,
            "node_Y": node_Y,
            "time": time,
            "time_steps": time_steps,
            "load": load,
            "layer_count": len(Mv)
        }

    if result_key not in st.session_state:
        st.info("Choose parameters and click `Solve 2D model`.")
    else:
        result = st.session_state[result_key]
        settlement_surface = result["settlement_surface"]
        total_settlement = result["total_settlement"]
        u_hist = result["u_hist"]
        unique_X = result["unique_X"]
        node_X = result["node_X"]
        node_Y = result["node_Y"]
        time = result["time"]
        time_steps = result["time_steps"]
        load = result["load"]
        layer_count = result["layer_count"]
        final_time_settlement = np.max(settlement_surface[-1, :])

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Total settlement", f"{total_settlement:.4f} m")
        metric2.metric("Settlement at final time", f"{final_time_settlement:.4f} m")
        metric3.metric("Layer count", f"{layer_count}")

        tab1, tab2, tab3 = st.tabs(["Mesh", "Settlement", "Pore Pressure"])

        with tab1:
            fig_mesh = Get_Mesh_Plot_Plotly(node_X, node_Y)
            st.plotly_chart(fig_mesh, use_container_width=True)

        with tab2:
            fig_hist = Get_Centre_Line_Settlement_Plot_Plotly(settlement_surface, unique_X, time)
            st.plotly_chart(fig_hist, use_container_width=True)

            settlement_idx = st.slider(
                "Settlement time step",
                min_value=0,
                max_value=int(time_steps) - 1,
                value=int(time_steps) - 1,
                key="twoD_settlement_slider",
            )
            fig_settlement = Get_Settlement_Plot_Plotly(settlement_surface, unique_X, settlement_idx, time)
            st.plotly_chart(fig_settlement, use_container_width=True)

        with tab3:
            pore_idx = st.slider(
                "Pore pressure time step",
                min_value=0,
                max_value=int(time_steps) - 1,
                value=int(time_steps) - 1,
                key="twoD_pore_slider",
            )
            fig_pore = Get_Pore_Pressure_Plot_Plotly(node_X, node_Y, u_hist, pore_idx, time, load)
            st.plotly_chart(fig_pore, use_container_width=True)
