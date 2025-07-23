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
        # 1️⃣ Infos de base du tournoi
        self.name = name  # Nom du tournoi
        self.place = place  # Lieu où se déroule le tournoi
        self.start_date = start_date  # Date de début, format "jj/mm/aaaa"
        self.end_date = end_date  # Date de fin, format "jj/mm/aaaa"
        self.description = description  # Texte libre pour décrire le tournoi
        self.total_rounds = total_rounds  # Nombre de rounds prévus (4 par défaut)

        # 2️⃣ État général du tournoi
        self.status = (
            "non démarré"  # Statut actuel: "non démarré", "en cours" ou "terminé"
        )
        self.current_round_index = 0  # Nombre de rounds déjà joués (0 au lancement)

        # 3️⃣ Conteneurs pour stocker les participants et les rounds
        self.players = []  # Liste des objets Player inscrits
        self.rounds = []  # Liste des objets Round déjà joués

        # 4️⃣ Historique des appariements
        #    On garde une liste de tuples (ID_joueur1, ID_joueur2)
        #    pour ne pas refaire deux fois le même match
        self.history = []

    # ---------- Logique d'appariement ----------

    def _pair_players(self):
        """Crée les paires pour le round courant (système suisse simple)."""
        # Affichage visuel pour suivre l’exécution
        print("\n▶️  Démarrage de l'appariement")

        # 1️⃣ Vérification qu’on a un nombre pair de joueurs
        print("  • Étape 1: vérification du nombre de joueurs")
        if len(self.players) % 2 != 0:
            # Impossible d’apparier un joueur seul → on stoppe et on signale l’erreur
            raise ValueError("Nombre de joueurs impair : impossible d'appariement.")

        # 2️⃣ Détermination de l’ordre des joueurs
        if self.current_round_index == 0:
            # Premier round : on mélange totalement pour démarrer de façon aléatoire
            print("  • Étape 2: round 1 → mélange aléatoire")
            random.shuffle(self.players)
        else:
            # Rounds suivants : on classe par points décroissants
            print("  • Étape 2: rounds suivants → tri par points")
            self.players.sort(key=lambda p: p.points, reverse=True)

            # Dans chaque groupe de même nombre de points, on mélange pour éviter les biais
            i = 0
            while i < len(self.players):
                # On cherche la tranche de joueurs ayant exactement les mêmes points
                j = i + 1
                while (
                    j < len(self.players)
                    and self.players[j].points == self.players[i].points
                ):
                    j += 1
                # On mélange ce sous-groupe
                subset = self.players[i:j]
                random.shuffle(subset)
                # On réinjecte le sous-groupe mélangé à sa place
                self.players[i:j] = subset
                i = j  # On passe au groupe suivant

        # 3️⃣ Construction des paires sans jamais refaire un même match
        print("  • Étape 3: construction des paires sans re-matchs")
        remaining = self.players[
            :
        ]  # copie pour travailler sans modifier self.players direct
        pairs = []

        # Tant qu’il reste des joueurs à apparier :
        while remaining:
            p1 = remaining.pop(0)  # on prend le premier joueur
            # On cherche un adversaire n’ayant jamais été contre p1
            partner_idx = 0
            for k, p2 in enumerate(remaining):
                duo = (p1.national_id, p2.national_id)
                duo_r = (p2.national_id, p1.national_id)
                # si ni duo ni duo inversé ne sont dans l’historique, c’est valide
                if duo not in self.history and duo_r not in self.history:
                    partner_idx = k
                    break
            # On retire l’adversaire choisi de la liste
            p2 = remaining.pop(partner_idx)
            # On crée le Match et on l’ajoute à la liste
            pairs.append(Match(p1, p2))
            # On enregistre cet appariement pour éviter de le refaire plus tard
            self.history.append((p1.national_id, p2.national_id))

        # Fin de l’appariement
        print("✅ Appariements créés \n")
        return pairs

    def start_next_round(self):
        """Démarre le round suivant."""
        # 1️⃣ On vérifie qu’on n’a pas déjà joué tous les rounds
        if self.current_round_index >= self.total_rounds:
            raise ValueError("Tous les rounds ont déjà été joués.")

        # 2️⃣ On forme les paires de joueurs
        matches = self._pair_players()

        # 3️⃣ On crée le nouvel objet Round
        new_round = Round(name=f"Round {self.current_round_index + 1}", matches=matches)

        # 4️⃣ On l’ajoute à la liste des rounds déjà joués
        self.rounds.append(new_round)

        # 5️⃣ On passe au round suivant
        self.current_round_index += 1

        # 6️⃣ On met à jour le statut pour indiquer
        #    qu’un round est en cours
        self.status = "en cours"

    def record_results(self, results):
        """
        Enregistre les scores et clôture le round courant.
        `results` est une liste de tuples (num_round, num_match, score1, score2)
        """
        # 1️⃣ Mise à jour des scores et des points
        #    On parcourt chaque résultat fourni :
        #    - r_idx : index du round dans self.rounds
        #    - m_idx : index du match dans ce round
        #    - s1, s2: scores respectifs du joueur 1 et du joueur 2
        for r_idx, m_idx, s1, s2 in results:
            # a) On récupère l’objet Match correspondant
            match = self.rounds[r_idx].matches[m_idx]
            # b) On stocke les scores dans l’objet Match
            match.scores = (s1, s2)
            # c) On ajoute les points aux joueurs
            match.players[0].points += s1
            match.players[1].points += s2

        # 2️⃣ Clôture du round courant
        #    - current_round_index pointe sur le prochain à jouer,
        #      donc on ferme celui d’avant (index - 1)
        self.rounds[self.current_round_index - 1].close()

        # 3️⃣ Si c’était le dernier round prévu,
        #    on passe le tournoi en statut "terminé"
        if self.current_round_index >= self.total_rounds:
            self.status = "terminé"

    # ---------- Sauvegarde / Chargement ----------

    def _file_path(self):
        """Renvoie le chemin du fichier JSON du tournoi."""
        # 1️⃣ On construit le nom du fichier à partir du nom du tournoi
        #    - self.name.lower() : tout en minuscules pour homogénéité
        #    - .replace(" ", "_") : on remplace les espaces par des underscores
        #    - + ".json" : on ajoute l’extension JSON
        filename = self.name.lower().replace(" ", "_") + ".json"

        # 2️⃣ On combine le dossier DATA_DIR avec ce nom de fichier
        #    - DATA_DIR est un Path (chemin vers le dossier de sauvegarde)
        #    - l’opérateur “/” de pathlib construit le chemin complet
        return DATA_DIR / filename

    def save(self):
        """Sauvegarde le tournoi en JSON."""

        # 1️⃣ Création (si nécessaire) du dossier de stockage
        #    - parents=True : crée tous les dossiers parents manquants
        #    - exist_ok=True : ne déclenche pas d’erreur si le dossier existe déjà
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # 2️⃣ Préparation des données à enregistrer
        #    On construit un dictionnaire Python qui reflète l’état du tournoi
        data = {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "total_rounds": self.total_rounds,
            "status": self.status,
            "current_round_index": self.current_round_index,
            # Pour les joueurs, on ne stocke que leur identifiant unique
            "players": [p.national_id for p in self.players],
            # Pour chaque round, on sauve son nom, ses matchs sérialisés et ses horaires
            "rounds": [
                {
                    "name": rnd.name,
                    "matches": [m.serialize() for m in rnd.matches],
                    "start_time": rnd.start_time,
                    "end_time": rnd.end_time,
                }
                for rnd in self.rounds
            ],
            # On conserve l’historique des appariements
            "history": self.history,
        }

        # 3️⃣ Écriture du fichier JSON
        #    - open(...) : on ouvre le fichier en mode écriture "w"
        #    - encoding="utf-8" : pour gérer correctement tous les caractères
        with open(self._file_path(), "w", encoding="utf-8") as f:
            # json.dump : transforme le dict en JSON et l’écrit dans le fichier
            # indent=4       : mise en forme lisible (4 espaces)
            # ensure_ascii=False : conserve les accents et caractères spéciaux
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, filename):
        """
        Charge un tournoi depuis un fichier JSON et le renvoie.
        `filename` doit être juste le nom du fichier (ex. 'mon_tournoi.json').
        """
        # 1️⃣ Construire le chemin vers le fichier JSON
        path = DATA_DIR / filename

        # 2️⃣ Lire le contenu du fichier
        #    - ouverture en mode lecture ("r") avec encodage UTF‑8 pour gérer les accents
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)  # raw est un dict Python issu du JSON

        # 3️⃣ Créer l’objet Tournament avec les infos de base
        tour = Tournament(
            raw["name"],
            raw["place"],
            raw["start_date"],
            raw["end_date"],
            raw["description"],
            raw["total_rounds"],
        )

        # 4️⃣ Restaurer le statut et l’indice du round déjà joué
        tour.status = raw["status"]
        tour.current_round_index = raw["current_round_index"]

        # 5️⃣ Charger tous les joueurs depuis la classe Player
        #    pour pouvoir les retrouver et les associer au tournoi
        Player.load_all()
        #    Player.registry contient maintenant tous les objets Player chargés
        id_map = {p.national_id: p for p in Player.registry}
        #    Reconstruire la liste tour.players en se basant sur les IDs
        tour.players = [id_map[nid] for nid in raw["players"]]

        # 6️⃣ Recréer chaque Round et ses Matchs
        for r in raw["rounds"]:
            matches = []
            for m in r["matches"]:
                # m est typiquement [(id1, score1), (id2, score2)]
                p1 = id_map[m[0][0]]  # joueur 1
                p2 = id_map[m[1][0]]  # joueur 2
                s1 = m[0][1]  # score du joueur 1
                s2 = m[1][1]  # score du joueur 2
                # On crée le Match en passant joueurs et scores
                matches.append(Match(p1, p2, score1=s1, score2=s2))

            # Créer l’objet Round avec son nom et ses matchs
            rnd = Round(name=r["name"], matches=matches)
            # Restaurer ses heures de début et de fin (si présentes)
            rnd.start_time = r.get("start_time")
            rnd.end_time = r.get("end_time")
            # Ajouter ce round au tournoi
            tour.rounds.append(rnd)

        # 7️⃣ Restaurer l’historique des appariements
        tour.history = raw.get("history", [])

        # 8️⃣ Recalculer les points des joueurs pour obtenir un classement à jour
        tour._recalculate_points()

        # 9️⃣ Retourner l’objet Tournament reconstitué
        return tour

    # ---------- Utilitaire calcul ----------

    def _recalculate_points(self):
        """
        Remet à zéro les points, puis recompte
        d'après tous les scores chargés.
        """
        # 1️⃣ Remise à zéro des points de chaque joueur
        #    On parcourt la liste des joueurs inscrits et on met leurs points à 0.0
        for p in self.players:
            p.points = 0.0

        # 2️⃣ Recalcul des points à partir des scores de chaque match
        #    Pour chaque round déjà joué…
        for rnd in self.rounds:
            # …et pour chaque match de ce round…
            for m in rnd.matches:
                # On récupère les scores stockés dans le Match
                s1, s2 = m.scores
                # On ajoute ces scores aux points des deux joueurs
                m.players[0].points += s1
                m.players[1].points += s2

        # (Optionnel) Affichage pour vérifier
        # print("✔️ Points recalculés avec succès !")
