import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.geotech_consolidation.models.terzaghi_1d.fem import Get_terzaghi1D_FEA
from src.plotting.terzaghi_1d.plot import Get_Settlement_Plot


# setting up Page config for streamlit 
st.set_page_config(layout ="wide")
st.title("1D terzaghi Consolidation Theory")


# pre text within 
st.subheader("Single-layer consolidation (Finite Element Analysis)")
st.write(
    "This dashboard solves 1D Terzaghi consolidation using the finite element method (FEM). "
    " Choose the parameter and numerical settings, then click **Solve** to compute excess pore pressure"
    " dissipation over and settlement over time. The initial excess pore pressure can be set to uniform "
    " (constant with depth) or a non-uniform (Boussinesq).")




col1, col2 = st.columns([3.5,1])
with col2: 
    H = st.number_input("depth (m)", value=5.0)  # in meters
    num = st.number_input("number of elements", value=100)
    P = st.number_input("Load applied (kPa)", value=100.0) 
    Tx = st.number_input("Final time (days)", value= 365.0)
    Tx = Tx*60*60*24
    time_step = st.number_input("time step", value=1000)
    Cv = st.number_input("Cv (1e-7)", value=2)
    Cv = 1e-7 * Cv 
    Mv = st.number_input("Mv (1e-4) (m^2/kN)", value=5)
    Mv = Mv*1e-4
    initial_conditions = st.toggle("Use uniform initial condition (U0)", value=False) 
    base = st.number_input("base of load placed (m)", value =2.5)

nodes = num + 1
Z = -np.linspace(0, H, num=nodes)


with col1:
    if st.button("Solve"):
        settlement_history, fem_udata_raw, settlement = Get_terzaghi1D_FEA(
            H,
            num,
            P,
            Tx,
            time_step,
            Cv,
            base,
            Mv,
            initial_conditions,
        )
            
        fem_udata = fem_udata_raw.T
        initial_pressure = fem_udata[:, 0]
        time_days = Tx / (60 * 60 * 24)
        time = np.linspace(0, time_days, num=time_step)
        total_settlement = np.sum(settlement)

        # plotting initial condition
        st.subheader("Initial Condition (FEM)")
        st.write(
            "Initial excess pore pressure profile at *t* = 0 computed by the FEM solver "
            "for the selected load and initial condition."
        )
        fig_ini, ax_ini = plt.subplots(figsize=(8, 5))
        ax_ini.plot(initial_pressure, Z, label="FEM initial condition")
        ax_ini.set_xlabel("Depths (z)")
        ax_ini.set_ylabel("Initial excess pore pressure, (u0 kPa)")
        ax_ini.legend()
        plt.title("Initial Conditions (U0) over depth (z)")
        st.pyplot(fig_ini)

        # plotting end settlement
        st.subheader("Settlement response (FEM)")
        st.write(
            "Settlement is computed from the FEM pore pressure and plotted"
            " over the selected time for the chosen initial condition."
        )
        fig_settl, ax = Get_Settlement_Plot(settlement_history, time)
        ax.set_ylim(-total_settlement, 0)
        st.pyplot(fig_settl)

        st.write(f"Total consolidation settlement: {total_settlement:.4f} m")
        st.write(f"Settlement after {time_days:.1f} days: {settlement_history[-1]:.4f} m")

        # plotting excess pore pressure heat map
        st.subheader("Excess Pore pressure dissipation (depth time map)")
        st.write("Heatmap of Pore pressure dissipation through time and depth")
        fig_cons, ax_cons = plt.subplots(figsize=(8, 5))
        kx = max(1, len(time) // 10)    # ~8 labels across, auto
        ky = max(1, len(Z) // 10)  # ~10 labels down, auto 
        ax_cons = sns.heatmap(
            fem_udata,
            annot=False,
            cmap="Blues",
            xticklabels=time,
            yticklabels=Z,
        )
        ax_cons.set_xticks(np.arange(0, len(time), kx) + 0.5)
        ax_cons.set_xticklabels(
            [f"{time[i]:.1f}" for i in range(0, len(time), kx)],
            rotation=0,
        )
        ax_cons.set_yticks(np.arange(0, len(Z), ky) + 0.5)
        ax_cons.set_yticklabels(
            [f"{Z[i]:.1f}" for i in range(0, len(Z), ky)],
            rotation=0,
        )
        ax_cons.set_xlabel("Time (Days)")
        ax_cons.set_ylabel("Depth (m)")
        ax_cons.set_title("Excess Pore Pressure dissipation over time in a 1D Mesh")
        st.pyplot(fig_cons)
