"""models/tournament.py
Représente un tournoi d'échecs (système suisse simple).
"""

import json
import random
from pathlib import Path
from models.player import Player
from models.round import Round
from models.match import Match

# Répertoire de sauvegarde des tournois
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tournaments"


class Tournament:
    """Représente un tournoi d'échecs (système suisse simple)."""

    def __init__(self, name, place, start_date, end_date, description, total_rounds=4):
        # Infos de base
        self.name = name
        self.place = place
        self.start_date = start_date  # format "jj/mm/aaaa"
        self.end_date = end_date  # format "jj/mm/aaaa"
        self.description = description
        self.total_rounds = total_rounds

        # État du tournoi
        self.status = "non démarré"  # autres: "en cours", "terminé"
        self.current_round_index = 0  # nombre de rounds déjà joués

        # Conteneurs
        self.players = []  # liste des Player inscrits
        self.rounds = []  # liste des Round joués

        # Historique des appariements (liste de tuples d'IDs)
        self.history = []

    # ---------- Logique d'appariement ----------

    def _pair_players(self):
        """Crée les paires pour le round courant (système suisse simple)."""
        print("\n▶️  Démarrage de l'appariement")  # visuel pour débutant

        # Étape 1: vérification d'un nombre pair de joueurs
        print("  • Étape 1: vérification du nombre de joueurs")
        if len(self.players) % 2 != 0:
            raise ValueError("Nombre de joueurs impair : impossible d'appariement.")

        # Étape 2: tirage ou tri+melange
        if self.current_round_index == 0:
            print("  • Étape 2: round 1 → mélange aléatoire")
            random.shuffle(self.players)
        else:
            print("  • Étape 2: rounds suivants → tri par points")
            self.players.sort(key=lambda p: p.points, reverse=True)

            # Mélange aléatoire dans chaque groupe ex‑æquo
            i = 0
            while i < len(self.players):
                j = i + 1
                while (
                    j < len(self.players)
                    and self.players[j].points == self.players[i].points
                ):
                    j += 1
                subset = self.players[i:j]
                random.shuffle(subset)
                self.players[i:j] = subset
                i = j

        # Étape 3: construction des paires
        print("  • Étape 3: construction des paires sans re-matchs")
        remaining = self.players[:]  # copie pour bricoler sans toucher à self.players
        pairs = []

        while remaining:
            p1 = remaining.pop(0)
            partner_idx = 0
            for k, p2 in enumerate(remaining):
                duo = (p1.national_id, p2.national_id)
                duo_r = (p2.national_id, p1.national_id)
                if duo not in self.history and duo_r not in self.history:
                    partner_idx = k
                    break
            p2 = remaining.pop(partner_idx)
            pairs.append(Match(p1, p2))
            # Enregistre l'historique des appariements
            self.history.append((p1.national_id, p2.national_id))

        print("✅ Appariements créés \n")  # fin de la méthode
        return pairs

    def start_next_round(self):
        """Démarre le round suivant."""
        if self.current_round_index >= self.total_rounds:
            raise ValueError("Tous les rounds ont déjà été joués.")
        matches = self._pair_players()
        new_round = Round(name=f"Round {self.current_round_index+1}", matches=matches)
        self.rounds.append(new_round)
        self.current_round_index += 1
        self.status = "en cours"

    def record_results(self, results):
        """
        Enregistre les scores et clôture le round courant.
        `results` est une liste de tuples (num_round, num_match, score1, score2)
        """
        # Mise à jour des points
        for r_idx, m_idx, s1, s2 in results:
            match = self.rounds[r_idx].matches[m_idx]
            match.scores = (s1, s2)
            match.players[0].points += s1
            match.players[1].points += s2
        # Clôture du round
        self.rounds[self.current_round_index - 1].close()
        # Si c’était le dernier round, on termine le tournoi
        if self.current_round_index >= self.total_rounds:
            self.status = "terminé"

    # ---------- Sauvegarde / Chargement ----------

    def _file_path(self):
        """Renvoie le chemin du fichier JSON du tournoi."""
        filename = self.name.lower().replace(" ", "_") + ".json"
        return DATA_DIR / filename

    def save(self):
        """Sauvegarde le tournoi en JSON."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "total_rounds": self.total_rounds,
            "status": self.status,
            "current_round_index": self.current_round_index,
            "players": [p.national_id for p in self.players],
            "rounds": [
                {
                    "name": rnd.name,
                    "matches": [m.serialize() for m in rnd.matches],
                    "start_time": rnd.start_time,
                    "end_time": rnd.end_time,
                }
                for rnd in self.rounds
            ],
            "history": self.history,
        }
        with open(self._file_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, filename):
        """
        Charge un tournoi depuis un fichier JSON et le renvoie.
        `filename` doit être juste le nom du fichier (ex. 'mon_tournoi.json').
        """
        path = DATA_DIR / filename
        # 1) Lire le JSON
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        # 2) Créer l'objet Tournament avec les attributs de base
        tour = Tournament(
            raw["name"],
            raw["place"],
            raw["start_date"],
            raw["end_date"],
            raw["description"],
            raw["total_rounds"],
        )
        # 3) Restaurer le statut et l'indice du round
        tour.status = raw["status"]
        tour.current_round_index = raw["current_round_index"]

        # 4) Charger les joueurs existants et recréer la liste
        Player.load_all()
        id_map = {p.national_id: p for p in Player.registry}
        tour.players = [id_map[nid] for nid in raw["players"]]

        # 5) Recréer chaque Round et ses Match
        for r in raw["rounds"]:
            # Reconstitue les Match
            matches = []
            for m in r["matches"]:
                p1 = id_map[m[0][0]]
                p2 = id_map[m[1][0]]
                s1 = m[0][1]
                s2 = m[1][1]
                matches.append(Match(p1, p2, score1=s1, score2=s2))
            # 2) Crée le Round en ne passant que name et matches…
            rnd = Round(name=r["name"], matches=matches)

            # 3) …puis restaure les dates de début et fin
            rnd.start_time = r.get("start_time")
            rnd.end_time = r.get("end_time")

            tour.rounds.append(rnd)

        # 6) Restaurer l'historique des appariements
        tour.history = raw.get("history", [])

        # 7) Recalculer les points pour afficher un classement à jour
        tour._recalculate_points()

        return tour

    # ---------- Utilitaire calcul ----------

    def _recalculate_points(self):
        """
        Remet à zéro les points, puis recompte
        d'après tous les scores chargés.
        """
        # print("🔄 Recalcule des points pour affichage")
        # On remet à zéro les points de chaque joueur
        for p in self.players:
            p.points = 0.0
        # On parcourt tous les rounds et matches pour recalculer les points
        for rnd in self.rounds:
            for m in rnd.matches:
                s1, s2 = m.scores
                m.players[0].points += s1
                m.players[1].points += s2
        # print("✔️ Points recalculés")
