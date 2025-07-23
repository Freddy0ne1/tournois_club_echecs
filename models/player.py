"""models/player.py
Représente un joueur et garde la liste de tous les joueurs.
"""

import json
from pathlib import Path

# Chemin vers le fichier JSON contenant les données des joueurs
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "players.json"

# -----------------------
#   CLASSE PLAYER
# -----------------------


class Player:
    """Représente un joueur et garde la liste de tous les joueurs."""

    # 1️⃣ Liste globale de tous les joueurs créés
    registry = []

    def __init__(self, last_name, first_name, birth_date, national_id):
        """
        Initialise un joueur avec ses informations personnelles.
        last_name   : nom de famille
        first_name  : prénom
        birth_date  : date de naissance ("jj/mm/aaaa")
        national_id : identifiant unique du joueur
        """

        # 2️⃣ Mise en forme des données pour homogénéité
        #    - noms de famille en MAJUSCULES
        #    - prénoms avec une majuscule initiale
        #    - ID national en MAJUSCULES
        self.last_name = last_name.upper()
        self.first_name = first_name.capitalize()
        self.birth_date = birth_date
        self.national_id = national_id.upper()

        # 3️⃣ Initialisation des points à zéro
        self.points = 0.0

        # 4️⃣ Enregistrement du joueur dans la liste globale
        #    Cela permet de retrouver tous les joueurs chargés à tout moment
        Player.registry.append(self)

    # -----------------------
    #   CHARGEMENT DES JOUEURS
    # -----------------------

    @classmethod
    def load_all(cls):
        """Charge tous les joueurs depuis players.json dans registry."""

        # 1️⃣ Vider la liste existante pour repartir à zéro
        #    On efface tous les joueurs précédemment chargés
        cls.registry.clear()

        # 2️⃣ Si le fichier n’existe pas, on retourne une liste vide
        if not DATA_FILE.exists():
            return cls.registry

        # 3️⃣ Lecture du JSON avec gestion d’erreur
        try:
            # Lire tout le contenu textuel du fichier
            text = DATA_FILE.read_text(encoding="utf-8")
            # Transformer ce texte JSON en liste de dicts Python
            data = json.loads(text)
        except (json.JSONDecodeError, OSError):
            # En cas de problème (fichier absent, mal formé ou erreur d’accès)
            print("⚠️ Fichier joueurs.json introuvable ou invalide.")
            return cls.registry

        # 4️⃣ Création des instances Player à partir des données
        for attrs in data:
            # a) Construire un joueur avec les champs essentiels
            p = Player(
                attrs.get("last_name", ""),
                attrs.get("first_name", ""),
                attrs.get("birth_date", ""),
                attrs.get("national_id", ""),
            )
            # b) Restaurer les points si cette clé existe dans le JSON
            p.points = attrs.get("points", 0.0)

        # 5️⃣ Retourner la liste complète des joueurs chargés
        return cls.registry

    # -----------------------
    #   SAUVEGARDE JOUEURS
    # -----------------------

    @classmethod
    def save_all(cls):
        """Sauvegarde la liste registry dans players.json."""

        # 1️⃣ S’assurer que le dossier de données existe
        #    - parents=True : crée tous les dossiers parents manquants
        #    - exist_ok=True : ne signale pas d’erreur si le dossier existe déjà
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        # 2️⃣ Préparer une liste « simple » de dictionnaires
        #    pour ne pas écrire d’objets complexes dans le JSON
        simple_list = []
        for p in cls.registry:
            simple_list.append(
                {
                    "last_name": p.last_name,
                    "first_name": p.first_name,
                    "birth_date": p.birth_date,
                    "national_id": p.national_id,
                    "points": p.points,
                }
            )

        # 3️⃣ Écrire cette liste dans le fichier JSON
        try:
            # Ouvrir en écriture (mode "w") et en UTF‑8 pour garder les accents
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                # json.dump transforme le Python dict/list en texte JSON
                # indent=4 pour une mise en forme lisible
                # ensure_ascii=False pour conserver les caractères spéciaux
                json.dump(simple_list, f, indent=4, ensure_ascii=False)
        except OSError:
            # Si l’écriture échoue (problème de permissions, disque plein…)
            print("❌ Impossible d'écrire dans players.json")
