"""File containing UI configuration constants for the Streamlit app."""

DISPLAY_SYMBOLS = {
    "X": "❌",
    "O": "⭕",
    None: "➖" # This symbol represents an empty cell in the tic tac toe grid 🗆
}

UI_MESSAGES = {
    "page_title": "Tic Tac Toe Game",
    "page_icon": "🎮​",
    "header_title": "🎮​ Tic Tac Toe Game",
    "header_subtitle": "Play the classic Tic Tac Toe game!"
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