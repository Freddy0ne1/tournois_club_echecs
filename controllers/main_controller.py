"""controllers/main_controller.py
Contrôleur principal pour démarrer l'application.
"""

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.player import Player


class MainController:
    """Contrôleur principal pour démarrer l'application."""

    def __init__(self):
        # 1️⃣ Instancie le contrôleur des joueurs
        self.player_ctrl = PlayerController()

        # 2️⃣ Instancie le contrôleur des tournois
        self.tour_ctrl = TournamentController()

        # 3️⃣ Recharge tous les joueurs existants depuis players.json
        Player.load_all()

    # -----------------------
    #   MÉTHODES D’AIDE
    # -----------------------

    def _show_menu(self, title, options):
        """
        Affiche un menu numéroté et retourne le choix validé.
        title   : titre du menu (str)
        options : liste de textes d'options (list de str)
        """
        # 1️⃣ Affiche un en‑tête clair avec le titre du menu
        print(f"\n=== {title} ===\n")

        # 2️⃣ Parcourt chaque option et l’affiche numérotée
        for idx, text in enumerate(options, 1):
            print(f"{idx}. {text}")

        # 3️⃣ Boucle de validation de la saisie utilisateur·rice
        while True:
            # 🅰 Invite à saisir un nombre
            val = input("\nVotre choix : ").strip()
            # 🅱 Vérifie que l’entrée est un entier
            if val.isdigit():
                num = int(val)
                # 🅲 Vérifie que ce nombre correspond à une option existante
                if 1 <= num <= len(options):
                    return num  # choix valide, on le retourne
            # 🅳 En cas d’entrée invalide, affiche un message d’erreur et redemande
            print(f"❌ Option invalide. Entrez un nombre entre 1 et {len(options)}.")

    # -----------------------
    #   MENU PRINCIPAL
    # -----------------------

    def run(self):
        """Boucle principale avec le menu racine."""

        # 1️⃣ Boucle infinie pour afficher le menu principal tant que
        # - l’utilisateur·rice ne choisit pas de quitter
        while True:
            # 2️⃣ Affiche le menu principal et récupère le choix (1 à 4)
            choice = self._show_menu(
                "Menu Principal",
                [
                    "Paramètres joueurs",
                    "Paramètres tournoi",
                    "Rapports",
                    "Quitter",
                ],
            )

            # 3️⃣ Redirige vers le sous‑menu « Paramètres joueurs »
            if choice == 1:
                self._player_menu()

            # 4️⃣ Redirige vers le sous‑menu « Paramètres tournoi »
            elif choice == 2:
                self._tournament_menu()

            # 5️⃣ Redirige vers le sous‑menu « Rapports »
            elif choice == 3:
                self._reports_menu()

            # 6️⃣ Option « Quitter » ou toute autre saisie (4)
            else:
                print("\nAu revoir !")
                break  # Sortie de la boucle et fin de l’application

    # -----------------------
    #   MENU JOUEURS
    # -----------------------

    def _player_menu(self):
        """Menu pour gérer les joueurs."""

        # 1️⃣ Boucle principale du menu joueurs : reste actif jusqu’à “Retour”
        while True:
            # 2️⃣ Affiche le menu des opérations sur les joueurs et récupère le choix
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

            # 3️⃣ Si choix “Créer joueur”, on appelle la création
            if choice == 1:
                self.player_ctrl.create_player()

            # 4️⃣ Si choix “Modifier joueur”, on modifie et on met à jour les références
            elif choice == 2:
                updated = self.player_ctrl.modify_player()
                if updated:
                    # Met à jour toute référence au Player modifié dans les tournois
                    self.tour_ctrl.update_player_references(updated)

            # 5️⃣ Si choix “Supprimer joueur”, on appelle la suppression
            elif choice == 3:
                self.player_ctrl.delete_player()

            # 6️⃣ Si choix “Rechercher joueur”, on lance la recherche
            elif choice == 4:
                self.player_ctrl.search_player()

            # 7️⃣ Si choix “Lister joueurs”, on affiche la liste complète
            elif choice == 5:
                self.player_ctrl.list_players()

            # 8️⃣ Si choix “Retour” (ou toute autre valeur), on sort du menu
            else:  # choice == 6
                break

    # -----------------------
    #   MENU TOURNOIS
    # -----------------------

    def _tournament_menu(self):
        """Menu pour gérer les tournois."""

        # 1️⃣ Boucle principale du menu tournois :
        # - active tant que l’utilisateur·rice ne choisit pas “Retour”
        while True:
            # 2️⃣ Affiche le menu des opérations disponibles et récupère le choix (1–10)
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

            # 3️⃣ Redirection vers la création de tournoi
            if choice == 1:
                self.tour_ctrl.create_tournament()

            # 4️⃣ Redirection vers la modification d’un tournoi
            elif choice == 2:
                self.tour_ctrl.modify_tournament()

            # 5️⃣ Suppression d’un tournoi
            elif choice == 3:
                self.tour_ctrl.delete_tournament()

            # 6️⃣ Affichage de la liste des tournois
            elif choice == 4:
                self.tour_ctrl.list_tournaments()

            # 7️⃣ Gestion des joueurs dans un tournoi (ajout/retrait)
            elif choice == 5:
                self.tour_ctrl.manage_players_in_tournament()

            # 8️⃣ Démarrage d’un tournoi
            elif choice == 6:
                self.tour_ctrl.start_tournament()

            # 9️⃣ Saisie des scores du round en cours
            elif choice == 7:
                self.tour_ctrl.enter_scores_current_round()

            # 🔟 Démarrage du round suivant
            elif choice == 8:
                self.tour_ctrl.start_next_round()

            # 1️⃣1️⃣ Affichage du classement du tournoi
            elif choice == 9:
                self.tour_ctrl.show_leaderboard()

            # 1️⃣2️⃣ Retour au menu principal
            else:  # choice == 10
                break

    # -----------------------
    #   MENU RAPPORTS
    # -----------------------

    def _reports_menu(self):
        """Menu pour afficher les rapports."""

        # 1️⃣ Boucle principale du menu « Rapports » :
        # - active tant que l’utilisateur·rice ne choisit pas “Retour”
        while True:
            # 2️⃣ Affiche les options de rapports disponibles et récupère le choix
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

            # 3️⃣ Si choix “1”, affiche tous les joueurs inscrits (ordre alphabétique)
            if choice == 1:
                self.tour_ctrl.list_registered_players()

            # 4️⃣ Si choix “2”, affiche la liste de tous les tournois
            elif choice == 2:
                self.tour_ctrl.list_tournaments()

            # 5️⃣ Si choix “3”, affiche le nom et les dates d’un tournoi choisi
            elif choice == 3:
                self.tour_ctrl.show_tournament_header()

            # 6️⃣ Si choix “4”, affiche les joueurs d’un tournoi sélectionné (ordre alphabétique)
            elif choice == 4:
                self.tour_ctrl.show_tournament_players()

            # 7️⃣ Si choix “5”, affiche tous les rounds et matches d’un tournoi
            elif choice == 5:
                self.tour_ctrl.show_all_rounds_and_matches()

            # 8️⃣ Si choix “6” ou autre (Retour), quitte le menu et revient au menu principal
            else:  # choice == 6
                break
