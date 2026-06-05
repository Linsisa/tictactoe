"""File of the UI components for the Tic Tac Toe game, including the main game window"""

import streamlit as st

from config.ui import BOARD_SYMBOLS, ICONS, UI_MESSAGES, GAME_RULES
from config.settings import SYMBOL_X, SYMBOL_O
from core.game_manager import GameManager


### RULES RENDERING
def render_rules() -> None:
    """
    Render the game rules in a expander on the main page of the application, allowing users to understand how to play the game and what the rules are.
    """
    with st.expander(UI_MESSAGES["rules_expander"]):
        st.text(GAME_RULES.format(BOARD_SYMBOLS[SYMBOL_X], BOARD_SYMBOLS[SYMBOL_O], BOARD_SYMBOLS[SYMBOL_X]))


### SIDEBAR OPTIONS RENDERING
def render_side_options(game_in_progress: bool) -> None:
    """
    Render the game options for the user to select game options by registering in session state.

    Args:
        game_in_progress (bool): A boolean indicating whether a game is in progress.
    """

    with st.sidebar:
        st.sidebar.title(UI_MESSAGES["options_title"])

        st.subheader(UI_MESSAGES["symbol_options"])
        player_symbol = st.sidebar.selectbox(
            label=UI_MESSAGES["choose_symbol"],
            key="player_symbol",
            options=[BOARD_SYMBOLS[SYMBOL_X], BOARD_SYMBOLS[SYMBOL_O]],
            disabled=game_in_progress
        )
        st.text(UI_MESSAGES["symbol_info"].format(BOARD_SYMBOLS[SYMBOL_X]))

        st.divider()
        if st.button(
            label=UI_MESSAGES["launch"],
            key="launch_button",
            disabled=game_in_progress
        ):
            player_symbol = SYMBOL_X if player_symbol == BOARD_SYMBOLS[SYMBOL_X] else SYMBOL_O
            st.session_state.options = {
                "player_symbol": player_symbol
            }


### BOARD RENDERING
def render_board(game: GameManager) -> tuple[int, int] | None:
    """
    Render the game board using Streamlit.
    
    Args:
        game (GameManager): The current game manager instance containing the game state.
        
    Returns:
        tuple[int, int] | None: The position of the cell clicked by the user,
        or None if no cell was clicked.
    """
    disable_cells = _disable_buttons(game)
    
    # Create colomns for centering the board, with dynamic padding based on the number of columns in the board
    _, col_centre, _ = st.columns(_get_layout_portion_for_columns(game))

    with col_centre:
        return _render_board_grid(game, disable_cells)


def _disable_buttons(game: GameManager) -> bool:
    """
    Determine whether the buttons on the game board should be disabled based on the current game state.

    Args:
        game (GameManager): The current game manager instance containing the game state.

    Returns:
        bool: A boolean indicating whether the buttons should be disabled.
    """
    is_human_turn = game.is_current_player_human()
    return game.game_over or not is_human_turn


def _get_layout_portion_for_columns(game: GameManager) -> tuple[int, int]:
    """
    Calculate the layout portion for the display based on the number of columns in the board.

    Args:
        game (GameManager): The current game manager instance containing the game state.

    Returns:
        tuple[int, int]: A tuple containing the layout portion for the center column and the padding.
    """
    col_num = len(game.get_current_board_state()[0]) if game.get_current_board_state() else 0
    padding = max(1, 8 - col_num)  # Adjust padding based on the number of columns
    return [padding, col_num, padding]


def _render_board_grid(game: GameManager, disable_cells: bool) -> None:
    """
    Render the game board as a grid of buttons.

    Args:
        game (GameManager): The current game manager instance containing the game state.
        disable_cells (bool): A boolean indicating whether the cells should be disabled.
    """
    board = game.get_current_board_state()
    row_num = len(board)
    col_num = len(board[0]) if board else 0

    clicked_cell = None
    st.html("<div class='tictactoe-board'>")  # Add a wrapper div with a specific class for styling
    for row in range(row_num):
        cols = st.columns(col_num) 

        for col in range(col_num):
            cell_value = BOARD_SYMBOLS.get(board[row][col])  # Display the UI symbol based on the board value
            
            with cols[col]:
                if st.button(
                        label=cell_value if cell_value else " ",
                        key=f"cell_{row}_{col}",
                        disabled=disable_cells,
                        use_container_width=True
                    ):
                        clicked_cell = (row, col)
    st.html("</div>")

    return clicked_cell


## GAME OVER SECTION RENDERING
def render_game_over(game: GameManager) -> None:
    """
    Render the end game screen with the result of the game and the option to replay.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if game.winner:
        success_message = UI_MESSAGES["victory"].format(game.winner.name, game.winner.symbol)
        st.success(success_message, icon=ICONS["victory"])
    else:
        st.info(UI_MESSAGES["draw"], icon=ICONS["draw"])

    if st.button(UI_MESSAGES["quick_restart"]):
        game.reset_game()
        st.rerun()
