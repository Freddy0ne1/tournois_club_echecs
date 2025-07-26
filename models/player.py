"""models/player.py
Représente un joueur et garde la liste de tous les joueurs.
"""

import json
from pathlib import Path

# 1️⃣ Définition du chemin du fichier JSON contenant les données des joueurs
#    - Path(__file__)          : chemin du fichier courant (ici, player.py)
#    - .resolve()              : convertit en chemin absolu
#    - .parent.parent          : remonte de deux niveaux (dossier du projet)
#    - / "data" / "players.json" : construit le chemin vers data/players.json
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "players.json"


# -----------------------
#   CLASSE PLAYER
# -----------------------


class Player:
    """
    Représente un joueur et gère l'enregistrement global de tous les joueurs.

    Rôle :
      - Stocker les informations personnelles d'un joueur
      (nom, prénom, date de naissance, identifiant national)
      - Normaliser les données saisies (majuscules pour le nom et l'ID, capitalisation du prénom)
      - Conserver une liste globale (registry) contenant tous les joueurs créés
      - Initialiser le score (points) à zéro
    """

    # 1️⃣ Liste globale qui conserve tous les joueurs instanciés
    registry = []

    # ------- Initialisation d'un nouvel objet joueur -------
    def __init__(self, last_name, first_name, birth_date, national_id):
        """
        Initialise un joueur avec ses informations personnelles.

        Paramètres :
          - last_name   : Nom de famille du joueur
          - first_name  : Prénom du joueur
          - birth_date  : Date de naissance (au format "jj/mm/aaaa")
          - national_id : Identifiant unique du joueur (ex. AB12345)
        """

        # 2️⃣ Mise en forme pour homogénéité
        #    - Nom : majuscules
        #    - Prénom : première lettre en majuscule
        #    - ID national : majuscules
        self.last_name = last_name.upper()
        self.first_name = first_name.capitalize()
        self.birth_date = birth_date
        self.national_id = national_id.upper()

        # 3️⃣ Initialisation du score du joueur à zéro
        self.points = 0.0

        # 4️⃣ Ajoute le joueur créé dans la liste globale registry
        #    Cela permet d'accéder à tous les joueurs sans base de données
        Player.registry.append(self)

    # -----------------------
    #   CHARGEMENT DES JOUEURS
    # -----------------------

    @classmethod
    def load_all(cls):
        """
        Charge tous les joueurs depuis le fichier JSON players.json
        et remplit la liste globale registry.

        Étapes :
        1. Vide la liste existante pour repartir à zéro
        2. Vérifie si le fichier existe
        3. Lit et décode le fichier JSON
        4. Crée une instance Player pour chaque entrée
        5. Retourne la liste registry
        """
        # 1️⃣ Réinitialisation de la liste des joueurs déjà en mémoire
        cls.registry.clear()

        # 2️⃣ Si aucun fichier de sauvegarde n'existe, retourne une liste vide
        if not DATA_FILE.exists():
            return cls.registry

        # 3️⃣ Lecture et conversion JSON en gérant les erreurs
        try:
            # 🅰 Lire le fichier (UTF-8)
            text = DATA_FILE.read_text(encoding="utf-8")
            # 🅱 Convertir le contenu JSON en liste de dictionnaires
            data = json.loads(text)
        except (json.JSONDecodeError, OSError):
            # 🅲 Affiche un message d'erreur si problème d'accès ou de format
            print("⚠️  Fichier players.json introuvable ou invalide.")
            return cls.registry

        # 4️⃣ Crée un objet Player pour chaque entrée du fichier
        for attrs in data:
            # 🅰 Instancie un joueur avec les données essentielles
            p = Player(
                attrs.get("last_name", ""),
                attrs.get("first_name", ""),
                attrs.get("birth_date", ""),
                attrs.get("national_id", ""),
            )
            # 🅱 Restaure le score si présent dans le fichier
            p.points = attrs.get("points", 0.0)

        # 5️⃣ Retourne la liste des joueurs désormais en mémoire
        return cls.registry

    # -----------------------
    #   SAUVEGARDE JOUEURS
    # -----------------------

    @classmethod
    def save_all(cls):
        """
        Sauvegarde la liste des joueurs (registry) dans le fichier JSON players.json.

        Étapes :
        1. Vérifie/crée le dossier de données si nécessaire
        2. Transforme chaque objet Player en dictionnaire simple
        3. Écrit la liste de dictionnaires dans un fichier JSON lisible
        """
        # 1️⃣ S'assurer que le dossier où se trouve le fichier existe
        #    - parents=True : crée tous les dossiers parents si absents
        #    - exist_ok=True : ne lève pas d'erreur si le dossier existe déjà
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        # 2️⃣ Préparer une liste simple de dictionnaires à partir de Player.registry
        simple_list = []
        for p in cls.registry:
            # 🅰 On prend uniquement les attributs de base (pas les objets)
            simple_list.append(
                {
                    "last_name": p.last_name,
                    "first_name": p.first_name,
                    "birth_date": p.birth_date,
                    "national_id": p.national_id,
                    "points": p.points,
                }
            )

        # 3️⃣ Sauvegarder cette liste dans le fichier JSON
        try:
            # 🅰 Ouvrir le fichier en écriture (création si nécessaire)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                # 🅱 Convertir la liste en JSON
                json.dump(simple_list, f, indent=4, ensure_ascii=False)
        except OSError:
            # 🅲 Si problème d'accès ou d'écriture, afficher un message d'erreur
            print("❌ Impossible d'écrire dans players.json")
