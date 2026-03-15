"""
snake_gui.py - Snake Game with TKinter GUI
==========================================
A fully playable Snake game with graphical interface.

Controls:
    Arrow keys  - Move the snake
    R           - Restart after game over
    Q / Escape  - Quit

Run with:
    python snake_gui.py
"""

import tkinter as tk
import random
from score import load_high_score, save_high_score, calculate_score

# ---------------------------------------------------------------------------
# Game configuration constants
# ---------------------------------------------------------------------------
CELL_SIZE    = 28          # Pixels per grid cell
GRID_W       = 20          # Grid columns
GRID_H       = 20          # Grid rows
CANVAS_W     = CELL_SIZE * GRID_W
CANVAS_H     = CELL_SIZE * GRID_H
INITIAL_DELAY = 140        # Milliseconds between ticks (lower = faster)
SPEED_INCREMENT = 3        # Ms to reduce delay per food eaten
MIN_DELAY    = 60          # Fastest possible speed

# Colours
BG_COLOUR       = '#1a1a2e'
GRID_COLOUR     = '#16213e'
SNAKE_HEAD      = '#00d4aa'
SNAKE_BODY      = '#00a884'
FOOD_COLOUR     = '#ff6b6b'
TEXT_COLOUR     = '#e0e0e0'
SCORE_BG        = '#0f3460'
OVERLAY_BG      = '#000000'
GAMEOVER_COLOUR = '#ff6b6b'
WIN_COLOUR      = '#00d4aa'

# Direction vectors
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


# ---------------------------------------------------------------------------
# Main application class
# ---------------------------------------------------------------------------

