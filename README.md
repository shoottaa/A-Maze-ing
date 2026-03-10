*This project has been created as part of the 42 curriculum by egaudich, malanos.*

# A-Maze-Ing

## Description

A-Maze-Ing est un générateur et solveur de labyrinthes écrit en Python. Le programme lit un fichier de configuration, génère un labyrinthe via l'algorithme **Recursive Backtracker (DFS)**, le résout avec un **BFS**, puis affiche le résultat dans une fenêtre graphique pilotée par MiniLibX. Un motif "42" est intégré au centre de chaque labyrinthe en guise de signature visuelle.

**Fonctionnalités principales :**
- Génération de labyrinthe avec taille, points d'entrée/sortie et mode parfait/imparfait configurables
- Résolution automatique par BFS avec affichage animé du chemin
- Rendu graphique via MiniLibX (dessin pixel par pixel, sans framework GUI externe)
- Contrôles interactifs : régénération, affichage du chemin, changement de couleur des murs
- Écriture du labyrinthe et de la solution dans un fichier texte

## Instructions

### Installation

```bash
make install
```

Crée un environnement virtuel Python et installe toutes les dépendances.

### Lancement

```bash
make run
```

Ou manuellement :

```bash
make -C mlx_CLXV
.venv/bin/python a_maze_ing.py config.txt
```

Il est possible de passer n'importe quel fichier de config :

```bash
.venv/bin/python a_maze_ing.py mon_config.txt
```

### Contrôles clavier

| Touche | Action |
|--------|--------|
| `R` | Régénérer un nouveau labyrinthe |
| `P` | Afficher / masquer le chemin solution animé |
| `C` | Changer la couleur des murs |
| `ESC` | Quitter |

### Fichier de sortie

Le programme écrit le labyrinthe dans le fichier défini par `OUTPUT_FILE` selon le format suivant :
- Un chiffre hexadécimal par cellule par ligne (murs encodés en bitmask 4 bits : N=0x1, E=0x2, S=0x4, W=0x8)
- Une ligne vide
- Les coordonnées de l'entrée (`x,y`)
- Les coordonnées de la sortie (`x,y`)
- Le chemin solution sous forme d'une chaîne de directions cardinales (`N`, `S`, `E`, `W`)

### Lint / vérification de types

```bash
make lint
```

---

## Format du fichier de configuration

Le fichier de config utilise un format simple `CLÉ=VALEUR`. Les lignes commençant par `#` et les lignes vides sont ignorées.

| Clé | Type | Description |
|-----|------|-------------|
| `WIDTH` | `int > 0` | Nombre de colonnes du labyrinthe |
| `HEIGHT` | `int > 0` | Nombre de lignes du labyrinthe |
| `ENTRY` | `x,y` | Coordonnées de la cellule d'entrée (indexées à 0) |
| `EXIT` | `x,y` | Coordonnées de la cellule de sortie (indexées à 0) |
| `OUTPUT_FILE` | `string` | Chemin du fichier de sortie |
| `PERFECT` | `True`/`False` | Si `True`, génère un labyrinthe parfait (un seul chemin entre deux cellules quelconques). Si `False`, supprime ~10% de murs supplémentaires pour créer des boucles. |
| `SEED` | `int` *(optionnel)* | Graine aléatoire fixe pour des labyrinthes reproductibles. Si absent, une graine aléatoire est utilisée. |

**Exemple (`config.txt`) :**

```
WIDTH=40
HEIGHT=35
ENTRY=0,0
EXIT=35,4
OUTPUT_FILE=maze.txt
PERFECT=True
```

---

## Algorithme de génération

### Recursive Backtracker (DFS)

Le générateur utilise l'algorithme **Recursive Backtracker**, implémenté de façon itérative avec une pile explicite :

1. Partir de la cellule d'entrée et la marquer comme visitée.
2. Choisir aléatoirement un voisin non visité.
3. Supprimer le mur entre la cellule courante et ce voisin.
4. Se déplacer vers ce voisin et recommencer.
5. Si aucun voisin non visité n'existe, revenir en arrière sur la pile.
6. Recommencer jusqu'à ce que toutes les cellules accessibles soient visitées.

