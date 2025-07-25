class ConsoleView:
    """Affiche les menus et les données du tournoi dans la console."""

    # -----------------------
    #   AFFICHAGE DU MENU
    # -----------------------

    @staticmethod
    def menu(title, options):
        """
        Affiche un menu numéroté et demande une sélection valide.
        title   : titre du menu (str)
        options : liste de textes d'options (list de str)
        Retourne l'entier choisi par l'utilisateur.
        """
        # 1️⃣ Affiche le titre du menu entouré de séparateurs
        print(f"\n=== {title} ===")

        # 2️⃣ Affiche chaque option numérotée
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # 3️⃣ Boucle jusqu'à obtenir un choix valide
        while True:
            choice = input(
                "Votre choix : "
            ).strip()  # on récupère la saisie et on enlève les espaces
            if choice.isdigit():  # vérifie que c'est un nombre
                num = int(choice)
                if (
                    1 <= num <= len(options)
                ):  # vérifie que le nombre est dans la bonne plage
                    return num  # retourne le choix valide
            # 4️⃣ En cas d'erreur, on affiche un message et on redemande
            print(f"❌ Option invalide, entrez un nombre entre 1 et {len(options)}.")

    # -----------------------
    #   AFFICHAGE DES JOUEURS
    # -----------------------

    @staticmethod
    def show_players(players):
        """
        Affiche la liste des joueurs, triée par nom puis prénom.
        players : liste d'objets Player
        """
        print("\n--- Liste des joueurs ---")

        # 1️⃣ Trie pour un affichage alphabétique
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))

        # 2️⃣ Affiche chaque joueur avec son numéro, son nom complet et ses infos
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
        Affiche la liste des tournois.
        tournaments : liste d'objets Tournament
        """
        print("\n--- Liste des tournois ---")

        # 1️⃣ Parcourt chaque tournoi et affiche ses principales données
        for idx, t in enumerate(tournaments, 1):
            print(
                f"{idx}. {t.name} - {t.place} - {t.start_date} → {t.end_date} - "
                f"{t.total_rounds} tours - {len(t.players)} joueurs - statut : {t.status}"
            )

    # -----------------------
    #   AFFICHAGE DU CLASSEMENT
    # -----------------------

    @staticmethod
    def show_leaderboard(tour):
        """
        Affiche le classement pour un tournoi donné.
        tour : objet Tournament
        """
        print(f"\n=== Classement : {tour.name} ===")

        # 1️⃣ Trie les joueurs par points décroissants
        ordered = sorted(tour.players, key=lambda p: p.points, reverse=True)

        # 2️⃣ Affiche le rang, le nom complet et le score de chaque joueur
        for rank, p in enumerate(ordered, 1):
            print(f"{rank}. {p.last_name} {p.first_name} - {p.points} pts")

    # -----------------------
    #   AFFICHAGE D'UN ROUND
    # -----------------------

    @staticmethod
    def show_round(round_obj):
        """
        Affiche les détails d'un round :
        round_obj : objet Round
        """
        # 1️⃣ Détermine si le round est toujours en cours ou déjà terminé
        status = round_obj.end_time or "en cours"
        print(f"\n--- {round_obj.name} : {round_obj.start_time} → {status} ---")

        # 2️⃣ Affiche chaque match avec les noms et scores des deux joueurs
        for idx, m in enumerate(round_obj.matches, 1):
            p1, p2 = m.players
            s1, s2 = m.scores
            print(
                f"{idx}. {p1.last_name} {p1.first_name} {s1} - {s2} {p2.last_name} {p2.first_name}"
            )
