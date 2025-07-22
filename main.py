"""Point d'entrée du programme.
On initialise le contrôleur principal puis on lance la boucle CLI.
"""

from controllers.main_controller import MainController

if __name__ == "__main__":
    MainController().run()
