"""File containing UI configuration constants for the Streamlit app."""

BOARDS_SYMBOLS = {
    "X": "❌",
    "O": "⭕",
    None: "➖" # This symbol represents an empty cell in the tic tac toe grid 🗆
}

ICONS = {
    "victory": "🏆",
    "draw": "🤝",
}

HUMAN_PLAYER_NAME = "You"
AI_PLAYER_NAME = "Computer"

UI_MESSAGES = {
    "page_title": "Tic Tac Toe Game",
    "page_icon": "🎮​",
    "header_title": "🎮​ Tic Tac Toe Game",
    "header_subtitle": "Play the classic Tic Tac Toe game!",
    "choose_symbol": "Choose your symbol to start the game:",
    "current_turn": "Current turn:",
}

CUSTOM_CSS = \
    """<style>
        /* Custom CSS to style the Streamlit app */
        .stMainBlockContainer {
            max-width: 150rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>"""
