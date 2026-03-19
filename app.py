import streamlit as st
from ui.style import page_style

page_style('Geotechnical Consolidation FEM')
st.title("Geotechnical Consolidation FEM")
st.write("""
    This dashboard solves geotechnical consolidation problems using
    the finite element method (FEM). It includes 1D single-layer,
    1D multilayer, and 2D multilayer models for analysing excess pore pressure
    dissipation and settlement under different soil conditions.
    """)

st.subheader("Current available models")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    ### 1D Single-layer
    - Homogeneous soil profile
    - Useful for verification and baseline studies
    - Tracks pore pressure and settlement with time
    """)
with col2:
    st.markdown("""
    ### 1D Multilayer
    - Layered soil profile
    - Different `Cv` and `Mv` per layer
    - Useful for realistic ground conditions
    """)
with col3:
    st.markdown("""
    ### 2D Model
    - Spatial settlement and pore pressure response
    - Includes mesh-based FEM behaviour
    - Useful for non-uniform geometry and loading
    """)

st.write('Notes:')
st.caption("""
- All models have been assumed to have a impermeable base.
- The models only currently account for boussinesq initial strip conditions
""")

st.divider()
st.subheader("How to use")
st.markdown("""
1. Open the sidebar and choose a model page  
2. Enter soil, geometry, and time parameters  
3. Run the model  
4. Review settlement curves, pore pressure plots, and output summaries  
""")

st.subheader("Notes")
st.info(
    """
    - Ensure units are consistent across all inputs
    - Multilayer models require matching layer depths and parameter lists
    - The 2D model may take longer to solve for finer meshes
    """
)

