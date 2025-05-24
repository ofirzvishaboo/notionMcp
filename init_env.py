import os
import torch
import asyncio
import streamlit as st

def init_environment():
    """Initialize the environment for the application."""
    # Set PyTorch to use CPU
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

    # Configure Streamlit
    st.set_page_config(
        page_title="Notion Learning Assistant",
        page_icon="📚",
        layout="wide"
    )

    # Initialize event loop if needed
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

if __name__ == "__main__":
    init_environment()