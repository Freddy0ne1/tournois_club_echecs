"""
Module tournament_creation
Gère la création d'un nouveau tournoi (saisie, validation et enregistrement).
"""

from datetime import datetime
from models.tournament import Tournament
from .tournament_controller_base import (
    TournamentController as BaseTournamentController,
    MAX_ATTEMPTS,
)


# -----------------------
#   CRÉATION TOURNOI
# -----------------------


class TournamentController(BaseTournamentController):
    """Ajoute les méthodes de création de tournoi."""

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
        print("\n=== Création d'un tournoi ===\n")

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
        - Utilise _input_nonempty pour s'assurer que la réponse n'est pas vide.
        - Retourne la valeur saisie ou None si l'utilisateur abandonne après
        plusieurs tentatives.
        """
        # 1️⃣ Appelle _input_nonempty avec le message d'invite fourni
        return self._input_nonempty(prompt)

    # ------- Demande et validation d'une date -------
    def _ask_date(self, prompt):
        """
        Demande une date au format jj/mm/aaaa.
        - Utilise _input_date pour valider la saisie et gérer les tentatives.
        - Retourne la date saisie (chaîne) ou None si l'utilisateur abandonne.
        """
        # 1️⃣ Appelle _input_date pour effectuer la saisie et la validation
        return self._input_date(prompt)

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
            saisie = self._input_date(prompt)
            if saisie is None:  # 🅱 Annulation directe si la saisie échoue
                return None

            # 2️⃣ Convertit les dates en objets datetime pour comparer
            dt_start = datetime.strptime(start_date, "%d/%m/%Y")
            dt_end = datetime.strptime(saisie, "%d/%m/%Y")

            # 3️⃣ Vérifie que la date de fin est postérieure ou égale à la date de début
            if dt_end >= dt_start:
                return saisie  # 🅰 Retourne la date valide

            # 4️⃣ Si la saisie est incorrecte, affiche un message d'erreur et réessaie
            print(
                f"\n❌ La date de fin doit être ≥ date de début ({attempt}/{MAX_ATTEMPTS}).\n"
            )

        # 5️⃣ Trop d'échecs → abandon de l'opération
        print("\n❌ Nombre de tentatives dépassé. Opération annulée.")
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
            print("Entrez un entier positif ou laissez vide pour 4.")

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
        print("\n✅ Tournoi créé.\n")

        # 3️⃣ Affiche un récapitulatif clair des données du tournoi
        print(f"--- Informations du tournoi '{tournament.name}' ---\n")
        print(f"Lieu             : {tournament.place}")
        print(f"Dates            : {tournament.start_date} → {tournament.end_date}")
        print(f"Description      : {tournament.description}")
        print(f"Nombre de tours  : {tournament.total_rounds}")
