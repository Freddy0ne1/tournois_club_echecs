"""
Module tournament_listing
Affiche et liste les tournois existants.
"""

from views.console_view import ConsoleView
from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour l'affichage et le listing des tournois.
    """

    # -----------------------
    #   LISTE TOURNOI
    # -----------------------

    def list_tournaments(self):
        """Affiche la liste des tournois."""
        # 1️⃣ Affichage de l'en‑tête pour démarquer la section
        print("\n--- Liste des tournois ---")

        # 2️⃣ Délégation de l'affichage détaillé à ConsoleView
        #    Cette méthode va lister chaque tournoi avec ses infos clés
        ConsoleView.show_tournaments(self._tournaments)
