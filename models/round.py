"""models/round.py
Représente un round d'un tournoi d'échecs.
"""

from datetime import datetime

# -----------------------
#   CLASSE ROUND
# -----------------------


class Round:
    """
    Représente un round (manche) d'un tournoi d'échecs.

    Rôle :
      - Contient la liste des matchs (Match) joués dans ce round
      - Enregistre le moment du début et, plus tard, de la fin du round
      - Permet de regrouper les matchs par manche dans un tournoi
    """

    # ------- Initialisation d'un nouvel objet Round -------
    def __init__(self, name, matches=None):
        """
        Initialise un round.

        Paramètres :
          - name    : Nom du round (exemple : "Round 1")
          - matches : Liste d'objets Match, ou None pour démarrer avec une liste vide
        """

        # 1️⃣ Enregistre le nom du round
        self.name = name

        # 2️⃣ Initialise la liste des matchs
        #    - Si une liste est fournie, on l'utilise
        #    - Sinon on crée une nouvelle liste vide
        self.matches = matches if matches is not None else []

        # 3️⃣ Note l'heure de début du round
        #    - datetime.now().isoformat(timespec="seconds") produit une chaîne
        #      au format ISO (ex. 2025-07-25T14:32:10)
        self.start_time = datetime.now().isoformat(timespec="seconds")

        # 4️⃣ Initialise l'heure de fin du round à None
        #    - Elle sera définie plus tard quand le round sera clôturé
        self.end_time = None

    # -----------------------
    #   CLÔTURE DU ROUND
    # -----------------------

    def close(self):
        """
        Termine le round en enregistrant l'heure de fin.

        Explications :
        - Cette méthode doit être appelée quand tous les matchs du round sont joués.
        - Elle fixe l'attribut `end_time` avec l'heure courante,
            ce qui permet de marquer le round comme terminé.
        """
        # 5️⃣ On fixe end_time avec la date et l'heure actuelles au format ISO (lisible)
        self.end_time = datetime.now().isoformat(timespec="seconds")
