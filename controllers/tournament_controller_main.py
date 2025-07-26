"""
Module tournament_controller_main
Point d'entrée principal pour le contrôleur des tournois.

Ce fichier rassemble toutes les fonctionnalités provenant
des différents sous-contrôleurs (création, modification, listing, etc.)
en une seule classe `TournamentController`.
"""

# Importation des sous-contrôleurs
from .tournament_creation import TournamentController as CreationController
from .tournament_modification import TournamentController as ModificationController
from .tournament_listing import TournamentController as ListingController
from .tournament_reports import TournamentController as ReportsController
from .tournament_utils import TournamentController as UtilsController
from .tournament_next_round import TournamentController as RoundController
from .tournament_delete import TournamentController as DeleteController
from .tournament_players import TournamentController as ManagePlayerController
from .tournament_start import TournamentController as StartController
from .tournament_scores import TournamentController as ScoresController


class TournamentController(
    CreationController,
    ModificationController,
    ListingController,
    ReportsController,
    UtilsController,
    RoundController,
    DeleteController,
    ManagePlayerController,
    StartController,
    ScoresController,
):
    """
    Contrôleur principal complet pour les tournois.
    Hérite de tous les sous-contrôleurs et regroupe l'ensemble
    des fonctionnalités de gestion :
      - Création
      - Modification
      - Listing
      - Rapports et classements
      - Outils et utilitaires
    """
