"""controllers/player_controller.py
Contrôleur pour gérer les joueurs.
"""

import re
from datetime import datetime
from views.display_message import DisplayMessage
from views.console_view import ConsoleView
from models.player import Player
from utils.input_utils import InputUtils, MAX_ATTEMPTS


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
            DisplayMessage.display_not_player()
            return None

        # 3️⃣ Affiche les joueurs numérotés grâce à la ConsoleView
        ConsoleView.show_players(players)

        # 4️⃣ Invite l'utilisateur à entrer le numéro du joueur
        choice = input(f"\nNuméro du joueur à {action} : ").strip()

        # 5️⃣ Vérifie que la saisie est un nombre valide
        if not choice.isdigit():
            DisplayMessage.display_not_isdigit()
            return None

        # 6️⃣ Convertit la saisie en entier et vérifie si l'index est dans la plage
        idx = int(choice)
        if 1 <= idx <= len(players):
            # 7️⃣ Si valide, retourne le joueur correspondant
            return players[idx - 1]

        # 8️⃣ Sinon, avertit que le numéro est hors plage et retourne None
        DisplayMessage.display_out_of_range()
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
        DisplayMessage.display_create_title()

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
        birth_date = InputUtils.input_date("Date de naissance (jj/mm/aaaa) : ")
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
            national_id = InputUtils.input_nonempty(
                "Identifiant national (AB+5 chiffres) : "
            )
            # 🅱 Si l'utilisateur abandonne, on quitte immédiatement
            if national_id is None:
                return None

            # 🅲 Mise en majuscules pour uniformiser
            national_id = national_id.upper()

            # 2️⃣ Vérification du format attendu : "AB" + 5 chiffres
            if not re.match(r"AB\d{5}$", national_id):
                DisplayMessage.display_not_re_match(attempt, MAX_ATTEMPTS)
                continue

            # 3️⃣ Vérification que cet identifiant n'existe pas déjà dans le registre
            if any(p.national_id == national_id for p in Player.registry):
                DisplayMessage.display_already_exists(attempt, MAX_ATTEMPTS)
                continue

            # 4️⃣ Si format et unicité sont valides, on retourne l'ID
            return national_id

        # 5️⃣ Si toutes les tentatives ont échoué
        DisplayMessage.display_abort_operation()
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
        name = InputUtils.input_nonempty(prompt)

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
        DisplayMessage.display_player_created()

        # 2️⃣ Affiche un titre clair avec le nom et le prénom du joueur
        DisplayMessage.display_player_info_title()

        # 3️⃣ Affiche les informations détaillées
        DisplayMessage.display_player_info(player)

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
        DisplayMessage.display_update_player_title()

        # 2️⃣ Demande à l'utilisateur de choisir le joueur à modifier
        player = self._choose_player("modifier")
        if not player:
            return None  # 🅰 Annule si aucun joueur n'est sélectionné

        # 3️⃣ Affiche les informations actuelles pour donner le contexte
        self._display_player_info(player, "actuelles")

        # 4️⃣ Mise à jour des champs du joueur (cette méthode renvoie False si annulartion)
        success = self._update_player_fields(player)
        if not success:  # 🅱 Si l'utilisateur abandonne la modification
            DisplayMessage.display_player_not_updated()
            return None  # Abandonne la modification

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
        DisplayMessage.display_current_player_info(label)

        # 2️⃣ Affiche les informations principales
        DisplayMessage.display_player_info_details(player)

        # 3️⃣ Si on affiche les infos actuelles, ajoute une note explicative
        if label == "actuelles":
            DisplayMessage.display_consigne()

    # ------- Mise à jour des champs d'un joueur existant (nom, prénom, date de naissance) -------
    def _update_player_fields(self, player):
        """
        Demande et met à jour les informations d'un joueur existant.
        Retourne True si une modification a été effectuée, sinon False.
        """
        updated = False  # ✅ Suivi des modifications

        # 1️⃣ Identifiant national
        for attempt in range(1, MAX_ATTEMPTS + 1):
            value = input(f"Identifiant national [{player.national_id}] : ").strip()
            if value == "":
                break  # ➜ Conserver l'ancien
            value = value.upper()
            if not re.match(r"AB\d{5}$", value):
                DisplayMessage.display_not_re_match(attempt, MAX_ATTEMPTS)
                continue
            if any(p.national_id == value and p != player for p in Player.registry):
                DisplayMessage.display_already_exists(attempt, MAX_ATTEMPTS)
                continue
            if value != player.national_id:
                player.national_id = value
                updated = True
            break
        else:
            DisplayMessage.display_abort_operation()
            return False

        # 2️⃣ Nom
        value = input(f"Nom [{player.last_name}] : ").strip()
        if value and value.upper() != player.last_name:
            player.last_name = value.upper()
            updated = True

        # 3️⃣ Prénom
        value = input(f"Prénom [{player.first_name}] : ").strip()
        if value and value.capitalize() != player.first_name:
            player.first_name = value.capitalize()
            updated = True

        # 4️⃣ Date de naissance
        value = input(f"Date de naissance [{player.birth_date}] : ").strip()
        if value:
            try:
                datetime.strptime(value, "%d/%m/%Y")
                if value != player.birth_date:
                    player.birth_date = value
                    updated = True
            except ValueError:
                DisplayMessage.display_error_format_date()

        return updated

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
        DisplayMessage.display_player_updated()

        # 2️⃣ Affiche un titre pour introduire les nouvelles informations
        DisplayMessage.display_player_new_info_title()

        # 3️⃣ Affiche les informations actualisées du joueur
        DisplayMessage.display_player_new_info_details(player)

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
        DisplayMessage.display_delete_player_title()

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
            DisplayMessage.display_player_deleted(player)
        else:
            # 7️⃣ Si l'utilisateur annule, afficher un message approprié
            DisplayMessage.display_player_not_deleted()

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
        DisplayMessage.display_search_title()

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
            DisplayMessage.display_player_not_found()

    # -----------------------
    #   LISTER JOUEUR
    # -----------------------

    def list_players(self):
        """
        Affiche la liste de tous les joueurs enregistrés, triés par nom puis prénom.
        Étapes :
        1. Récupère les joueurs triés par nom et prénom
        2. Vérifie si la liste est vide
        3. Affiche les joueurs via ConsoleView
        4. Ajoute une ligne vide pour une meilleure lisibilité
        """

        # 1️⃣ Récupère la liste triée de tous les joueurs
        players = self._get_sorted_players()

        # 2️⃣ Si aucun joueur n'est enregistré, affiche un message et sort
        if not players:
            DisplayMessage.display_no_players_found()
            return

        # 3️⃣ Affiche la liste des joueurs avec numérotation et détails
        ConsoleView.show_players(players)
