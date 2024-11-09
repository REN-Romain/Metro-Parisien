from algo import *

# Test ouverture d'un graphe 
file = open("project_file/metro.txt", "r")
graphe, stations = getGraphe(file)
print()
print("Voici le graphe stocké dans un dictionnaire : -------------------------------------")
print(graphe)

# Test connexité d'un graphe
file = open("project_file/metro.txt", "r")
print()
print("Voici le test de connexité du graphe : ")
if (isConnexe(graphe)):
    print("Le graphe est connexe")
else :
    print("Erreur : Le graphe n'est pas connexe")
    
# Test algorithme de Bellman-Ford

# Test algorithme de Prim
print()
print("Voici le test l'algorithme de Prim : ---------------------------------------------")
print(arbreCouvrant(graphe))

print()
print("Voici le test de l'algorithme de Bellman-Ford")
print(bellmanFord(graphe, "Carrefour Pleyel", "Villejuif, P. Vaillant Couturier", stations))
