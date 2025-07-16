"""models/round.py
Représente un round d'un tournoi d'échecs.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from .match import Match


@dataclass
class Round:
    """Représente un round d'un tournoi d'échecs."""

    name: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    matches: List[Match] = field(default_factory=list)
