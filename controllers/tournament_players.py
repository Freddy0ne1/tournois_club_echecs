"""
Module tournament_players
Gère l'ajout et la suppression de joueurs dans un tournoi.
"""

from models.player import Player
from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour gérer l'ajout et le retrait de joueurs dans un tournoi.
    """

    # -----------------------
    #   AJOUT/RETRAIT JOUEUR(S)
    # -----------------------

    # ------- Gestion des joueurs dans un tournoi (ajout / retrait) -------
    def manage_players_in_tournament(self):
        """
        Gère les joueurs d'un tournoi (ajout ou suppression).
        Étapes :
        1. Sélectionne le tournoi
        2. Vérifie que le tournoi n'est pas encore démarré
        3. Affiche un menu en boucle pour ajouter ou retirer des joueurs
        """
        # 1️⃣ Affiche un titre pour indiquer la gestion des joueurs
        print("\n--- Gestion des joueurs d'un tournoi ---")

        # 2️⃣ Permet de choisir le tournoi concerné
        tournament = self._choose("gérer les joueurs de")
        if not tournament:  # 🅰 Annule si aucun tournoi n'est sélectionné
            return

        # 3️⃣ Empêche toute modification si le tournoi est déjà démarré
        if tournament.status != "non démarré":
            print("\n❌ Impossible après démarrage.")
            return

        # 4️⃣ Boucle du menu : permet d'ajouter, retirer des joueurs ou quitter
        while True:
            # 🅰 Affiche le résumé du tournoi et le menu des actions
            self._show_tournament_summary(tournament)

            # 🅱 Demande le choix de l'utilisateur
            choice = input("Votre choix : ").strip()

            # 🅲 Exécute l'action correspondante
            if choice == "1":
                self._add_players(tournament)  # Ajout de joueurs
            elif choice == "2":
                self._remove_players(tournament)  # Suppression de joueurs
            elif choice == "0":
                break  # Sortie du menu

    # ------- Affiche le résumé du tournoi et le menu de gestion des joueurs -------
    def _show_tournament_summary(self, tournament):
        """
        Affiche les informations principales d'un tournoi
        et présente le menu de gestion des joueurs (ajout/retrait).
        """
        # 1️⃣ Affiche un titre visuel
        print("\n🏆 Informations du tournoi :\n")

        # 2️⃣ Affiche les informations détaillées du tournoi
        print(f"Nom                : {tournament.name}")
        print(f"Lieu               : {tournament.place}")
        print(f"Dates              : {tournament.start_date} → {tournament.end_date}")
        print(f"Description        : {tournament.description}")
        print(f"Nombre de tours    : {tournament.total_rounds}")
        print(f"Joueurs inscrits   : {len(tournament.players)}\n")

        # 3️⃣ Affiche les options disponibles pour la gestion des joueurs
        print("--- Ajouter ou retirer joueur(s) ---")
        print("1. Ajouter joueur(s)")
        print("2. Retirer joueur(s)")
        print("0. Retour\n")

    # -----------------------
    #   AJOUTER JOUEUR(S)
    # -----------------------

    # ------- Ajoute des joueurs sélectionnés dans un tournoi -------
    def _add_players(self, tournament):
        """
        Ajoute des joueurs à un tournoi :
        1. Liste tous les joueurs disponibles (non encore inscrits)
        2. Permet de sélectionner plusieurs joueurs par numéro
        3. Met à jour la liste des joueurs et sauvegarde
        """
        # 1️⃣ Récupère tous les joueurs triés par NOM puis prénom
        all_players = sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

        # 2️⃣ Filtre ceux qui ne sont pas déjà inscrits dans le tournoi
        available = [p for p in all_players if p not in tournament.players]

        # 3️⃣ Si aucun joueur disponible, affiche un message et quitte
        if not available:
            print("\n👤 Tous les joueurs sont déjà inscrits.")
            return

        # 4️⃣ Affiche la liste des joueurs disponibles avec un numéro
        self._display_available_players(available)

        # 5️⃣ Invite l'utilisateur à choisir les joueurs à ajouter (séparés par des virgules)
        nums = input("\nNuméros à ajouter (séparés par des virgules) : ")

        # 6️⃣ Traite la saisie et récupère les joueurs ajoutés
        added = self._process_selected_players(nums, available, tournament)

        # 8️⃣ Finalisation après ajout
        self._finalize_added_players(added, tournament)

    # ------- Affichage de la liste des joueurs disponibles pour ajout -------
    def _display_available_players(self, available):
        """Affiche la liste numérotée des joueurs disponibles à l'ajout."""
        print("\n--- Joueurs disponibles à l'ajout ---")
        for i, p in enumerate(available, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    # ------- Traitement de la saisie des joueurs sélectionnés et ajout au tournoi -------
    def _process_selected_players(self, nums, available, tournament):
        """Analyse la saisie de l'utilisateur et ajoute les joueurs au tournoi."""
        added = []  # Liste des joueurs ajoutés
        seen = set()  # Ensemble pour éviter les doublons de saisie

        # Traite chaque numéro saisi
        for token in nums.split(","):
            token = token.strip()

            # 🅰 Ignore les valeurs qui ne sont pas numériques
            if not token.isdigit():
                continue

            # 🅱 Ignore les doublons de saisie
            if token in seen:
                print(f"⚠️  Numéro {token} dupliqué, ignoré.")
                continue
            seen.add(token)

            # 🅲 Vérifie que le numéro correspond à un joueur disponible
            idx = int(token) - 1
            if 0 <= idx < len(available):
                p = available[idx]
                tournament.players.append(p)  # Ajoute le joueur au tournoi
                added.append(p)
            else:
                print(f"⚠️  Le numéro {token} n'est pas valide.")

        return added

    # ------- Finalisation après ajout des joueurs (tri, sauvegarde et affichage) -------
    def _finalize_added_players(self, added, tournament):
        """Trie, sauvegarde et affiche le résultat final de l'ajout des joueurs."""
        if added:
            # 🅰 Trie la liste des joueurs inscrits après l'ajout
            tournament.players.sort(key=lambda p: (p.last_name, p.first_name))

            # 🅱 Sauvegarde le tournoi mis à jour
            self._save(tournament)

            # 🅲 Affiche les joueurs qui viennent d'être ajoutés
            print("\n👤 Joueur(s) ajouté(s) :")
            for p in added:
                print(f"- {p.last_name} {p.first_name} [{p.national_id}]")
        else:
            # 9️⃣ Si aucun ajout n'a eu lieu
            print("\n👤 Aucun nouveau joueur ajouté.")

    # -----------------------
    #   RETIRER JOUEUR(S)
    # -----------------------

    # ------- Retire un ou plusieurs joueurs sélectionnés d’un tournoi -------
    def _remove_players(self, tournament):
        """
        Retire un ou plusieurs joueurs d'un tournoi non démarré :
        1. Affiche la liste des joueurs inscrits
        2. Permet de sélectionner des joueurs par numéro
        3. Demande confirmation avant suppression
        4. Met à jour et sauvegarde la liste des joueurs
        """

        # 1️⃣ Vérifie si des joueurs sont inscrits
        if not tournament.players:
            print("\n👤 Aucun joueur inscrit.")
            return

        # 2️⃣ Trie et affiche les joueurs inscrits
        self._display_registered_players(tournament)

        # 3️⃣ Demande la liste des joueurs à retirer
        to_remove = self._ask_players_to_remove(tournament)
        if not to_remove:
            print("\n❌ Aucun numéro valide.")
            return

        # 4️⃣ Confirmation et suppression
        removed = self._confirm_and_remove_players(tournament, to_remove)

        # 5️⃣ Finalisation (sauvegarde et affichage)
        self._finalize_player_removal(tournament, removed)

    # ------- Affichage des joueurs inscrits dans un tournoi -------
    def _display_registered_players(self, tournament):
        """Trie et affiche la liste numérotée des joueurs inscrits au tournoi."""
        tournament.players.sort(key=lambda p: (p.last_name, p.first_name))
        print("\n--- Joueurs inscrits ---")
        for i, p in enumerate(tournament.players, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    # ------- Sélection des joueurs à retirer d’un tournoi -------
    def _ask_players_to_remove(self, tournament):
        """Demande à l'utilisateur quels joueurs retirer et retourne une liste d'objets joueurs."""
        nums = input("\nNuméros à retirer (séparés par des virgules) : ")
        to_remove = []
        for token in nums.split(","):
            token = token.strip()
            if not token.isdigit():
                continue
            idx = int(token) - 1
            if 0 <= idx < len(tournament.players):
                to_remove.append(tournament.players[idx])
        return to_remove

    # ------- Confirmation et suppression des joueurs sélectionnés -------
    def _confirm_and_remove_players(self, tournament, to_remove):
        """Demande confirmation et supprime les joueurs sélectionnés du tournoi."""
        removed = []
        for p in to_remove:
            if input(f"Supprimer {p.last_name} {p.first_name} (o/N) ? ").lower() == "o":
                tournament.players.remove(p)
                removed.append(p)
        return removed

    # ------- Finalisation après suppression des joueurs -------
    def _finalize_player_removal(self, tournament, removed):
        """Trie, sauvegarde et affiche le résultat final après suppression."""
        if removed:
            tournament.players.sort(key=lambda p: (p.last_name, p.first_name))
            self._save(tournament)
            print("\n👤 Joueur(s) retiré(s) :")
            for p in removed:
                print(f"- {p.last_name} {p.first_name} [{p.national_id}]")
        else:
            print("\n👤 Aucune suppression effectuée.")

    # ------- Liste des joueurs disponibles (non inscrits) pour un tournoi -------
    def _available_players(self, tournament):
        """
        Retourne la liste des joueurs disponibles pour un tournoi donné.
        - Trie tous les joueurs par nom puis prénom.
        - Exclut ceux qui sont déjà inscrits dans le tournoi.
        """

        # 1️⃣ Récupère tous les joueurs triés par NOM puis prénom
        all_players = sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

        # 2️⃣ Filtre et retourne uniquement les joueurs non encore inscrits
        return [p for p in all_players if p not in tournament.players]

    # ------- Affichage d'une liste numérotée de joueurs avec titre -------
    def _show_player_list(self, players, title):
        """
        Affiche une liste numérotée de joueurs avec un titre.
        - Chaque joueur est affiché sous la forme :
        numéro. NOM Prénom | Identifiant | Date de naissance
        """

        # 1️⃣ Affiche le titre fourni
        print(f"\n--- {title} ---")

        # 2️⃣ Parcourt la liste des joueurs et affiche chaque joueur avec un numéro
        for i, p in enumerate(players, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    # ------- Analyse et validation des numéros de joueurs saisis -------
    def _parse_player_selection(self, nums, available):
        """
        Analyse une saisie utilisateur contenant des numéros séparés par des virgules.
        Retourne la liste des joueurs correspondants dans `available`.

        - Ignore les valeurs non numériques
        - Ignore les doublons et prévient l'utilisateur
        - Vérifie que chaque numéro correspond à un joueur disponible
        """
        # 1️⃣ Prépare la liste des joueurs sélectionnés et un set pour éviter les doublons
        selected = []
        seen = set()

        # 2️⃣ Découpe la chaîne saisie par l'utilisateur sur les virgules
        for token in nums.split(","):
            token = token.strip()

            # 3️⃣ Vérifie que la saisie est bien un nombre et pas déjà vue
            if not token.isdigit() or token in seen:
                if token in seen:
                    print(f"⚠️ Numéro {token} dupliqué, ignoré.")
                continue

            # 4️⃣ Ajoute le numéro dans l'ensemble pour éviter les doublons
            seen.add(token)

            # 5️⃣ Convertit en index (base 0) et vérifie qu'il est valide
            idx = int(token) - 1
            if 0 <= idx < len(available):
                selected.append(available[idx])
            else:
                print(f"⚠️ Le numéro {token} n'est pas valide.")

        # 6️⃣ Retourne la liste des joueurs sélectionnés valides
        return selected
