# Import des librairies utilisées
import re # Librairie d'expressions régulières
import tkinter as tk # Librairie de l'interface graphique

# Lecture du fichier metro.txt
file = open("../project_file/metro.txt", "r")

# Initialisation des listes contenant les stations et les arcs
stations =  []
aretes = []

# Initialisation des expressions régulières utilisées pour récupérer les valeurs dans metro.txt
vertex_regex = r"V (\d{4}) (.*?);(\d+|[0-9bis]+) ;(True|False) (\d)"
edge_regex = r"E (\d+) (\d+) (\d+)"

# Récupération des valeurs et ajout dans les listes stations et aretes
for line in file:
    vertices = re.findall(vertex_regex, line)
    for v in vertices:
        stations.append([int(v[0]), v[1], v[2], v[3], int(v[4])])

    edges = re.findall(edge_regex, line)
    for e in edges:
        aretes.append([int(e[0]), int(e[1]), int(e[2])])

# Initialisation d'un dictionnaire graphe contenant les stations reliées entre elles
graphe = {}
for i in range(len(aretes)):
    if aretes[i][0] not in graphe:
        graphe[aretes[i][0]] = [(aretes[i][1], aretes[i][2])]
    else :
        graphe[aretes[i][0]].append((aretes[i][1], aretes[i][2]))
    if aretes[i][1] not in graphe:
        graphe[aretes[i][1]] = [(aretes[i][0], aretes[i][2])]
    else :
        graphe[aretes[i][1]].append((aretes[i][0], aretes[i][2]))

# Fermeture du fichier metro.txt
file.close()

def bellman_ford(graph, debut, fin):
    # Initialise les distances
    distances = {noeud: float('inf') for noeud in graph}
    distances[debut] = 0  # Distance to the debut vertex is 0
    predecessors = {noeud: None for noeud in graph}

    for _ in range(len(graph) - 1):
        for noeud in graph:
            for voisin, poids in graph[noeud]:
                if distances[noeud] + poids < distances[voisin]:
                    distances[voisin] = distances[noeud] + poids
                    predecessors[voisin] = noeud

    # Vérifie s'il y a des valeurs négatifs (Bellman-Ford)
    for noeud in graph:
        for voisin, poids in graph[noeud]:
            if distances[noeud] + poids < distances[voisin]:
                raise ValueError("Il y a une valeur négatif")

    # Construit le chemin le plus court
    chemin = []
    actuel = fin
    while actuel is not None:
        chemin.insert(0, actuel)
        actuel = predecessors[actuel]

    if distances[fin] == float('inf'):
        return None, float('inf')

    for i in range(len(chemin)):
        print(stations[chemin[i]][1], "" , chemin[i])
    return chemin, distances[fin]

# Example usage
debut_station = 48  # Replace with your debuting station
end_station = 365  # Replace with your destination station

chemin, distance = bellman_ford(graphe, debut_station, end_station)

"""print("Voici le chemin : ")
print(chemin)
print("Voici la distance : ")
print(distance)"""
file.close()
