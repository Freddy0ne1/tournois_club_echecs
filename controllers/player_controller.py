"""controllers/player_controller.py
CRUD Joueurs + synchro tournois. Validation date de naissance JJ/MM/AAAA.
"""

import re
from dataclasses import asdict, fields
from typing import List
from datetime import datetime

from models.player import Player
from services.storage_service import (
    load_players,
    save_players,
    load_tournaments,
    save_tournaments,
)


class PlayerController:
    """Contrôleur des joueurs."""

    def __init__(self) -> None:
        allowed = {f.name for f in fields(Player)}
        self.players: List[Player] = [
            Player(**{k: v for k, v in d.items() if k in allowed})
            for d in load_players()
        ]

    # ---------------- Persistance ----------------
    def _persist(self) -> None:
        save_players([asdict(p) for p in self.players])

    # ---------------- Helpers date naissance ----------------
    @staticmethod
    def _prompt_birthdate(
        prompt: str, allow_blank: bool = False, default: str = ""
    ) -> str:
        """Boucle de saisie d'une date JJ/MM/AAAA.
        - allow_blank=True : Entrée vide -> renvoie default (inchangé).
        """
        while True:
            raw = input(prompt).strip()
            if allow_blank and raw == "":
                return default
            try:
                dt = datetime.strptime(raw, "%d/%m/%Y")
            except ValueError:
                print("Format invalide. Exemple : 07/09/1985.")
                continue
            # Option : refuser dates futures
            if dt > datetime.today():
                print("Date dans le futur refusée.")
                continue
            return dt.strftime("%d/%m/%Y")

    # ---------------- CREATE ----------------
    def create_player(self) -> None:
        """Crée un joueur avec ID national, nom, prénom et date de naissance."""
        print("\n=== Création d'un joueur ===")
        # ID
        while True:
            pid = input("ID national (AB12345) : ").strip().upper()
            if not re.fullmatch(r"AB\d{5}", pid):
                print("Format invalide (AB + 5 chiffres).")
                continue
            if any(p.id_national == pid for p in self.players):
                print("ID déjà utilisé.")
                continue
            break
        # Nom / Prénom
        ln = input("Nom : ").strip().title()
        fn = input("Prénom : ").strip().title()
        # Date naissance validée
        bd = self._prompt_birthdate("Date de naissance (JJ/MM/AAAA) : ")
        # Ajout
        self.players.append(Player(pid, ln, fn, bd))
        self._persist()
        print(f"✅ Joueur {fn} {ln} ajouté.")

    # ---------------- READ ----------------
    def list_players(self) -> None:
        """Affiche la liste des joueurs triée par nom, prénom."""
        print("\n=== Liste des joueurs ===")
        if not self.players:
            print("Aucun joueur enregistré.")
            return
        for idx, p in enumerate(
            sorted(self.players, key=lambda x: (x.last_name, x.first_name)), 1
        ):
            print(
                f"{idx}. {p.last_name} {p.first_name} [ID:{p.id_national}] Naissance : {p.birth_date}"
            )

    # ---------------- UPDATE ----------------
    def update_player(self) -> None:
        """Modifie un joueur en utilisant la même numérotation que l'affichage trié."""
        if not self.players:
            print("Aucun joueur.")
            return

        print("\n=== Modifier un joueur ===")

        # On construit *une seule fois* la liste triée qui sert à l'affichage ET à la sélection.
        ordered = sorted(self.players, key=lambda p: (p.last_name, p.first_name))
        for i, p in enumerate(ordered, 1):
            print(f"{i}. {p.last_name} {p.first_name} [ID:{p.id_national}]")

        key = input("Numéro ou ID : ").strip().upper()

        # --- Recherche dans la liste triée ---
        if key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(ordered):
                player = ordered[idx]
            else:
                print("Numéro invalide.")
                return
        else:
            player = next((p for p in self.players if p.id_national == key), None)
            if not player:
                print("Joueur introuvable.")
                return

        old_id = player.id_national

        new_id = (
            input(f"ID [{player.id_national}] : ").strip().upper() or player.id_national
        )
        if new_id != player.id_national:
            if not re.fullmatch(r"AB\\d{5}", new_id):
                print("Format invalide (AB12345).")
                return
            if any(p.id_national == new_id for p in self.players if p is not player):
                print("ID déjà pris.")
                return

        new_ln = (
            input(f"Nom [{player.last_name}] : ").strip().title() or player.last_name
        )
        new_fn = (
            input(f"Prénom [{player.first_name}] : ").strip().title()
            or player.first_name
        )

        # Date naissance validée (Entrée = inchangé)
        prompt_bd = f"Date de naissance [{player.birth_date}] (Entrée = inchangé) : "
        new_bd = self._prompt_birthdate(
            prompt_bd, allow_blank=True, default=player.birth_date
        )

        # Applique
        player.id_national = new_id
        player.last_name = new_ln
        player.first_name = new_fn
        player.birth_date = new_bd

        # Sauvegarde + synchro
        self._persist()
        self._sync_player_everywhere(old_id, player)
        print(f"✅  Joueur {player.first_name} {player.last_name} mis à jour partout.")

    # ---------------- DELETE ----------------
    def delete_player(self) -> None:
        """Supprime un joueur de la base joueurs (l'historique tournois reste)."""
        if not self.players:
            print("Aucun joueur.")
            return

        print("\n=== Supprimer un joueur ===")
        ordered = sorted(self.players, key=lambda p: (p.last_name, p.first_name))
        for i, p in enumerate(ordered, 1):
            print(f"{i}. {p.last_name} {p.first_name} [ID:{p.id_national}]")
        key = input("Numéro ou ID : ").strip().upper()

        # par numéro
        if key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(ordered):
                removed = ordered[idx]
                self.players.remove(removed)
                self._persist()
                print(
                    f"✅  Joueur {removed.first_name} {removed.last_name} supprimé de la base joueurs."
                )
                return
            print("Numéro invalide.")
            return

        # par ID
        for p in self.players:
            if p.id_national == key:
                self.players.remove(p)
                self._persist()
                print(
                    f"✅  Joueur {p.first_name} {p.last_name} supprimé de la base joueurs."
                )
                return

        print("Joueur introuvable.")

    # ---------------- SYNCHRO GLOBALE ----------------
    def _sync_player_everywhere(self, old_id: str, player: Player) -> None:
        """Met à jour ce joueur dans *tous* les tournois persistés.
        On n'écrase PAS les champs score ni autres données tournois.
        """
        tourneys = load_tournaments()  # liste de dicts
        fields_copy = ["id_national", "last_name", "first_name", "birth_date"]
        changed = False

        for t in tourneys:
            # update players list
            for p in t.get("players", []):
                if p.get("id_national") == old_id:
                    for f in fields_copy:
                        p[f] = getattr(player, f)
                    changed = True

            # update match ids
            for rd in t.get("rounds", []):
                for m in rd.get("matches", []):
                    if m.get("player1_id") == old_id:
                        m["player1_id"] = player.id_national
                        changed = True
                    if m.get("player2_id") == old_id:
                        m["player2_id"] = player.id_national
                        changed = True

        if changed:
            save_tournaments(tourneys)
