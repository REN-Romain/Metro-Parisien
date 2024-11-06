import re # Librairie d'expressions régulières

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
    
    return graphe


# Fonction pour déterminser si le graphe est connexe (Parcours en largeur)
def isConnexe(graphe):
    debut = next(iter(graphe)) # choix d'un sommet arbitraire
    file = [debut] # file des éléments visités
    parcours = [debut] # liste des sommets visités

    while file:
        noeud = file.pop(0) # en enlève l'élément en tête de file 

        # parcours des voisins
        for v, _ in graphe[noeud]:
            if v not in parcours: # si on n'a pas encore visité le sommet 
                parcours.append(v)
                file.append(v)

    return len(parcours) == len(graphe)

# recherche du plus court chemin (bellman-ford)
def bellman_ford(graph, start, end):
    # Initialize distances from the start vertex to all other vertices as infinity
    distances = {node: float('inf') for node in graph}
    distances[start] = 0  # Distance to the start vertex is 0
    predecessors = {node: None for node in graph}

    # Relax edges repeatedly
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    predecessors[neighbor] = node

    # Check for negative weight cycles
    for node in graph:
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative weight cycle")

    # Reconstruct the shortest path from start to end
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]

    if distances[end] == float('inf'):
        return None, float('inf')

    return path, distances[end]

# recherche de l'arbre couvrant de poids minimum
def arbreCouvrant(graphe):
    debut = next(iter(graphe)) # choix arbitraire du départ 

    # initialisations
    arbre = [] # liste des arêtes de l'arbre couvrant minimal
    visites = set([debut])
    aretes = [(poids, debut, voisin) for voisin, poids in graphe[debut]]

    while aretes:
        aretes.sort() # on trie d'abord les arêtes dans l'ordre croissant 
        poids, u, v = aretes.pop(0) # on choisit l'arpete de plus petit poids 

        if v not in visites: # si le sommet n'a pas encore été visité, on l'ajoute dans l'arbre
            arbre.append((u, v, poids))  
            visites.add(v)

            for voisin, poids_voisin in graphe[v]: # on rajoute les nouveaux sommets à vérifier (voisin du sommet visité )
                if voisin not in visites:
                    aretes.append((poids_voisin, v, voisin))
    
    return arbre 