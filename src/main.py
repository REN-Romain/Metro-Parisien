import tkinter as tk
from tkinter import Canvas
import math
from algo import *
from PIL import Image, ImageTk  # nécessite la librairie Pillow

class MetroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carte du métro de Paris")

        # image de fond de la carte du métro
        self.metro_image = Image.open("project_file/metrof_r.png")
        
        # appliquer un redimensionnement de l'image à 90%
        self.image_width, self.image_height = self.metro_image.size
        self.image_width = int(self.image_width)
        self.image_height = int(self.image_height)
        
        # redimensionner l'image
        self.metro_image = self.metro_image.resize((self.image_width, self.image_height))
        self.metro_photo = ImageTk.PhotoImage(self.metro_image)

        # taille de la fenêtre ajustée pour correspondre à l'image redimensionnée
        self.root.geometry(f"{self.image_width}x{self.image_height + 50}")  # +50 pour la zone des boutons
        # désactivation de la redimension de la fenêtre
        self.root.resizable(False, False)

        # dictionnaire pour les positions des stations et leurs marqueurs graphiques
        self.stations_positions = []
        self.station_markers = {}  # clé : nom de la station, valeur : ID du cercle sur le canvas

        # canvas pour afficher le fond et les lignes de métro
        self.canvas = Canvas(self.root, width=self.image_width, height=self.image_height, bg="beige")
        self.canvas.pack()

        # affichage de l'image de fond redimensionnée
        self.canvas.create_image(0, 0, anchor="nw", image=self.metro_photo)

        # Frame pour le bouton et les messages (modifié pour le placer en haut)
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side="top", pady=10)  # Le frame est maintenant en haut

        # bouton pour afficher l'ACPM (modifié pour qu'il reste à gauche dans la frame en haut)
        self.acpm_button = tk.Button(self.control_frame, text="Afficher l'ACPM", command=self.afficherACPM)
        self.acpm_button.pack(side="top", pady=5)  # Le bouton est maintenant en haut du frame

        # bouton pour réinitialiser la sélection des stations
        self.reset_button = tk.Button(self.control_frame, text="Réinitialiser", command=self.reinitialiser)
        self.reset_button.pack(side="top", padx=10, pady=5)

        # étiquette pour afficher des messages
        self.message_label = tk.Label(self.control_frame, text="Cliquez sur deux stations pour définir un parcours", font=("Arial", 12))
        self.message_label.pack(side="top", pady=5)

        # liaison pour la gestion des clics
        self.canvas.bind("<Button-1>", self.gestionClic)

        # variables initiales
        self.station_depart = None
        self.station_arrivee = None
        self.graphe = None
        self.stations = None
        self.lines = []  # liste pour les lignes dessinées


    def lirePositions(self):
        """lecture des positions des stations à partir d'un fichier .txt et ajout de marqueurs bleus pour chaque station"""
        with open("project_file/pospoints.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                x, y, nom = int(parts[0]), int(parts[1]), parts[2].replace("@", " ")
                self.stations_positions.append((x, y, nom))
                
                # ajouter un marqueur bleu pour la station
                marker = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", outline="")
                self.station_markers[nom] = marker  # enregistrer le marqueur avec le nom de la station

    def getStation(self, x, y, seuil=15):
        """nom de la station la plus proche des coordonnées cliquées, si elle est dans un rayon donné"""
        station_proche = None
        distance_min = float('inf')

        # recherche de la station la plus proche
        for station_x, station_y, nom in self.stations_positions:
            distance = math.sqrt((station_x - x) ** 2 + (station_y - y) ** 2)
            if distance < distance_min:
                distance_min = distance
                station_proche = nom.strip()  # nom standardisé

        if station_proche is not None and distance_min <= seuil:
            print(f"Station sélectionnée: {station_proche}")
            return station_proche  # retour du nom de la station la plus proche
        else:
            print("Aucune station trouvée proche du clic.")
            return None

    def getCoordonnees(self, id):
        """coordonnées d'une station en fonction de son identifiant"""
        for station in self.stations:
            for station_pos in self.stations_positions:
                if station[1] == station_pos[2] and station[0] == id:
                    return (station_pos[0], station_pos[1])
        return None

    def afficherParcours(self, parcours):
        """affichage du chemin le plus court entre deux stations"""
        for i in range(len(parcours) - 1):
            # coordonnées des stations actuelles et suivantes
            coord1 = self.getCoordonnees(parcours[i])
            coord2 = self.getCoordonnees(parcours[i + 1])

            # vérification de la validité des coordonnées
            if coord1 is not None and coord2 is not None:
                x1, y1 = coord1
                x2, y2 = coord2
                # dessin de la ligne et ajout dans la liste des lignes
                line = self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
                self.lines.append(line)  # stockage de la ligne dans self.lines pour la réinitialisation
            else:
                print(f"Erreur : Impossible de trouver les coordonnées pour {parcours[i]} ou {parcours[i + 1]}")

    def clearLines(self):
        """effacement des lignes précédemment dessinées (chemin) sur le canvas"""
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()  # réinitialisation de la liste des lignes

    def gestionClic(self, clic):
        """gestion des clics pour sélectionner les stations de départ et d'arrivée, et calculer le chemin"""
        x, y = clic.x, clic.y
        station_id = self.getStation(x, y)
        print("-----", station_id)
        if not station_id:
            print("Aucune station trouvée proche du clic.")
            return

        # définition de la station de départ
        if self.station_depart is None:
            self.station_depart = station_id
            print(f"Station de départ sélectionnée : {self.station_depart}")
            self.message_label.config(text=f"Station de départ: {self.station_depart}")
            # changer le marqueur de la station en rouge
            self.canvas.itemconfig(self.station_markers[self.station_depart], fill="red")
        # définition de la station d'arrivée et calcul du chemin
        elif self.station_arrivee is None:
            self.station_arrivee = station_id
            print(f"Station d'arrivée sélectionnée : {self.station_arrivee}")
            self.message_label.config(text=f"Station d'arrivée: {self.station_arrivee}")

            # changer le marqueur de la station en rouge
            self.canvas.itemconfig(self.station_markers[self.station_arrivee], fill="red")

            # effacer le chemin précédent
            self.clearLines()

            # calcul du plus court chemin
            parcours, distance = bellmanFord(self.graphe, self.station_depart, self.station_arrivee, self.stations)
            if parcours:
                print(f"Chemin trouvé entre {self.station_depart} et {self.station_arrivee}")
                self.afficherParcours(parcours)
                print(f"Distance totale : {distance}")
                self.message_label.config(text=f"Distance totale: {distance}")
            else:
                self.message_label.config(text="Aucun chemin trouvé")

            # remettre les marqueurs des stations de départ et d'arrivée en bleu
            self.canvas.itemconfig(self.station_markers[self.station_depart], fill="blue")
            self.canvas.itemconfig(self.station_markers[self.station_arrivee], fill="blue")

            # réinitialisation des stations pour permettre une nouvelle sélection
            self.station_depart = None
            self.station_arrivee = None

    def afficherACPM(self):
        """Calcul et affichage de l'ACPM (Arbre de Couverture de Poids Minimal)"""
        # Remplacer cette ligne par le calcul de l'ACPM
        acpm_parcours, _ = arbreCouvrant(self.graphe, self.stations)  # Utilise l'algorithme de Prim
        if acpm_parcours:
            print("ACPM calculé avec succès")
            self.afficherParcours(acpm_parcours)
        else:
            print("Erreur dans le calcul de l'ACPM")

    def reinitialiser(self):
        """réinitialisation des stations de départ et d'arrivée"""
        self.clearLines()  # effacement des lignes affichées
        self.station_depart = None
        self.station_arrivee = None
        # réinitialiser les marqueurs en bleu
        for marker in self.station_markers.values():
            self.canvas.itemconfig(marker, fill="blue")
        self.message_label.config(text="Cliquez sur deux stations pour définir un parcours")


# fonction principale
root = tk.Tk()
app = MetroApp(root)

# chargement des positions et du graphe
app.lirePositions()
with open("project_file/metro.txt", "r") as f:  # fichier des stations dans metro.txt
    app.graphe, app.stations = getGraphe(f)

root.mainloop()