class SnakeGame(tk.Tk):
    """Root Tk window that hosts the entire Snake game."""

    def __init__(self) -> None:
        super().__init__()
        self.title('Snake — Keele Edition')
        self.resizable(False, False)
        self.configure(bg=BG_COLOUR)

        self._build_ui()
        self._centre_window()
        self.bind('<KeyPress>', self._on_key)

        self._init_game()
        self._tick()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Create all widgets."""
        # Score bar
        score_bar = tk.Frame(self, bg=SCORE_BG, pady=6)
        score_bar.pack(fill='x')

        self.score_var = tk.StringVar(value='Score: 0')
        tk.Label(score_bar, textvariable=self.score_var,
                 font=('Segoe UI', 11, 'bold'),
                 bg=SCORE_BG, fg=TEXT_COLOUR).pack(side='left', padx=14)

        self.high_var = tk.StringVar(value=f'Best: {load_high_score()}')
        tk.Label(score_bar, textvariable=self.high_var,
                 font=('Segoe UI', 11),
                 bg=SCORE_BG, fg='#a0b4c8').pack(side='right', padx=14)

        # Game canvas
        self.canvas = tk.Canvas(
            self, width=CANVAS_W, height=CANVAS_H,
            bg=BG_COLOUR, highlightthickness=0,
        )
        self.canvas.pack()

        # Status bar
        status_bar = tk.Frame(self, bg='#0a0a1a', pady=4)
        status_bar.pack(fill='x')
        tk.Label(status_bar,
                 text='Arrow keys: move   R: restart   Q / Esc: quit',
                 font=('Segoe UI', 8), bg='#0a0a1a', fg='#555577').pack()

    # ------------------------------------------------------------------
    # Game initialisation
    # ------------------------------------------------------------------

    def _init_game(self) -> None:
        """Reset all game state for a new game."""
        mid_x = GRID_W // 2
        mid_y = GRID_H // 2
        # Snake starts as 3 segments moving right
        self.snake     = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = RIGHT
        self.next_dir  = RIGHT
        self.food      = self._place_food()
        self.alive     = True
        self.delay     = INITIAL_DELAY
        self.score_var.set('Score: 0')
        self._after_id = None

    def _place_food(self) -> tuple[int, int]:
        """Return a random grid position not occupied by the snake."""
        while True:
            pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
            if pos not in self.snake:
                return pos

    # ------------------------------------------------------------------
    # Game loop
    # ------------------------------------------------------------------

    def _tick(self) -> None:
        """Advance the game by one frame."""
        if self.alive:
            self._update()
        self._draw()
        self._after_id = self.after(self.delay, self._tick)

    def _update(self) -> None:
        """Update game state: move snake, check collisions, handle food."""
        # Apply direction (cannot reverse)
        if self.next_dir != OPPOSITE.get(self.direction):
            self.direction = self.next_dir

        dx, dy = self.direction
        hx, hy = self.snake[0]
        new_head = (hx + dx, hy + dy)

        # Wall collision
        if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            self._game_over()
            return

        # Self collision
        if new_head in self.snake:
            self._game_over()
            return

        # Move snake
        self.snake = [new_head] + self.snake[:-1]

        # Food collision
        if new_head == self.food:
            self.snake.append(self.snake[-1])   # Grow
            self.food = self._place_food()
            # Update score
            score = calculate_score(len(self.snake))
            self.score_var.set(f'Score: {score}')
            # Speed up
            self.delay = max(MIN_DELAY, self.delay - SPEED_INCREMENT)

    def _game_over(self) -> None:
        """Handle end-of-game: save high score, show overlay."""
        self.alive = False
        score = calculate_score(len(self.snake))
        save_high_score(score)
        self.high_var.set(f'Best: {load_high_score()}')

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _draw(self) -> None:
        """Redraw the entire canvas."""
        self.canvas.delete('all')
        self._draw_grid()
        self._draw_food()
        self._draw_snake()
        if not self.alive:
            self._draw_game_over_overlay()

    def _draw_grid(self) -> None:
        """Draw faint grid lines."""
        for x in range(0, CANVAS_W, CELL_SIZE):
            self.canvas.create_line(x, 0, x, CANVAS_H, fill=GRID_COLOUR)
        for y in range(0, CANVAS_H, CELL_SIZE):
            self.canvas.create_line(0, y, CANVAS_W, y, fill=GRID_COLOUR)

    def _draw_snake(self) -> None:
        """Draw every segment of the snake."""
        for i, (cx, cy) in enumerate(self.snake):
            x1 = cx * CELL_SIZE + 2
            y1 = cy * CELL_SIZE + 2
            x2 = x1 + CELL_SIZE - 4
            y2 = y1 + CELL_SIZE - 4
            colour = SNAKE_HEAD if i == 0 else SNAKE_BODY
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=colour, outline='', width=0,
            )
            # Draw eyes on the head
            if i == 0:
                self._draw_eyes(cx, cy)

    def _draw_eyes(self, cx: int, cy: int) -> None:
        """Draw two small eyes on the snake's head.

        Args:
            cx: Grid column of the head.
            cy: Grid row of the head.
        """
        base_x = cx * CELL_SIZE
        base_y = cy * CELL_SIZE
        size = 4
        offsets = {
            RIGHT: [(18, 6),  (18, 16)],
            LEFT:  [(6,  6),  (6,  16)],
            UP:    [(6,  6),  (16, 6)],
            DOWN:  [(6,  18), (16, 18)],
        }
        for ox, oy in offsets.get(self.direction, [(18, 6), (18, 16)]):
            x, y = base_x + ox, base_y + oy
            self.canvas.create_oval(x, y, x + size, y + size,
                                    fill=BG_COLOUR, outline='')

    def _draw_food(self) -> None:
        """Draw the food as a circle."""
        fx, fy = self.food
        x1 = fx * CELL_SIZE + 4
        y1 = fy * CELL_SIZE + 4
        x2 = x1 + CELL_SIZE - 8
        y2 = y1 + CELL_SIZE - 8
        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=FOOD_COLOUR, outline='#ff4444', width=1)

    def _draw_game_over_overlay(self) -> None:
        """Draw a semi-transparent game-over overlay with instructions."""
        # Dim overlay
        self.canvas.create_rectangle(
            0, 0, CANVAS_W, CANVAS_H,
            fill=OVERLAY_BG, stipple='gray50', outline='',
        )
        score = calculate_score(len(self.snake))
        # Game over text
        self.canvas.create_text(
            CANVAS_W // 2, CANVAS_H // 2 - 40,
            text='GAME OVER', font=('Segoe UI', 26, 'bold'),
            fill=GAMEOVER_COLOUR,
        )
        self.canvas.create_text(
            CANVAS_W // 2, CANVAS_H // 2,
            text=f'Score: {score}', font=('Segoe UI', 16),
            fill=TEXT_COLOUR,
        )
        self.canvas.create_text(
            CANVAS_W // 2, CANVAS_H // 2 + 36,
            text='Press R to restart', font=('Segoe UI', 12),
            fill='#a0b4c8',
        )

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------

    def _on_key(self, event: tk.Event) -> None:
        """Handle keyboard input.

        Args:
            event: Tkinter key event.
        """
        key = event.keysym
        direction_map = {
            'Up': UP, 'Down': DOWN, 'Left': LEFT, 'Right': RIGHT,
            'w': UP,  's': DOWN,   'a': LEFT,  'd': RIGHT,
        }
        if key in direction_map:
            self.next_dir = direction_map[key]
        elif key == 'r' and not self.alive:
            if self._after_id:
                self.after_cancel(self._after_id)
            self._init_game()
            self._tick()
        elif key in ('q', 'Escape'):
            self.destroy()

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def _centre_window(self) -> None:
        """Centre the window on screen."""
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f'+{x}+{y}')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app = SnakeGame()
    app.mainloop()
