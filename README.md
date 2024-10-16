# 🚇 Vas-y dans le Métro — Paris Subway Route Finder

## Contexte du Projet

Ce projet a été réalisé dans le cadre du cours **Théorie des Graphes** à Efrei Paris. Il s'agit d'une application pratique de la théorie des graphes appliquée au réseau du métro parisien. Le programme permet de vérifier la connexité du réseau, de calculer le plus court chemin entre deux stations, et d'extraire l'Arbre couvrant de poids minimum (ACPM) en utilisant des algorithmes bien connus tels que Bellman-Ford et Prim.

---

## Fonctionnalités

### 1. Vérification de la Connexité
Le réseau est modélisé sous forme d'un graphe non orienté à partir des données fournies dans le fichier `metro.txt`. Notre programme vérifie que le graphe est **connexe**, c'est-à-dire qu'il est possible d'aller de n'importe quelle station à une autre. Si des liaisons manquent, le programme les ajoutera automatiquement afin d'assurer la connexité complète du réseau.

### 2. Calcul du Plus Court Chemin (PCC)
Grâce à l'algorithme de Bellman-Ford, notre programme permet à l'utilisateur de trouver le **meilleur itinéraire** entre deux stations du métro. En entrant une station de départ et une station d'arrivée, le programme affiche :
- Les lignes de métro à emprunter.
- Les changements de lignes à effectuer.
- La durée estimée du trajet.

### 3. Extraction de l'Arbre Couvrant de Poids Minimum (ACPM)
Utilisant l'algorithme de Prim, notre programme extrait et affiche l'**Arbre couvrant minimal** du réseau. Cela permet d'obtenir une vue optimisée des connexions minimales nécessaires pour relier toutes les stations.

---

## Bonus

### 🎨 Interface Graphique (Optionnel)
Pour améliorer l'expérience utilisateur, nous avons inclus une fonctionnalité bonus :
- Une **carte interactive** du métro parisien qui permet à l'utilisateur de cliquer sur les stations de départ et d'arrivée. Le plus court chemin s'affiche visuellement sur le plan du métro, avec la durée du trajet.
- De plus, l'ACPM peut être affiché directement sur la carte, permettant une visualisation dynamique de l'arbre couvrant minimal.

---

## Structure du Projet

- `metro.txt` : Fichier contenant les données du réseau de métro sous forme de graphe.
- `pospoints.txt` : Coordonnées des stations sur la carte.
- `metrofr.png` : Image du plan du métro parisien.
- `src/` : Répertoire contenant le code source du projet.
- `README.md` : Ce fichier de présentation du projet.
- `rapport.pdf` : Rapport décrivant les algorithmes et structures de données utilisés (inclus dans la soumission finale).
- `Makefile` ou `script.sh` : Permet de lancer le programme.

---

## Prérequis

- **Python**
- Bibliothèques nécessaires pour Python (si utilisé) : 
  - `matplotlib` pour l'affichage des graphiques
  - `Tkinter` ou autre bibliothèque graphique pour l'interface utilisateur

### Installation

1. Clonez le repository GitHub :
   ```bash
   git clone https://github.com/username/metro-graph-project.git
   cd metro-graph-project
   ```

2. Installez les dépendances Python (si applicable) :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancer le programme :
   ```bash
   python main.py
   ```

---

## Utilisation

### Vérification de la Connexité
Le programme s'assure que le graphe du métro est connexe. Si des liaisons sont manquantes, elles seront ajoutées automatiquement. Vous pouvez visualiser les modifications directement dans la sortie du programme.

### Calcul du Plus Court Chemin (PCC)
Entrez la station de départ et la station de destination pour obtenir l'itinéraire le plus court. Le programme vous indiquera :
- Les lignes à emprunter.
- Les stations où changer de ligne.
- Le temps estimé du trajet.

### Extraction de l'Arbre Couvrant (ACPM)
Lancez l'extraction de l'arbre couvrant minimal et observez les connexions minimales du réseau via l'algorithme de Prim.

---

## Exemple d'Exécution

```bash
> Entrez la station de départ : Carrefour Pleyel
> Entrez la station de destination : Villejuif, P. Vaillant Couturier

- Vous êtes à Carrefour Pleyel.
- Prenez la ligne 13 direction Châtillon-Montrouge.
- À Champs-Élysées Clémenceau, changez pour la ligne 1 direction Château de Vincennes.
- À Palais Royal - Musée du Louvre, changez pour la ligne 7 direction Villejuif - Louis Aragon.
- Vous arriverez à Villejuif, P. Vaillant Couturier dans environ 29 minutes.
```

---

## Algorithmes Utilisés

- **Bellman-Ford** : Pour calculer le plus court chemin entre deux stations, en prenant en compte la possibilité de cycles négatifs (même si ici, cela n'est pas applicable au métro).
- **Prim** : Pour extraire l'Arbre couvrant minimal du graphe du métro.

---

## Auteurs

- Maeva RAMAHATAFANDRY
- Romain REN

---

## Remarques

- Le fichier `metro.txt` peut contenir des doublons de certaines stations. Cela représente des **correspondances** où une même station est sur plusieurs lignes.
- Ce projet utilise des données du métro parisien de 1998 à 2002. Certaines stations plus récentes peuvent ne pas être incluses dans les données.

---

## Licence

Ce projet est sous licence MIT. Vous êtes libre de le réutiliser et de l'améliorer.

---

## Bon Courage ! 👾
