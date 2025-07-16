"""controllers/tournament_controller.py
Tournament Controller - CRUD, start, persistence.
Rapports (affichage) + wrapper d'export CSV (tournoi choisi) délégué à services.export_csv_service.
"""

from dataclasses import asdict, fields
from datetime import datetime
from typing import List, Optional, Dict
import random

from services.storage_service import load_tournaments, save_tournaments, load_players
from services.export_csv_service import export_tournament_csv
from models.tournament import Tournament
from models.player import Player
from models.match import Match
from models.round import Round


# ---------- dict->dataclass ----------
def _dict_to_player(d) -> Player:
    return Player(**d) if isinstance(d, dict) else d


def _dict_to_match(d) -> Match:
    return Match(**d) if isinstance(d, dict) else d


def _dict_to_round(d) -> Round:
    if isinstance(d, Round):
        return d
    matches = [_dict_to_match(m) for m in d.get("matches", [])]
    start = (
        datetime.fromisoformat(d["start_time"])
        if isinstance(d["start_time"], str)
        else d["start_time"]
    )
    end = None
    if d.get("end_time"):
        end = (
            datetime.fromisoformat(d["end_time"])
            if isinstance(d["end_time"], str)
            else d["end_time"]
        )
    return Round(name=d["name"], start_time=start, end_time=end, matches=matches)


