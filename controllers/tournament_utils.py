"""
Module tournament_utils
Fonctions utilitaires pour recharger les tournois et mettre à jour les références des joueurs.
"""

from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour les fonctions utilitaires des tournois :
    - Recharger les tournois depuis le disque
    - Mettre à jour les références des joueurs
    """

    # -----------------------
    #   RECHARGER TOURNOIS DISQUE
    # -----------------------

    # ------- Recharge en mémoire tous les tournois depuis les fichiers JSON -------
    def reload_tournaments(self):
        """
        Recharge la liste des tournois à partir des fichiers JSON présents dans DATA_DIR.
        Étapes :
        1. Appelle la méthode interne _load()
            - Vide d'abord la liste interne (_tournaments)
            - Parcourt tous les fichiers JSON dans DATA_DIR
            - Recharge chaque tournoi valide en mémoire
        """
        # 1️⃣ Appelle la méthode _load() pour rafraîchir la liste des tournois
        self._load()

    # ------- Met à jour les références d'un joueur dans tous les tournois -------
    def update_player_references(self, updated_player):
        """
        Met à jour les références d'un joueur dans tous les tournois chargés.
        Pour chaque tournoi :
        - Recherche un joueur ayant le même identifiant national
        - Remplace l'ancienne instance Player par updated_player
        - Sauvegarde le tournoi si une modification a été effectuée
        """
        # 1️⃣ Parcourt tous les tournois actuellement en mémoire
        for tournament in self._tournaments:
            changed = False  # Drapeau indiquant si une mise à jour a été faite

            # 2️⃣ Parcourt tous les joueurs inscrits dans le tournoi
            for idx, p in enumerate(tournament.players):
                # 🅰 Vérifie si l'ID national correspond
                if p.national_id == updated_player.national_id:
                    # 🅱 Remplace l'ancienne instance Player par la nouvelle
                    tournament.players[idx] = updated_player
                    changed = True

            # 3️⃣ Si une ou plusieurs références ont été mises à jour, on sauvegarde
            if changed:
                self._save(tournament)
