"""Main application file for the Tic Tac Toe Streamlit app."""

import streamlit as st
import st_yled as sty

from app_utils import game_exists, is_game_in_progress, refresh_app_rendering, handle_turn
from config.settings import BOARD_SIZE, WIN_LENGTH, SYMBOL_X, SYMBOL_O
from config.ui import HUMAN_PLAYER_NAME, AI_PLAYER_NAME, UI_MESSAGES, CUSTOM_CSS
from core.game_manager import GameManager
from core.player import Player
from core.strategies import HumanStrategy, RandomAIStrategy
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
    handle_turn(game, clicked_cell)

    # Check if game is over to render the end game screen with the result and the option to replay
    if game.is_game_over():
        render_game_over(game)


### Game functions ###
def start_game(human_symbol: str) -> None:
    """
    Initialize the game with 2 players (human and AI) based on the symbol chosen by the user

    Args:
        human_symbol (str): The symbol chosen by the user for the human player.
    """
    ai_symbol = SYMBOL_O if human_symbol == SYMBOL_X else SYMBOL_X

    # Create player instances
    player_1 = Player(HUMAN_PLAYER_NAME, human_symbol, HumanStrategy())
    player_2 = Player(AI_PLAYER_NAME,    ai_symbol,    RandomAIStrategy())

    # X always starts first, _define_starting_player handles this in GameManager
    st.session_state.game = GameManager(player_1, player_2, BOARD_SIZE, WIN_LENGTH)

def should_start_new_game() -> bool:
    """Return True if the conditions to start a new game are met, False otherwise."""
    return st.session_state.options is not None and not is_game_in_progress()


### MAIN APP FUNCTION ###
def main():
    """
    Main function to run the Tic Tac Toe Game Streamlit app.
    """
    # Configure the main page and initialize session state variables
    init_session_state()
    setup_main_page()

    render_side_options(is_game_in_progress())
    render_game_status()

    if should_start_new_game():
        selected_symbol = st.session_state.options["player_symbol"]
        st.session_state.options = None
        start_game(selected_symbol)
        refresh_app_rendering()
        return

    if game_exists():
        render_game()


if __name__ == "__main__":
    main()
