"""models/player.py
Représente un joueur d'échecs.
"""

from dataclasses import dataclass, field


@dataclass
class Player:
    """Représente un joueur d'échecs."""

    id_national: str  # format AB12345
    last_name: str
    first_name: str
    birth_date: str  # JJ/MM/AAAA
    score: float = field(default=0.0)
