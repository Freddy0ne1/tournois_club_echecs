"""utils/input_utils.py
Fonctions utilitaires pour la saisie utilisateur.
Rôle :
  - Gérer les saisies utilisateur avec validation
  - Fournir des fonctions pour des saisies spécifiques (non vide, date)
"""

from datetime import datetime
from views.display_message import DisplayMessage

# Nombre maximum de tentatives pour une saisie utilisateur
MAX_ATTEMPTS = 3


class InputUtils:
    """
    Classe utilitaire pour les saisies utilisateur.
    Rôle :
      - Fournit des méthodes statiques pour gérer les saisies utilisateur
      - Gère les erreurs et les validations de saisie
    """

    # -----------------------
    #   SAISIE NON VIDE
    # -----------------------

    @staticmethod
    def input_nonempty(prompt):
        """
        Demande une saisie non vide à l'utilisateur·rice.
        Étapes :
        1. Affiche un message (prompt) pour demander une saisie
        2. Vérifie que la saisie n'est pas vide
        3. Réessaie jusqu'à MAX_ATTEMPTS
        4. Retourne la valeur saisie ou None si échec
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle : répète la demande jusqu'à atteindre MAX_ATTEMPTS
        while attempt < MAX_ATTEMPTS:
            # 🅰 Affiche le prompt et récupère la saisie utilisateur (supprime espaces inutiles)
            value = input(prompt).strip()

            # 🅱 Si l'utilisateur a saisi une valeur non vide, on la retourne immédiatement
            if value:
                return value

            # 🅲 Sinon, incrémente le compteur et affiche un message d'erreur
            attempt += 1
            DisplayMessage.display_input_nonempty(attempt)

        # 3️⃣ Si le nombre maximum de tentatives est atteint, on abandonne
        DisplayMessage.display_abort_operation()
        # 🅰 Retourne None pour indiquer l'échec
        return None

    # -----------------------
    #   SAISIE ET VALIDATION D'UNE DATE
    # -----------------------

    @staticmethod
    def input_date(prompt_text):
        """
        Demande une date à l'utilisateur·rice au format jj/mm/aaaa.
        Étapes :
        1. Affiche un message (prompt) pour demander une date
        2. Vérifie que la saisie respecte le format jj/mm/aaaa
        3. Réessaie jusqu'à MAX_ATTEMPTS si la saisie est incorrecte
        4. Retourne la date saisie ou None si échec
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle : répète la demande jusqu'à atteindre MAX_ATTEMPTS
        while attempt < MAX_ATTEMPTS:
            # 🅰 Affiche le prompt et récupère la saisie utilisateur (supprime espaces inutiles)
            date_str = input(prompt_text).strip()
            try:
                # 🅱 Tente de convertir la saisie au format jj/mm/aaaa
                datetime.strptime(date_str, "%d/%m/%Y")
                # 🅲 Si la conversion réussit, retourne immédiatement la date saisie
                return date_str
            except ValueError:
                # 🅳 Sinon, incrémente le compteur et affiche un message d'erreur
                attempt += 1
                DisplayMessage.display_input_date(attempt)

        # 3️⃣ Si le nombre maximum de tentatives est atteint, on abandonne
        DisplayMessage.display_abort_operation()
        # 🅰 Retourne None pour indiquer l'échec
        return None
