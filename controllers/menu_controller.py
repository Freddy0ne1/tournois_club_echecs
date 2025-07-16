"""controllers/menu_controller.py
Menu principal avec option Rapport (tournoi) -> sous-menu + export CSV tournoi.
"""

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController


class MenuController:
    """Contrôleur du menu principal."""

    def __init__(self) -> None:
        self.pc = PlayerController()
        self.tc = TournamentController()

    def run(self) -> None:
        """Lance le menu principal."""
        print("Sélectionnez une option :")
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Paramètres joueur")
            print("2. Paramètres tournoi")
            print("3. Quitter")
            choice = input("> ").strip()
            match choice:
                case "1":
                    self._menu_players()
                case "2":
                    self._menu_tournaments()
                case "3" | "q" | "Q":
                    return
                case _:
                    print("Choix invalide.")

    def _menu_players(self) -> None:
        while True:
            print("\n--- PARAMÈTRES JOUEUR ---")
            print("1. Créer un joueur")
            print("2. Lister les joueurs")
            print("3. Modifier un joueur")
            print("4. Supprimer un joueur")
            print("0. Retour")
            ch = input("> ").strip()
            match ch:
                case "1":
                    self.pc.create_player()
                case "2":
                    self.pc.list_players()
                case "3":
                    self.pc.update_player()
                    self.tc.refresh_from_disk()  # sync tournois
                case "4":
                    self.pc.delete_player()
                    self.tc.refresh_from_disk()  # sync tournois
                case "0":
                    return
                case _:
                    print("Choix invalide.")

    def _menu_tournaments(self) -> None:
        while True:
            print("\n--- PARAMÈTRES TOURNOI ---")
            print("1. Créer un tournoi")
            print("2. Lister les tournois")
            print("3. Modifier un tournoi")
            print("4. Supprimer un tournoi")
            print("5. Démarrer un tournoi")
            print("6. Saisir les scores du round en cours")
            print("7. Démarrer le round suivant")
            print("8. Afficher le classement")
            # print("9. Lister les joueurs d'un tournoi")
            print("9. Rapports / Export CSV tournoi")
            print("0. Retour")
            ch = input("> ").strip()
            match ch:
                case "1":
                    self.tc.create_tournament()
                case "2":
                    self.tc.list_tournaments()
                case "3":
                    self.tc.update_tournament()
                case "4":
                    self.tc.delete_tournament()
                case "5":
                    self.tc.start_tournament()
                case "6":
                    t = self.tc.select_tournament()
                    if t and RoundController.enter_results(t):
                        self.tc.save()
                case "7":
                    t = self.tc.select_tournament()
                    if t and RoundController.next_round(t):
                        self.tc.save()
                case "8":
                    t = self.tc.select_tournament()
                    if t:
                        RoundController.show_standings(t)
                # case "9": self.tc.list_players_in_tournament()
                case "9":
                    self.tc.report_menu()
                case "0":
                    return
                case _:
                    print("Choix invalide.")