class TournamentController:
    """CRUD Tournois + démarrage, persistance.
    Rapports + export CSV (tournoi choisi).
    Option 1: joueurs inscrits (tous tournois).
    Option 2: sélectionner un tournoi pour voir les joueurs.
    """

    def __init__(self) -> None:
        allowed = {f.name for f in fields(Tournament)}
        raw = load_tournaments()
        self.tourneys: List[Tournament] = [
            Tournament(**{k: v for k, v in d.items() if k in allowed}) for d in raw
        ]
        for t in self.tourneys:
            t.players = [_dict_to_player(p) for p in t.players]
            t.rounds = [_dict_to_round(r) for r in t.rounds]
        self.refresh_players()

    # ----- persistence -----
    def _persist(self) -> None:
        save_tournaments([asdict(t) for t in self.tourneys])

    def save(self) -> None:
        """Sauvegarde les tournois et les joueurs."""
        self._persist()

    # ----- rehydration helpers -----
    @staticmethod
    def _to_player(d):
        return Player(**d) if isinstance(d, dict) else d

    @staticmethod
    def _to_match(d):
        return Match(**d) if isinstance(d, dict) else d

    @staticmethod
    def _to_round(d):
        if isinstance(d, Round):
            return d
        matches = [TournamentController._to_match(m) for m in d.get("matches", [])]
        start = (
            datetime.fromisoformat(d["start_time"])
            if isinstance(d["start_time"], str)
            else d["start_time"]
        )
        end = None
        if d.get("end_time"):
            end = (
                datetime.fromisoformat(d["end_time"])
                if isinstance(d["end_time"], str)
                else d["end_time"]
            )
        return Round(name=d["name"], start_time=start, end_time=end, matches=matches)

    # ----- players -----
    def refresh_players(self) -> None:
        """Recharge la liste des joueurs depuis le stockage."""
        self._all_players: List[Player] = [self._to_player(p) for p in load_players()]

    # ----- dates -----
    @staticmethod
    def _prompt_date(label: str) -> datetime:
        while True:
            raw = input(f"{label} (JJ/MM/AAAA) : ").strip()
            try:
                return datetime.strptime(raw, "%d/%m/%Y")
            except ValueError:
                print("Format invalide. Exemple : 05/08/2025.")

    @staticmethod
    def _fmt_date(dt: datetime) -> str:
        return dt.strftime("%d/%m/%Y")

    # ----- select tournament -----
    def select_tournament(self) -> Optional[Tournament]:
        """Sélectionne un tournoi par son numéro ou son nom."""
        print("\n=== Sélectionnez un tournoi ===")
        if not self.tourneys:
            print("Aucun tournoi.")
            return None
        for idx, t in enumerate(self.tourneys, 1):
            print(f"{idx}. {t.name} — {t.start_date}->{t.end_date}")
        key = input("Numéro ou NOM : ").strip()
        if key.isdigit():
            i = int(key) - 1
            if 0 <= i < len(self.tourneys):
                return self.tourneys[i]
        for t in self.tourneys:
            if t.name.casefold() == key.casefold():
                return t
        print("Introuvable.")
        return None

    # ----- create -----
    def create_tournament(self) -> None:
        """Création d'un tournoi."""
        print("\n=== Création d'un tournoi ===")
        name = input("Nom du tournoi à créer : ").strip().title()
        loc = input("Lieu : ").strip().title()
        start_dt = self._prompt_date("Date début")
        while True:
            end_dt = self._prompt_date("Date fin")
            if end_dt < start_dt:
                print("La date de fin doit être >= date début.")
            else:
                break
        desc = input("Description : ").strip()
        rt = int(input("Nombre de rounds (déf.4) : ") or 4)
        self.tourneys.append(
            Tournament(
                name, loc, self._fmt_date(start_dt), self._fmt_date(end_dt), desc, rt
            )
        )
        self.save()
        print(f"✅ Tournoi {name} créé avec succés.")

    # ----- list -----
    def list_tournaments(self) -> None:
        """Affiche la liste des tournois."""
        print("\n=== Liste des tournois ===")
        if not self.tourneys:
            print("Aucun tournoi.")
            return
        for idx, t in enumerate(self.tourneys, 1):
            finished = (
                t.rounds and len(t.rounds) == t.rounds_total and t.rounds[-1].end_time
            )
            status = " [Terminé]" if finished else ""
            print(
                f"{idx}. {t.name} — {t.start_date}->{t.end_date} ({t.location}){status}"
            )

    # ----- add players -----
    def _add_players(self, t: Tournament) -> bool:
        print(f"\n=== Ajouter des joueurs à {t.name} ===")
        self.refresh_players()
        if not self._all_players:
            print("Pas de joueurs.")
            return False
        for idx, p in enumerate(self._all_players, 1):
            print(f"{idx}. {p.first_name} {p.last_name} [ID:{p.id_national}]")
        raw = input("Numéros (virgules) : ").strip()
        try:
            idxs = {int(x.strip()) - 1 for x in raw.split(",") if x.strip()}
        except ValueError:
            print("Saisie invalide.")
            return False
        selected = [
            self._all_players[i]
            for i in idxs
            if 0 <= i < len(self._all_players) and self._all_players[i] not in t.players
        ]
        if len(selected) == 0 or len(selected) % 2 != 0:
            print("Il faut un nombre pair de joueurs.")
            return False
        t.players.extend(selected)
        return True

    # ----- start -----
    def start_tournament(self) -> None:
        """Démarre un tournoi en générant le premier round."""
        print("\n=== Démarrer un tournoi ===")
        t = self.select_tournament()
        if not t:
            return
        if not t.players and not self._add_players(t):
            return
        if len(t.players) % 2 != 0:
            print("Nombre impair")
            return
        if t.rounds:
            print("Déjà démarré")
            return
        players = t.players.copy()
        random.shuffle(players)
        matches = [
            Match(players[i].id_national, players[i + 1].id_national)
            for i in range(0, len(players), 2)
        ]
        t.rounds.append(Round(name="Round 1", matches=matches))
        self.save()
        print("Round 1 généré :")
        for m in matches:
            print(f"{m.player1_id} vs {m.player2_id}")

    # ----- update -----
    def update_tournament(self) -> None:
        """Met à jour les informations d'un tournoi."""
        print("\n=== Mettre à jour un tournoi ===")
        t = self.select_tournament()
        if not t:
            return
        t.name = input(f"Nom [{t.name}] : ").strip().title() or t.name
        t.location = input(f"Lieu [{t.location}] : ").strip().title() or t.location
        t.description = (
            input(f"Description [{t.description}] : ").strip() or t.description
        )
        raw = input(f"Date début [{t.start_date}] (Entrée = inchangé) : ").strip()
        if raw:
            try:
                start_dt = datetime.strptime(raw, "%d/%m/%Y")
                t.start_date = self._fmt_date(start_dt)
            except ValueError:
                print("Date début ignorée (format invalide).")
        raw = input(f"Date fin [{t.end_date}] (Entrée = inchangé) : ").strip()
        if raw:
            try:
                end_dt = datetime.strptime(raw, "%d/%m/%Y")
                try:
                    start_dt_cmp = datetime.strptime(t.start_date, "%d/%m/%Y")
                except ValueError:
                    start_dt_cmp = end_dt
                if end_dt < start_dt_cmp:
                    print("Fin < début : valeur ignorée.")
                else:
                    t.end_date = self._fmt_date(end_dt)
            except ValueError:
                print("Date fin ignorée (format invalide).")
        try:
            t.rounds_total = int(
                input(f"Nb rounds [{t.rounds_total}] : ") or t.rounds_total
            )
        except ValueError:
            print("Valeur invalide.")
        self.save()
        print("Tournoi mis à jour.")

    # ----- delete -----
    def delete_tournament(self) -> None:
        """Supprime un tournoi de la base."""
        print("\n=== Supprimer un tournoi ===")
        t = self.select_tournament()
        if t:
            self.tourneys.remove(t)
            self.save()
            print(f"✅ Tournoi {t.name} supprimé.")

    # ----- refresh_from_disk -----
    def refresh_from_disk(self) -> None:
        """Recharge les tournois depuis le stockage."""
        allowed = {f.name for f in fields(Tournament)}
        raw = load_tournaments()
        self.tourneys = [
            Tournament(**{k: v for k, v in d.items() if k in allowed}) for d in raw
        ]
        for t in self.tourneys:
            t.players = [self._to_player(p) for p in t.players]
            t.rounds = [self._to_round(r) for r in t.rounds]

    # ----- list players in tournament -----
    def list_players_in_tournament(self) -> None:
        """Affiche les joueurs inscrits dans un tournoi."""
        t = self.select_tournament()
        if not t:
            return
        if not t.players:
            print(f"Aucun joueur inscrit dans {t.name}.")
            return
        print(f"\n=== Joueurs de {t.name} ===")
        for idx, p in enumerate(
            sorted(t.players, key=lambda pl: (pl.last_name, pl.first_name)), 1
        ):
            print(
                f"{idx}. {p.last_name} {p.first_name} [ID:{p.id_national}] Score:{p.score}"
            )

    # ============================= RAPPORTS =============================
    def report_menu(self) -> None:
        """Affiche le menu des rapports."""
        print("\n=== Menu Rapports ===")
        while True:
            print("\n--- RAPPORTS ---")
            print("1. Joueurs inscrits (tous tournois) A->Z")
            print("2. Joueurs d'un tournoi (sélection) A->Z")
            print("3. Tous les tournois (en cours & terminés)")
            print("4. Nom et dates d’un tournoi")
            print("5. Tous les tours & matchs d’un tournoi")
            print("6. Exporter en CSV (tournoi choisi)")
            print("0. Retour")
            ch = input("> ").strip()
            match ch:
                case "1":
                    self.report_all_players()
                case "2":
                    self.report_players_per_tournament()
                case "3":
                    self.report_all_tournaments()
                case "4":
                    self.report_name_dates()
                case "5":
                    self.report_rounds_matches()
                case "6":
                    self.export_tournament_csv_wrapper()
                case "0":
                    return
                case _:
                    print("Choix invalide.")

    # ---- [1] joueurs inscrits (tous tournois) ----
    def report_all_players(self) -> None:
        """Affiche tous les joueurs inscrits dans les tournois."""
        print("\n=== Joueurs inscrits (tous tournois) ===")
        seen: Dict[str, Player] = {}
        for t in self.tourneys:
            for p in t.players:
                seen[p.id_national] = p
        if not seen:
            print("Aucun joueur inscrit dans un tournoi.")
            return
        print("\n=== Joueurs inscrits (tous tournois) ===")
        ordered = sorted(seen.values(), key=lambda pl: (pl.last_name, pl.first_name))
        for p in ordered:
            print(
                f"- {p.last_name} {p.first_name} [ID:{p.id_national}] Naiss:{p.birth_date}"
            )

    # ---- [2] joueurs d'un tournoi (sélection) ----
    def report_players_per_tournament(self) -> None:
        """Affiche les joueurs d'un tournoi sélectionné."""
        print("\n=== Joueurs d'un tournoi ===")
        if not self.tourneys:
            print("Aucun tournoi.")
            return
        t = self.select_tournament()
        if not t:
            return
        print(f"\n--- Joueurs de {t.name} ({t.start_date}->{t.end_date}) ---")
        if not t.players:
            print("Aucun joueur.")
            return
        for p in sorted(t.players, key=lambda pl: (pl.last_name, pl.first_name)):
            sc = getattr(p, "score", 0)
            print(f"- {p.last_name} {p.first_name} [ID:{p.id_national}] Score:{sc}")

    # ---- [3] tous les tournois ----
    def report_all_tournaments(self) -> None:
        """Affiche tous les tournois (en cours & terminés)."""
        print("\n=== Tous les tournois ===")
        if not self.tourneys:
            print("Aucun tournoi.")
            return
        print("\n=== Tous les tournois ===")
        for i, t in enumerate(self.tourneys, 1):
            finished = (
                t.rounds and len(t.rounds) == t.rounds_total and t.rounds[-1].end_time
            )
            status = (
                " (Terminé)"
                if finished
                else " (En cours)" if t.rounds else " (Non démarré)"
            )
            print(f"{i}. {t.name} {t.start_date}->{t.end_date} {status}")

    # ---- [4] nom & dates ----
    def report_name_dates(self) -> None:
        """Affiche le nom et les dates d'un tournoi."""
        print("\n=== Nom et dates d'un tournoi ===")
        t = self.select_tournament()
        if not t:
            return
        print(f"\n=== Tournoi : {t.name} ===")
        print(f"Lieu  : {t.location}")
        print(f"Dates : {t.start_date} -> {t.end_date}")
        print(f"Rounds prévus : {t.rounds_total}")
        print(f"Rounds joués  : {len(t.rounds)}")

    # ---- [5] rounds & matchs ----
    def report_rounds_matches(self) -> None:
        """Affiche les rounds et matchs d'un tournoi."""
        t = self.select_tournament()
        if not t:
            return
        print(f"\n=== Rounds & Matchs : {t.name} ===")
        if not t.rounds:
            print("Le tournoi n'a pas encore démarré.")
            return
        idmap = {p.id_national: p for p in t.players}
        self.refresh_players()
        for gp in self._all_players:
            idmap.setdefault(gp.id_national, gp)
        for r_idx, rd in enumerate(t.rounds, 1):
            st = rd.start_time.strftime("%Y-%m-%d %H:%M") if rd.start_time else "?"
            et = rd.end_time.strftime("%Y-%m-%d %H:%M") if rd.end_time else "…"
            print(f"\nRound {r_idx} – {rd.name} ({st} -> {et})")
            if not rd.matches:
                print("  (aucun match)")
                continue
            for m_idx, m in enumerate(rd.matches, 1):
                p1 = idmap.get(m.player1_id)
                p2 = idmap.get(m.player2_id)
                n1 = f"{p1.first_name} {p1.last_name}" if p1 else m.player1_id
                n2 = f"{p2.first_name} {p2.last_name}" if p2 else m.player2_id
                s1 = getattr(
                    m,
                    "score1",
                    getattr(m, "score_p1", getattr(m, "score_player1", None)),
                )
                s2 = getattr(
                    m,
                    "score2",
                    getattr(m, "score_p2", getattr(m, "score_player2", None)),
                )
                score_txt = f"{s1}-{s2}" if (s1 is not None and s2 is not None) else "?"
                print(f"  {m_idx}. {n1} vs {n2} [{score_txt}]")

    # ----- export CSV wrapper -----
    def export_tournament_csv_wrapper(self):
        """Export CSV pour le tournoi sélectionné."""
        print("\n=== Export CSV Tournoi ===")
        t = self.select_tournament()
        if not t:
            return None
        out_dir = export_tournament_csv(t)
        print(f"Export CSV terminé : {out_dir}")
        return out_dir
