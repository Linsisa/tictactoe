"""Main application file for the Tic Tac Toe Streamlit app."""

import streamlit as st
import st_yled as sty

from config.ui import ui_messages, custom_css


def setup_main_page() -> None:
    """Set up the main page configuration and title for the Streamlit app."""

    st.set_page_config(
        page_title=ui_messages["page_title"],
        page_icon=ui_messages["page_icon"],
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.html(custom_css)  # Apply custom CSS style to the app
    
    sty.title(ui_messages["header_title"], text_alignment="center")
    sty.subheader(ui_messages["header_subtitle"], text_alignment="center", color="#6B7280", font_size="1rem")


def main():
    """
    Main function to run the Tic Tac Toe Game Streamlit app.
    """

    # Initialize st_yled for enhanced styling capabilities
    sty.init()

    setup_main_page()



if __name__ == "__main__":
    main()