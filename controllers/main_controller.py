"""controllers/main_controller.py
Contrôleur principal pour démarrer l'application.
"""

from models.player import Player

from controllers.tournament_management import TournamentManagement
from controllers.tournament_players import TournamentPlayers
from controllers.player_controller import PlayerController
from controllers.tournament_reports import TournamentReports
from controllers.tournament_rounds import TournamentRound
from views.console_view import ConsoleView
from .tournament_controller_base import TournamentControllerBase


class MainController:
    """
    Contrôleur principal de l'application.
    Rôle :
      - Point d'entrée de l'application
      - Initialise les différents sous-contrôleurs (joueurs, tournois)
      - Fournit la boucle principale et la navigation dans les menus
    """

    def __init__(self):
        """
        Initialise le contrôleur principal.
        Étapes :
        1. Instancie le contrôleur des joueurs
        2. Instancie le contrôleur des tournois
        3. Recharge les joueurs existants depuis players.json
        """
        # 1️⃣ Crée le contrôleur dédié aux joueurs
        self.player_ctrl = PlayerController()

        # 2️⃣ Crée le contrôleur dédié aux tournois
        self.tour_ctrl = TournamentManagement()
        self.tour_ctrl2 = TournamentReports()
        self.tour_ctrl3 = TournamentPlayers()
        self.tour_ctrl4 = TournamentRound()
        self.tour_ctrl5 = ConsoleView()
        self.tour_ctrl_base = TournamentControllerBase()

        # 3️⃣ Recharge les joueurs sauvegardés précédemment
        Player.load_all()

    # -----------------------
    #   MÉTHODES D'AIDE
    # -----------------------

    # ------- Affichage d’un menu numéroté et lecture du choix utilisateur -------
    def _show_menu(self, title, options):
        """
        Affiche un menu numéroté et lit le choix de l'utilisateur·rice.
        Paramètres :
        - title   : titre du menu (str)
        - options : liste d'options (list de str)
        Étapes :
        1. Affiche le titre du menu
        2. Affiche chaque option avec un numéro
        3. Demande une saisie numérique valide correspondant à une option
        4. Retourne le numéro choisi
        """
        # 1️⃣ Affiche l'en‑tête avec le titre du menu
        print(f"\n=== {title} ===\n")

        # 2️⃣ Parcourt la liste d'options et les affiche avec numérotation
        for idx, text in enumerate(options, 1):
            print(f"{idx}. {text}")

        # 3️⃣ Boucle de saisie pour obtenir un choix valide
        while True:
            # 🅰 Invite l'utilisateur à saisir un numéro
            val = input("\nVotre choix : ").strip()

            # 🅱 Vérifie que la saisie est bien un nombre
            if val.isdigit():
                num = int(val)

                # 🅲 Vérifie que le nombre correspond à une option disponible
                if 1 <= num <= len(options):
                    return num  # Retourne le choix validé

            # 🅳 Si la saisie est invalide, affiche un message d'erreur et redemande
            print(f"❌ Option invalide. Entrez un nombre entre 1 et {len(options)}.")

    # -----------------------
    #   MENU PRINCIPAL
    # -----------------------

    # ------- Boucle principale et navigation dans les menus -------
    def run(self):
        """
        Boucle principale de l'application avec le menu racine.
        Étapes :
        1. Définit les actions possibles et leurs options
        2. Affiche le menu principal
        3. Redirige vers le sous-menu choisi
        4. Quitte l'application si l'utilisateur sélectionne 'Quitter'
        """
        # 1️⃣ Dictionnaire reliant les numéros aux méthodes correspondantes
        actions = {
            1: self._player_menu,
            2: self._tournament_menu,
            3: self._reports_menu,
        }

        # 2️⃣ Liste des options affichées dans le menu principal
        options = [
            "Paramètres joueurs",
            "Paramètres tournoi",
            "Rapports",
            "Quitter",
        ]

        # 3️⃣ Boucle infinie jusqu'à ce que l'utilisateur choisisse de quitter
        while True:
            # 🅰 Affiche le menu et récupère le choix de l'utilisateur
            choice = self._show_menu("Menu Principal", options)

            # 🅱 Si l'utilisateur choisit de quitter, on sort de la boucle
            if choice == 4:
                print("\nAu revoir !")
                break

            # 🅲 Exécute l'action correspondant au choix si elle existe
            action = actions.get(choice)
            if action:
                action()

    # -----------------------
    #   MENU JOUEURS
    # -----------------------

    def _player_menu(self):
        """
        Menu dédié à la gestion des joueurs.
        Étapes :
        1. Définit les actions disponibles : création, modification, suppression,
            recherche et affichage des joueurs.
        2. Affiche les options et lit le choix de l'utilisateur·rice.
        3. Exécute l'action choisie jusqu'à ce que 'Retour' soit sélectionné.
        """

        # 1️⃣ Action spéciale pour modification : met à jour aussi les références dans les tournois
        def modify_and_update():
            updated = self.player_ctrl.modify_player()
            if updated:
                # Si un joueur est modifié, on met à jour toutes ses occurrences dans les tournois
                self.tour_ctrl_base.update_player_references(updated)

        # 2️⃣ Dictionnaire des actions associées aux numéros de menu
        actions = {
            1: self.player_ctrl.create_player,
            2: modify_and_update,
            3: self.player_ctrl.delete_player,
            4: self.player_ctrl.search_player,
            5: self.player_ctrl.list_players,
        }

        # 3️⃣ Liste des options affichées à l'utilisateur
        options = [
            "Créer joueur",
            "Modifier joueur",
            "Supprimer joueur",
            "Rechercher joueur",
            "Lister joueurs",
            "Retour",
        ]

        # 4️⃣ Boucle d'affichage et de gestion des choix
        while True:
            # 🅰 Affiche le menu des joueurs
            choice = self._show_menu("Menu Joueurs", options)

            # 🅱 Option 'Retour' → sortir de la boucle
            if choice == 6:
                break

            # 🅲 Récupère et exécute l'action associée au choix
            action = actions.get(choice)
            if action:
                action()

    # -----------------------
    #   MENU TOURNOIS
    # -----------------------

    def _tournament_menu(self):
        """
        Menu dédié à la gestion des tournois.
        Étapes :
        1. Définit les actions disponibles pour la gestion des tournois :
            création, modification, suppression, ajout/retrait de joueurs,
            démarrage, saisie des scores, rounds et affichage du classement.
        2. Affiche les options et lit le choix de l'utilisateur·rice.
        3. Exécute l'action choisie jusqu'à ce que 'Retour' soit sélectionné.
        """
        # 1️⃣ Dictionnaire associant chaque numéro d'option à une méthode du contrôleur de tournois
        actions = {
            1: self.tour_ctrl.create_tournament,
            2: self.tour_ctrl.modify_tournament,
            3: self.tour_ctrl.delete_tournament,
            4: self.tour_ctrl.list_tournaments,
            5: self.tour_ctrl3.manage_players_in_tournament,
            6: self.tour_ctrl4.start_tournament,
            7: self.tour_ctrl4.enter_scores_current_round,
            8: self.tour_ctrl4.start_next_round,
            9: self.tour_ctrl2.show_leaderboard,
        }

        # 2️⃣ Liste des options affichées dans le menu tournois
        options = [
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
        ]

        # 3️⃣ Boucle d'affichage et de gestion des choix
        while True:
            # 🅰 Affiche le menu des tournois et lit la saisie
            choice = self._show_menu("Menu Tournois", options)

            # 🅱 Si l'utilisateur choisit 'Retour', on sort de la boucle
            if choice == 10:
                break

            # 🅲 Recherche et exécution de l'action associée
            action = actions.get(choice)
            if action:
                action()

    # -----------------------
    #   MENU RAPPORTS
    # -----------------------

    def _reports_menu(self):
        """
        Menu dédié à la consultation des rapports et statistiques.
        Étapes :
        1. Définit les actions disponibles : affichage des joueurs,
            liste des tournois, détails d'un tournoi, joueurs d'un tournoi
            et affichage de tous les rounds et matches.
        2. Affiche les options et lit le choix de l'utilisateur·rice.
        3. Exécute l'action choisie jusqu'à ce que 'Retour' soit sélectionné.
        """
        # 1️⃣ Dictionnaire des actions disponibles pour chaque option du menu Rapports
        actions = {
            1: self.tour_ctrl2.list_registered_players,
            2: self.tour_ctrl.list_tournaments,
            3: self.tour_ctrl2.show_tournament_header,
            4: self.tour_ctrl2.show_tournament_players,
            5: self.tour_ctrl2.show_all_rounds_and_matches,
        }

        # 2️⃣ Liste des options affichées dans le menu Rapports
        options = [
            "Liste de tous les joueurs (ordre alphabétique)",
            "Liste de tous les tournois",
            "Nom et dates d'un tournoi donné",
            "Joueurs d'un tournoi (ordre alphabétique)",
            "Tous les rounds + matches d'un tournoi",
            "Retour",
        ]

        # 3️⃣ Boucle de navigation dans le menu Rapports
        while True:
            # 🅰 Affiche le menu et lit le choix de l'utilisateur
            choice = self._show_menu("Menu Rapports", options)

            # 🅱 Si l'utilisateur choisit 'Retour', on sort de la boucle
            if choice == 6:
                break

            # 🅲 Recherche et exécution de l'action correspondant au choix
            action = actions.get(choice)
            if action:
                action()
