import os
import streamlit as st

def input_form():
    form = st.form("agent_form")
    
    st.session_state.instructions = form.text_area(
        "Enter your instructions", height=100
    )

    st.session_state.show_thinking_process = form.toggle(
        "Show thinking process", value=True
    )
    form.form_submit_button("Submit", type="primary")
