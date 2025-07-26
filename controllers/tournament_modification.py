"""
Module tournament_modification
Ce module gère les fonctionnalités de modification des tournois.
"""

from datetime import datetime
from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur spécialisé dans la modification des informations
    d'un tournoi existant (hérite de BaseTournamentController).
    """

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
        print("\n--- Modification d'un tournoi ---")

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
        print(f"\n--- Infos actuelles du tournoi '{tournament.name}' ---")

        # 2️⃣ Affiche les détails principaux du tournoi
        print(f"Lieu             : {tournament.place}")
        print(f"Dates            : {tournament.start_date} → {tournament.end_date}")
        print(f"Description      : {tournament.description}")
        print(f"Nombre de tours  : {tournament.total_rounds}")

        # 3️⃣ Rappel pour l'utilisateur : un champ vide garde l'ancienne valeur
        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

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
                        print("❌ La date doit être ≥ à la date de début.")
                        continue  # Redemande la saisie

                # 4️⃣ Retourne la nouvelle date valide
                return new

            except ValueError:
                # 5️⃣ En cas de format invalide, affiche un exemple et recommence
                print("❌ Format invalide. Exemple : 31/12/2025")

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
            print("Entrez un entier positif ou laissez vide pour conserver.")

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
        print("\n✅ Mise à jour effectuée.\n")

        # 3️⃣ Affiche les informations actualisées du tournoi
        print(f"--- Nouvelles infos du tournoi '{tournament.name}' ---\n")
        print(f"Lieu             : {tournament.place}")
        print(f"Dates            : {tournament.start_date} → {tournament.end_date}")
        print(f"Description      : {tournament.description}")
        print(f"Nombre de tours  : {tournament.total_rounds}")
