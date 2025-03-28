import os
from loguru import logger
import streamlit as st
from ui.constants import CURRENT_VERSION


def header():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(parent_dir, "..", "static")
    logger.info(f"Static directory: {static_dir}")
    col1, col2, col3, _ = st.columns([3, 1, 3, 5])
    col1.image(os.path.join(static_dir, "cai_logo.png"))
    col2.markdown("## ×")
    col3.image(os.path.join(static_dir, "netnam_logo.png"))

    st.markdown(
        f"<h1>Deep Research Agent <small>{CURRENT_VERSION}</small></h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        Deep Research Agent is an AI agent that uses multiple specialized agents to research any topic. It gathers info from the web, academic sources, and news, then analyzes and summarizes it into a final report. Perfect for anyone needing thorough research quickly.
        """
    )

    st.divider()
