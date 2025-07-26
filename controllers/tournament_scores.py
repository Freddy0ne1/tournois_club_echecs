"""
Module tournament_scores
Gère la saisie des scores pour le round en cours d'un tournoi.
"""

from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour la saisie et l'enregistrement des scores.
    """

    # -----------------------
    #   SAISIE SCORES
    # -----------------------

    # ------- Saisie et enregistrement des scores du round en cours -------
    def enter_scores_current_round(self):
        """
        Saisit les scores du round en cours d'un tournoi.
        Étapes :
        1. Sélectionne le tournoi
        2. Vérifie que les scores peuvent être saisis
        3. Si le round est déjà terminé, affiche le récapitulatif
        4. Sinon, collecte les scores pour chaque match
        5. Enregistre et affiche le résumé des résultats
        """
        # 1️⃣ Affiche un titre pour signaler la saisie des scores
        print("\n--- Saisie des scores du round en cours ---")

        # 2️⃣ Sélection du tournoi
        tournament = self._choose("saisir les scores")
        if not tournament:  # 🅰 Annule si aucun tournoi sélectionné
            return

        # 3️⃣ Vérifie si les scores peuvent être saisis (tournoi en cours, etc.)
        if not self._can_enter_scores(tournament):
            return

        # 4️⃣ Récupère le round en cours et son numéro
        rnd, num = tournament.rounds[-1], tournament.current_round_index

        # 5️⃣ Vérifie si le round est déjà terminé, si oui on sort
        if self._is_round_finished(rnd, num):
            return

        # 6️⃣ Collecte les scores saisis pour chaque match du round
        results, recap = self._collect_scores(rnd, num, tournament.name)

        # 7️⃣ Enregistre les résultats dans le tournoi
        tournament.record_results(results)

        # 8️⃣ Sauvegarde l'état mis à jour
        self._save(tournament)

        # 9️⃣ Affiche le récapitulatif des scores saisis
        self._display_scores_recap(recap, num)

    # ------- Vérification des conditions pour saisir les scores -------
    def _can_enter_scores(self, tournament):
        """
        Vérifie si les scores peuvent être saisis pour le tournoi donné.
        Conditions :
        - Le tournoi doit être démarré
        - Il ne doit pas être terminé
        Retourne True si la saisie des scores est possible, sinon False.
        """
        # 1️⃣ Vérifie si le tournoi n'a pas encore démarré
        if tournament.status == "non démarré":
            print("\n❌ Impossible : Le tournoi n'a pas encore démarré.")
            print("💡 Utilisez l'option 6 du menu Tournoi pour démarrer le tournoi.")
            return False

        # 2️⃣ Vérifie si le tournoi est déjà terminé
        if tournament.status == "terminé":
            print(f"\nℹ️  Le tournoi '{tournament.name}' est déjà terminé.")
            return False

        # 3️⃣ Si les conditions sont respectées, on peut saisir les scores
        return True

    # ------- Vérifie si le round est déjà terminé et affiche les scores -------
    def _is_round_finished(self, rnd, num):
        """
        Vérifie si un round est déjà terminé.
        - Si terminé, affiche un récapitulatif des scores
        et retourne True.
        - Sinon retourne False.
        """
        # 1️⃣ Si le round n'a pas de end_time, il n'est pas terminé
        if not rnd.end_time:
            return False

        # 2️⃣ Affiche un message indiquant que le round est déjà joué
        print("\n🥊 Round déjà joué.")
        print("💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant.")

        # 3️⃣ Affiche le récapitulatif des scores du round terminé
        print(f"\n--- Récapitulatif du round {num} ---")
        for m in rnd.matches:
            p1, p2 = m.players
            s1, s2 = m.scores
            print(
                f"{p1.last_name} {p1.first_name} {s1} - {s2} {p2.last_name} {p2.first_name}"
            )

        # 4️⃣ Retourne True pour indiquer que le round est déjà clôturé
        return True

    # ------- Collecte et enregistre les scores des matchs d’un round -------
    def _collect_scores(self, rnd, num, tournament_name):
        """
        Collecte les scores pour chaque match du round en cours.
        Étapes :
        1. Affiche un en-tête avec le nom du tournoi et le numéro du round
        2. Pour chaque match, demande un score valide (1-0, 0-1, 0.5-0.5)
        3. Construit deux listes :
            - results : tuples prêts à être enregistrés
            - recap : tuples pour afficher le récapitulatif
        Retourne (results, recap)
        """
        # 1️⃣ Affiche le titre et les instructions de saisie
        print(f"\n===== Score du tournoi {tournament_name} =====")
        print("📌 Rappel : format 1-0, 0-1, 0.5-0.5 (1 victoire, 0 défaite, 0.5 nul)")
        print(f"\n🥊 Round {num}\n")

        results = []  # contiendra les scores sous une forme prête pour record_results
        recap = []  # contiendra les données pour affichage final

        # 2️⃣ Parcourt les matchs du round
        for i, m in enumerate(rnd.matches, 1):
            p1, p2 = m.players
            while True:
                # 🅰 Demande la saisie du score
                s = (
                    input(
                        f"{p1.last_name} {p1.first_name}[{p1.national_id}] VS "
                        f"{p2.last_name} {p2.first_name}[{p2.national_id}] : "
                    )
                    .strip()
                    .replace(" ", "")
                )

                # 🅱 Vérifie le format de la saisie
                if s in ("1-0", "0-1", "0.5-0.5"):
                    a, b = map(float, s.split("-"))
                    break

                # 🅲 Message d'erreur si format incorrect
                print("❌ Exemple valide : 1-0, 0-1 ou 0.5-0.5")

            # 🅳 Ajoute le résultat au tableau results et recap
            results.append((num - 1, i - 1, a, b))
            recap.append((p1, p2, a, b))

        return results, recap

    # ------- Demande et valide la saisie du score pour un match -------
    def _ask_match_score(self, match):
        """
        Demande à l'utilisateur·rice de saisir un score valide pour un match.
        Format accepté :
        - 1-0  (le premier joueur gagne)
        - 0-1  (le second joueur gagne)
        - 0.5-0.5 (match nul)
        Retourne un tuple (score_joueur1, score_joueur2) sous forme de float.
        """
        # 1️⃣ Récupère les deux joueurs du match
        p1, p2 = match.players

        # 2️⃣ Boucle jusqu'à obtenir un score valide
        while True:
            # 🅰 Demande la saisie du score
            s = (
                input(
                    f"{p1.last_name} {p1.first_name}[{p1.national_id}] VS "
                    f"{p2.last_name} {p2.first_name}[{p2.national_id}] : "
                )
                .strip()
                .replace(" ", "")
            )

            # 🅱 Vérifie que la saisie correspond à l'un des formats valides
            if s in ("1-0", "0-1", "0.5-0.5"):
                return map(float, s.split("-"))

            # 🅲 Affiche un message d'erreur si le format est incorrect
            print("❌ Exemple valide : 1-0, 0-1 ou 0.5-0.5")

    # ------- Affichage du récapitulatif des scores d’un round -------
    def _display_scores_recap(self, recap, num):
        """
        Affiche le récapitulatif des scores saisis pour un round.
        Paramètres :
        - recap : liste de tuples (p1, p2, score1, score2)
        - num   : numéro du round (1-based)
        """
        # 1️⃣ Affiche le titre du récapitulatif
        print(f"\n--- Récapitulatif du round {num} ---")

        # 2️⃣ Parcourt la liste recap et affiche chaque score
        for p1, p2, a, b in recap:
            print(
                f"{p1.last_name} {p1.first_name} {a} - {b} "
                f"{p2.last_name} {p2.first_name}"
            )

        # 3️⃣ Confirmation de l'enregistrement
        print("\n💾 Scores enregistrés.")
        print("💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant.")
