# The next 3 lines are here for compatibility with the Streamlit Cloud platform
import sys

if sys.platform.startswith("linux"):
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import streamlit as st
from ui.sections.metadata import metadata
from ui.sections.header import header
from ui.sections.input_form import input_form
from ui.sections.response import response
from ui.sections.footer import footer
from ui.sections.sidebar import sidebar


metadata()
header()
# sidebar()
input_form()

if st.session_state.instructions and st.session_state.llm_id:
    with st.spinner("Processing...", show_time=True):
        response()

footer()
