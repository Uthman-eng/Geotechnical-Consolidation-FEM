import streamlit as st
import numpy as np
import plotly.express as px

from ui.inputs import parse_float_list
from ui.style import page_style
from src.geotech_consolidation.models.terzaghi_1d_multi.fem import Get_terzaghi1dMultilayer_FEA
from src.plotting.terzaghi_1d.plot import Get_Settlement_Plot_Plotly, consolidation_heatmap_plotly


page_style("1D Multilayer Consolidation")

seconds_to_days = 60 * 60 * 24
gamma_w = 9.81


st.title("1D Terzaghi Consolidation - Multilayer")
st.caption("Layer-wise `Cv` and `Mv` with the same 1D FEM formulation.")

controls, results = st.columns([1.05, 2.4], gap="large")
result_key = "oneD_multi_result"

with controls:
    with st.form("oneD_multi_form"):
        num = int(st.number_input("Elements", min_value=10, max_value=1000, value=100))
        load = st.number_input("Load applied (kPa)", min_value=0.0, value=100.0)
        final_time_days = st.number_input("Final time (days)", min_value=1.0, value=365.0)
        time_steps = int(st.number_input("Time steps", min_value=10, max_value=5000, value=1000))
        initial_conditions = st.toggle("Use uniform initial condition", value=False)
        base = st.number_input("Loaded width (m)", min_value=0.1, value=2.5)
        depths = parse_float_list(st.text_input("Depths (m)", "1, 2, 4, 5"))
        H = max(depths)
        Mv = parse_float_list(st.text_input("Mv by layer", "5e-4, 10e-4, 5e-4, 5e-4"))
        k_list = parse_float_list(st.text_input("Permeability k by layer", "9.81e-10, 19.62e-10, 9.81e-10, 9.81e-10"))
        gamma_w = 9.81
        Cv = [k_i / (Mv_i * gamma_w) for k_i, Mv_i in zip(k_list, Mv)]
        st.caption("Cv: " + ", ".join(f"{value:.2e}" for value in Cv))

        solve = st.form_submit_button("Solve multilayer model", use_container_width=True)

with results:
    if solve:
        final_time = final_time_days * seconds_to_days
        settlement_history, u_hist_raw, settlement = Get_terzaghi1dMultilayer_FEA( depths, num, load, final_time, time_steps, Cv, Mv, base, U0=initial_conditions)

        u_hist = u_hist_raw.T
        depth = -np.linspace(0.0, H, num + 1)
        time = np.linspace(0.0, final_time_days, num=time_steps)
        total_settlement = np.trapezoid(settlement)
        final_time_settlement = settlement_history[-1]
        st.session_state[result_key] = {
            "u_hist": u_hist,
            "depth": depth,
            "time": time,
            "total_settlement": total_settlement,
            "final_time_settlement": final_time_settlement,
            "settlement_history": settlement_history,
            "layer_count": len(Mv),
        }

    if result_key not in st.session_state:
        st.info("Choose the layer properties and click `Solve multilayer model`.")
    else:
        result = st.session_state[result_key]
        u_hist = result["u_hist"]
        depth = result["depth"]
        time = result["time"]
        total_settlement = result["total_settlement"]
        final_time_settlement = result["final_time_settlement"]
        settlement_history = result["settlement_history"]
        layer_count = result["layer_count"]

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Total settlement", f"{total_settlement:.4f} m")
        metric2.metric('Settlement at final time',f'{final_time_settlement:.4f} m')
        metric3.metric("Layer count", f'{layer_count}')

        tab1, tab2, tab3 = st.tabs(["Settlement", "Initial Profile", "Pore Pressure"])

        with tab1:
            fig_settlement = Get_Settlement_Plot_Plotly(settlement_history, time)
            st.plotly_chart(fig_settlement, use_container_width=True)

        with tab2:
            fig_ini = px.line(
                x=u_hist[:, 0],
                y=depth,
                title="Initial pore pressure profile",
                labels={"x": "Excess pore pressure (kPa)", "y": "Depth (m)"},
            )
            fig_ini.update_layout(height=650)
            st.plotly_chart(fig_ini, use_container_width=True)

        with tab3:
            fig_cons = consolidation_heatmap_plotly(u_hist, time, depth)
            st.plotly_chart(fig_cons, use_container_width=True)
