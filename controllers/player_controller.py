"""controllers/player_controller.py
Contrôleur pour gérer les joueurs.
"""

import re
from datetime import datetime
from views.console_view import ConsoleView
from models.player import Player


class PlayerController:
    """Contrôleur pour gérer les joueurs."""

    def _input_nonempty(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("\n🔴  Ce champ est obligatoire.\n")

    def _get_sorted_players(self):
        # Retourne la liste des joueurs ordonnés par nom puis prénom
        return sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

    def create_player(self):
        """Crée un nouveau joueur et l'ajoute à la liste."""
        print("\n--- Création d'un nouveau joueur ---\n")
        # 1) Identifiant national
        while True:
            national_id = self._input_nonempty(
                "Identifiant national (AB+5 chiffres) : "
            ).upper()
            if not re.match(r"AB\d{5}$", national_id):
                print("\n❌ Format invalide. Exemple : AB12345\n")
                continue
            if any(p.national_id == national_id for p in Player.registry):
                print("\n❌ ID déjà utilisé.\n")
                continue
            break

        # 2) Nom et prénom
        last_name = self._input_nonempty("Nom : ").upper()
        first_name = self._input_nonempty("Prénom : ").capitalize()

        # 3) Date de naissance
        while True:
            birth = self._input_nonempty("Date de naissance (jj/mm/aaaa) : ")
            try:
                datetime.strptime(birth, "%d/%m/%Y")
                break
            except ValueError:
                print("\n❌ Format invalide. Exemple : 31/12/1990\n")

        # 4) Création et sauvegarde
        # ATTENTION à l'ordre des arguments !
        new_player = Player(last_name, first_name, birth, national_id)
        Player.save_all()
        print("\n✅ Joueur créé.\n")
        print(
            f"--- Informations du joueur {new_player.last_name} {new_player.first_name} ---\n"
        )
        print(f"Date de naissance : {new_player.birth_date}")
        print(f"ID : {new_player.national_id}")

    def list_players(self):
        """Affiche la liste des joueurs."""
        players = self._get_sorted_players()
        ConsoleView.show_players(players)

    def _choose_player(self, action):
        players = self._get_sorted_players()
        if not players:
            print("Aucun joueur disponible.")
            return None
        ConsoleView.show_players(players)
        choice = input(f"\nNuméro du joueur à {action} : ").strip()
        if not choice.isdigit():
            print("Entrée invalide.")
            return None
        idx = int(choice)
        if 1 <= idx <= len(players):
            return players[idx - 1]
        print("Indice hors plage.")
        return None

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

    def delete_player(self):
        """Supprime un joueur existant."""
        print("\n--- Suppression d'un joueur ---\n")
        # Choisir le joueur à supprimer
        player = self._choose_player("supprimer")
        if not player:
            return
        confirm = input(
            f"\n⚠️  Voulez-vous supprimer {player.first_name} {player.last_name} (o/N) ? : "
        ).lower()
        if confirm == "o":
            Player.registry.remove(player)
            Player.save_all()
            print(f"\n✅ {player.first_name} {player.last_name} a été supprimé.")

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
            print("Aucun résultat trouvé.")
