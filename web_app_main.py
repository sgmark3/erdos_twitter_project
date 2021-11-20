import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import norm
import streamlit as st
from web_app import web_app_intro, next_steps

st.sidebar.markdown(
"""
# Control Panel
"""
)
PAGES = {
    "Introduction": web_app_intro,
    "next step" : next_steps
}
selection = st.sidebar.radio("Navigation", list(PAGES.keys()))
page = PAGES[selection]
page.app()