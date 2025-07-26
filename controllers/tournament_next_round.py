"""
Module tournament_next_round
Gère le démarrage du round suivant d'un tournoi en cours.
"""

from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour gérer le lancement du round suivant.
    """

    # -----------------------
    #   ROUND SUIVANT
    # -----------------------

    def start_next_round(self):
        """
        Démarre le round suivant du tournoi sélectionné.
        Étapes :
        1. Sélection du tournoi
        2. Vérifie que le tournoi n'est pas terminé
        3. Vérifie que le round précédent est bien clôturé
        4. Vérifie que le nombre maximum de rounds n'est pas dépassé
        5. Lance le round suivant et sauvegarde l'état du tournoi
        """
        # 1️⃣ Affiche le titre pour indiquer l'action en cours
        print("\n--- Démarrage du round suivant ---")

        # 2️⃣ Permet à l'utilisateur de choisir le tournoi
        tournament = self._choose("démarrer le round suivant")
        if not tournament:  # 🅰 Annule si aucun tournoi sélectionné
            return

        # 3️⃣ Empêche de lancer un round si le tournoi est déjà terminé
        if tournament.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tournament.name}' est déjà terminé.")
            return

        # 4️⃣ Vérifie que le dernier round est bien clôturé avant d'en lancer un nouveau
        if tournament.rounds and not tournament.rounds[-1].end_time:
            print("⚠️  Il faut clôturer le round en cours avant de démarrer le suivant.")
            return

        # 5️⃣ Vérifie que le nombre maximum de rounds n'est pas déjà atteint
        if tournament.current_round_index >= tournament.total_rounds:
            print("ℹ️  Tous les rounds ont déjà été joués.")
            return

        # 6️⃣ Lance le nouveau round et sauvegarde l'état du tournoi
        tournament.start_next_round()
        self._save(tournament)
        print("🏁 Nouveau round démarré.")
