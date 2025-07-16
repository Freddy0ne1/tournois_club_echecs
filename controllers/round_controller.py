"""controllers/round_controller.py
Scores à saisir + rounds suivantes + classement.
"""

import csv
import os
from datetime import datetime
from models.tournament import Tournament
from models.match import Match
from models.round import Round


class RoundController:
    """Scores à saisir + rounds suivantes + classement."""

    # ---------------- Saisie MANUELLE des scores ----------------
    @staticmethod
    def enter_results(t: Tournament) -> bool:
        """Invite l'utilisateur à entrer le résultat de chaque match."""
        if not t.rounds:
            print("Aucun round à saisir.")
            return False

        rnd = t.rounds[-1]
        if rnd.end_time:
            print("⚠️  Les scores du round courant sont déjà enregistrés.")
            return False

        print(f"\n=== Saisie des scores — {rnd.name} ===")
        print("Formats acceptés : 1-0  |  0-1  |  0.5-0.5  |  ½-½")

        for m in rnd.matches:
            while True:
                res = input(f"{m.player1_id} vs {m.player2_id} : ").strip()
                if res == "1-0":
                    m.score1, m.score2 = 1.0, 0.0
                    break
                if res == "0-1":
                    m.score1, m.score2 = 0.0, 1.0
                    break
                if res in {"0.5-0.5", "½-½"}:
                    m.score1 = m.score2 = 0.5
                    break
                print("Saisie invalide, recommence.")

        rnd.end_time = datetime.now()

        # Mise à jour des scores cumulés
        for m in rnd.matches:
            p1 = next(p for p in t.players if p.id_national == m.player1_id)
            p2 = next(p for p in t.players if p.id_national == m.player2_id)
            p1.score += m.score1
            p2.score += m.score2

        print("✅  Tous les scores ont été enregistrés.")
        return True

    # ---------------------- Round suivant ----------------------
    @staticmethod
    def next_round(t: Tournament) -> bool:
        """Génère le round suivant en fonction des scores des joueurs."""
        if len(t.rounds) >= t.rounds_total:
            print("Tournoi fini.")
            return False
        if t.rounds and not t.rounds[-1].end_time:
            print("Finis le round courant.")
            return False
        players = sorted(t.players, key=lambda p: (-p.score, p.last_name, p.first_name))
        matches = []
        used = set()

        def played(a, b):
            return any(
                (m.player1_id == a and m.player2_id == b)
                or (m.player1_id == b and m.player2_id == a)
                for rd in t.rounds
                for m in rd.matches
            )

        for p in players:
            if p.id_national in used:
                continue
            opp = None
            for q in players:
                if q.id_national in used or q is p:
                    continue
                if not played(p.id_national, q.id_national):
                    opp = q
                    break
            if opp is None:
                opp = next(
                    q for q in players if q.id_national not in used and q is not p
                )
            matches.append(Match(p.id_national, opp.id_national))
            used.update({p.id_national, opp.id_national})
        num = len(t.rounds) + 1
        t.rounds.append(Round(name=f"Round {num}", matches=matches))
        print(f"Round {num} généré.")
        return True

    # ---------------------- Classement ----------------------
    @staticmethod
    def show_standings(t: Tournament, csv_path: str | None = None):
        """Affiche le classement des joueurs du tournoi."""
        ranked = sorted(t.players, key=lambda p: (-p.score, p.last_name, p.first_name))
        for i, p in enumerate(ranked, 1):
            print(f"{i}. {p.first_name} {p.last_name} — {p.score}")
        if csv_path:
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Rank", "ID", "Nom", "Prénom", "Score"])
                for i, p in enumerate(ranked, 1):
                    w.writerow([i, p.id_national, p.last_name, p.first_name, p.score])
            print(f"Exporté -> {csv_path}")
