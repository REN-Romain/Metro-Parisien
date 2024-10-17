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

# Création et paramètrage de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Metro Parisien")
fenetre.geometry("800x800")

label = tk.Label(fenetre, text="Hello World")
label.pack()

fenetre.mainloop()