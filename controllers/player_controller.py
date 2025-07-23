"""controllers/player_controller.py
Contrôleur pour gérer les joueurs.
"""

import re
from datetime import datetime
from views.console_view import ConsoleView
from models.player import Player

# -----------------------
#   Constantes globales
# -----------------------

# 1️⃣ Nombre maximal de tentatives pour chaque saisie obligatoire
#    Utilisé par les méthodes d’entrée pour limiter les boucles d’invite.
MAX_ATTEMPTS = 3


class PlayerController:
    """
    Gère la création, l'affichage, la modification,
    la suppression et la recherche des joueurs.
    """

    # À venir : méthodes pour ajouter un joueur, modifier ses infos,
    # lister tous les joueurs, supprimer et rechercher.

    # -----------------------
    #   MÉTHODES D’AIDE
    # -----------------------

    # -------- Demande de saisie obligatoire ---------

    def _input_nonempty(self, prompt):
        """
        Demande une saisie non vide à l'utilisateur·rice.
        Réessaie jusqu'à obtenir une valeur ou atteint MAX_ATTEMPTS.
        Retourne la chaîne ou None si annulé.
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle de saisie : on autorise MAX_ATTEMPTS essais
        while attempt < MAX_ATTEMPTS:
            # 🅰 On affiche l’invite et on lit la saisie, en supprimant espaces en trop
            value = input(prompt).strip()
            # 🅱 Si l’utilisateur·rice a bien saisi quelque chose, on retourne cette valeur
            if value:
                return value

            # 🅲 Sinon, on incrémente le compteur et on renseigne l’utilisateur·rice
            attempt += 1
            print(
                f"\n🔴  Ce champ est obligatoire. "
                f"({attempt}/{MAX_ATTEMPTS}). Réessayez.\n"
            )

        # 3️⃣ Si le nombre max de tentatives est atteint sans succès
        print("❌ Nombre de tentatives dépassé. Opération abandonnée.")
        return None

    # -------- Demande de saisie date ---------

    def _input_date(self, prompt_text):
        """
        Demande une date au format jj/mm/aaaa.
        Réessaie jusqu'à obtenir un format valide ou atteint MAX_ATTEMPTS.
        Retourne la chaîne valide ou None.
        """
        # 1️⃣ Initialisation du compteur de tentatives
        attempt = 0

        # 2️⃣ Boucle de saisie, limitée à MAX_ATTEMPTS essais
        while attempt < MAX_ATTEMPTS:
            # 🅰 Affiche l’invite et lit la saisie sans espaces superflus
            date_str = input(prompt_text).strip()
            try:
                # 🅱 Vérifie que la chaîne correspond au format jj/mm/aaaa
                datetime.strptime(date_str, "%d/%m/%Y")
                # 🅲 Si la conversion réussit, retourne immédiatement la date saisie
                return date_str
            except ValueError:
                # 🅳 En cas d’erreur de format, incrémente le compteur et informe
                attempt += 1
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}). Ex.: 31/12/1990\n"
                )

        # 3️⃣ Si toutes les tentatives échouent, affiche un message d’abandon et retourne None
        print("🔁❌ Nombre de tentatives dépassé. Opération abandonnée.")
        return None

    # -------- Liste triée joueur de la base ---------

    def _get_sorted_players(self):
        """
        Retourne la liste des Player.registry triée par nom puis prénom.
        """
        # 1️⃣ Récupère la liste de tous les joueurs depuis registry
        # 2️⃣ Utilise sorted() pour créer une nouvelle liste triée
        #    - key=lambda p: (p.last_name, p.first_name) trie d’abord sur le nom,
        #      puis sur le prénom pour départager les homonymes
        # 3️⃣ Retourne cette liste triée sans modifier l’original registry
        return sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

    # -------- sélectionner un joueur ---------

    def _choose_player(self, action):
        """
        Affiche les joueurs et demande de choisir un numéro pour une action.
        Retourne le Player choisi ou None.
        """
        # 1️⃣ Récupère la liste des joueurs triée (nom, prénom)
        players = self._get_sorted_players()

        # 2️⃣ Si la liste est vide, informe et renvoie None
        if not players:
            print("🔍 Aucun joueur disponible.")
            return None

        # 3️⃣ Affiche les joueurs avec leurs numéros via la vue console
        ConsoleView.show_players(players)

        # 4️⃣ Invite l’utilisateur·rice à saisir un numéro pour l’action donnée
        choice = input(f"\nNuméro du joueur à {action} : ").strip()

        # 5️⃣ Vérifie que la saisie est bien un nombre
        if not choice.isdigit():
            print("❌ Entrée invalide. Utilisez un numéro")
            return None

        # 6️⃣ Convertit en entier et vérifie que c’est dans la plage
        idx = int(choice)
        if 1 <= idx <= len(players):
            # 7️⃣ Si c’est valide, renvoie l’objet Player correspondant
            return players[idx - 1]

        # 8️⃣ Sinon, informe que l’indice est hors plage et renvoie None
        print("❌ Indice hors plage.")
        return None

    # -----------------------
    #   CREATION JOUEUR
    # -----------------------

    def create_player(self):
        """Crée un nouveau joueur et l'ajoute à la liste."""

        # 🔔 1️⃣ En‑tête de la création
        print("\n--- Création d'un nouveau joueur ---\n")

        # 2️⃣ Saisie et validation de l’identifiant national (max MAX_ATTEMPTS essais)
        for attempt in range(1, MAX_ATTEMPTS + 1):
            # 🅰 Demande une saisie non vide
            national_id = self._input_nonempty(
                "Identifiant national (AB+5 chiffres) : "
            )
            if national_id is None:
                return  # Abandon si l’utilisateur·rice échoue ou annule

            # 🅱 Normalise en majuscules
            national_id = national_id.upper()

            # 🅲 Vérifie le format "AB" suivi de 5 chiffres
            if not re.match(r"AB\d{5}$", national_id):
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}). Ex. : AB12345\n"
                )
                continue

            # 🅳 Assure l’unicité de l’ID dans le registre
            if any(p.national_id == national_id for p in Player.registry):
                print(f"\n❌ Identifiant déjà utilisé ({attempt}/{MAX_ATTEMPTS}).\n")
                continue

            # ID validé et unique → on sort de la boucle
            break
        else:
            # Tous les essais ont échoué
            print("❌ Échec de la saisie de l'ID. Annulation.")
            return

        # 3️⃣ Saisie du nom (obligatoire)
        last_name = self._input_nonempty("Nom du joueur : ")
        if last_name is None:
            return
        last_name = last_name.upper()  # Mise en majuscules pour homogénéité

        # 4️⃣ Saisie du prénom (obligatoire)
        first_name = self._input_nonempty("Prénom : ")
        if first_name is None:
            return
        first_name = first_name.capitalize()  # Première lettre en majuscule

        # 5️⃣ Saisie de la date de naissance (format jj/mm/aaaa)
        birth_date = self._input_date("Date de naissance (jj/mm/aaaa) : ")
        if birth_date is None:
            return  # Annulation si format invalide

        # 6️⃣ Création de l’instance Player et sauvegarde globale
        new_player = Player(last_name, first_name, birth_date, national_id)
        Player.save_all()  # Persiste la liste complète des joueurs dans players.json

        # 7️⃣ Confirmation et récapitulatif
        print("\n✅ Joueur créé avec succès !\n")
        print(
            f"--- Informations du joueur {new_player.last_name} {new_player.first_name} ---\n"
        )
        print(f"Date de naissance : {new_player.birth_date}")
        print(f"Identifiant       : {new_player.national_id}")

    # -----------------------
    #   MODIFICATION JOUEUR
    # -----------------------

    def modify_player(self):
        """Modifie les informations d'un joueur existant."""

        # 1️⃣ Affiche un titre pour entrer en mode modification
        print("\n--- Modification d'un joueur ---\n")

        # 2️⃣ Sélection du joueur à modifier (affiche la liste et renvoie un Player ou None)
        player = self._choose_player("modifier")
        if not player:  # Si annulation ou saisie invalide, on quitte
            return

        # 3️⃣ Affiche les infos actuelles pour que l’utilisateur sache quoi modifier
        print(
            f"\n--- Informations actuelles de {player.first_name} {player.last_name} ---"
        )
        print(f"ID                : {player.national_id}")
        print(f"Date de naissance : {player.birth_date}")
        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

        # 4️⃣ Modification du nom de famille
        value = input(f"Nom [{player.last_name}] : ").strip()
        if value:  # Si l’utilisateur saisit quelque chose
            player.last_name = value.upper()  # On met en majuscules

        # 5️⃣ Modification du prénom
        value = input(f"Prénom [{player.first_name}] : ").strip()
        if value:
            player.first_name = value.capitalize()  # Majuscule initiale

        # 6️⃣ Modification de la date de naissance (boucle jusqu’à format valide ou vide)
        while True:
            value = input(f"Date de naissance [{player.birth_date}] : ").strip()
            if value == "":  # Vide → on conserve l’ancienne valeur
                break
            try:
                # Vérifie le format jj/mm/aaaa
                datetime.strptime(value, "%d/%m/%Y")
                player.birth_date = value
                break
            except ValueError:
                print("❌ Format invalide. Exemple : 31/12/1990")

        # 7️⃣ Sauvegarde de tous les joueurs mis à jour dans players.json
        Player.save_all()

        # 8️⃣ Confirmation et récapitulatif des nouvelles valeurs
        print("\n✅ Mise à jour effectuée.\n")
        print("--- Nouvelles informations du joueur ---\n")
        print(
            f"{player.last_name} {player.first_name} - {player.birth_date} - "
            f"ID: {player.national_id}"
        )

        return player

    # -----------------------
    #   SUPPRESSION JOUEUR
    # -----------------------

    def delete_player(self):
        """Supprime un joueur existant après confirmation."""

        # 1️⃣ Affichage de l’en‑tête pour entrer en mode suppression
        print("\n--- Suppression d'un joueur ---\n")

        # 2️⃣ Sélection du joueur à supprimer via _choose_player (affiche la liste et renvoie un Player ou None)
        player = self._choose_player("supprimer")
        if player is None:  # Si annulation ou saisie invalide
            return

        # 3️⃣ Confirmation explicite : seul "o" valide la suppression
        confirm = (
            input(
                f"⚠️  Voulez-vous vraiment supprimer {player.first_name} "
                f"{player.last_name} (o/N) ? "
            )
            .strip()
            .lower()
        )
        if confirm == "o":
            # 4️⃣ Suppression de l’objet Player du registre global
            Player.registry.remove(player)
            # 5️⃣ Persistance : écriture immédiate du fichier players.json
            Player.save_all()
            # 6️⃣ Message de succès pour rassurer l’utilisateur·rice
            print(f"\n✅ {player.first_name} {player.last_name} a été supprimé.\n")
        else:
            # 7️⃣ Annulation : l’utilisateur·rice décide de ne pas supprimer
            print("❌ Suppression annulée.\n")

    # -----------------------
    #   RECHERCHE
    # -----------------------

    def search_player(self):
        """Recherche des joueurs par nom, prénom ou identifiant national."""

        # 1️⃣ Affiche un titre pour guider l’utilisateur·rice
        print("\n--- Recherche de joueurs ---\n")

        # 2️⃣ Lit le terme de recherche, en minuscules et sans espaces superflus
        term = input("Recherche : ").lower().strip()

        # 3️⃣ Parcourt tous les joueurs du registre et sélectionne ceux qui contiennent le terme
        results = []
        for p in Player.registry:
            if (
                term in p.last_name.lower()
                or term in p.first_name.lower()
                or term in p.national_id.lower()
                or term in p.birth_date.lower()
            ):
                results.append(p)

        # 4️⃣ Si on a trouvé au moins un résultat, on les trie et on les affiche
        if results:
            # a) Tri alphabétique par nom puis prénom
            results = sorted(results, key=lambda p: (p.last_name, p.first_name))
            # b) Affichage via la vue console
            ConsoleView.show_players(results)
        else:
            # 5️⃣ Aucun résultat → message clair
            print("🔍  Aucun résultat trouvé.")

    # -----------------------
    #   LISTER JOUEUR
    # -----------------------

    def list_players(self):
        """Affiche la liste triée des joueurs."""
        # 1️⃣ Affiche un en‑tête pour démarquer la section
        print("\n--- Liste des joueurs ---\n")

        # 2️⃣ Récupère la liste des joueurs triés par nom puis prénom
        players = self._get_sorted_players()

        # 3️⃣ Si la liste est vide, informe et quitte la méthode
        if not players:
            print("Aucun joueur trouvé.\n")
            return

        # 4️⃣ Délègue l’affichage détaillé à ConsoleView (numérotation, nom, ID, date de naissance)
        ConsoleView.show_players(players)

        # 5️⃣ Ajoute une ligne vide pour l’espacement final
        print()
