"""
Contrôleur des rounds et de la saisie des scores.

Ce module gère toutes les étapes liées au déroulement d'un tournoi :
- Démarrage d'un tournoi (initialisation et génération du premier round)
- Passage au round suivant
- Affichage des appariements et résultats
- Saisie et enregistrement des scores

Il repose sur TournamentRoundController (hérité de TournamentControllerBase)
pour la gestion des tournois et la persistance des données.
"""

from views.console_view import ConsoleView
from .tournament_controller_base import (
    TournamentControllerBase as TournamentRoundController,
)


class TournamentRound(TournamentRoundController):
    """
    Contrôleur pour la gestion du déroulement des rounds.

    Responsabilités :
    - Démarrer un tournoi (vérification des conditions et génération du premier round)
    - Lancer le round suivant après clôture du précédent
    - Afficher les appariements des joueurs pour chaque round
    - Saisir et enregistrer les scores des matchs
    - Afficher les résultats et récapitulatifs

    Cette classe s'appuie sur TournamentRoundController pour :
    - Les outils de sélection de tournoi (_choose)
    - La sauvegarde de l'état des tournois (_save)
    """

    # -----------------------
    #   DEMARRAGE TOURNOI
    # -----------------------

    # ------- Démarrage d’un tournoi et création du premier round -------
    def start_tournament(self):
        """
        Démarre un tournoi si toutes les conditions sont réunies :
        1. Choisit le tournoi
        2. Vérifie les conditions (au moins 2 joueurs, nombre pair, etc.)
        3. Lance le tournoi (changement de statut et création du premier round)
        4. Affiche les matchs du premier round
        """
        # 1️⃣ Affiche un titre pour signaler l'action
        print("\n--- Démarrage d'un tournoi ---")

        # 2️⃣ Recharge les tournois depuis les fichiers
        self.reload_tournaments()

        # 3️⃣ Ne garde que les tournois non démarrés
        non_started = [t for t in self._tournaments if t.status == "non démarré"]

        # 4️⃣ Vérifie qu'il en reste
        if not non_started:
            print("\n🔍 Aucun tournoi non démarré trouvé.")
            print(
                "⚠️  Créez-en un pour commencer (Menu Tournois -> 1. Créer un tournoi)\n"
            )
            return

        # 5️⃣ Sélection du tournoi à démarrer
        tournament = self._choose("démarrer", tournament_list=non_started)
        if not tournament:  # 🅰 Annule si aucun tournoi sélectionné
            return

        # 6️⃣ Vérifie si le tournoi peut être démarré (via méthode dédiée)
        if not self._can_start_tournament(tournament):
            return

        # 7️⃣ Lance le tournoi et crée le premier round
        self._launch_tournament(tournament)

        # 8️⃣ Affiche les appariements (matchs) du round en cours
        self._display_rounds(tournament)

        # 9️⃣ Indique à l'utilisateur comment saisir les scores
        print(
            "\n💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
        )

    # ------- Vérification des conditions avant de démarrer un tournoi -------
    def _can_start_tournament(self, tournament):
        """
        Vérifie toutes les conditions avant de démarrer un tournoi :
        - Il doit y avoir des joueurs inscrits
        - Leur nombre doit être pair et ≥ 2
        - Le tournoi ne doit pas être déjà terminé ou en cours
        Retourne True si toutes les conditions sont réunies, sinon False.
        """
        # 1️⃣ Vérifie qu'il y a au moins un joueur inscrit
        if not tournament.players:
            print(
                f"\n❌ Aucun joueur inscrit pour le tournoi '{tournament.name}' "
                "(5. Ajouter/Retirer joueurs)."
            )
            return False

        # 2️⃣ Vérifie que le nombre de joueurs est pair et au moins 2
        count = len(tournament.players)
        if count < 2 or count % 2 != 0:
            print("\n❌ Il faut un nombre pair de joueurs (au moins 2).")
            return False

        # 3️⃣ Vérifie que le tournoi n'est pas déjà terminé
        if tournament.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tournament.name}' est déjà terminé.")
            return False

        # 4️⃣ Vérifie que le tournoi n'est pas déjà en cours
        if tournament.status == "en cours":
            print(f"\nℹ️  Statut du tournoi '{tournament.name}' : {tournament.status}.")
            print(
                "💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
            )
            return False

        # 5️⃣ Si toutes les conditions sont réunies, retourne True
        return True

    # ------- Lancer un tournoi : statut, premier round et sauvegarde -------
    def _launch_tournament(self, tournament):
        """
        Lance le tournoi :
        - Passe son statut à "en cours"
        - Crée le premier round avec les appariements
        - Sauvegarde l'état mis à jour
        """
        # 1️⃣ Affiche un message de confirmation de démarrage
        count = len(tournament.players)
        print(f"\n🏁 Tournoi '{tournament.name}' démarré.\n")
        print(f"Joueurs inscrits : {count}")
        print(f"Nombre de rounds : {tournament.total_rounds}\n")

        # 2️⃣ Met à jour le statut du tournoi
        tournament.status = "en cours"

        # 3️⃣ Crée le premier round et génère les appariements
        tournament.start_next_round()

        # 4️⃣ Sauvegarde l'état du tournoi après démarrage
        self._save(tournament)

    # ------- Afficher les rounds et leurs matchs d'un tournoi -------
    def _display_rounds(self, tournament):
        """
        Affiche les appariements (matchs) de tous les rounds du tournoi.
        Pour chaque round :
        - Affiche son numéro
        - Liste les matchs sous la forme :
            Joueur1 [ID] VS Joueur2 [ID]
        """
        # 1️⃣ Parcourt tous les rounds du tournoi avec leur index
        for idx, rnd in enumerate(tournament.rounds, 1):
            # 🅰 Affiche le numéro du round
            print(f"\n🥊 Round {idx} :")

            # 🅱 Affiche chaque match avec les deux joueurs
            for m in rnd.matches:
                p1, p2 = m.players
                print(
                    f"{p1.last_name} {p1.first_name} [{p1.national_id}] VS "
                    f"{p2.last_name} {p2.first_name} [{p2.national_id}]"
                )

    # -----------------------
    #   ROUND SUIVANT
    # -----------------------

    def start_next_round(self):
        """
        Démarre le round suivant du tournoi sélectionné.

        Étapes :
        1. Recharge les tournois depuis les fichiers
        2. Filtre uniquement les tournois en cours
        3. Affiche un message s'il n'y a aucun tournoi disponible
        4. Sélectionne le tournoi à mettre à jour
        5. Vérifie les conditions avant de démarrer le round
        6. Si tous les rounds sont joués, clôture silencieuse
        7. Sinon, lance le round suivant et sauvegarde les données
        """
        # 1️⃣ Affiche un titre pour l’action
        print("\n--- Démarrage du round suivant ---")

        # 2️⃣ Recharge les données à jour depuis les fichiers
        self.reload_tournaments()

        # 3️⃣ Filtre les tournois avec statut "en cours" et trie par nom
        in_progress = sorted(
            [t for t in self._tournaments if t.status == "en cours"],
            key=lambda t: t.name.lower(),
        )

        # 4️⃣ Si aucun tournoi en cours, message d'information
        if not in_progress:
            print("\n🔍 Aucun tournoi en cours pour le moment.")
            print("💡 Démarrez un tournoi avant d'accéder à cette fonctionnalité.\n")
            return

        # 5️⃣ Sélection du tournoi concerné
        tournament = self._choose(
            "démarrer le round suivant", tournament_list=in_progress
        )
        if not tournament:
            return

        # 6️⃣ Vérifie si le dernier round est clôturé
        if tournament.rounds and not tournament.rounds[-1].end_time:
            print(
                "⚠️  Il faut clôturer le round en cours avant d'en démarrer un nouveau."
            )
            return

        # 7️⃣ Si tous les rounds ont été joués, on clôture sans message
        if tournament.current_round_index >= tournament.total_rounds and all(
            r.end_time for r in tournament.rounds
        ):
            tournament.status = "terminé"
            self._save(tournament)
            return

        # 8️⃣ Démarre le prochain round
        tournament.start_next_round()
        self._save(tournament)
        print("🏁 Nouveau round démarré.")

    # -----------------------
    #   SAISIE SCORES
    # -----------------------

    # ------- Saisie et enregistrement des scores du round en cours -------
    def enter_scores_current_round(self):
        """
        Saisie des scores du round en cours.

        """
        # 1️⃣ Affiche le titre principal
        print("\n--- Saisie des scores du round en cours ---")

        # 2️⃣ Recharge les tournois depuis les fichiers présents dans /data/tournaments
        self.reload_tournaments()

        # 3️⃣ Filtre les tournois avec statut "en cours" (et trie par ordre alphabétique)
        in_progress = sorted(
            [t for t in self._tournaments if t.status == "en cours"],
            key=lambda t: t.name.lower(),
        )

        # 4️⃣ Si aucun tournoi en cours, affiche un message d'information et quitte
        if not in_progress:
            print("\n🔍 Aucun tournoi démarré pour le moment.")
            print("💡 Utilisez l'option 6 pour démarrer un tournoi.\n")
            return

        # 5️⃣ Permet à l'utilisateur de choisir un tournoi en cours
        tournament = self._choose("saisir les scores", tournament_list=in_progress)
        if not tournament or not self._can_enter_scores(tournament):
            return  # Annulation ou tournoi non éligible

        # 6️⃣ Récupère le round actuel et son numéro
        rnd, num = tournament.rounds[-1], tournament.current_round_index

        # 7️⃣ Vérifie si le round est déjà terminé
        if self._is_round_finished(rnd, num):
            return

        # 8️⃣ Collecte les scores pour chaque match du round
        results, recap = self._collect_scores(rnd, num, tournament.name)

        # 9️⃣ Enregistre les résultats et sauvegarde l’état du tournoi
        tournament.record_results(results)
        self._save(tournament)

        # 🔟 Affiche un récapitulatif des scores saisis
        self._display_scores_recap(recap, num)

        # 🏁 Si tous les rounds ont été joués, on clôture le tournoi et annonce le vainqueur
        if tournament.current_round_index >= tournament.total_rounds:
            self._finaliser_tournoi_si_termine(tournament)

    # ------- Finalisation du tournoi si tous les rounds sont joués -------
    def _finaliser_tournoi_si_termine(self, tournament):
        """
        Clôture un tournoi arrivé à son terme et détermine le gagnant.

        Règles de départage :
        1. Score le plus élevé
        2. Résultat du duel direct si égalité
        3. Ordre alphabétique en cas d'égalité parfaite
        """
        # 1️⃣ Met à jour le statut du tournoi et sauvegarde
        tournament.status = "terminé"
        self._save(tournament)

        # 2️⃣ Récupère le score maximal et les joueurs ex-æquo
        top_score = max(p.points for p in tournament.players)
        top_players = [p for p in tournament.players if p.points == top_score]

        # 3️⃣ S'il y a un seul gagnant, on l'affiche directement
        if len(top_players) == 1:
            winner = top_players[0]
        else:
            # 4️⃣ Si plusieurs joueurs ont le même score : tentative de départage par duel direct
            winner = None
            for rnd in tournament.rounds:
                for match in rnd.matches:
                    p1, p2 = match.players
                    s1, s2 = match.scores
                    if {p1, p2} <= set(top_players):
                        if s1 > s2:
                            winner = p1
                        elif s2 > s1:
                            winner = p2
                        break
                if winner:
                    break

            # 5️⃣ Si match nul ou aucun duel, départage alphabétique
            if not winner:
                winner = sorted(
                    top_players,
                    key=lambda p: (p.last_name.lower(), p.first_name.lower()),
                )[0]

        # 6️⃣ Affiche le message de fin de tournoi et le classement final
        print(f"\n🏆 Tournoi « {tournament.name} » terminé !")
        print(f"📍 Lieu : {tournament.place}")
        print(f"📅 Du {tournament.start_date} au {tournament.end_date}")
        print(f"👥 Participants : {len(tournament.players)}")
        print(f"🎖 Gagnant : {winner.last_name} {winner.first_name}")

        # 7️⃣ Affiche le classement complet des joueurs
        ConsoleView.show_leaderboard(tournament)

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
