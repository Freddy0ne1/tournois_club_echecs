"""main.py
Point d'entrée du programme.
"""

from controllers.menu_controller import MenuController
from views.menu_view import welcome


def main():
    """Point d'entrée du programme."""

    welcome()
    MenuController().run()


if __name__ == "__main__":
    main()
