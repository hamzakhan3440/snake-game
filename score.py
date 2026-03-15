"""
score.py - Score tracking for Snake Game
Handles current score, high score, and score file persistence.
"""

import os

SCORE_FILE = 'highscore.txt'


def load_high_score() -> int:
    """Load the high score from file. Returns 0 if file does not exist."""
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return 0
    return 0


def save_high_score(score: int) -> None:
    """Save the high score to file if it beats the current record.

    Args:
        score: The score to potentially save.
    """
    current_best = load_high_score()
    if score > current_best:
        with open(SCORE_FILE, 'w') as f:
            f.write(str(score))


def calculate_score(length: int) -> int:
    """Calculate score based on snake length.

    Each food eaten = 10 points.

    Args:
        length: Current length of the snake.

    Returns:
        Integer score value.
    """
    # Snake starts at length 3, so subtract starting length
    return max(0, (length - 3) * 10)
