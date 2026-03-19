import streamlit as st
import numpy as np
import plotly.express as px

from ui.style import page_style

from src.geotech_consolidation.models.terzaghi_1d.fem import Get_terzaghi1D_FEA
from src.plotting.terzaghi_1d.plot import Get_Settlement_Plot_Plotly, consolidation_heatmap_plotly
page_style("1D Terzaghi Consolidation")

seconds_to_days = 60 * 60 * 24

st.title("1D Terzaghi Consolidation")
st.caption("Single layer FEM model with uniform or Boussinesq initial pore pressure.")

controls, results = st.columns([1, 2.75], gap="large")
result_key = "oneD_single_result"

with controls:
    with st.form("oneD_single_form"):
        H = st.number_input("Depth (m)", min_value=0.5, value=5.0)
        num = int(st.number_input("Elements", min_value=10, max_value=1000, value=100))
        load = st.number_input("Load applied (kPa)", min_value=0.0, value=100.0)
        final_time_days = st.number_input("Final time (days)", min_value=1.0, value=365.0)
        time_steps = int(st.number_input("Time steps", min_value=10, max_value=10000, value=1000))
        Mv = st.number_input("Mv (m²/kN)", min_value=1e-12, value=5.0e-4)
        k = st.number_input("Permeability k (m/s)", min_value=1e-12, value=9.81e-10, format="%.2e")
        gamma_w = 9.81
        Cv = k / (Mv * gamma_w)
        st.caption(f"Cv = {Cv:.2e} m²/s")
        initial_conditions = st.toggle("Use uniform initial condition", value=False)
        base = st.number_input("Loaded width (m)", min_value=0.1, value=2.5)
        solve = st.form_submit_button("Solve 1D model", use_container_width=True)

with results:
    if solve:
        final_time = final_time_days * seconds_to_days
        settlement_history, u_hist_raw, settlement = Get_terzaghi1D_FEA(H, num, load, final_time, time_steps, Cv, base, Mv, initial_conditions)

        u_hist = u_hist_raw.T
        depth = -np.linspace(0.0, H, num + 1)
        time = np.linspace(0.0, final_time_days, num=time_steps)
        total_settlement = np.sum(settlement)
        final_time_settlement = settlement_history[-1]
        st.session_state[result_key] = {
            "u_hist": u_hist,
            "depth": depth,
            "time": time,
            "total_settlement": total_settlement,
            "final_time_settlement": final_time_settlement,
            "settlement_history": settlement_history,
            "final_time_days": final_time_days,
        }

    if result_key not in st.session_state:
        st.info("Choose parameters and click **Solve 1D model**.")
    else:
        result = st.session_state[result_key]
        u_hist = result["u_hist"]
        depth = result["depth"]
        time = result["time"]
        total_settlement = result["total_settlement"]
        final_time_settlement = result["final_time_settlement"]
        settlement_history = result["settlement_history"]
        final_time_days = result["final_time_days"]

        metric1, metric2, metric3 = st.columns([1, 1, 1])
        metric1.metric("Total settlement", f"{total_settlement:.4f} m")
        metric2.metric(f"Settlement at **{final_time_days}** days", f"{final_time_settlement:.4f} m")

        tab1, tab2, tab3 = st.tabs(["Settlement", "Initial Profile", "Pore Pressure"])

        with tab1:
            fig_settlement = Get_Settlement_Plot_Plotly(settlement_history, time)
            st.plotly_chart(fig_settlement, use_container_width=True)


        with tab2:
            fig_ini = px.line(x = u_hist[:,0], y = depth,
                  title = "Initial pore pressure profile",
                  labels = {
                      'x' : "Initial pore pressure profile",
                      'y' : "Depth (m)"
                  })
            fig_ini.update_layout(height=650)
            st.plotly_chart(fig_ini, use_container_width=True)


        with tab3:
            fig_cons = consolidation_heatmap_plotly(u_hist, time, depth)
            st.plotly_chart(fig_cons, use_container_width=True)


 
