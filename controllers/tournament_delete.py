"""
Module tournament_delete
Gère la suppression d'un tournoi existant.
"""

from .tournament_controller_base import (
    TournamentController as BaseTournamentController,
    DATA_DIR,
)


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour gérer la suppression de tournois.
    """

    # -----------------------
    #   SUPPRESSION TOURNOI
    # -----------------------

    # ------- Suppression d'un tournoi existant -------
    def delete_tournament(self):
        """Supprime un tournoi existant."""
        # 1️⃣ Affichage de l'en‑tête de suppression
        print("\n--- Suppression d'un tournoi ---")

        # 2️⃣ Sélection du tournoi à supprimer
        #    _choose("supprimer") affiche la liste et renvoie l'objet ou None
        tournament = self._choose("supprimer")
        if not tournament:  # Si aucun tournoi n'est sélectionné ou erreur
            return

        # 3️⃣ Demande de confirmation à l'utilisateur·rice
        #    Seul "o" (oui) en minuscules valide la suppression
        if input(f"\nSupprimer {tournament.name} (o/N) ? ").lower() != "o":
            return

        # 4️⃣ Construction du chemin vers le fichier JSON correspondant
        #    On reprend la même logique que _file_path : nom en minuscules et underscores
        path = DATA_DIR / f"{tournament.name.lower().replace(' ', '_')}.json"

        # 5️⃣ Suppression du fichier JSON si présent
        if path.exists():
            path.unlink()  # supprime physiquement le fichier

        # 6️⃣ Retrait de l'objet Tournament de la liste en mémoire
        self._tournaments.remove(tournament)

        # 7️⃣ Message de confirmation final
        print(
            f"\n✅ Le tournoi '{tournament.name}' - {tournament.place} a été supprimé."
        )
