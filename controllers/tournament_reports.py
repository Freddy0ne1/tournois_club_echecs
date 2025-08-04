"""
Module tournament_reports
Affiche les classements, rapports et propose l'export des données.
"""

import csv
from models.player import Player
from views.console_view import ConsoleView
from .tournament_controller_base import (
    TournamentControllerBase as TournamentReportsController,
    EXPORT_DIR,
    create_export_directory,
)


class TournamentReports(TournamentReportsController):
    """
    Sous-contrôleur pour l'affichage des rapports et classements,
    et la génération d'exports CSV/HTML.
    """

    # -----------------------
    #   CLASSEMENT / RAPPORTS / EXPORTS
    # -----------------------

    # ------- Affichage classement joueur d’un tournoi sélectionné -------
    def show_leaderboard(self):
        """
        Affiche le classement des joueurs pour un tournoi sélectionné.

        Étapes :
        1. Recharge les tournois depuis les fichiers
        2. Filtre uniquement les tournois démarrés ou terminés
        3. Affiche un message s'il n'y a aucun tournoi à afficher
        4. Permet à l'utilisateur de sélectionner un tournoi
        5. Affiche le classement via la vue console
        """
        # 1️⃣ Recharge les tournois à jour
        self.reload_tournaments()

        # 2️⃣ Ne conserve que les tournois en cours ou terminés (statut != "non démarré")
        eligible = sorted(
            [t for t in self._tournaments if t.status != "non démarré"],
            key=lambda t: t.name.lower(),
        )

        # 3️⃣ Si aucun tournoi éligible, affiche un message et quitte
        if not eligible:
            print("\n🔍 Aucun tournoi démarré ou terminé pour le moment.")
            print("💡 Démarrez un tournoi pour pouvoir consulter son classement.\n")
            return

        # 4️⃣ Titre et sélection du tournoi concerné
        print("\n--- Affichage du classement ---")
        tournament = self._choose("consulter le classement", tournament_list=eligible)
        if not tournament:
            return

        # 5️⃣ Affiche le classement via la vue
        ConsoleView.show_leaderboard(tournament)

    # ------- Liste de tous les joueurs inscrits à au moins un tournoi -------
    def list_registered_players(self):
        """
        Affiche la liste de tous les joueurs inscrits à au moins un tournoi.
        Étapes :
        1. Affiche un titre
        2. Collecte les identifiants uniques des joueurs inscrits
        3. Si aucun joueur trouvé, affiche un message et quitte
        4. Reconstruit la liste d'objets Player à partir du Player.registry
        5. Trie la liste par nom puis prénom
        6. Affiche les joueurs via la vue console
        7. Prépare les données pour un éventuel export
        8. Propose l'export des données (CSV, JSON, etc.)
        """
        # 1️⃣ Collecte des identifiants uniques des joueurs inscrits
        ids = set()
        for t in self._tournaments:
            for p in t.players:
                ids.add(p.national_id)

        # 2️⃣ Si aucun joueur n'est inscrit à aucun tournoi
        if not ids:
            print("\nAucun joueur inscrit à un tournoi.\n")
            return

        # 3️⃣ Construit une liste des joueurs correspondant aux IDs collectés
        registered = [p for p in Player.registry if p.national_id in ids]

        # 4️⃣ Trie les joueurs par nom puis par prénom
        registered.sort(key=lambda p: (p.last_name, p.first_name))

        # 5️⃣ Affiche la liste via la vue console
        print("\n--- Joueurs inscrits à un tournoi ---")
        ConsoleView.show_players(registered)

        # 6️⃣ Prépare les données pour un export éventuel
        rows = [[p.last_name, p.first_name, p.national_id] for p in registered]
        headers = ["Nom", "Prénom", "ID"]

        # 7️⃣ Demande à l'utilisateur s'il souhaite exporter les données
        self._ask_export(rows, headers, "joueurs_inscrits")

    # ------- Sélection d’un tournoi via la méthode _choose -------
    def _pick_tournament(self, action):
        """
        Permet de sélectionner un tournoi en utilisant la méthode _choose.
        Paramètre :
        - action : chaîne décrivant l'action (exemple : "modifier", "supprimer")
        Retour :
        - L'objet Tournament choisi ou None si annulation ou erreur.
        """

        # 1️⃣ Appelle la méthode _choose avec l'action spécifiée.
        #    _choose se charge d'afficher la liste des tournois et de lire la saisie.
        # 2️⃣ Retourne directement le tournoi sélectionné (ou None).
        return self._choose(action)

    # ------- Affichage du nom et des dates d’un tournoi sélectionné -------
    def show_tournament_header(self):
        """
        Affiche uniquement le nom et les dates d'un tournoi choisi.
        Étapes :
        1. Affiche un titre
        2. Demande à l'utilisateur de sélectionner un tournoi
        3. Affiche le nom et les dates si un tournoi est sélectionné
        """
        # 1️⃣ Affiche un titre pour guider l'utilisateur
        print("\n=== Sélectionner un tournoi pour afficher les détails ===")

        # 2️⃣ Demande à l'utilisateur de choisir un tournoi
        tournament = self._pick_tournament("consulter")

        # 3️⃣ Si un tournoi est bien sélectionné, affiche son nom et ses dates
        if tournament:
            print("\n--- Détails du tournoi sélectionné ---")
            # 🅰 Affiche le nom du tournoi
            print(f"\nNom               : {tournament.name}")
            print(f"Lieu              : {tournament.place}")
            print(
                f"Dates             : {tournament.start_date} → {tournament.end_date}"
            )
            print(f"Description       : {tournament.description}")
            print(f"Nombre de rounds  : {tournament.total_rounds}")
            print(f"Statut            : {tournament.status}\n")

    # ------- Affichage des joueurs d’un tournoi sélectionné -------
    def show_tournament_players(self):
        """
        Affiche la liste des joueurs d'un tournoi sélectionné.
        Étapes :
        1. Affiche un titre pour guider l'utilisateur
        2. Demande à l'utilisateur de choisir un tournoi
        3. Affiche la liste des joueurs du tournoi (triés par nom et prénom)
        4. Propose un export des données affichées
        """
        # 1️⃣ Affiche un titre pour guider l'utilisateur
        print("\n=== Sélectionner un tournoi pour afficher les joueurs ===")

        # 2️⃣ Demande à l'utilisateur de choisir un tournoi
        tournament = self._pick_tournament("afficher joueurs")
        if not tournament:  # 🅰 Annule si aucun tournoi n'est sélectionné
            return

        # 3️⃣ Affiche le titre de la liste des joueurs pour le tournoi choisi
        print(f"\n--- Joueurs du tournoi {tournament.name} ---")

        # 4️⃣ Trie la liste des joueurs par NOM puis prénom
        order = sorted(tournament.players, key=lambda p: (p.last_name, p.first_name))

        # 5️⃣ Affiche les joueurs via la vue console
        ConsoleView.show_players(order)

        # 6️⃣ Prépare les données pour une exportation éventuelle
        print("\n--- Exportation ---")
        rows = [[p.last_name, p.first_name, p.national_id] for p in order]
        headers = ["Nom", "Prénom", "ID"]

        # 7️⃣ Propose l'export avec un nom de fichier basé sur le tournoi
        self._ask_export(rows, headers, f"joueurs_{tournament.name}")

    # ------- Affichage de tous les rounds et matchs d’un tournoi -------
    def show_all_rounds_and_matches(self):
        """
        Affiche tous les rounds et matchs d'un tournoi sélectionné.
        Étapes :
        1. Demande à l'utilisateur de choisir un tournoi
        2. Affiche les rounds et leurs matchs avec les scores
        3. Prépare les données pour une exportation éventuelle
        """
        # 1️⃣ Affiche un titre pour guider l'utilisateur
        print("\n=== Sélectionner un tournoi pour afficher les rounds et matches ===")

        # 2️⃣ Demande à l'utilisateur de choisir un tournoi
        tournament = self._pick_tournament("afficher rounds & matches")
        if not tournament or not tournament.rounds:
            print("Aucun round disponible.")
            return

        # 3️⃣ Affiche tous les rounds et les matchs associés
        for idx, rnd in enumerate(tournament.rounds, 1):
            print(f"\n🥊 Round {idx} :")
            for m in rnd.matches:
                p1, p2 = m.players
                s1, s2 = m.scores
                print(
                    f"{p1.last_name} {p1.first_name}[{p1.national_id}] "
                    f"{s1} - {s2} {p2.last_name} {p2.first_name}[{p2.national_id}]"
                )
        print()

        # 4️⃣ Prépare les données sous forme tabulaire pour un export
        rows = []
        for idx, rnd in enumerate(tournament.rounds, 1):
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

        # 5️⃣ Définition des en-têtes et du nom de fichier d'export
        headers = ["Round", "Joueur 1", "Joueur 2", "Score 1", "Score 2"]
        name = f"rounds_{tournament.name.lower().replace(' ', '_')}"

        # 6️⃣ Propose un export des données (CSV, JSON, etc.)
        self._ask_export(rows, headers, name)

    # -----------------------
    #   EXPORT (CSV ou HTML)
    # -----------------------

    # ------- Exportation des données (CSV ou HTML) -------
    def _export(self, rows, headers, filename, fmt="csv"):
        """
        Exporte des données dans un fichier au format CSV ou HTML.
        Paramètres :
        - rows     : liste de listes, chaque sous-liste représente une ligne
        - headers  : liste des noms de colonnes
        - filename : nom du fichier (sans extension)
        - fmt      : format d'export, "csv" ou autre (HTML par défaut)
        Étapes :
        1. Détermine le chemin du fichier
        2. Si CSV → écrit les données en CSV
        3. Sinon → écrit les données dans un tableau HTML
        4. Affiche un message de confirmation avec le chemin complet
        """
        # 1️⃣ Vérifie que le dossier d'export existe, sinon le crée
        create_export_directory()

        # 2️⃣ Construit le chemin complet du fichier d'export
        path = EXPORT_DIR / f"{filename}.{fmt}"

        # 3️⃣ Si le format demandé est CSV
        if fmt == "csv":
            # 🅰 Ouvre le fichier en écriture texte avec UTF-8
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # 🅱 Écrit la ligne d'en-têtes
                writer.writerow(headers)
                # 🅲 Écrit toutes les lignes de données
                writer.writerows(rows)

        else:
            # 4️⃣ Si le format n'est pas CSV → export HTML
            with path.open("w", encoding="utf-8") as f:
                # 🅰 Début du tableau HTML avec en-têtes
                f.write("<table border='1'>\n<tr>")
                for h in headers:
                    f.write(f"<th>{h}</th>")
                f.write("</tr>\n")

                # 🅱 Ajoute les lignes de données
                for row in rows:
                    cells = "".join(f"<td>{c}</td>" for c in row)
                    f.write(f"<tr>{cells}</tr>\n")

                # 🅲 Fin du tableau
                f.write("</table>")

        # 5️⃣ Affiche un message confirmant la création du fichier
        print(f"✓ Exporté dans : {path.resolve()}")

    # ------- Demande et exécution d'un export de rapport -------
    def _ask_export(self, rows, headers, default_name):
        """
        Propose à l'utilisateur d'exporter un rapport et lance l'export si validé.
        Paramètres :
        - rows         : liste de lignes (liste de listes) à exporter
        - headers      : liste des noms de colonnes
        - default_name : nom de fichier sans extension
        Étapes :
        1. Demande si l'utilisateur souhaite exporter le rapport
        2. Demande le format d'export (CSV ou HTML)
        3. Valide le format (CSV par défaut si invalide)
        4. Lance l'export avec la méthode _export
        """
        # 1️⃣ Demande si l'utilisateur souhaite exporter
        if input("\nExporter ce rapport ? (o/N) ").lower() == "o":

            # 2️⃣ Demande le format d'export
            fmt = input("Format csv ou html ? ").lower()

            # 3️⃣ Vérifie que le format est valide (sinon CSV par défaut)
            if fmt not in ("csv", "html"):
                fmt = "csv"

            # 4️⃣ Lance l'export avec les paramètres fournis
            self._export(rows, headers, default_name, fmt)
