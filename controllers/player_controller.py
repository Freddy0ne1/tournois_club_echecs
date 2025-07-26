"""controllers/player_controller.py
Contrôleur pour gérer les joueurs.
"""

import re
from datetime import datetime
from views.console_view import ConsoleView
from models.player import Player

# -----------------------
#   LIMITE DE TENTATIVES
# -----------------------

# 1️⃣ Nombre maximal de tentatives autorisées pour une saisie obligatoire
MAX_ATTEMPTS = 3

# -----------------------
#   CONTROLEUR JOUEURS
# -----------------------


class PlayerController:
    """
    Contrôleur pour la gestion des joueurs.
    Responsabilités :
      - Créer de nouveaux joueurs
      - Modifier les informations existantes
      - Supprimer un joueur
      - Lister tous les joueurs
      - Rechercher un joueur spécifique
    """

    # Les méthodes implémentées dans cette classe couvriront :
    #   - create_player() : création d'un joueur
    #   - modify_player() : modification d'un joueur existant
    #   - delete_player() : suppression d'un joueur
    #   - list_players()  : affichage de tous les joueurs
    #   - search_player() : recherche d'un joueur par ID, nom, etc.

    # -----------------------
    #   SAISIE NON VIDE
    # -----------------------

    def _input_nonempty(self, prompt):
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
            print(
                f"\n🔴  Ce champ est obligatoire. "
                f"({attempt}/{MAX_ATTEMPTS}). Réessayez.\n"
            )

        # 3️⃣ Si le nombre maximum de tentatives est atteint, on abandonne
        print("❌ Nombre de tentatives dépassé. Opération abandonnée.")
        return None

    # -----------------------
    #   SAISIE ET VALIDATION D'UNE DATE
    # -----------------------

    def _input_date(self, prompt_text):
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
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}). "
                    f"Exemple attendu : 31/12/1990\n"
                )

        # 3️⃣ Si le nombre maximal d'essais est atteint, abandonne
        print("🔁❌ Nombre de tentatives dépassé. Opération abandonnée.")
        return None

    # -----------------------
    #   TRI ALPHABÉTIQUE DES JOUEURS
    # -----------------------

    def _get_sorted_players(self):
        """
        Retourne une nouvelle liste des joueurs (Player.registry) triée par nom puis prénom.
        Étapes :
        1. Récupère la liste globale des joueurs depuis Player.registry
        2. Trie la liste par nom (last_name) puis par prénom (first_name)
        3. Retourne la liste triée (sans modifier Player.registry)
        """
        # 1️⃣ Accède à la liste des joueurs enregistrés (Player.registry)
        # 2️⃣ Utilise sorted() pour générer une liste triée
        #    - key=lambda p: (p.last_name, p.first_name) : tri alphabétique
        #      en priorité sur le nom, puis sur le prénom
        # 3️⃣ Retourne la nouvelle liste triée
        return sorted(Player.registry, key=lambda p: (p.last_name, p.first_name))

    # -----------------------
    #   SÉLECTION D'UN JOUEUR
    # -----------------------

    def _choose_player(self, action):
        """
        Affiche la liste des joueurs et demande à l'utilisateur d'en choisir un
        pour réaliser une action donnée (modifier, supprimer, etc.).
        Paramètre :
        - action : texte affiché pour indiquer l'action (ex. "modifier")
        Retour :
        - L'objet Player sélectionné ou None si saisie invalide ou annulation
        Étapes :
        1. Récupère la liste triée des joueurs
        2. Vérifie si la liste est vide
        3. Affiche la liste des joueurs avec un numéro
        4. Demande à l'utilisateur d'entrer un numéro
        5. Vérifie que la saisie est un nombre
        6. Vérifie que l'index saisi est valide
        7. Retourne le joueur sélectionné ou None
        """
        # 1️⃣ Récupère la liste triée des joueurs (par nom puis prénom)
        players = self._get_sorted_players()

        # 2️⃣ Si la liste est vide, affiche un message et retourne None
        if not players:
            print("🔍 Aucun joueur disponible.")
            return None

        # 3️⃣ Affiche les joueurs numérotés grâce à la ConsoleView
        ConsoleView.show_players(players)

        # 4️⃣ Invite l'utilisateur à entrer le numéro du joueur
        choice = input(f"\nNuméro du joueur à {action} : ").strip()

        # 5️⃣ Vérifie que la saisie est un nombre valide
        if not choice.isdigit():
            print("❌ Entrée invalide. Utilisez un numéro.")
            return None

        # 6️⃣ Convertit la saisie en entier et vérifie si l'index est dans la plage
        idx = int(choice)
        if 1 <= idx <= len(players):
            # 7️⃣ Si valide, retourne le joueur correspondant
            return players[idx - 1]

        # 8️⃣ Sinon, avertit que le numéro est hors plage et retourne None
        print("❌ Indice hors plage.")
        return None

    # -----------------------
    #   CREATION JOUEUR
    # -----------------------

    # ------- Questions pour créer un nouveau joueur -------
    def create_player(self):
        """
        Crée un nouveau joueur en posant une série de questions à l'utilisateur·rice.
        Étapes :
        1. Affiche un en-tête
        2. Demande un identifiant national unique et valide
        3. Demande le nom (transformé en majuscules)
        4. Demande le prénom (capitalisé)
        5. Demande et valide la date de naissance (format jj/mm/aaaa)
        6. Crée le joueur et sauvegarde le registre
        7. Affiche un récapitulatif des informations saisies
        """
        # 1️⃣ Affiche un titre pour indiquer la création d'un joueur
        print("\n--- Création d'un nouveau joueur ---\n")

        # 2️⃣ Demande l'identifiant national unique
        national_id = self._ask_unique_national_id()
        if not national_id:  # 🅰 Abandon si aucun identifiant valide n'a été saisi
            return

        # 3️⃣ Demande et formate le nom en majuscules
        last_name = self._ask_name("Nom du joueur : ", upper=True)
        if not last_name:
            return

        # 4️⃣ Demande et formate le prénom (1re lettre en majuscule)
        first_name = self._ask_name("Prénom : ", capitalize=True)
        if not first_name:
            return

        # 5️⃣ Demande la date de naissance et vérifie son format
        birth_date = self._input_date("Date de naissance (jj/mm/aaaa) : ")
        if birth_date is None:
            return

        # 6️⃣ Crée le joueur et sauvegarde le registre
        new_player = Player(last_name, first_name, birth_date, national_id)
        Player.save_all()

        # 7️⃣ Affiche les informations du joueur nouvellement créé
        self._display_new_player(new_player)

    # ------- Vérification et saisie d'un identifiant national unique -------
    def _ask_unique_national_id(self):
        """
        Demande un identifiant national unique et valide au format 'AB12345'.
        Étapes :
        1. Autorise MAX_ATTEMPTS tentatives
        2. Vérifie que la saisie n'est pas vide
        3. Vérifie le format (AB + 5 chiffres)
        4. Vérifie que l'identifiant n'existe pas déjà
        5. Retourne l'ID validé ou None si échec
        """
        # 1️⃣ Boucle sur un nombre limité de tentatives
        for attempt in range(1, MAX_ATTEMPTS + 1):

            # 🅰 Demande une saisie obligatoire (non vide)
            national_id = self._input_nonempty(
                "Identifiant national (AB+5 chiffres) : "
            )
            # 🅱 Si l'utilisateur abandonne, on quitte immédiatement
            if national_id is None:
                return None

            # 🅲 Mise en majuscules pour uniformiser
            national_id = national_id.upper()

            # 2️⃣ Vérification du format attendu : "AB" + 5 chiffres
            if not re.match(r"AB\d{5}$", national_id):
                print(
                    f"\n❌ Format invalide ({attempt}/{MAX_ATTEMPTS}). "
                    f"Exemple attendu : AB12345\n"
                )
                continue

            # 3️⃣ Vérification que cet identifiant n'existe pas déjà dans le registre
            if any(p.national_id == national_id for p in Player.registry):
                print(f"\n❌ Identifiant déjà utilisé ({attempt}/{MAX_ATTEMPTS}).\n")
                continue

            # 4️⃣ Si format et unicité sont valides, on retourne l'ID
            return national_id

        # 5️⃣ Si toutes les tentatives ont échoué
        print("❌ Échec de la saisie de l'ID. Annulation.")
        return None

    # ------- Demande et formatage du nom ou prénom d'un joueur -------
    def _ask_name(self, prompt, upper=False, capitalize=False):
        """
        Demande un nom ou un prénom à l'utilisateur·rice.
        Étapes :
        1. Utilise _input_nonempty pour garantir une saisie non vide
        2. Applique un formatage selon les options :
            - upper=True      → met tout en majuscules
            - capitalize=True → met la première lettre en majuscule
        3. Retourne la valeur formatée ou None si abandon
        """
        # 1️⃣ Demande une saisie obligatoire
        name = self._input_nonempty(prompt)

        # 2️⃣ Si l'utilisateur abandonne, on retourne None
        if name is None:
            return None

        # 3️⃣ Application éventuelle du formatage
        if upper:  # 🅰 Tout en majuscules
            return name.upper()
        if capitalize:  # 🅱 Première lettre en majuscule
            return name.capitalize()

        # 4️⃣ Sinon, retourne la valeur brute
        return name

    # ------- Affichage de confirmation et détails d'un nouveau joueur -------
    def _display_new_player(self, player):
        """
        Affiche un message de confirmation et les informations du joueur créé.
        Étapes :
        1. Affiche un message de succès
        2. Affiche un en-tête contenant le nom et le prénom
        3. Affiche les détails : date de naissance et identifiant national
        """
        # 1️⃣ Affiche un message confirmant la création du joueur
        print("\n✅ Joueur créé avec succès !\n")

        # 2️⃣ Affiche un titre clair avec le nom et le prénom du joueur
        print(
            f"--- Informations du joueur {player.last_name} {player.first_name} ---\n"
        )

        # 3️⃣ Affiche les informations détaillées
        print(f"Date de naissance : {player.birth_date}")
        print(f"Identifiant       : {player.national_id}")

    # -----------------------
    #   MODIFICATION JOUEUR
    # -----------------------

    # ------- Modification des informations d'un joueur existant -------
    def modify_player(self):
        """
        Modifie les informations d'un joueur existant.
        Étapes :
        1. Affiche un en-tête clair
        2. Demande de sélectionner un joueur existant
        3. Affiche les informations actuelles du joueur
        4. Permet de modifier ses champs (nom, prénom, date de naissance)
        5. Sauvegarde les modifications
        6. Confirme la mise à jour et affiche un récapitulatif
        7. Retourne le joueur mis à jour
        """
        # 1️⃣ Affiche un titre pour indiquer qu'on entre en mode modification
        print("\n--- Modification d'un joueur ---\n")

        # 2️⃣ Demande à l'utilisateur de choisir le joueur à modifier
        player = self._choose_player("modifier")
        if not player:  # 🅰 Annule si aucun joueur n'est sélectionné
            return

        # 3️⃣ Affiche les informations actuelles pour donner le contexte
        self._display_player_info(player, "actuelles")

        # 4️⃣ Demande et met à jour les champs modifiables
        self._update_player_fields(player)

        # 5️⃣ Sauvegarde les changements dans le registre (players.json)
        Player.save_all()

        # 6️⃣ Confirmation et affichage des nouvelles informations
        self._confirm_player_update(player)

        # 7️⃣ Retourne le joueur modifié
        return player

    # ------- Affichage des informations d'un joueur (actuelles ou mises à jour) -------
    def _display_player_info(self, player, label="actuelles"):
        """
        Affiche les informations d'un joueur.
        Étapes :
        1. Affiche un titre contextuel (ex. infos actuelles ou nouvelles)
        2. Affiche les détails du joueur : identifiant et date de naissance
        3. Si label vaut "actuelles", ajoute une note expliquant que laisser
            un champ vide permet de conserver la valeur existante
        """
        # 1️⃣ Affiche un titre contextualisé (actuelles ou nouvelles infos)
        print(
            f"\n--- Informations {label} de {player.first_name} {player.last_name} ---"
        )

        # 2️⃣ Affiche les informations principales
        print(f"ID                : {player.national_id}")
        print(f"Date de naissance : {player.birth_date}")

        # 3️⃣ Si on affiche les infos actuelles, ajoute une note explicative
        if label == "actuelles":
            print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

    # ------- Mise à jour des champs d'un joueur existant (nom, prénom, date de naissance) -------
    def _update_player_fields(self, player):
        """
        Demande et met à jour les informations d'un joueur existant.
        Étapes :
        1. Demande un nouveau nom (vide = conserver l'ancien)
        2. Demande un nouveau prénom (vide = conserver l'ancien)
        3. Demande une nouvelle date de naissance (vide = conserver l'ancienne)
            - Valide le format jj/mm/aaaa
        """
        # 1️⃣ Demande un nouveau nom de famille (laisser vide pour garder l'ancien)
        value = input(f"Nom [{player.last_name}] : ").strip()
        if value:  # 🅰 Met le nom en majuscules si une nouvelle valeur est saisie
            player.last_name = value.upper()

        # 2️⃣ Demande un nouveau prénom (laisser vide pour garder l'ancien)
        value = input(f"Prénom [{player.first_name}] : ").strip()
        if value:  # 🅱 Met une majuscule initiale si une nouvelle valeur est saisie
            player.first_name = value.capitalize()

        # 3️⃣ Demande une nouvelle date de naissance
        while True:
            value = input(f"Date de naissance [{player.birth_date}] : ").strip()
            if value == "":
                # 🅰 Vide → on conserve la valeur actuelle et on sort
                break
            try:
                # 🅱 Vérifie que la date est bien au format jj/mm/aaaa
                datetime.strptime(value, "%d/%m/%Y")
                # Si c'est correct, on met à jour et on quitte la boucle
                player.birth_date = value
                break
            except ValueError:
                # 🅲 Si le format est incorrect, on indique l'exemple attendu
                print("❌ Format invalide. Exemple : 31/12/1990")

    # ------- Confirmation et affichage des informations mises à jour d'un joueur -------
    def _confirm_player_update(self, player):
        """
        Affiche un message de confirmation après modification d'un joueur.
        Étapes :
        1. Affiche un message de confirmation visuel
        2. Affiche un titre pour présenter les informations modifiées
        3. Affiche les nouvelles informations du joueur (nom, prénom, date, ID)
        """
        # 1️⃣ Affiche un message confirmant que la mise à jour a bien été effectuée
        print("\n✅ Mise à jour effectuée.\n")

        # 2️⃣ Affiche un titre pour introduire les nouvelles informations
        print("--- Nouvelles informations du joueur ---\n")

        # 3️⃣ Affiche les informations actualisées du joueur
        print(
            f"{player.last_name} {player.first_name} - {player.birth_date} "
            f"- ID: {player.national_id}"
        )

    # -----------------------
    #   SUPPRESSION JOUEUR
    # -----------------------

    def delete_player(self):
        """
        Supprime un joueur existant après confirmation.
        Étapes :
        1. Affiche un en-tête clair
        2. Permet de sélectionner un joueur à supprimer
        3. Demande confirmation explicite
        4. Supprime le joueur du registre si confirmé
        5. Sauvegarde les modifications
        6. Affiche un message de succès ou d'annulation
        """
        # 1️⃣ Affiche un titre pour entrer en mode suppression
        print("\n--- Suppression d'un joueur ---\n")

        # 2️⃣ Sélectionne un joueur grâce à _choose_player
        player = self._choose_player("supprimer")
        if player is None:  # 🅰 Si annulation ou saisie invalide
            return

        # 3️⃣ Demande confirmation explicite avant la suppression
        confirm = (
            input(
                f"⚠️  Voulez-vous vraiment supprimer {player.first_name} "
                f"{player.last_name} (o/N) ? "
            )
            .strip()
            .lower()
        )

        if confirm == "o":
            # 4️⃣ Retire le joueur du registre global
            Player.registry.remove(player)

            # 5️⃣ Sauvegarde immédiate de la liste mise à jour
            Player.save_all()

            # 6️⃣ Message confirmant la suppression
            print(f"\n✅ {player.first_name} {player.last_name} a été supprimé.\n")
        else:
            # 7️⃣ Si l'utilisateur annule, afficher un message approprié
            print("❌ Suppression annulée.\n")

    # -----------------------
    #   RECHERCHE
    # -----------------------

    def search_player(self):
        """
        Recherche des joueurs dans le registre par nom, prénom,
        identifiant national ou date de naissance.
        Étapes :
        1. Affiche un en-tête clair
        2. Demande un terme de recherche
        3. Cherche les joueurs dont un champ contient ce terme
        4. Si résultats trouvés : trie et affiche
        5. Sinon, affiche un message indiquant qu'il n'y a aucun résultat
        """
        # 1️⃣ Affiche un titre pour signaler le début de la recherche
        print("\n--- Recherche de joueurs ---\n")

        # 2️⃣ Demande le terme de recherche et le met en minuscules
        term = input("Recherche : ").lower().strip()

        # 3️⃣ Parcourt le registre et sélectionne les joueurs correspondant
        results = []
        for p in Player.registry:
            if (
                term in p.last_name.lower()
                or term in p.first_name.lower()
                or term in p.national_id.lower()
                or term in p.birth_date.lower()
            ):
                results.append(p)

        # 4️⃣ Si des joueurs sont trouvés, on les trie et on les affiche
        if results:
            # a) Trie par nom puis prénom
            results = sorted(results, key=lambda p: (p.last_name, p.first_name))
            # b) Affiche la liste via la ConsoleView
            ConsoleView.show_players(results)
        else:
            # 5️⃣ Aucun résultat trouvé : affiche un message explicite
            print("🔍  Aucun résultat trouvé.")

    # -----------------------
    #   LISTER JOUEUR
    # -----------------------

    def list_players(self):
        """
        Affiche la liste de tous les joueurs enregistrés, triés par nom puis prénom.
        Étapes :
        1. Affiche un en-tête clair
        2. Récupère les joueurs triés par nom et prénom
        3. Vérifie si la liste est vide
        4. Affiche les joueurs via ConsoleView
        5. Ajoute une ligne vide pour une meilleure lisibilité
        """
        # 1️⃣ Affiche un titre clair pour la liste des joueurs
        print("\n--- Liste des joueurs ---\n")

        # 2️⃣ Récupère la liste triée de tous les joueurs
        players = self._get_sorted_players()

        # 3️⃣ Si aucun joueur n'est enregistré, affiche un message et sort
        if not players:
            print("Aucun joueur trouvé.\n")
            return

        # 4️⃣ Affiche la liste des joueurs avec numérotation et détails
        ConsoleView.show_players(players)

        # 5️⃣ Ajoute un saut de ligne final pour l'aération
        print()
