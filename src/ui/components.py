"""File of the UI components for the Tic Tac Toe game, including the main game window"""

import streamlit as st

from config.settings import SYMBOL_X, SYMBOL_O
from config.ui import BOARD_SYMBOLS, ICONS, UI_MESSAGES, GAME_RULES
from core.game_manager import GameManager


### RULES RENDERING ###
def render_rules() -> None:
    """
    Render the game rules in a expander on the main page of the application, allowing users to understand how to play the game and what the rules are.
    """
    with st.expander(UI_MESSAGES["rules_expander"]):
        st.text(GAME_RULES.format(BOARD_SYMBOLS[SYMBOL_X], BOARD_SYMBOLS[SYMBOL_O], BOARD_SYMBOLS[SYMBOL_X]))


### SIDEBAR OPTIONS RENDERING ###
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


### BOARD RENDERING ###
def render_board(game: GameManager) -> tuple[int, int] | None:
    """
    Render the game board using Streamlit.
    
    Args:
        game (GameManager): The current game manager instance containing the game state.
        
    Returns:
        tuple[int, int] | None: The position of the cell clicked by the user,
        or None if no cell was clicked.
    """
    board_state = game.get_current_board_state()
    num_columns = len(board_state[0]) if board_state else 0
    disable_cells = _disable_buttons(game)
    
    # Create colomns for centering the board, with dynamic padding based on the number of columns in the board
    _, col_centre, _ = st.columns(_get_layout_portion_for_columns(num_columns))

    with col_centre:
        return _render_board_grid(board_state, disable_cells)


def _disable_buttons(game: GameManager) -> bool:
    """
    Determine whether the buttons on the game board should be disabled based on the current game state.

    Args:
        game (GameManager): The current game manager instance containing the game state.

    Returns:
        bool: A boolean indicating whether the buttons should be disabled.
    """
    return not game.is_human_input_allowed()


def _get_layout_portion_for_columns(num_columns: int) -> tuple[int, int]:
    """
    Calculate the layout portion for the display based on the number of columns in the board.

    Args:
        num_columns (int): The number of columns in the game board.


    Returns:
        tuple[int, int]: A tuple containing the layout portion for the center column and the padding.
    """
    max_padding = 12
    padding = max(1, max_padding - num_columns)  # Adjust padding based on the number of columns
    return [padding, num_columns, padding]


def _render_board_grid(board: "Board", disable_cells: bool) -> tuple[int, int] | None:
    """
    Render the game board as a grid of buttons.

    Args:
        board (list[list[str | None]]): The current state of the game board.
        disable_cells (bool): A boolean indicating whether the cells should be disabled.
    """
    clicked_cell = None

    st.html("<div class='tictactoe-board'>")  # Add a wrapper div with a specific class for styling
    for row_idx, row in enumerate(board):
        cols = st.columns(len(row))  # Create columns for each cell in the row

        for col_idx, cell in enumerate(row):
            cell_value = BOARD_SYMBOLS.get(cell)  # Display the UI symbol based on the board value

            with cols[col_idx]:
                if st.button(
                        label=cell_value,
                        key=f"cell_{row_idx}_{col_idx}",
                        disabled=disable_cells,
                        width="stretch",
                        use_container_width=True
                    ):
                        clicked_cell = (row_idx, col_idx)
    st.html("</div>")

    return clicked_cell


### GAME OVER SECTION RENDERING ###
def render_game_over(game: GameManager) -> None:
    """
    Render the end game screen with the result of the game and the option to replay.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if game.is_winner():
        success_message = UI_MESSAGES["victory"].format(game.get_winner().name, game.get_winner().symbol)
        st.success(success_message, icon=ICONS["victory"])
    else:
        st.info(UI_MESSAGES["draw"], icon=ICONS["draw"])

    if st.button(UI_MESSAGES["quick_restart"]):
        game.reset_game()
        st.rerun()
