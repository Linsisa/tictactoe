"""Main application file for the Tic Tac Toe Streamlit app."""

import streamlit as st
import st_yled as sty

from time import sleep
from config.settings import BOARD_SIZE, WIN_LENGTH, AI_SLEEP_TIME, SYMBOL_X, SYMBOL_O
from config.ui import HUMAN_PLAYER_NAME, AI_PLAYER_NAME, UI_MESSAGES, CUSTOM_CSS
from core.game_manager import GameManager
from core.player import Player
from core.strategies import HumanStrategy, RandomAIStrategy
from ui.board import render_board
from ui.components import render_rules, render_game_over
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
def refresh_app_rendering() -> None:
    """Refresh the Streamlit app rendering to reflect changes in the game state."""
    st.rerun()


def render_current_turn(game: GameManager) -> None:
    """
    Render the current turn information at the top of the game screen.
    
    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if not game.is_game_over():
        st.info(UI_MESSAGES["current_turn"] + f" **{game.get_current_player().name} ({game.get_current_player().symbol})**")


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


### Turn handling functions ###
def handle_turn(game: GameManager, clicked_cell: tuple[int, int] | None) -> None:
    """
    Handle the current turn for both AI and human players based on the game state and user interactions.

    Args:
        game (GameManager): The current game manager instance containing the game state.
        clicked_cell (tuple[int, int] | None): The row and column indices of the cell clicked by the user, or None if no cell was clicked.
    """
    is_ai_turn = game.is_ai_input_allowed()
    
    if is_ai_turn:
        handle_ai_turn(game)
    elif clicked_cell:
        handle_human_turn(game, clicked_cell)


def handle_ai_turn(game: GameManager) -> None:
    """
    Make AI play if it's AI's turn and the game is not over, then refresh the app rendering.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    sleep(AI_SLEEP_TIME)  # Simulate thinking time for the AI
    game.play_turn()  # Make AI play its turn (position is None, AI will choose its move)
    refresh_app_rendering()


def handle_human_turn(game: GameManager, clicked_cell: tuple[int, int]) -> None:
    """
    Handle the human player's turn by playing the move at the clicked cell and refreshing the app rendering.

    Args:        
        game (GameManager): The current game manager instance containing the game state.
        clicked_cell (tuple[int, int]): The row and column indices of the cell clicked by the user.
    """
    game.play_turn(position=clicked_cell)
    refresh_app_rendering()


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


def is_game_in_progress() -> bool:
    """Return True if a game is currently in progress, False otherwise."""
    return game_exists() and not st.session_state.game.is_game_over()


def game_exists() -> bool:
    """Return True if a game exists in session state, False otherwise."""
    return st.session_state.game is not None


def should_start_new_game() -> bool:
    """Return True if the conditions to start a new game are met, False otherwise."""
    return st.session_state.options is not None and not is_game_in_progress()

### MAIN APP FUNCTION ###
def main():
    """
    Main function to run the Tic Tac Toe Game Streamlit app.
    """
    # Configure the main page and initialize session state variables
    setup_main_page()
    init_session_state()

    render_side_options(is_game_in_progress())  

    if should_start_new_game():
        selected_symbol = st.session_state.options["player_symbol"]
        st.session_state.options = None
        start_game(selected_symbol)
        refresh_app_rendering()
        return

    if not game_exists():
        sty.text(UI_MESSAGES["choose_options"],
                font_size="1.25rem", 
                color="#6B7280"
                )
        return
    
    render_game()


if __name__ == "__main__":
    main()
