"""
views/console_view.py
Vue console pour l'application Tournois Club Échecs.

Ce module gère exclusivement l'affichage dans le terminal :
- Menus interactifs
- Listes des joueurs et des tournois
- Classements et rounds
Aucune logique métier ni traitement des données n'est effectuée ici.
"""


class ConsoleView:
    """
    Vue console de l'application.

    Rôle :
      - Afficher les informations à l'écran (menus, listes, classements)
      - Proposer des choix interactifs à l'utilisateur
    Contraintes :
      - Ne contient aucune logique métier
      - Ne modifie pas les données, se contente de présenter les résultats
    """

    # -----------------------
    #   AFFICHAGE DU MENU
    # -----------------------

    @staticmethod
    def menu(title, options):
        """
        Affiche un menu interactif numéroté et retourne le choix sélectionné.

        Paramètres :
        - title (str)   : le titre du menu à afficher.
        - options (list): liste de chaînes représentant les différentes options.

        Retour :
        - int : numéro de l'option choisie par l'utilisateur (1 = première option).
        """
        # 1️⃣ Affiche un en-tête clair pour présenter le menu
        print(f"\n=== {title} ===")

        # 2️⃣ Parcourt toutes les options et les affiche avec une numérotation
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # 3️⃣ Boucle jusqu'à obtenir une saisie valide
        while True:
            # 🅰 Demande une saisie utilisateur et supprime les espaces inutiles
            choice = input("Votre choix : ").strip()

            # 🅱 Vérifie si la saisie est bien un nombre entier
            if choice.isdigit():
                num = int(choice)
                # 🅲 Vérifie si ce nombre est dans la plage d'options disponibles
                if 1 <= num <= len(options):
                    return num  # choix valide → on retourne le numéro choisi

            # 4️⃣ En cas d'erreur (non nombre ou hors plage), on réaffiche un message
            print(f"❌ Option invalide, entrez un nombre entre 1 et {len(options)}.")

    # -----------------------
    #   AFFICHAGE DES JOUEURS
    # -----------------------

    @staticmethod
    def show_players(players):
        """
        Affiche une liste de joueurs sous forme numérotée et triée.

        Paramètres :
        - players (list) : liste d'objets Player à afficher.

        Affichage :
        - Chaque ligne contient :
            numéro. NOM Prénom | Identifiant | Date de naissance
        """
        # 1️⃣ Affiche un titre clair avant la liste
        print("\n--- Liste des joueurs ---\n")

        # 2️⃣ Trie la liste reçue par ordre alphabétique
        #    - d'abord par le nom (last_name)
        #    - puis par le prénom (first_name)
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))

        # 3️⃣ Parcourt la liste triée et affiche chaque joueur avec un numéro
        for idx, p in enumerate(players_sorted, 1):
            print(
                f"{idx}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    # -----------------------
    #   AFFICHAGE DES TOURNOIS
    # -----------------------

    @staticmethod
    def show_tournaments(tournaments):
        """
        Affiche une liste numérotée de tournois et leurs informations principales.

        Paramètres :
        - tournaments (list) : liste d'objets Tournament à afficher.

        Affichage :
        - Chaque ligne contient :
            numéro. Nom - Lieu - Date début → Date fin - Nb tours - Nb joueurs - Statut
        """
        # 1️⃣ Affiche un titre clair avant la liste
        print("\n--- Liste des tournois ---\n")

        # 2️⃣ Parcourt la liste des tournois et affiche les informations clés pour chacun
        for idx, t in enumerate(tournaments, 1):
            print(
                f"{idx}. {t.name} - {t.place} - {t.start_date} → {t.end_date} - "
                f"{t.total_rounds} tours - {len(t.players)} joueurs - statut : {t.status}"
            )

    # -----------------------
    #   AFFICHAGE DU CLASSEMENT
    # -----------------------

    @staticmethod
    def show_leaderboard(tournament):
        """
        Affiche le classement des joueurs pour un tournoi donné.

        Paramètres :
        - tournament (Tournament) : tournoi dont on veut afficher le classement.

        Affichage :
        - Classement trié par points décroissants.
        - Chaque ligne contient :
            rang. NOM Prénom - points pts
        """
        # 1️⃣ Affiche un titre avec le nom du tournoi
        print(f"\n=== Classement du tournoi : {tournament.name} ===")

        # 2️⃣ Trie les joueurs par nombre de points décroissant
        ordered = sorted(tournament.players, key=lambda p: p.points, reverse=True)

        # 3️⃣ Affiche le classement avec rang, nom complet et points
        for rank, p in enumerate(ordered, 1):
            print(f"{rank}. {p.last_name} {p.first_name} - {p.points} pts")

    # -----------------------
    #   AFFICHAGE D'UN ROUND
    # -----------------------

    @staticmethod
    def show_round(round_obj):
        """
        Affiche les informations d'un round précis.

        Paramètres :
        - round_obj (Round) : round à afficher

        Affichage :
        - En-tête indiquant le nom du round, la date/heure de début et
        la date/heure de fin (ou "en cours").
        - La liste des matchs du round avec le format :
            numéro. NOM1 Prénom1 score1 - score2 NOM2 Prénom2
        """
        # 1️⃣ Détermine le statut du round : terminé (end_time) ou en cours
        status = round_obj.end_time or "en cours"

        # 2️⃣ Affiche l'en‑tête du round avec sa période
        print(f"\n--- {round_obj.name} : {round_obj.start_time} → {status} ---")

        # 3️⃣ Parcourt et affiche chaque match de ce round
        for idx, m in enumerate(round_obj.matches, 1):
            p1, p2 = m.players
            s1, s2 = m.scores
            print(
                f"{idx}. {p1.last_name} {p1.first_name} {s1} - {s2} {p2.last_name} {p2.first_name}"
            )
