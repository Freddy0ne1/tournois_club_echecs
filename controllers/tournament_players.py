"""
Contrôleur pour la gestion des joueurs dans un tournoi.

Ce module permet :
- L'ajout de joueurs dans un tournoi sélectionné
- Le retrait de joueurs d'un tournoi
- L'affichage de la liste des joueurs inscrits

Il s'appuie sur TournamentControllerBase pour :
- Sélectionner un tournoi (_choose)
- Sauvegarder l'état du tournoi (_save)
"""

from views.display_message import DisplayMessage
from models.player import Player
from .tournament_controller_base import (
    TournamentControllerBase as TournamentPlayersController,
)


class TournamentPlayers(TournamentPlayersController):
    """
    Sous-contrôleur pour gérer l'ajout et le retrait de joueurs dans un tournoi.
    """

    # -----------------------
    #   AJOUT/RETRAIT JOUEUR(S)
    # -----------------------

    # ------- Gestion des joueurs dans un tournoi (ajout / retrait) -------
    def manage_players_in_tournament(self):
        """
        Gère les joueurs d'un tournoi : ajout ou suppression.

        Étapes :
        1. Affiche un en-tête clair pour l'action en cours
        2. Recharge tous les tournois existants depuis le disque
        3. Ne conserve que ceux qui sont "non démarré" et les trie A → Z
        4. Demande à l'utilisateur de choisir un tournoi à modifier
        5. Affiche une boucle d'actions possibles :
        - Ajouter des joueurs
        - Retirer des joueurs
        - Quitter la gestion
        """
        # 1️⃣ Affiche un titre pour introduire la section
        DisplayMessage.display_manage_players_title()

        # 2️⃣ Recharge la liste des tournois depuis le dossier /data/tournaments
        self.reload_tournaments()

        # 3️⃣ Filtre les tournois pour ne garder que ceux "non démarré", triés A→Z
        self._tournaments = sorted(
            [t for t in self._tournaments if t.status == "non démarré"],
            key=lambda t: t.name.lower(),
        )

        # 4️⃣ Demande à l’utilisateur de choisir un tournoi à gérer
        tournament = self._choose("gérer les joueurs de")
        if not tournament:  # ❌ Annule si aucun tournoi n’est sélectionné
            return

        # 5️⃣ Boucle principale : propose d’ajouter, retirer ou quitter
        while True:
            # 🅰 Affiche les infos du tournoi + menu d’options
            self._show_tournament_summary(tournament)

            # 🅱 Demande une action à l’utilisateur
            choice = input("Votre choix : ").strip()

            # 🅲 Exécute l’action choisie
            if choice == "1":
                self._add_players(tournament)  # ➕ Ajouter des joueurs
            elif choice == "2":
                self._remove_players(tournament)  # ➖ Retirer des joueurs
            elif choice == "0":
                break  # 🔚 Quitter la gestion

    # ------- Affiche le résumé du tournoi et le menu de gestion des joueurs -------
    def _show_tournament_summary(self, tournament):
        """
        Affiche les informations principales d'un tournoi
        et présente le menu de gestion des joueurs (ajout/retrait).
        """
        # 1️⃣ Affiche un titre visuel
        DisplayMessage.display_tournament_title()

        # 2️⃣ Affiche les informations détaillées du tournoi
        DisplayMessage.display_tournament_info(tournament)

        # 3️⃣ Affiche les options disponibles pour la gestion des joueurs
        DisplayMessage.display_manage_players_menu()

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
            DisplayMessage.display_not_player()
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
        DisplayMessage.display_player_available(available)

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
                DisplayMessage.display_player_duplicate_warning(token)
                continue
            seen.add(token)

            # 🅲 Vérifie que le numéro correspond à un joueur disponible
            idx = int(token) - 1
            if 0 <= idx < len(available):
                p = available[idx]
                tournament.players.append(p)  # Ajoute le joueur au tournoi
                added.append(p)
            else:
                DisplayMessage.display_player_not_added(token)

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
            DisplayMessage.display_player_added(added)
        else:
            # 9️⃣ Si aucun ajout n'a eu lieu
            DisplayMessage.display_player_not_added_players()

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
            DisplayMessage.display_no_players_in_tournament()
            return

        # 2️⃣ Trie et affiche les joueurs inscrits
        self._display_registered_players(tournament)

        # 3️⃣ Demande la liste des joueurs à retirer
        to_remove = self._ask_players_to_remove(tournament)
        if not to_remove:
            DisplayMessage.display_no_valid_number()
            return

        # 4️⃣ Confirmation et suppression
        removed = self._confirm_and_remove_players(tournament, to_remove)

        # 5️⃣ Finalisation (sauvegarde et affichage)
        self._finalize_player_removal(tournament, removed)

    # ------- Affichage des joueurs inscrits dans un tournoi -------
    def _display_registered_players(self, tournament):
        """Trie et affiche la liste numérotée des joueurs inscrits au tournoi."""
        tournament.players.sort(key=lambda p: (p.last_name, p.first_name))
        DisplayMessage.display_registered_players_list(tournament)

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
            DisplayMessage.display_finalize_player_removal(removed)
        else:
            DisplayMessage.display_player_not_removed()

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
        DisplayMessage.display_registered_players_title(players, title)

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
                    DisplayMessage.display_player_duplicate_warning(token)
                continue

            # 4️⃣ Ajoute le numéro dans l'ensemble pour éviter les doublons
            seen.add(token)

            # 5️⃣ Convertit en index (base 0) et vérifie qu'il est valide
            idx = int(token) - 1
            if 0 <= idx < len(available):
                selected.append(available[idx])
            else:
                DisplayMessage.display_player_not_added(token)

        # 6️⃣ Retourne la liste des joueurs sélectionnés valides
        return selected
