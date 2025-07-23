"""models/round.py
Représente un round d'un tournoi d'échecs.
"""

from datetime import datetime

# -----------------------
#   CLASSE ROUND
# -----------------------


class Round:
    """Représente un round d'un tournoi d'échecs."""

    def __init__(self, name, matches=None):
        # 1️⃣ Nom du round (ex. "Round 1")
        self.name = name

        # 2️⃣ Liste des objets Match :
        #    si matches fourni, on l’utilise, sinon on crée une liste vide
        self.matches = matches if matches is not None else []

        # 3️⃣ Heure de démarrage du round :
        #    on enregistre l’instant courant au format ISO (YYYY‑MM‑DDTHH:MM:SS)
        self.start_time = datetime.now().isoformat(timespec="seconds")

        # 4️⃣ Heure de fin / clôture :
        #    à None tant que le round n'est pas fermé via close()
        self.end_time = None

    # -----------------------
    #   CLÔTURE DU ROUND
    # -----------------------

    def close(self):
        """Marque le round comme terminé en enregistrant l'heure de fin."""
        # 5️⃣ Quand on appelle close(), on met à jour end_time
        #    pour dire “round terminé” à cet instant précis
        self.end_time = datetime.now().isoformat(timespec="seconds")
