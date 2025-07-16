"""models/tournament.py
Représente un tournoi d'échecs.
"""

from dataclasses import dataclass, field
from typing import List
from .player import Player
from .round import Round


@dataclass
class Tournament:
    """Représente un tournoi d'échecs."""

    name: str
    location: str
    start_date: str  # JJ/MM/AAAA
    end_date: str
    description: str
    rounds_total: int = 4
    players: List[Player] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
