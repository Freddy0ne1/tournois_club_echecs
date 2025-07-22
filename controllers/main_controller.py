"""controllers/main_controller.py
Contrôleur principal pour démarrer l'application.
"""

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.player import Player


class MainController:
    """Contrôleur principal pour démarrer l'application."""

    def __init__(self):
        self.player_ctrl = PlayerController()
        self.tour_ctrl = TournamentController()
        # Charge tous les joueurs existants
        Player.load_all()

    def run(self):
        """Boucle principale avec le menu racine."""
        while True:
            choice = self._show_menu(
                "Menu Principal",
                [
                    "Paramètres joueurs",
                    "Paramètres tournoi",
                    "Rapports",
                    "Quitter",
                ],
            )
            if choice == 1:
                self._player_menu()
            elif choice == 2:
                self._tournament_menu()
            elif choice == 3:
                self._reports_menu()
            else:  # choice == 4
                print("\nAu revoir !")
                break

    def _player_menu(self):
        """Menu pour gérer les joueurs."""
        while True:
            choice = self._show_menu(
                "Menu Joueurs",
                [
                    "Créer joueur",
                    "Modifier joueur",
                    "Supprimer joueur",
                    "Rechercher joueur",
                    "Lister joueurs",
                    "Retour",
                ],
            )
            if choice == 1:
                self.player_ctrl.create_player()
            elif choice == 2:
                updated = self.player_ctrl.modify_player()
                if updated:
                    self.tour_ctrl.update_player_references(updated)
            elif choice == 3:
                self.player_ctrl.delete_player()
            elif choice == 4:
                self.player_ctrl.search_player()
            elif choice == 5:
                self.player_ctrl.list_players()
            else:  # choice == 6 (Retour)
                break

    def _tournament_menu(self):
        """Menu pour gérer les tournois."""
        while True:
            choice = self._show_menu(
                "Menu Tournois",
                [
                    "Créer un tournoi",
                    "Modifier un tournoi",
                    "Supprimer un tournoi",
                    "Lister les tournois",
                    "Ajouter/Retirer joueur(s) à un tournoi",
                    "Démarrer un tournoi",
                    "Saisir scores du round",
                    "Démarrer le round suivant",
                    "Afficher le classement",
                    "Retour",
                ],
            )
            if choice == 1:
                self.tour_ctrl.create_tournament()
            elif choice == 2:
                self.tour_ctrl.modify_tournament()
            elif choice == 3:
                self.tour_ctrl.delete_tournament()
            elif choice == 4:
                self.tour_ctrl.list_tournaments()
            elif choice == 5:
                self.tour_ctrl.manage_players_in_tournament()
            elif choice == 6:
                self.tour_ctrl.start_tournament()
            elif choice == 7:
                self.tour_ctrl.enter_scores_current_round()
            elif choice == 8:
                self.tour_ctrl.start_next_round()
            elif choice == 9:
                self.tour_ctrl.show_leaderboard()
            else:  # choice == 10 (Retour)
                break

    def _reports_menu(self):
        """Menu pour afficher les rapports."""
        while True:
            choice = self._show_menu(
                "Menu Rapports",
                [
                    "Liste de tous les joueurs (ordre alphabétique)",
                    "Liste de tous les tournois",
                    "Nom et dates d'un tournoi donné",
                    "Joueurs d'un tournoi (ordre alphabétique)",
                    "Tous les rounds + matches d'un tournoi",
                    "Retour",
                ],
            )
            if choice == 1:
                self.tour_ctrl.list_registered_players()
            elif choice == 2:
                self.tour_ctrl.list_tournaments()
            elif choice == 3:
                self.tour_ctrl.show_tournament_header()
            elif choice == 4:
                self.tour_ctrl.show_tournament_players()
            elif choice == 5:
                self.tour_ctrl.show_all_rounds_and_matches()
            else:  # choice == 6 (Retour)
                break

    def _show_menu(self, title, options):
        """
        Affiche un menu numéroté et retourne le choix validé.
        title   : titre du menu (str)
        options : liste de textes d'options (list de str)
        """
        print(f"\n=== {title} ===\n")
        for idx, text in enumerate(options, 1):
            print(f"{idx}. {text}")
        while True:
            val = input("\nVotre choix : ").strip()
            if val.isdigit():
                num = int(val)
                if 1 <= num <= len(options):
                    return num
            print(f"❌ Option invalide. Entrez un nombre entre 1 et {len(options)}.")
