"""models/match.py
Représente un match entre deux joueurs et leurs scores.
"""

# -----------------------
#   CLASSE MATCH
# -----------------------


class Match:
    """Représente un match entre deux joueurs et leurs scores."""

    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        # 1️⃣ Stocke toujours les deux joueurs ensemble
        #    self.players est un tuple (joueur1, joueur2)
        self.players = (player1, player2)
        # 2️⃣ Stocke toujours les deux scores ensemble
        #    self.scores est un tuple (score1, score2)
        self.scores = (score1, score2)

    # -----------------------
    #   SÉRIALISATION DU MATCH
    # -----------------------

    def serialize(self):
        """Prépare ce match pour l'enregistrer en JSON."""
        # 3️⃣ On récupère les joueurs et leurs scores
        p1, p2 = self.players
        s1, s2 = self.scores
        # 4️⃣ On renvoie un tuple de deux tuples :
        #    - chaque sous-tuple contient (ID du joueur, son score)
        return (
            (p1.national_id, s1),
            (p2.national_id, s2),
        )
