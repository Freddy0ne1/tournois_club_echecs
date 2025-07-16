"""services/export_csv_service.py
Fonctions d'export CSV pour les tournois (séparées du TournamentController).
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

from models.tournament import Tournament


def _slug(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]+', '_', name.strip()).strip('_').lower() or 'tournoi'


def export_tournament_csv(t: Tournament, base_dir: Path | str = "exports") -> Path:
    """Exporte un tournoi (infos, joueurs, rounds+matchs) en CSV dans un dossier horodaté.
    Retourne le Path du dossier créé.
    """
    base_dir = Path(base_dir)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = base_dir / f"{_slug(t.name)}_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Infos tournoi
    with (out_dir / "tournament_info.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "location", "start_date", "end_date", "rounds_total", "rounds_played"])
        w.writerow([t.name, t.location, t.start_date, t.end_date, t.rounds_total, len(t.rounds)])

    # 2. Joueurs
    with (out_dir / "tournament_players.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_national", "last_name", "first_name", "birth_date", "score"])
        for p in sorted(t.players, key=lambda pl: (pl.last_name, pl.first_name)):
            w.writerow([p.id_national, p.last_name, p.first_name, p.birth_date, getattr(p, "score", 0)])

    # 3. Rounds + matchs
    with (out_dir / "tournament_rounds_matches.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["round_index","round_name","round_start","round_end","match_index","player1_id","player2_id","score1","score2"])
        for r_idx, rd in enumerate(t.rounds, 1):
            st = rd.start_time.isoformat() if rd.start_time else ""
            et = rd.end_time.isoformat() if rd.end_time else ""
            if not rd.matches:
                w.writerow([r_idx, rd.name, st, et, "", "", "", "", ""])
                continue
            for m_idx, m in enumerate(rd.matches, 1):
                s1 = getattr(m,"score1", getattr(m,"score_p1", getattr(m,"score_player1","")))
                s2 = getattr(m,"score2", getattr(m,"score_p2", getattr(m,"score_player2","")))
                w.writerow([r_idx, rd.name, st, et, m_idx, m.player1_id, m.player2_id, s1, s2])

    return out_dir
