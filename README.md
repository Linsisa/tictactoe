# 🎮 Tic Tac Toe

🚀 **Live Demo** : Try it now on **streamlit cloud**: [tictactoe](https://tictactoe-linsisa.streamlit.app/)

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [License](#license)


## About

**Tic Tac Toe** is a Python implementation of the classic game with a Streamlit web interface.
The game includes a simple AI opponent based on a random strategy, allowing players to enjoy a quick match against the computer.  

The architecture of the project is designed to separate game logic from the user interface, making it easy to maintain and extend in the future.

## Features
### 🎮 Interactive Web Interface
- **Interactive Gameplay**: Real-time updates through a web interface.

### 🤖 AI Opponent
- **Random AI Strategy**: Simple AI that makes random valid moves, providing a basic challenge for players.

### ⚙️ Game Configuration
- **Symbol Selection**: Choose player symbol (X / O) before starting.
- **Board Size**: Game logic supports different board sizes (currently 3x3, but easily extendable).
- **Win Length**: Configurable win length (number of aligned symbols required to win).

### 🕒 Game Flow
- **Restart Game**: Ability to restart the game without refreshing the page.
- **Quick Restart**: Button (↻ Quick Restart) to quickly reset the game state and start a new match.

### ✅ Testing
- **Unit Tests**: Basic unit tests for core project components (board, game_manager, player, rules, strategies).

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit 1.58.0 |
| **Python** | 3.12+ |

See [requirements.txt](requirements.txt) for the complete dependency list.

## Installation & Setup

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Linsisa/tictactoe.git
   cd tictactoe
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

### Run App Locally

From the root directory of the project, run the following command to start the Streamlit app:

```bash
streamlit run src/app.py
```

The app will open at `http://localhost:8501` in your browser.

### Using the App

1. **Select a Symbol**
    - Choose your symbol in the sidebar to start the game. The computer will play with the opposite symbol.

2. **Play the Game**
    - Click on the *Launch game* button in the sidebar to start a new game.  
    - The game board will appear. Click a cell on the grid, the computer will automatically make its move after yours. 
    - The game continues until there is a winner or a draw.

3. **Restart Game**
    - When the game is over, click on the *Quick Restart* button below the game result to reset the game state and start a new match with the same parameters.
    - Alternatively, you can change the symbol selection and click *Launch game* again to start a new game with different settings.


---
### Run live version on Streamlit Cloud

A live version of the app is available on Streamlit Cloud. Click the link below to explore the features without any setup.  

[Try the Live Demo](https://tictactoe-linsisa.streamlit.app/)

### Run Tests
To run the unit tests for the project, use the following command from the root directory:

```bash
pytest tests -v
```


## Project Structure

```
tictactoe/
├── src/
│   ├── app.py                         # Main Streamlit entry point
│   ├── config/
│   │   ├── settings.py                # Application settings
│   │   ├── test_settings.py           # Test settings
│   │   └── ui.py                      # UI configuration
│   ├── core/
│   │   ├── board.py                   # Game Board implementation
│   │   ├── game_manager.py            # Main game logic
│   │   ├── player.py                  # Player implementation
│   │   ├── rules.py                   # Tic Tac Toe rules and win conditions
│   │   └── strategies.py              # Different player strategies (e.g., random AI)
│   └── ui/
│       └── components.py              # Streamlit UI components (game board, sidebar, etc.)
├── tests/
│   ├── test_board.py                  # Unit tests for board logic
│   ├── test_game_manager.py           # Unit tests for game flow and state management
│   ├── test_player.py                 # Unit tests for player class
│   ├── test_rules.py                  # Unit tests for tic tac toe rules and win conditions    
│   └── test_strategies.py             # Unit tests for players strategies (e.g., random AI)   
├── .gitignore                         # Git ignore rules
├── LICENSE                            # License information
├── pyproject.toml                     # Python project configuration
├── README.md                          # This file
├── requirements.in                    # Dependency specifications
└── requirements.txt                   # Python dependencies
```

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.


## Acknowledgments

Built with [Streamlit](https://streamlit.io/).