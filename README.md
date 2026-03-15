# Snake Game — Python / TKinter

A classic Snake game built in Python using TKinter for the GUI.

## How to Run

```bash
python snake_gui.py
```

No external libraries required — uses Python's built-in `tkinter` module only.

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move the snake |
| R | Restart after game over |
| Q / Escape | Quit |

## Files

| File | Description |
|---|---|
| `snake_gui.py` | Main game with TKinter GUI |
| `snake.py` | Core game logic (movement, collision detection) |
| `score.py` | Score calculation and high score persistence |
| `highscore.txt` | Auto-created — stores your best score |

## Features

- Smooth TKinter GUI with animated snake
- Speed increases as you eat more food
- Persistent high score saved between sessions
- Snake eyes that follow direction of movement
- Clean restart without relaunching

## Requirements

- Python 3.10+
- No third-party packages needed
