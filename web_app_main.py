
import streamlit as st
from web_app import web_app_intro, next_steps, intro, Data_exploration, ml_framework

st.sidebar.markdown(
"""
# Control Panel
"""
)
PAGES = {
    "Prediction": web_app_intro,
    "Introduction" : intro,
    "Data exploration" : Data_exploration,
    "Machine learning framework" :ml_framework,
    "next step" : next_steps
}
selection = st.sidebar.radio("Navigation", list(PAGES.keys()))
page = PAGES[selection]
page.app()

st.sidebar.title("Team members")
st.sidebar.markdown('''
- [Jithin Madhusudanan Sreekala](https://www.linkedin.com/in/jithinms)
- [Shashank Markande](https://www.linkedin.com/in/smarkande)
- [Andrew McMillan](https://www.linkedin.com/in/andrew-mcmillan-68983b96)
- [Yossathorn (Josh) Tawabutr](https://www.linkedin.com/in/yossathorn-tawabutr)

''')