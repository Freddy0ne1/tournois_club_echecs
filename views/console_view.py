"""views/console_view.py"""


class ConsoleView:
    """Affiche les menus et les données du tournoi dans la console."""

    @staticmethod
    def menu(title, options):
        """
        Affiche un menu numéroté et demande une sélection valide.
        title   : titre du menu (str)
        options : liste de textes d'options (list de str)
        Retourne l'entier choisi par l'utilisateur.
        """
        print(f"\n=== {title} ===")
        # Affiche les options numérotées
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        while True:
            choice = input("Votre choix : ").strip()
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(options):
                    return num
            print(f"❌ Option invalide, entrez un nombre entre 1 et {len(options)}.")

    @staticmethod
    def show_players(players):
        """
        Affiche la liste des joueurs, triée par nom puis prénom.
        players : liste d'objets Player
        """
        print("\n--- Liste des joueurs ---")
        # on trie ici pour garantir l'ordre alphabétique
        players_sorted = sorted(players, key=lambda p: (p.last_name, p.first_name))
        for idx, p in enumerate(players_sorted, 1):
            print(
                f"{idx}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    @staticmethod
    def show_tournaments(tournaments):
        """
        Affiche la liste des tournois.
        tournaments : liste d'objets Tournament
        """
        print("\n--- Liste des tournois ---")
        for idx, t in enumerate(tournaments, 1):
            print(
                f"{idx}. {t.name} - {t.place} - {t.start_date} → {t.end_date} - "
                f"{t.total_rounds} tours - {len(t.players)} joueurs - statut : {t.status}"
            )

    @staticmethod
    def show_leaderboard(tour):
        """
        Affiche le classement pour un tournoi donné.
        tour : objet Tournament
        """
        print(f"\n=== Classement : {tour.name} ===")
        # tri par points décroissants
        ordered = sorted(tour.players, key=lambda p: p.points, reverse=True)
        for rank, p in enumerate(ordered, 1):
            print(f"{rank}. {p.last_name} {p.first_name} - {p.points} pts")

    @staticmethod
    def show_round(round_obj):
        """
        Affiche les détails d'un round :
        round_obj : objet Round
        """
        status = round_obj.end_time or "en cours"
        print(f"\n--- {round_obj.name} : {round_obj.start_time} → {status} ---")
        for idx, m in enumerate(round_obj.matches, 1):
            p1, p2 = m.players
            s1, s2 = m.scores
            print(
                f"{idx}. {p1.last_name} {p1.first_name} {s1} - {s2} {p2.last_name} {p2.first_name}"
            )
