import re
file = open("../project_file/metro.txt", "r")

stations =  []
aretes = []

vertex_regex = r"V (\d{4}) (.*?);(\d+|[0-9bis]+) ;(True|False) (\d)"
edge_regex = r"E (\d+) (\d+) (\d+)"

for line in file:
    vertices = re.findall(vertex_regex, line)
    for v in vertices:
        stations.append([int(v[0]), v[1], v[2], v[3], int(v[4])])

    edges = re.findall(edge_regex, line)
    for e in edges:
        aretes.append([int(e[0]), int(e[1]), int(e[2])])

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

print(graphe)

file.close()