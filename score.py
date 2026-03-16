import os

SCORE_FILE = 'highscore.txt'


def load_high_score() -> int:
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return 0
    return 0


def save_high_score(score: int) -> None:
    current_best = load_high_score()
    if score > current_best:
        with open(SCORE_FILE, 'w') as f:
            f.write(str(score))


def calculate_score(length: int) -> int:
    # Snake starts at length 3, so subtract starting length
    return max(0, (length - 3) * 10)
