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

# 1️⃣ Nombre maximal de tentatives pour chaque saisie obligatoire
MAX_ATTEMPTS = 3

# 2️⃣ Racine du projet (un niveau au-dessus du dossier courant)
#    - Path(__file__)       : chemin vers ce fichier
#    - .resolve()           : chemin absolu, sans liens symboliques
#    - .parents[1]          : remonte d’un dossier
BASE_DIR = Path(__file__).resolve().parents[1]

# 3️⃣ Dossiers de données et d’export
#    - DATA_DIR   : où sont stockés les JSON des tournois
#    - EXPORT_DIR : où on place les fichiers d’export (rapports, CSV…)
DATA_DIR = BASE_DIR / "data" / "tournaments"
EXPORT_DIR = BASE_DIR / "export"

# 4️⃣ Création automatique du dossier d’export s’il n’existe pas
#    - exist_ok=True : pas d’erreur si le dossier est déjà présent
EXPORT_DIR.mkdir(exist_ok=True)


class TournamentController:
    """Gère la création, modification, suppression, déroulement et exports."""

    def __init__(self):
        """Initialise la liste des tournois en mémoire."""
        # 5️⃣ Liste interne pour stocker les objets Tournament chargés
        self._tours = []

        # 6️⃣ Chargement automatique des tournois existants depuis DATA_DIR
        #    (implémenté dans la méthode _load)
        self._load()

    def _input_nonempty(self, prompt):
        """
        Demande une saisie non vide à l'utilisateur·rice.
        Retourne la chaîne saisie, ou None si limite d'essais atteinte.
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle de saisie : on autorise MAX_ATTEMPTS essais
        while attempt < MAX_ATTEMPTS:
            # a) On affiche l’invite et on récupère la saisie, sans espaces superflus
            value = input(prompt).strip()
            # b) Si la saisie n'est pas vide, on la retourne immédiatement
            if value:
                return value

            # c) Sinon, on incrémente le compteur et on affiche un message d’erreur
            attempt += 1
            print(
                f"\n🔴  Ce champ est obligatoire. "
                f"({attempt}/{MAX_ATTEMPTS}) Veuillez réessayer.\n"
            )

        # 3️⃣ Si on a dépassé le nombre de tentatives autorisées
        print("🔁❌ Nombre de tentatives dépassé. Opération annulée.")
        return None

    def _input_date(self, prompt):
        """
        Demande une date au format jj/mm/aaaa.
        Retourne la date validée en chaîne, ou None si limite d'essais atteinte.
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle de saisie : on autorise MAX_ATTEMPTS essais
        while attempt < MAX_ATTEMPTS:
            # a) Affiche l’invite et récupère la saisie sans espaces superflus
            value = input(prompt).strip()
            try:
                # b) Tente de convertir la chaîne en date selon le format jour/mois/année
                datetime.strptime(value, "%d/%m/%Y")
                # c) Si la conversion réussit, on retourne la valeur saisie
                return value
            except ValueError:
                # d) En cas d’erreur de format, on incrémente les tentatives
                attempt += 1
                # e) Message d’erreur indiquant le format attendu et le nombre d’essais restants
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}) "
                    f"- (ex. 31/12/2025). Veuillez réessayer.\n"
                )

        # 3️⃣ Si on a épuisé toutes les tentatives sans succès
        print("\n❌ Nombre de tentatives dépassé. Opération annulée.")
        return None

    def _choose(self, action):
        """
        Affiche la liste des tournois et demande de choisir un index.
        Retourne l'objet Tournament ou None.
        """
        # 1️⃣ Si la liste des tournois est vide, on prévient et on sort
        if not self._tours:
            print("\n🔍 Aucun tournoi disponible.")
            return None

        # 2️⃣ Affiche les tournois disponibles
        ConsoleView.show_tournaments(self._tours)

        # 3️⃣ Demande à l’utilisateur·rice de choisir un numéro
        choice = input(f"\nNuméro du tournoi pour {action} : ").strip()

        # 4️⃣ Vérification de la saisie : doit être un nombre
        if not choice.isdigit():
            print("\n❌ Veuillez entrer un numéro valide.")
            return None

        # 5️⃣ Conversion en entier et vérification de la plage
        idx = int(choice)
        if 1 <= idx <= len(self._tours):
            # 6️⃣ Si tout est OK, on renvoie l’objet Tournament sélectionné
            return self._tours[idx - 1]

        # 7️⃣ Si le chiffre est hors de la plage, on prévient et on sort
        print("\n❌ Numéro hors plage.")
        return None

    # -----------------------
    #   CHARGEMENT / RELOAD
    # -----------------------

    def _load(self):
        """Charge tous les tournois valides depuis data/tournaments."""
        # 1️⃣ Réinitialise la liste interne des tournois
        self._tours.clear()

        # 2️⃣ Si le dossier de données n'existe pas, il n'y a rien à charger
        if not DATA_DIR.exists():
            return

        # 3️⃣ Parcourt chaque fichier JSON du répertoire
        for file in DATA_DIR.glob("*.json"):
            try:
                # a) Tente de charger le tournoi via la méthode de classe
                tour = Tournament.load(file.name)
            except (ValueError, json.JSONDecodeError):
                # b) Si le fichier est mal formé ou invalide, on l'ignore en avertissant
                print(f"⚠️  Ignoré : impossible de charger {file.name}")
            else:
                # c) Si tout se passe bien, on ajoute le tournoi à la liste
                self._tours.append(tour)

    # -----------------------
    #   SAUVEGARDE
    # -----------------------

    def _save(self, tour):
        """
        Sauvegarde un tournoi dans le répertoire data/tournaments
        en appelant sa méthode save().
        """
        # Délègue la sauvegarde de l'objet Tournament à sa propre méthode
        tour.save()

    # -----------------------
    #   CRÉATION
    # -----------------------

    def create_tournament(self):
        """
        Guide la création pas à pas d'un nouveau tournoi.
        1) Nom  2) Lieu  3) Date début  4) Date fin  5) Description  6) Rounds
        """
        # 1️⃣ Affichage de l’en‑tête de création
        print("\n=== Création d'un tournoi ===\n")

        # 2️⃣ Saisie du nom du tournoi (obligatoire)
        name = self._input_nonempty("Nom du tournoi : ")
        if name is None:  # si l’utilisateur abandonne après MAX_ATTEMPTS
            return

        # 3️⃣ Saisie du lieu (obligatoire)
        place = self._input_nonempty("Lieu : ")
        if place is None:
            return

        # 4️⃣ Saisie de la date de début (format jj/mm/aaaa)
        start_date = self._input_date("Date début (jj/mm/aaaa) : ")
        if start_date is None:  # abandon en cas de format invalide
            return

        # 5️⃣ Saisie et validation de la date de fin
        #    On boucle jusqu’à MAX_ATTEMPTS pour s’assurer que date_fin ≥ date_début
        end_date = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            saisie = self._input_date("Date fin (jj/mm/aaaa) : ")
            if saisie is None:
                return
            # Conversion en datetime pour comparer
            dt_start = datetime.strptime(start_date, "%d/%m/%Y")
            dt_end = datetime.strptime(saisie, "%d/%m/%Y")
            if dt_end >= dt_start:
                end_date = saisie
                break
            # Message d’erreur si fin < début
            print(
                f"\n❌ La date de fin doit être ≥ date de début "
                f"({attempt}/{MAX_ATTEMPTS}).\n"
            )
        if end_date is None:
            print("\n❌ Nombre de tentatives dépassé. Opération annulée.")
            return

        # 6️⃣ Saisie de la description (obligatoire)
        description = self._input_nonempty("Description         : ")
        if description is None:
            return

        # 7️⃣ Saisie facultative du nombre de tours (défaut = 4)
        while True:
            nb = input("Nombre de tours (défaut 4) : ").strip()
            if nb == "":
                total_rounds = 4
                break
            if nb.isdigit() and int(nb) > 0:
                total_rounds = int(nb)
                break
            print("Entrez un entier positif ou laissez vide pour 4.")

        # 8️⃣ Création de l’objet Tournament et ajout à la liste
        tour = Tournament(name, place, start_date, end_date, description, total_rounds)
        self._tours.append(tour)

        # 9️⃣ Sauvegarde immédiate et message de confirmation
        self._save(tour)
        print("\n✅ Tournoi créé.\n")

        # 🔟 Affichage récapitulatif des infos du tournoi
        print(f"--- Informations du tournoi '{tour.name}' ---\n")
        print(f"Lieu             : {tour.place}")
        print(f"Dates            : {tour.start_date} → {tour.end_date}")
        print(f"Description      : {tour.description}")
        print(f"Nombre de tours  : {tour.total_rounds}")

    # -----------------------
    #   MODIFICATION
    # -----------------------

    def modify_tournament(self):
        """Modifie les informations d'un tournoi existant."""
        # 1️⃣ Titre de la section de modification
        print("\n--- Modification d'un tournoi ---")

        # 2️⃣ Sélection du tournoi à modifier
        tour = self._choose("modifier")
        if not tour:  # Si aucun tournoi sélectionné ou erreur de saisie
            return

        # 3️⃣ Affichage des informations actuelles pour référence
        print(f"\n--- Infos actuelles du tournoi '{tour.name}' ---")
        print(f"Lieu             : {tour.place}")
        print(f"Dates            : {tour.start_date} → {tour.end_date}")
        print(f"Description      : {tour.description}")
        print(f"Nombre de tours  : {tour.total_rounds}")

        # 4️⃣ Info pour l'utilisateur·rice : laisser vide pour conserver l’ancienne valeur
        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

        # 5️⃣ Modification du nom
        new = input(f"Nom [{tour.name}] : ").strip()
        if new:
            tour.name = new

        # 6️⃣ Modification du lieu
        new = input(f"Lieu [{tour.place}] : ").strip()
        if new:
            tour.place = new

        # 7️⃣ Modification de la date de début
        while True:
            new = input(f"Date début [{tour.start_date}] : ").strip()
            if not new:  # vide → conserver
                break
            try:
                # vérifie le format jj/mm/aaaa
                datetime.strptime(new, "%d/%m/%Y")
                tour.start_date = new
                break
            except ValueError:
                print("❌ Format invalide. Exemple : 31/12/2025")

        # 8️⃣ Modification de la date de fin
        while True:
            new = input(f"Date fin [{tour.end_date}] : ").strip()
            if not new:  # vide → conserver
                break
            try:
                date_fin = datetime.strptime(new, "%d/%m/%Y")
                date_deb = datetime.strptime(tour.start_date, "%d/%m/%Y")
                if date_fin >= date_deb:
                    tour.end_date = new
                    break
                else:
                    print("❌ La date de fin doit être ≥ date de début.")
            except ValueError:
                print("❌ Format invalide. Exemple : 31/12/2025")

        # 9️⃣ Modification de la description
        new = input(f"Description [{tour.description}] : ").strip()
        if new:
            tour.description = new

        # 🔟 Modification du nombre de tours
        while True:
            nb = input(f"Nombre de tours [{tour.total_rounds}] : ").strip()
            if nb == "":  # vide → conserver
                break
            if nb.isdigit() and int(nb) > 0:
                tour.total_rounds = int(nb)
                break
            print("Entrez un entier positif ou laissez vide pour conserver.")

        # 1️⃣1️⃣ Sauvegarde et confirmation
        self._save(tour)
        print("\n✅ Mise à jour effectuée.\n")

        # 1️⃣2️⃣ Affichage des nouvelles infos pour vérifier
        print(f"--- Nouvelles infos du tournoi '{tour.name}' ---\n")
        print(f"Lieu             : {tour.place}")
        print(f"Dates            : {tour.start_date} → {tour.end_date}")
        print(f"Description      : {tour.description}")
        print(f"Nombre de tours  : {tour.total_rounds}")

    # -----------------------
    #   SUPPRESSION
    # -----------------------

    def delete_tournament(self):
        """Supprime un tournoi existant."""
        # 1️⃣ Affichage de l’en‑tête de suppression
        print("\n--- Suppression d'un tournoi ---")

        # 2️⃣ Sélection du tournoi à supprimer
        #    _choose("supprimer") affiche la liste et renvoie l'objet ou None
        tour = self._choose("supprimer")
        if not tour:  # Si aucun tournoi n’est sélectionné ou erreur
            return

        # 3️⃣ Demande de confirmation à l’utilisateur·rice
        #    Seul "o" (oui) en minuscules valide la suppression
        if input(f"\nSupprimer {tour.name} (o/N) ? ").lower() != "o":
            return

        # 4️⃣ Construction du chemin vers le fichier JSON correspondant
        #    On reprend la même logique que _file_path : nom en minuscules et underscores
        path = DATA_DIR / f"{tour.name.lower().replace(' ', '_')}.json"

        # 5️⃣ Suppression du fichier JSON si présent
        if path.exists():
            path.unlink()  # supprime physiquement le fichier

        # 6️⃣ Retrait de l’objet Tournament de la liste en mémoire
        self._tours.remove(tour)

        # 7️⃣ Message de confirmation final
        print(f"\n✅ Le tournoi '{tour.name}' - {tour.place} a été supprimé.")

    # -----------------------
    #   LISTE
    # -----------------------

    def list_tournaments(self):
        """Affiche la liste des tournois."""
        # 1️⃣ Affichage de l’en‑tête pour démarquer la section
        print("\n--- Liste des tournois ---")

        # 2️⃣ Délégation de l’affichage détaillé à ConsoleView
        #    Cette méthode va lister chaque tournoi avec ses infos clés
        ConsoleView.show_tournaments(self._tours)

    # -----------------------
    #   AJOUT/RETRAIT JOUEUR(S)
    # -----------------------

    def manage_players_in_tournament(self):
        """Ajoute ou retire des joueurs d'un tournoi."""
        # 1️⃣ Titre de la section pour guider l’utilisateur·rice
        print("\n--- Gestion des joueurs d'un tournoi ---")

        # 2️⃣ Sélection du tournoi à gérer
        tour = self._choose("gérer les joueurs de")
        if not tour:  # Si aucun tournoi sélectionné ou erreur de saisie
            return

        # 3️⃣ Interdire la modification une fois le tournoi démarré
        if tour.status != "non démarré":
            print("\n❌ Impossible après démarrage.")
            return

        # 4️⃣ Boucle du menu de gestion jusqu’à retour (option 0)
        while True:
            # 🅰 Affichage des infos clés du tournoi
            print("\n🏆 Informations du tournoi :\n")
            print(f"Nom                : {tour.name}")
            print(f"Lieu               : {tour.place}")
            print(f"Dates              : {tour.start_date} → {tour.end_date}")
            print(f"Description        : {tour.description}")
            print(f"Nombre de tours    : {tour.total_rounds}")
            print(f"Joueurs inscrits   : {len(tour.players)}")

            # 🅱 Menu d’actions
            print("\n--- Ajouter ou retirer joueur(s) ---")
            print("1. Ajouter joueur(s)")
            print("2. Retirer joueur(s)")
            print("0. Retour\n")

            # 🅲 Lecture du choix de l’utilisateur·rice
            choice = input("Votre choix : ").strip()

            # 🅳 Exécution de l’action choisie
            if choice == "1":
                self._add_players(tour)
            elif choice == "2":
                self._remove_players(tour)
            elif choice == "0":
                break  # Sortie de la boucle et fin de la méthode
            # 🅴 Toute autre saisie invalide redémarre la boucle sans action

    def _add_players(self, tour):
        """Ajoute des joueurs à un tournoi, sans doublons et sans saisie multiple."""
        # 1️⃣ On récupère la liste complète des joueurs et on la trie par nom/prénom
        all_players = sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

        # 2️⃣ On retire de cette liste ceux qui sont déjà inscrits dans le tournoi
        available = [p for p in all_players if p not in tour.players]

        # 3️⃣ Si plus personne n’est disponible, on informe et on arrête
        if not available:
            print("\n👤 Tous les joueurs sont déjà inscrits.")
            return

        # 4️⃣ Affichage numéroté des joueurs qu’on peut ajouter
        print("\n--- Joueurs disponibles à l'ajout ---")
        for i, p in enumerate(available, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

        # 5️⃣ On demande les numéros (séparés par des virgules) pour ajouter plusieurs joueurs
        nums = input("\nNuméros à ajouter (séparés par des virgules) : ")
        added = []  # liste des joueurs effectivement ajoutés
        seen = set()  # pour éviter les doublons dans la saisie

        # 6️⃣ Traitement de chaque jeton saisi
        for token in nums.split(","):
            token = token.strip()
            # 🅰 Ignorer si ce n’est pas un nombre
            if not token.isdigit():
                continue
            # 🅱 Ignorer les doublons de saisie
            if token in seen:
                print(f"⚠️  Numéro {token} dupliqué, ignoré.")
                continue
            seen.add(token)

            # 🅲 Vérifier que le numéro correspond à un index valide
            idx = int(token) - 1
            if 0 <= idx < len(available):
                p = available[idx]
                tour.players.append(p)  # ajout au tournoi
                added.append(p)  # enregistrement pour le retour utilisateur
            else:
                print(f"⚠️  Le numéro {token} n'est pas valide.")

        # 7️⃣ Si au moins un joueur a été ajouté :
        if added:
            # 🅰 On trie à nouveau la liste des joueurs du tournoi
            tour.players.sort(key=lambda p: (p.last_name, p.first_name))
            # 🅱 On sauvegarde immédiatement le tournoi mis à jour
            self._save(tour)
            # 🅲 On affiche la liste des ajouts
            print("\n👤 Joueur(s) ajouté(s) :")
            for p in added:
                print(f"- {p.last_name} {p.first_name} [{p.national_id}]")
        else:
            # 8️⃣ Sinon, on indique qu’aucun ajout n’a eu lieu
            print("\n👤 Aucun nouveau joueur ajouté.")

    def _remove_players(self, tour):
        """Retire un ou plusieurs joueurs d'un tournoi NON démarré, avec confirmation."""

        # 1️⃣ Vérifie s’il y a des joueurs inscrits
        if not tour.players:
            print("\n👤 Aucun joueur inscrit.")
            return

        # 2️⃣ Trie la liste des joueurs par nom puis prénom pour un affichage ordonné
        tour.players.sort(key=lambda p: (p.last_name, p.first_name))

        # 3️⃣ Affiche la liste numérotée des joueurs
        print("\n--- Joueurs inscrits ---")
        for i, p in enumerate(tour.players, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

        # 4️⃣ Demande les numéros (virgule‑séparés) des joueurs à retirer
        nums = input("\nNuméros à retirer (séparés par des virgules) : ")
        to_remove = []
        for token in nums.split(","):
            token = token.strip()
            # a) Ignorer si ce n’est pas un chiffre
            if not token.isdigit():
                continue
            idx = int(token) - 1
            # b) Si l’index est valide, ajoute le joueur à la liste de retrait
            if 0 <= idx < len(tour.players):
                to_remove.append(tour.players[idx])

        # 5️⃣ Si aucun numéro valide n’a été saisi, on informe et on sort
        if not to_remove:
            print("\n❌ Aucun numéro valide.")
            return

        # 6️⃣ Pour chaque joueur sélectionné, demande confirmation avant suppression
        removed = []
        for p in to_remove:
            if input(f"Supprimer {p.last_name} {p.first_name} (o/N) ? ").lower() == "o":
                tour.players.remove(p)
                removed.append(p)

        # 7️⃣ Si des suppressions ont eu lieu, on trie, sauvegarde et on affiche le retour
        if removed:
            # a) Re‑trie la liste des joueurs restants
            tour.players.sort(key=lambda p: (p.last_name, p.first_name))
            # b) Sauvegarde l’état du tournoi mis à jour
            self._save(tour)
            # c) Affiche la liste des joueurs retirés
            print("\n👤 Joueur(s) retiré(s) :")
            for p in removed:
                print(f"- {p.last_name} {p.first_name} [{p.national_id}]")
        else:
            # 8️⃣ Si aucune suppression confirmée, on l’indique à l’utilisateur·rice
            print("\n👤 Aucune suppression effectuée.")

    # -----------------------
    #   DÉMARRER
    # -----------------------

    def start_tournament(self):
        """Démarre un tournoi si suffisamment de joueurs sont inscrits."""
        # 1️⃣ Titre de la section pour informer l’utilisateur·rice
        print("\n--- Démarrage d'un tournoi ---")

        # 2️⃣ Sélection du tournoi à démarrer
        tour = self._choose("démarrer")
        if not tour:  # Si aucun tournoi n’est sélectionné ou erreur de saisie
            return

        # 3️⃣ Vérifier qu’il y a au moins 1 joueur inscrit
        if not tour.players:
            print("\n❌ Impossible : aucun joueur n'est inscrit.")
            return

        # 4️⃣ Vérifier qu’il y a un nombre pair de joueurs (et au moins 2)
        count = len(tour.players)
        if count < 2 or count % 2 != 0:
            print("\n❌ Il faut un nombre pair de joueurs (au moins 2).")
            return

        # 5️⃣ Empêcher de relancer un tournoi déjà terminé
        if tour.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tour.name}' est déjà terminé.")
            return

        # 6️⃣ Si le tournoi est déjà en cours, orienter vers la saisie des scores
        if tour.status == "en cours":
            print(f"\nℹ️  Statut du tournoi '{tour.name}' : {tour.status}.")
            print(
                "💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
            )
            return

        # 7️⃣ Annoncer le démarrage et afficher quelques infos
        print(f"\n🏁 Tournoi '{tour.name}' démarré.\n")
        print(f"Joueurs inscrits : {count}")
        print(f"Nombre de rounds : {tour.total_rounds}\n")

        # 8️⃣ Passer le statut à "en cours" et créer le 1er round
        tour.status = "en cours"
        tour.start_next_round()
        self._save(tour)  # sauvegarde immédiate de l’état

        # 9️⃣ Afficher les appariements du ou des rounds créés
        for idx, rnd in enumerate(tour.rounds, 1):
            print(f"\n🥊 Round {idx} :")
            for m in rnd.matches:
                p1, p2 = m.players
                print(
                    f"{p1.last_name} {p1.first_name} [{p1.national_id}] VS "
                    f"{p2.last_name} {p2.first_name} [{p2.national_id}]"
                )

        # 🔟 Rappel de la marche à suivre pour saisir les scores
        print(
            "\n💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
        )

    # -----------------------
    #   SAISIE SCORES
    # -----------------------

    def enter_scores_current_round(self):
        """Saisit les scores du round en cours, ou affiche un message si non démarré/terminé."""

        # 1️⃣ En‑tête de la saisie
        print("\n--- Saisie des scores du round en cours ---")

        # 2️⃣ Sélection du tournoi cible
        tour = self._choose("saisir les scores")
        if not tour:  # si aucun tournoi sélectionné ou erreur de saisie
            return

        # 3️⃣ Cas où le tournoi n'a pas encore démarré
        if tour.status == "non démarré":
            print("\n❌ Impossible : Le tournoi n'a pas encore démarré.")
            print("💡 Utilisez l'option 6 du menu Tournoi pour démarrer le tournoi.")
            return

        # 4️⃣ Cas où le tournoi est déjà terminé
        if tour.status == "terminé":
            print(f"\nℹ️  Le tournoi '{tour.name}' est déjà terminé.")
            return

        # 👉 À partir d'ici, le tournoi est en cours
        rnd = tour.rounds[-1]  # dernier round créé
        num = tour.current_round_index  # indice 1-based du round

        # 5️⃣ Si le round est déjà clôturé, affiche un récap
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

        # 6️⃣ Invitation à saisir les scores
        print(f"\n===== Score du tournoi {tour.name} =====")
        print("📌 Rappel : format 1-0, 0-1, 0.5-0.5 (1 victoire, 0 défaite, 0.5 nul)")
        print(f"\n🥊 Round {num}\n")

        results = []  # liste brute pour record_results
        recap = []  # stockage local pour l’affichage de fin

        # 7️⃣ Boucle sur chaque match pour lire un score valide
        for i, m in enumerate(rnd.matches, 1):
            p1, p2 = m.players
            while True:
                # 🅰 Invite l’utilisateur à entrer le score
                s = (
                    input(
                        f"{p1.last_name} {p1.first_name}[{p1.national_id}] VS "
                        f"{p2.last_name} {p2.first_name}[{p2.national_id}] : "
                    )
                    .strip()
                    .replace(" ", "")
                )
                # 🅱 Valide le format
                if s in ("1-0", "0-1", "0.5-0.5"):
                    a, b = map(float, s.split("-"))
                    break
                print("❌ Exemple valide : 1-0, 0-1 ou 0.5-0.5")

            # 🅲 Enregistre l’entrée pour le traitement et pour le récap
            results.append((num - 1, i - 1, a, b))
            recap.append((p1, p2, a, b))

        # 8️⃣ Enregistrement des scores et clôture du round
        tour.record_results(results)
        self._save(tour)

        # 9️⃣ Affichage du récapitulatif des scores saisis
        print(f"\n--- Récapitulatif du round {num} ---")
        for p1, p2, a, b in recap:
            print(
                f"{p1.last_name} {p1.first_name} {a} - {b} {p2.last_name} {p2.first_name}"
            )

        # 🔟 Confirmation et conseil pour la suite
        print("\n💾 Scores enregistrés.")
        print("💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant.")

    # -----------------------
    #   ROUND SUIVANT
    # -----------------------

    def start_next_round(self):
        """Démarre le round suivant du tournoi en cours."""

        # 1️⃣ Affichage de l’en‑tête pour guider l’utilisateur·rice
        print("\n--- Démarrage du round suivant ---")

        # 2️⃣ Sélection du tournoi sur lequel agir
        tour = self._choose("démarrer le round suivant")
        if not tour:  # si aucun tournoi sélectionné ou annulation
            return

        # 3️⃣ Empêche de lancer un round si le tournoi est déjà terminé
        if tour.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tour.name}' est déjà terminé.")
            return

        # 4️⃣ Vérification que le round précédent est bien clôturé
        #    - tour.rounds[-1].end_time existe seulement si on a déjà joué et fermé un round
        if tour.rounds and not tour.rounds[-1].end_time:
            print("⚠️  Il faut clôturer le round en cours avant de démarrer le suivant.")
            return

        # 5️⃣ Vérifie qu’on n’a pas déjà atteint le nombre maximal de rounds
        if tour.current_round_index >= tour.total_rounds:
            print("ℹ️  Tous les rounds ont déjà été joués.")
            return

        # 6️⃣ Tout est OK → on lance le nouveau round, on sauvegarde et on notifie
        tour.start_next_round()
        self._save(tour)
        print("🏁 Nouveau round démarré.")

    # -----------------------
    #   CLASSEMENT
    # -----------------------

    def show_leaderboard(self):
        """Affiche le classement des joueurs du tournoi."""

        # 1️⃣ Recharge tous les tournois pour s’assurer d’avoir
        #    les dernières infos et que les Player.registry
        #    est à jour (remappage des national_id → Player)
        self.reload_tournaments()

        # 2️⃣ Affiche un titre et demande à l’utilisateur·rice
        #    de choisir le tournoi dont il veut voir le classement
        print("\n--- Affichage du classement ---")
        tour = self._choose("consulter le classement")
        if not tour:  # si aucune sélection ou annulation
            return

        # 3️⃣ Délègue l’affichage du classement à la vue console
        ConsoleView.show_leaderboard(tour)

    # -----------------------
    #   RAPPORTS
    # -----------------------

    # -------- Joueurs inscrits à au moins un tournoi --------

    def list_registered_players(self):
        """Affiche les joueurs inscrits à un tournoi."""
        # 1️⃣ Affichage de l’en‑tête pour informer l’utilisateur·rice
        print("\n--- Joueurs inscrits à un tournoi ---")

        # 2️⃣ Collecte des IDs uniques de joueurs inscrits dans n’importe quel tournoi
        ids = set()
        for t in self._tours:
            for p in t.players:
                ids.add(p.national_id)

        # 3️⃣ Si aucun ID n’a été trouvé → pas de joueurs inscrits
        if not ids:
            print("\nAucun joueur inscrit à un tournoi.\n")
            return

        # 4️⃣ Reconstruction de la liste d’objets Player à partir du registry
        #    On ne garde que les joueurs dont l’ID est dans la liste précédente
        registered = [p for p in Player.registry if p.national_id in ids]

        # 5️⃣ Tri alphabétique : d’abord par nom de famille, puis par prénom
        registered.sort(key=lambda p: (p.last_name, p.first_name))

        # 6️⃣ Affichage détaillé via la vue console
        print("\n--- Joueurs inscrits à un tournoi ---")
        ConsoleView.show_players(registered)

        # 7️⃣ Préparation des données pour un éventuel export
        #    - rows : liste de listes [Nom, Prénom, ID] pour chaque joueur
        rows = [[p.last_name, p.first_name, p.national_id] for p in registered]
        headers = ["Nom", "Prénom", "ID"]

        # 8️⃣ Proposition d’export (CSV, JSON…) en appelant la méthode d’aide
        self._ask_export(rows, headers, "joueurs_inscrits")

    # ---------- Liste des tournois ----------

    def _pick_tournament(self, action):
        """
        Récupère un tournoi en déléguant à la méthode _choose.
        action : verbe décrivant ce qu’on veut faire (ex. "modifier", "supprimer", etc.)
        Retourne l’objet Tournament sélectionné ou None.
        """
        # 1️⃣ On appelle _choose en passant le même “action” :
        #    _choose affiche la liste des tournois et lit la saisie de l’utilisateur·rice.
        # 2️⃣ _choose renvoie soit un objet Tournament, soit None en cas d’erreur/annulation.
        return self._choose(action)

    # ---------- Nom/dates tournoi ----------

    def show_tournament_header(self):
        """Affiche le nom et les dates d'un tournoi."""

        # 1️⃣ Affiche un titre pour guider l’utilisateur·rice
        print("\n=== Sélectionner un tournoi pour afficher les détails ===")

        # 2️⃣ Demande de choisir un tournoi via _pick_tournament (alias de _choose)
        tour = self._pick_tournament("consulter")
        #    _pick_tournament affiche la liste et retourne l’objet ou None
        if tour:
            # 3️⃣ Si un tournoi est bien sélectionné, on affiche son nom et ses dates
            print(f"\n{tour.name} — {tour.start_date} → {tour.end_date}\n")

    # ---------- Liste joueurs à un tournoi ----------

    def show_tournament_players(self):
        """Affiche les joueurs d'un tournoi."""

        # 1️⃣ Affiche un titre pour guider l’utilisateur·rice
        print("\n=== Sélectionner un tournoi pour afficher les joueurs ===")

        # 2️⃣ Demande à l’utilisateur de choisir un tournoi via _pick_tournament (alias de _choose)
        tour = self._pick_tournament("afficher joueurs")
        if not tour:  # Annule si aucun tournoi n’est sélectionné ou en cas d’erreur
            return

        # 3️⃣ Affiche l’en‑tête du listing des joueurs pour ce tournoi
        print(f"\n--- Joueurs du tournoi {tour.name} ---")

        # 4️⃣ Trie alphabétiquement la liste des joueurs par nom puis prénom
        order = sorted(tour.players, key=lambda p: (p.last_name, p.first_name))

        # 5️⃣ Délègue l’affichage détaillé à la vue console (nom, ID, date de naissance)
        ConsoleView.show_players(order)

        # 6️⃣ Prépare les données pour une éventuelle exportation
        print("\n--- Exportation ---")
        rows = [[p.last_name, p.first_name, p.national_id] for p in order]
        headers = ["Nom", "Prénom", "ID"]

        # 7️⃣ Appelle la méthode d’aide à l’export (_ask_export) avec les données et un nom de fichier basé sur le tournoi
        self._ask_export(rows, headers, f"joueurs_{tour.name}")

    # ---------- Rounds/Matches tournoi ----------

    def show_all_rounds_and_matches(self):
        """Affiche tous les rounds et matches d'un tournoi."""

        # 1️⃣ En‑tête pour guider l’utilisateur·rice
        print("\n=== Sélectionner un tournoi pour afficher les rounds et matches ===")

        # 2️⃣ Choix du tournoi via _pick_tournament (alias de _choose)
        tour = self._pick_tournament("afficher rounds & matches")
        #    Si aucun tournoi choisi ou erreur de saisie, on arrête
        if not tour or not tour.rounds:
            print("Aucun round disponible.")
            return

        # 3️⃣ Parcours de chaque round existant et affichage
        for idx, rnd in enumerate(tour.rounds, 1):
            print(f"\n🥊 Round {idx} :")
            # 4️⃣ Pour chaque match du round, on récupère joueurs et scores
            for m in rnd.matches:
                p1, p2 = m.players
                s1, s2 = m.scores
                # 5️⃣ Affichage formaté : Nom Prénom[ID] score1 - score2 Nom Prénom[ID]
                print(
                    f"{p1.last_name} {p1.first_name}[{p1.national_id}] "
                    f"{s1} - {s2} {p2.last_name} {p2.first_name}[{p2.national_id}]"
                )
        print()

        # 6️⃣ Préparation des données pour un export éventuel
        rows = []
        for idx, rnd in enumerate(tour.rounds, 1):
            for m in rnd.matches:
                p1, p2 = m.players
                s1, s2 = m.scores
                # Chaque ligne contient : Round, Joueur1, Joueur2, Score1, Score2
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
        # 7️⃣ Nom de fichier basé sur le nom du tournoi (minuscules, underscores)
        name = f"rounds_{tour.name.lower().replace(' ', '_')}"
        # 8️⃣ Appel à la méthode d’export pour proposer CSV/JSON…
        self._ask_export(rows, headers, name)

    # -----------------------
    #   EXPORT (CSV ou HTML)
    # -----------------------

    def _export(self, rows, headers, filename, fmt="csv"):
        """
        Exporte des données (rows, headers) vers un fichier CSV ou HTML.
        rows     : liste de listes, chaque sous-liste est une ligne de données
        headers  : liste de chaînes pour les en-têtes de colonnes
        filename : nom de base du fichier (sans extension)
        fmt      : format d'export, "csv" ou autre (HTML par défaut)
        """
        # 1️⃣ Construction du chemin complet vers le fichier d’export
        #    - EXPORT_DIR est le dossier dédié aux exports
        #    - on ajoute l’extension selon fmt ("csv" ou autre)
        path = EXPORT_DIR / f"{filename}.{fmt}"

        # 2️⃣ Choix du format CSV
        if fmt == "csv":
            # 🅰 Ouverture du fichier en mode écriture textuelle
            #    - newline="" pour éviter les lignes vides entre chaque écriture sous Windows
            #    - encoding="utf-8" pour conserver les accents
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # 🅱 Écriture de la ligne d’en‑têtes
                writer.writerow(headers)
                # 🅲 Écriture de toutes les lignes de données
                writer.writerows(rows)
        else:
            # 3️⃣ Autre format → création d’un tableau HTML simple
            with path.open("w", encoding="utf-8") as f:
                # 🅰 Début du tableau et ligne d’en‑têtes
                f.write("<table border='1'>\n<tr>")
                for h in headers:
                    f.write(f"<th>{h}</th>")
                f.write("</tr>\n")
                # 🅱 Lignes de données : une <tr> par ligne, avec autant de <td> que de colonnes
                for row in rows:
                    cells = "".join(f"<td>{c}</td>" for c in row)
                    f.write(f"<tr>{cells}</tr>\n")
                # 🅲 Fin du tableau
                f.write("</table>")

        # 4️⃣ Confirmation à l’utilisateur·rice
        #    .resolve() renvoie le chemin absolu pour que ce soit clair où trouver le fichier
        print(f"✓ Exporté dans : {path.resolve()}")

    def _ask_export(self, rows, headers, default_name):
        """
        Propose à l’utilisateur·rice d’exporter un rapport et lance l’export si validé.
        rows         : liste de lignes (list de listes) à exporter
        headers      : liste d’en‑têtes de colonnes
        default_name : nom de fichier sans extension
        """
        # 1️⃣ On demande si l’utilisateur·rice souhaite exporter le rapport
        if input("\nExporter ce rapport ? (o/N) ").lower() == "o":
            # 2️⃣ Choix du format : CSV ou HTML
            fmt = input("Format csv ou html ? ").lower()
            # 3️⃣ Validation du format : si l’entrée n’est pas "csv" ou "html", on utilise "csv" par défaut
            if fmt not in ("csv", "html"):
                fmt = "csv"
            # 4️⃣ Appel à la méthode d’export avec le format choisi
            self._export(rows, headers, default_name, fmt)

    # -----------------------
    #   RECHARGER TOURNOIS DISQUE
    # -----------------------

    def reload_tournaments(self):
        """Recharge la liste des tournois depuis les fichiers JSON."""

        # 1️⃣ Appel de la méthode _load()
        #    - _load() vide d’abord la liste interne (_tours)
        #    - puis parcourt tous les fichiers JSON dans DATA_DIR
        #    - pour recharger chaque Tournament valide en mémoire
        self._load()

    def update_player_references(self, updated_player):
        """
        Pour chaque tournoi chargé, remplace l'ancien objet Player
        (même national_id) par updated_player dans tour.players.
        """
        # 1️⃣ Parcours de tous les tournois en mémoire
        for tour in self._tours:
            changed = False  # drapeau pour savoir si on a fait un remplacement

            # 2️⃣ Recherche du joueur à mettre à jour dans la liste tour.players
            for idx, p in enumerate(tour.players):
                # 🅰 Si l’ID national correspond à celui du joueur mis à jour
                if p.national_id == updated_player.national_id:
                    # 🅱 On remplace l’ancienne instance par la nouvelle
                    tour.players[idx] = updated_player
                    changed = True  # on note qu’il y a eu une modification

            # 3️⃣ Si au moins un remplacement a eu lieu, on persiste le tournoi
            if changed:
                # sauvegarde pour conserver les nouvelles références Player→tour
                self._save(tour)
