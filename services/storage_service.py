"""services/storage_service.py
Service de stockage pour les données du tournoi, joueurs, etc.
"""

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def _load(path: Path) -> Any:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _save(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def load_players():
    """Charge la liste des joueurs depuis le fichier JSON."""
    return _load(DATA_DIR / "players.json")


def save_players(players):
    """Sauvegarde la liste des joueurs dans le fichier JSON."""
    _save(DATA_DIR / "players.json", players)


def load_tournaments():
    """Charge la liste des tournois depuis le fichier JSON."""
    return _load(DATA_DIR / "tournaments.json")


def save_tournaments(tournaments):
    """Sauvegarde la liste des tournois dans le fichier JSON."""
    _save(DATA_DIR / "tournaments.json", tournaments)
