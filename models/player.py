"""models/player.py
Représente un joueur et garde la liste de tous les joueurs.
"""

import json
from pathlib import Path

# Fichier de données pour les joueurs
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "players.json"


class Player:
    """Représente un joueur et garde la liste de tous les joueurs."""

    # liste publique de tous les joueurs chargés
    registry = []

    def __init__(self, last_name, first_name, birth_date, national_id):
        # On met en forme les données
        self.last_name = last_name.upper()
        self.first_name = first_name.capitalize()
        self.birth_date = birth_date  # format "jj/mm/aaaa"
        self.national_id = national_id.upper()
        self.points = 0.0

        # On ajoute le nouvel objet à la liste des joueurs
        Player.registry.append(self)

    @classmethod
    def load_all(cls):
        """Charge tous les joueurs depuis players.json dans registry."""
        cls.registry.clear()
        if not DATA_FILE.exists():
            return cls.registry

        # Lecture du fichier JSON
        try:
            text = DATA_FILE.read_text(encoding="utf-8")
            data = json.loads(text)
        except (json.JSONDecodeError, OSError):
            print("⚠️ Fichier joueurs.json introuvable ou invalide.")
            return cls.registry

        # Création des instances Player
        for attrs in data:
            p = Player(
                attrs.get("last_name", ""),
                attrs.get("first_name", ""),
                attrs.get("birth_date", ""),
                attrs.get("national_id", ""),
            )
            # Restaurer les points si présent
            p.points = attrs.get("points", 0.0)

        return cls.registry

    @classmethod
    def save_all(cls):
        """Sauvegarde la liste registry dans players.json."""
        # S’assure que le dossier existe
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Prépare la liste de dicts
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

        # Écrit le JSON
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(simple_list, f, indent=4, ensure_ascii=False)
        except OSError:
            print("❌ Impossible d'écrire dans players.json")
