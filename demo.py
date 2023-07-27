import streamlit as st
import streamlit.components.v1 as components

# Adding Image to web app
st.set_page_config(page_title="Nik", page_icon = im ,layout="wide",initial_sidebar_state="auto")
st.title("Nikhil_Dashboard")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


