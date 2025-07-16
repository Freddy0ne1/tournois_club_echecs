"""models/match.py"""

from dataclasses import dataclass


@dataclass
class Match:
    """Représente un match entre deux joueurs."""

    player1_id: str
    player2_id: str
    score1: float = 0.0
    score2: float = 0.0
