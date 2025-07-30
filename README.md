# Tournois Club Échecs

Bienvenue dans **Tournois Club Échecs**, une application Python interactive pour gérer les joueurs et les tournois d’échecs dans un club.

---

## 🎯 Objectifs du projet

- Gérer facilement les **joueurs**, **tournois** et **rounds** depuis un terminal.
- Fournir une architecture claire : contrôleurs, modèles et vues.
- Assurer une qualité de code constante grâce à **Flake8**.

---

## 📂 Structure du projet

```
tournois_club_echecs/
├── README.md
├── main.py                       # Point d’entrée
├── requirements.txt              # Dépendances Python
├── .flake8                       # Configuration Flake8
├── controllers/                  # Logique métier
│   ├── main_controller.py
│   ├── player_controller.py
│   ├── tournament_management.py
│   ├── tournament_players.py
│   ├── tournament_rounds.py
│   ├── tournament_reports.py
│   ├── tournament_controller_base.py
│   └── __init__.py
├── models/                       # Entités : Player, Tournament, Round, Match
├── views/                        # Affichage en console
└── data/
    └── tournaments/              # Données JSON des tournois
```

---

## 🚀 Prérequis

- **Python 3.10+**
- Un terminal (PowerShell, Bash, …)
- (Optionnel) Environnement virtuel Python recommandé

---

## 🛠 Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/Freddy0ne1/tournois_club_echecs
   cd tournois_club_echecs
   ```

2. **Créer et activer un environnement virtuel (recommandé)**

   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Lancer l’application

Exécute depuis la racine :

```bash
python main.py
```

Le menu principal s’affiche :

```
=== Menu Principal ===

1. Paramètres joueurs
2. Paramètres tournoi
3. Rapports
4. Quitter
```

---

## 🧭 Exemples rapides

### Créer un joueur

- Menu principal → 1 → "Créer joueur"
- Suivre les instructions (nom, prénom, date de naissance, identifiant).

### Créer un tournoi

- Menu principal → 2 → "Créer un tournoi"
- Remplir les informations demandées.

Les fichiers sont sauvegardés automatiquement dans `data/tournaments/`.

---

## 🧹 Vérification du code avec Flake8

### 1. Lancer une vérification simple

```bash
flake8
```

### 2. Vérifier uniquement le dossier controllers

```bash
flake8 controllers/
```

### 3. Générer un rapport HTML Flake8

```bash
flake8 --format=html --htmldir=flake8-report
```

Ensuite, ouvre `flake8-report/index.html` dans un navigateur.

---

## ✨ Qualité du code

Le fichier `.flake8` fixe les règles (max-line-length : 119) pour assurer une cohérence.
Exécute régulièrement Flake8 pour garder le projet propre.

---

Bonne gestion de vos tournois ! ♟🚀
