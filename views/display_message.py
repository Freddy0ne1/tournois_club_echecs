"""
views/display_message.py
Ce fichier centralise tous les affichages console utilisés dans les contrôleurs.
Chaque fonction correspond à un print original.
"""

# from controllers.player_controller import MAX_ATTEMPTS


class DisplayMessage:
    """Classe pour gérer les messages d'affichage dans la console."""

    # -----------------------
    #   Display Messages Main_Controller
    # -----------------------
    @staticmethod
    def display_goodbye():
        """Affiche un message d'au revoir."""
        print("\nMerci d'avoir utilisé l'application !")

    # -----------------------
    #   Display Messages Player_Controller
    # -----------------------
    @staticmethod
    def display_input_nonempty(attempt, max_attempts=3):
        """Affiche un message demandant une saisie non vide avec tentative."""
        print(
            f"\n🔴  Ce champ est obligatoire. "
            f"({attempt}/{max_attempts}). Réessayez.\n"
        )

    @staticmethod
    def display_abort_operation():
        """Affiche un message d'abandon de l'opération."""
        print("❌ Nombre de tentatives dépassé. Opération abandonnée.")

    @staticmethod
    def display_input_date(attempt, max_attempts=3):
        """Affiche un message demandant une saisie de date valide avec tentative."""
        print(
            f"\n🔴  La date doit être au format 31/07/2025. "
            f"({attempt}/{max_attempts}). Réessayez.\n"
        )

    @staticmethod
    def display_not_player():
        """Affiche un message indiquant qu'aucun joueur n'a été trouvé."""
        print("🔍 Aucun joueur disponible.")

    @staticmethod
    def display_not_isdigit():
        """Affiche un message indiquant que l'entrée doit être un nombre."""
        print("🔴  L'entrée doit être un nombre. ")

    @staticmethod
    def display_out_of_range():
        """Affiche un message indiquant que le choix est hors de portée."""
        print("🔴  Choix hors plage. Veuillez réessayer.")

    @staticmethod
    def display_create_title():
        """Affiche le titre pour la création d'un joueur."""
        print("\n👤  Création d'un nouveau joueur :\n")

    @staticmethod
    def display_not_re_match(attempt, max_attempts=3):
        """Affiche un message indiquant que l'entrée ne correspond pas au format requis."""
        print(
            f"\n🔴  L'entrée doit correspondre au format requis. "
            f"({attempt}/{max_attempts}). Réessayez.\n"
        )

    @staticmethod
    def display_already_exists(attempt, max_attempts=3):
        """Affiche un message indiquant que l'entrée existe déjà."""
        print(
            f"\n🔴  L'entrée existe déjà. " f"({attempt}/{max_attempts}). Réessayez.\n"
        )

    @staticmethod
    def display_player_created():
        """Affiche un message de confirmation de création d'un joueur."""
        print("\n✅  Joueur créé avec succès !\n")

    @staticmethod
    def display_player_info_title():
        """Affiche le titre pour les informations d'un joueur."""
        print("\n👤  Informations sur le joueur :\n")

    @staticmethod
    def display_player_info(player):
        """Affiche les informations d'un joueur."""
        print(f"Nom               : {player.last_name}")
        print(f"Prénom            : {player.first_name}")
        print(f"Date de naissance : {player.birth_date}")
        print(f"Identifiant       : {player.national_id}")

    # -----------------------
    #   MODIFICATION JOUEUR
    # -----------------------
    @staticmethod
    def display_update_player_title():
        """Affiche le titre pour la mise à jour d'un joueur."""
        print("\n🔄  Mise à jour des informations du joueur :\n")

    @staticmethod
    def display_player_not_updated():
        """Affiche un message indiquant que le joueur n'a pas été mis à jour."""
        print("\n❌  Aucune modification apportée au joueur.\n")

    @staticmethod
    def display_current_player_info(label="actuelles"):
        """Affiche les informations actuelles d'un joueur."""
        print(f"\n🔍  Informations {label} du joueur :\n")

    @staticmethod
    def display_player_info_details(player):
        """Affiche les détails d'un joueur."""
        print(f"Nom               : {player.last_name}")
        print(f"Prénom            : {player.first_name}")
        print(f"Date de naissance : {player.birth_date}")
        print(f"Identifiant       : {player.national_id}\n")

    @staticmethod
    def display_consigne():
        """Affiche une consigne pour l'utilisateur."""
        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

    @staticmethod
    def display_error_format_date():
        """Affiche un message d'erreur pour un format de date invalide."""
        print("🔴  ❌ Format invalide. Exemple : 31/12/1990")

    @staticmethod
    def display_player_updated():
        """Affiche un message de confirmation de mise à jour d'un joueur."""
        print("\n✅  Joueur mis à jour avec succès !\n")

    @staticmethod
    def display_player_new_info_title():
        """Affiche un titre pour les nouvelles informations d'un joueur."""
        print("\n🔄  Nouvelles informations du joueur :\n")

    @staticmethod
    def display_player_new_info_details(player):
        """Affiche les nouvelles informations d'un joueur."""
        print(f"Nom               : {player.last_name}")
        print(f"Prénom            : {player.first_name}")
        print(f"Date de naissance : {player.birth_date}")
        print(f"Identifiant       : {player.national_id}\n")

    # -----------------------
    #   SUPPRESSION JOUEUR
    # -----------------------
    @staticmethod
    def display_delete_player_title():
        """Affiche le titre pour la suppression d'un joueur."""
        print("\n🗑️  Suppression d'un joueur :\n")

    @staticmethod
    def display_player_deleted(player):
        """Affiche un message de confirmation de suppression d'un joueur."""
        print(
            f"\n✅  {player.first_name} {player.last_name} a été supprimé avec succès.\n"
        )

    @staticmethod
    def display_player_not_deleted():
        """Affiche un message indiquant que la suppression du joueur a été annulée."""
        print("❌  Suppression annulée.\n")

    # -----------------------
    #   RECHERCHE
    # -----------------------
    @staticmethod
    def display_search_title():
        """Affiche le titre pour la recherche d'un joueur."""
        print("\n🔍  Recherche d'un joueur :\n")

    @staticmethod
    def display_player_not_found():
        """Affiche un message indiquant qu'aucun joueur n'a été trouvé."""
        print("❌  Aucun joueur trouvé.\n")

    # -----------------------
    #   LISTER JOUEUR
    # -----------------------
    @staticmethod
    def display_no_players_found():
        """Affiche un message indiquant qu'aucun joueur n'a été trouvé."""
        print("\n🔍  Aucun joueur enregistré.\n")
        print("⚠️  Veuillez d'abord créer des joueurs (1. Créer un joueur).\n")

    # -----------------------
    #   SÉLECTION D'UN TOURNOI
    # -----------------------
    @staticmethod
    def display_tournament_not_saved():
        """Affiche un message indiquant que le tournoi n'a pas été enregistré."""
        print("\n🔍 Aucun tournoi enregistré pour le moment.")
        print("⚠️  Créez-en un pour commencer (Menu Tournois -> 1. Créer un tournoi)\n")

    # -----------------------
    #   CHARGEMENT DES TOURNOIS
    # -----------------------
    @staticmethod
    def display_load_tournament_failed(file_name):
        """Affiche un message indiquant que le rechargement des tournois a échoué."""
        print("\n❌ Échec du rechargement des tournois.")
        print(f"⚠️  Veuillez vérifier le fichier de données : {file_name}\n")

    # -----------------------
    #   CRÉATION TOURNOI
    # -----------------------
    @staticmethod
    def display_create_tournament_title():
        """Affiche le titre pour la création d'un tournoi."""
        print("\n=== 🏆  Création d'un nouveau tournoi ===:\n")

    @staticmethod
    def display_error_tournament_date(attempt, max_attempts):
        """Affiche un message d'erreur pour une date de tournoi invalide."""
        print(
            f"\n❌ La date de fin doit être ≥ date de début ({attempt}/{max_attempts}).\n"
        )

    @staticmethod
    def display_tournament_rounds():
        """Affiche un message demandant le nombre de tours pour un tournoi."""
        print(
            "\nℹ️  Veuillez saisir le nombre de tours pour le tournoi ou laissez vide pour 4.\n"
        )

    @staticmethod
    def display_tournament_created_message():
        """Affiche un message de confirmation de création d'un tournoi."""
        print("\n✅  Tournoi créé avec succès !\n")

    @staticmethod
    def display_tournament_info_details(tournament):
        """Affiche les détails d'un tournoi."""
        print("--- Informations du tournoi créé ---\n")
        print(f"Nom du tournoi       : {tournament.name}")
        print(f"Lieu du tournoi      : {tournament.place}")
        print(f"Date de début        : {tournament.start_date} → {tournament.end_date}")
        print(f"Description          : {tournament.description}\n")
        print(f"Nombre de tours      : {tournament.total_rounds}")

    # -----------------------
    #   MODIFICATION TOURNOI
    # -----------------------
    @staticmethod
    def display_update_tournament_title():
        """Affiche le titre pour la mise à jour d'un tournoi."""
        print("\n--- 🔄  Mise à jour des informations du tournoi ---\n")

    @staticmethod
    def display_current_tournament_info(label="actuelles"):
        """Affiche les informations actuelles d'un tournoi."""
        print(f"\n🔍  Informations {label} du tournoi :\n")

    @staticmethod
    def display_tournament_updated_details(tournament):
        """Affiche les détails mis à jour d'un tournoi."""
        print(f"Nom du tournoi       : {tournament.name}")
        print(f"Lieu du tournoi      : {tournament.place}")
        print(f"Date de début        : {tournament.start_date} → {tournament.end_date}")
        print(f"Description          : {tournament.description}")
        print(f"Nombre de tours      : {tournament.total_rounds}")

    @staticmethod
    def display_tournament_consigne():
        """Affiche une consigne pour la mise à jour d'un tournoi."""
        print("\nℹ️  Laisser vide pour conserver la valeur actuelle.\n")

    @staticmethod
    def display_tournament_end_date_error():
        """Affiche un message d'erreur pour une date de fin de tournoi invalide."""
        print("🔴  ❌ La date de fin doit être ≥ date de début. Veuillez réessayer.")

    @staticmethod
    def display_tournament_update_rounds():
        """Affiche un message demandant le nombre de tours pour la mise à jour d'un tournoi."""
        print(
            "\nℹ️  Veuillez saisir le nombre de tours du "
            "tournoi ou laissez vide pour conserver l'ancien.\n"
        )

    @staticmethod
    def display_tournament_updated_message():
        """Affiche un message de confirmation de mise à jour d'un tournoi."""
        print("\n✅  Tournoi mis à jour avec succès !\n")

    @staticmethod
    def display_tournament_updated_info(tournament):
        """Affiche les informations mises à jour d'un tournoi."""
        print("--- Nouvelles infos du tournoi ---\n")
        print(f"Nom du tournoi       : {tournament.name}")
        print(f"Lieu du tournoi      : {tournament.place}")
        print(f"Date de début        : {tournament.start_date} → {tournament.end_date}")
        print(f"Description          : {tournament.description}")
        print(f"Nombre de tours      : {tournament.total_rounds}\n")

    # -----------------------
    #   SUPPRESSION TOURNOI
    # -----------------------
    @staticmethod
    def display_delete_tournament_title():
        """Affiche le titre pour la suppression d'un tournoi."""
        print("\n--- 🗑️  Suppression d'un tournoi ---\n")

    @staticmethod
    def display_tournament_deleted(tournament):
        """Affiche un message de confirmation de suppression d'un tournoi."""
        print(f"\n✅  Le tournoi '{tournament.name}' a été supprimé avec succès.\n")

    # -----------------------
    #   GESTION DES JOUEURS
    # -----------------------
    @staticmethod
    def display_manage_players_title():
        """Affiche le titre pour la gestion des joueurs d'un tournoi."""
        print("\n--- 👥  Gestion des joueurs d'un tournoi ---")

    @staticmethod
    def display_tournament_title():
        """Affiche le titre visuel du tournoi."""
        print("\n--- 🏆  Informations du tournoi ---\n")

    @staticmethod
    def display_tournament_info(tournament):
        """Affiche les informations détaillées d'un tournoi."""
        print(f"Nom                : {tournament.name}")
        print(f"Lieu               : {tournament.place}")
        print(f"Dates              : {tournament.start_date} → {tournament.end_date}")
        print(f"Description        : {tournament.description}")
        print(f"Nombre de tours    : {tournament.total_rounds}")
        print(f"Joueurs inscrits   : {len(tournament.players)}\n")

    @staticmethod
    def display_manage_players_menu():
        """Affiche le menu de gestion des joueurs d'un tournoi."""
        print("--- 👥  Menu de gestion des joueurs ---")
        print("1. Ajouter  joueur(s)")
        print("2. Retirer  joueur(s)")
        print("0. Retour\n")

    # -----------------------
    #   AJOUTER JOUEUR(S)
    # -----------------------
    @staticmethod
    def display_player_available(available):
        """Affiche un message indiquant les joueurs disponibles pour l'ajout."""
        print("\n--- 👥  Joueurs disponibles à l'ajout ---")
        for i, p in enumerate(available, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    @staticmethod
    def display_player_duplicate_warning(token):
        """Affiche un avertissement pour un numéro de joueur dupliqué."""
        print(f"⚠️  Numéro {token} dupliqué, ignoré.")

    @staticmethod
    def display_player_not_added(token):
        """Affiche un avertissement pour un numéro de joueur non valide."""
        print(f"⚠️  Le numéro {token} n'est pas valide.")

    @staticmethod
    def display_player_added(added):
        """Affiche un message de confirmation d'ajout d'un joueur."""
        print("\n👤 Joueur(s) ajouté(s) :")
        for p in added:
            print(f"- {p.last_name} {p.first_name} [{p.national_id}]")

    @staticmethod
    def display_player_not_added_players():
        """Affiche un message indiquant qu'aucun joueur n'a été ajouté."""
        print("\n👤 Aucun nouveau joueur ajouté.")

    # -----------------------
    #   RETIRER JOUEUR(S)
    # -----------------------
    @staticmethod
    def display_no_players_in_tournament():
        """Affiche un message indiquant qu'il n'y a pas de joueurs dans le tournoi."""
        print("\n🔍 Aucun joueur inscrit dans ce tournoi.")

    @staticmethod
    def display_no_valid_number():
        """Affiche un message indiquant qu'aucun numéro valide n'a été saisi."""
        print("\n🔴  Aucun numéro valide saisi. Veuillez réessayer.")

    @staticmethod
    def display_registered_players_list(tournament):
        """Affiche le titre pour la liste des joueurs inscrits."""
        print("\n--- Joueurs inscrits ---")
        for i, p in enumerate(tournament.players, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    @staticmethod
    def display_finalize_player_removal(removed):
        """Affiche un message de confirmation de la suppression des joueurs."""
        print("\n👤 Joueur(s) retiré(s) :")
        for p in removed:
            print(f"- {p.last_name} {p.first_name} [{p.national_id}]")

    @staticmethod
    def display_player_not_removed():
        """Affiche un message indiquant qu'aucun joueur n'a été retiré."""
        print("\n👤 Aucun joueur retiré.")

    @staticmethod
    def display_registered_players_title(players, title):
        """Affiche le titre pour la liste des joueurs inscrits dans un tournoi."""
        print(f"\n--- {title} ---")
        for i, p in enumerate(players, 1):
            print(
                f"{i}. {p.last_name} {p.first_name} | {p.national_id} | {p.birth_date}"
            )

    # -----------------------
    #   CLASSEMENT / RAPPORTS / EXPORTS
    # -----------------------
    @staticmethod
    def display_leaderboard_not_eligible():
        """Affiche un message indiquant qu'aucun tournoi n'est éligible pour le classement."""
        print("\n🔍 Aucun tournoi démarré ou terminé pour le moment.")
        print("💡 Démarrez un tournoi pour pouvoir consulter son classement.\n")

    @staticmethod
    def display_no_players_registered():
        """Affiche un message indiquant qu'aucun joueur n'est inscrit dans le tournoi."""
        print("\nAucun joueur n'est inscrit à un tournoi.\n")

    @staticmethod
    def display_players_tournament_title():
        """Affiche le titre pour la liste des joueurs d'un tournoi."""
        print("\n--- Joueurs inscrits à un tournoi ---")

    @staticmethod
    def display_tournament_selected_title():
        """Affiche le titre pour le tournoi sélectionné."""
        print("\n=== Détails du tournoi sélectionné ===\n")

    @staticmethod
    def display_tournament_details_report(tournament):
        """Affiche les détails du tournoi pour le rapport."""
        print(f"Nom du tournoi       : {tournament.name}")
        print(f"Lieu du tournoi      : {tournament.place}")
        print(f"Dates                : {tournament.start_date} → {tournament.end_date}")
        print(f"Description          : {tournament.description}")
        print(f"Nombre de tours      : {tournament.total_rounds}")
        print(f"Joueurs inscrits     : {len(tournament.players)}")
        print(f"Statut du tournoi    : {tournament.status}\n")

    @staticmethod
    def display_tournament_players_title_report(tournament):
        """Affiche le titre pour le tournoi sélectionné."""
        print(f"\n=== Détails des joueurs du tournoi : {tournament.name} ===")

    @staticmethod
    def display_no_rounds_available():
        """Affiche un message indiquant qu'aucun round n'est disponible."""
        print("Aucun round disponible.")

    @staticmethod
    def display_round_details(idx):
        """Affiche les détails d'un round."""
        print(f"\n🥊 Round {idx} :")

    @staticmethod
    def display_match_details(rnd):
        """Affiche les détails d'un match."""
        for m in rnd.matches:
            p1, p2 = m.players
            s1, s2 = m.scores
            print(
                f"{p1.last_name} {p1.first_name}[{p1.national_id}] "
                f"{s1} - {s2} {p2.last_name} {p2.first_name}[{p2.national_id}]\n"
            )

    @staticmethod
    def display_export_success(path):
        """Affiche un message de succès pour l'exportation."""
        print(f"✓ Exporté dans : {path.resolve()}")

    # -----------------------
    #   DEMARRAGE TOURNOI
    # -----------------------
    @staticmethod
    def display_start_tournament_title():
        """Affiche le titre pour le démarrage d'un tournoi."""
        print("\n--- 🏁  Démarrage d'un tournoi ---")

    @staticmethod
    def display_tournament_not_started():
        """Affiche un message indiquant que le tournoi n'a pas été démarré."""
        print("\n🔍 Aucun tournoi non démarré trouvé.")
        print("⚠️  Créez-en un pour commencer (Menu Tournois -> 1. Créer un tournoi)\n")

    @staticmethod
    def display_tournament_option_7():
        """Affiche un message pour l'option 7 du menu des tournois."""
        print(
            "\n💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round."
        )

    @staticmethod
    def display_message_check_players_in_tournament(tournament):
        """Affiche un message pour vérifier les joueurs dans un tournoi."""
        print(
            f"\n❌ Aucun joueur inscrit pour le tournoi '{tournament.name}' "
            "(5. Ajouter/Retirer joueurs)."
        )

    @staticmethod
    def display_message_check_even_number_of_players():
        """Affiche un message pour vérifier le nombre de joueurs."""
        print("\n❌ Il faut un nombre pair de joueurs (au moins 2).")

    @staticmethod
    def display_message_check_finished_tournament(tournament):
        """Affiche un message pour vérifier si le tournoi est terminé."""
        print(f"❌ Impossible : le tournoi '{tournament.name}' est déjà terminé.")

    @staticmethod
    def display_check_tournament_status(tournament):
        """Vérifie le statut du tournoi."""
        print(f"\nℹ️  Statut du tournoi '{tournament.name}' : {tournament.status}.")
        print("💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores du round.")

    @staticmethod
    def display_start_tournament_success(tournament, count):
        """Affiche un message de succès pour le démarrage d'un tournoi."""
        print(f"\n🏁 Tournoi '{tournament.name}' démarré.\n")
        print(f"Joueurs inscrits : {count}")
        print(f"Nombre de rounds : {tournament.total_rounds}\n")

    @staticmethod
    def display_round_matches(rnd):
        """Affiche chaque match avec les deux joueurs."""
        for m in rnd.matches:
            p1, p2 = m.players
            print(
                f"{p1.last_name} {p1.first_name} [{p1.national_id}] VS "
                f"{p2.last_name} {p2.first_name} [{p2.national_id}]"
            )

    @staticmethod
    def display_start_next_round_title():
        """Affiche le titre pour le démarrage du round suivant."""
        print("\n--- Démarrage du round suivant ---")

    @staticmethod
    def display_no_tournament_in_progress():
        """Affiche un message si aucun tournoi n'est en cours."""
        print("\n🔍 Aucun tournoi en cours pour le moment.")
        print("💡 Utilisez l'option 6 (Menu Tournois -> 6. Démarrer un tournoi).\n")

    @staticmethod
    def display_round_in_progress():
        """Affiche un message si un round est en cours."""
        print("\n⚠️  Il faut clôturer le round en cours avant d'en démarrer un nouveau.")
        print("💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores.")

    @staticmethod
    def display_next_round_started():
        """Affiche un message de succès pour le démarrage du round suivant."""
        print("🏁 Nouveau round démarré.\n")
        print("💡 Utilisez l'option 7 du menu Tournoi pour saisir les scores.")

    @staticmethod
    def display_score_input_title():
        """Affiche le titre pour la saisie des scores."""
        print("\n--- Saisie des scores du round en cours ---")

    @staticmethod
    def display_end_tournament_message(tournament, winner):
        """Affiche un message de fin de tournoi avec les détails."""
        print(f"\n🏆 Tournoi « {tournament.name} » terminé !\n")
        print(f"📍 Lieu : {tournament.place}")
        print(f"📅 Du {tournament.start_date} au {tournament.end_date}")
        print(f"👥 Participants : {len(tournament.players)}\n")
        print(f"🎖 Gagnant : {winner.last_name} {winner.first_name}")

    @staticmethod
    def display_no_tournament_started_message():
        """Affiche un message si aucun tournoi n'a été démarré."""
        print("\n❌ Impossible : Le tournoi n'a pas encore démarré.")
        print("💡 Utilisez l'option 6 du menu Tournoi pour démarrer le tournoi.")

    @staticmethod
    def display_tournament_already_finished(tournament):
        """Affiche un message si le tournoi est déjà terminé."""
        print(f"\nℹ️  Le tournoi '{tournament.name}' est déjà terminé.")

    @staticmethod
    def display_round_already_played():
        """Affiche un message si le round a déjà été joué."""
        print("\n🥊 Round déjà joué.")
        print("💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant.")

    @staticmethod
    def display_round_recap(num, rnd):
        """Affiche le récapitulatif d'un round."""
        print(f"\n--- Récapitulatif du round {num} ---")
        for m in rnd.matches:
            p1, p2 = m.players
            s1, s2 = m.scores
            print(
                f"{p1.last_name} {p1.first_name} {s1} - {s2} {p2.last_name} {p2.first_name}"
            )

    @staticmethod
    def display_tournament_consigne_title(tournament_name, num):
        """Affiche le titre et les instructions de saisie."""
        print(f"\n===== Score du tournoi {tournament_name} =====")
        print("📌 Rappel : format 1-0, 0-1, 0.5-0.5 (1 victoire, 0 défaite, 0.5 nul)")
        print(f"\n🥊 Round {num}\n")

    @staticmethod
    def display_tournament_scores_example():
        """Affiche un exemple de saisie valide pour les scores."""
        print("❌ Exemple valide : 1-0, 0-1 ou 0.5-0.5")

    @staticmethod
    def display_round_recap_summary(num, recap):
        """Affiche le récapitulatif des scores d'un round."""
        print(f"\n--- Récapitulatif du round {num} ---")

        # 2️⃣ Parcourt la liste recap et affiche chaque score
        for p1, p2, a, b in recap:
            print(
                f"{p1.last_name} {p1.first_name} {a} - {b} "
                f"{p2.last_name} {p2.first_name}"
            )

    @staticmethod
    def display_scores_saved_message():
        """Affiche un message de confirmation de l'enregistrement des scores."""
        print("\n💾 Scores enregistrés.")
        print("💡 Utilisez l'option 8 du menu Tournoi pour démarrer le round suivant.")

    @staticmethod
    def display_last_scores_saved():
        """Affiche un message de confirmation des derniers scores enregistrés."""
        print("\n✅ Derniers scores enregistrés. Le tournoi est maintenant terminé.\n")
