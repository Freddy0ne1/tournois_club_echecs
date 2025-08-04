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
            print("⚠️  Créez-en un pour commencer (1. Créer un tournoi)\n")
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
        1. Sélection du tournoi
        2. Vérifie que le tournoi n'est pas terminé
        3. Vérifie que le round précédent est bien clôturé
        4. Vérifie que le nombre maximum de rounds n'est pas dépassé
        5. Lance le round suivant et sauvegarde l'état du tournoi
        """
        # 1️⃣ Affiche le titre pour indiquer l'action en cours
        print("\n--- Démarrage du round suivant ---")

        # 2️⃣ Permet à l'utilisateur de choisir le tournoi
        tournament = self._choose("démarrer le round suivant")
        if not tournament:  # 🅰 Annule si aucun tournoi sélectionné
            return

        # 3️⃣ Empêche de lancer un round si le tournoi est déjà terminé
        if tournament.status == "terminé":
            print(f"❌ Impossible : le tournoi '{tournament.name}' est déjà terminé.")
            return

        # 4️⃣ Vérifie que le dernier round est bien clôturé avant d'en lancer un nouveau
        if tournament.rounds and not tournament.rounds[-1].end_time:
            print("⚠️  Il faut clôturer le round en cours avant de démarrer le suivant.")
            return

        # 5️⃣ Vérifie que le nombre maximum de rounds n'est pas déjà atteint
        if tournament.current_round_index >= tournament.total_rounds:
            print("ℹ️  Tous les rounds ont déjà été joués.")
            return

        # 6️⃣ Lance le nouveau round et sauvegarde l'état du tournoi
        tournament.start_next_round()
        self._save(tournament)
        print("🏁 Nouveau round démarré.")

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
