"""
Contrôleur de gestion des tournois.

Ce module regroupe les fonctionnalités interactives permettant de :
- Créer de nouveaux tournois
- Lister les tournois existants
- Modifier les informations d'un tournoi
- Supprimer un tournoi

Ce contrôleur étend TournamentManagementBase afin d'utiliser :
- Les outils de saisie et validation utilisateur
- Le chargement et la sauvegarde des données
- La gestion des répertoires de données
"""

from datetime import datetime

from models.tournament import Tournament
from views.display_message import DisplayMessage
from views.console_view import ConsoleView
from utils.input_utils import InputUtils, MAX_ATTEMPTS
from .tournament_controller_base import (
    TournamentControllerBase as TournamentManagementController,
    DATA_DIR,
)


class TournamentManagement(TournamentManagementController):
    """
    Contrôleur dédié aux opérations CRUD sur les tournois
    (Créer, Lire/Lister, Mettre à jour, Supprimer).

    Responsabilités principales :
    - Créer un tournoi pas à pas (saisie guidée)
    - Afficher la liste des tournois disponibles
    - Modifier les informations d'un tournoi (nom, lieu, dates, description, rounds)
    - Supprimer un tournoi existant

    Cette classe s'appuie sur TournamentManagementBase pour :
    - Les méthodes de saisie utilisateur validée (input_nonempty, _input_date, _choose)
    - La persistance des données (_load, _save)
    """

    # -----------------------
    #   CRÉATION TOURNOI
    # -----------------------

    # ------- Étapes interactives pour créer un nouveau tournoi -------
    def create_tournament(self):
        """
        Crée un nouveau tournoi en interrogeant l'utilisateur·rice étape par étape :
        1. Nom
        2. Lieu
        3. Date de début et de fin
        4. Description
        5. Nombre de rounds
        - Vérifie chaque saisie et annule si l'une d'elles échoue.
        - Enregistre ensuite le tournoi et affiche une confirmation.
        """

        # 1️⃣ Affiche un en-tête indiquant la création d'un tournoi
        DisplayMessage.display_create_tournament_title()

        # 2️⃣ Demande le nom du tournoi (obligatoire)
        name = self._ask_required_field("Nom du tournoi : ")
        if name is None:  # 🅰 Annule si la saisie est vide ou abandonnée
            return

        # 3️⃣ Demande le lieu du tournoi (obligatoire)
        place = self._ask_required_field("Lieu : ")
        if place is None:
            return

        # 4️⃣ Demande la date de début (format jj/mm/aaaa)
        start_date = self._ask_date("Date début (jj/mm/aaaa) : ")
        if start_date is None:
            return

        # 5️⃣ Demande la date de fin et s'assure qu'elle est postérieure à la date de début
        end_date = self._ask_end_date("Date fin (jj/mm/aaaa) : ", start_date)
        if end_date is None:
            return

        # 6️⃣ Demande une description du tournoi
        description = self._ask_required_field("Description         : ")
        if description is None:
            return

        # 7️⃣ Demande le nombre de rounds (par défaut 4 si vide)
        total_rounds = self._ask_rounds()

        # 8️⃣ Création et enregistrement du tournoi
        tournament = Tournament(
            name, place, start_date, end_date, description, total_rounds
        )
        self._tournaments.append(tournament)

        # 9️⃣ Sauvegarde et affichage de confirmation
        self._save_and_confirm(tournament)

    # ------- Demande d'un champ obligatoire (non vide) -------
    def _ask_required_field(self, prompt):
        """
        Demande un champ obligatoire à l'utilisateur·rice.
        - Utilise input_nonempty pour s'assurer que la réponse n'est pas vide.
        - Retourne la valeur saisie ou None si l'utilisateur abandonne après
        plusieurs tentatives.
        """
        # 1️⃣ Appelle input_nonempty avec le message d'invite fourni
        return InputUtils.input_nonempty(prompt)

    # ------- Demande et validation d'une date -------
    def _ask_date(self, prompt):
        """
        Demande une date au format jj/mm/aaaa.
        - Utilise _input_date pour valider la saisie et gérer les tentatives.
        - Retourne la date saisie (chaîne) ou None si l'utilisateur abandonne.
        """
        # 1️⃣ Appelle _input_date pour effectuer la saisie et la validation
        return InputUtils.input_date(prompt)

    # ------- Demande et validation d'une date de fin -------
    def _ask_end_date(self, prompt, start_date):
        """
        Demande une date de fin au format jj/mm/aaaa en s'assurant qu'elle
        est postérieure ou égale à la date de début.
        - Autorise MAX_ATTEMPTS tentatives.
        - Retourne la date valide ou None si abandon ou trop d'erreurs.
        """
        # 1️⃣ Boucle sur un nombre limité de tentatives
        for attempt in range(1, MAX_ATTEMPTS + 1):

            # 🅰 Demande une saisie de date en utilisant _input_date
            saisie = InputUtils.input_date(prompt)
            if saisie is None:  # 🅱 Annulation directe si la saisie échoue
                return None

            # 2️⃣ Convertit les dates en objets datetime pour comparer
            dt_start = datetime.strptime(start_date, "%d/%m/%Y")
            dt_end = datetime.strptime(saisie, "%d/%m/%Y")

            # 3️⃣ Vérifie que la date de fin est postérieure ou égale à la date de début
            if dt_end >= dt_start:
                return saisie  # 🅰 Retourne la date valide

            # 4️⃣ Si la saisie est incorrecte, affiche un message d'erreur et réessaie
            DisplayMessage.display_error_tournament_date(attempt, max_attempts=3)

        # 5️⃣ Trop d'échecs → abandon de l'opération
        DisplayMessage.display_abort_operation()
        return None

    # ------- Demande du nombre de tours pour un tournoi -------
    def _ask_rounds(self):
        """
        Demande à l'utilisateur·rice le nombre de tours pour le tournoi.
        - Si aucune valeur n'est saisie, utilise 4 par défaut.
        - Vérifie que la valeur saisie est un entier positif.
        - Répète la demande tant qu'une valeur correcte n'est pas fournie.
        """
        # 1️⃣ Boucle infinie jusqu'à obtenir une saisie correcte
        while True:
            # 🅰 Lecture de la saisie et suppression des espaces superflus
            nb = input("Nombre de tours (défaut 4) : ").strip()

            # 2️⃣ Si l'utilisateur ne saisit rien → valeur par défaut 4
            if nb == "":
                return 4

            # 3️⃣ Si la saisie est un entier positif → on retourne ce nombre
            if nb.isdigit() and int(nb) > 0:
                return int(nb)

            # 4️⃣ Sinon, message d'erreur et on redemande
            DisplayMessage.display_tournament_rounds()

    # ------- Sauvegarde et confirmation après création d'un tournoi -------
    def _save_and_confirm(self, tournament):
        """
        Sauvegarde le tournoi nouvellement créé et affiche un résumé.
        - Utilise la méthode _save() pour enregistrer les données.
        - Affiche ensuite les informations principales du tournoi.
        """
        # 1️⃣ Sauvegarde immédiate des données du tournoi dans un fichier ou une base locale
        self._save(tournament)

        # 2️⃣ Affiche une confirmation visuelle de création réussie
        DisplayMessage.display_tournament_created_message()

        # 3️⃣ Affiche un récapitulatif clair des données du tournoi
        DisplayMessage.display_tournament_info_details(tournament)

    # -----------------------
    #   LISTE TOURNOI
    # -----------------------

    def list_tournaments(self):
        """Affiche la liste des tournois triée par nom."""
        # 1️⃣ Trie les tournois par nom (insensible à la casse)
        tournaments_sorted = sorted(self._tournaments, key=lambda t: t.name.lower())
        # 2️⃣ Délégation de l'affichage détaillé à ConsoleView
        #    Cette méthode va lister chaque tournoi avec ses infos clés
        ConsoleView.show_tournaments(tournaments_sorted)
        # 3️⃣ Si aucun tournoi n'est enregistré, affiche un message approprié
        if not tournaments_sorted:
            DisplayMessage.display_tournament_not_saved()

    # -----------------------
    #   MODIFICATION TOURNOI
    # -----------------------

    # ------- Modification des informations d'un tournoi existant -------
    def modify_tournament(self):
        """
        Modifie les informations d'un tournoi existant en utilisant des méthodes dédiées :
        1. Sélectionne le tournoi à modifier
        2. Affiche ses informations actuelles
        3. Met à jour chaque champ (nom, lieu, dates, description, rounds)
        4. Sauvegarde et confirme la mise à jour
        """
        # 1️⃣ Affiche le titre pour signaler l'entrée en mode modification
        DisplayMessage.display_update_tournament_title()

        # 2️⃣ Sélection du tournoi à modifier via un menu
        tournament = self._choose("modifier")
        if not tournament:  # 🅰 Annulation si aucun tournoi n'est sélectionné
            return

        # 3️⃣ Affiche les informations actuelles pour donner un contexte
        self._display_tournament_info(tournament)

        # 4️⃣ Modification des champs un par un, en utilisant les méthodes utilitaires

        # 🅰 Nom du tournoi (vide = conserve l'ancien)
        tournament.name = self._edit_text_field("Nom", tournament.name)

        # 🅱 Lieu du tournoi
        tournament.place = self._edit_text_field("Lieu", tournament.place)

        # 🅲 Date de début (avec vérification du format jj/mm/aaaa)
        tournament.start_date = self._edit_date_field(
            "Date début", tournament.start_date
        )

        # 🅳 Date de fin (vérification du format + cohérence >= date début)
        tournament.end_date = self._edit_date_field(
            "Date fin", tournament.end_date, tournament.start_date
        )

        # 🅴 Description du tournoi
        tournament.description = self._edit_text_field(
            "Description", tournament.description
        )

        # 🅵 Nombre de tours (entier positif ou garde la valeur existante)
        tournament.total_rounds = self._edit_rounds(tournament.total_rounds)

        # 5️⃣ Sauvegarde du tournoi modifié et affichage d'un résumé
        self._confirm_and_save(tournament)

    # ------- Affichage des informations actuelles d'un tournoi -------
    def _display_tournament_info(self, tournament):
        """
        Affiche les informations actuelles d'un tournoi :
        - Nom, lieu, dates, description et nombre de tours.
        - Indique que laisser un champ vide conserve la valeur actuelle.
        """
        # 1️⃣ Affiche le titre avec le nom du tournoi
        DisplayMessage.display_current_tournament_info()

        # 2️⃣ Affiche les détails principaux du tournoi
        DisplayMessage.display_tournament_updated_details(tournament)

        # 3️⃣ Rappel pour l'utilisateur : un champ vide garde l'ancienne valeur
        DisplayMessage.display_tournament_consigne()

    # ------- Édition d’un champ texte avec valeur actuelle proposée -------
    def _edit_text_field(self, label, current):
        """
        Demande une nouvelle valeur pour un champ texte.
        - Affiche la valeur actuelle entre crochets.
        - Si l'utilisateur saisit une valeur, elle est retournée.
        - Si l'utilisateur laisse vide, on conserve la valeur actuelle.
        """
        # 1️⃣ Demande une saisie en affichant la valeur actuelle
        new = input(f"{label} [{current}] : ").strip()

        # 2️⃣ Retourne la nouvelle valeur si saisie, sinon garde l'ancienne
        return new if new else current

    # ------- Édition d’une date avec validation du format et cohérence -------
    def _edit_date_field(self, label, current, min_date=None):
        """
        Demande une nouvelle date (format jj/mm/aaaa) pour un champ.
        - Si l'utilisateur laisse vide, conserve la date actuelle.
        - Valide le format et, si min_date est fourni, vérifie que la nouvelle date
        est postérieure ou égale à cette min_date.
        """
        # 1️⃣ Boucle jusqu'à obtenir une saisie correcte ou conserver la valeur existante
        while True:
            # 🅰 Demande la saisie en affichant la valeur actuelle
            new = input(f"{label} [{current}] : ").strip()

            # 🅱 Si aucune saisie → on garde la valeur actuelle
            if not new:
                return current

            try:
                # 2️⃣ Conversion de la saisie en objet date pour validation
                date_val = datetime.strptime(new, "%d/%m/%Y")

                # 3️⃣ Si une min_date est fournie, on vérifie la cohérence
                if min_date:
                    min_val = datetime.strptime(min_date, "%d/%m/%Y")
                    if date_val < min_val:
                        DisplayMessage.display_tournament_end_date_error()
                        continue  # Redemande la saisie

                # 4️⃣ Retourne la nouvelle date valide
                return new

            except ValueError:
                # 5️⃣ En cas de format invalide, affiche un exemple et recommence
                DisplayMessage.display_error_format_date()

    # ------- Édition du nombre de tours avec validation -------
    def _edit_rounds(self, current):
        """
        Demande un nouveau nombre de tours pour un tournoi.
        - Affiche la valeur actuelle et permet de la conserver si aucune saisie.
        - Valide que la saisie est un entier positif.
        """
        # 1️⃣ Boucle jusqu'à obtenir une saisie correcte ou conserver la valeur actuelle
        while True:
            # 🅰 Demande une saisie en affichant le nombre actuel
            nb = input(f"Nombre de tours [{current}] : ").strip()

            # 2️⃣ Si aucune saisie → conserve la valeur actuelle
            if nb == "":
                return current

            # 3️⃣ Vérifie que la saisie est un entier positif
            if nb.isdigit() and int(nb) > 0:
                return int(nb)

            # 4️⃣ Message d'erreur si la saisie est invalide et relance la demande
            DisplayMessage.display_tournament_update_rounds()

    # ------- Sauvegarde et confirmation après création -------
    def _confirm_and_save(self, tournament):
        """
        Sauvegarde un tournoi après modification et affiche un récapitulatif.
        Étapes :
        1. Sauvegarde des données mises à jour
        2. Affiche une confirmation visuelle
        3. Montre toutes les informations actuelles du tournoi
        """
        # 1️⃣ Sauvegarde du tournoi mis à jour
        self._save(tournament)

        # 2️⃣ Message de confirmation
        DisplayMessage.display_tournament_updated_message()

        # 3️⃣ Affiche les informations actualisées du tournoi
        DisplayMessage.display_tournament_info_details(tournament)

    # -----------------------
    #   SUPPRESSION TOURNOI
    # -----------------------

    # ------- Suppression d'un tournoi existant -------
    def delete_tournament(self):
        """Supprime un tournoi existant."""
        # 1️⃣ Affichage de l'en‑tête de suppression
        DisplayMessage.display_delete_tournament_title()

        # 2️⃣ Sélection du tournoi à supprimer
        #    _choose("supprimer") affiche la liste et renvoie l'objet ou None
        tournament = self._choose("supprimer")
        if not tournament:  # Si aucun tournoi n'est sélectionné ou erreur
            return

        # 3️⃣ Demande de confirmation à l'utilisateur·rice
        #    Seul "o" (oui) en minuscules valide la suppression
        if input(f"\nSupprimer {tournament.name} (o/N) ? ").lower() != "o":
            return

        # 4️⃣ Construction du chemin vers le fichier JSON correspondant
        #    On reprend la même logique que _file_path : nom en minuscules et underscores
        path = DATA_DIR / f"{tournament.name.lower().replace(' ', '_')}.json"

        # 5️⃣ Suppression du fichier JSON si présent
        if path.exists():
            path.unlink()  # supprime physiquement le fichier

        # 6️⃣ Retrait de l'objet Tournament de la liste en mémoire
        self._tournaments.remove(tournament)

        # 7️⃣ Message de confirmation final
        DisplayMessage.display_tournament_deleted(tournament)
