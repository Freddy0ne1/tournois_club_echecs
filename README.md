# Échecs_Tournois

Bienvenue dans **Échecs_Tournois**, une application Python simple et interactive pour gérer des tournois d’échecs. Cette application vous guide pas à pas, de la création de joueurs à l’organisation complète de tournois.

---

## 🎯 Objectifs du projet

- Offrir une interface en ligne de commande claire et intuitive.
- Simplifier la gestion des **joueurs**, des **rounds** et des **tournois**.
- Faciliter la contribution grâce à une structure de projet lisible.

---

## 📂 Structure du projet

```
Échecs_Tournois/
├── README.md                  # Documentation (toi qui la lis !)
├── main.py                    # Point d’entrée de l’application
├── requirements.txt           # Dépendances Python nécessaires
├── setup.cfg                  # Configuration pour les tools (Lint, etc.)
├── controllers/               # Logique métier (contrôleurs)
│   ├── main_controller.py     # Orchestration principale (menus CLI)
│   ├── player_controller.py   # Gestion des joueurs
│   └── tournament_controller.py # Gestion des tournois
├── models/                    # Définition des entités métier
│   ├── player.py              # Classe Player
│   ├── round.py               # Classe Round
│   ├── match.py               # Classe Match
│   └── tournament.py          # Classe Tournament
└── views/                     # Affichage dans la console
    └── console_view.py        # Fonctions d’affichage (menus, messages)
```

---

## 🚀 Prérequis

- **Python 3.8+** installé sur votre machine.
- Un terminal (PowerShell, Bash, cmd, etc.).
- (Facultatif) Un environnement virtuel Python pour isoler les dépendances.

---

## 🛠️ Installation pas à pas

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/Freddy0ne1/tournois_club_echecs
   cd echecs_tournois
   ```

2. **Créer un environnement virtuel** (fortement recommandé)

   ```bash
   python -m venv env
   # Windows
   source env/Scripts/activate
   # macOS / Linux
   source env/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Vérifier la structure**

   > Assurez-vous d’avoir bien ce dossier **`data/`**, qui sera créé automatiquement lors du premier lancement.

---

## ▶️ Lancer l’application

Dans votre terminal, exécutez :

```bash
python main.py
```

Vous verrez un menu principal s’afficher :

```
📁 Data dir : ./data
1. Créer un joueur
2. Lancer un tournoi
3. Quitter
Choix :
```

---

## 🧭 Tutoriel : Créer un joueur

Suivez ces étapes :

1. **Choisir l’option** `1` puis `Entrée`.
2. **Saisir le nom** du joueur quand le programme vous le demande.
3. **Valider** la date de naissance au format `jj-mm-aaaa`.
4. **Voir la confirmation** :

   ```
   ✅ Joueur créé.

   --- Informations du joueur ALICE Dupont ---

   Date de naissance : 28/03/1989
   ID : AB12568



   ```

5. Le fichier `data/players.json` se met automatiquement à jour.

---

## 🏆 Tutoriel : Lancer un tournoi

1. **Sélectionner l’option** `2` puis `Entrée`.
2. **Sélectionner les joueurs** disponibles (par numéro).
3. **Donner un nom** au tournoi (ex. `Tournoi du Club`).
4. **Choisir le nombre de tours** (généralement 4 ou 5).
5. **Valider** les paires de chaque round.
6. **Suivre** l’avancement des parties et saisir les résultats.
7. **Consulter** le classement final et les ronds joués.

Les données sont sauvegardées sous : `data/tournaments/<nom_tournoi>.json`.

---

Bonne gestion de tournois ! 🚀
