"""controllers/player_controller.py
Contrôleur pour gérer les joueurs.
"""

import re
from datetime import datetime
from views.console_view import ConsoleView
from models.player import Player

# -----------------------
#   Constantes globales
# -----------------------

# Nombre maximal de tentatives pour chaque saisie obligatoire
MAX_ATTEMPTS = 3


class PlayerController:
    """Gère la création, l'affichage, la modification, la suppression et la recherche des joueurs."""

    # -----------------------
    #   MÉTHODES D’AIDE
    # -----------------------

    def _input_nonempty(self, prompt):
        """
        Demande une saisie non vide à l'utilisateur·rice.
        Réessaie jusqu'à obtenir une valeur ou atteint MAX_ATTEMPTS.
        Retourne la chaîne ou None si annulé.
        """
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            value = input(prompt).strip()
            if value:
                return value
            attempt += 1
            print(
                f"\n🔴  Ce champ est obligatoire. ({attempt}/{MAX_ATTEMPTS}). Réessayez.\n"
            )
        print("❌ Nombre de tentatives dépassé. Opération abandonnée.")
        return None

    def _input_date(self, prompt_text):
        """
        Demande une date au format jj/mm/aaaa.
        Réessaie jusqu'à obtenir un format valide ou atteint MAX_ATTEMPTS.
        Retourne la chaîne valide ou None.
        """
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            date_str = input(prompt_text).strip()
            try:
                datetime.strptime(date_str, "%d/%m/%Y")
                return date_str
            except ValueError:
                attempt += 1
                print(
                    f"  ➤ Format invalide ({attempt}/{MAX_ATTEMPTS}). Ex.: 31/12/1990"
                )
        print("❌ Nombre de tentatives dépassé. Opération abandonnée.")
        return None

    def _get_sorted_players(self):
        """
        Retourne la liste des Player.registry triée par nom puis prénom.
        """
        # Retourne la liste des joueurs ordonnés par nom puis prénom
        return sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

    def _choose_player(self, action):
        """
        Affiche les joueurs et demande de choisir un numéro pour une action.
        Retourne le Player choisi ou None.
        """
        players = self._get_sorted_players()
        if not players:
            print("🔍 Aucun joueur disponible.")
            return None
        ConsoleView.show_players(players)
        choice = input(f"\nNuméro du joueur à {action} : ").strip()
        if not choice.isdigit():
            print("❌ Entrée invalide. Utilisez un numéro")
            return None
        idx = int(choice)
        if 1 <= idx <= len(players):
            return players[idx - 1]
        print("❌ Indice hors plage.")
        return None

    # -----------------------
    #   CREATION
    # -----------------------

    def create_player(self):
        """Crée un nouveau joueur et l'ajoute à la liste."""
        print("\n--- Création d'un nouveau joueur ---\n")
        # Identifiant national
        for _ in range(MAX_ATTEMPTS):
            national_id = self._input_nonempty(
                "Identifiant national (AB+5 chiffres) : "
            )
            if national_id is None:
                return
            national_id = national_id.upper()

            if not re.match(r"AB\d{5}$", national_id):
                print("\n❌ Format invalide. Ex. : AB12345\n")
                continue
            if any(p.national_id == national_id for p in Player.registry):
                print("\n❌ Identifiant déjà utilisé.\n")
                continue
            break
        else:
            print("❌ Échec de la saisie de l'ID. Annulation.")
            return

        # Nom
        last_name = self._input_nonempty("Nom du joueur : ")
        if last_name is None:
            return
        last_name = last_name.upper()

        # Prénom
        first_name = self._input_nonempty("Prénom : ")
        if first_name is None:
            return
        first_name = first_name.capitalize()

        #  Date de naissance
        birth_date = self._input_date("4) Date de naissance (jj/mm/aaaa) : ")
        if birth_date is None:
            return

        #  Création et sauvegarde
        new_player = Player(last_name, first_name, birth_date, national_id)
        Player.save_all()
        print("\n✅ Joueur créé.\n")
        print(
            f"--- Informations du joueur {new_player.last_name} {new_player.first_name} ---\n"
        )
        print(f"Date de naissance : {new_player.birth_date}")
        print(f"ID : {new_player.national_id}")

    # -----------------------
    #   LISTE
    # -----------------------

    def list_players(self):
        """Affiche la liste triée des joueurs."""
        print("\n--- Liste des joueurs ---\n")
        players = self._get_sorted_players()
        if not players:
            print("Aucun joueur trouvé.\n")
            return
        ConsoleView.show_players(players)
        print()

    # -----------------------
    #   MODIFICATION
    # -----------------------

    def modify_player(self):
        """Modifie les informations d'un joueur existant."""
        print("\n--- Modification d'un joueur ---\n")
        # Choisir le joueur à modifier
        player = self._choose_player("modifier")
        if not player:
            return
        print(
            f"\n--- Informations actuelles de {player.first_name} {player.last_name} ---"
        )
        print(f"ID : {player.national_id}")
        print(f"Date de naissance : {player.birth_date}")
        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

        # Modifier le nom
        value = input(f"Nom [{player.last_name}] : ").strip()
        if value:
            player.last_name = value.upper()

        # Modifier le prénom
        value = input(f"Prénom [{player.first_name}] : ").strip()
        if value:
            player.first_name = value.capitalize()

        # Modifier la date de naissance
        while True:
            value = input(f"Date de naissance [{player.birth_date}] : ").strip()
            if value == "":
                break
            try:
                datetime.strptime(value, "%d/%m/%Y")
                player.birth_date = value
                break
            except ValueError:
                print("❌ Format invalide. Exemple : 31/12/1990")

        Player.save_all()
        print("\n✅ Mise à jour effectuée.\n")
        print("--- Nouvelles informations du joueur ---\n")
        print(
            f"{player.last_name} {player.first_name} - {player.birth_date} - ID: {player.national_id}"
        )
        return player

    # -----------------------
    #   SUPPRESSION
    # -----------------------

    def delete_player(self):
        """Supprime un joueur existant après confirmation."""
        print("\n--- Suppression d'un joueur ---\n")
        player = self._choose_player("supprimer")
        if player is None:
            return

        confirm = (
            input(
                f"⚠️  Voulez-vous vraiment supprimer {player.first_name} {player.last_name} (o/N) ? "
            )
            .strip()
            .lower()
        )
        if confirm == "o":
            Player.registry.remove(player)
            Player.save_all()
            print(f"\n✅ {player.first_name} {player.last_name} a été supprimé.\n")
        else:
            print("❌ Suppression annulée.\n")

    # -----------------------
    #   RECHERCHE
    # -----------------------

    def search_player(self):
        """Recherche des joueurs par nom, prénom ou identifiant national."""
        print("\n--- Recherche de joueurs ---\n")
        term = input("Recherche : ").lower().strip()
        results = []
        for p in Player.registry:
            if (
                term in p.last_name.lower()
                or term in p.first_name.lower()
                or term in p.national_id.lower()
                or term in p.birth_date.lower()
            ):
                results.append(p)
        if results:
            results = sorted(results, key=lambda p: (p.last_name, p.first_name))
            ConsoleView.show_players(results)
        else:
            print("🔍  Aucun résultat trouvé.")
