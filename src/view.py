import tkinter as tk
from tkinter import Canvas
import math

# Classe
class MetroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carte du métro de Paris - PPC")
        self.root.geometry("1600x900")

        self.stations_positions = []
        self.canvas = Canvas(self.root, width=1000, height=1000, bg="beige")

    def lire_positions(self):
        with open("../pospoints.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                x, y, nom = int(parts[0]), int(parts[1]), parts[2].replace("@", " ")
                self.stations_positions.append((x, y, nom))
    
    

# Fonction principale
root = tk.Tk()
app = MetroApp(root)
root.mainloop()