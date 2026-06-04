"""File containing UI configuration constants for the Streamlit app."""

BOARD_SYMBOLS = {
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
    "choose_options": "Choose options in the sidebar to launch the game",
    "choose_symbol": "Choose your symbol:",
    "symbol_options": "Symbol options:",
    "current_turn": "Current turn:",
    "draw": "It's a draw!",
    "victory": "{} wins! Symbol: {}",
    "launch": "Launch Game",
    "quick_restart": "↻ Quick Restart",
    "options_title": "⚙️ Game Options"
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