Avant le démarrage du DFS, le motif "42" est dessiné au centre du labyrinthe : ces cellules sont traitées comme des obstacles solides et exclues du parcours DFS.

Si `PERFECT=False`, environ 10% des murs restants sont supprimés aléatoirement après la génération pour introduire des boucles et des chemins multiples.

### Pourquoi cet algorithme ?

Le Recursive Backtracker a été choisi parce que :
- Il produit des **couloirs longs et sinueux** avec peu de culs-de-sac, ce qui donne des labyrinthes naturels et challengeants.
- Il est **simple à comprendre et à implémenter**.
- Sa forme itérative avec pile explicite évite les limites de récursion de Python, même pour de grands labyrinthes.

---

## Parties réutilisables

| Module | Rôle | Comment réutiliser |
|--------|------|--------------------|
| `src/maze.py` | Structures `Cell` et `Maze` avec représentation bitmask des murs | Importer `Maze` et `Cell` pour tout projet nécessitant un modèle de grille |
| `src/generate.py` | `generate_maze(maze, seed, perfect)` | Appeler avec n'importe quelle instance `Maze` pour la peupler |
| `src/solve.py` | `solve(maze)` → chaîne de directions, `solve_cells(maze)` → liste de `(x, y)` | Solveur BFS clé en main, fonctionne sur n'importe quelle instance `Maze` |
| `src/parse_config.py` | `parse_config(path)` → dict de config validé | Chargeur de config réutilisable pour tout projet au format `CLÉ=VALEUR` |
| `src/color.py` | `ColorManager` avec cycle de couleurs | Gestionnaire d'état de couleur réutilisable pour tout projet de dessin pixel |

---

## Équipe et gestion de projet

### Rôles

| Membre | Rôle |
|--------|------|
| **egaudich** | Rendu graphique — intégration MiniLibX, dessin pixel, contrôles UI, gestion des couleurs, animation du chemin |
| **malanos** | Cœur algorithmique — génération DFS, résolution BFS, parsing de config, format du fichier de sortie |

### Planning et déroulement

Dès le départ, le projet a été divisé en deux axes parallèles : un membre sur le modèle de données et les algorithmes, l'autre sur la couche d'affichage. Cette séparation a bien fonctionné car l'objet `Maze` a servi d'interface claire entre les deux côtés, sans couplage fort.

L'intégration (brancher le générateur dans l'affichage, gérer la régénération avec une nouvelle graine) a nécessité quelques échanges, mais s'est faite sans difficulté majeure une fois l'API stabilisée.

**Ce qui a bien marché :**
- La séparation nette entre logique et affichage dès le début.
- La représentation bitmask des murs, compacte et rapide à manipuler.
- L'intégration du motif "42" en pré-traitement, ce qui n'a pas nécessité de modifier le cœur du DFS.

**Ce qui pourrait être amélioré :**
- La vitesse d'animation du chemin est codée en dur (`PATH_SPEED = 1`) ; elle pourrait être rendue configurable.
- Les bindings Python de MiniLibX nécessitent une compilation manuelle (`make -C mlx_CLXV`), une étape d'installation plus automatisée améliorerait l'expérience.

### Outils utilisés

- **Python 3** — langage principal
- **MiniLibX** — bibliothèque graphique bas niveau (rendu pixel)
- **flake8** — linting
- **mypy** — vérification de types statique
- **make** — automatisation du build

---

## Ressources

- [BFS — Breadth-First Search (Wikipedia)](https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_largeur)
- [Documentation MiniLibX](https://harm-smits.github.io/42docs/libs/minilibx)

### Utilisation de l'IA

L'IA a été utilisée pour la **compréhension** — clarifier le fonctionnement conceptuel des algorithmes DFS Backtracker et BFS, ainsi que la représentation bitmask des murs. Aucun code n'a été généré directement par l'IA.
