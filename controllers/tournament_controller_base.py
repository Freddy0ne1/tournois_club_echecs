"""Contrôleur principal — partie commune et utilitaires."""

# import csv
import json
from datetime import datetime
from pathlib import Path

# from models.player import Player
from models.tournament import Tournament
from views.console_view import ConsoleView

# -----------------------
#   Constantes globales
# -----------------------

# 1️⃣ Nombre maximal de tentatives autorisées pour une saisie obligatoire
MAX_ATTEMPTS = 3

# 2️⃣ Définition des chemins principaux du projet
#    - Path(__file__)  : chemin vers le fichier actuel
#    - .resolve()      : convertit en chemin absolu sans liens symboliques
#    - .parents[1]     : remonte d'un dossier (racine du projet)
BASE_DIR = Path(__file__).resolve().parents[1]

# 3️⃣ Dossiers pour les données et les exports
#    - DATA_DIR   : répertoire contenant les fichiers JSON des tournois
#    - EXPORT_DIR : répertoire où seront générés les fichiers exportés (rapports, CSV…)
DATA_DIR = BASE_DIR / "data" / "tournaments"
EXPORT_DIR = BASE_DIR / "export"


def create_export_directory():
    """
    Crée le dossier d'export pour les rapports.
    Étapes :
    1. Vérifie si le dossier existe déjà
    2. Si non, le crée
    """
    # 1️⃣ Vérifie si le dossier existe déjà
    if not EXPORT_DIR.exists():
        # 2️⃣ Si non, le crée
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)


