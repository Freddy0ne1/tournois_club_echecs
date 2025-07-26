"""
Module tournament_start
Gère le démarrage d'un tournoi et la création du premier round.
"""

from .tournament_controller_base import TournamentController as BaseTournamentController


class TournamentController(BaseTournamentController):
    """
    Sous-contrôleur pour le démarrage d'un tournoi.
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

        # 2️⃣ Sélection du tournoi à démarrer
        tournament = self._choose("démarrer")
        if not tournament:  # 🅰 Annule si aucun tournoi sélectionné
            return

        # 3️⃣ Vérifie si le tournoi peut être démarré (via méthode dédiée)
        if not self._can_start_tournament(tournament):
            return

        # 4️⃣ Lance le tournoi et crée le premier round
        self._launch_tournament(tournament)

        # 5️⃣ Affiche les appariements (matchs) du round en cours
        self._display_rounds(tournament)

        # 6️⃣ Indique à l'utilisateur comment saisir les scores
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
            print("\n❌ Impossible : aucun joueur n'est inscrit.")
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
