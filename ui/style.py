import streamlit as st

def page_style(page_title :  str):
    st.set_page_config(page_title = page_title, layout = 'wide')
    st.markdown(
        """
        <style>
        div.block-container {
            padding-top: 1.2rem;
            padding-bottom: 1.2rem;
            max-width: 1400px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.35rem;
        }
        .small-note {
            color: #4b5563;
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
