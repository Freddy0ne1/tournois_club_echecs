# Logiciel de Gestion de Tournois d'Échecs (CLI hors‑ligne)

> Projet Python MVC pour gérer des tournois d'échecs **sans connexion Internet**, avec stockage **JSON**, menus en ligne de commande, synchronisation des joueurs, rapports et **export CSV**.

---

## 📌 Sommaire

- [Objectif du projet](#objectif-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Modèles de données](#modèles-de-données)
- [Installation](#installation)
- [Lancement](#lancement)
- [Menus & Flux d’utilisation](#menus--flux-dutilisation)
  - [Paramètres joueur](#paramètres-joueur)
  - [Paramètres tournoi](#paramètres-tournoi)
  - [Rapports & Export CSV](#rapports--export-csv)
- [Formats & Règles métier](#formats--règles-métier)
- [Sauvegarde / Fichiers de données](#sauvegarde--fichiers-de-données)
- [Exporter en CSV](#exporter-en-csv)
- [Qualité du code (PEP8, flake8-html)](#qualité-du-code-pep8-flake8-html)
- [Structure recommandée du dépôt](#structure-recommandée-du-dépôt)
- [Feuille de route](#feuille-de-route)
- [Licence](#licence)

---

## Objectif du projet

Le club d’échecs souhaitait un outil simple, portable et **off‑line** pour organiser des tournois : création des joueurs, inscriptions, appariements, saisie des scores, suivi des rounds, consultation des résultats et export des données.  
Ce projet sert aussi de **support pédagogique** pour pratiquer la Programmation Orientée Objet (POO), l’architecture **MVC**, la persistance JSON et les bonnes pratiques Python.

---

## Fonctionnalités

✅ Créer / lister / modifier / supprimer des **joueurs**.  
✅ Validation d’ID joueur (`AB` + 5 chiffres).  
✅ Validation format date (JJ/MM/AAAA).  
✅ Synchronisation des données joueur dans les tournois existants (ID, nom, etc.) sans perdre les scores.  
✅ Créer / lister / modifier / supprimer des **tournois**.  
✅ Ajouter des joueurs à un tournoi (nombre pair requis).  
✅ Démarrer un tournoi → génération automatique du Round 1 (appariements aléatoires).  
✅ Saisie manuelle des scores (pas de génération automatique).  
✅ Avancement des rounds & génération de la ronde suivante (RoundController).  
✅ Rapports consultables en CLI (joueurs, tournois, rounds, etc.).  
✅ **Export CSV** d’un tournoi sélectionné (infos, joueurs, rounds & matchs).  
✅ Fonctionne **hors connexion**.

---

## Architecture

Le projet suit une structure inspirée MVC :

- **models/** : définitions des entités (Player, Tournament, Round, Match, …).
- **controllers/** : logique applicative + interactions utilisateur par menus (console).
- **views/** : fonctions d’affichage (optionnel, certains écrans sont imprimés directement par les contrôleurs).
- **services/** : utilitaires transverses (stockage JSON, export CSV, etc.).
- **data/** : fichiers de persistance (`players.json`, `tournaments.json`).

---

## Modèles de données

### Player

| Champ         | Type              | Description                                               |
| ------------- | ----------------- | --------------------------------------------------------- |
| `id_national` | str               | Identifiant unique format **AB#####**.                    |
| `last_name`   | str               | Nom.                                                      |
| `first_name`  | str               | Prénom.                                                   |
| `birth_date`  | str (JJ/MM/AAAA)  | Date de naissance.                                        |
| `score`       | float (optionnel) | Score courant dans un tournoi (géré côté tournoi/matchs). |

### Tournament

| Champ          | Type             | Description                         |
| -------------- | ---------------- | ----------------------------------- |
| `name`         | str              | Nom du tournoi.                     |
| `location`     | str              | Lieu.                               |
| `start_date`   | str (JJ/MM/AAAA) | Début.                              |
| `end_date`     | str (JJ/MM/AAAA) | Fin.                                |
| `description`  | str              | Notes libres.                       |
| `rounds_total` | int              | Nombre de rounds prévus (défaut 4). |
| `players`      | List[Player]     | Joueurs inscrits.                   |
| `rounds`       | List[Round]      | Rounds effectivement joués.         |

### Round

| Champ        | Type             | Description                   |
| ------------ | ---------------- | ----------------------------- |
| `name`       | str              | Nom du round (ex: "Round 1"). |
| `start_time` | datetime         | Date/heure début.             |
| `end_time`   | datetime \| None | Fin quand round terminé.      |
| `matches`    | List[Match]      | Matchs du round.              |

### Match

| Champ        | Type          | Description                 |
| ------------ | ------------- | --------------------------- |
| `player1_id` | str           | ID joueur 1.                |
| `player2_id` | str           | ID joueur 2.                |
| `score1`     | float \| None | Score joueur 1 (0, 0.5, 1). |
| `score2`     | float \| None | Score joueur 2.             |

---

## Installation

### Prérequis

- Python **3.10+** (recommandé 3.11).
- Accès en écriture au répertoire (pour les fichiers JSON et exports).

### Étapes

```bash

python -m venv env
source env/bin/activate  # Windows: env/Scripts/activate
pip install -r requirements.txt
```

> `re` (regex) est un module standard ⇒ **ne pas** l’ajouter à `requirements.txt`.

---

## Lancement

```bash
python main.py
```

---

## Menus & Flux d’utilisation

### Paramètres joueur

```
1. Créer un joueur
2. Lister les joueurs
3. Modifier un joueur
4. Supprimer un joueur
0. Retour
```

- Validation ID : `AB` + 5 chiffres (ex: AB01234).
- Date naissance contrôlée (JJ/MM/AAAA, boucle jusqu’à saisie valide).
- Modification synchronisée dans les tournois déjà existants (IDs & noms mis à jour).

---

### Paramètres tournoi

```
1. Créer un tournoi
2. Lister les tournois
3. Modifier un tournoi
4. Supprimer un tournoi
5. Démarrer un tournoi
6. Saisir les scores du round cours
7. Démarrer le round suivant
8. Afficher le classement
9. Rapports / Export CSV tournoi
0. Retour
```

---

### Rapports & Export CSV

Sous‑menu Rapports :

```
1. Joueurs inscrits (tous tournois) A->Z
2. Joueurs d'un tournoi (sélection) A->Z
3. Tous les tournois (en cours & terminés)
4. Nom et dates d’un tournoi
5. Tous les tours & matchs d’un tournoi
6. Exporter en CSV (tournoi choisi)
0. Retour
```

---

## Sauvegarde / Fichiers de données

Par défaut :

```
data/
├─ players.json
└─ tournaments.json
```

Chaque opération **CRUD** met à jour immédiatement les fichiers.  
Copie ces fichiers pour archivage ou transfert (hors‑ligne).

---

## Exporter en CSV

### Où ?

Menu : **Paramètres tournoi → 9 (Rapports) → 6 (Exporter en CSV)**.

### Ce que ça fait

1. Tu choisis un tournoi.
2. Le contrôleur appelle le service : `services/export_csv_service.export_tournament_csv()`.
3. Un dossier est créé : `exports/<nom-tournoi-normalisé>_<horodatage>/`.
4. Trois fichiers CSV sont générés :

| Fichier                         | Contenu                                         |
| ------------------------------- | ----------------------------------------------- |
| `tournament_info.csv`           | Meta données du tournoi.                        |
| `tournament_players.csv`        | Joueurs du tournoi + scores.                    |
| `tournament_rounds_matches.csv` | Tous les rounds + matchs + scores + timestamps. |

---

## Qualité du code (PEP8, flake8-html)

Le projet vise un code propre et pédagogique.

### Vérifier avec flake8

```bash
flake8 .
```

### Rapport HTML

Fichier `.flake8` ou `setup.cfg` :

```ini
[flake8]
format = html
htmldir = flake-report
max-line-length = 88
extend-ignore = E203,W503
```

Puis :

```bash
flake8 .
open flake-report/index.html  # selon OS
```

---

## Structure recommandée du dépôt

```
chess_tournament_cli/
├─ main.py
├─ requirements.txt
├─ README.md
├─ data/
│  ├─ players.json
│  └─ tournaments.json
├─ models/
│  ├─ __init__.py
│  ├─ player.py
│  ├─ tournament.py
│  ├─ round.py
│  └─ match.py
├─ services/
│  ├─ __init__.py
│  ├─ storage_service.py
│  └─ export_csv_service.py
└─ controllers/
   ├─ __init__.py
   ├─ menu_controller.py
   ├─ player_controller.py
   ├─ tournament_controller.py
   └─ round_controller.py
```

---

**Dernière mise à jour : 2025-07-16**

Bons tournois ! ♟️🔥