class TournamentControllerBase:
    """
    Contrôleur principal pour la gestion des tournois.
    Responsabilités :
      - Créer, modifier, supprimer les tournois
      - Démarrer et gérer les rounds
      - Gérer l'inscription des joueurs
      - Exporter ou afficher des rapports
    """

    def __init__(self):
        """
        Initialise un contrôleur de tournois.
        Étapes :
          1. Initialise une liste interne pour stocker les tournois
          2. Charge les tournois existants depuis DATA_DIR
        """
        # 1️⃣ Crée une liste interne pour stocker les objets Tournament
        self._tournaments = []

        # 2️⃣ Charge automatiquement les tournois existants
        #    depuis DATA_DIR via la méthode _load()
        self._load()

    # -----------------------
    #   SAISIE NON VIDE
    # -----------------------

    def _input_nonempty(self, prompt):
        """
        Demande une saisie non vide à l'utilisateur·rice.
        Retour :
        - La chaîne saisie si elle n'est pas vide
        - None si le nombre maximal d'essais est atteint
        Étapes :
        1. Autorise plusieurs tentatives (MAX_ATTEMPTS)
        2. Refuse les chaînes vides
        3. Retourne la saisie ou None en cas d'échec
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle de saisie avec limite MAX_ATTEMPTS
        while attempt < MAX_ATTEMPTS:
            # 🅰 Affiche l'invite et récupère la saisie (retire les espaces inutiles)
            value = input(prompt).strip()

            # 🅱 Si une valeur non vide est saisie, la retourne immédiatement
            if value:
                return value

            # 🅲 Sinon, incrémente le compteur et affiche un message d'erreur
            attempt += 1
            print(
                f"\n🔴  Ce champ est obligatoire. "
                f"({attempt}/{MAX_ATTEMPTS}) Veuillez réessayer.\n"
            )

        # 3️⃣ Si la limite est atteinte sans succès
        print("🔁❌ Nombre de tentatives dépassé. Opération annulée.")
        return None

    # -----------------------
    #   SAISIE ET VALIDATION D'UNE DATE
    # -----------------------

    def _input_date(self, prompt):
        """
        Demande une date au format jj/mm/aaaa à l'utilisateur·rice.
        Retour :
        - Chaîne saisie si la date est valide
        - None si le nombre maximal d'essais est atteint
        Étapes :
        1. Autorise plusieurs tentatives (MAX_ATTEMPTS)
        2. Vérifie que la saisie respecte le format jj/mm/aaaa
        3. Retourne la date saisie ou None si échec
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle jusqu'à atteindre MAX_ATTEMPTS
        while attempt < MAX_ATTEMPTS:
            # 🅰 Affiche l'invite et lit la saisie (supprime les espaces)
            value = input(prompt).strip()
            try:
                # 🅱 Vérifie le format de la date (jj/mm/aaaa)
                datetime.strptime(value, "%d/%m/%Y")
                # 🅲 Si le format est correct, retourne la valeur saisie
                return value
            except ValueError:
                # 🅳 Incrémente le compteur si le format est incorrect
                attempt += 1
                # 🅴 Affiche un message d'erreur avec exemple et numéro d'essai
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}) "
                    f"- (ex. 31/12/2025). Veuillez réessayer.\n"
                )

        # 3️⃣ Si toutes les tentatives échouent, on abandonne
        print("\n❌ Nombre de tentatives dépassé. Opération annulée.")
        return None

    # -----------------------
    #   SÉLECTION D'UN TOURNOI
    # -----------------------

    def _choose(self, action):
        """
        Affiche la liste des tournois disponibles et demande à l'utilisateur
        de choisir un index pour effectuer une action donnée.
        Paramètre :
        - action : texte affiché pour préciser l'action (ex. "modifier", "supprimer")
        Retour :
        - L'objet Tournament sélectionné, ou None si annulation ou saisie invalide.
        """
        # 1️⃣ Si aucun tournoi n'est disponible, on informe l'utilisateur et on quitte
        if not self._tournaments:
            print("\n🔍 Aucun tournoi disponible.")
            return None

        # 2️⃣ Affiche la liste des tournois via la ConsoleView
        ConsoleView.show_tournaments(self._tournaments)

        # 3️⃣ Demande à l'utilisateur de saisir le numéro du tournoi
        choice = input(f"\nNuméro du tournoi pour {action} : ").strip()

        # 4️⃣ Vérifie que la saisie est bien un nombre
        if not choice.isdigit():
            print("\n❌ Veuillez entrer un numéro valide.")
            return None

        # 5️⃣ Convertit la saisie en entier et vérifie que l'index est valide
        idx = int(choice)
        if 1 <= idx <= len(self._tournaments):
            # 6️⃣ Retourne le tournoi sélectionné
            return self._tournaments[idx - 1]

        # 7️⃣ Si l'index est hors plage, on avertit et on quitte
        print("\n❌ Numéro hors plage.")
        return None

    # -----------------------
    #   CHARGEMENT DES TOURNOIS
    # -----------------------

    def _load(self):
        """
        Charge tous les tournois valides à partir des fichiers JSON présents
        dans le répertoire DATA_DIR (data/tournaments).
        Étapes :
        1. Vide la liste interne _tournaments
        2. Vérifie l'existence du dossier de données
        3. Parcourt les fichiers JSON et tente de charger chaque tournoi
            - Ignore les fichiers invalides ou corrompus avec un avertissement
        """
        # 1️⃣ Vide la liste interne des tournois avant de recharger
        self._tournaments.clear()

        # 2️⃣ Parcourt tous les fichiers JSON présents dans le dossier
        for file in DATA_DIR.glob("*.json"):
            try:
                # 🅰 Tente de charger le tournoi grâce à Tournament.load()
                tournament = Tournament.load(file.name)
            except (ValueError, json.JSONDecodeError):
                # 🅱 En cas d'erreur (JSON invalide ou autre problème), on ignore le fichier
                print(f"⚠️  Ignoré : impossible de charger {file.name}")
            else:
                # 🅲 Si le fichier est valide, on ajoute le tournoi dans la liste
                self._tournaments.append(tournament)

    # -----------------------
    #   SAUVEGARDE D'UN TOURNOI
    # -----------------------

    def _save(self, tournament):
        """
        Sauvegarde un tournoi spécifique dans le répertoire data/tournaments.
        Étapes :
        1. Appelle la méthode save() de l'objet Tournament concerné
            (c'est la classe Tournament qui gère la sérialisation JSON).
        """
        # 1️⃣ Délègue la sauvegarde de l'objet Tournament à sa propre méthode save()
        tournament.save()

    # -----------------------
    #   RECHARGER TOURNOIS DISQUE
    # -----------------------

    # ------- Recharge en mémoire tous les tournois depuis les fichiers JSON -------
    def reload_tournaments(self):
        """
        Recharge la liste des tournois à partir des fichiers JSON présents dans DATA_DIR.
        Étapes :
        1. Appelle la méthode interne _load()
            - Vide d'abord la liste interne (_tournaments)
            - Parcourt tous les fichiers JSON dans DATA_DIR
            - Recharge chaque tournoi valide en mémoire
        """
        # 1️⃣ Appelle la méthode _load() pour rafraîchir la liste des tournois
        self._load()

    # ------- Met à jour les références d'un joueur dans tous les tournois -------
    def update_player_references(self, updated_player):
        """
        Met à jour les références d'un joueur dans tous les tournois chargés.
        Pour chaque tournoi :
        - Recherche un joueur ayant le même identifiant national
        - Remplace l'ancienne instance Player par updated_player
        - Sauvegarde le tournoi si une modification a été effectuée
        """
        # 1️⃣ Parcourt tous les tournois actuellement en mémoire
        for tournament in self._tournaments:
            changed = False  # Drapeau indiquant si une mise à jour a été faite

            # 2️⃣ Parcourt tous les joueurs inscrits dans le tournoi
            for idx, p in enumerate(tournament.players):
                # 🅰 Vérifie si l'ID national correspond
                if p.national_id == updated_player.national_id:
                    # 🅱 Remplace l'ancienne instance Player par la nouvelle
                    tournament.players[idx] = updated_player
                    changed = True

            # 3️⃣ Si une ou plusieurs références ont été mises à jour, on sauvegarde
            if changed:
                self._save(tournament)
