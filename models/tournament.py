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

# -----------------------
#   INITIALISATION DU TOURNOI
# -----------------------


class Tournament:
    """
    Représente un tournoi d'échecs basé sur un système suisse simple.

    Attributs :
        - name           : Nom du tournoi
        - place          : Lieu où se déroule le tournoi
        - start_date     : Date de début ("jj/mm/aaaa")
        - end_date       : Date de fin ("jj/mm/aaaa")
        - description    : Description courte du tournoi
        - total_rounds   : Nombre de rounds prévus (par défaut : 4)
        - status         : Statut actuel ("non démarré", "en cours", "terminé")
        - current_round_index : Nombre de rounds déjà joués
        - players        : Liste des joueurs inscrits (objets Player)
        - rounds         : Liste des rounds joués (objets Round)
        - history        : Historique des matchs (tuples d'ID de joueurs)
    """

    # ------- Initialisation d'un nouvel objet tournoi -------
    def __init__(self, name, place, start_date, end_date, description, total_rounds=4):
        """
        Initialise un nouveau tournoi avec ses informations principales.
        """

        # 1️⃣ Informations générales du tournoi
        self.name = name  # Nom du tournoi
        self.place = place  # Lieu où il se déroule
        self.start_date = start_date  # Date de début (format jj/mm/aaaa)
        self.end_date = end_date  # Date de fin (format jj/mm/aaaa)
        self.description = description  # Courte description
        self.total_rounds = total_rounds  # Nombre de rounds prévus (par défaut 4)

        # 2️⃣ Suivi de l'état du tournoi
        #    - "non démarré" par défaut
        #    - "en cours" après lancement
        #    - "terminé" à la fin
        self.status = "non démarré"
        self.current_round_index = 0  # Nombre de rounds joués (aucun au début)

        # 3️⃣ Participants et rounds
        self.players = []  # Liste d'objets Player inscrits
        self.rounds = []  # Liste d'objets Round générés au fur et à mesure

        # 4️⃣ Historique des matchs joués (évite de rejouer les mêmes)
        #    Chaque élément est un tuple (ID_joueur1, ID_joueur2)
        self.history = []

    # -----------------------
    #   APPARIEMENT DES JOUEURS
    # -----------------------

    # ------- Génération des appariements de joueurs (système suisse) -------
    def _pair_players(self):
        """
        Crée les paires pour le round courant selon le système suisse.
        Étapes :
        1. Vérifie qu'il y a un nombre pair de joueurs.
        2. Prépare l'ordre des joueurs (aléatoire au 1er round, par points sinon).
        3. Génère les paires en évitant les matches déjà joués.
        Retourne une liste d'objets Match.
        """
        print("\n▶️  Démarrage de l'appariement")

        # 1️⃣ Vérifie que le nombre de joueurs est valide
        self._check_even_players()

        # 2️⃣ Prépare l'ordre des joueurs selon le round
        self._prepare_players_order()

        # 3️⃣ Construit les appariements et retourne la liste
        pairs = self._build_pairs()
        print("✅ Appariements créés \n")
        return pairs

    # ------- Vérification que le nombre de joueurs est pair -------
    def _check_even_players(self):
        """
        Vérifie que le nombre de joueurs est pair.
        Étapes :
        1. Affiche une étape d'information.
        2. Lève une erreur si le nombre de joueurs est impair.
        """
        # 1️⃣ Affiche l'étape de vérification
        print("  • Étape 1: vérification du nombre de joueurs")

        # 2️⃣ Si le nombre de joueurs est impair, on bloque le processus
        if len(self.players) % 2 != 0:
            raise ValueError("Nombre de joueurs impair : impossible d'appariement.")

    # ------- Préparer l'ordre des joueurs avant un round -------
    def _prepare_players_order(self):
        """
        Prépare l'ordre des joueurs pour le round courant.
        Étapes :
        1. Si c'est le premier round, mélange aléatoirement tous les joueurs.
        2. Sinon, trie par points décroissants et mélange les groupes de joueurs
        ayant le même nombre de points.
        """
        # 1️⃣ Premier round : ordre aléatoire complet
        if self.current_round_index == 0:
            print("  • Étape 2: round 1 → mélange aléatoire")
            random.shuffle(self.players)
        else:
            # 2️⃣ Rounds suivants : tri par points décroissants
            print("  • Étape 2: rounds suivants → tri par points")
            self.players.sort(key=lambda p: p.points, reverse=True)
            # Puis mélange des groupes de points égaux
            self._shuffle_equal_points_groups()

    # ------- Mélanger les groupes de joueurs avec le même nombre de points -------
    def _shuffle_equal_points_groups(self):
        """
        Mélange aléatoirement les sous-groupes de joueurs ayant le même nombre de points.
        """
        # 1️⃣ Parcourt la liste des joueurs et identifie les groupes par points
        i = 0
        while i < len(self.players):
            j = i + 1
            while (
                j < len(self.players)
                and self.players[j].points == self.players[i].points
            ):
                j += 1

            # 2️⃣ Mélange le sous-groupe et le réinjecte dans la liste principale
            subset = self.players[i:j]
            random.shuffle(subset)
            self.players[i:j] = subset

            # 3️⃣ Passe au groupe suivant
            i = j

    # ------- Construction des appariements pour un round -------
    def _build_pairs(self):
        """
        Construit la liste des paires de joueurs pour ce round.
        Étapes :
        1. Travaille sur une copie de la liste des joueurs restants.
        2. Retire les joueurs un à un et leur trouve un partenaire disponible.
        3. Crée les objets Match et met à jour l'historique des appariements.
        4. Retourne la liste des paires.
        """
        print("  • Étape 3: construction des paires sans re-matchs")

        # 1️⃣ Copie de la liste des joueurs pour travailler proprement
        remaining = self.players[:]
        pairs = []

        # 2️⃣ Boucle tant qu'il reste des joueurs à apparier
        while remaining:
            p1 = remaining.pop(0)
            # Trouver l'indice du partenaire compatible
            partner_idx = self._find_partner_index(p1, remaining)
            # Retirer le partenaire et créer un match
            p2 = remaining.pop(partner_idx)
            pairs.append(Match(p1, p2))
            # Ajouter cet appariement à l'historique
            self.history.append((p1.national_id, p2.national_id))

        return pairs

    # ------- Recherche d'un partenaire valide pour l'appariement -------
    def _find_partner_index(self, p1, remaining):
        """
        Trouve l'indice du partenaire valide pour p1 parmi les joueurs restants.
        Critère :
        - Le duo (p1, p2) ne doit pas avoir déjà été rencontré dans l'historique.
        """
        # 1️⃣ Parcourt tous les joueurs restants
        for k, p2 in enumerate(remaining):
            duo = (p1.national_id, p2.national_id)
            duo_r = (p2.national_id, p1.national_id)
            # 2️⃣ Vérifie si cette paire est nouvelle
            if duo not in self.history and duo_r not in self.history:
                return k
        # 3️⃣ Si aucun partenaire valide trouvé, prend le premier par défaut
        return 0

    # -----------------------
    #   DÉMARRAGE ROUND SUIVANT
    # -----------------------

    def start_next_round(self):
        """
        Démarre le round suivant dans le tournoi.
        Étapes :
        1. Vérifie que tous les rounds prévus n'ont pas déjà été joués.
        2. Génère les appariements des joueurs via _pair_players().
        3. Crée un objet Round pour ce nouveau round.
        4. Ajoute ce round à la liste des rounds existants.
        5. Met à jour l'indice du round courant.
        6. Met à jour le statut du tournoi pour indiquer qu'il est en cours.
        """

        # 1️⃣ Vérifie qu'il reste encore des rounds à jouer
        if self.current_round_index >= self.total_rounds:
            raise ValueError("Tous les rounds ont déjà été joués.")

        # 2️⃣ Crée les appariements pour ce round
        matches = self._pair_players()

        # 3️⃣ Instancie un nouvel objet Round pour représenter ce round
        new_round = Round(name=f"Round {self.current_round_index + 1}", matches=matches)

        # 4️⃣ Ajoute ce round à la liste des rounds déjà créés
        self.rounds.append(new_round)

        # 5️⃣ Incrémente l'indice du round courant
        self.current_round_index += 1

        # 6️⃣ Met à jour le statut général du tournoi
        self.status = "en cours"

    # -----------------------
    #   ENREGISTREMENT DES SCORES
    # -----------------------

    def record_results(self, results):
        """
        Enregistre les scores des matchs d'un round et met à jour l'état du tournoi.

        Paramètres
        ----------
        results : list[tuple]
            Liste de tuples au format (num_round, num_match, score1, score2)
            - num_round : index du round (0-based)
            - num_match : index du match dans ce round
            - score1 / score2 : points attribués aux deux joueurs

        Étapes :
        1. Met à jour les scores et les points pour chaque match.
        2. Clôture le round en cours (mise à jour de end_time).
        3. Si le dernier round vient d'être joué, passe le tournoi en statut "terminé".
        """

        # 1️⃣ Mise à jour des scores et des points
        for r_idx, m_idx, s1, s2 in results:
            # a) Récupère l'objet Match correspondant dans le bon round
            match = self.rounds[r_idx].matches[m_idx]
            # b) Stocke les scores dans le match
            match.scores = (s1, s2)
            # c) Ajoute les points aux joueurs
            match.players[0].points += s1
            match.players[1].points += s2

        # 2️⃣ Clôture du round en cours
        #    - current_round_index pointe vers le prochain round à jouer,
        #      donc on ferme celui qui vient d'être joué (index - 1)
        self.rounds[self.current_round_index - 1].close()

        # 3️⃣ Si le dernier round est atteint, passe le tournoi en "terminé"
        if self.current_round_index >= self.total_rounds:
            self.status = "terminé"

    # -----------------------
    #   CHEMIN DU FICHIER JSON
    # -----------------------

    def _file_path(self):
        """
        Construit et retourne le chemin complet du fichier JSON associé au tournoi.

        Étapes :
        1. Transforme le nom du tournoi en un nom de fichier standardisé.
        - tout en minuscules
        - espaces remplacés par des underscores "_"
        - ajoute l'extension .json
        2. Combine ce nom avec le dossier DATA_DIR pour former un chemin complet.

        Retour
        ------
        Path : chemin du fichier JSON où sauvegarder/charger ce tournoi
        """
        # 1️⃣ Normalise le nom du tournoi pour générer un nom de fichier sûr
        filename = self.name.lower().replace(" ", "_") + ".json"

        # 2️⃣ Construit le chemin complet en joignant DATA_DIR et le nom du fichier
        return DATA_DIR / filename

    # -----------------------
    #   SAUVEGARDE DU TOURNOI
    # -----------------------

    # ------- Sauvegarde d'un tournoi dans un fichier JSON -------
    def save(self):
        """
        Sauvegarde l'état actuel du tournoi dans un fichier JSON.

        Étapes :
        1. S'assure que le dossier de stockage existe (DATA_DIR).
        2. Prépare un dictionnaire Python représentant toutes les informations
        importantes du tournoi (joueurs, rounds, historique, etc.).
        3. Écrit ce dictionnaire dans un fichier JSON (lisible et encodé en UTF-8).
        """

        # 1️⃣ Création (si nécessaire) du dossier de stockage
        #    - parents=True : crée automatiquement les dossiers parents
        #    - exist_ok=True : ne lève pas d'erreur si le dossier existe déjà
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # 2️⃣ Préparation des données
        data = self._build_tournament_data()

        # 3️⃣ Écriture dans le fichier
        self._write_tournament_file(data)

    # ------- Construction du dictionnaire de données du tournoi -------
    def _build_tournament_data(self):
        """
        Construit un dictionnaire Python représentant complètement l'état du tournoi.

        - Les joueurs sont enregistrés uniquement par leur identifiant national.
        - Chaque round et match est converti en structure simple (serialize).
        """

        # 1️⃣ Construction de la structure de données
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "total_rounds": self.total_rounds,
            "status": self.status,
            "current_round_index": self.current_round_index,
            # On ne sauvegarde que les IDs des joueurs
            "players": [p.national_id for p in self.players],
            # Conversion des rounds en dictionnaires simples
            "rounds": [
                {
                    "name": rnd.name,
                    "matches": [m.serialize() for m in rnd.matches],
                    "start_time": rnd.start_time,
                    "end_time": rnd.end_time,
                }
                for rnd in self.rounds
            ],
            # Historique des matchs déjà joués
            "history": self.history,
        }

    # ------- Écriture des données du tournoi dans un fichier JSON -------
    def _write_tournament_file(self, data):
        """
        Écrit les données d'un tournoi dans un fichier JSON lisible.

        - indent=4 pour rendre lisible
        - ensure_ascii=False pour conserver les accents
        """
        with open(self._file_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # -----------------------
    #   CHARGEMENT D'UN TOURNOI
    # -----------------------

    # ------- Chargement d'un tournoi complet depuis un fichier JSON -------
    @classmethod
    def load(cls, filename):
        """
        Charge un tournoi depuis un fichier JSON et le retourne sous forme d'objet Tournament.

        Étapes principales :
        1. Lecture du fichier JSON.
        2. Création d'un objet Tournament avec les infos de base.
        3. Restauration du statut et de l'avancement.
        4. Association des joueurs (à partir de leurs IDs).
        5. Reconstruction des rounds et des matchs.
        6. Restauration de l'historique des appariements.
        7. Recalcul des points.

        Paramètre :
            filename (str) : nom du fichier JSON (exemple : "mon_tournoi.json")

        Retournament :
            Tournament : un objet Tournament complet et prêt à être utilisé.
        """
        # 1️⃣ Lire les données JSON brutes
        raw = cls._load_raw_data(filename)

        # 2️⃣ Créer l'objet Tournament avec les infos générales
        tournament = cls._restore_basic_info(raw)

        # 3️⃣ Restaurer les joueurs inscrits
        id_map = cls._restore_players(raw, tournament)

        # 4️⃣ Restaurer les rounds et leurs matchs
        cls._restore_rounds(raw, tournament, id_map)

        # 5️⃣ Restaurer l'historique et recalculer les points
        cls._restore_history_and_points(raw, tournament)

        return tournament

    # ------- Lecture brute des données JSON d'un tournoi -------
    @staticmethod
    def _load_raw_data(filename):
        """
        Lit un fichier JSON contenant les données d'un tournoi et
        retourne son contenu sous forme de dictionnaire.

        Paramètres :
            filename (str) : nom du fichier JSON (exemple : "mon_tournoi.json")

        Retournament :
            dict : les données du fichier JSON converties en dictionnaire Python
        """

        # 1️⃣ Construire le chemin complet vers le fichier à lire
        #    - DATA_DIR est le dossier contenant les fichiers de tournois
        #    - l'opérateur "/" permet d'ajouter le nom du fichier au chemin
        path = DATA_DIR / filename

        # 2️⃣ Ouvrir le fichier en mode lecture texte avec encodage UTF-8
        #    - "r" = read (lecture seule)
        #    - encoding="utf-8" pour bien gérer les caractères accentués
        with open(path, "r", encoding="utf-8") as f:
            # 3️⃣ Charger le contenu du fichier JSON et le convertir en dictionnaire Python
            data = json.load(f)

        # 4️⃣ Retourner les données obtenues
        return data

    # ------- Restauration des infos de base d'un tournoi -------
    @staticmethod
    def _restore_basic_info(raw):
        """
        Restaure les informations de base d'un tournoi à partir d'un dictionnaire brut
        (issu du fichier JSON) et retourne une instance de Tournament pré-remplie.

        Paramètres :
            raw (dict) : données du tournoi lues depuis le JSON

        Retournament :
            Tournament : une instance de Tournament avec ses attributs de base renseignés
        """

        # 1️⃣ Crée une nouvelle instance de Tournament en utilisant les champs principaux
        #    - Ces champs sont directement lus dans le dictionnaire `raw`
        #    - Les autres données (joueurs, rounds, historique) seront ajoutées ensuite
        tournament = Tournament(
            raw["name"],  # Nom du tournoi
            raw["place"],  # Lieu du tournoi
            raw["start_date"],  # Date de début (format "jj/mm/aaaa")
            raw["end_date"],  # Date de fin (format "jj/mm/aaaa")
            raw["description"],  # Description du tournoi
            raw["total_rounds"],  # Nombre total de rounds
        )

        # 2️⃣ Restaurer le statut du tournoi (non démarré, en cours, terminé)
        tournament.status = raw["status"]

        # 3️⃣ Restaurer l'indice du round actuel (combien de rounds ont déjà été joués)
        tournament.current_round_index = raw["current_round_index"]

        # 4️⃣ Retourner l'objet Tournament partiellement reconstruit
        return tournament

    # ------- Restauration des joueurs d'un tournoi -------
    @staticmethod
    def _restore_players(raw, tournament):
        """
        Restaure les joueurs d'un tournoi à partir des données JSON.

        Étapes :
        1. Recharge tous les joueurs existants depuis players.json.
        2. Crée une table de correspondance national_id → Player.
        3. Associe au tournoi les joueurs dont les IDs sont listés dans le JSON.

        Paramètres :
            raw (dict)   : dictionnaire contenant les données brutes du tournoi
            tournament (Tournament) : instance du tournoi à compléter avec ses joueurs

        Retournament :
            dict : table de correspondance {national_id: Player}
        """

        # 1️⃣ Charger tous les joueurs connus dans Player.registry
        #    (cela permet de retrouver les instances déjà existantes)
        Player.load_all()

        # 2️⃣ Créer un dictionnaire {ID national → instance Player}
        #    pour un accès rapide aux objets joueurs via leur identifiant unique
        id_map = {p.national_id: p for p in Player.registry}

        # 3️⃣ Associer les joueurs listés dans raw["players"] au tournoi
        #    en utilisant le dictionnaire id_map
        tournament.players = [id_map[nid] for nid in raw["players"]]

        # 4️⃣ Retourner la table id_map (utile pour la suite de la reconstruction)
        return id_map

    # ------- Restauration des rounds et des matchs -------
    @staticmethod
    def _restore_rounds(raw, tournament, id_map):
        """
        Reconstruit les rounds et les matchs d'un tournoi à partir des données JSON.

        Étapes :
        1. Parcourt la liste `raw["rounds"]` (chaque élément correspond à un round).
        2. Pour chaque round, recrée les matchs avec les joueurs et leurs scores.
        3. Restaure les informations temporelles (start_time, end_time).
        4. Ajoute chaque round reconstruit à l'objet `tour`.

        Paramètres :
            raw (dict)          : dictionnaire contenant toutes les données brutes du tournoi
            tournament (Tournament)   : instance de tournoi à compléter avec ses rounds
            id_map (dict)       : dictionnaire {national_id: Player} pour retrouver les joueurs
        """

        # 1️⃣ Parcourt tous les rounds contenus dans les données JSON
        for r in raw["rounds"]:
            matches = []

            # 2️⃣ Pour chaque match du round, recrée les joueurs et scores
            for m in r["matches"]:
                # m est une liste de 2 tuples : [(id_j1, score1), (id_j2, score2)]
                p1 = id_map[m[0][0]]  # Retrouver le joueur 1 par son ID
                p2 = id_map[m[1][0]]  # Retrouver le joueur 2 par son ID
                s1 = m[0][1]  # Score du joueur 1
                s2 = m[1][1]  # Score du joueur 2

                # Création d'un objet Match avec joueurs et scores restaurés
                matches.append(Match(p1, p2, score1=s1, score2=s2))

            # 3️⃣ Création du Round avec son nom et ses matchs
            rnd = Round(name=r["name"], matches=matches)

            # 4️⃣ Restauration des horaires (début et fin) s'ils sont présents
            rnd.start_time = r.get("start_time")
            rnd.end_time = r.get("end_time")

            # 5️⃣ Ajout du round reconstruit à la liste des rounds du tournoi
            tournament.rounds.append(rnd)

    # ------- Restauration de l’historique et recalcul des points -------
    @staticmethod
    def _restore_history_and_points(raw, tournament):
        """
        Restaure l'historique des appariements et recalcule les points du tournoi.

        Étapes :
        1. Récupère la clé "history" depuis les données brutes (liste des matchs déjà joués).
        2. Réassigne cette liste dans l'attribut `tournament.history`.
        3. Lance le recalcul des points de tous les joueurs inscrits via `recalculate_points()`.

        Paramètres :
            raw (dict)        : dictionnaire des données brutes du tournoi
            tournament (Tournament) : instance du tournoi à mettre à jour
        """

        # 1️⃣ Restaure la liste des appariements déjà effectués
        tournament.history = raw.get("history", [])

        # 2️⃣ Recalcule les points en fonction des scores enregistrés
        tournament.recalculate_points()

    # -----------------------
    #   RECALCUL DES POINTS
    # -----------------------

    def recalculate_points(self):
        """
        Recalcule les points des joueurs en fonction de tous les matchs joués.

        Étapes :
        1. Remet à zéro les points de tous les joueurs inscrits au tournoi.
        2. Parcourt chaque round et chaque match pour additionner les scores.
        3. Met à jour les points cumulés dans chaque objet Player.
        """

        # 1️⃣ Réinitialise les points de tous les joueurs à 0.0
        for p in self.players:
            p.points = 0.0

        # 2️⃣ Pour chaque round déjà enregistré dans le tournoi
        for rnd in self.rounds:
            # 3️⃣ Pour chaque match joué dans ce round
            for m in rnd.matches:
                # Récupère les scores des deux joueurs
                s1, s2 = m.scores

                # Ajoute les points aux joueurs correspondants
                m.players[0].points += s1
                m.players[1].points += s2
