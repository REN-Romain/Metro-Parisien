from algo import *

# test ouverture d'un graphe 
file = open("project_file/metro.txt", "r")
graphe = getGraphe(file)
print(graphe)

# test connexité d'un graphe
file = open("project_file/metro.txt", "r")
print(isConnexe(graphe))

# test algorithme de prim
print(arbreCouvrant(graphe))
