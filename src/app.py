"""Main application file for the Tic Tac Toe Streamlit app."""

import streamlit as st
import st_yled as sty

import app_utils as app_utils
from config.ui import UI_MESSAGES, CUSTOM_CSS
from core.game_manager import GameManager
from ui.board import render_board
from ui.components import render_rules, render_game_status, render_current_turn, render_game_over
from ui.sidebar import render_side_options


### Setup functions ###
def setup_main_page() -> None:
    """Set up the main page configuration and title for the Streamlit app."""
    st.set_page_config(
        page_title=UI_MESSAGES["page_title"],
        page_icon=UI_MESSAGES["page_icon"],
        layout="wide",
        initial_sidebar_state="auto",
    )

    sty.init()  # Initialize st_yled for enhanced styling capabilities
    st.html(CUSTOM_CSS)  # Apply custom CSS style to the app
    
    sty.title(UI_MESSAGES["header_title"])
    sty.subheader(UI_MESSAGES["header_subtitle"], color="#6B7280", font_size="1rem")

    render_rules()  # Render the game rules expander at the top of the page
    st.markdown("---")  # Add a horizontal divider after the header section

def init_session_state() -> None:
    """
    Initialize the Streamlit session state variables for the game.
    This function ensures that the necessary session state variables are set up before the game starts.
    Keeps track of the game manager instance and the human player's chosen symbol.
    """
    if "game" not in st.session_state:
        st.session_state.game = None
    if "options" not in st.session_state:
        st.session_state.options = None


### Rendering functions ###
def render_game() -> None:
    """
    Render the main game screen, including the current turn,
    the game board, and handle the game logic for both human and AI turns.
    Also handles the end game screen when the game is over.
    """
    # Get the current game manager instance from session state
    game: GameManager = st.session_state.game

    # Display the current turn information at the top of the game screen
    render_current_turn(game)

    # Render the game board and get the position of the cell clicked by the user (if any)
    clicked_cell = render_board(game)
    app_utils.handle_turn(game, clicked_cell)

    # Check if game is over to render the end game screen with the result and the option to replay
    if game.is_game_over():
        render_game_over(game)


### MAIN APP FUNCTION ###
def main():
    """
    Main function to run the Tic Tac Toe Game Streamlit app.
    """
    # Configure the main page and initialize session state variables
    init_session_state()
    setup_main_page()

    render_side_options(app_utils.is_game_in_progress())
    render_game_status()

    if app_utils.should_start_new_game():
        selected_symbol = st.session_state.options["player_symbol"]
        st.session_state.options = None
        app_utils.create_game(selected_symbol)
        app_utils.refresh_app_rendering()
        return

    if app_utils.game_exists():
        render_game()


if __name__ == "__main__":
    main()
