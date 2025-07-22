"""models/match.py
Représente un match entre deux joueurs et leurs scores.
"""


class Match:
    """Représente un match entre deux joueurs et leurs scores."""

    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        # On stocke toujours les deux joueurs dans une seule propriété .players
        self.players = (player1, player2)
        # On stocke toujours les deux scores dans une seule propriété .scores
        self.scores = (score1, score2)

    def serialize(self):
        """Prépare ce match pour l'enregistrer en JSON."""
        # On renvoie deux tuples : (ID du joueur, score du joueur)
        p1, p2 = self.players
        s1, s2 = self.scores
        return (
            (p1.national_id, s1),
            (p2.national_id, s2),
        )
