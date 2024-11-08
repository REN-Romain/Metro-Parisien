import tkinter as tk
from tkinter import Canvas
import math
from algo import *
from PIL import Image, ImageTk  # Requires Pillow library

class MetroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carte du métro de Paris")

        # Charger l'image de fond de la carte du métro
        self.metro_image = Image.open("project_file/metrof_r.png")
        self.image_width, self.image_height = self.metro_image.size  # Get the original size of the image
        self.metro_photo = ImageTk.PhotoImage(self.metro_image)

        # Set the window size to match the image size
        self.root.geometry(f"{self.image_width}x{self.image_height}")

        # Prevent the window from being resized
        self.root.resizable(False, False)

        # Liste des stations et leurs positions
        self.stations_positions = []

        # Canvas pour afficher le fond et les lignes de métro
        self.canvas = Canvas(self.root, width=self.image_width, height=self.image_height, bg="beige")
        self.canvas.pack()

        # Afficher l'image de fond
        self.canvas.create_image(0, 0, anchor="nw", image=self.metro_photo)

        # Ajouter un bouton pour réinitialiser la sélection des stations
        self.reset_button = tk.Button(self.root, text="Réinitialiser", command=self.reinitialiser)
        self.reset_button.pack(pady=10)

        # Ajouter une étiquette pour afficher des messages
        self.message_label = tk.Label(self.root, text="Cliquez sur deux stations pour définir un parcours", font=("Arial", 12))
        self.message_label.pack(pady=20)

        # Liaison pour la gestion des clics
        self.canvas.bind("<Button-1>", self.gestionClic)

        # Initialiser les variables
        self.station_depart = None
        self.station_arrivee = None
        self.graphe = None
        self.stations = None
        self.lines = []  

    def lirePositions(self):
        """Lit les positions des stations à partir d'un fichier .txt et les stocke dans une liste."""
        with open("project_file/pospoints.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                x, y, nom = int(parts[0]), int(parts[1]), parts[2].replace("@", " ")
                self.stations_positions.append((x, y, nom))

    def getStation(self, x, y, seuil=15):
        """Retourne le nom de la station la plus proche des coordonnées cliquées, si elle est dans un rayon donné."""
        station_proche = None
        distance_min = float('inf')

        # Loop over the stations positions and find the nearest station
        for station_x, station_y, nom in self.stations_positions:
            distance = math.sqrt((station_x - x) ** 2 + (station_y - y) ** 2)
            if distance < distance_min:
                distance_min = distance
                station_proche = nom.strip()  # Standardize the name

        if station_proche is not None and distance_min <= seuil:
            print(f"Station sélectionnée: {station_proche}")
            return station_proche  # Return the name of the closest station
        else:
            print("Aucune station trouvée proche du clic.")
            return None

    def getCoordonnees(self, id):
        """Retourne les coordonnées d'une station en fonction de son identifiant."""
        for station in self.stations:
            for station_pos in self.stations_positions:
                if station[1] == station_pos[2] and station[0] == id:
                    return (station_pos[0], station_pos[1])
        return None

    def afficherParcours(self, parcours):
        """Affiche le chemin le plus court entre deux stations."""
        for i in range(len(parcours) - 1):
            # Get coordinates for the current and next station
            coord1 = self.getCoordonnees(parcours[i])
            coord2 = self.getCoordonnees(parcours[i + 1])

            # Check if both coordinates are valid
            if coord1 is not None and coord2 is not None:
                x1, y1 = coord1
                x2, y2 = coord2
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
            else:
                print(f"Erreur : Impossible de trouver les coordonnées pour {parcours[i]} ou {parcours[i + 1]}")

    def clearLines(self):
        """Clear the previously drawn lines (path) from the canvas."""
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()  # Reset the list of lines

    def gestionClic(self, clic):
        """Gestion des clics pour sélectionner les stations de départ et d'arrivée, et calculer le chemin."""
        x, y = clic.x, clic.y
        station_id = self.getStation(x, y)
        print("-----", station_id)
        if not station_id:
            print("Aucune station trouvée proche du clic.")
            return

        # Définir la station de départ
        if self.station_depart is None:
            self.station_depart = station_id
            print(f"Station de départ sélectionnée : {self.station_depart}")
            self.message_label.config(text=f"Station de départ: {self.station_depart}")
        # Définir la station d'arrivée et calculer le chemin
        elif self.station_arrivee is None:
            self.station_arrivee = station_id
            print(f"Station d'arrivée sélectionnée : {self.station_arrivee}")
            self.message_label.config(text=f"Station d'arrivée: {self.station_arrivee}")

            # Calcul du plus court chemin
            parcours, distance = bellmanFord(self.graphe, self.station_depart, self.station_arrivee, self.stations)
            if parcours:
                print(f"Chemin trouvé entre {self.station_depart} et {self.station_arrivee}")
                self.afficherParcours(parcours)
                print(f"Distance totale : {distance}")
                self.message_label.config(text=f"Distance totale: {distance}")
            else:
                self.message_label.config(text="Aucun chemin trouvé")

            # Réinitialiser les stations pour permettre une nouvelle sélection
            self.station_depart = None
            self.station_arrivee = None

    def reinitialiser(self):
        """Réinitialiser les stations de départ et d'arrivée."""
        self.station_depart = None
        self.station_arrivee = None
        self.message_label.config(text="Cliquez sur deux stations pour définir un parcours")

# Fonction principale
root = tk.Tk()
app = MetroApp(root)

# Charger les positions et le graphe
app.lirePositions()
with open("project_file/metro.txt", "r") as f:  # Assume que le fichier des stations est dans metro.txt
    app.graphe, app.stations = getGraphe(f)

root.mainloop()
