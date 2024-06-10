import pyautogui
import tkinter as tk
import csv

def update_coordinates():
    # Obtient les coordonnées x, y de la souris
    x, y = pyautogui.position()
    # Met à jour le texte dans la fenêtre
    coordinates_label.config(text=f"Coordonnées de la souris : X = {x}, Y = {y}")
    # Déplace le cercle à la position y
    canvas.coords(marker, 0, y - 7.5, 15, y + 7.5)
    # Programme une mise à jour toutes les 100 millisecondes
    coordinates_label.after(100, update_coordinates)

def main():
    # Crée la fenêtre
    window = tk.Tk()
    window.title("Coordonnées de la souris")
    # Définit la taille de la fenêtre
    window.geometry("30x2000")  # Ajuste la taille pour accueillir les graduations

    # Crée un canevas pour dessiner la marque
    global canvas
    canvas = tk.Canvas(window, width=30, height=2000)
    canvas.pack()

    # Crée une étiquette pour afficher les coordonnées
    global coordinates_label
    coordinates_label = tk.Label(window, text="")
    coordinates_label.pack(padx=10, pady=10)

    # Dessine les graduations tous les 100 pixels
    for i in range(0, 2000, 100):
        canvas.create_line(15, i, 30, i, fill="black")
        canvas.create_text(10, i, anchor="e", text=str(i))

    # Dessine la marque initiale au milieu du canevas
    global marker
    marker = canvas.create_oval(0, 992.5, 15, 1007.5, fill="red")  # Dessine un cercle plein avec un rayon de 7.5 autour de la position Y initiale

    # Lance la mise à jour des coordonnées
    update_coordinates()

    # Démarre la boucle principale de l'interface graphique
    window.mainloop()

if __name__ == "__main__":
    main()
