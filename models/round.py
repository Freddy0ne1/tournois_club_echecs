"""models/round.py
Représente un round d'un tournoi d'échecs.
"""

from datetime import datetime


class Round:
    """Représente un round d'un tournoi d'échecs."""

    def __init__(self, name, matches=None):
        # Nom du round (ex. "Round 1")
        self.name = name
        # Liste des objets Match (vide par défaut)
        self.matches = matches if matches is not None else []
        # Date/heure de début (format ISO)
        self.start_time = datetime.now().isoformat(timespec="seconds")
        # None tant que le round n'est pas clôturé
        self.end_time = None

    def close(self):
        """Marque le round comme terminé en enregistrant l'heure de fin."""
        self.end_time = datetime.now().isoformat(timespec="seconds")
