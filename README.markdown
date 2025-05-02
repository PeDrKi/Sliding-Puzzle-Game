# Sliding Puzzle Game

A classic sliding puzzle game implemented in Python using Pygame. The game allows players to solve puzzles with numbered tiles or custom images, featuring an interactive interface and an A* algorithm for automatic solving.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Limitations](#limitations)
- [License](#license)

## Features
- **Multiple Grid Sizes**: Choose from 3x3, 4x4, or 5x5 grids.
- **Game Modes**:
  - **Number Mode**: Arrange numbered tiles in ascending order.
  - **Image Mode**: Load a custom image and solve the puzzle to restore it.
- **Auto Solve**: Uses the A* algorithm with Manhattan Distance heuristic to find the shortest solution path.
- **User-Friendly Interface**: Pastel-colored buttons with hover effects, error messages, and a stats popup upon winning.
- **Sound and Music**: Tile movement sounds and toggleable background music (requires audio files).
- **Home Screen**: Options to start the game, select grid size, toggle music, view instructions, or exit.
- **Instructions**: A "How to Play" section explaining gameplay and the A* algorithm.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd sliding-puzzle-game
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.6+ installed. Install the required libraries using pip:
   ```bash
   pip install pygame pillow
   ```

3. **Prepare Audio Files** (Optional):
   - Place a `move.wav` file in the `assets/` directory for tile movement sound and background music.
   - If the audio file is missing, the game will run without sound.

4. **Run the Game**:
   ```bash
   python main.py
   ```

## How to Play
1. **Home Screen**:
   - **Start**: Begin the game with the selected grid size.
   - **Size**: Choose a grid size (3x3, 4x4, or 5x5).
   - **How to Play**: View instructions and learn about the A* algorithm.
   - **Music**: Toggle background music on or off.
   - **Exit**: Close the game.

2. **Game Screen**:
   - **Number Mode**: Click tiles next to the empty space to move them and arrange numbers in order (1 to N).
   - **Choose Image**: Load a custom image (JPG or PNG) to play in image mode.
   - **Shuffle**: Randomize the board (ensures a solvable puzzle).
   - **Auto Solve**: Let the A* algorithm solve the puzzle automatically.
   - **Pause**: Pause auto-solving to take manual control.
   - **Exit**: Return to the home screen.
   - **Winning**: When the puzzle is solved, a stats popup shows the number of moves, A* steps, nodes expanded, and time taken.

3. **Tips**:
   - Smaller grids (3x3, 4x4) are easier for beginners.
   - Use "Pause" during auto-solving to make manual moves.
   - Ensure images are clear and appropriately sized for better visibility.

## Project Structure
```
sliding-puzzle-game/
├── assets/
│   └── move.wav           # Audio file for tile movement and background music
├── main.py                # Main entry point, initializes Pygame and game loop
├── constants.py           # Constants for window size, colors, fonts, and sounds
├── utils.py               # Utility functions for image loading, board shuffling, and solvability checks
├── puzzle_game.py         # Core game logic, handles board state and user interactions
├── ui.py                  # UI rendering for board, buttons, and stats popup
├── solver.py              # A* algorithm implementation for auto-solving
├── home.py                # Home screen with start, size, music, and instruction options
└── README.md              # Project documentation
```

## Dependencies
- **Python 3.6+**
- **Pygame**: For game rendering and event handling.
- **Pillow (PIL)**: For image processing in image mode.
- **tkinter**: For file dialog in image selection (included with standard Python).

Install dependencies:
```bash
pip install pygame pillow
```

## Limitations
- **Grid Size**: Limited to 3x3, 4x4, and 5x5 due to performance considerations with the A* algorithm.
- **Audio**: Requires a `move.wav` file in `assets/`; otherwise, sound and music are disabled.
- **Image Mode**: Large images or high-resolution images may slow down loading or rendering.
- **No Save Feature**: Game state is not saved between sessions.

Please ensure your code follows the existing style and includes appropriate comments.

## License
This project is made by Perfect Dragon King (PDK). If you have any problem related to the project, please contact email: 
- [Email me](mailto:pdkhue2004@gmail.com)
- [Call me] (tel:+84867758620)
