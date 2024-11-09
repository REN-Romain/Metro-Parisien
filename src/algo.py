import re # Librairie d'expressions régulières
import math # Librairie permettant certaines fonctions de calculs mathématiques
import heapq  # Librairie pour les tas de priorité (min-heap)

# Fonction pour obtenir un graphe depuis le fichier test 
def getGraphe(file):
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
            stations.append([int(v[0]), v[1][:-1], v[2], v[3], int(v[4])]) # n° de station, nom, ligne de métro, terminus, n° de branchement 

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
    
    return graphe, stations


# Fonction pour déterminser si le graphe est connexe (Parcours en largeur)
def isConnexe(graphe):
    debut = next(iter(graphe)) # choix d'un sommet arbitraire
    file = [debut] # file des éléments à visités
    parcours = [debut] # liste des sommets visités

    while file:
        noeud = file.pop(0) # en enlève l'élément en tête de file 

        # parcours des voisins
        for v, _ in graphe[noeud]:
            if v not in parcours: # si on n'a pas encore visité le sommet 
                parcours.append(v)
                file.append(v)

    return len(parcours) == len(graphe)

# Rercherche du plus court chemin (bellman-ford)
def bellmanFord(graph, station_debut, station_fin, stations):
    debut = None
    fin = None
    for i in range(len(stations)):
        if (stations[i][1] == station_debut):
            debut = stations[i][0]
        elif (stations[i][1] == station_fin):
            fin = stations[i][0]
    
    if (debut == None or fin == None):
        print("Erreur : Nom de station inexistant")
        return None
        
    # Initialise les distances
    distances = {noeud: float('inf') for noeud in graph}
    distances[debut] = 0  
    predecesseurs = {noeud: None for noeud in graph}

    for i in range(len(graph) - 1):
        for noeud in graph:
            for voisin, poids in graph[noeud]:
                if distances[noeud] + poids < distances[voisin]:
                    distances[voisin] = distances[noeud] + poids
                    predecesseurs[voisin] = noeud

    # Construit le chemin le plus court
    chemin = []
    station_actuel = fin
    while station_actuel is not None:
        chemin.insert(0, station_actuel)
        station_actuel = predecesseurs[station_actuel]
    
    station_precedente = None
    print("Le chemin le plus court est : ")
    for i in range(len(chemin)):
        if (stations[chemin[i]][1] == station_precedente):
            print("Changement de ligne " + stations[chemin[i]][2] + " : " +stations[chemin[i]][1])
        else : 
            print(stations[chemin[i]][2] + " : " +stations[chemin[i]][1])
        station_precedente = stations[chemin[i]][1]
    print("La distance totale est : ", distances[fin]//60, " minutes et" , distances[fin]%60, "secondes.")

    return chemin, distances[fin]

def arbreCouvrant(graphe, stations):
    # Choix arbitraire du départ (un sommet de l'arbre)
    debut = next(iter(graphe))  # Choisir un sommet arbitraire

    # Initialisations
    arbre = []  # Liste des arêtes de l'arbre couvrant minimal
    visites = set([debut])  # Ensemble des sommets visités
    aretes = []  # Liste des arêtes à examiner, sous forme de tas de priorité

    # Ajoute les arêtes du sommet de départ dans le tas
    for voisin, poids in graphe[debut]:
        heapq.heappush(aretes, (poids, debut, voisin))  # heapq permet de maintenir l'ordre par poids

    while aretes:
        # On extrait l'arête ayant le poids minimal
        poids, u, v = heapq.heappop(aretes)

        # Si le sommet v n'a pas été visité, on l'ajoute dans l'arbre
        if v not in visites:
            arbre.append((u, v, poids))  # On ajoute l'arête à l'arbre
            visites.add(v)

            # On ajoute toutes les arêtes sortant de v dans le tas
            for voisin, poids_voisin in graphe[v]:
                if voisin not in visites:
                    heapq.heappush(aretes, (poids_voisin, v, voisin))

    # Conversion de l'arbre en chemin de stations avec distances (uniquement les identifiants)
    chemin = []
    total_distance = 0

    # Pour chaque arête de l'arbre, reconstruire le chemin de stations
    for u, v, poids in arbre:
        chemin.append(u)
        chemin.append(v)
        total_distance += poids

    # Suppression des doublons de stations consécutives dans le chemin
    chemin = [chemin[0]] + [chemin[i] for i in range(1, len(chemin)) if chemin[i] != chemin[i - 1]]

    return chemin, total_distance


