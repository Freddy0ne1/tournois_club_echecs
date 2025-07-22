"""Contrôleur des tournois — gestion CRUD, déroulement et exports."""

import csv
import json

# import random
from datetime import datetime
from pathlib import Path

from models.player import Player
from models.tournament import Tournament
from views.console_view import ConsoleView

# -----------------------
#   Constantes globales
# -----------------------

# Nombre maximal de tentatives pour chaque saisie obligatoire
MAX_ATTEMPTS = 3

# Racine du projet (un niveau au-dessus du dossier courant)
BASE_DIR = Path(__file__).resolve().parents[1]

# Dossiers de données et d'export
DATA_DIR = BASE_DIR / "data" / "tournaments"
EXPORT_DIR = BASE_DIR / "export"

# Création du dossier d’export s’il n’existe pas
EXPORT_DIR.mkdir(exist_ok=True)


class TournamentController:
    """Gère la création, modification, suppression, déroulement et exports."""

    def __init__(self):
        """Initialise la liste des tournois en mémoire."""
        # Liste des tournois chargés
        self._tours = []
        # Chargement des tournois existants
        self._load()

    # -----------------------
    #   MÉTHODES D’AIDE
    # -----------------------

    def _input_nonempty(self, prompt):
        """
        Demande une saisie non vide à l'utilisateur·rice.
        Retourne la chaîne saisie, ou None si limite d'essais atteinte.
        """
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            value = input(prompt).strip()
            if value:
                return value
            attempt += 1
            # Affiche un message d'erreur avec le nombre de tentatives restantes
            print(
                f"\n🔴  Ce champ est obligatoire. ({attempt}/{MAX_ATTEMPTS}). Veuillez réessayer.\n"
            )
        print("❌ Nombre de tentatives dépassé. Opération annulée.")
        return None

    def _input_date(self, prompt):
        """
        Demande une date au format jj/mm/aaaa.
        Retourne la date validée en chaîne, ou None si limite d'essais atteinte.
        """
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            value = input(prompt).strip()
            try:
                datetime.strptime(value, "%d/%m/%Y")
                return value
            except ValueError:
                attempt += 1
                # Affiche un message d'erreur avec le nombre de tentatives restantes
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}) - (ex. 31/12/2025). Veuillez réessayer.\n"
                )
        print("\n❌ Nombre de tentatives dépassé. Opération annulée.")
        return None

    def _choose(self, action):
        """
        Affiche la liste des tournois et demande de choisir un index.
        Retourne l'objet Tournament ou None.
        """
        if not self._tours:
            print("\n🔍 Aucun tournoi disponible.")
            return None
        ConsoleView.show_tournaments(self._tours)
        choice = input(f"\nNuméro du tournoi pour {action} : ").strip()
        # Vérification de la saisie
        if not choice.isdigit():
            print("\n❌ Veuillez entrer un numéro valide.")
            return None
        idx = int(choice)
        if 1 <= idx <= len(self._tours):
            return self._tours[idx - 1]
        print("\n❌ Numéro hors plage.")
        return None

    # -----------------------
    #   CHARGEMENT / RELOAD
    # -----------------------

    def _load(self):
        """Charge tous les tournois valides depuis data/tournaments."""
        self._tours.clear()
        if not DATA_DIR.exists():
            return

        # Parcours tous les fichiers JSON dans le répertoire
        for file in DATA_DIR.glob("*.json"):
            try:
                tour = Tournament.load(file.name)
            except (ValueError, json.JSONDecodeError):
                # Fichier JSON mal formé ou contenu incorrect
                print(f"⚠️  Ignoré : impossible de charger {file.name}")
            else:
                self._tours.append(tour)

    # -----------------------
    #   SAUVEGARDE
    # -----------------------

    # Sauvegarde un tournoi dans le répertoire data/tournaments
    def _save(self, tour):
        tour.save()

    # -----------------------
    #   CRÉATION
    # -----------------------

    def create_tournament(self):
        """
        Guide la création pas à pas d'un nouveau tournoi.
        1) Nom  2) Lieu  3) Date début  4) Date fin  5) Description  6) Rounds
        """
        print("\n=== Création d'un tournoi ===\n")
        # 1) Nom du tournoi
        name = self._input_nonempty("Nom du tournoi : ")
        if name is None:
            return
        # 2) Lieu
        place = self._input_nonempty("Lieu : ")
        if place is None:
            return
        # 3) Date de début
        start_date = self._input_date("Date début (jj/mm/aaaa) : ")
        if start_date is None:
            return  # Annulation si date invalide

        # 4) Date de fin
        attempt = 0

        # On initialise end_date à None pour vérifier plus tard
        end_date = None
        for _ in range(MAX_ATTEMPTS):
            saisie = self._input_date("Date fin (jj/mm/aaaa) : ")
            if saisie is None:
                return
            dt_start = datetime.strptime(start_date, "%d/%m/%Y")
            dt_end = datetime.strptime(saisie, "%d/%m/%Y")
            if dt_end >= dt_start:
                end_date = saisie
                break
            attempt += 1
            # Affiche un message d'erreur avec le nombre de tentatives restantes
            print(
                f"\n❌ La date de fin doit être supérieure ou égale à la date de début.\
                ({attempt}/{MAX_ATTEMPTS}).\n"
            )
        if end_date is None:
            print("\n❌ Nombre de tentatives dépassé. Opération annulée.")
            return
        # 5) Description
        description = self._input_nonempty("Description         :")
        if description is None:
            return
        # 6) Nombre de tours (optionnel, par défaut 4)
        while True:
            nb = input("Nombre de tours (défaut 4) : ").strip()
            if nb == "":
                total_rounds = 4
                break
            if nb.isdigit() and int(nb) > 0:
                total_rounds = int(nb)
                break
            print("Entrez un entier positif ou laissez vide pour 4.")
        tour = Tournament(name, place, start_date, end_date, description, total_rounds)
        self._tours.append(tour)
        self._save(tour)
        print("\n✅ Tournoi créé.\n")
        print(f"--- Informations du tournoi '{tour.name}' ---\n")
        print(f"Lieu : {tour.place}")
        print(f"Dates : {tour.start_date} → {tour.end_date}")
        print(f"Description : {tour.description}")
        print(f"Nombre de tours : {tour.total_rounds}")

    def modify_tournament(self):
        """Modifie les informations d'un tournoi existant."""
        print("\n--- Modification d'un tournoi ---")
        # Choisir le tournoi à modifier
        tour = self._choose("modifier")
        if not tour:
            return
        print(f"\n--- Informations actuelles du tournoi '{tour.name}' ---")
        print(f"Lieu : {tour.place}")
        print(f"Dates : {tour.start_date} → {tour.end_date}")
        print(f"Description : {tour.description}")
        print(f"Nombre de tours : {tour.total_rounds}")

        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")
        new = input(f"Nom [{tour.name}] : ").strip()
        if new:
            tour.name = new
        new = input(f"Lieu [{tour.place}] : ").strip()
        if new:
            tour.place = new
            # Modification de la date de début
        while True:
            new = input(f"Date début [{tour.start_date}] : ").strip()
            # Laisser vide pour conserver l’ancienne valeur
            if not new:
                break
            try:
                # On vérifie le format
                datetime.strptime(new, "%d/%m/%Y")
                tour.start_date = new
                break
            except ValueError:
                print("❌ Format invalide. Exemple : 31/12/2025")

        # Modification de la date de fin
        while True:
            new = input(f"Date fin [{tour.end_date}] : ").strip()
            if not new:
                break
            try:
                # Vérification du format
                date_fin = datetime.strptime(new, "%d/%m/%Y")
                date_deb = datetime.strptime(tour.start_date, "%d/%m/%Y")
                if date_fin >= date_deb:
                    tour.end_date = new
                    break
                else:
                    print("❌ La date de fin doit être ≥ date de début.")
            except ValueError:
                print("❌ Format invalide. Exemple : 31/12/2025")

        new = input(f"Description [{tour.description}] : ").strip()
        if new:
            tour.description = new
        while True:
            nb = input(f"Nombre de tours [{tour.total_rounds}] : ").strip()
            if nb == "":
                break
            if nb.isdigit() and int(nb) > 0:
                tour.total_rounds = int(nb)
                break
            print("Entrez un entier positif ou laissez vide pour conserver.")
        self._save(tour)
        print("\n✅  Mise à jour effectuée.\n")
        print(f"--- Nouvelles informations du tournoi '{tour.name}' ---\n")
        print(f"Lieu : {tour.place}")
        print(f"Dates : {tour.start_date} → {tour.end_date}")
        print(f"Description : {tour.description}")
        print(f"Nombre de tours : {tour.total_rounds}")

    def delete_tournament(self):
        """Supprime un tournoi existant."""
        print("\n--- Suppression d'un tournoi ---")
        # Choisir le tournoi à supprimer
        tour = self._choose("supprimer")
        if not tour:
            return
        if input(f"\nSupprimer {tour.name} (o/N) ? ").lower() != "o":
            return
        path = DATA_DIR / f"{tour.name.lower().replace(' ', '_')}.json"
        if path.exists():
            path.unlink()
        self._tours.remove(tour)
        print(f"\n✅ Le tournoi '{tour.name}' - {tour.place}  a été supprimé.")

    def list_tournaments(self):
        """Affiche la liste des tournois."""
        print("\n--- Liste des tournois ---")
        ConsoleView.show_tournaments(self._tours)

    # ---------- Rapports ----------

    def list_registered_players(self):
        """Affiche les joueurs inscrits à un tournoi."""
        print("\n--- Joueurs inscrits à un tournoi ---")
        ids = set()
        for t in self._tours:
            for p in t.players:
                ids.add(p.national_id)
        if not ids:
            print("\nAucun joueur inscrit à un tournoi.\n")
            return
        registered = [p for p in Player.registry if p.national_id in ids]
        registered.sort(key=lambda p: (p.last_name, p.first_name))
        print("\n--- Joueurs inscrits à un tournoi ---")
        ConsoleView.show_players(registered)

        # Export option
        rows = [[p.last_name, p.first_name, p.national_id] for p in registered]
        headers = ["Nom", "Prénom", "ID"]
        self._ask_export(rows, headers, "joueurs_inscrits")

    # ---------- Ajouter/Retirer joueurs ----------

    def manage_players_in_tournament(self):
        """Ajoute ou retire des joueurs d'un tournoi."""
        print("\n--- Gestion des joueurs d'un tournoi ---")
        tour = self._choose("gérer les joueurs de")
        if not tour:
            return
        if tour.status != "non démarré":
            print("\n❌ Impossible après démarrage.")
            return
        while True:
            print("\n🏆 Informations du tournoi :\n")
            print(f"Nom : {tour.name}")
            print(f"Lieu : {tour.place}")
            print(f"Dates : {tour.start_date} → {tour.end_date}")
            print(f"Description : {tour.description}")
            print(f"Nombre de tours : {tour.total_rounds}")
            print(f"Joueurs inscrits : {len(tour.players)}")
            print("\n--- Ajouter ou retirer joueur(s) ---")
            print("1. Ajouter joueur(s)")
            print("2. Retirer joueur(s)")
            print("0. Retour\n")
            choice = input("Votre choix : ").strip()
            if choice == "1":
                self._add_players(tour)
            elif choice == "2":
                self._remove_players(tour)
            elif choice == "0":
                break

    def _add_players(self, tour):
        """Ajoute des joueurs à un tournoi, sans doublons et sans saisie multiple."""
        all_players = sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))
        available = [p for p in all_players if p not in tour.players]

        if not available:
            print("\n👤 Tous les joueurs sont déjà inscrits.")
            return

        # Affiche la liste numérotée des joueurs disponibles
        print("\n--- Joueurs disponibles à l'ajout ---")
        for i, p in enumerate(available, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

        nums = input("\nNuméros à ajouter (séparés par des virgules) : ")
        added = []
        seen = set()  # pour suivre les numéros déjà traités

        for token in nums.split(","):
            token = token.strip()
            if not token.isdigit():
                continue
            if token in seen:
                print(f"⚠️  Numéro {token} dupliqué, ignoré.")
                continue
            seen.add(token)

            idx = int(token) - 1
            if 0 <= idx < len(available):
                p = available[idx]
                tour.players.append(p)
                added.append(p)
            else:
                print(f"⚠️  Le numéro {token} n'est pas valide.")

        if added:
            tour.players.sort(key=lambda p: (p.last_name, p.first_name))
            self._save(tour)
            print("\n👤 Joueur(s) ajouté(s) :")
            for p in added:
                print(f"- {p.last_name} {p.first_name} [{p.national_id}]")
        else:
            print("\n👤 Aucun nouveau joueur ajouté.")

    def _remove_players(self, tour):
        """Retire un ou plusieurs joueurs d'un tournoi NON démarré, avec confirmation."""
        # 1) Vérifie qu’il y a bien des joueurs
        if not tour.players:
            print("\n👤 Aucun joueur inscrit.")
            return

        # 2) Tri alphabétique des joueurs par nom, puis prénom
        tour.players.sort(key=lambda p: (p.last_name, p.first_name))

        # 3) Affiche la liste numérotée, déjà triée
        print("\n--- Joueurs inscrits ---")
        for i, p in enumerate(tour.players, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

        # 4) Lecture des numéros à supprimer
        nums = input("\nNuméros à retirer (séparés par des virgules) : ")
        to_remove = []
        for token in nums.split(","):
            token = token.strip()
            if not token.isdigit():
                continue
            idx = int(token) - 1
            if 0 <= idx < len(tour.players):
                to_remove.append(tour.players[idx])

        if not to_remove:
            print("\n❌ Aucun numéro valide.")
            return

        # 5) Confirmation individuelle et suppression
        removed = []
        for p in to_remove:
            if input(f"Supprimer {p.last_name} {p.first_name} (o/N) ? ").lower() == "o":
                tour.players.remove(p)
                removed.append(p)

        # 6) Tri et sauvegarde après suppression
        if removed:
            tour.players.sort(key=lambda p: (p.last_name, p.first_name))
            self._save(tour)
            print("\n👤 Joueur(s) retiré(s) :")
            for p in removed:
                print(f"- {p.last_name} {p.first_name} [{p.national_id}]")
        else:
            print("Aucune suppression effectuée.")

    # ---------- Déroulement ----------

    def start_tournament(self):
        """Démarre un tournoi si suffisamment de joueurs sont inscrits."""
        print("\n--- Démarrage d'un tournoi ---")
        tour = self._choose("démarrer")
        if not tour:
            return

        # 1) Vérifie qu'il y a au moins 1 joueur
        if not tour.players:
            print("\n❌ Impossible : aucun joueur n'est inscrit.")
            return

        # 2) Vérifie qu'il y a un nombre pair de joueurs (et ≥ 2)
        count = len(tour.players)
        if count < 2 or count % 2 != 0:
            print("\n❌ Il faut un nombre pair de joueurs (au moins 2).")
            return

        # 3) Si le tournoi est terminé, on arrête tout de suite
        if tour.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tour.name}' est déjà terminé.")
            return

        # 4) Si le statut en cours
        if tour.status in ("en cours"):
            print(f"\nℹ️  Statut du tournoi '{tour.name}' : {tour.status}.")
            print(
                "💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
            )
            return

        # 4) Affiche que le tournoi a démarré,les joueurs inscrits, et round total
        print(f"\n🏁 Tournoi '{tour.name}' démarré.\n")
        print(f"Joueurs inscrits : {len(tour.players)}")
        print(f"Nombre de rounds : {tour.total_rounds}\n")

        # 5) Passe en statut 'en cours' et crée le premier round
        tour.status = "en cours"
        tour.start_next_round()
        self._save(tour)

        # 6) Affiche les appariements
        for idx, rnd in enumerate(tour.rounds, 1):
            print(f"\n🥊 Round {idx} :")
            for m in rnd.matches:
                p1, p2 = m.players
                print(
                    f"{p1.last_name} {p1.first_name} [{p1.national_id}] VS "
                    f"{p2.last_name} {p2.first_name} [{p2.national_id}]"
                )
        print(
            "\n💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
        )

    def enter_scores_current_round(self):
        """Saisit les scores du round en cours, ou affiche un message si non démarré/terminé."""
        print("\n--- Saisie des scores du round en cours ---")
        tour = self._choose("saisir les scores")
        if not tour:
            return

        # Cas où le tournoi n'a pas encore démarré
        if tour.status == "non démarré":
            print("\n❌ Impossible : Le tournoi n'a pas encore démarré.")
            print("💡 Utilisez l'option 6 du menu Tournoi pour démarrer le tournoi.")
            return

        # Cas où le tournoi est terminé
        if tour.status == "terminé":
            print(f"\nℹ️  Le tournoi '{tour.name}' est déjà terminé.")
            return

        # À partir d'ici, status == "en cours"
        rnd = tour.rounds[-1]
        num = tour.current_round_index  # numéro du round 1-based

        # Cas où ce round est déjà clôturé
        if rnd.end_time:
            print("\n🥊 Round déjà joué.")
            print(
                "💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant."
            )
            print(f"\n--- Récapitulatif du round {num} ---")
            for m in rnd.matches:
                p1, p2 = m.players
                s1, s2 = m.scores
                print(
                    f"{p1.last_name} {p1.first_name} {s1} - {s2} {p2.last_name} {p2.first_name}"
                )
            return

        # Sinon, on procède à la saisie des scores
        print(f"\n===== Score du tournoi {tour.name} =====")
        print("📌 Rappel : format 1-0, 0-1, 0.5-0.5 (1 victoire, 0 défaite, 0.5 nul)")
        print(f"\n🥊 Round {num}\n")

        results = []
        recap = []
        for i, m in enumerate(rnd.matches, 1):
            p1, p2 = m.players
            while True:
                s = (
                    input(
                        f"{p1.last_name} {p1.first_name}[{p1.national_id}] VS "
                        f"{p2.last_name} {p2.first_name}[{p2.national_id}] : "
                    )
                    .strip()
                    .replace(" ", "")
                )
                if s in ("1-0", "0-1", "0.5-0.5"):
                    a, b = map(float, s.split("-"))
                    break
                print("❌ Exemple valide : 1-0, 0-1 ou 0.5-0.5")
            results.append((num - 1, i - 1, a, b))
            recap.append((p1, p2, a, b))

        # Enregistrement des scores et clôture du round
        tour.record_results(results)
        self._save(tour)

        # Affichage du récapitulatif juste saisi
        print(f"\n--- Récapitulatif du round {num} ---")
        for p1, p2, a, b in recap:
            print(
                f"{p1.last_name} {p1.first_name} {a} - {b} {p2.last_name} {p2.first_name}"
            )
        print("\n💾 Scores enregistrés.")
        print("💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant.")

    def start_next_round(self):
        """Démarre le round suivant du tournoi en cours."""
        print("\n--- Démarrage du round suivant ---")
        tour = self._choose("démarrer le round suivant")
        if not tour:
            return

        # 1) Si le tournoi est terminé, on arrête tout de suite
        if tour.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tour.name}' est déjà terminé.")
            return

        # 2) Si aucun round n'est encore clôturé, on ne peut pas lancer le suivant
        if tour.rounds and not tour.rounds[-1].end_time:
            print("⚠️  Il faut clôturer le round en cours avant de démarrer le suivant.")
            return

        # 3) Si on a déjà joué tous les rounds, on informe
        if tour.current_round_index >= tour.total_rounds:
            print("ℹ️  Tous les rounds ont déjà été joués.")
            return

        # 4) Sinon, on peut lancer le round
        tour.start_next_round()
        self._save(tour)
        print("🏁 Nouveau round démarré.")

    def show_leaderboard(self):
        """Affiche le classement des joueurs du tournoi."""
        # 1) Recharge les tournois (ils vont remapper chaque national_id
        #    sur l’instance Player à jour dans Player.registry)
        self.reload_tournaments()

        # 2) Affiche le titre et demande quel tournoi on veut consulter
        print("\n--- Affichage du classement ---")
        tour = self._choose("consulter le classement")
        if not tour:
            return

        # 3) Affiche le classement via la vue console
        ConsoleView.show_leaderboard(tour)

    # ---------- Rapports détaillés ----------

    def _pick_tournament(self, action):
        return self._choose(action)

    def show_tournament_header(self):
        """Affiche le nom et les dates d'un tournoi."""
        print("\n=== Selectionner un tournoi pour afficher les détails ===")
        tour = self._pick_tournament("consulter")
        if tour:
            print(f"\n{tour.name} — {tour.start_date} → {tour.end_date}\n")

    def show_tournament_players(self):
        """Affiche les joueurs d'un tournoi."""
        print("\n=== Selectionner un tournoi pour afficher les joueurs ===")
        tour = self._pick_tournament("afficher joueurs")
        if not tour:
            return
        print(f"\n--- Joueurs du tournoi {tour.name} ---")
        order = sorted(tour.players, key=lambda p: (p.last_name, p.first_name))
        ConsoleView.show_players(order)
        print("\n--- Exportation ---")
        rows = [[p.last_name, p.first_name, p.national_id] for p in order]
        headers = ["Nom", "Prénom", "ID"]
        self._ask_export(rows, headers, f"joueurs_{tour.name}")

    def show_all_rounds_and_matches(self):
        """Affiche tous les rounds et matches d'un tournoi."""
        print("\n=== Selectionner un tournoi pour afficher les rounds et matches ===")
        tour = self._pick_tournament("afficher rounds & matches")
        if not tour or not tour.rounds:
            print("Aucun round disponible.")
            return
        for idx, rnd in enumerate(tour.rounds, 1):
            print(f"\n🥊 Round {idx} :")
            for m in rnd.matches:
                p1, p2 = m.players
                s1, s2 = m.scores
                print(
                    f"{p1.last_name} {p1.first_name}[{p1.national_id}] "
                    f"{s1} - {s2} {p2.last_name} {p2.first_name}[{p2.national_id}]"
                )
        print()
        rows = []
        for idx, rnd in enumerate(tour.rounds, 1):
            for m in rnd.matches:
                p1, p2 = m.players
                s1, s2 = m.scores
                rows.append(
                    [
                        f"Round {idx}",
                        f"{p1.last_name} {p1.first_name}",
                        f"{p2.last_name} {p2.first_name}",
                        s1,
                        s2,
                    ]
                )
        headers = ["Round", "Joueur 1", "Joueur 2", "Score 1", "Score 2"]
        name = f"rounds_{tour.name.lower().replace(' ', '_')}"
        self._ask_export(rows, headers, name)

    # ---------- Export utilitaire (csv ou html) ----------

    def _export(self, rows, headers, filename, fmt="csv"):
        path = EXPORT_DIR / f"{filename}.{fmt}"
        if fmt == "csv":
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
        else:
            with path.open("w", encoding="utf-8") as f:
                f.write("<table border='1'>\n<tr>")
                for h in headers:
                    f.write(f"<th>{h}</th>")
                f.write("</tr>\n")
                for row in rows:
                    cells = "".join(f"<td>{c}</td>" for c in row)
                    f.write(f"<tr>{cells}</tr>\n")
                f.write("</table>")
        print(f"✓ Exporté dans : {path.resolve()}")

    def _ask_export(self, rows, headers, default_name):
        if input("\nExporter ce rapport ? (o/N) ").lower() == "o":
            fmt = input("Format csv ou html ? ").lower()
            if fmt not in ("csv", "html"):
                fmt = "csv"
            self._export(rows, headers, default_name, fmt)

    def reload_tournaments(self):
        """Recharge la liste des tournois depuis les fichiers JSON."""
        self._load()

    def update_player_references(self, updated_player):
        """
        Pour chaque tournoi chargé, remplace l'ancien objet Player
        (même national_id) par updated_player dans tour.players.
        """
        for tour in self._tours:
            changed = False
            for idx, p in enumerate(tour.players):
                if p.national_id == updated_player.national_id:
                    tour.players[idx] = updated_player
                    changed = True
            if changed:
                # sauvegarde pour persister le lien Player→tour
                self._save(tour)
