from loguru import logger
import streamlit as st
from ui.constants import DEFAULT_SESSION_STATE
import os


def metadata():
    st.set_page_config(
        page_title="Deep Research Agent",
        page_icon="🤖",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    # logger.info(f"Current working directory: {os.getcwd()}")
    # logger.info(f"Current file location: {os.path.abspath(__file__)}")
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(parent_dir, "..", "static")
    logger.info(f"Static directory: {static_dir}")

    with open(os.path.join(static_dir, "style.css")) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    st.session_state.update(DEFAULT_SESSION_STATE)
